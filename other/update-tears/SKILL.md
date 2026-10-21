---
name: update-tears
description: Update PROJECT_CONTINUITY.md and notes.toml with current session state. Use proactively before context compaction or when switching tasks.
disable-model-invocation: false
---

# Update Tears

Capture current session state to survive context compaction.

## Files to update

### PROJECT_CONTINUITY.md

Update these sections:

1. **Right Now**: What you're actively working on. Include:
   - Task description and date
   - Branch name
   - What's done in this session
   - What still needs to happen
   - Any open PRs

2. **Parked**: Threads to revisit later (moved from Right Now when switching tasks)

3. **Open Issues**: Keep current — check if any listed issues were closed

4. **Architecture**: Update version, test count, or structural changes if they happened

### docs/notes.toml

Add notes for any surprises from this session via CLI:

```bash
cqs notes add "note text" --sentiment 0.5 --mentions file.rs,concept
```

- Bugs that were non-obvious (sentiment: -1 or -0.5)
- Patterns that worked well (sentiment: 0.5 or 1)
- Observations worth remembering (sentiment: 0)

**Sentiment is DISCRETE**: only use -1, -0.5, 0, 0.5, 1.

## Rules

- Don't log activity — git history has that
- Focus on state that would be lost: what's in progress, what decisions were made, what's blocked
- Keep PROJECT_CONTINUITY.md concise — it's read on every resume
- Check for dirty files with `git status` and note uncommitted work in Pending Changes
