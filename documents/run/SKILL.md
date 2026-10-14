---
name: plan-mode-run
description: Execute an accepted plan and track real progress. Use when the user says to run, carry out, or continue a plan, including one partly completed or disrupted by other work.
license: MIT
---

# Run

Resume from reality, not from step one. The plan guides the work; the current state determines the next action.

1. Read the accepted goal, plan, constraints, and latest state. Inspect existing changes and ownership before editing. Mark steps already complete with evidence, and find the first incomplete step whose prerequisites hold.
2. Execute that step with the smallest coherent change. Preserve unrelated and unfinished work. A plan does not itself grant permission for a push, deployment, or external write; check the user's existing authorization before those actions.
3. At each step boundary, run its completion check and retain the result. Do not infer success from code being present, a command merely starting, or a typecheck standing in for behavior.
4. If a prerequisite or assumption fails, stop repeating the same attempt. Record the failing observation and use **plan-mode-reroute** to choose a revised path. Carry forward completed work and the original goal.
5. Use **plan-mode-verify** against the acceptance evidence before claiming the run is complete. Report what changed, what passed, what remains, and the exact blocker if progress cannot continue.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
