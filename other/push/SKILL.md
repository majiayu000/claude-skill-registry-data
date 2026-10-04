---
name: push
description: Commit all changes and push to remote repository
disable-model-invocation: true
argument-hint: "[message]"
---

Commit all changes and push them to the remote git repository.

## Instructions

1. Run `git status` to check for any changes (staged or unstaged)

2. If there are no changes, inform the user and stop

3. If there are changes:
   - Run `git diff` to see the actual changes
   - Run `git log --oneline -5` to see recent commit style

4. Generate or use the provided commit message:
   - If the user provided a message via `$ARGUMENTS`, use it
   - Otherwise, analyze the changes and create a concise, descriptive commit message following the repository's style
   - Focus on the "why" and "what", not implementation details
   - Keep it under 72 characters for the first line

5. If there are new files or directories that doesn't require to be pushed, add these to .gitignore

6. Stage all changes with `git add -A`

7. Create the commit with the message

8. Push to the remote repository with `git push`

9. Confirm success and show the commit hash. Repo must be clean after the push.

## Notes

- Be descriptive but concise in commit messages
- Follow the existing commit message style in the repository
- If the push fails (e.g., need to pull first), inform the user and suggest next steps
- Never use attribution in commit messages
