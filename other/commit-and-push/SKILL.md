---
name: commit-and-push
description: "Commit and push current changes."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before committing or pushing (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/git-hosts.md`

## Operations

| Operation | Tool (see `<project-root>/docs/git-hosts.md`) | CLI fallback per `<project-root>/docs/git-hosts.md` |
|-----------|--------------|--------------|
| Load change state | git host change scan (see `<project-root>/docs/git-hosts.md` in the project root) | `git branch --show-current` + `git status --short` + `git diff --stat` + `git diff --cached --stat` + `git log @{u}..HEAD --oneline` |
| Stage and commit | git host commit (see `<project-root>/docs/git-hosts.md` in the project root, with `message`) | `git add -A` + `git commit -m "<message>"` |
| Push to remote | git host push (see `<project-root>/docs/git-hosts.md` in the project root) | `git push` (retry `git push -u origin <branch>` if no upstream) |

Follow `<project-root>/docs/git-hosts.md` in the project root for all git/gh operations.

### 1. Interpret Arguments

- Wording influencing commit message → `<additional-context>`
- Otherwise undefined

### 2. Load Changes

If a pre-scan was already forwarded, skip to step 3.

Otherwise:

Step 1: Load uncommitted changes via the operations table above. Store `<uncommitted>`.

Step 2: If `<uncommitted>` is empty, load commits ahead using `@{u}..HEAD`. Store `<ahead-commits>`.

Step 3: Analyze scope:
- Primary `<uncommitted>`; fallback `<ahead-commits>` (push only, no commit).
- Group into logical themes. Summarize "what" and "why", not "how".
- Store as `<change-summary>`, including `<additional-context>`.

### 3. Check Blockers

- If `<uncommitted>` and `<ahead-commits>` are both empty, STOP: "Nothing to commit or push"

### 4. Create Commit

Skip if `<uncommitted>` is empty (push ahead commits only).

Commit message follows git conventions.

Commit:
1. Stage (`-A` or specific files).
2. Generate message from `<change-summary>` and `<additional-context>`.
3. Commit via git host commit or `git commit -m`; store `<hash>`.

### 5. Push to Remote

Push via git host push or `git push`. If no upstream, retry `git push -u origin <branch>`. Store `<push-target>`. If push fails, STOP and report the error. On success, output `<hash>` and `<push-target>`.

