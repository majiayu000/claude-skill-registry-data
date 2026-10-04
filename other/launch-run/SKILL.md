---
name: launch-run
description: Launch a specific Coval evaluation with explicit cases and execution bounds. Use when resources are already selected; for result analysis use quick-eval.
argument-hint: "[agent] [test-set]"
---

# Launch a Coval run

Use `quick-eval` when installed; it covers planning, bounded execution and the
result audit. Do not bypass its session budget when invoked from that workflow.
If this skill is installed alone, follow the same minimum launch contract:

1. Confirm the intended organization, workspace and API environment. Read the
   agent, persona, exact cases and selected metric definitions. Check command
   help and errors. Authentication is not proof of tenant identity.
2. Prepare a structured launch request with explicit `options.test_case_ids`,
   iteration count, concurrency, metric IDs and a verified per-call duration
   limit. Count cases × iterations × (1 + mutation count), per persona, including
   any prior runs in the session. Concurrency does not reduce total cost.
3. Show the concrete plan and bounded stopping condition. A request to plan or
   inspect is not paid-run authority; honor already granted execution authority
   and ask only when scope/budget must expand. Default to proposing one call for
   an untested connection, not the entire test set.
4. Execute `coval --agent runs launch --input-json @run.json`. Check `ok` and
   exit status. Save the returned run ID. If the response is ambiguous, inspect
   matching runs before retrying; never blindly retry a launch.
5. Return the run ID and actual observed status. Queued is not completed. Follow
   the user's requested scope: for a completed evaluation, poll and audit results
   as in `quick-eval`; for launch-only, hand back the run without claiming quality.

Use the current [runs schema](https://api.coval.dev/v1/openapi/runs). Do not use
`/eval/*`, invent command flags, add schedules, change agent defaults, or rerun
unattended. A local plan is not a server-enforced spending cap.
