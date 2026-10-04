---
name: pipeline
description: Use when the user asks to take a substantial feature from an initial idea through implementation in one mostly autonomous run.
argument-hint: "[resume|status]"
---

# Superb Pipeline

## Purpose

Pipeline is a thin controller around Superpowers. It keeps the approved design,
plans, decisions, execution state, and evidence in project files so a compacted
or restarted session can continue without inventing requirements or repeating
work.

The controller owns orchestration and durable transitions. It does not
reimplement the skills that investigate, plan, implement, debug, review, and
verify the work.

## Invocation

Trim whitespace from this complete argument string, then select exactly one
mode:

`$ARGUMENTS`

| Argument | Mode |
| --- | --- |
| empty | Full run: begin with planning. |
| `resume` | Resume one compatible v2 run from its files and Git evidence. Never create or replace a run. |
| `status` | Strictly read-only inspection. Do not lock, write, reconcile, dispatch, test, fix, or initialize. |
| anything else | Stop and ask what the user meant. Do not guess a verb or expose an internal remediation mode. |

Use the whole argument string, never an indexed positional placeholder.

For `resume` or `status`, use [references/persistence.md](references/persistence.md).
If no run is identifiable, report that. If multiple runs qualify, ask the user
which one. Recency is not selection authority.

## Zero-assumption law

Before making any required decision, inspect these sources in order:

1. the user's explicit instructions;
2. recorded explicit user answers;
3. the approved design/specification;
4. the approved master plan and phase plans;
5. explicit written repository rules.

If they explicitly answer the question, cite and follow the answer. If they do
not, or they conflict:

1. stop only the affected work;
2. record the exact question and blocked task/gate;
3. ask the user and wait;
4. persist the explicit answer;
5. update affected approved artifacts transparently when required;
6. resume through the validated controller transition.

Another agent may investigate facts and explain options, but it cannot decide
an unresolved requirement for the user. Generic approval or “continue” does
not answer a choice. Do not ask again when an explicit applicable answer is
already recorded.

**Configurability, reversibility, convention, a familiar codebase pattern, and
documenting an assumption do not authorize choosing an unanswered option.** If
the sources do not select the behavior, record and ask before implementing it.

This law applies during discovery, planning, implementation, tests, debugging,
review, fixes, and recovery. Final plan approval authorizes execution only of
the decisions the approved files actually contain.

## Files are the authority

The project must retain:

```text
docs/superpowers/
├── specs/<feature>-design.md
├── plans/<feature>-master-plan.md
├── plans/<feature>/phase-*.md
└── runs/<run-id>/
    ├── progress.md
    ├── decisions.md
    ├── findings.md
    ├── fix-plan-<gate>-r<n>.md
    └── agent-output/
```

Use an explicit repository convention when one exists. Never write project run
state into this installed skill directory.

`progress.md` is the sole mutable execution tracker. Plans define the work;
decisions, findings, fix plans, worker results, and verification records are
referenced evidence, not competing trackers. Only the controller performs
tracker transitions and result import. A worker may invoke only
`publish_worker_result` for its own assigned immutable result. Workers never
edit `progress.md`.

Before updating an existing run or dispatching from one, validate its v2 schema
and run identity. Initialize a fresh run only through the planning/persistence
contract. Ordinary resume supports only valid v2 state. Recognized v1, missing,
malformed, unknown, or unsupported schema information is a read-only stop:
preserve the directory, change no files, dispatch nothing, and do not migrate,
rename, reinitialize, or silently create a replacement. A fresh v2 run is a
separate explicit choice in a separate directory.

After compaction, interruption, or session restart, reconstruct the next action
from the approved files, tracker, decisions/findings, worker results, and Git
evidence. Reconcile every in-progress attempt before redispatch. A stale
`next_action` summary never overrides the underlying facts. Do not repeat
verified completed work or skip unfinished work.

## Stage routing

Load only the reference needed for the active stage:

| Active work | Required route |
| --- | --- |
| Discovery, design approval, master/phase planning, coverage and worker-limit decisions | [references/planning.md](references/planning.md) |
| Task/batch dispatch, TDD, integration, and phase verification | [references/execution.md](references/execution.md) |
| Tracker operations, status, resume, results, and recovery | [references/persistence.md](references/persistence.md) |
| Required high-risk gates, master review, findings, and remediation | [references/review.md](references/review.md) |

When creating or changing a skill, use `superpowers:writing-skills` for RED and
GREEN pressure scenarios. Label real-agent evidence separately from simulations.

### Planning

Use `superpowers:brainstorming` to investigate and reach a user-approved design.
Use `superpowers:writing-plans` for the complete master plan and one detailed
file per phase. Phase-expansion workers use writing-plans and report unresolved
interfaces; they do not invent them. Before implementation, require approval of
the executable plan, no more than 12 genuine tasks per phase, explicit task
dependencies/kinds/scopes/outputs/tests, phase verification, and review-risk
classification.

Every run needs an explicit positive `worker_limit` compatible with detected
runtime capacity. If it is absent or cannot be supported, ask before the first
worker dispatch. Persist it and apply it globally across planning,
implementation, fix, and review workers. Workers may not spawn untracked
helpers.

### Execution

Use `superpowers:using-git-worktrees` for isolation and
`superpowers:dispatching-parallel-agents` only for ready independent batches.
A task is a durable planning/recovery checkpoint, not automatically an agent
boundary. Compatible sequential tasks may share an executor. Before every
actual start, serialize the reservation and revalidate dependencies, decisions,
capacity, ownership, and typed write-scope conflicts.

Persist task state, owner, and attempt before dispatch. Each worker receives the
zero-assumption contract and returns exactly one of:

`DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `PLAN_CONFLICT`, `BLOCKED`.

A question result either resolves from an existing explicit applicable answer
or reaches the user. Stop new dependent dispatch and integration while it is
unanswered; independent running work may finish. A worker's `DONE` is evidence,
not acceptance.

Use `superpowers:test-driven-development` for testable behavior and fixes, and
`superpowers:systematic-debugging` for unexpected failures. Preserve per-task
checkpoints within a multi-task batch. Verify source commits, artifact evidence,
and complete Git integration provenance before downstream work becomes ready.
New source attempts persist their target baseline; completion proves the exact
nonempty in-scope commit range and digest-bound typed task evidence. Integration
and phase verification likewise require typed evidence for the exact code state
and the plan's exact ordered command suite. Every phase receives that planned
mechanical verification on the applicable integrated code state. A failing
implementation or verification gate keeps the phase unfinished and returns to
repair, not formal review.

### Review and completion

An ordinary phase marked `final-only` gets mechanical verification and no
formal phase reviewer. A phase explicitly marked `required` gets one independent
reviewer only after complete integration and successful mechanical verification;
dependent work waits for that gate.

After every phase is accepted, the mandatory master gate uses exactly two
independent complementary reviewers over the complete edge from the immutable
tracker `base_commit` to the last approved phase's recorded verified integrated
HEAD. Neither reviewer may be a persisted task implementation owner.
Collect all required reports before consolidating or dispatching fixes. Apply
the shared `Critical` / `Important` / `Minor` acceptance and bounded remediation
contract in [references/review.md](references/review.md). Every
repository-changing review fix is verified and re-reviewed at the same gate.
There is no per-task formal review.

Use `superpowers:verification-before-completion` for fresh final evidence. The
last accepted phase routes to the mandatory master gate, not project completion.
Completion requires the master gate, final verification, all intended work
committed and integrated on the designated clean feature branch, and consistent
recoverable files. Persist the final verification against the accepted master
HEAD so a fresh session derives `complete` from files and Git rather than a
previous completion message.

Do not invoke superpowers:subagent-driven-development or
superpowers:executing-plans. Their generated task-review/handoff workflows
conflict with this approved batch-and-phase architecture; a writing-plans header
does not override this route. Do not use
`superpowers:finishing-a-development-branch` or an interactive completion menu.

Never push, publish, create a pull request, or merge into `main`/`master`.
Leave the clean, committed feature branch as-is and report its final evidence.

## Stop checks

Stop and read the authoritative files when you are about to:

- choose behavior from convention, convenience, configurability, or an
  undocumented “safe default”;
- dispatch without a persisted assignment or from a stale readiness result;
- infer that a missing result means work is complete or must be repeated;
- advance past failed verification or an unresolved required review;
- let a task implementation report trigger a formal task review;
- treat available capacity as permission for conflicting, dependent, early, or
  duplicate work;
- treat a final phase as complete before the master gate; or
- perform a remote, PR, publish, or main/master mutation.

If a required answer is absent, record and ask the user. Otherwise derive the
next eligible action from the validated v2 state and continue.
