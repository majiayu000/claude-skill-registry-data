---
name: ls-workflow-ops-guarded
description: Use when risky operations need approval checkpoints, impact review, or guarded execution; hand off sudo, elevated, PTY, or interactive password execution to ls-workflow-ops-tmux-session.
metadata:
  version: "1.0"
---

Use this workflow package to authorize and bound risky operations before they
run. Compose `ls-safety-and-backup`; do not replace its risk, backup, or
rollback rules with an informal impact summary.

Primary references: `ls/skills/ls-safety-and-backup/SKILL.md` and
`ls/workflows/ls-workflow-ops-tmux-session/SKILL.md`.

## Required gate sequence

1. Classify the proposed operation as LOW, MEDIUM, HIGH, or CRITICAL under
   `ls-safety-and-backup`. Record likely consequences and the affected users,
   services, files, and persistent state. Prefer a dry run when supported.
2. Before changing sensitive configuration or persistent state, create and
   verify the required backup and record the exact rollback or restore action.
   If a backup is not applicable or the user declines one, record the reason
   and residual risk before continuing.
3. Freeze one approval payload containing the exact command or edit, target,
   values, risk class, likely consequences, affected scope, backup result,
   rollback action, and safer manual option when one exists.
4. Immediately before execution, show that payload and wait for explicit user
   approval of its exact command or edit, values, and target. A changed command,
   value, target, scope, or rollback plan invalidates approval and returns to
   the applicable earlier gate.
5. Execute only the approved operation. Capture the result and verify the
   intended state without widening the approved scope.

## Privileged or interactive handoff

When the approved operation needs `sudo`, root/admin elevation,
`require_escalated`, pseudo-terminal/PTY handling, or an interactive password
prompt, hand execution to `ls-workflow-ops-tmux-session` only after all four
pre-execution gates pass and the frozen approval payload still matches.

The tmux workflow owns session selection, readiness probes, the user-mediated
`sudo ready` exchange, execution, status, and cancellation. Never collect the
password, bypass its probe, or use the handoff to alter the approved command,
values, or target.
