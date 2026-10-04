---
name: backlog-grooming-assistant
description: "Analyze backlog files (CSV or Markdown) to flag problematic items and generate a structured grooming agenda. No Jira API needed — works entirely with local exports. Use when preparing for sprint grooming, auditing accumulated tasks, or reviewing the backlog after a sprint. Triggers: 'groom my backlog', 'backlog grooming assistant', 'подготовь повестку груминга', 'груминг-ассистент', 'проверь бэклог на проблемы'."
version: 1.0.0
---

# Backlog Grooming Assistant

This skill reads a local backlog export (CSV or Markdown table), flags problematic items using a structured checklist, and produces a grooming session agenda with a scorecard. No external service connections required — works entirely from pasted or uploaded file contents.

**Input:**
- Backlog file contents: CSV (with column headers) or Markdown table — pasted directly or uploaded
- Minimum required columns: item ID and title; additional columns (owner, priority, estimate, status, last-updated) enable more flags

**Output:**
- Markdown document with: Scorecard → Top Issues → Grooming Agenda → Skipped Checks

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

The detected language applies to **all output text**: section headings, table column headers, field labels, agenda topic titles, error messages, and recommended actions. Translate every part of the output format template into the detected language — do not leave any section header or label in English when responding in Russian.

---

## Instructions

### Step 1: Parse and Validate Input

1. Accept backlog content from the user (pasted text or file contents)
   - If content is empty: stop and return — "Backlog is empty — no items to analyze. Paste CSV or Markdown table content."

2. Detect format:
   - CSV: first line contains comma-separated headers
   - Markdown table: lines starting with `|` and separator row `|---|`
   - If neither format detected: stop — "Format not recognized. Supported: CSV with headers, Markdown table. Paste the file contents in chat."

3. Parse rows: extract all items as a list of key-value pairs
   - Identify available columns by name (case-insensitive matching)
   - Map common synonyms: "Task" → title, "Assignee" → owner, "SP"/"Points" → estimate, "Updated"/"Modified" → last-updated
   - If columns cannot be mapped automatically: ask user to specify column mapping for the ambiguous columns, then continue

4. Validate row count:
   - If 0 data rows (headers only): stop — "Backlog is empty — no items to analyze."
   - If all rows have status "Done" or "Closed": stop — "All items are completed — no active tasks for grooming."

### Step 2: Apply Flag Checklist

For each item, evaluate applicable flags (skip flags that require unavailable columns):

| Flag | Condition | Required column(s) |
|------|-----------|-------------------|
| `NO_OWNER` | Owner/Assignee field is empty or missing | owner |
| `NO_ESTIMATE` | Estimate/story points field is empty or zero | estimate |
| `UNCLEAR_SCOPE` | Description/title is absent or fewer than 5 words | title, description |
| `STALE` | Last-updated date is more than 14 days ago | last-updated |
| `BLOCKED_NO_ETA` | Status contains "blocked" with no ETA/date mentioned | status, description |
| `ALL_HIGH_PRIORITY` | Signal: more than 50% of all items marked High/Critical | priority (applied to entire backlog, not per item) |
| `DUPLICATE_TITLE` | Title is ≥80% similar to another item in the backlog | title |

Compile per-item flag list and a backlog-wide summary count for each flag type.

**Edge Cases:**
- Column missing for a flag: skip that flag for all items; record the skipped check in output
- `STALE` check: if date format is ambiguous, skip and note in skipped checks
- `ALL_HIGH_PRIORITY`: apply once to the whole backlog; annotate in scorecard, not per-item

### Step 3: Identify Top Issues

1. Sort flagged items by flag count (descending)
2. Select top 10 items (or fewer if backlog is small)
3. For each top item: collect ID, title, flags, and priority level

### Step 4: Generate Grooming Agenda

Group top issues by flag type into agenda topics:

- **No Owner** → agenda item: "Assign owners to unowned tasks"
- **No Estimate** → "Estimate unscored items"
- **Unclear Scope** → "Clarify scope / rewrite descriptions"
- **Stale Items** → "Review or close items with no recent activity"
- **Blocked Items** → "Resolve blockers or set ETA"
- **Priority Inflation** → "Re-prioritize — too many High/Critical items"
- **Possible Duplicates** → "Review and merge duplicate candidates"

For each agenda topic, list the affected item IDs and a recommended action.

### Step 5: Produce Output

Write the full output in the format specified in the Output Format section below.

---

## Negative Cases

- **Empty input or headers-only file:** Stop. Return "Backlog is empty — no items to analyze."
- **Unrecognized format:** Stop. Return "Format not recognized. Supported: CSV with headers, Markdown table."
- **All items Done/Closed:** Stop. Return "All items are completed — no active tasks for grooming."
- **Plain text list without structure:** Warn — "Insufficient structure for flag analysis. Try adding columns: status, owner, priority." Produce minimal output based on titles only (UNCLEAR_SCOPE check only).

---

## Output Format

```markdown
# Grooming Report — [date]

## Scorecard
- Total items: N
- Flagged items: N (X%)
- No owner: N
- No estimate: N
- Stale (>14 days): N
- Blocked without ETA: N
- Possible duplicates: N
- Priority inflation: YES / NO

## Top Issues for Grooming

| Item | Title | Flags | Priority |
|------|-------|-------|----------|
| [ID] | [Title] | NO_OWNER, NO_ESTIMATE | High |
| ... | ... | ... | ... |

## Grooming Agenda

### 1. [Topic]
**Items:** [ID1], [ID2]
**Problem:** [description]
**Recommended action:** [what to discuss / decide]

### 2. ...

## Skipped Checks
The following checks were not applied due to missing columns:
- [Flag name]: requires column "[column name]"
```

**Field rules:**
- Scorecard numbers must be accurate counts from the parsed data
- Top Issues table: max 10 rows, sorted by flag count descending
- Agenda topics: include only those with at least one affected item
- Skipped Checks: list only checks that were actually skipped; omit section if none skipped
