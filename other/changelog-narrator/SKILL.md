---
name: changelog-narrator
description: "Compare two document versions and produce a structured changelog — no git needed. Use for PRDs, SOPs, contracts, strategy docs. Triggers: 'compare these two documents', 'what changed between versions', 'generate a changelog', 'сравни две версии документа', 'что изменилось', 'сделай changelog'."
version: 1.0.0
---

# Changelog Narrator

This skill compares two versions of a business document and produces a structured, human-readable changelog — without git, CLI, or "Track Changes". Designed for non-technical users who receive updated drafts and need to understand what changed at a glance.

**Input:**
- Two local files (`.md` or `.txt`) in the Cowork workspace — old version (v1) and new version (v2)
- Optional: version labels if filenames are ambiguous; optional focus area (e.g., "only compare Section 3")

**Output:**
- Markdown changelog: Summary → Added → Removed → Modified → Notes

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Identify and Validate Files

1. Check that exactly two files are provided
   - If only one file is given: stop — "Two documents are required. Please provide both the old version (v1) and the new version (v2)."
   - If no files are given: scan the Cowork workspace for `.md` and `.txt` files; list them and ask the user to specify which two to compare

2. Read both files
   - If a file is unreadable (binary, corrupted, unsupported format): stop — "Could not read [filename]. changelog-narrator works with .md and .txt files only."

3. Determine version order (which is v1, which is v2)
   - Infer from filename markers: `v1`/`v2`, `old`/`new`, `draft`/`final`, date suffixes (earlier date = v1)
   - If version order is ambiguous (e.g., `strategy-a.md` vs `strategy-b.md`): ask — "Which file is the older version?" — do not guess

### Step 2: Split Documents into Comparable Units

1. Segment each document into logical units:
   - H1/H2/H3 headings → use as section labels
   - Paragraphs under each heading → compare as blocks
   - Numbered or bulleted list items → compare as individual items
   - Table rows → compare row by row

2. Build a section map for each document:
   - Key: section heading (or "Intro" for content before the first heading)
   - Value: list of content units under that heading

3. If user specified a focus area (e.g., "only Section 3" or "only the Risks section"):
   - Filter both maps to matching section only
   - Note in output: "Comparison limited to: [Section Name]"

### Step 3: Compare and Classify Changes

1. Align sections by heading label across v1 and v2
2. For each content unit, classify:
   - **Added**: present in v2 but absent in v1
   - **Removed**: present in v1 but absent in v2
   - **Modified**: present in both, but content differs
   - **Unchanged**: identical in both → do NOT include in output

3. For **Modified** items:
   - Describe the change briefly: what was the key shift? (e.g., "Timeline changed from Q2 to Q3", "Metric updated from 10% to 15%", "Scope narrowed from 5 to 3 segments")
   - Do NOT reprint full paragraphs from both versions
   - If the change is structural (section renamed, split, merged): flag as Modified with note "Section restructured"

4. For tables:
   - Compare rows as discrete units — flag each added/removed/modified row individually
   - Do not collapse entire table into a single "Modified" entry

**Edge Cases:**
- Files are identical: output "No changes detected between [v1] and [v2]." Do not produce an empty changelog.
- Section exists in v2 but not in v1 → entire section is Added
- Section exists in v1 but not in v2 → entire section is Removed

### Step 4: Write Summary

Write 2–3 sentences capturing:
- Overall scope of changes (how many sections affected, what type of changes dominate)
- The apparent intent behind the changes (e.g., "Scope was narrowed", "Risks section significantly expanded", "Timelines shifted across the board")
- Avoid generic statements — reference specific sections or patterns

### Step 5: Format and Output Changelog

1. Assemble the changelog using the Output Format structure below
2. Populate each section: Added, Removed, Modified — each with N (count)
3. Skip any section with 0 entries (e.g., if nothing was removed, omit "Removed")
4. Add Notes section for all assumptions about version order, skipped content, focus-area limitations, table handling

---

## Negative Cases

- **Only one file provided:** Stop — "Two documents are required. Please provide both the old version (v1) and the new version (v2)."
- **No files found in workspace:** Stop — "No files found. Please upload your document versions or confirm they're in the selected Cowork folder, then try again."
- **File is binary/unreadable:** Stop — "Could not read [filename]. changelog-narrator works with .md and .txt files only."
- **More than two files provided:** Clarify — "I can compare two versions at a time. Please specify which two to compare first. You can run the skill again for additional pairs."
- **User asks for visual/side-by-side diff:** Explain — "I produce a structured text changelog. For a visual side-by-side diff, paste both files into a tool like Diffchecker.com."

---

## Output Format

```markdown
## Changelog: [Document Title] — [v1 filename] → [v2 filename]

**Compared:** `[filename-v1]` vs `[filename-v2]`
**Date:** [YYYY-MM-DD]

### Summary
[2–3 sentences: overall scope and intent of changes — specific sections and patterns, not generic phrasing]

---

### Added (N)

- **[Section / Heading]:** [Brief description of what was added]
- **[Section / Heading]:** [Brief description of what was added]

### Removed (N)

- **[Section / Heading]:** [Brief description of what was removed]

### Modified (N)

- **[Section / Heading]:** [Key change — e.g., "Timeline extended from Q2 to Q3"; "Success metric changed from 10% to 15% retention"]
- **[Section / Heading → Sub-item]:** [Brief description]

---

### Notes
- [Assumption: e.g., "Treated `strategy-a.md` as v1 based on earlier file modification date"]
- [Flag: e.g., "Table in Section 4 had 3 rows added — listed under Added separately"]
- [Scope note: e.g., "Comparison limited to Section 3 as requested"]
```
