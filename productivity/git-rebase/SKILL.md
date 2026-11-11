---
description: Rebase the current branch on master and resolve the conflicts
model: haiku
---

# Goal
- Rebase the current branch on `master` with `i git_rebase_master`, resolve every
  conflict, and run `git rebase --continue` until the rebase finishes

# Workflow

## Check the Starting State
- Confirm no rebase is already in progress:
  ```bash
  > ls -a .git | grep -E "rebase-merge|rebase-apply"
  ```
  - If a rebase is in progress, skip to `## Resolve the Conflicts`
- Confirm the current branch is not `master`:
  ```bash
  > git branch --show-current
  ```

## Start the Rebase
- Run the invoke task:
  ```bash
  > i git_rebase_master
  ```
- If the task finishes without conflicts, go to `# Verification`
- If the task stops with conflicts, go to `## Resolve the Conflicts`
- If the task does not exist or fails for another reason, stop and report the
  error to the user

## Resolve the Conflicts
- List the files with conflicts:
  ```bash
  > git diff --name-only --diff-filter=U
  ```

### Ignore the `helpers_root` Conflict
- `helpers_root` is a submodule, so Git reports a conflict on its pointer
- Do not resolve it, do not update the submodule, and keep it as it is in the
  working tree:
  ```bash
  > git add helpers_root
  ```
- Do this only for the path `helpers_root`, never for files inside it

### Resolve the Other Conflicts
- For every other file with conflicts, follow
  `.claude/skills/git.merge_conflicts/SKILL.md`
  - The operation in progress is a `rebase`
  - Skip its step `## Finalize the Operation`: this skill runs
    `git rebase --continue` below
  - Keep its rule to ask the user when a conflict is ambiguous
- Note: in a rebase, `<SOURCE>` is the branch being replayed (the user's commits)
  and `<TARGET>` is `master`

## Continue the Rebase
- Once no file has conflicts, continue without opening an editor:
  ```bash
  > GIT_EDITOR=true git rebase --continue
  ```
- Calling this skill is the user's permission to run `git rebase --continue`
- If Git stops again on the next commit with new conflicts, go back to
  `## Resolve the Conflicts`
- Repeat until `git status` reports that no rebase is in progress

# Constraints
- Do not run `git rebase --abort` or `git rebase --skip` unless the user asks
- Do not skip hooks (e.g., `--no-verify`)
- Do not push: a rebase rewrites history, so tell the user that the next push
  needs `--force-with-lease`
- Do not commit anything other than what `git rebase --continue` creates

# Verification
- [ ] No rebase is in progress:
  ```bash
  > ls -a .git | grep -E "rebase-merge|rebase-apply"
  ```
- [ ] No conflict markers remain:
  ```bash
  > git grep -n '^<<<<<<<\|^>>>>>>>'
  ```
- [ ] The working tree is clean, apart from files that were not clean before the
  rebase:
  ```bash
  > git status
  ```
- [ ] The branch contains the tip of `master`:
  ```bash
  > git log --oneline -1 master
  > git merge-base --is-ancestor master HEAD && echo OK
  ```
