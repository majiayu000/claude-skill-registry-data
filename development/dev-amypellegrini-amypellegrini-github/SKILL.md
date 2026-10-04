---
name: dev
description: "Drive a scoped feature through implementation, validation, and a reviewable handoff using the target repository’s conventions."
metadata:
  category: Development
---

# Dev

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve whether the request is an existing issue, a new feature, or rework on an existing PR. Inspect the appropriate repository and preserve the user's existing work.
2. Establish observable acceptance criteria and scope. Reuse the business-analyst or pickup-issue skill when available; otherwise clarify requirements and prepare an appropriate branch/worktree directly. An issue tracker is optional for a local implementation request.
3. Identify the project's build/test capabilities and plan proportionally. Report a missing capability rather than silently skipping required validation or imposing a new framework.
4. Implement acceptance criteria incrementally. Use a TDD cycle where suitable: establish the expected failure, implement behavior, refactor, and run relevant checks. For changes where an automated test is inappropriate, use the project's accepted verification method and explain its limits.
5. Inspect the complete diff against scope, perform required validation, and address concrete failures. Group commits by concern when committing is authorized.
6. If a PR was requested, open or update it, verify the current-head CI status, and address authorized review feedback. If only local changes were requested, provide the diff and validation without publishing.
7. Stop at the requested reviewable handoff. Report pending checks, review, QA, or human acceptance rather than claiming the feature is merged or accepted. A general implementation request does not authorize merge, deployment, or issue closure.

## Runtime and deliverable

Use an installed development agent if the runtime supports it and delegation is permitted. Otherwise execute locally. Companion skills are conveniences, not hidden prerequisites. Return the issue/task, branch/worktree, changes, validation, PR if any, and remaining gates.
