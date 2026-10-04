---
name: draft-pr
description: Prepare commits, push a branch, and create a draft PR targeting your base branch.
---

# Draft PR

## Invocation

This skill defaults to running in the `Developer` persona. If you are not already running as `Developer` (for example, the user invoked `/draft-pr` directly or you are the parent agent), delegate execution to a `Developer` subagent and stop. If you are already running as `Developer`, continue with the steps below.

## Objective

Prepare a clean branch and create a draft PR targeting your base branch.

## Instructions

1. Review the current changes with `git status`.
2. Run the applicable verification checks before proceeding.
3. Confirm or create a feature branch if the current branch is your base branch.
4. Gather commit details and use a **conventional commit** message (see below).
5. Push the branch.
6. Generate the PR body via `/pr-description`.
7. Create the draft PR targeting your base branch. **PR title**: if the branch name contains a ticket key, include it in the PR title. If there is no recognizable key and the user did not supply one, omit it.
8. End with the commit hash, branch name, PR URL or creation instructions, and the recommended next step: `/review`.

## Commit messages

- Format: `type(scope): subject` (scope optional). Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `revert`.
- Subject: imperative, concise, lowercase except proper nouns/acronyms.
- Do not add auto-generated `Co-authored-by:` trailers from tooling.
- Before the **first** commit on a change, run a full verification pass from the repo root; targeted checks are fine while iterating but not a substitute for that pre-commit pass.
