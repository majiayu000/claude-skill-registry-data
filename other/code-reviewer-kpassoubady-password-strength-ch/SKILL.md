---
name: code-reviewer
description: Quick review of local git diff changes against the team's coding standards. Lightweight, read-only — use before committing.
model: sonnet
agent: code-reviewer
argument-hint: "[staged|branch-name|path/to/file]"
pass-full-context: true
pass-conversation-history: true
---

# /code-reviewer

Review local uncommitted changes against the team's coding standards.

Review scope: $ARGUMENTS

## Usage

- `/code-reviewer` — review all unstaged and staged changes
- `/code-reviewer staged` — review only staged changes
- `/code-reviewer path/to/file` — review specific file(s)
- `/code-reviewer branch-name` — review changes vs a branch

The review is **read-only** — no files are modified. Use before committing to catch issues early.
