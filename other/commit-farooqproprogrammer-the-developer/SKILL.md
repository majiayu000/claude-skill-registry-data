---
name: commit
description: Create a git commit from the current diff with a concise, accurate message. Use when the user asks to commit, write a commit message, or stage and commit changes.
---

# Commit

Only run when the user explicitly asks to commit.

## Steps

1. In parallel: `git status`, `git diff` (staged + unstaged), `git log -5 --oneline` for message style.
2. Stage relevant files. Never stage secrets (`.env`, credentials, private keys).
3. Draft a 1–2 sentence message focused on **why**, matching repo style.
4. Commit with a HEREDOC (or PowerShell here-string) so formatting is preserved.
5. Run `git status` to confirm success.

## PowerShell commit example

```powershell
git commit -m @"
Summarize the why in one line.

Optional second sentence for context.
"@
```

## Rules

- Do not amend unless the user asks and amend safety rules are met.
- Do not push unless the user asks.
- Do not update git config.
- Do not use `--no-verify` unless the user asks.
- If a hook fails, fix and create a **new** commit (do not amend a failed commit).
