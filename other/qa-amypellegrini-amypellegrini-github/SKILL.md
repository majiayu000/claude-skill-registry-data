---
name: qa
description: "Coordinate either a repository quality assessment or acceptance-criteria verification of a specific feature."
metadata:
  category: Quality
---

# Qa

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Choose the mode

- A repository quality request selects static assessment: testing strategy, CI coverage, and commit hooks, or the dimension the user names.
- An issue, feature branch, or request to test behavior selects dynamic verification against acceptance criteria.
- If the request is materially ambiguous, ask which outcome is wanted; do not silently substitute code inspection for running the feature.

## Procedure

Use an installed QA agent when the runtime supports it and delegation is permitted. Otherwise perform the workflow directly. For static assessment, follow qa-assessment: inspect the three dimensions, compare to documented standards, and consolidate evidence-backed gaps. For feature testing, follow qa-test: resolve the exact revision, define scenarios from the criteria, execute in the appropriate environment, and record pass/fail/blocked outcomes.

If companion skills are absent, use those same procedures with the available project tools. Keep implementation unchanged, distinguish suggested standards from required ones, and never mark unavailable testing as a pass. Save a report with the evaluated revision, evidence, findings, and limitations. External reports and board transitions require authorization and must follow the target project's actual workflow.

## Deliverable

State the chosen mode and scope, findings/verdict, report path, and next action. Recommendations and QA passes do not themselves authorize a merge, issue closure, or human acceptance.
