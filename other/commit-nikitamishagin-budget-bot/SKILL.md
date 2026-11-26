---
name: commit
description: Commit the files changed in the current task as logical conventional commits after the user approves. Use at the end of every task that changed files.
user-invocable: false
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git commit *)
---

# Commit

1. Run `git status`, `git diff`, `git diff --staged` and `git log --oneline -15`.
2. Group only the files changed during the current task into logical commits, one concern per commit. If other
   uncommitted changes exist, list them in one line and leave them out.
3. Show the proposal: for each commit, its files and full message. Wait for the user's approval or edits.
4. After approval, stage each group with `git add <files>` and commit it. If the user declines, leave the changes
   uncommitted.

## Message format

```
<type>(<scope>): <short summary>

<body: what changed and why, 1-2 brief sentences>
```

- Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`.
- Scope is the affected package or area: `telegram`, `handler`, `memory`, `store`, `llmparser`, `config`, `app`,
  `agent`, `e2e`, `enrichment`, `readme`, `claude`.
- Short summary is at most 50 characters.
- Body is 1-2 short sentences. Avoid verbose descriptions and unnecessary details.
- Don't use colons or semicolons in the description.
- If code comments in the diff explain a change, use them to understand why it was made.

## Never

- Never commit secrets (`api-key`, `telegram-bot-token`, `postgres.env`, `.env`), `data/`, or e2e `expected.draft.json`.
- Never push, amend, rebase or use `--no-verify`.
- Never commit without the user's approval of the proposal.
