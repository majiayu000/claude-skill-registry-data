---
name: commit-and-push
description: "Commit the requested changes and push the intended branch while respecting remote and branch protections."
metadata:
  category: Delivery
---

# Commit And Push

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Inspect the working tree, staged changes, branch, remote, upstream, and repository rules. Use the atomic-commit procedure: stage only task changes, follow local message conventions, and run applicable hooks and checks.
2. Create the authorized commit and verify that it exists before attempting a push. If there are no changes, determine whether there are already committed changes the user intended to push; report a no-op when there is nothing to send.
3. Confirm the target remote and branch from the request and Git configuration. If an upstream is missing, set it for an unambiguous new feature branch as part of the requested push; ask when the destination is ambiguous.
4. Respect protected/default-branch restrictions. Do not infer permission to bypass branch protections or force-push from a general shipping request. Use an ordinary push by default; on divergence, inspect and reconcile within scope rather than overwriting remote history.
5. If the staged change includes submodule pointers, verify referenced commits are available on their intended remotes before pushing the containing repository. Skip this check for repositories without such changes.
6. Verify the remote branch's resulting commit and report partial outcomes accurately, such as commit succeeded but push failed.

## Deliverable

Report local commit, remote branch, push result, and any remaining action. Do not open or merge a PR unless that is also requested.
