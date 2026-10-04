---
name: pickup-issue
description: "Prepare an issue for implementation by checking requirements, repository context, and a suitable working branch."
metadata:
  category: Planning
---

# Pickup Issue

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the issue and its owning repository. Read its full description and relevant discussion; summarize the intended behavior and acceptance criteria.
2. Check business value, scope, observable acceptance criteria, and verification steps. Resolve only gaps that prevent correct implementation. Do not require a second approval when the user has already settled the scope.
3. Inspect the current branch and working tree. Reuse an appropriate feature branch, or create an isolated branch/worktree from the discovered base branch. Fetch needed refs without overwriting or stashing unrelated work. Follow the repository's branch naming conventions.
4. Identify the relevant code, tests, build commands, and implementation steps. Follow an existing plan-approval requirement if one applies; otherwise plan proportionally and proceed within the user's request.
5. If board updates are authorized and a board exists, move the issue to its actual working state and verify the change. An absent board is not a reason to block implementation.

## Deliverable

Report the issue, repository, branch/worktree, acceptance criteria, proposed checks, and any blocker. If asked only to prepare or pick up the issue, stop at that boundary. If asked to implement, continue with the development workflow.
