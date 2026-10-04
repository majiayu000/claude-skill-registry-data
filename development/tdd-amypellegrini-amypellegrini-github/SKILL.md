---
name: tdd
description: "Implement one acceptance criterion through a verified red, green, and refactor cycle using the project’s test tools."
metadata:
  category: Development
---

# Tdd

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Select one explicit acceptance criterion or a focused behavior from the agreed task. If none is specified, identify the next uncovered criterion from the issue and current diff. Clarify a criterion that cannot be tested as written. Follow any existing planning requirements without asking for approval already given.
2. Use the repository's test framework and a suitable test boundary. Write a small test that exercises the intended behavior, not the implementation's exact wording or structure.
3. Run the test and confirm a failure caused by the missing behavior. Fix setup/import errors before treating the run as red. If it passes immediately, inspect whether the behavior already exists and whether the test would catch a relevant defect; use a safely reversible local mutation when useful and always restore it before continuing.
4. Make the smallest implementation change that produces the intended behavior. Rerun the targeted test and relevant surrounding checks. Do not broaden unrelated behavior merely to make a weak test pass.
5. Refactor only the code involved in the criterion while keeping relevant tests green. Run the affected suite after meaningful refactors and complete the project's required checks.
6. Commit the completed concern when that is part of the authorized workflow, following repository conventions; otherwise leave a reviewable diff. A missing commit skill does not prevent creating a focused commit with the available Git tools.

## Deliverable

Report the criterion, red/green evidence, final checks, changes or commit, and any limitations. One invocation covers one criterion; return control to the caller instead of silently taking on the remaining feature.
