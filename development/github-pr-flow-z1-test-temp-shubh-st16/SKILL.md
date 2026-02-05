---
name: github-pr-flow
description: manage branches and full pull request lifecycle, from creation to merge
---

## What is it?

The **PR Flow Skill** handles the logistics of code contribution: creating branches, opening Pull Requests, synchronizing branches, and merging.

## Success Criteria
- Branch exists before PR creation.
- PR titles follow [Conventional Commits](../github-kernel/references/CONVENTIONAL_COMMITS.md).
- PR description clearly states the changes.
- Syncing (updating) branches is performed when conflicts occur or before merge.
- Merges are performed only after approvals and passing checks.

## When to use this skill

- "Create a new branch for feature X."
- "Open a PR for my current changes."
- "Update this PR branch with the latest main."
- "Merge PR #50."

## What this skill can do

- **Branch Management**: Create feature branches from specific bases.
- **PR Creation**: Open Draft or Ready-for-review PRs.
- **Maintenance**: Update PR branches (sync with base) using `update_pull_request_branch`.
- **Conclusion**: Merge PRs (squash, merge, rebase).

## What this skill will NOT do

- Review code (use `github-review-cycle`).
- Modify file contents (use `github-kernel` tools like `create_or_update_file`).
- Run CI/CD checks (it only views status).

## How to use this skill

1. **Branch**: Always start by ensuring a branch exists (`create_branch`).
2. **Commit**: (Performed via file editing tools, not this skill).
3. **PR**: Create the PR (`create_pull_request`).
4. **Sync**: If CI fails due to conflicts or age, use `update_pull_request_branch`.
5. **Merge**: When approved and green, use `merge_pull_request`.

## Tool usage rules

- **Conventions**: PR Titles should follow [Conventional Commits](../github-kernel/references/CONVENTIONAL_COMMITS.md) (e.g., `feat: new login flow`).

- **Creation**: `create_branch` -> `create_pull_request`.
- **Updates**: `update_pull_request` (metadata) or `update_pull_request_branch` (git sync).

- **Merge**: `merge_pull_request` (Prefer `squash` for features, `merge` for long-lived branches).

## Examples

See [references/examples.md](references/examples.md) for compliant PR flow examples.

## Limitations

- Cannot resolve merge conflicts automatically (requires manual or file-edit intervention).
- Cannot bypass branch protection rules.
