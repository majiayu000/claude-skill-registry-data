---
description: "Create a PR. Verify build and test pass, then run gh pr create"
user-invokable: true
---

# /pr

A skill for creating Pull Requests.

## Steps

1. **Build verification**: Run `make build` and confirm no errors
2. **Run tests**: Run `make test` and confirm all tests pass
3. **Review diff**: Check changes with `git diff main...HEAD`
4. **Generate PR title**: Create a title in Conventional Commits format (`feat(scope): description`)
5. **Generate PR body**: Generate body including a summary of changes and test plan
6. **Create PR**: Run `gh pr create --title "<title>" --body "<body>"`
7. **Display result**: Show the PR URL

## PR Body Template

```markdown
## Summary
- <bulleted list of changes>

## Test plan
- [ ] Test items

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Notes

- If build or tests fail, do not create the PR and report the problem instead
- Default base branch is `main`

## Stacked PRs

When PR B is stacked on PR A's branch (`B.base == A.head_branch`) and you merge PR A with `gh pr merge --delete-branch`, GitHub auto-closes PR B because its base branch no longer exists. Auto-closed PRs cannot be reopened (`gh pr reopen` returns "Could not open the pull request") nor have their base changed (`gh pr edit --base` returns "Cannot change the base branch of a closed pull request").

Two safe sequences:

1. **Retarget before merging upstream** (preferred when you have time):
   ```bash
   gh pr edit <B>  --base <A's base>     # B will temporarily show A's diff too — fine if A merges first
   gh pr merge <A> --squash --admin --delete-branch
   ```

2. **Recreate downstream after merging upstream**:
   ```bash
   gh pr merge <A> --squash --admin --delete-branch     # closes B
   # in a worktree on B's branch:
   git rebase --onto origin/<base> <A's-original-head-commit>     # drops A's commits, replays only B's
   git push --force-with-lease
   gh pr create --base <base> --head <B's-branch>
   ```

Do **not** use `--delete-branch` on the upstream PR if the downstream has not been retargeted — you lose the PR thread (closed PRs are still readable but lose `OPEN` semantics for review-gate and merge-queue tooling).
