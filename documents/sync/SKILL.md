---
name: sync
description: End-of-session documentation sync — updates TODO.md and PROGRESS.md only (run /commit after to commit everything)
when_to_use: "end of session, update TODO.md and PROGRESS.md, check off completed items, session wrap-up — NOT for post-release doc sync (use /document-release)"
argument-hint: ''
user_invocable: true
---

# Sync Skill

End-of-session documentation ritual. Reviews what was done and updates project docs — no commit. Run `/commit` after to commit everything (docs + code) split by module.

## What it does

1. Reviews recent git history to understand what was accomplished
2. Auto-updates TODO.md (checks off completed items)
3. Prepends a session summary to PROGRESS.md (newest-first; appending puts today's work first in line to be archived)
4. Flags a root README over the 300-line landing-page cap, naming the sections that should move to `docs/`

## Usage

```
/sync            # Update TODO.md + PROGRESS.md
/commit          # Commit all changes (code + docs) split by module — local only
/commit --publish  # Commit, then publish the owned branch
```
