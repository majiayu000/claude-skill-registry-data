---
name: speckit-git-pr
description: 'Open a GitHub PR for the current feature branch, auto-appending Closes
  #N from .specify/feature.json when source_issue is set; --draft opens it as a draft
  and leaves the issue open'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.pr.md
---

# Create PR for Current Feature

Open a GitHub pull request from the current feature branch into `main` (or another base passed as an argument). If `.specify/feature.json` carries a `source_issue` field — written by `/speckit-git-feature` when it created or was bound to a GitHub issue — the PR body will include a `Closes #N` line so merging the PR automatically closes that issue. That is the file's only field; every other part of the feature's identity is derived from git at read time (issue #33).

Designed to be invoked as the `after_implement` hook (alongside the existing auto-commit hook), or directly via `/speckit-git-pr`.

## Arguments

`/speckit-git-pr [base_branch] [--draft]`

- `base_branch` — defaults to `main`.
- `--draft` — **draft handoff mode**: open the PR as a draft *and* skip the
  `/speckit-archive-feature` pre-step. Use this whenever a human still has to review
  before the work is considered delivered — notably every `/speckit-autopilot-run`.

## Pre-Execution (Mandatory)

Before any PR checks or `gh pr create` execution, run these commands in order:

1. `/speckit-archive-feature` — **skipped when `--draft` is passed.** Archiving closes
   the tracking issue and moves the spec out of the active tree; in draft mode the
   issue must stay open and the spec must stay in place until a human merges the PR
   (issue #28). Archive after the merge instead.
2. `/speckit-git-commit` — always runs, draft or not.

If a command that is supposed to run is unavailable or fails, stop and return an error. Do not continue to PR creation.

## Behavior

1. Run mandatory pre-execution commands:
   - `/speckit-archive-feature` (skipped in `--draft` mode)
   - `/speckit-git-commit`
2. Verify `gh` is installed and the cwd is a git repo on a non-default branch.
3. Resolve the feature:
   - The feature directory is derived from the current branch (`specs/<branch>`, honouring `SPECIFY_FEATURE_DIRECTORY`/`SPECIFY_FEATURE`) → used to derive the PR title from the spec's H1 and to mention spec/plan/tasks paths in the PR body.
   - `source_issue` is read from `.specify/feature.json`, its only field → if present and numeric, append `Closes #N` to the PR body.
4. If `squash_before_pr: true` in `git-config.yml`, squash every commit between `merge-base(HEAD, <base>)` and `HEAD` into a single commit (title from the spec H1, body listing the original commit subjects). Aborts if the working tree has uncommitted changes.
5. If the branch isn't yet on `origin`, push it (`git push -u origin <branch>`). If it was already pushed and a squash happened, force-push with `--force-with-lease`.
6. If a PR already exists for the branch, print its URL and exit. In `--draft` mode, if that existing PR is *not* a draft, also print a warning naming `gh pr ready <url> --undo` — the script does not mutate a PR it did not create.
7. Otherwise, run `gh pr create --base <base> --head <branch> --title <derived> --body <derived>`, adding `--draft` in draft mode. The draft flag is passed to `gh pr create` directly — never create a mergeable PR and convert it afterwards with `gh pr ready --undo`.

## Execution

Run the script:

- **Bash**: `.specify/extensions/git/scripts/bash/create-pr.sh [base_branch] [--draft]`

Default `base_branch` is `main`. Pass an alternative as the first argument if needed.
`--draft` may appear in either position. The script owns the draft flag on
`gh pr create`; skipping `/speckit-archive-feature` is this command's half of the
contract, since the script never invokes that command itself.

## Graceful Degradation

- If `/speckit-archive-feature` (non-draft mode only) or `/speckit-git-commit` is unavailable or fails: error and stop before PR creation.
- If an unknown option or a second positional argument is passed: error with the usage line and stop.
- In `--draft` mode with a pre-existing non-draft PR: warn with the `gh pr ready --undo` hint and exit successfully; the existing PR is left untouched.
- If `gh` is missing: error with install hint.
- If the current branch equals the base branch: refuse.
- If no `source_issue` is recorded: PR is created without a closing keyword (still works, just doesn't auto-close an issue).
- If a PR already exists for this branch: prints the existing URL, does not duplicate.
- If `squash_before_pr: true` but the merge-base with `<base>` cannot be computed, or the working tree has uncommitted changes: error and stop before pushing.