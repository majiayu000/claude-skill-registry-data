---
name: byte-status
description: "Inspect progress, blockers, and remaining work in a Byte project."
---

# Byte Status

Report status from live evidence, not from narrative claims alone.

Inspect the relevant files, version control state, tests, processes, outputs, and
Byte OS notes in proportion to the question. Treat stale or conflicting status
documents as evidence to reconcile, not as the source of truth.

Read `.byte-os/LESSONS.md` when present. Report an active lesson only when it is
relevant to current risk, a repeated mistake, or the next action; do not make the
status report a full notebook dump.

Summarize:

- what is demonstrably complete;
- what is in progress or uncertain;
- blockers and their exact cause;
- the highest-value next action.

Use counts or percentages only when the underlying units are meaningful. Mention
parked or future ideas separately from active scope. Do not mutate the project
unless the user also asks to continue or repair it.

Interpret legacy Byte OS artifacts as ordinary evidence; their recorded stage
does not override explicit intent or live behavior.

## Scheduled Work

For an existing long-running handoff, inspect the job identity, live scheduler
or process state, terminal receipt, expected outputs, and monitor status. Report
phase-goal completion separately from job success and overall completion.
Compare the saved monitor scope with remaining work and report stale targets or
intervals; status-only requests do not change the automation. A
missing process or stale log is not proof of success. Status-only requests do not
create goals or monitors; authorized continuation follows
[the long-running workflow](references/long-running-work.md).

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
