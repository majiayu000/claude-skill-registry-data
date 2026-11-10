---
name: beads-merge-cleanup
description: Finish completed Beads issue work by committing a feature branch, merging it back to the base branch, closing the bead, and cleaning up local worktree and branch state. Use when the user asks to commit/merge/close a Beads issue, clean up a Beads worktree, or complete a bd issue workflow.
---

# Beads Merge Cleanup

## Overview

Complete a Beads-backed development branch with evidence: verify, commit, merge to the base branch, verify again, close the bead, then remove local worktree and branch resources.

## Workflow

1. Identify the bead and branch.
   - Prefer an explicit bead ID from the user.
   - Otherwise infer from the current branch/worktree and confirm if unclear.
   - Stop and report the branch unless it is a **safe branch name** before running any command with it: run `node <script> -- '<branch>'`, where `<script>` is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs) resolved from this skill's directory, and continue only on exit 0. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check.
   - Run `bd show <id>`.
2. Inspect git state in the feature worktree.
   - `git status --short --branch`
   - Review the relevant diff.
   - Stage only intended files.
3. Verify before commit.
   - Run focused tests/builds that prove the bead acceptance criteria.
   - Run `git diff --check` or `git diff --cached --check` as appropriate.
   - Stop on failure and report the blocker.
4. Commit the feature branch.
   - Use `git-commit` conventions.
   - Use a conventional commit message tied to the bead scope.
   - Do not include unrelated or user-owned changes.
5. Merge back to the base branch.
   - Prefer `main` unless local context says otherwise.
   - From the main checkout, run `git merge --ff-only <feature-branch>` when possible.
   - Do not rebase or force-push unless explicitly requested.
6. Verify on the merged base branch.
   - Re-run the same focused verification used before commit.
   - Compile/build if the touched files require it.
7. Close the bead only after merge and merged-branch verification pass.
   - Add a final `bd note` with commit hash and verification summary when useful.
   - `bd close <id> --reason "Merged <summary> in <hash>."`
8. Clean up local resources.
   - Follow `../worktree-runtime-cleanup/SKILL.md` for the worktree path. If that file is absent, say so in the report.
   - Remove the worktree from a safe directory, never from inside the worktree.
   - `git worktree remove <path>`
   - `git worktree prune`
   - Delete the local feature branch after the worktree is removed: `git branch -d <branch>`.
9. Report final state.
   - Commit hash, base branch status, tests run, bead status, cleanup result, and next ready bead from `bd ready`.

## Safety Checks

- If the feature branch is dirty after commit, stop before merging.
- If the merge is not fast-forward, stop and explain the conflict or divergence.
- If merged-branch verification fails, do not close the bead or clean up the worktree.
- If branch/worktree removal is refused, report the exact blocker.
- Never delete a remote branch unless the user explicitly asks.
- Treat cleanup as destructive; only do it when the user asked for cleanup or confirmed the completion workflow.

## Sandbox Notes

Git operations that update `.git` refs or worktree registrations may require escalation in restricted sandboxes. If a command fails with a read-only `.git` lock/ref error, rerun the same necessary command with approval rather than changing the workflow.
