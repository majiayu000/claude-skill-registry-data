---
name: quick-commit
description: Create a git commit with a short message (up to 50 characters). Use when the user asks to commit changes with a short/concise message.
allowed-tools: Bash
---

# Quick Commit Skill

This skill helps create git commits with short, concise messages (up to 50 characters).

## Instructions

When the user asks to commit changes with a short message:

1. **Review Changes**: Run `git status` and `git diff` in parallel to see what changes exist
2. **Review Commit History**: Run `git log -5 --oneline` to see recent commit message style
3. **Draft Message**: Create a concise commit message that:
    - Is 50 characters or less
    - Uses present tense ("Add" not "Added")
    - Describes what the change does
    - Follows the project's commit message patterns
4. **Commit**: Add files and commit using the heredoc format:
   ```bash
   git add <files> && git commit -m "$(cat <<'EOF'
   Your commit message here.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```
5. **Verify**: Run `git status` to confirm the commit succeeded

## Examples

Common patterns for this codebase:
- "Nalog za prevoz - [feature]"
- "Add [feature] to [component]"
- "Fix [issue] in [module]"
- "Update [entity] with [property]"

## Important Notes

- Always include the Claude Code footer in commits
- Keep the main message under 50 characters
- Follow existing commit message patterns in the project