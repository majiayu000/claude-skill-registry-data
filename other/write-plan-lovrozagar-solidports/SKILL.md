---
name: write-plan
description: 'Write a local checklist under .tmp/grunt/plans/. Then /implement-plan {n}.'
---
# write-plan

You author the plan. Persist under `.tmp/grunt/plans/` via Write (hook runs `.rulesync/scripts/persist-plan.mjs`). Format: `.rulesync/reference/plan-format.md`.

Empty task → ask for a task and stop.

Body starts with `PLAN_NAME: <3-6 word name>`, then Goal, Context, Constraints, Watch-outs, Steps, Verify. All boxes `[ ]`. Tests: new behavior or bug → failing test leaf before impl; other behavior → test leaf right after impl; docs/rename/config/generated → skip. Verify is the end gate.

After research, pick one type from `.rulesync/reference/scope.md` ## Types. Context starts with `Task type: {name}` and `Named checks:`. Copy that row's checks into Steps or Verify, including a Read leaf for each named principle. Also copy a Read leaf for every fact in ## Facts that is true of this plan. No fact, no leaf. Verify includes a Read leaf for `principle-prove-it-works`. For `cross-cut`, Context also holds architect lite: types, signatures, module map, and the rejected shape. A named check that does not apply is a Context skip with a reason.

Before you ask the user, read `principle-never-block-on-the-human`. Ask only when the user alone can answer or the action is destructive. Before a large dump or a fan-out, read `principle-guard-the-context-window` and route the bulk through `node .rulesync/scripts/grunt-job.mjs`.

Author `commit: type(scope): subject` on its own line before persist (scope optional). Conventional Commits subject: imperative lowercase, no trailing period. Types: feat fix docs style refactor perf test build ci chore revert.

The plan is the proposal and caps the result (`.rulesync/reference/scope.md`). Before writing, research until every leaf is defensible; ask any plan-shaping question the user alone can answer, then research again on the answer. Do not default a plan-shaping choice. A minor open choice goes under Constraints as the chosen default plus "confirm".

Report: serial N at `.tmp/grunt/plans/{file}`, the goal, the phase list, the top risks, and any assumption to confirm. Do not dump the plan. Stop and ask for approval; on feedback, revise this file and stop again. Run `/implement-plan {n}` in the same turn when the request said "plan and do it", or when `/implement-roadmap` is running a `locked` or `in-progress` roadmap. A plan-shaping question still stops.
