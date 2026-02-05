---
name: starting-implementation
description: Provides guidelines for verifying implementation requirements before creating, editing, or deleting files, and taking appropriate actions when requirements are not met.
---

## Instructions

1. Run `git branch --show-current` to obtain the **current branch name**.
2. Run `git status --porcelain` to check for **uncommitted changes**.
   - If the output contains 0 lines: Set **uncommitted changes** to `false`.
   - If the output contains 1 or more lines: Set **uncommitted changes** to `true`.
3. Based on the **current branch name** and **uncommitted changes**, follow the appropriate procedure:
   - **If the current branch is `main` or `master`:**
     - Inform the user that they are starting work on the `main` branch.
     - Require the user to create and switch to a new branch using `git switch -c <branch name>` with a branch name appropriate for the changes.
   - **If the current branch is not `main` or `master` and there are uncommitted changes:**
     - Inform the user that uncommitted changes exist on a non-main branch.
     - Ask the user whether they want to switch to a new branch now.
     - If the user chooses to switch, create and switch to a new branch using `git switch -c <branch name>`.
     - If the user chooses not to switch, proceed with caution and remind them to commit or stash changes as appropriate.
   - **If the current branch is not `main` or `master` and there are no uncommitted changes:**
     - Proceed with the implementation on the current branch, or recommend creating a new branch if appropriate for the scope of the changes.
