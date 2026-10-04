---
name: changelog
argument-hint: [digit]
description: add details for the current branch to a project CHANGELOG for developer reference 
user-invocable: true
---

**digit** argument refers to MAJOR, MINOR, or PATCH (case-insensitive)
**CHANGELOG.md** lives in the project root and should be created if it does not exist

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

## Committing
after creating/updating the changelog, add it to staged changes and commit it using `git add CHANGELOG.md && git commit -m "CHANGELOG Updated [MAJOR.MINOR.PATCH]"`

## Versioning
- version numbers adhere to standard conventions `MAJOR.MINOR.PATCH`
- This version numbering does not necessarily correlate to a release version
- **MAJOR** version is for large releases, likely with breaking changes, and should only be updated if explicitly instructed
- **MINOR** version is for incremental development of new features and code refactors
- **PATCH** version is for small changes, bug fixes, code quality improvements (like adding tests)
- If no argument is passed in, **suggest** a MINOR or PATCH version based on the diff, then **ask the user to confirm** before proceeding

## Formatting and Order
- Changelog entry title includes version and date of entry `[MAJOR.MINOR.PATCH] YYYY-MM-DD`
- Order is **Reverse Chronological**, ie, new entries at the top of the file
- **The Date** should be the current date according to this device's locale in the format of `YYYY-MM-DD`
- use bullet points under headings for **Added/Changed/Fixed/Removed**
