---
name: ship
description: Commit and push changes with an auto-generated commit message. Use when the user says "ship it", "commit and push", or wants to save and deploy their changes.
---

# Ship

Commit and push all changes with a well-crafted commit message.

## Instructions

1. **Check current state**
   - Run `git status` to see all changes
   - Run `git diff` to understand what changed
   - Run `git log --oneline -5` to see recent commit style

2. **Stage changes**
   - Add relevant files with `git add`
   - NEVER commit sensitive files (.env, credentials.json, secrets/, etc.)
   - Warn the user if sensitive files are detected

3. **Generate commit message**
   - Write in English
   - Focus on the "why" rather than the "what"
   - Keep the first line concise (50-72 chars)
   - Use imperative mood ("Add feature" not "Added feature")

4. **Commit with signature**
   Use HEREDOC format for proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   Your commit message here

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

5. **Push to remote**
   - Run `git push`
   - If no upstream is set, use `git push -u origin <branch>`

6. **Report result**
   - Show the commit hash
   - Confirm which branch was pushed
   - Confirm push was successful

## Safety

- NEVER force push
- NEVER push to main/master without explicit user approval
- NEVER commit files that look like secrets or credentials
- If there are no changes, inform the user instead of creating an empty commit
