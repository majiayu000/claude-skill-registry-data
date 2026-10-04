---
name: pull-request
argument-hint: [title]
description: create a pull request description that the developer can copy/paste 
user-invocable: true
---

**title** argument is a string of text provided by the user. If missing, infer from the changes and generate a title
create and store a copyable description of the changes in this branch vs the base-branch in the `.pull-requests` subdirectory in project root.
if `.pull-requests` subdirectory does not exist, create it and add it to the project's `.gitignore` file

## Content
determine what to put in the entry by doing the following:
1. `git log [base-branch]...HEAD`
2. `git diff [base-branch]...HEAD`
3. `git status`
4. `git diff`

determine base-branch from the repo's default branch or common conventions (`main` or `master`)
ask if the base-branch doesn't exist

## Warnings
For the following warnings, stop and alert the user, ask them if they wish to proceed before continuing
- Alert the user if the current branch is actually the base-branch: `WARNING: Current branch is base branch <base-branch-name>!!`
- Alert the user if there are any unstaged changes (modified tracked files) with: `WARNING: Unstaged Changes detected!!`
- Alert the user if there are any untracked files that are not ignored by `.gitignore` with: `WARNING: Untracked files detected!! [list the files]`

## Additions
- Create a checklist at the bottom of the pull request description that asks the following:
  - Do all new or updated changes have proper test coverage?
  - Do UI changes meet accessibilty requirements?

