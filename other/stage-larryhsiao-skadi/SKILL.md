---
name: stage
description: Stage local files to git. Shows unstaged/untracked files and lets user pick which to stage.
purpose: Shows unstaged and untracked files and lets you pick which to stage.
user_invocable: true
args: "[file...]"
stage: forge
---

# Stage Files to Git

## Arguments

- No argument: show unstaged/untracked files and ask user which to stage
- `file...`: stage the specified files directly

## Workflow

### With arguments
1. Run `git add` on the specified files
2. Run `git status` to confirm

### Without arguments
1. Run `git status` to list unstaged and untracked files
2. If no files to stage, say "Nothing to stage." and stop
3. Present the files as options using AskUserQuestion (multiSelect: true)
4. Stage the selected files with `git add`
5. Run `git status` to confirm

## Rules

- Never use `git add .` or `git add -A`
- Always stage specific files by name
- Show git status after staging so the user can see the result
