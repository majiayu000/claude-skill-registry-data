---
name: summary
description: Summarize staged changes. Defaults to brief natural language; use `--list` for structured per-file output.
purpose: Summarizes staged changes.
user_invocable: true
args: "[--list]"
stage: forge
composes: stage:dispatch
---

# Summarize Staged Changes

## Arguments

- No argument: brief natural language summary (default)
- `--list`: structured list with file path + description per file

## Workflow

1. Run `git status` and `git diff --cached` in parallel
2. Analyze the staged changes only
3. Output the summary in the chosen format

## Output Formats

### Default (brief natural language)
A 1-3 sentence description of what changed and why, e.g.:
> Added input validation to the login form and refactored the user model to support email verification.

### `--list` (structured)
A markdown list with each changed file and a short description:
```
- `src/auth/login.dart` — Added email format validation
- `lib/models/user.dart` — Added `emailVerified` field and migration
```

## Rules

- Only look at staged changes (exclude unstaged files)
- If there are no staged changes, invoke the `/stage` skill to let the user stage files first
- Keep the natural language summary concise — no more than 3 sentences
