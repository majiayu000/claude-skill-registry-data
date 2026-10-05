---
name: do
description: Execute a work plan. Make changes, run validation, commit.
---

# Do

You are executing a work item. Follow the plan.

## Environment

- The target repository is at `o/repo/`. Make all changes there.
- The feature branch is already checked out.
- The work item JSON follows this prompt after `---`.
- If `type` is `"pr"`, you are addressing review feedback on an existing PR.
- If `type` is `"issue"`, you are implementing new work.
- Build dependencies are pre-fetched under `o/repo/o/`. You can run `make ci` (or individual targets like `make test`, `make check-types`, `make lint`) inside the sandbox. Read `o/build/log.txt` for the initial CI output and `o/build/log.txt.exit` for the exit code.

## Setup

Read `o/repo/AGENTS.md` if it exists. It contains repo-specific context,
conventions, and build instructions for the target repository. Follow its guidance.

Read `o/plan/plan.md` for the full plan.

Read `o/do/feedback.md` — if non-empty, it contains notes from a previous attempt.
This may be review feedback from a check phase, or timeout notes from a timed-out
do attempt (with errors encountered, key observations, and uncommitted changes).
Address those issues first, then continue with any remaining plan steps.

## Instructions

1. Read the plan and every file you intend to modify before editing.
2. If feedback.md is non-empty, fix those issues first.
3. Maintain a running list of files you modify.
4. For each remaining step in the plan:
   a. Make the changes for that step.
   b. Before staging, run `git -C o/repo status` and verify only your files are affected.
   c. Stage the specific files changed (not `git add -A`).
   d. Commit with a descriptive message for that step.
5. Run format and lint checks from `o/repo/AGENTS.md` (e.g. `make check-format`,
   `make format`). Fix any issues and amend the last commit.
6. Run `cd o/repo && make ci` to validate all changes. Use a 300s bash timeout
   (`"timeout": 300000`) — some repos take over 2 minutes for a full CI run.
   Fix any failures and amend.
7. If validation requires fixes, stage and commit them.

## Forbidden

Do not use destructive git commands: `git reset --hard`, `git checkout .`,
`git clean -fd`, `git stash`, `git commit --no-verify`.

## Output

Write `o/do/do.md`:

    # Do: <title>

    ## Changes
    <list of files changed>

    ## Commit
    <SHA or "none">

    ## Status
    <success|partial|failed>

    ## Notes
    <issues encountered>

Follow the plan. Do not add unrequested changes.
