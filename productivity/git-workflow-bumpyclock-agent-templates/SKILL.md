---
name: git-workflow
description: Use when managing Git commits, branches, pull requests, conflicts, or CI checks.
---

# Git workflow

Follow repository conventions for branches, commit messages, PR templates, and merge methods. Without a convention, choose a concise format appropriate to the change.

For verification, use [Programming](../programming/references/verification-before-completion.md). This skill owns Git operations, not additional verification gates.

## Global rules

- Perform routine local Git operations within the authorized task without separate approval for each command.
- Use authorization already present in the conversation. Require explicit authorization for destructive actions and published history rewrites.
- Before an external action, establish that the user's request authorizes it. A local edit request alone does not authorize publication.
- Inspect the relevant repository state before a write. Preserve unrelated work, including changes already in the index.
- If an operation would overwrite unrelated work, stop and ask for direction.
- Use `gh` for GitHub operations. Confirm the target repository and account before an external write.

## Task guides

Read only the guide relevant to the task.

| Task | Read |
| --- | --- |
| Merge a PR, resolve conflicts, repair CI | `merge-and-ci.md` |
| Create or update a changelog | `add-changelog.md` |
| Create an interactive HTML PR walkthrough | `../pr-review-canvas/SKILL.md` |

## Commits

Create coherent commits that contain only intended changes. Inspect the complete proposed commit, including any existing staged changes. Select explicit paths or hunks to exclude unrelated work.

If a hook fails, address its cause within the authorized scope. Preserve the index when the failure requires user action.

Explain the change and its reason in the commit message. Add detail when the subject alone does not explain a material decision or consequence.

Amend agent-created, unpublished commits when the amendment belongs to the authorized task. Use session evidence to establish ownership. Obtain explicit authorization before changes to published or unrelated commits.

## Branches

Choose branch names and update methods from repository policy and branch ownership. Preserve collaborators' work when you choose merge or rebase. Apply the authorization rules above to any published history rewrite.

## Cleanup

Identify the actual base branch and exact deletion targets. Check for unique commits and active worktrees before branch deletion. Delete only branches within the authorized cleanup scope.

Report the operation result and any unresolved blocker. Distinguish local completion from push, merge, and CI status.
