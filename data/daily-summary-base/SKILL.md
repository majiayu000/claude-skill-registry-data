---
name: daily-summary-base
description: Framework for creating session summary documents. Use when user says "daily summary", "generate summary", or similar. Provides structured markdown template with date verification, filename patterns, and formatting guidelines. Supports range-based naming for sessions spanning calendar boundaries. Extend with personal metrics and domain-specific content.
---

# Daily Summary Generator (Base Framework)

**Purpose:** Create summary document capturing a conversation session's events.

**Key principle:** Summary is OF the session, not FOR the next day. Filename reflects the time span covered.

**Reality acknowledged:** Sessions often span calendar boundaries. Summaries may cover "Thursday afternoon through Friday morning" rather than clean calendar days. The naming convention should reflect actual coverage.

## Process

### 1. Verify Current Date/Time

**CRITICAL FIRST STEP** - Prevents date confusion

```bash
TZ='America/New_York' date '+%A, %B %d, %Y - %I:%M %p %Z'
```

Confirm actual date/time in user's timezone.

### 2. Determine Summary Range

Ask user: "What time range does this summary cover?"

**Typical scenarios:**
- Same-day session: "Today from morning until now"
- Spanning session: "Yesterday afternoon through this morning"
- Backfilling: User provides specific range

**Always confirm:** "Generating summary covering [Start Day/Time] to [End Day/Time]. Correct?"

**Determine if single-day or range:**
- If session starts and ends on same calendar day → single-day format
- If session spans calendar boundaries → range format

### 3. Ask for Context Tag

"What's the context tag for this session?"

User provides tag representing current state (e.g., `week-3-day-2`, `rest-day`).

### 4. Generate Filename

**⚠️ CRITICAL: Filename must follow template exactly**

**Single-day format:**
```
Summary-YYYY-MM-DD-Day-[context-tag].md
```
Example: `Summary-2025-11-15-Saturday-week-3-day-2.md`

**Range format (spans calendar boundaries):**
```
Summary-YYYY-MM-DD-Day-to-DD-Day-[context-tag].md
```
Example: `Summary-2026-01-15-Thu-to-16-Fri-week-5-long-run.md`

**Rules:**
- Use abbreviated day names in range format: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun`
- Use full day names in single-day format: `Monday`, `Tuesday`, etc.
- Range uses primary day's context tag (the day with bulk of session content)
- Save to: `/mnt/user-data/outputs/`

**Critical:** Dates in filename = dates of events inside.

### 5. Create Document Structure

**Formatting rules:**
- Use only standard markdown (headers, lists, bold, italic, code blocks, tables)
- NO HTML tags (`<details>`, `<summary>`, `<div>`)
- ASCII-safe characters only:
  - Use `->` not `→`
  - Use `"` not `"`
  - Use `-` not `—`
  - Avoid Unicode special characters

**Emoji usage guidelines:**

**Projects limitation:** Claude Projects file export mangles UTF-8 emojis into broken Unicode.

**Recommended pattern:**
- **Avoid emojis in data sections** (tables, timestamps, key metrics) - keep machine-readable
- **Use sparingly in narrative sections** if they add meaning
- **When in doubt:** Use plain text. Emojis are decorative, not essential.

**Required sections:**

```markdown
# Daily Summary: [Date or Date Range]

**[Context Tag]** | **[Secondary Tag if applicable]**

---

## GROUND TRUTH

- Covers: [Specific time range being summarized]
- State: [current state/phase]
- [Long-running counters if applicable]

---

## TL;DR - Day Summary

- [Session trajectory - what moved]
- [Key decision or insight]
- [Capacity/state summary]

---

## Key Numbers

| Metric | Morning | Evening | Notes |
|--------|---------|---------|-------|
| [Data] | | | |

---

## Timeline

| Time | Event |
|------|-------|
| [timestamp] | [event] |

---

## Insights & Learnings

[Major insights, patterns, results]

---

## Decisions Made

[Decisions for future, adjustments, changes]

---

## What Worked

- [Successes from session]

---

## What Didn't Work

| Challenge | Learning |
|-----------|----------|
| [issue] | [takeaway] |

---

## What Mattered This Day

[Clear summary of session's significance]

---

## Tomorrow's Seeds

**Threads still warm:**
- [Contemplation thread that could continue - not a task, a question or idea]
- [Decision mentioned but not yet acted on]
- [Experiment queued but not started]

**One thing from today:**
[A single insight, question, or observation from the session - seed for reflection, not action]

---

*Generated: [Current timestamp]*
*Summary OF: [Time range covered]*
*[Context tags]*

---

**[One-line closer capturing the session]**
```

### 6. Save to Outputs

```
/mnt/user-data/outputs/Summary-[filename].md
```

### 7. Remind User

"Summary created: [filename]

This captures [time range]. Click 'add to project' to save it."

## Critical Rules

1. **Date/time verification FIRST** - bash command, no assumptions
2. **Summary range = events range** - filename matches content coverage
3. **User confirms range** - "Generating summary covering [X] to [Y]. Correct?"
4. **Filename follows format** - ISO date(s) + day name(s) + exact tag user provided
5. **Ground truth at top** - explicit time range being summarized
6. **Save to outputs** - user manually adds to project

## Filename Examples

**Single-day (session within one calendar day):**
- `Summary-2025-11-15-Saturday-week-3-day-2.md`
- `Summary-2025-11-20-Thursday-rest-day.md`
- `Summary-2025-12-01-Monday-race-prep.md`

**Range (session spans calendar boundaries):**
- `Summary-2026-01-15-Thu-to-16-Fri-week-5-long-run.md`
- `Summary-2026-01-18-Sat-to-19-Sun-recovery-weekend.md`

## Why Range-Based Naming

**Problem:** Summary generation requires cognitive capacity that's unpredictable. Forcing summaries at calendar boundaries creates pressure. Sessions naturally span boundaries (afternoon → next morning).

**Solution:** Filename reflects actual coverage. The summary captures what happened, named for when it happened, generated when capacity exists.

**Tradeoff:** Slightly more complex filenames, but accurate representation of reality.

## Tomorrow's Seeds as Conversation Starters

**Purpose:** Tomorrow's Seeds bridges this session to the next. It's not a task list - it's conversation starters.

**"Threads still warm"** should capture:
- Contemplation topics that weren't exhausted
- Questions raised but not fully explored
- Decisions mentioned but not acted on
- Experiments discussed but not started

**"One thing from today"** should capture:
- A single insight worth sitting with
- A reframe that emerged
- A question that's still pulling
- Something that surprised or moved

**The morning brief skill uses these** to reopen contemplation rather than jumping straight to logistics. The summary document becomes the bridge between sessions, carrying forward not just what happened but what's still alive.
