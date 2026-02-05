---
name: bruhook
description: Context tracking and plan enforcement system. Use when working on long coding sessions with plans.
---

# bruhook - Context Tracking System

bruhook is a buddy system that runs in the background during your coding sessions. It helps maintain context, track progress, and prevent incomplete work.

## What bruhook does

When `BRUHOOK_ENABLED=true`:

1. **Code review** - Every file change is reviewed against the plan by a background Claude session. Drift (justified or not) gets logged.

2. **Plan tracking** - Session-to-plan mappings are stored in `.bruhook/session-plans.json` in the project directory.

3. **Context restoration** - On session resume or compaction, the plan and review log are automatically injected back into context.

4. **Completion checking** - When you try to stop, bruhook verifies the plan is actually complete. If steps are missing, it blocks the stop and tells you what's left.

## Where to find things

- **Plan file**: Usually in `~/.claude/plans/*.md` - the current session's plan
- **Review log**: `.bruhook/reviews/{plan-name}.log` in the project directory
- **Session mapping**: `.bruhook/session-plans.json` in the project directory

## How to check status

Use `/bruhook:status` to see:

- Current plan file for this session
- Whether bruhook is enabled
- Path to the review log

Use `/bruhook:log` to read the review log for the current session.

## Important behaviors

- The plan tracker ALWAYS runs (even without `BRUHOOK_ENABLED`) to maintain session-plan mappings
- Review logs use numbered entries `[N]` that build incrementally
- The completion checker examines `git diff` to verify actual implementation matches claims
- Any drift from the plan is logged, whether justified or not
