---
name: run-state-management
description: "Manage FlowRun state at `.flow/runs/<ISO-timestamp-id>/run.yaml` — create runs at command entry, write activity records via `bin/flow-record-activity.sh` at phase boundaries, transition `state.status` (active → completed | blocked | cancelled), and persist resumable next-action hints to `events.jsonl`. Use when a flow command begins (creates the run), when a phase boundary completes (writes an activity), or when SessionEnd needs to mark a resumable next action. This skill MUST be consulted because runs without recorded activities cannot be resumed — `/flow:resume` reads `state.completed_activities[]` to identify the next safe action; an empty array forces the user to start over."
allowed-tools: Bash, Read, Write
context: fork
agent: general-purpose
---

# Run State Management

## Contract

Iron law: no phase transition without an activity write — `state.completed_activities[]` is the source of truth for `/flow:resume`, and a missing activity makes resume skip ahead and lose work. Invoked when `FLOW_RUN_STATE=create` (gated by `flow.runtime.enabled`) by `/flow:start`, `/flow:debug`, `/flow:address`, `/flow:review`, `/flow:merge`, `/flow:release` at command entry (create), at every phase boundary (activity), and at completion (terminal transition); `/flow:pr` appends activities to the active `start-issue` run; `/flow:resume` reads its output. Returns `.flow/runs/<id>/run.yaml`, `activities/<NNN>-<name>.yaml`, `events.jsonl`, and a `workflow-run` journal artifact. Permitted skips: only when `flow.runtime.enabled` is `false`, or when step 1 refuses the run directory because `.flow`, `.flow/runs` or the run directory is a symlink — then nothing under `.flow/` is written.

## Inputs

The invoking command MUST pass:

1. **Workflow id** — `start-issue | debug | address-pr | review-pr | merge-pr | release` (matches `plugins/flow/workflows/<id>.workflow.yaml`).
2. **Run id** — `<ISO-8601-compact-timestamp>-<target-slug>`, e.g. `2026-05-20T143000Z-issue-42`.
3. **Context** — repo, branch, issue/pr number, linked journal path, linked goal id (or `null`).
4. **Phase** — initial phase id (`preflight` at creation; the workflow's phase order thereafter).

## Outputs

1. `.flow/runs/<id>/run.yaml` — FlowRun conforming to `schemas/v1/run.schema.json`.
2. `.flow/runs/<id>/activities/<NNN>-<name>.yaml` — one FlowActivity per phase boundary, `schemas/v1/activity.schema.json`.
3. `.flow/runs/<id>/events.jsonl` — line-per-event ledger.
4. `workflow-run` artifact in the linked decision journal (`bin/journal-record.sh --type workflow-run`), updated with the final status at the terminal transition.

Exact document shapes and the per-workflow phase-order table: `references/run-state-templates.md`.

## Workflow

1. **Create the FlowRun** at command entry. First create its directory with this block, `RUN_ID` set to the run id:

```bash
# RUN_DIR_CREATE_BLOCK_BEGIN
case "${RUN_ID:-}" in
  ''|.|..|*/*|*..*) printf '%s\n' "ERROR: RUN_ID must be a run id without '/' or '..', got '${RUN_ID:-}'" >&2; exit 1 ;;
esac
# Never through a symlink: a repository can commit .flow or .flow/runs as a
# link to a directory outside the checkout, where run.yaml would be written.
"$(__fr="${CLAUDE_PLUGIN_ROOT:-}";[ -x "$__fr/bin/cascade-resolve.sh" ]||__fr=$({ printf '%s\n' plugins/flow;ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/synapti-marketplace/flow/*/ 2>/dev/null|sort -Vr;printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/synapti-marketplace/plugins/flow"; }|while read -r __p;do [ -x "${__p%/}/bin/cascade-resolve.sh" ]&&{ printf '%s\n' "${__p%/}";break;};done);printf '%s\n' "$__fr")/bin/flow-mkdir.sh" -- ".flow/runs/$RUN_ID" || { [ $? -eq 3 ] && exit 3; exit 1; }
printf '%s\n' "RUN_DIR=.flow/runs/$RUN_ID"
# RUN_DIR_CREATE_BLOCK_END
```

If it exits non-zero, create no run: say why — exit 1 is a refused symlink, exit 3 a check that could not run (python3 missing), not a symlink — and carry on as when `flow.runtime.enabled` is `false`. Otherwise write `run.yaml` into `RUN_DIR` (`state.status: active`, `current_phase` = initial phase, `completed_activities: []`, `events: [run_started]`) by direct file write — race-free because the run is new — and emit the `workflow-run` journal artifact with `status=active`.

2. **Record an activity at every phase boundary** (and significant sub-steps): compose the FlowActivity YAML to a temp file, then `bin/flow-record-activity.sh --run-id <id> --activity-file <path>`. The helper assigns the sequence number, validates against the schema, writes atomically (O_NOFOLLOW + flock + tempfile+rename), and appends to `events.jsonl`.
3. **Update `state.current_*`** after each activity: advance `current_phase` at a boundary, set `current_activity`, append the recorded id to `completed_activities[]`. Read-merge-write through `bin/_journal_atomic.py` (`acquire_lock(run.yaml.lock)` + atomic write) — never a bare overwrite.
4. **Terminal transition** when the command ends: `state.status` → `completed` (verdict PASS / action succeeded), `blocked` with `blocked_reason` (verdict FAIL or session ended mid-workflow), `failed`, or `cancelled`; then re-emit the `workflow-run` artifact with the final status.
5. **SessionEnd** (`hooks/scripts/session-end-state.sh`, not this skill): appends a `session_end` event to each active run's `events.jsonl` and prints `flow: N active FlowRun(s) persisted` — it does not mutate `run.yaml`; status changes are the user's decision via `/flow:resume`.

## Rules

- Never write `run.yaml` outside the helper except the initial create — concurrent updates need flock.
- Never advance `state.current_phase` without writing an activity.
- Never mark `state.status: completed` with an empty `completed_activities[]`.
- Readers of `events.jsonl` MUST skip un-parseable trailing lines (atomic at write, tolerant at read).
- Never auto-resume a `blocked` run without surfacing `blocked_reason` first.

## Reuse map

- `plugins/flow/skills/autonomous-workflow/SKILL.md` — phase structure source of truth; this skill materializes its phase boundaries.
- `plugins/flow/bin/flow-record-activity.sh` — atomic activity writer.
- `plugins/flow/bin/flow-mkdir.sh` — creates the run directory, never through a symlink.
- `plugins/flow/bin/_journal_atomic.py` — `acquire_lock`, `_atomic_write` for run.yaml updates.
- `plugins/flow/schemas/v1/run.schema.json`, `activity.schema.json` — document schemas.
- `plugins/flow/references/decision-journal-schema.md` — `workflow-run` and `run-state-transition` artifact rows.
- `plugins/flow/references/flow-runtime-state.md` — `.flow/` layout, gitignore policy, resumability.
