---
name: merge-prep
description: Prepare for merge by cleaning up and consolidating commits. Invoke only when explicitly called by user.
user-invocable: true
disable-model-invocation: false
---
# Merge Preparation

Prepare the current branch for merge into the default branch by resetting its commits and rebuilding them as a comprehensive, logically grouped set.

This skill rewrites history.
Complete the preflight checks before touching anything, and stop and ask rather than guessing at any step that names a branch, a remote, or a base commit.

## Preflight

Do all of the following before making any change.
Stop and report if any check fails; do not work around a failed check.

1. Confirm the working tree is clean:

   ```bash
   git status --porcelain
   ```

   Any output means uncommitted or untracked changes are present.
   Stop and ask the user whether to commit, stash, or discard them.
   Do not proceed with a dirty tree: `git reset --mixed` puts the branch's committed work into the same unstaged pile as those changes, and the verification in the Rebuild section can no longer tell them apart.

2. Determine the remote and the default branch instead of assuming `origin` and `main`:

   ```bash
   git remote
   git symbolic-ref --quiet refs/remotes/<remote>/HEAD
   ```

   When the symbolic ref is missing, refresh it with `git remote set-head <remote> --auto` and read it again.
   When there are several remotes, or the default branch still cannot be determined, ask the user which remote and default branch to use.

3. Confirm the current branch is not the default branch:

   ```bash
   git rev-parse --abbrev-ref HEAD
   ```

   Stop if it matches the default branch; this skill rewrites the checked-out branch and must never do that to the default branch.

4. Record whether the branch has an upstream, because that decides whether the rewrite needs a force-push later:

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name '@{u}'
   ```

## Steps

1. Check all README files and update.
   Commit any changes made.
2. Make a backup branch at the current HEAD.
   Use a name that identifies the branch and the date, and report the name to the user.
3. Review all commits in the delta between current HEAD and the default branch identified in preflight.
4. Plan a new set of commits, grouping files logically.
   Present the plan to the user before resetting.
5. Verify the backup, then reset the branch:
   - Confirm the backup branch resolves to the same commit as HEAD:
     `git rev-parse HEAD` and `git rev-parse <backup-branch>` must print the same hash.
     Stop if they differ or if the backup branch does not exist.
   - Set `BASE=$(git merge-base HEAD <remote>/<default-branch>)` using the values from preflight.
   - Show the user the backup branch name, `BASE`, and the number of commits about to be replaced, then ask for explicit confirmation to proceed.
   - Run `git reset --mixed "$BASE"` so all branch changes become unstaged working-tree changes (no commits removed from backup).
6. New logical commits:
   - Stage and commit files in separate commits by theme.
   - Use conventional, descriptive, multi-line commit messages.
   - Pass a multi-line message with `git commit -F -` rather than `\n` inside `-m`; see the make-commit skill for the mechanics.
7. Compare the updated branch against the backup to make sure there is no diff:

   ```bash
   git diff --stat <backup-branch>
   ```

   Empty output means the rebuilt branch has identical content.
   Any output is a defect in the rebuild; investigate and fix it before continuing, and never resolve it by editing the backup.
8. Create a suggested PR description as a markdown file in the ./tmp dir.
   Name the file appropriately; e.g. `PR_DESC_<branch_name_normalized>.md`
   - Do not include references to the backup branch.
   - Do not include a list of the commits.

## Publishing the Rewritten Branch

Do not push as part of this skill; report the state and let the user decide.

When the branch recorded an upstream in preflight, its history no longer matches the remote, so publishing it requires `git push --force-with-lease` rather than a plain push.
Tell the user that explicitly, and warn that anyone else who has checked out or built on the branch will need to reset to the rewritten version.
Never force-push without the user asking for it in that session.

Keep the backup branch until the user confirms the rewritten branch is merged or accepted.
