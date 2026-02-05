---
name: vault-concurrent
description: Find notes edited around the same time as a given note. Triggers on "concurrent notes", "edited around same time", "what else was I working on", "contemporaneous".
auto_trigger: true
trigger_keywords:
  - "concurrent notes"
  - "edited around same time"
  - "what else was I working on"
  - "contemporaneous"
  - "same time as"
  - "edited together"
  - "working on when"
  - "related by time"
  - "same session"
  - "around same time"
  - "editing session"
  - "what else then"
  - "simultaneous"
  - "co-edited"
allowed-tools: mcp__flywheel__get_contemporaneous_notes
---

# Concurrent Notes Finder

Find notes that were edited around the same time as a reference note.

## When to Use

Invoke when you want to:
- Reconstruct context: "What was I working on when I wrote this?"
- Find related work from the same session
- Identify notes that might be conceptually related (edited together)
- Understand your workflow patterns

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `path` | Yes | - | Path to the reference note |
| `hours` | No | 24 | Time window in hours (before and after) |

## Process

### 1. Parse User Input

Identify the reference note and time window:
- "what else was I editing when I wrote [[Project Alpha]]?"
- "notes edited around the same time as today's daily note"
- "concurrent notes within 4 hours of this meeting note"

### 2. Call MCP Tool

```
mcp__flywheel__get_contemporaneous_notes(
  path: "projects/Project Alpha.md",
  hours: 24
)
```

### 3. Format Results

**Concurrent Notes Found:**
```
Concurrent Notes
=================================================

Reference: [[Project Alpha]]
Modified: 2025-12-30 14:23:15
Window: ±24 hours

Found 8 notes edited in same period:

-------------------------------------------------

Same Hour (14:00-15:00):
  📝 tech/frameworks/React.md
      Modified: 14:18:42 (5 min before)
      Likely same work session

  📝 projects/Alpha-Architecture.md
      Modified: 14:45:23 (22 min after)
      Likely same work session

Same Day (2025-12-30):
  📝 daily-notes/2025-12-30.md
      Modified: 09:15:00
      Daily log entry

  📝 work/meetings/Sprint-Planning.md
      Modified: 10:30:45
      Meeting notes

  📝 tech/tools/TypeScript.md
      Modified: 16:22:10
      Research note

Previous Day (2025-12-29):
  📝 projects/Alpha-Requirements.md
      Modified: 22:15:30
      Evening session

  📝 personal/goals/Q4-Review.md
      Modified: 21:45:00
      Evening session

  📝 daily-notes/2025-12-29.md
      Modified: 23:55:00
      End of day

-------------------------------------------------

Insights:
  - Core work session: 14:00-16:30 (4 notes)
  - You were working on Project Alpha context
  - Related: React, TypeScript, Architecture
  - Consider: Link these notes if not already

=================================================
```

**No Concurrent Notes:**
```
Concurrent Notes
=================================================

Reference: [[Isolated Note]]
Modified: 2024-06-15 03:45:00
Window: ±24 hours

No other notes modified in this period.

This was an isolated editing session.

Possible reasons:
  - Late night/early morning work
  - One-off note creation
  - Vault was new at this time

=================================================
```

## Understanding Time Windows

| Window | Use Case |
|--------|----------|
| 1 hour | Same work session |
| 4 hours | Same focus block |
| 24 hours | Same day/night cycle |
| 72 hours | Same project sprint |

## Use Cases

- **Context recovery**: "What was I researching when I wrote this?"
- **Session reconstruction**: "Show my work session from that day"
- **Relationship discovery**: "Find notes I edited together"
- **Workflow analysis**: "How do I work across notes?"

## Integration

Works well with other skills:
- **vault-activity**: Get broader activity patterns
- **vault-path**: Check if concurrent notes are linked
- **vault-common**: Find shared references among concurrent notes
- **vault-backlinks**: See if concurrent notes reference each other

---

**Version:** 1.0.0
