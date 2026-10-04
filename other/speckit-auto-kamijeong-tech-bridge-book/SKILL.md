---
name: "speckit-auto"
description: "Orchestrate the Claude Spec Kit sub-agent workflow with mandatory token observability."
compatibility: "Requires Spec Kit feature artifacts and Claude project-scoped agents"
---

# Spec Kit Auto Workflow

Default mode is `gated`. Before starting a full workflow, check token-analyzer
availability with `.claude/skills/speckit-guards/scripts/guard-token-analyzer-available.sh`.

## GitHub Issue Trigger Mode

When a GitHub issue title, body, or comment contains `/speckit-auto`, treat the
issue as an instruction to run this skill for Claude-only work. Use the issue
body as the feature request and inspect linked comments, checklists, and
sub-issues before starting. `$speckit-auto` is reserved for Codex issue routing
and MUST NOT be claimed by the Claude issue runner unless the issue also
explicitly contains `/speckit-auto`.

This trigger does not override normal safety gates. Follow the requested mode
from the issue when present; otherwise use `gated`. Treat human-readable issue
template choices that include `(gated)`, `(auto-implement)`, or `(auto-pr)` as
the corresponding mode. Also treat `(auto-stack-pr)` as stacked PR mode.
Implementation is allowed only when the issue explicitly requests
`auto-implement`, `auto-pr`, `auto-stack-pr`, or when the user has already
approved implementation in the current conversation. `auto-commit`, `auto-pr`,
and `auto-stack-pr` are supported terminal actions, but they still require
explicit permission before Claude commits, pushes, opens a PR, or submits a PR
stack.

Use GitHub issue labels as live workflow state:

- Add `trigger:speckit-auto` and `agent:claude` when taking the issue.
- Add exactly one `mode:*` label when the mode is known.
- Add `status:in-progress` when work starts.
- Move the active `phase:*` label after every completed phase.
- Use `status:needs-clarification` when a required decision is missing.
- Use `status:blocked` when a stop condition is hit.
- Use `status:waiting-review` after implementation and review evidence are ready.
- Use `status:done` only after the requested terminal action is complete.
- Use `status:failed` when the workflow cannot continue because validation or a
  required external operation failed.

## Sub-Agent Execution

Run workflow phases through the existing project-scoped Claude sub-agents
whenever the phase maps to a dedicated role. Use the role that matches the
phase:

- `speckit-slicer`: intake and slicing
- `speckit-scheduler`: scheduling
- `speckit-specifier`: specify
- `speckit-clarifier`: clarify
- `speckit-checklister`: checklist
- `speckit-planner`: plan
- `speckit-tasker`: tasks
- `speckit-analyzer`: analyze
- `speckit-implementer`: implement
- `speckit-reviewer`: review
- `speckit-integrator`: integration
- `speckit-token-reporter`: token reporting
- `speckit-committer`: commit
- `speckit-pr-creator`: PR creation

Only keep work local when a stop condition, missing agent definition, or runtime
limitation prevents safe delegation. When delegation is unavailable, record that
limitation in the issue comment and continue only if the requested mode allows
it.

Always add an issue comment before starting a phase and after completing a phase.
Also add a short comment before any terminal action such as commit, push, or PR
creation. Comments should state what Claude is doing, which files or artifacts are
in scope, which label changed, and any gate result. Keep comments short and
factual.

If the issue is too broad or Claude determines sub-issues are needed, create
sub-issues only in the same GitHub repository. Link them from the parent issue,
label the parent with `status:needs-sub-issues` and `relationship:parent`, label
each child with `relationship:sub-issue`, `trigger:speckit-auto`, `agent:claude`,
and the relevant `type:*`, `priority:*`, `risk:*`, and `mode:*` labels. Add a
parent issue comment explaining the split and the execution order.

Use the GitHub app tools when available for labels, comments, issue creation,
and issue inspection. Use `gh` only as a fallback when the app tools cannot
perform the needed operation.

## Orchestration Order

1. intake
2. slicing
3. scheduling
4. per-slice Spec Kit workflow
5. implementation
6. review
7. integration
8. token reporting
9. commit
10. PR creation

After every completed phase, record token usage using token-analyzer when
available or `.agents/skills/speckit-guards/scripts/record-token-step.sh` when a
phase is custom or unsupported. Token reporting is mandatory before commit or
PR creation.

## Intake And Slicing

Accept the feature request and determine whether it should be split before
running specify. Treat the request as a slicing candidate when it spans multiple
independent deliverables, shared contracts, or more than one implementation area,
unless the user or workflow explicitly overrides the decision.

Intake artifacts should capture:

- original request summary
- target epic slug
- proposed slice ids
- explicit overrides
- assumptions
- token run label

## Scheduling

For sliced work, build:

- dependency graph
- conflict matrix
- execution plan
- selected strategy

Allowed strategies are `single-spec`, `sequential`,
`foundation-first-then-parallel`, `parallel-safe`, and `stop-and-ask`. Use
`stop-and-ask` when dependency, file, contract, configuration, or repository-state
conflicts are unclear.

## Per-Slice Workflow

For each approved slice, run:

1. specify
2. clarify
3. checklist
4. plan
5. tasks
6. analyze
7. implement
8. review

In `plan-only`, stop after analyze and token reporting. In `gated`, ask before
implementation, commit, and PR. In `auto-implement`, implement only when analyze
passes and the slice is low risk. In `auto-commit`, validate, token-report, and
commit only when explicit permission is present. In `auto-pr`, implement,
validate, token-report, commit, push, and create a draft PR only when explicitly
requested. In `auto-stack-pr`, implement validated slices as an ordered stack,
commit each slice separately, run integration before publication, then use
`gh stack submit --auto` to create or update stacked draft PRs only when
explicitly requested.

## Integration

After multiple slices are implemented, check cross-slice file conflicts, shared
contract drift, integration risks, and merge readiness. Record token analysis for
integration.

## Commit

Commit only after review and validation pass. Use conventional commits by
default. Commit only intended files, never secrets, and include token-analysis
artifacts only when they belong to the current run. `auto-commit` is an explicit
permission flag, not a standalone mode, and may be used to authorize the commit
step of an `auto-pr` or `auto-stack-pr` run.

## Draft PR

Use GitHub CLI. Create draft PRs by default. Never push directly from `main`,
`master`, or `develop`. Include changed files, spec, plan, tasks, tests, risks,
reviewer notes, and token summary. Print PR URLs after creation.

For `auto-stack-pr`, use `gh stack` rather than individual `gh pr create`
commands. The scheduler's dependency order becomes the stack order: foundation
or shared-contract slices closest to the trunk, dependent slices above them.
Each stack branch must contain only its slice changes plus required token
artifacts for the current run. Run the PR guard with stacked mode enabled before
submitting, then use `gh stack submit --auto` so PRs remain drafts by default.
Stop before submission if the stack order is unclear, a slice is not separately
committed, `gh stack` is missing, or the current branch is protected.

Required PR section:

```markdown
## Token Analysis

- Run label:
- Token report:
- Total tokens:
- Most expensive phase:
- Missing token data:
- Token budget status:
- Notes:
```
