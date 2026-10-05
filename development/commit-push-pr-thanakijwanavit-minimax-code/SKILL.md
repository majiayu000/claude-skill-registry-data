---
name: commit-push-pr
description: Creates a git commit and pushes to remote. Use -a to amend. Optionally accepts a commit message.
---

## Task

Create a git commit with all modified code and push to the remote repository.

### Step 1: Stage Changes

Run `git status` to see what files have changed. Stage the relevant changes:

- Stage files that are related to the current work
- Do NOT stage unrelated changes or files that shouldn't be committed (e.g., local config, debug files)
- Use `git add <file>` for specific files or `git add -A` if all changes should be committed

### Step 2: Commit

If amending:

- If a commit message is provided, use `git commit --amend -m "<message>"`
- Otherwise, use `git commit --amend --no-edit` to keep the previous message

Otherwise:

- If a commit message is provided, use it
- If no message provided, run `git diff --cached` to see what's staged, then draft a concise commit message
- Create a new commit with the message

### Step 3: Push to Remote

Push to the remote. If amending, use `git push --force-with-lease`. If no upstream exists, add `-u origin <branch-name>`. Both flags can be combined if needed.

### Step 4: Create or Update PR

Check if a PR already exists for this branch: `gh pr view --json url 2>/dev/null`

- If no PR exists, create one as a **draft**: `gh pr create --draft --title "<title>" --body "<body>"`
- If a PR already exists, skip this step (the push already updated it)

### Important Notes

- NEVER use `--force` unless explicitly requested
- NEVER skip hooks (`--no-verify`) unless explicitly requested
- ALWAYS create PRs as drafts — never create non-draft PRs
- If the commit fails due to pre-commit hooks, fix the issues
- If push fails due to remote changes, pull and rebase before retrying
- If push fails with 403/permission denied, fork the repo (`gh repo fork --remote=true`), then push to the fork and open a PR against the upstream repo
