---
name: pr-flow
description: Branch naming, chained PRs (>400 lines), PR template, review. Load before opening a PR.
triggers:
  - pr
  - "pull request"
  - branch
  - "stacked pr"
  - "chained pr"
  - review
---

# PR flow

## Branch naming

`<type>/<short-kebab-slug>` where type matches the commit convention.

Examples:
- `feat/native-multiplex`
- `fix/pty-resize-race`
- `chore/bump-tauri`
- `docs/agents-readme`

Branch from `main`. Rebase before opening the PR (no merge commits).

## Size

- **Default target**: ≤400 lines of diff (excluding generated, lock files, snapshots).
- **>400**: open **chained PRs** (stacked). One coherent slice per PR; each builds on the previous.

Reasons:
- Reviewers do a worse job on big PRs (well-documented).
- Smaller PRs ship faster, get unblocked faster.
- Bugs are easier to bisect.

Use [Graphite](https://graphite.dev/) or `git rebase --interactive` to manage stacks.

## When ≤400 lines is impossible

Sometimes a coherent change genuinely needs to land atomically (e.g., a schema migration + its consumers). In that case:

1. Open the PR with `size:exception` label.
2. Justify in the description: *why* this can't be split.
3. Get explicit maintainer approval before merging.

Don't abuse the exception. Most "atomic" changes can split if you think hard.

## PR description template

```markdown
## Summary

- Bullet 1: what changed (1 sentence)
- Bullet 2: why it matters
- Bullet 3 (optional): any tricky decision worth flagging

## Test plan

- [ ] Manual repro step 1
- [ ] Manual repro step 2
- [ ] `cargo test` passes
- [ ] `cargo clippy --all -- -D warnings` clean
- [ ] `pnpm test` passes
- [ ] [for UI changes] screenshot/recording attached

## Refs

Closes #42 (or Refs #42 if partial)
```

Closes-vs-Refs:
- `Closes #N` — auto-closes the issue on merge. Use when this PR completes the issue.
- `Refs #N` — links without closing. Use for partial work on an epic.

## Review

- Self-review first. Read your own diff in the GitHub UI before requesting review.
- Tag the right people. For SDD changes: the maintainer plus anyone who reviewed the spec.
- Don't address every comment with code — sometimes "good catch, I'll handle this in a follow-up issue" is the right answer.

## Merge

- **Squash merge** to `main`. Commit message = PR title (Conventional).
- PR body becomes the squash commit body (optional cleanup).
- Branch auto-deletes on merge (`deleteBranchOnMerge=true`).

## After merge

- Update the related issue/epic with a comment: "Landed in #N".
- If the change unblocks others, ping them.
- If the change reveals a follow-up bug or refactor, open a fresh issue — don't tack it onto an unrelated PR.

## Don't do

- ❌ `git push --force` to `main`. Ever.
- ❌ Force-push to a PR branch after review started (rewrites review context). If you must, leave a comment.
- ❌ Skip CI. Don't merge with red CI; fix the build.
- ❌ Merge your own PR without review (unless it's a docs typo and the maintainer approved that workflow).
