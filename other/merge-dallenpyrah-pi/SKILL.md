---
name: merge
description: Merge the current PR after /learn has committed and pushed the learning file. Verifies a clean tree, open PR, up-to-date pushed head, passing required checks, and reviewability before merging with the repository's safe strategy, deleting the branch, checking out the base branch, and pulling it forward.
---

# /merge

Before rendering user-facing output, read `../_shared/plain-output.md`.

Merge the reviewed PR after the learning file has been committed and pushed.

## Preconditions

1. `/learn` has completed on this PR and pushed its learning commit.
2. The current branch is the PR branch, not `main`, `master`, or `trunk`.
3. Working tree is clean: `git status --porcelain` is empty.
4. `gh` authenticated.
5. The PR is open.

## Process

1. Identify the current branch and PR:

```bash
git branch --show-current
gh pr view --json number,url,state,baseRefName,headRefName,headRefOid,isDraft,reviewDecision,mergeStateStatus
```

Stop if:

- branch is `main`, `master`, or `trunk`
- no PR is associated with the branch
- PR state is not `OPEN`
- PR is draft
- `headRefName` does not match the current branch

2. Verify `/learn` ran for this PR.

Use the PR body to find `Closes #<issue>`, then check the current branch contains a pushed learning commit:

```bash
gh pr view --json body -q .body
git log --oneline -20 --grep "docs: capture learning for #<issue>"
git status --porcelain=v1 --branch
```

Stop if no matching commit exists. Stop if the branch status shows the local branch is ahead of upstream; tell the user to run `/learn` again or push the missing commit.

3. Verify checks are green.

```bash
gh pr checks --watch --fail-fast
```

- If GitHub reports no checks, treat that as `none-configured` and continue.
- If checks fail, surface the failing check names and stop.
- If checks are pending, wait because `--watch` blocks until termination.

4. Verify review state.

Use `reviewDecision` from `gh pr view`:

- `APPROVED` — continue.
- empty/null — continue only if the repo has no review requirement; state that explicitly in output.
- `REVIEW_REQUIRED` or `CHANGES_REQUESTED` — stop. Do not bypass review.

5. Capture the exact head commit and merge.

Use `--match-head-commit` so a race cannot merge a different commit than the one verified.

Default strategy is squash because the compound workflow produces many mechanical commits and the issue/PR preserve the history. If the repository only allows merge queues, omit the strategy and let GitHub enqueue it.

```bash
HEAD_SHA=$(git rev-parse HEAD)
gh pr merge --squash --delete-branch --match-head-commit "$HEAD_SHA"
```

If GitHub reports the repository requires a merge queue or rejects the squash strategy, do not guess repeatedly. Read the error, then use the smallest compatible command:

```bash
gh pr merge --delete-branch --match-head-commit "$HEAD_SHA"
```

Do not use `--admin`.

6. Move the local checkout to the base branch and update it.

```bash
git checkout "<baseRefName>"
git pull --ff-only origin "<baseRefName>"
```

If the local branch deletion did not happen automatically, delete it after checkout:

```bash
git branch -d "<headRefName>"
```

## Output

If the PR merged immediately, use Plain Senior output:

````markdown
## Decision
PR merged: <url>.

## Why
- merge_result=merged
- base=<baseRefName>
- head=<verified HEAD_SHA>

## Example
```bash
gh pr merge --squash --delete-branch --match-head-commit "$HEAD_SHA"
```

## Risk
None known.

## Next
Base branch <base> is up to date.
````

Then end with exactly this line and stop:

> PR merged: <url>. Base branch <base> is up to date.

If GitHub queued the PR instead of merging immediately, print the queue status using the same shape and end with exactly this line and stop:

> PR queued: <url>. GitHub will merge it when the merge queue admits it.

## Rules

- Never merge from trunk directly; this skill only merges a PR branch through GitHub.
- Never use `--admin`.
- Never merge with failing checks, unresolved changes requested, or a dirty working tree.
- Never merge a commit different from the one checked by this skill; use `--match-head-commit`.
- If GitHub queues the PR instead of merging immediately, say so and do not claim the base branch contains the changes yet.
