---
name: assess-test-pyramid
description: "Assess test distribution and meaningful coverage using the repository’s own testing strategy."
metadata:
  category: Quality
---

# Assess Test Pyramid

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Locate the documented testing strategy and definitions of test layers. Discover the language, runners, test directories, and test-selection rules. Avoid assuming that file names identify behavior accurately.
2. Inventory first-party tests, excluding generated, vendored, and dependency trees. Inspect representative tests and classify by actual isolation boundary and dependencies. Keep an unknown category when a classification cannot be supported.
3. Count by a consistent unit, such as test cases or test files, and state that unit. Avoid double-counting parameterized or multi-runner tests. Report layer totals and percentages against the appropriate denominator.
4. Compare with the project's stated expectations, not an invented universal percentage. If no strategy exists, describe the observed distribution, state any heuristics used, and recommend documenting the intended balance.
5. Identify behavioral gaps, brittle end-to-end dependence, duplication, and critical integration paths with concrete examples. A distribution shape alone is not proof of good or bad coverage; consider the product's architecture and risk.

## Deliverable

Produce an auditable report with the revision, counting method, policy source, classifications, distribution, limitations, and prioritized recommendations. Use the project's report format or a readable Markdown report. Do not add tests or alter thresholds as part of the assessment.
