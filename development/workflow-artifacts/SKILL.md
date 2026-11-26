---
name: workflow-artifacts
description: Use to create, update, and read durable workflow state under .mtk/workflows/ so orchestration survives compaction, crash, and session handoff.
type: skill
license: MIT
compatibility:
  - claude-code
  - cursor
  - codex
user-invocable: false
---

# Workflow Artifacts

## Overview

Orchestration state that lives only in chat is lost on compaction or restart. This skill stores it on disk under `.mtk/workflows/{uuid}.json` plus an append-only event log, using a small bash helper. `implement` (a `BUILD` workflow) and `setup-audit` / `setup-bootstrap` create workflows; the skills `implement` composes (incremental- and subagent-implementation, verification, review) write to the active one at phase boundaries and gate decisions. `fix` and `batch-fix` do not create a workflow. The helper also accepts `DEBUG`, `REVIEW`, `PLAN` and `FIX` types, but no shipped skill initialises them today.

## When To Use

- At the start of every `/mtk implement` (BUILD) run, and of `setup-audit` / `setup-bootstrap`.
- At every phase transition inside `/mtk implement`.
- Whenever a named orchestration gate is evaluated (see `.claude/references/orchestration-gates.md`).
- When resuming after compaction, restart, or handoff — list active workflows before starting fresh work.

### When NOT To Use

- Throwaway exploration where no commit will happen.
- Single-turn read-only questions ("what does file X do?").
- Inside subagents — only the orchestrator (main implement loop) writes artifacts. Subagents return structured output; the orchestrator decides what to persist.

## Workflow

1. **Resolve helper path once into `$WFA`.** The script ships at `scripts/workflow-artifact.sh` in this repo and at the same path in target installs, but a plugin install has it only under the plugin root — written `${CLAUDE_PLUGIN_ROOT}` (braces), which Claude Code substitutes into this text at load time; it is never set in the Bash environment. Resolve it once with the same three-tier idiom `spec-driven-development` uses for `learnings.sh` — `MTK_HELPER_ROOT` first (a checkout you pin; see `CLAUDE.md`), then the project copy, then the plugin copy — and call `"$WFA"` everywhere below instead of a bare path:
   ```bash
   WFA="$([ -n "${MTK_HELPER_ROOT:-}" ] && echo "$MTK_HELPER_ROOT/scripts/workflow-artifact.sh" || ([ -f scripts/workflow-artifact.sh ] && echo scripts/workflow-artifact.sh || echo "${CLAUDE_PLUGIN_ROOT}/scripts/workflow-artifact.sh"))"
   ```
   Set `MTK_HELPER_ROOT=<toolkit checkout>` to force the scripts from that clone — the reliable path when dogfooding MTK from a separate checkout, or to pin one version out of a multi-version plugin cache.
   **State is project-anchored:** the script writes `.mtk/workflows/` under `$CLAUDE_PROJECT_DIR` (falling back to the git top-level, then cwd), so when MTK skills live outside the target project (plugin/marketplace install), export `CLAUDE_PROJECT_DIR=<project root>` or run from the project root — otherwise state lands in the wrong tree.
2. **Init at workflow start.** Prune expired workflows, capture the returned uuid into a session variable `MTK_WF_UUID`, and emit the first phase marker, all in the same call:
   ```bash
   "$WFA" prune --older-than 30 >/dev/null; MTK_WF_UUID=$("$WFA" init BUILD --goal "<one-line user goal>") && "$WFA" event "$MTK_WF_UUID" phase_started --data '{"phase":"phase-0"}'
   ```
   `prune` deletes finished workflows (`completed` / `abandoned`) and any workflow not updated for 30 days, with their event logs; it never touches an active workflow updated within the window. Preview with `--dry-run`. Run it before `init`, never after, so it cannot touch the workflow being started. A prune failure must not block the init, hence `;`.
   **Bookkeeping rides along, never alone.** Every artifact write below goes in the *same* Bash call as the action it records — appended with `&&` to the checkpoint command, the lint, the sidecar write — or several writes go in one `"$WFA" batch` call. A standalone `"$WFA" set …` turn costs a full model round-trip for one line of JSON; a 65-call run spends a quarter of its turns on bookkeeping. The `batch` form takes ordinary subcommand argv without the uuid, separated by a bare `--`:
   ```bash
   dotnet build --nologo -v q && "$WFA" batch "$MTK_WF_UUID" \
     gate phase_exit_gate pass --reason "batch B2 green" -- \
     set results.batches_completed=2 -- \
     event agent_returned --data '{"agent":"batch:B2"}'
   ```
   `event … --ts <iso8601>` replays a timestamp captured elsewhere (a dynamic workflow's per-batch dispatch/return times); tag such events `"source":"workflow-replay"` in `--data`.
3. **Persist anchors as soon as they exist.** When the spec, plan, and todo files are written, record their paths — in the same call as the next command that runs anyway (the context-pack build, the manifest pre-flight, the EARS lint in extended mode):
   ```bash
   bash scripts/build-context-pack.sh "$MTK_WF_UUID" docs/specs/2026-05-07-foo.json && "$WFA" set "$MTK_WF_UUID" \
     results.spec_path=docs/specs/2026-05-07-foo.md \
     results.plan_path=docs/plans/2026-05-07-foo.md \
     results.todo_path=tasks/todo.md
   ```
4. **Emit phase events.** At the start and end of every phase, in one call with the gate that closes it:
   ```bash
   "$WFA" batch "$MTK_WF_UUID" \
     gate phase_exit_gate pass --reason "all batch tests green" -- \
     event phase_completed --data '{"phase":"phase-3"}' -- \
     event phase_started   --data '{"phase":"phase-3.5"}'
   ```
   A `phase_started` event carrying a `phase` auto-advances the artifact's `phase_cursor` to that phase — no separate `set phase_cursor=` call is needed, and the resume protocol (step 7) can trust `phase_cursor` rather than replaying the event log.
5. **Record gate decisions.** Every named gate (`plan_trust_gate`, `phase_exit_gate`, `failure_stop_gate`, `memory_sync_gate`) must be persisted via:
   ```bash
   "$WFA" gate "$MTK_WF_UUID" phase_exit_gate pass --reason "all batch tests green"
   ```
   `fail` on any gate is a hard stop — see `failure_stop_gate` semantics.
6. **Carry a trap list across phases.** A *trap* is a written, specific gotcha a phase learned the hard way (a stale generated contract, an analyzer that fires only under `format`, a fixture that silently seeds the wrong state). A 2026-09 six-phase field run found this hand-carried list was the one mechanism that demonstrably worked — the final phase had zero repair cycles — and that it survived only because the driver remembered to paste it. Persist each trap the moment it is learned, riding along in the call that runs anyway (`trap` is batchable):
   ```bash
   "$WFA" batch "$MTK_WF_UUID" trap add --title "OpenAPI spec goes stale between phases" \
     --body "Regenerate the contract from a running API each phase — build/tests miss uncallable routes." \
     --phase phase-1 --severity high -- event phase_completed --data '{"phase":"phase-1"}'
   ```
   At the **start of every phase**, and in every implementer brief the orchestrator builds, inject the accumulated list:
   ```bash
   "$WFA" trap list "$MTK_WF_UUID"   # paste into the brief's "Known traps" block
   ```
   Adding a trap whose title already exists refreshes it in place. Traps are orchestrator-owned like every other artifact write: an implementer *reports* candidate traps in its result (`traps[]`, see `.claude/references/subagent-implementer-prompt.md`) and the orchestrator records them (S5.2).
7. **Resume protocol.** On entry to a workflow with no explicit uuid:
   - Run `"$WFA" list`.
   - If a single active workflow matches the requested type, offer resume.
   - If multiple, ask via `AskUserQuestion` which uuid to resume.
   - If none, init a new one (`init TASK` for a lightweight one with no other workflow).
   - To continue a checkpointed workflow, `"$WFA" resume <uuid>` prints a read-only RESUME block (drift since the checkpoint, `next_command`, open questions).
   - `"$WFA" checkpoint <uuid> --next … --decision … --verify …` re-renders the one canonical note and snapshots the tree; it is batchable as the LAST op (exit 3 = `--next` names a finished unit). Schema: `.claude/references/workflow-artifact-schema.md`.
8. **Close the workflow.** At end of phase 7, one call:
   ```bash
   "$WFA" batch "$MTK_WF_UUID" gate memory_sync_gate pass --reason "<what Phase 7 did>" -- \
     set status=completed -- event workflow_completed --data '{"summary":"<short>"}'
   ```
   A closing phase that did not run adds `event phase_skipped --data '{"phase":"<phase>","reason":"<why>"}'` to that call, and a skipped Phase 7 leaves out the `memory_sync_gate pass` op so the gate stays `pending` (`implement` → Final Report).
   On unrecoverable failure, close with the failure pair instead:
   ```bash
   "$WFA" batch "$MTK_WF_UUID" set status=failed -- event workflow_failed --data '{"reason":"<short>"}'
   ```

## Viewing Progress (Dashboard)

For a visual, read-only view of all workflows — status, phase, gate decisions, results, and event timeline — render the HTML dashboard:

```bash
scripts/workflow-dashboard.sh            # render once -> .mtk/workflows/dashboard/index.html, open it
scripts/workflow-dashboard.sh --watch    # regenerate + serve over http://127.0.0.1:8787/ (auto-refresh)
scripts/workflow-dashboard.sh --watch 10 --port 9000   # custom interval/port
```

The dashboard reads the same `{uuid}.json` + `{uuid}.events.jsonl` files this skill writes — it never mutates them, so it is safe to run during an active workflow. `--watch` regenerates on an interval and serves a static page (meta-refresh, no WebSocket) so a tech lead can watch a multi-batch run live. To share with non-CLI stakeholders, expose the served port with any tunnel tool (ngrok, cloudflared, ...) — the script intentionally stays a self-contained static renderer and does not embed a tunnel. Requires `python3` (the same dependency the helper already uses).

## Rules

- All writes go through `workflow-artifact.sh`. Never `Edit` or `Write` `{uuid}.json` directly — the event log would desync.
- Bookkeeping never gets its own turn: append `"$WFA"` calls to the command they record with `&&`, or group them with `batch`. The only standalone calls are `init` (with its `prune` prefix), `list`, `read`, and `verify-seal`.
- Subagents do not write workflow artifacts. The orchestrator persists subagent results via `event agent_returned`.
- Traps are carried, not re-derived. Record a trap the moment a phase learns it (`trap add`) and inject `trap list` into every subsequent phase brief — a trap that lives only in a phase report is lost the moment that report scrolls out of context.
- `.mtk/` is gitignored by default. Treat artifacts as local diagnostic state, not committed history.
- A `failure_stop_gate: fail` event terminates the workflow. Do not emit further events after `workflow_failed`.

## Verification

- [ ] `"$WFA" list` (resolved per step 1) shows the current workflow with the expected type and phase
- [ ] The event log ends with the most recent gate or phase event (no orphan state)
- [ ] On a fresh session, `list` plus reading the artifact reproduces the workflow's current state without chat history
- [ ] No direct `Edit`/`Write` calls were made against `.mtk/workflows/*.json`
- [ ] Traps discovered in a phase were recorded via `trap add`, and `trap list` was injected into the next phase's brief (not left in a phase report)
