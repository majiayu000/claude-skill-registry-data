---
name: suspend
description: Use this skill when the user runs /suspend or asks to pause, disable, or temporarily turn off the SDLC workflow. Disables enforcement by snapshotting governance artifacts and switching the active marker to .suspended. Requires a stated reason. Hard-blocks if workflow is not currently enabled.
next_suggestions:
  - when: suspend_complete
    suggest: "run /start to re-enable the SDLC workflow and reconcile any changes made during suspension"
---

# Suspend — Pause SDLC Enforcement

Snapshot governance state, log the suspension, switch `.enabled` → `.suspended`. Six steps in order. No step may be skipped.

## Step 1 — Guard: workflow must be enabled

Check for `.claude/sdlc/.enabled`.

If absent:
```
[SDLC] Workflow is not enabled — nothing to suspend.
Run /start to enable the workflow first.
```
Stop. Do not proceed.

## Step 2 — Require a suspension reason

Prompt:
```
Reason for suspension (required): _
```

Hard-block if the response is empty, whitespace-only, or a single character. Re-prompt once:
```
A reason is required to log the suspension. Please enter a brief description: _
```

If the second response is also empty: print `[SDLC] Suspend aborted — reason is required for audit log.` and stop. Do not proceed without a reason.

## Step 3 — Show active plans and unsigned gates

Read every `.md` file in `.claude/sdlc/plans/` (exclude versioned files matching `*.v[0-9]*.md`). For each, check its corresponding gate file in `.claude/sdlc/gates/` for unsigned status (gate file absent or missing `**Signed at:**` line).

Display:
```
Active plans:
  REQ-001  add-login-page  [build gate unsigned]
  REQ-000  scope-setup     [signed — all phases complete]

Warning: REQ-001 has an unsigned build gate.
Suspending will pause enforcement. The gate remains open until you re-enable and complete it.
Proceed? [Y/n]
```

If no active plans exist, omit the plan list and just show:
```
No active plans found.
Proceed with suspension? [Y/n]
```

If the user enters `n` or `N`: print `[SDLC] Suspend aborted.` and stop.

## Step 4 — Run suspend-snapshot.sh

Call `hooks/suspend-snapshot.sh suspend` (relative to the plugin root, or absolute if `$CLAUDE_PLUGIN_ROOT` is set).

The script handles openssl availability, the gitignore check for `config/tools.local.json`, and manifest encryption. If the script exits non-zero or outputs an ERROR line, surface the error to the user and stop — do not rename the marker.

If the script prints `Suspend aborted. Workflow remains enabled.` (the openssl absent + user declined path), echo that message and stop.

## Step 5 — Log suspension window entry

Append one JSON line to `.claude/sdlc/.suspension-log.jsonl` (create the file if absent):

```json
{"event":"suspend","at":"<ISO-8601>","reason":"<reason from Step 2>","active_plans":["REQ-001","REQ-000"]}
```

Use UTC for the timestamp. `active_plans` is the list of REQ-IDs from Step 3 (all plans, not just unsigned ones).

## Step 6 — Switch marker and confirm

```bash
mv .claude/sdlc/.enabled .claude/sdlc/.suspended
```

Print:
```
[SDLC] Workflow suspended. Snapshot saved. Enforcement paused.
Suspension logged. Run /start to re-enable.
```

## What this skill must NOT do

- Do not suspend if `.enabled` is absent — never create `.suspended` without a prior `.enabled`.
- Do not skip the reason prompt, even if the user gives a task description that implies a reason.
- Do not rename the marker before the snapshot succeeds (Step 4 before Step 6).
- Do not interpret "I want to take a break" or similar as an implied reason — ask explicitly.

## Graceful degradation

- `.claude/sdlc/plans/` does not exist → treat as no active plans. Proceed with empty list in Step 5.
- `hooks/suspend-snapshot.sh` not found → surface the error; do not proceed with the marker rename. The snapshot is a required step, not optional.
- `config/tools.local.json` write fails (e.g. read-only filesystem) → surface the error; stop.

## References

- `hooks/suspend-snapshot.sh` — snapshot and verify substrate
- `docs/rfcs/opt-in-activation-suspend-resume.md` §6 — full suspend flow spec
- `skills/start/SKILL.md` — re-enable reconciliation (invoked after /start on a suspended repo)
