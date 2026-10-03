---
name: forge-verify
description: Runs Forge's verify-loop — checks a completion claim against events.jsonl and the ticket store, sends it back if false. Use after every agent/work-package completion in a run.
---

# forge-verify — the verify-loop

**Self-improvement substrate (wp-skill-evals, 2026-07-31):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction (an owner fix, a false assumption caught, a preference stated), append it to
`learnings.md` with a date and real evidence — never invent a lesson that didn't happen.

Closes the honesty gap between "an agent said it's done" and "the recorded events actually show it's
done." Never trusts a completion claim on its own.

## When to use (MANDATORY)

- **After each agent/work-package completes** in a `/forge` run — before the Lead treats that agent's
  output as final.
- **At the end of the run**, before writing the final report — a last honest check across every agent
  and every ticket the run touched.
- Whenever the owner asks "did that agent actually finish?" or "check the tickets are really closed."

## How to run

```
node .claude/forge-bin/forge-verify.cjs <run_id>                      # report only, exit 0/1
node .claude/forge-bin/forge-verify.cjs <run_id> --enforce            # report + send mismatches back
node .claude/forge-bin/forge-verify.cjs <run_id> --json               # full machine-readable result
node .claude/forge-bin/forge-verify.cjs <run_id> --root <projectRoot> # target a different project root
```

Exit code: 0 when there are no mismatches and no open tickets for the run; 1 otherwise — safe to gate a
hook/CI step on it.

## What it checks

Reconstructs per-agent task state from `<run>/events.jsonl` using forge-verify.cjs's own `BACKBONE` +
`taskStatus()` — the sole, canonical classification since v2.9.0 (this used to also mirror the retired
per-project Control Center's `forge-dashboard/app.js`, which was removed along with the rest of that
dashboard): structural milestone events (`run_started`,
`agent_completed`, `lead_review_completed`, …) are never counted as a "task"; every other event
attributed to an agent is a task, and a task is "done" only when its status genuinely resolves to done.
An agent "claims completed" once it has logged `agent_completed` or `subagent_completed`. A **mismatch**
is an agent that claims completed while some of its own tasks are still open, running, or failed.

It also checks the ticket store (`forge-bin/forge-store.cjs`, `forge-tickets/`): any ticket whose
`run_id` matches this run and whose `status` isn't `done` is reported **open**.

## What `--enforce` does

For every mismatch, logs three already-registered events (no invented event_type names — see
`forge-dashboard/log-event.cjs` `KNOWN_EVENT_TYPES`):
`lead_review_completed` (the review finding) → `rework_task_created` (what's wrong + the required fix) →
`rework_assigned` (back to the same agent).

For every open ticket belonging to the run: re-stores it with `status: 'open'` **unchanged** plus a note,
and logs `ticket_updated`.

The task is now visibly back with the agent. **The Lead must re-dispatch that agent** with the open
items listed in the rework event before treating the work as done again.

## Honesty rule

`forge-verify` **never marks anything done**. It only reopens or flags — closing a task or ticket is
always a real agent/human action, verified again by the next `forge-verify` pass. The dashboard shows
the exact same mismatch (⚠) using the same `taskStatus()` logic, so the tool and the dashboard never
disagree about what "done" means.
