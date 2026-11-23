---
name: qfai-implement
title: QFAI Implement (TDD micro-cycle)
description: "Use when invoked by name or handed a QFAI work order to implement, diagnose or repair the examples of one business flow."
argument-hint: "<BF-ID> [EX-ID...]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, TodoWrite, Task, Agent]
steps:
  - implement-scaffold
  - implement-credentials
  - implement-tdd
  - implement-diagnose
  - implement-regression-fix
  - implement-test-fix
  - implement-seam
  - implement-bisect
  - implement-revert
  - implement-minimize
  - implement-stress-harness
  - implement-oracle-parity
  - implement-benchmark
  - implement-refactor
  - implement-retire
  - implement-sweep
  - implement-quarantine
  - implement-dep-bump
  - implement-tooling
  - implement-backport
  - implement-acceptance
  - implement-procedure
  - implement-settled-edit
requires: [common-review-cycle]
mode: approval-gated
---

## /qfai-implement — Implement a business flow

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

## Inputs

- `<BF-ID>`: the business flow, `BF-NNNN`.
- `[EX-ID...]`: optional examples of that flow, worked in the order given.
- The flow's stories, acceptance criteria, examples and contracts, from the
  configured `paths.specsDir` and `paths.contractsDir`.
- For UI work, root `DESIGN.md` and the flow's UI contracts. The rendered
  surface is reviewed, not only the source. Before calling a screen done, check
  it against
  `.qfai/assistant/skill/qfai-sdd/references/design-anti-patterns.md#information-architecture-and-flow`
  and
  `.qfai/assistant/skill/qfai-sdd/references/design-anti-patterns.md#states-and-accessibility`.
- No deliberation record: this stage opens no file under `paths.deliberationDir`.

Every step follows `.qfai/assistant/rule/shared-skill-operating-baseline.md`,
`.qfai/assistant/rule/shared-skill-delegation-baseline.md` and
`.qfai/assistant/rule/test-layers.md`. Every question to the user follows
`.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.

## Steps

`<BF-ID> [EX-ID...]` runs these steps, in this order:

| Step                    | File                                                 | Runs                                                                |
| ----------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| `implement-scaffold`    | `.qfai/assistant/step/implement-scaffold/STEP.md`    | First: the flow's missing acceptance tests, each with an empty body |
| `implement-credentials` | `.qfai/assistant/step/implement-credentials/STEP.md` | Only when an acceptance test in scope needs an authenticated actor  |
| `implement-tdd`         | `.qfai/assistant/step/implement-tdd/STEP.md`         | Every owed example, Red, Green, Refactor                            |

In the `apply-settled` route, `implement-settled-edit`
(`.qfai/assistant/step/implement-settled-edit/STEP.md`) runs first, before
`implement-scaffold` and `implement-tdd`. It makes a delegated release's
hand-made edit and passes on any other work order.

Acceptance tests come in two phases. `implement-scaffold` writes them with
empty bodies before the examples are implemented; `implement-acceptance`
writes their bodies once the system's shape has settled. Unit and component
tests stay test first, in `implement-tdd`.

The completion gate above therefore leaves the acceptance bodies empty, by
design. They are written by the `write-acceptance-tests` route, or by
`implement-acceptance` run alone, and the report says which BF and AC tests
still have an empty body.

For that report or a handoff of unfinished BF/AC bodies, read
`.qfai/assistant/step/verify-repo-gate/STEP.md#acceptance-evidence-and-follow-up`.
It separates annotation proof, body states, actual behavior and execution,
and the remaining work's owner and completion criteria.

Each of these runs alone, instead of that order, when the request is not new
behaviour but a failure, a repair or upkeep:

| Step                       | File                                                    | Runs instead, when                                                        |
| -------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------- |
| `implement-diagnose`       | `.qfai/assistant/step/implement-diagnose/STEP.md`       | A failure is reported and its cause is not yet known                      |
| `implement-regression-fix` | `.qfai/assistant/step/implement-regression-fix/STEP.md` | A diagnosis found a regression that a correct existing test catches       |
| `implement-test-fix`       | `.qfai/assistant/step/implement-test-fix/STEP.md`       | A diagnosis found a defective test                                        |
| `implement-seam`           | `.qfai/assistant/step/implement-seam/STEP.md`           | An acceptance result asks for a seam before its RED can be taken          |
| `implement-bisect`         | `.qfai/assistant/step/implement-bisect/STEP.md`         | A behaviour that worked at an earlier revision fails now                  |
| `implement-revert`         | `.qfai/assistant/step/implement-revert/STEP.md`         | A bisection named a culprit that can be undone whole                      |
| `implement-minimize`       | `.qfai/assistant/step/implement-minimize/STEP.md`       | A crash came with a large input that causes it                            |
| `implement-stress-harness` | `.qfai/assistant/step/implement-stress-harness/STEP.md` | A failure comes and goes and nothing reproduces it on demand              |
| `implement-oracle-parity`  | `.qfai/assistant/step/implement-oracle-parity/STEP.md`  | The expected behaviour is set by a standard or a reference implementation |
| `implement-benchmark`      | `.qfai/assistant/step/implement-benchmark/STEP.md`      | A path is slow: once before the change, once after it                     |
| `implement-refactor`       | `.qfai/assistant/step/implement-refactor/STEP.md`       | The code is to be rearranged with no change in behaviour                  |
| `implement-retire`         | `.qfai/assistant/step/implement-retire/STEP.md`         | A recorded decision retires a mechanism                                   |
| `implement-sweep`          | `.qfai/assistant/step/implement-sweep/STEP.md`          | A widened check has to be run over the whole tree                         |
| `implement-quarantine`     | `.qfai/assistant/step/implement-quarantine/STEP.md`     | A named test passes and fails on the same code                            |
| `implement-dep-bump`       | `.qfai/assistant/step/implement-dep-bump/STEP.md`       | A dependency is to be raised to a new version                             |
| `implement-tooling`        | `.qfai/assistant/step/implement-tooling/STEP.md`        | A workflow, a script or a development tool is to change                   |
| `implement-backport`       | `.qfai/assistant/step/implement-backport/STEP.md`       | A merged change is to be carried to a release branch                      |
| `implement-acceptance`     | `.qfai/assistant/step/implement-acceptance/STEP.md`     | The flow's acceptance tests have empty bodies to write                    |

Read the `STEP.md` of the current step only, run it, then move to the next.
Each step names the common steps it runs in `requires`; read those when the
step reaches them.

Inside an `npx qfai workflow` run, the plan's stage lists the steps to run, and
its work order names the flow; this file adds nothing.

### Reviewer Gate

After the last step, run one review through `common-review-cycle`: the code
review, by `implementation-reviewer`. The review also checks for code
written only to pass a test: no value hard-coded to the test's inputs and no branch written only for the test, and a wrong test or infeasible task raised as a specification change, not worked around
(`.qfai/assistant/rule/test-layers.md#a-passing-test-is-not-the-solution`).

The review also checks that the
change adds test files sized like their neighbours, commits no scratch checks,
follows § 4 on unrequested fixes, including its exception for a necessary fix
and reporting requirement, and states any assumption it built on
(`.qfai/assistant/rule/test-layers.md#test-suite-sizing`,
`.agents/rules/minimal-implementation.md` § 4).

## Route-only procedure authoring

When the plan names `implement-procedure`, follow
`.qfai/assistant/step/implement-procedure/STEP.md`.
Business-flow invocations skip it; existing flow steps apply.

## Completion

The invocation completes on the gate of its last step once
every finding of its one review is fixed or answered. Invoked by name, it runs
`npx qfai validate --profile tdd --fail-on error --flow BF-NNNN` once, at
completion; when that fresh validate result has no test-obligation EX finding
for this BF, the invocation reports "nothing to do", and reads or writes no
ledger status. Inside a route it runs no validate: the verify stage does.
When the next step needs the user's answer, ask a question listing the next
actions, `/qfai-verify` recommended, per `.agents/rules/user-questions.md` § 6.
Completion-only reports ask nothing. Under a no-question mode, list remaining
actions instead.

## Default Autopilot Policy

- auto-decide:
  - equivalent-option pick: implementation seam, test selector, and local
    refactor that preserve the active story and contract behavior
- ask-user: critical product choices.

The BF, EX, and contract sources come from the invocation and configured tree.
If they cannot be resolved, stop at preflight and report the missing source.

project_memory:

- Select EX work from a fresh flow-scoped validator result, one EX at a time.
- BF maps to E2E; AC maps to integration or API; EX maps to every other test.
