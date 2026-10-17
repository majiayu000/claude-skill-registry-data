---
name: file-pr
description: Commit the work and file a concise pull request. Use when the user asks to file, open, raise, or create a PR. "uat PR" or "PR to uat" means the UAT flow.
---

# File PR

Commit the work on the current branch and file the PR for it. This skill is
about committing and filing well, not writing code: if the change isn't
finished, say so and stop.

Two flavours: a normal PR into the primary branch (default), and a UAT PR
(only when the user says uat).

## Commit

- Commit whatever uncommitted work belongs to the task. If the diff contains
  changes that look unrelated to the task, stop and ask; never sweep them in.
- Commit messages are short imperative English describing observable
  behaviour, no trailing period, no Conventional Commits. Ticket work starts
  with the key (`SULF-1234: ...`).
- If everything is already committed, skip straight to filing.

## Before filing

- Check whether a PR for this branch already exists. If it does, update it
  instead of opening a duplicate.
- Review the diff locally against upstream's primary to make sure its
  contents match the goal. Anything unrelated in the diff: stop and ask.
- Confirm the branch name and every commit message contain no AI reference
  (`codex`, `claude`, `openai`, `chatgpt`, `gpt`, or similar) and no
  `Co-Authored-By` / "Generated with" trailers. If one does, stop and tell
  the user; never file it as-is.
- Work repos: `upstream` is the company repo, `origin` the fork; the PR goes
  from origin to upstream. Personal repos have origin only.
- Find the primary branch (`master`, `main`, or `prod`; check the repo).

## Title

PR titles usually become commit messages, so follow the repository's title
conventions: look at recently merged PRs and git history for examples. Prefer
a concise, human-readable title that explains why the change matters, in
short imperative English. Ticket work starts with the key (`SULF-1234: ...`).
No Conventional Commits.

- Bad example: `Update preflight checks, parse CLI version and fix server`
- Good example: `Stop preflight failing when local and remote CLI versions drift`

## Description

Open the description with a simple explanation of the problem based on the
user's original prompt, then briefly explain the solution. Do not lead with
an implementation inventory.

- Bad example: "Removed implicit workspace carryover from every new thread
  entry point. New threads now inherit only the project from context, branch,
  worktree..."
- Good example: "My new-worktree default was ignored when starting new
  threads on existing worktrees, which was super unintuitive. Now the
  preference always applies."

A test plan line only when there is something real to run. If the description
needs headings to stay readable, it is probably too long.

## Normal PR

1. Run `git-pr <primary>` (zsh shell function): it pulls upstream's primary
   into the branch and pushes to origin. If the function is missing from your
   shell, say so; do not improvise the push.
2. Resolve conflicts from the pull yourself wherever the change's stated
   intent decides them: keep unrelated upstream hunks, rerun lint and tests
   on the merged result, and note the resolution in one line of the PR body.
   Stop only on a hunk that needs a product or ownership decision, and name
   it. Still file every other requested PR.
3. Create the PR into upstream's primary:
   `gh pr create --repo <upstream-owner>/<repo> --head <origin-owner>:<branch> --base <primary>`

## UAT PR

1. Run `git-uat` (zsh shell function): it creates `<branch>-uat`, merges
   `upstream/uat` into it, pushes it to origin, and returns to the original
   branch. Same rules: a missing function means stop and report; resolve
   conflicts as in Normal PR step 2.
2. Create the PR from `<branch>-uat` into upstream's `uat`:
   `gh pr create --repo <upstream-owner>/<repo> --head <origin-owner>:<branch>-uat --base uat`

## After filing

Open a real PR rather than a draft so the review bots run. If the user also
asked to babysit, continue with the babysit-pr skill. Otherwise reply with
the PR URL and one line of status. Nothing else.
