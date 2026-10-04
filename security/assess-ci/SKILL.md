---
name: assess-ci
description: "Audit the repository’s CI coverage against its documented quality requirements and report evidence-backed gaps."
metadata:
  category: Quality
---

# Assess Ci

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Locate pipeline definitions and the project's documented quality requirements. Discover the CI provider rather than assuming a specific service or file path.
2. Inspect triggers, branch/path filters, required checks, runtime/tool versions, and actual commands. Classify build, unit/integration/end-to-end tests, lint, type checks, and security checks according to the project's needs.
3. Trace referenced scripts and reusable workflows. A step named test is not proof of meaningful test execution; identify what it runs and how failures propagate. Distinguish code inspection from observed run results.
4. Compare coverage with documented requirements. If no policy exists, identify observed behavior and explicitly label any suggested baseline as a recommendation. Do not invent mandatory gates or fail a repository against an unstated standard.
5. Record missing coverage, bypass paths, unreliable triggers, and failure-handling problems with concrete file/line or run evidence. Prioritize by impact and suggest a focused remedy for each gap.

## Deliverable

Write a report at the project's established report location, or a session output location if none exists. Include the evaluated revision, policy source, covered and missing dimensions, limitations, and actionable findings. This assessment does not edit pipelines, enforce new rules, or rerun jobs unless separately requested.
