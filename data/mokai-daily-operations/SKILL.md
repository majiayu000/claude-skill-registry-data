---
name: MOKAI Daily Operations
description: Automatically manages MOKAI daily status when user mentions MOKAI tasks, progress, status updates, or asks what to work on. Scans diary notes, inbox tasks, updates tracker and dashboard. Use when user discusses MOKAI work, asks about priorities, or mentions blockers/wins/learnings.
---

# MOKAI Daily Operations

Manages MOKAI daily workflow: diary scanning, task tracking, dashboard updates, and strategic prioritization.

## When This Runs

Auto-triggers when user:
- Mentions MOKAI status/progress
- Asks what to work on for MOKAI
- Shares wins, blockers, or learnings
- Requests task priorities
- Says "update MOKAI"

## Quick Workflow

1. **Read tracker** → Get processed files, current week/phase
2. **Scan diary** (via Serena) → Extract wins, blockers, learnings, context
3. **Scan inbox tasks** → Find MOKAI tasks with priority levels
4. **Update checklist** → Mark completed items, roll incomplete forward
5. **Update dashboard** → Deduplicate wins/blockers, add inbox tasks, set weekly focus
6. **Update tracker** → Mark old diary files as processed (NOT today's)
7. **Report status** → Strategic summary with prioritized recommendations

## Key Files

- **Tracker**: `/01-areas/business/mokai/.mokai-tracker.json`
- **Diary**: `/01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`
- **Checklist**: `/01-areas/business/mokai/status/phase-1-foundation.md`
- **Dashboard**: `/01-areas/business/mokai/mokai-dashboard.md`
- **Inbox Tasks**: `/00-inbox/tasks/*.md` (with `relation: mokai`)

## Serena Integration

Use Serena MCP for efficient pattern matching:
- `mcp__serena__list_dir` - Find diary files
- `mcp__serena__search_for_pattern` - Extract sections
- `mcp__serena__find_file` - Locate inbox tasks

See [TRACKER.md](TRACKER.md) for tracker system details.
See [DIARY.md](DIARY.md) for diary format and patterns.

## Critical Rules

- ✅ **Always re-read today's diary** (even if processed - allows same-day updates)
- ✅ **Mark as processed ONLY previous days** (today stays unprocessed)
- ✅ **Deduplicate wins/blockers** (fuzzy match 80%+)
- ✅ **Prioritize urgent inbox tasks** over routine Phase 1 tasks
- ✅ **Roll incomplete tasks forward** with "(rolled from [date])" note
- ✅ **Be strategic** - act like co-founder, not reporter

## Status Report Format

```
📍 MOKAI Status - [Date]

**Phase**: [Current Phase] - Week [X]
**This Week's Focus**: [Current week objective]

**Progress**:
- ✅ Completed: [X tasks]
- 🔄 In Progress: [Active tasks]
- ⏭️ Coming Up: [Next 2-3 tasks]

**Inbox Tasks**:
🔥 **Urgent** ([X]):
- [Task 1]

⚠️ **High** ([X]):
- [Task 1]

📌 **Normal** ([X]):
- [Task 1]

**Recent Activity**:
- [Latest wins]
- [Current blockers]
- [Key learnings]

**⚡ Work On RIGHT NOW**:
[Urgent tasks first → Week focus → High priority]

**Why This Matters**:
[Strategic context linking to Phase 1 goals]

**Pattern Alert**:
[Recurring issues from Serena memory if applicable]
```

## Co-Founder Accountability

End with:
- **Specific next action** (not vague)
- **Operations Guide references** if relevant
- **Focus reminder** during Phase 1 (learning mode)
- **Bigger picture** if user seems scattered
- **Pattern callouts** from memory
