---
name: qa-assessment
description: "Run a combined assessment of test strategy, CI coverage, and commit hooks, then consolidate actionable findings."
metadata:
  category: Quality
---

# Qa Assessment

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the assessment scope and revision. Run all three dimensions unless the user selects a subset: test distribution, CI coverage, and pre-commit hooks.
2. Use assess-test-pyramid, assess-ci, and assess-pre-commit when installed. If they are absent, inspect tests and their isolation boundaries, pipeline triggers/commands and failure behavior, and hook setup/enforcement directly. Do not report an unexamined dimension as passed.
3. Use a QA agent when available and permitted, or perform the assessment locally. Each dimension must name its policy source, observed evidence, and uncertainty. When no policy exists, separate the observed baseline from suggested improvements.
4. Consolidate duplicate findings and prioritize by user impact, likelihood, and evidence. Size each recommended action so it can become a focused issue. Avoid forcing unrelated issues into a particular tracker.
5. Save the report to the established project location or a session output directory. For each finding include the problem, evidence, consequence, proposed scope, and acceptance/verification guidance.

## Deliverable

Return a per-dimension result and one consolidated report with actionable findings and limitations. Do not edit implementation, create issues, post messages, or change project policy unless those actions are also authorized.
