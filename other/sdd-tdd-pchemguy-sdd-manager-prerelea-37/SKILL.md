---
name: sdd-tdd
description: Use when defining an SDD project's testing strategy, deriving test scenarios from accepted contracts, writing or reviewing tests, reproducing a bug, or guiding a test-first red-green-refactor cycle for a selected implementation task.
license: MIT
---

# Design tests and guide test-first implementation

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Choose the requested operation and load its references:

| Work | Load |
| --- | --- |
| Define testing strategy and scenario coverage | [testing strategy](references/testing-strategy.md) |
| Guide a feature, bug fix, or behavior change through TDD | [test-first cycle](references/test-first-cycle.md) and [writing good tests](references/writing-good-tests.md) |
| Write, revise, or review tests, doubles, or test helpers | [writing good tests](references/writing-good-tests.md) |

Use the selected TASKS or FEATURE-TASKS entry, accepted SPEC contracts, relevant design, PLAN and layout, inspected implementation, and project test commands. **sdd-manage** coordinates scope and a current **sdd-orient** handoff establishing Git eligibility, governing instructions, and ownership of dirty changes. Strategy and review can remain read-only; test edits and execution follow the authorized scope and environment.

For new or changed behavior and bug fixes, establish a test that fails for the intended reason before the production change. Observe the failure, guide the smallest implementation that satisfies the accepted contract, and refactor with checks remaining green. **sdd-tdd** owns test strategy, scenarios, test changes, and development-cycle test execution. The active implementation workflow, **sdd-implement** for main task work or **sdd-steer** for a checkpoint amendment, owns production changes and applies the GREEN and production-refactoring steps; this skill supplies the test and evidence at each handoff. A strategy-only request does not authorize implementation.

Preserve existing work when resuming. If code predates the tests, report missing test-first evidence and use characterization or a safe isolated baseline where appropriate; do not delete or reset code to reconstruct an unobserved history. Follow applicable project policy and previously authorized exceptions for work that cannot use a meaningful test-first cycle. When an exception is still required and undecided, explain the concrete limitation and defer that decision to the user.

Return the testing strategy or test changes, covered contracts and scenarios, actual RED and GREEN commands and outcomes, regression results, remaining coverage gaps, and any exception or blocker. Do not invent a failed run or infer whole-project correctness from a focused passing test. **sdd-verify** owns the verification campaign and acceptance assessment; the active implementation workflow owns completion updates, commits, pushes, and issue-closure coordination. **sdd-docs** owns documentation maintenance and **sdd-report** presents completion evidence.

This skill adapts both Superpowers TDD and its test-writing companion. See [upstream provenance and adaptation](references/upstream-provenance.md) and the included [license](LICENSE).
