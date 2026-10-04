---
name: "commit"
description: >-
  v1.0.0 — Use when the user asks to commit work that already exists in a dirty
  worktree: inspect the changes, split that diff into logical commits, stage
  hunks, and create the commits. Plan every requested repository and execute
  the complete commit run in the same response. Not for work this session is
  still authoring — the `commits` skill owns that.
---

# Commit skill

Create small, reviewable conventional commits from the requested worktree(s).

## Scope, and how this differs from the `commits` skill

This skill is the **salvage** path: someone hands you an existing dirty
worktree and asks for it to be committed. You did not author those changes in
this session, so the only available grouping evidence is the diff itself, and
the steps below derive the plan from changed hunks.

The separately selected `commits` skill is the **authoring** path. When this
session is writing the code, that skill owns the work: it derives a numbered
Feature ledger from the user's request sentences and commits each Feature as it
is finished, so a commit boundary is decided before the diff exists.

The two must not run against the same work:

- Session is authoring the change → follow `commits`. Do not re-plan its
  Features from the accumulated diff, and do not defer its commits so this
  skill can batch them at the end.
- Change already exists and was not authored here → follow this skill.
- Both selected and both apparently applicable → `commits` wins for anything it
  has a ledger entry for; this skill covers only the leftover pre-existing
  changes.

Isolation, branch policy, merging, and reapplication belong to the `worktree`
skill in every case. The temporary detached worktree in step 6 is a throwaway
validation checkout, not a task worktree; create it outside the repository and
remove it in the same step.

## Workflow

1. Inspect every requested repository before staging:

   ```bash
   git rev-parse HEAD
   git status --short
   git diff --stat
   git diff --staged --stat
   git diff
   git diff --staged
   git ls-files --others --exclude-standard
   ```

   Read relevant untracked files. If anything is already staged, rebuild the
   index with `git restore --staged -- :/` and inspect again.

2. Print a numbered plan covering every changed hunk. Group by purpose, not by
   filename. Keep implementation, its focused tests, and required docs or
   installer changes together. Mark mixed files as `partial`.

3. Start plan item 1 immediately. The plan is not an approval checkpoint.
   Never ask whether to proceed or wait for confirmation.

4. Stage only the current group. Use exact paths or interactive patch mode:

   ```bash
   git add -- path/to/file
   git add -p -- path/to/mixed_file
   ```

   Never use `git add .`, `git add -A`, `git add -u`, or stage a whole mixed
   file. Check the staged and unstaged sides after partial staging.

5. Before committing, verify:

   ```bash
   git diff --staged --name-status
   git diff --staged --stat
   git diff --staged --check
   git status --short
   ```

   Confirm that every staged hunk belongs to this plan item, every staged test
   has its implementation, and later groups remain unstaged.

6. Validate the staged snapshot, not the dirty worktree. Apply only the staged
   patch to a temporary detached worktree based on the starting commit and run
   the narrowest relevant tests, lint, type, or build checks. Remove the
   temporary worktree afterward.

7. Create one conventional commit for the group, then repeat steps 4–6:

   ```bash
   git commit -m "type(scope): short description" \
     -m "Explain what this group changes and why."
   ```

   Allowed types: `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`,
   `perf`. Use the repository's configured identity. Never amend, rebase,
   reset, stash, force-push, skip hooks, or use `--no-verify`.

8. Finish by verifying `git show --stat --oneline HEAD` and `git status --short`.
   Report every hash and subject, the files or hunks in each commit, and any
   intentionally uncommitted changes with the concrete reason.

## Safety rules

- Cover every repository the user named; do not silently stop after one.
- Do not commit secrets, credentials, `.env` files, logs, caches, generated
  output, editor state, or unrelated user changes.
- Do not modify source files while composing commits; stage existing changes
  only.
- A commit must work without later commits or unstaged worktree changes.
- If no safe coherent grouping exists, stop and explain the blocker.
