---
name: daily-summary-base
description: Framework for creating end-of-day summary documents. Use when user says "daily summary", "generate summary", or similar at end of day. Provides structured markdown template with date verification, filename patterns, and formatting guidelines. Extend with personal metrics and domain-specific content.
---

# Daily Summary Generator (Base Framework)

**Purpose:** Create end-of-day summary document for the specific date being summarized.

**Key principle:** Summary is OF a date, not FOR the next day. Filename matches the events it contains.

## Process

### 1. Verify Current Date

**CRITICAL FIRST STEP** - Prevents date confusion

```bash
TZ='America/New_York' date '+%A, %B %d, %Y - %I:%M %p %Z'
```

Confirm actual date in user's timezone.

### 2. Determine Summary Date

Ask user: "Which date's summary are we generating?"

**Typical scenarios:**
- End of day, same chat: "Today" (the date just verified)
- Next morning: "Yesterday" (verified date - 1)
- Backfilling: User provides specific date

**Always confirm:** "Generating summary for [Day], [Full Date]. Correct?"

### 3. Ask for Context Tag

"What's the context tag for this day?"

User provides tag representing experimental state for that specific day.

### 4. Generate Filename

**⚠️ CRITICAL: Filename must follow template exactly**

**Format:**
```
Summary-YYYY-MM-DD-DayName-[context-tag].md
```

**Example:**
```
Summary-2025-11-15-Saturday-example-tag.md
```

**Rules:**
- Date in filename = date of events inside (NOT next day)
- Day name format: `Monday`, `Tuesday`, etc. (full name, capitalized)
- Context tag: User-provided, hyphen-separated
- Save to: `/mnt/user-data/outputs/`
- Common mistake: Wrong date, generic names

**Critical:** Date in filename = date of events inside.

### 5. Check Context Usage (Optional)

After tool calls, system shows token usage:
```
Token usage: 127200/190000; 62800 remaining
```

**Interpret:**
- <75%: Plenty of room
- 75-85%: Good time for summary
- 85-95%: Generate soon
- >95%: Generate immediately

Note to user if high: "Context at [X]% - generating summary now to capture full day."

### 6. Create Document Structure

**Formatting rules:**
- Use only standard markdown (headers, lists, bold, italic, code blocks, tables)
- NO HTML tags (`<details>`, `<summary>`, `<div>`)
- ASCII-safe characters only:
  - Use `->` not `→`
  - Use `"` not `""`
  - Use `-` not `—`
  - Avoid Unicode special characters

**Emoji usage guidelines:**

**Projects limitation:** Claude Projects file export mangles UTF-8 emojis into broken Unicode (e.g., `ðŸ"¬` instead of 🔬). Root Claude.ai has clean artifact view, but Projects does not (yet).

**Recommended pattern:**
- **Avoid emojis in data sections** (tables, timestamps, key metrics) - keep machine-readable
- **Use sparingly in narrative sections** if they add meaning
- **Consolidate at document end** for easy cleanup:
  ```markdown
  ✨🔬🧪💻🚀
  ```
  Single line after wrap-up = easy to find/remove if export mangles them

**Export preservation strategy:**
1. View summary in Projects web UI (clean UTF-8)
2. Copy-paste into local text editor (preserves emojis)
3. OR: Accept export breakage, manually clean up `ð` characters on local save
4. **Future:** Nanoagent will have proper UTF-8 file handling + custom UI

**When in doubt:** Use plain text. Emojis are decorative, not essential. Prefer clarity over style.

**Required sections:**

```markdown
# [Day], [Date] - Daily Summary

**GROUND TRUTH:**
- Date: [Full day and date being summarized]
- [Context state - cycle/phase/day info]
- [Long-running counters if applicable]

---

## TL;DR - Day Summary

[2-3 sentence summary of trajectory]
[Key decision or insight]
[How capacity showed up]

---

## Key Numbers

| Metric | Morning | Evening | Notes |
|--------|---------|---------|-------|
| [Data] | | | |

---

## Timeline

### Detailed Events

[Chronological events with timestamps]

---

## Insights & Learnings

### What This Day Revealed

[Major insights, patterns, experimental results]

---

## Decisions Made

### What Was Decided

[Decisions for future, protocol adjustments, changes]

---

## What Mattered This Day

[Clear summary of day's significance]
[No ambiguity]
```

### 7. Save to Outputs

```
/mnt/user-data/outputs/Summary-YYYY-MM-DD-DayName-context-tag.md
```

### 8. Remind User

"Summary created: Summary-2025-11-22-Saturday-[context-tag].md

This captures Saturday's events. Click 'add to project' to save it."

## Critical Rules

1. **Date verification FIRST** - bash command, no assumptions
2. **Summary date = events date** - filename matches content, NOT next day
3. **User confirms date** - "Generating summary for [Day]. Correct?"
4. **Filename follows format** - ISO date + day name + exact tag user provided
5. **Ground truth at top** - absolute date being summarized in document
6. **Save to outputs** - user manually adds to project

## How This Differs From "Carryover"

**Old approach (broken):**
- Filename: Carryover-2025-11-16-Sunday.md
- Contains: Saturday's events
- Result: Off-by-one error for weekly reviews

**Current approach (correct):**
- Filename: Summary-2025-11-15-Saturday.md
- Contains: Saturday's events
- Result: Weekly review searches Nov 10-16, gets correct events

The summary IS the daily record.
