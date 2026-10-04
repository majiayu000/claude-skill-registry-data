---
name: commit
description: "Create focused Git commits with accurate messages and verification appropriate to the change."
metadata:
  category: Delivery
---

# Commit

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Inspect repository status, branch, staged diff, and unstaged diff. Identify which changes belong to the current task; preserve unrelated edits and existing staged work.
2. Group changes by independently understandable concern. Stage explicit files or hunks; avoid a blanket add when other work is present.
3. Run the required checks for the concern and inspect the staged diff for accidental files or credentials. Do not bypass failing hooks. Report environmental blockers separately from code failures.
4. Use the repository's commit-message convention. If none is established, use a concise imperative subject; Conventional Commits is an optional fallback, not a universal requirement. Include the issue reference where appropriate.
5. Commit only when requested or already authorized. Amend an existing commit only when that is within scope; do not rewrite shared history by default.
6. Verify the resulting commit and remaining working-tree state. If a hook fails, fix an in-scope problem or report it; do not claim the commit succeeded.

## Deliverable

Return commit hashes, purposes, checks, and remaining changes. A commit request does not imply permission to push or merge.
