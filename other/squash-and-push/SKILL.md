---
name: squash-and-push
description: Squash the current branch's full history since its base into one commit and force-push with lease. Manual command — run with /squash-and-push when the user asks to squash and push the current branch as a single commit.
disable-model-invocation: true
---

# Squash and Push

Squash all commits on the current branch (since it diverged from the base branch) into one commit, then push with `--force-with-lease`.

1. **Safety + scope checks**
   - Run `git branch --show-current`; abort if on `main`/`master`.
   - Run `git status --short` and `git rev-parse --abbrev-ref --symbolic-full-name @{u}`.
   - If upstream is missing, stop and ask which base/upstream to use.
   - Run `git fetch origin main` (substitute the repo's actual default branch throughout).

2. **Commit working changes first (required when dirty)**
   - If `git status --short` is not empty, stage with `git add -A` and commit using the repo's commit-message convention.
   - Always pass the commit message via HEREDOC.

3. **Determine the full squash span**
   - Use the base branch as the root reference:
     - `BASE=$(git merge-base origin/main HEAD)`
     - `BRANCH_COMMITS=$(git rev-list --count "$BASE..HEAD")`
   - Sanity check to avoid misparsed ranges:
     - `MAIN_DELTA=$(git rev-list --count origin/main..HEAD)`
     - If `BRANCH_COMMITS` and `MAIN_DELTA` differ, stop and report the blocker before squashing.
   - The span is always the full branch history since base — including commits already pushed — never just `@{u}..HEAD`.
   - If `BRANCH_COMMITS` is `0`, report the blocker (nothing to squash) and stop.

4. **Squash into one commit**
   - `git add -A`.
   - If `BRANCH_COMMITS > 1`, run `git reset --soft HEAD~$BRANCH_COMMITS`.
   - Create one final commit in the repo's message convention, via HEREDOC.

5. **Push safely**
   - `git push --force-with-lease`.

6. **Verify + report**
   - `git status --short` (expect clean).
   - Recompute: `git rev-list --count "$(git merge-base origin/main HEAD)..HEAD"` (expect `1`) and `git rev-list --count origin/main..HEAD` (expect `1`).
   - Report branch name, new commit SHA, and confirmation of a single-commit branch.

## Hard constraints

- Never calculate the squash span from `@{u}..HEAD`.
- Never run `git reset --soft origin/main` or any non-`HEAD~N` reset target for the squash.
- Never use plain `--force`; always `--force-with-lease`.
- If conflicts or errors occur, stop and report the exact blocker before retrying.
