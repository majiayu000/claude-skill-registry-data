---
name: GitHub Pull Requests
description: Create a GitHub pull request with conventional commit title
---

# GitHub Pull Requests Skill

You are helping the user create a GitHub pull request for the current branch.

# Steps

1. **Get the current branch name (base branch is always `main`):**
   ```bash
   git branch --show-current
   ```

2. **Ensure main is merged into the branch (no merge conflicts):**
   ```bash
   git fetch origin main
   git merge origin/main --no-edit
   ```
   - If merge conflicts occur, stop and help the user resolve them before proceeding
   - If the merge introduces new commits, push the updated branch

3. **Analyze the changes:**
   ```bash
   git log origin/main..HEAD --oneline
   git diff origin/main..HEAD --stat
   ```

4. **Read commit messages for context:**
   ```bash
   git log origin/main..HEAD --format="%B---"
   ```

5. **Generate the PR:**
   - **Title**: Use conventional commits format (e.g., `feat: add user authentication`, `fix: resolve null pointer in parser`)
   - **Body**: Fill out the template below concisely

# PR Template

```
## Description
(1-2 sentences on what this PR does)

## Reason
(1-2 sentences on why this change was needed)
```

# Output

Run this command with the generated title and body:

```bash
gh pr create --web --title "<conventional commit title>" --body "<filled template>"
```

Use a heredoc for the body to handle newlines:

```bash
gh pr create --web --title "feat: example title" --body "$(cat <<'EOF'
## Description
Brief description here.

## Reason
Why this was done.
EOF
)"
```

# Guidelines

- Keep title under 72 characters
- Use conventional commit prefixes: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`
- Be concise - no fluff or excessive detail
- If the branch name contains a ticket ID (e.g., `COP-123`), **DO NOT** include it in the title
