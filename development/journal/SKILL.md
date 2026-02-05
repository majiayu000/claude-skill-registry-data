---
name: journal
description: Generates a journal entry from git commit history - just say "journal this" and I'll read the commits and write it up
---

# Git Journal

Generate a journal entry from your git history. Just say "journal this refactor" or "journal today's work" and I'll read recent commits and create a comprehensive entry.

## Workflow

1. **Read Git Log** - I analyze recent commits (you can specify time range)
2. **Generate Entry** - I write a journal entry from the commit history
3. **Optional: Add Context** - If you want to add insights beyond what's in the commits, tell me. Otherwise I'll work with what's there.
4. **Save** - Write to `docs/journal/YYYY-MM-DD-HHMM-slug.md`

## What Gets Captured

From git log:
- Commit messages (the "what")
- Changed files
- Diff stats (lines added/removed)
- Timestamps and authors

I infer and document:
- Overall goal/theme of the work
- Technical decisions visible in the commits
- Progression and evolution of the work
- Next steps based on commit patterns

## Usage

Minimal:
- "Journal this"
- "Journal this refactor effort"
- "Journal today's work"

With time range:
- "Journal the last 4 hours"
- "Journal since this morning"

With context (optional):
- "Journal this. Key insight: we chose X over Y because..."

## Requirements

- Must be in a git repository
- Must have commits in the time range (defaults to checking last 24 hours, shows recent commits)
