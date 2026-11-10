---
name: software-development
description: Use to implement code additions or changes, bug fixes, and refactoring. Use Simple Design and small feedback cycles, with TDD techniques when selected or independently required. Do not use for specification work, consultation, investigation, or document creation alone.
---

# Develop software through small feedback cycles

Work within the requested purpose and approved execution scope. `docs/` below refers to the working repository.
Read material corresponding to the stage. Do not add unrelated UI/performance validation or design patterns.

- For responsibility, dependency, or comment design decisions: [Responsibilities, contracts, and comments](references/design.md).
- For domain rules, shared external contracts, or acceptance conditions: [Shared understanding and acceptance conditions](#shared-understanding-and-acceptance-conditions). Reuse agreed specifications.
- For tests starting from assertions, test layers, reproducibility, UI, or performance validation design: [Change units and reproducible validation](references/testing.md).
- Before the first Navigator request for code changes: [Internal Driver/Navigator communication](references/agent-communication.md). Follow common application/stop conditions and share the contents with the Navigator.
- When continuation with a required Navigator is impossible: pause dependent code changes, read [Handoff and rechecking](references/navigator-recovery.md), and transfer as much context as possible to a new Navigator without waiting for user confirmation. Not needed for ordinary initial launch.
- For continued checking requests to the same Navigator in GitHub Copilot CLI: [Runtime-specific implementation](references/copilot-cli-pairing.md). Do not require the same tools or arguments in other runtimes.

## Execution scope and completion

- Before editing, reuse a saved and verified Issue plan or record the purpose, scope, success conditions, and validation. Retrieve the saved body, check agreement and display, and present its URL. Planning alone does not approve implementation; retain clear execution requests without asking again for the same scope.
- Confirm permission before publishing unpublished information, identifying the necessary content and destination. Continue adjustments within the approved purpose and success conditions; confirm changed purpose, outcomes, acceptance conditions, external impact, or authority before dependent work.
- Check repository instructions, current diffs, worktrees, and required main checks. Protect other sessions' work and prepare a task branch before editing. Recover failing main before ordinary subsequent work.
- Deliver approved changes through commits, push, a draft PR, required CI, conflict resolution, and ordinary review of the latest HEAD. Confirm successful required CI and no conflicts before each ordinary review request, including after revisions. Preserve required approvals and checks; do not substitute pair checks for PR review. Honor explicit stopping points.
- Use the repository's permitted squash or merge-commit method, preserving the final PR title and body verbatim. Do not use rebase merging. Confirm actual-main checks after integration, synchronize, and clean up the task branch. Failed or unobtainable results remain incomplete; report actual validation and any remaining restrictions.

## Start with a story

Build systems and features story-first: before design, describe who can do what, in which situation, after completion. If stories or acceptance conditions are unsettled, organize concrete examples and questions for people with the relevant knowledge and decision authority. Reuse existing agreed stories; connect technical fixes or cleanup to existing purposes and expected results.

## Evolve design from current requirements

Make XP's five values concrete in shared ToDos, short tests, and pair feedback through the [Mapping in the bundled design material](references/design.md#using-the-five-xp-values-in-implementation-decisions). For Simple Design, check that current contracts and tests are satisfied, intent is clear, duplication of the same rules decreases, and unnecessary elements are not added. Follow YAGNI; do not preemptively add interfaces, extension points, or configuration for hypothetical future features. Introduce structure needed by actual requirements or feedback in small Refactor steps. Use [Design material](references/design.md#simple-design-and-yagni) for the detailed decision criteria.

## Starting XP alone

For learning or practice by one human, propose beginning with this Skill's small TDD cycles, design evolving from current requirements, and short feedback from existing automated builds and tests. Distinguish human numbers from AI Driver/Navigator roles, and preserve existing staged checks, ordinary review, required CI, and integration conditions.

- Follow “Start with a story,” dividing work by small meaningful user outcomes and completion conditions. Do not use commit counts or one TDD iteration as outcome units.
- When selecting automated validation, prefer existing fast checks for small changes and slower overall checks at useful stages. Execution remains discretionary unless independently required. CI is frequent integration and validation of shared code; small commits or pushes alone do not achieve it. Complete [integration and main checks](#execution-scope-and-completion) within the approved scope. Releases deliver something users can actually use; distinguish integration, deployment, and release, and follow existing publication permission.
- For ongoing personal work or planning consultation, propose choosing small outcomes and completion conditions to deliver at the week's start, and briefly reflecting on results, difficulties, and one next change at week's end. Reuse existing Issues and ToDos; do not require weekly rituals or dedicated documents for every short code task. Follow existing procedures for reassessing plans between integration units.
- Separate required outcomes from work to do if time allows. If time is insufficient, adjust scope without dropping agreed outcomes, required tests, or review. Confirm with the requester before reducing agreed outcomes or acceptance conditions; do not arbitrarily move them to optional.
- Humans should choose sustainable work including rest rather than push through fatigue. Agents do not infer fatigue; when users request rest or interruption, respond by preserving confirmed results, incomplete items, and the next step. Do not create unrequested reminders or weekly automations.

## Design scope and change decomposition

Write current working guidance for new contributors in documents, historical judgments and reasons in self-contained PRs/commits, and Why-not constraints beside the relevant code. Let code express behavior and tests express contracts. Current policy has no prescribed directory. When judging design policy, impact, change size, or decomposition into Sub-issues or small integration units, read [Responsibilities, contracts, and comments](references/design.md#change-scope-and-decomposition). If scope grows during implementation, reassess decomposition and [execution scope](#execution-scope-and-completion) before exceeding approval.

## Shared understanding and acceptance conditions

Before implementation, organize purposes, rules, representative examples, and unanswered questions, and define corresponding acceptance conditions. Distinguish existing agreements from assumptions; do not settle unagreed business decisions through agreement between AIs.

When adding or changing domain rules, even agreed ones, save `docs/behavior/<feature-name>.feature.md` before implementation. Use OKF v0.2 YAML frontmatter with a nonempty `type`, plus `title` and `description`, and [Markdown with Gherkin](https://github.com/cucumber/gherkin/blob/main/MARKDOWN_WITH_GHERKIN.md) in the repository's English or Japanese language. Preserve existing metadata and sources. Separate rules from concrete scenarios; express observable outcomes rather than internal classes or UI click sequences. Do not unnecessarily rewrite correct existing specifications; keep mappings to tests traceable. For external technical contracts, use existing authoritative API specifications and schemas where appropriate.

## Test-driven development (TDD)

These are techniques for selected TDD work, not a universal PR validation-execution requirement. Execution, method, scope, rigor, and timing are discretionary unless the task or repository independently requires them. Describe `Not run`, partial checks, or post-merge plans accurately. Never claim Red/Green execution that did not occur. Required CI and explicitly agreed acceptance conditions remain required.

For each small change, connect agreed behavior to [applicable preconditions, postconditions, and invariants](references/design.md#expressing-agreed-behavior-as-contracts), then to [observable tests](references/testing.md#mapping-contracts-to-observable-tests) and minimal implementation. Reuse existing agreements and identify only relevant conditions; preserve the incremental scope below.

Require black-box tests of specified behavior at every selected test level and exclude tests of tests; follow [Testing boundaries and cleanup](references/testing.md#black-box-tests-at-the-intended-boundary).

For incremental design, first list representative normal paths in a ToDo list including test items. Include variants, boundaries, and failure conditions only as needed for explicit requirements, existing contracts, confirmed defects, or minimal protection against concrete risks, without covering imaginary cases. Begin bug fixes with reproduction tests, without using incremental design to omit existing behavior protection or necessary design improvements.
Do not implement all tests at once; repeat the following one item at a time from the list. In pair work, Driver and Navigator evolve the same shared ToDo list and discuss the next single item and its selection reasons. This skill defines TDD targets and validation; the target repository's pairing guidance governs roles, edit authority, review boundaries, and stop conditions.
For changes only to internal technical processing, do not create feature documents; write necessary specifications in tests.

1. **Red**: As test-first work, express expected post-implementation behavior in executable tests before the corresponding implementation code. Use assert-first: write the assertion that must ultimately pass first, then add necessary target operations and setup. Confirm failure because the specification is unmet.
2. **Green**: Implement the minimum that passes the new test and existing related tests. Do not anticipate unrequired features or generalization.
3. **Refactor**: Improve implementation and test design while keeping Green. If no improvement is needed, do not add changes; proceed to the next test.

- Prefer fast unit tests, choosing contract, integration, or acceptance tests according to the defect's nature. If actual DB or communication boundaries cause the problem, do not substitute only mocks unable to detect it.
- Do not treat environment deficiencies or test errors as confirmed Red.
- For behavior-preserving cleanup, first confirm existing test coverage and success. Reuse sufficient tests; if insufficient, supplement them from assertions of existing specifications and confirm success before cleanup. Keep Green; do not create additional tests or intentional failures for formality.
- Do not achieve success by weakening assertions or copying implementation output directly into expectations. Compare newly discovered cases with current scope, adding only those needed for current requirements and contracts to the ToDo list. Do not make future improvements mandatory now, or substitute another recorded item for fixes establishing the current stage or regressions.

## Validation and reporting

Read [Change units and reproducible validation](references/testing.md#reproducing-and-reporting-defects) for reproduction tests, specification mappings, test layers, and exploratory/acceptance validation. Report executed tests, Red / Green, other validation, and unverified scope, without treating unexecuted checks or environment deficiencies as success.
