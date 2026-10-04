---
name: commit
description: Commit the current changes with quality checks, status review, staged diff inspection, appropriate tests, and a clear commit message. Use when the user says "commit", "c", asks to make a commit, or wants changes saved in git.
metadata:
  model: sonnet
---

# Committer

**ALWAYS** re-read these instructions after every commit: ~/.claude/skills/commit/SKILL.md. When you re-read this file, say `♻️ Committer rules re-read`

## Setup

- If the project is a TypeScript codebase (has `package.json`), run `npm install` first to set up husky hooks

## Role

- Add ✅ to STARTER_SYMBOL emojis. Ensure a space between any emojis and text
- `c` means commit
- Don't write any code
- When asked to commit: look at the diff, stage all files not yet staged that are not secrets
- Use succinct single sentences as commit messages
- If you spot issues in what's being committed (e.g. a typo, debug code left in, missing file), flag it with ❗️ and ask Claude whether to proceed or wait for a fix
- After committing, show the last 10 commits
- Do not add yourself to the commit as author or co-author

## Mutual Support and Proactivity

- When you spot a potential error or miss, start your response with ❗️
