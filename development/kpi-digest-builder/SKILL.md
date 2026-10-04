---
name: kpi-digest-builder
description: "Aggregate numeric KPIs from local files (.md, .txt, .csv) into a weekly snapshot with delta vs. previous week. Use when preparing weekly reports. Triggers: 'build kpi digest', 'weekly kpi snapshot', 'собери KPI дайджест', 'еженедельный снапшот KPI'."
version: 1.0.0
---

# KPI Digest Builder

This skill aggregates numeric KPI values from local workspace files (.md, .txt, .csv) into a weekly snapshot table with delta vs. the previous week and a plain-language summary. No code, no API, no integrations required.

**Input:**
- One or more local files containing KPI data: `.md`, `.txt`, or `.csv` in the Cowork workspace
- Optional: specification of which file is "current week" and which is "previous week"

**Output:**
- Markdown digest with KPI snapshot table (Previous | Current | Δ | Δ% | Trend), plain-language summary, and Notes

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Locate Files

1. Identify the source file(s) from the user's message
   - If a filename or path is provided: use it directly
   - If no file specified: scan the Cowork workspace folder for files with KPI-related names (e.g., metrics, kpi, stats, report) or common formats (.md, .txt, .csv)
   - If no files found: stop and report — "No files found. Please upload your KPI files or confirm they're in your selected Cowork folder, then try again."

2. Determine which data is "current" and which is "previous"
   - If user specifies two files: treat the designated current file as this week, previous file as last week
   - If a single file has multiple date sections or a "last week" column: split accordingly
   - If dates are present but ambiguous: use the most recent date as current, earlier date as previous; note the assumption in Notes

### Step 2: Extract KPI Values

1. Read each file and extract all named numeric values
   - For `.md` / `.txt`: look for patterns like `KPI Name: 1,234`, `KPI Name — 45%`, `| KPI | Value |` tables, or bullet-point metric lists
   - For `.csv`: treat the first column as KPI name; numeric columns as values; use column headers (if present) to distinguish current vs. previous week
   - Preserve the original KPI names exactly as found (for matching across files)

2. Normalize all numeric values
   - Strip commas: `1,234` → `1234`
   - Strip currency symbols: `$45,000` → `45000`
   - Strip percent signs: `12%` → `12`
   - Convert shorthand: `1.2K` → `1200`, `3.5M` → `3500000`
   - Note any conversions in Notes

3. If no numeric values are found in any file: stop and report — "No numeric KPI values found. Please check that your files contain metrics (e.g., 'Revenue: 45,000' or a CSV with numeric columns). Then try again."

### Step 3: Match and Calculate Deltas

1. For each KPI found in the current dataset:
   - Look for a matching entry in the previous dataset by name (case-insensitive, strip extra spaces)
   - If a match is found: calculate Delta = Current − Previous; calculate Delta % = (Delta / Previous) × 100, rounded to 1 decimal place
   - If no match is found: record Current value only; note "no previous data" for this KPI

2. Handle conflicts and edge cases:
   - If two files contain the same KPI name with different values: show both values and flag "Conflict: two values found for [KPI] — please verify source"
   - If file has >30 KPIs: process all; note "Large dataset — showing all N KPIs" and offer to filter to top movers

3. Assign trend indicator:
   - Delta > 0: ↑
   - Delta < 0: ↓
   - Delta = 0 or no previous data: →

**Edge Cases:**
- No previous-week data at all: build snapshot with current values only; use → for all trends; note "Previous data unavailable — delta not calculated"
- KPI value is 0 in previous week: Delta % is undefined; note "Previous value was 0 — % change not calculable"
- KPI names slightly different across files (e.g., "MRR" vs "Monthly Revenue"): do not auto-merge; list separately; add note "Possible duplicate — verify if these are the same metric"

### Step 4: Write Plain-Language Summary

1. Identify the 2–3 KPIs with the largest absolute delta (either direction)
2. Write 2–3 sentences in plain language describing what moved and why it matters
   - Write for a business audience: avoid formulas, percentages with many decimals, or technical framing
   - If all KPIs are flat (zero delta): note "No significant movement this week"
   - If previous data is unavailable for all KPIs: write a current-state snapshot sentence instead

### Step 5: Format and Output Digest

1. Build the output in the structure defined in the Output Format section
2. Populate the Notes section with all assumptions, conversions, conflicts, and flags identified in Steps 1–3
3. If Notes is empty: omit the Notes section entirely
4. Output as a markdown response (not a file) unless the user asks to save to a file

---

## Output Format

```markdown
## KPI Digest — Week of [date or "current"]

| KPI | Previous | Current | Δ | Δ% | Trend |
|-----|----------|---------|---|----|-------|
| Revenue | 40,000 | 45,000 | +5,000 | +12.5% | ↑ |
| Active Users | 1,200 | 1,150 | -50 | -4.2% | ↓ |
| Support Tickets | 87 | 87 | 0 | 0% | → |
| Churn Rate | — | 3.2% | — | — | → |

### Summary
[2–3 plain-language sentences about the most significant movements]

### Notes
- [Assumption or flag, e.g., "Previous data not found for Churn Rate — delta unavailable"]
- [Format conversion, e.g., "Revenue normalized from '$45K' to '45,000'"]
```

**Field rules:**
- Previous / Current: use normalized numeric value + original unit suffix if present (e.g., 45,000 not 45000 if original used commas)
- Δ: show `+` prefix for positive, `−` for negative, `0` for flat; omit if no previous data (show `—`)
- Δ%: one decimal place; show `—` if previous value was 0 or no previous data
- Trend: ↑ / ↓ / → (never omit; use → when flat or no previous data)
- KPI names: preserve original spelling and capitalization from source files

---

## Negative Cases

- **No files found:** Stop with message — "No files found. Please upload your KPI files or confirm they're in your selected Cowork folder, then try again."
- **No numeric values in files:** Stop with message — "No numeric KPI values found. Please check that your files contain metrics (e.g., 'Revenue: 45,000' or a CSV with numeric columns). Then try again."
- **Unreadable file (binary, corrupted):** Skip the file; report — "Could not read [filename] — unsupported or corrupted file. Continuing with remaining files." If no readable files remain, stop with the "no files found" message.
