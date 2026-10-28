---
name: pb-aos-e2e
description: >-
  AOS release E2E in a sandbox: install the packed tarball, verify
  doctor, gates, memB, hub, update, uninstall. Run before a release merge.
category: engineering-method
kind: playbook
trigger: ["aos e2e", "release e2e", "aos release check", "installer e2e", "e2e check aos"]
inputs: [repo_dir, "sandbox?", "with_update?"]
requires:
  skills: [pb-release-aos, pb-machine-setup, verification-before-completion, systematic-debugging, quick-recap, plan-canvas, agenttrail, gogate]
  agents: [reviewer]
  mcps: []
  tools: [npm, node, bash, docker, curl]
  store: []
go_points: [merge-release-pr, publish-release]
outputs: ["production_artifacts/pb-aos-e2e-<date>.md", "aos-e2e-output/summary.txt"]
verify: "Install from tarball exits 0 in a fresh HOME; aos doctor exits 0 with only optional warnings; go-gate registered in Claude, agy, Codex (OpenCode when detected) and the gate off/on round trip restores it; memB inject runs and returns a block; aos hub status answers; update keeps gate off off; uninstall leaves no AOS registration."
difficulty: advanced
est_time: 20-60 min
---

# AOS release E2E check in a clean sandbox

What you get: one automated pass over the whole install lifecycle of a packed AOS tarball inside a throwaway `HOME` — install, doctor, hook registration per harness, gate setting round trip, injected context budget, memB inject, hub, update and uninstall — with a pass/fail judgement per step and a summary file.

## Inputs
- repo_dir — the AOS repository or worktree to check (default: current directory)
- sandbox (optional) — where the fresh `HOME` lives; default: auto-detect (netcup runner, else Docker)
- with_update (optional) — `1` enables the update-from-previous-version step; it needs network access to the npm registry

## Sandbox: a fresh HOME, never the real one

The check must run against a throwaway `$HOME` inside a container, VM or dedicated test user — never the operator's real home. Pick the first available runner:

1. **netcup aos-ci runner (preferred):** `~/.aos/cloud-sandbox/scripts/aos-ci-run` with the worktree as its argument — passes the worktree to the cloud sandbox runner and runs the E2E script inside it. Unverified when the script is absent locally; skip to the next runner.
2. **Docker:** `docker run --rm -v "$PWD":/aos -w /aos node:24-bookworm bash scripts/e2e/aos-e2e.sh` — the script itself requires `AOS_TEST_SANDBOX=1` and creates its own fresh `HOME` with `mktemp -d`.
3. **Local dry shape (no container):** not allowed for the install/uninstall steps. `tests/installer-e2e.sh` shows the minimal shape; the E2E script refuses to run without `AOS_TEST_SANDBOX=1`.

## Steps

1. **Build the tarball** — `npm pack --pack-destination <out_dir>` in `repo_dir`:
   - Command: `npm pack --pack-destination aos-e2e-output`
   - Expected: one `aos-<version>.tgz` (package `@hybridlabor-api/aos`) and the `prepack` hash build from scripts/build-shipped-hashes.mjs exits 0.
   - Pass: a tarball path exists. Fail: npm errors or no tarball produced.
2. **Install from the tarball, non-interactive** — global install, then install into a fresh `HOME`:
   - Command: `npm install -g <tarball>` then `HOME=<sandbox_home> aos -y --profile standard --platforms=1,2,5` (1 = Antigravity, 2 = Claude, 5 = Codex; OpenCode is wired when its binary is detected).
   - Expected: exit 0; `~/.agents/.bdb-manifest.json` written; skills synced under `~/.claude/skills/`.
   - Pass: exit 0 and the manifest file exists. Fail: nonzero exit or missing manifest — read the installer output for the failed step.
3. **`aos doctor` all green except documented optional rows**:
   - Command: `HOME=<sandbox_home> aos doctor`
   - Expected: exit 0. Optional rows (`uv`, `gh`, `mcsc`, optional agy/Codex pieces) may print warnings; critical rows must not fail.
   - Pass: exit 0 (doctor exits 1 only on critical failures). Fail: exit 1 — treat every critical row it names as blocking.
4. **Hooks registered per harness, go-gate on**:
   - Command (file checks in the sandbox `HOME`):
     - Claude: `~/.claude/settings.json` registers `go-gate.mjs` (and `memb-inject.mjs`).
     - agy: `~/.gemini/config/hooks.json` contains the `aos-go-gate` hook.
     - Codex: `~/.codex/config.toml` references `go-gate.mjs`.
     - OpenCode: `~/.config/opencode/plugins/bdb-aos.js` exists — only when the `opencode` binary was detected; otherwise record `SKIP (opencode not detected)`.
     - Gate setting: `~/.aos/v5-settings.json` has no `"gate": "off"` (absent or `"on"` = on).
   - Pass: every detected harness shows its gate hook and the setting is on. Fail: a detected harness missing its hook.
5. **Settings gate toggle off/on round trip** (the `gate` setting, `lib/v5/profile.js` `GATE_HOOKS`):
   - Command: set `"gate": "off"` in `~/.aos/v5-settings.json`, run `HOME=<sandbox_home> aos repair -y --platforms=1,2,5`; then set `"gate": "on"` and repair again.
   - Expected: with the setting off, repair drops the gate hook registrations (go-gate, go-token, go-grant, graph-gate) from the harness configs while the script files stay on disk, and update/repair never re-enables a user-disabled gate; with it on, the hooks are registered again.
   - Pass: off → hook entries gone from `~/.claude/settings.json`; on → entries back. Fail: hooks still registered while off, or not restored while on.
6. **Fresh-session injected context stays under the profile caps**:
   - Command: `node scripts/measure-session-context.mjs` when the script exists in `repo_dir`; else record `SKIP (measure-session-context.mjs not present)`.
   - Expected: measured injected context per harness is at or under the profile caps for the standard profile.
   - Pass: at or under cap. Fail: over cap. Skip: script absent — note it in the summary.
7. **memB inject returns a block**:
   - Command: `echo '{}' | HOME=<sandbox_home> node ~/.claude/hooks/memb-inject.mjs` (hooks read Claude Code's JSON on stdin; `{}` is what the empty-input probe sends).
   - Expected: exit 0 and a non-empty injected block on stdout. On a fresh memory the block may legitimately be empty — record that as a note, not a failure, unless the hook exits nonzero.
   - Pass: exit 0. Fail: nonzero exit or a crash traceback.
8. **plan-canvas open + trail produce an agenttrail plan**:
   - Command: `aos-plan-canvas open <plan>`, then check the trail board shows the plan (`aos-trail`, or open the agenttrail board).
   - Expected: the canvas serves the plan in a browser and the trail lists it as a live plan.
   - Pass/fail: judge interactively — needs a browser and display. The E2E script records `SKIP (needs a browser)` here.
9. **Hub supervisor status**:
   - Command: `HOME=<sandbox_home> aos hub start` then `HOME=<sandbox_home> aos hub status --json`
   - Expected: status JSON answers with `ok: true` and `service: "aos-hub"`.
   - Pass: health probe ok. Fail: connection refused or `ok: false`.
10. **Update from the previous version keeps user settings** (needs `with_update=1` and network):
    - Command: install the previous published version (`npm install -g @hybridlabor-api/aos@latest`), set `"gate": "off"` in `~/.aos/v5-settings.json`, then `HOME=<sandbox_home> aos update -y`, then reinstall this build's tarball.
    - Expected: the update keeps `"gate": "off"` in the settings file and does not re-register the gate hooks (update/repair never re-enable a user-disabled gate).
    - Pass: setting still off and hooks stay unregistered. Fail: gate silently back on. Skip: no network or `with_update` unset — note it.
11. **[GO] Merge or publish the release** (`merge-release-pr`, `publish-release`): review the run log and every failed or skipped step before touching the release PR. The run stops here until the human types GO.
12. **Uninstall leaves no AOS registration**:
    - Command: `HOME=<sandbox_home> aos-uninstall --yes`, then check the sandbox `HOME`.
    - Expected: no `~/.agents/.bdb-install-manifest.json`, no `~/.agents/.bdb-uninstall-records.json`, no `~/.agents/bin/aos*.mjs` launchers, no `go-gate`/`memb-inject` entries left in `~/.claude/settings.json`, no `aos-go-gate` in `~/.gemini/config/hooks.json`, no OpenCode plugin file.
    - Pass: all absent. Fail: any AOS launcher or hook registration survives.

Run log: `production_artifacts/pb-aos-e2e-<date>.md` in the start directory, never committed; `aos-e2e-output/summary.txt` is written by the script into the directory it runs from.

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries beyond what a step names.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
- The install, update and uninstall steps touch a real `$HOME` shape; never point them at the operator's home. A blocked command is reported, never worked around.
