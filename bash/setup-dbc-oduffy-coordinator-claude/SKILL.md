---
name: setup
description: "Install-chain step 5/5: verify the engine, finish install."
allowed-tools: ["Read", "Bash"]
argument-hint: "[--skip-dep-check --accept-missing-deps-risk]"
---

# /coordinator:setup

Chain-walker skill for coordinator-claude (chain position 5 of 5 — root of the OSS
plugin-adoption chain). Reads the install manifest, walks `direct_deps` (ONE hard entry — the
control-plane engine), and emits the chain-complete terminal banner once satisfied, or fails loud
with remediation if the engine is unresolvable. Does NOT replace `coordinator:install` (OSS plugin
bootstrap into `~/.claude/`) or `coordinator:repo-setup` (consumer-project first-time
scaffolding) — three distinct verbs; disambiguation rationale: wiki.

**`setup_skill` in the manifest is informational, not the dispatch primitive.** This skill uses
direct Bash calls, not subagent dispatch (the engine dependency self-confirms via
`claude_klabauter_seam_resolvable`).

**Registry-key resolution:** a dev-tree session resolves the engine via `repos.claude_klabauter` (in
`<settings-home>/machine-local/registry.local.toml`) /
`REPO_CLAUDE_KLABAUTER`; an OSS install resolves the same engine (published as `claude-klabauter`)
via `docs/install/AGENT.md`.

---

## Out-of-scope for all dispatched agents in this skill

DO NOT run `gh pr create`, `gh pr merge`, `git push origin main`, `gh release create`, or any `gh`
command mutating GitHub state beyond pushing the current branch. DO NOT commit to `main` directly.
Surface a needed merge to the EM instead of doing it.

- Writing outside `plugins/coordinator-claude/coordinator/`.
- Modifying `docs/install/agent-install-manifest.json` at runtime (static artifact, read-only here).
- Touching the DR, example-game-repo, ue-addon, or project-rag trees.
- Any `git commit` or `git push`.

---

## Step 1 — Detect layout

`PLUGIN_ROOT` is two levels up from this skill file (`coordinator/skills/setup/SKILL.md` →
`coordinator/`); resolve it relative to wherever this file lives on disk.

**On a PowerShell host, invoke the `.exe` launcher through the call operator** (Shape W) for every
`setup-verify` invocation on this page, never the `${...}` POSIX-shell form shown. Ladder and
shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

Run `& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" layout --plugin-root "<PLUGIN_ROOT>"` (Shape W; ladder and POSIX shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`).
Prints `Layout: <flat|nested>` and `Manifest path: <path>`; exits 1 with a "Manifest not found"
remediation if `docs/install/agent-install-manifest.json` is absent under the resolved repo root.
Surface an exit-1 error verbatim.

---

## Step 2 — Read the install manifest

Verify `${MANIFEST}` exists (error and exit if missing), then parse it. Extract:
`agent_install_contract_version` (must be 1, 2, or 3 — reject otherwise), `repo_id` (should be
`"coordinator-claude"`), `direct_deps` (the walk list — one hard entry), `override_flags` (the
consent-gate flag-pair names). On a JSON parse failure, surface the error and exit — do not
continue with a corrupt manifest.

---

## Step 3 — Initialise the visited-set

Disk-resident, for diamond-DAG and cycle detection:
`<settings-home>/coordinator-claude/chain-walk-<session-id>.json`, where `<settings-home>` is
resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape W on PowerShell hosts).

Run `& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" visited-init` (Shape W)
— generates a session id, prunes `chain-walk-*.json` files older than 60 minutes, writes the new
file with an empty `visited` array, prints `Session ID:` and `Visited-set:`.

---

## Step 4 — Walk direct_deps and resolve system prerequisites

Python is pre-verified (hard exit if absent — the sole hard gate on this path). Run
`python3 -m coordinator_core.ops.setup_chain_walker --coordinator-root "${CLAUDE_PLUGIN_ROOT}"`
(the engine resolves itself; no root variable to set). **Never the deprecated `setup.py`
forwarder.**

This calls `_co_run_prereq_gate post-consumer`, which emits one dep row (the engine, hard) and the
prereq probe rows (git, python, uv, gh, node, pwsh, ue, clone_auth, longpaths, git_lfs) at the
severities the Step 5 terminal report shows below.

Advisory failures print `[WARN]` to stderr and do not block exit 0. A missing/broken engine
dependency triggers the [FAIL] hard-fail path — exit 1 (`--preflight`/`--check`) or consent-gate
codes 90/91/92 (full install), remediation pointing at the engine-root resolver. Full
contract detail (severity taxonomy, consent-gate banner, exit codes): wiki.

**Read-only flags** (`--help`, `--version`, `--phase-list`, `--last-status`, `--check`) are
serviced before any dep-walking and do not trigger the override check.

**Override flags** — both must be passed TOGETHER: `--skip-dep-check` and
`--accept-missing-deps-risk`. Validate via
`& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" check-override-flags -- $args`
(Shape W)
— exits 93 when exactly one is present, 0 otherwise (printing which path applies). Passing only
one degrades most mutating coordinator operations (no bash fallback under the big-bang cutover);
both together bypass the consent gate.

---

## Step 5 — Terminal report

Report: header `## /coordinator:setup — chain step 5 of 5`; manifest path, contract version,
layout, session id; a prerequisite table (python hard — the sole hard gate; gh, node, git,
clone_auth, uv, pwsh, ue, longpaths, git_lfs advisory, WARN does not block); a dependency row
(the engine, hard, `claude_klabauter_seam_resolvable`, self-confirming); result line `coordinator
install-chain walker — chain step 5 of 5: all deps satisfied.` then `coordinator-claude install
chain complete.` Exit 0 (advisory WARN rows do not affect it).

---

## Step 6 — Live Claude-Code-integration validation

Asserts the plugin is running-in-Claude-Code, not just present on disk: plugin enabled in
`settings.json`/`enabledPlugins`; hooks registered and live at their expected paths; skill
discovery preconditions met (a representative skill file parses and has a `description:`).

### Restart-batch (emit before the per-item probe table)

Collect every **restart-gated** finding into one block, emitted only if non-empty: "The following
items require a Claude Code restart to take effect. Restart Claude Code NOW, then re-validate
(re-run /coordinator:setup)." then one `[restart-gated] <item>` line each.

### Restart discriminator

- **restart-gated-expected** — fails, no restart since the config write → restart-batch; not a
  hard failure.
- **configured-but-broken** — fails after a restart (or its settle window) → fail loud.
- **pending-settle** — fails within the settle window → re-probe once, then reclassify.

### Probes

Run via Bash. Resolve `PLUGIN_ROOT` per-probe if not already in scope (each probe must be
self-contained). Rationale for probe ordering and design: wiki.

**Probe 0 — Plugin reachable.**
`& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" check-plugin-registered --plugin coordinator --marketplace coordinator-claude --marketplace-source dbc-oduffy/coordinator-claude --plugin-dir "<PLUGIN_ROOT>"`
(Shape W).
Asserts reachability (marketplace registration OR live `--plugin-dir` resolution — `PASS
(live-resolved)`), not mere enablement. **Never restart-gated.**

**Probe 1 — Plugin enabled in settings.json.**
`& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" check-settings-membership --plugin-dir "<PLUGIN_ROOT>"`
(Shape W; optional `--settings <path>`, default `~/.claude/settings.json`).
Pass the same `<PLUGIN_ROOT>` Probe 0 got — omitting `--plugin-dir` FAILs a live-resolved install.
`PASS`/exit 0, `[WARN]`/exit 0 if settings.json missing/unparseable, `FAIL`/exit 1 otherwise. A
FAIL after a config write with no subsequent restart is restart-gated-expected; after a restart,
configured-but-broken.
**Probe 0 governs this one.** On `PASS (live-resolved)`, Probe 1 degrades to `[WARN]`/exit 0 —
absence from enabledPlugins is that shape's expected state.

**Probe 2 — Hooks registered and live on disk.**
`& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" check-hooks --plugin-root "<PLUGIN_ROOT>"`
(Shape W).
Parses `<PLUGIN_ROOT>/hooks/hooks.json`, verifies each coordinator-owned hook path exists on disk
(named lookup, not a blanket file count). `PASS`/exit 0, `FAIL` (lists missing paths)/exit 1,
`[WARN]` (hooks.json absent/unparseable, or no coordinator hooks)/exit 0. Absent from disk →
configured-but-broken; present but not yet loaded → restart-gated-expected.

**Probe 3 — Skill discovery preconditions.**
Use this skill itself as the representative: `<PLUGIN_ROOT>/skills/setup/SKILL.md`.
`& "$env:COORDINATOR_SETTINGS_HOME\bin\setup-verify.exe" check-skill-description --skill-file "<PLUGIN_ROOT>/skills/setup/SKILL.md"`
(Shape W).
`PASS`/exit 0, `FAIL` (missing file, no frontmatter, no/empty `description:`)/exit 1 — always
configured-but-broken, never restart-gated. Probe 1's WARN propagates here.

**Probe 4 — Windows launch shape (dogfood shape only).**
`python3 "<PLUGIN_ROOT>/bin/check-launch-shape.py"`.
Asserts the interactive `claude.exe` would be a DIRECT child of the invoking shell (no `claude-author`
shadowing the real launcher on PATH; shim and launcher shapes intact). `PASS`/exit 0, `FAIL`
(names the offender)/exit 1, `SKIP`/exit 0 on non-Windows or with no rendered launcher pair on
PATH. Always configured-but-broken on FAIL, **never restart-gated**.

### Validation summary table

```
### Step 6 — Live Claude-Code-integration validation (running-in-Claude-Code)

| Probe | Surface | Result | Classification |
|-------|---------|--------|----------------|
| Plugin reachable | marketplace registration OR `--plugin-dir` live resolution | PASS/FAIL | live / configured-but-broken (never restart-gated) |
| Plugin enabled | settings.json enabledPlugins | PASS/WARN/FAIL | live / restart-gated-expected or live-resolved (Probe 0 PASS) / configured-but-broken |
| Hooks live on disk | ~/.claude/hooks/ | PASS/WARN/FAIL | live / restart-gated-expected / configured-but-broken |
| Skill discovery preconditions | skills/setup/SKILL.md | PASS/WARN | live / configured-but-broken |
| Windows launch shape | PATH resolution of claude-author + rendered shim/launcher | PASS/FAIL/SKIP | live / configured-but-broken (never restart-gated) / not-this-shape |
```

### Exit-code semantics

`configured-but-broken` → `[ERROR]` to stderr, exit non-zero (the exception to the advisory-WARN
model). `restart-gated-expected` → WARN row and restart-batch, exit code unchanged. All PASS → exit 0.

---

## Negative-spec

<!-- negative-spec: this skill does NOT dispatch subagents (no recursive chain-walk; the visited-set is for contract-conformance only), does NOT replace coordinator:install or coordinator:repo-setup (it only asserts reachability via Probe 0), and does NOT seed install-leg spinoffs into the install-baton rendezvous (/spinoff only). -->
