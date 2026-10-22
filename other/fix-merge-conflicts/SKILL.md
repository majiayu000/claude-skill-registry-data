---
name: fix-merge-conflicts
description: "Use when the user says 'fix merge conflicts', 'resolve merge conflicts', or the current branch conflicts with its base branch. Pulls the latest base, resolves every conflict, verifies, commits, and pushes."
---

# Fix Merge Conflicts

## Purpose

Bring the current branch up to date with its base, resolve every
conflict, then commit and push.

Invoking this skill is the explicit request to commit and push for this
run, scoped to conflict resolution only. It does not carry over to any
other work in the session.

## Process

1. **Check state.** Run `git status` and `gh pr view --json baseRefName,number,url`.
   If a rebase or merge is already in progress, or the tree has
   unrelated uncommitted changes, stop and ask. If there is no PR, use
   the repo's default branch as the base.

2. **Pull the latest base.**
   ```bash
   git fetch origin
   git merge origin/<base>
   ```
   Use a merge, not a rebase, so the push never needs a force. If the
   merge is clean, skip to step 4.

3. **Resolve every conflict**, in every file and every hunk, not just
   the first. For each hunk:
   1. Read both sides and the base (`git log origin/<base> -p -- <file>`)
      to learn what each side intended.
   2. Write the result that keeps both intents. Never pick a side
      blindly.
   3. Remove all markers. Confirm with `git grep -nE '^(<<<<<<<|=======|>>>>>>>)'`.
   Regenerate lockfiles and generated files with the repo's tool. Do
   not hand-merge them.

4. **Verify.** Run lockfile consistency checks and the tests, lint, and
   type checks that cover the files touched. Confirm they pass.

5. **Commit and push** the merge to the PR branch. Never force-push
   unless the user says so. If the push is rejected, fetch, merge
   again, and retry once. Then stop and ask.

## Output

1. **Conflicts resolved:** each file and how it was resolved.
2. **Verification:** which checks ran and their result.
3. **Pushed:** the commit hash and branch.
