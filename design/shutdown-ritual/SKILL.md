---
name: shutdown-ritual
description: "Evening task selection ceremony for maker work (discovery: requirements-clarity). Evaluate at requirements-clarity when user mentions shutdown ritual, evening ceremony, select for book, end of day selection, or tomorrow's tasks."
---

# Shutdown Ritual

Two-step evening ceremony: validate data quality, then select maker tasks for tomorrow's book.

## Workflow

### Step 1: Data Quality Check

Run `scripts/data_quality_check.sh` to find items missing maker/manager classification.

**Scope:** All assignees, to-do/in-progress/review, excludes CLAUDE-CODE-IMPROVEMENTS and sub-issues.

**Expected result:** Empty (all items classified). If items found, user fixes before proceeding.

### Step 2: Maker Selection

Run `scripts/maker_selection.sh` to display maker items grouped by status.

**Scope:** MariusWilsch only, maker items, excludes CLAUDE-CODE-IMPROVEMENTS and sub-issues.

**Output format - YOU MUST preserve exactly:**
```
=== REVIEW (n) ===
#123: Title...

=== IN-PROGRESS (n) ===
#456: Title...

=== TO-DO (n) — select max 3 for book ===
#789: Title...
```

**Format enforcement:** Present script output EXACTLY as shown above. No tables, no reformatting, no "summary" versions. Reformatting = user confusion about what matches their board. Every time.

User selects max 3 from TO-DO for tomorrow's physical book.

## Rules

- Step 1 must pass before Step 2
- Max 3 items in book (realistic daily capacity)
- Board closes after selection until tomorrow
