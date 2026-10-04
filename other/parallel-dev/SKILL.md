---
name: parallel-dev
description: "Coordinate multiple independent work items with isolated working trees and explicit per-item handoffs."
metadata:
  category: Development
---

# Parallel Dev

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the requested work items and owning repositories. Identify dependencies, shared files, existing branches/PRs, and whether each item is new work or rework. Do not assume a parent repository, submodules, or a fixed set of child projects.
2. Reuse appropriate existing worktrees for rework; create distinct feature branches and worktrees for new independent items from each repository's discovered base. Use a writable scratch location and preserve active checkouts and uncommitted changes.
3. Parallelize only independent work when the runtime offers workers and the session permits delegation. Respect available concurrency. Otherwise process the items sequentially and say so; do not pretend workers were spawned.
4. Give each worker its exact repository/worktree, issue criteria, scope, local instructions, relevant checks, and authorization boundaries. A worker's report must distinguish implementation, checks, commits, and any PR actually created.
5. Follow the dev workflow for each item: clarify blocking gaps, implement criteria, verify relevant behavior, and provide the requested local or PR handoff. Discover generated-file and synchronization rules from each project; do not invent cross-repository file paths or scripts.
6. Track results and surface shared-file conflicts, cross-repository compatibility, and dependency ordering. Reconcile only within authorized scope; avoid concurrent edits to the same checkout or shared generated artifacts.
7. Verify each reported result against its current revision and check status. Mark blocked or incomplete items explicitly. Do not promote tracker states based only on a worker's optimistic summary.
8. Preserve worktrees containing active work. Remove only clean, no-longer-needed temporary resources created for this batch, and report remaining paths.

## Deliverable

Return a table of work item, repository, branch/PR, current SHA, checks, outcome, and next action. Implementation workers stop at reviewable work. Merging, deployment, issue closure, and optional parent-pointer updates require their own authorization and completion gates.
