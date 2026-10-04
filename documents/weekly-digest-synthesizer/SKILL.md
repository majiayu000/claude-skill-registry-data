---
name: weekly-digest-synthesizer
description: "Compile weekly status digests from multiple .md/.txt files. Extracts project updates, action items, and blockers into a structured report. Use when aggregating team status notes into a weekly summary. Triggers: 'compile weekly digest', 'weekly digest', 'составь дайджест', 'скомпилируй статусы'."
version: 1.0.0
---

# Weekly Digest Synthesizer

This skill compiles status updates from multiple local `.md` and `.txt` files into a structured weekly digest. It groups content by project area, surfaces action items and blockers, and outputs a ready-to-share markdown file named `weekly-digest-YYYY-MM-DD.md`.

**Input:**
- Folder path or list of `.md` / `.txt` files containing status updates
- Optional: digest date (defaults to today), output format preference (concise / detailed)

**Output:**
- `weekly-digest-YYYY-MM-DD.md` — structured digest with Summary, Projects, Action Items table, Risks & Blockers

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Determine input source from the user's message:
   - Folder path → scan all `.md` and `.txt` files in that folder
   - List of files → use those files directly
   - No path provided → scan the current working directory for `.md` and `.txt` files

2. Verify files exist and are readable:
   - If no files found: stop. Report "No .md or .txt files found at [path]. Provide a folder path or list of files to process."
   - If a specific file path does not exist: stop. Report "File not found: [path]. Check the path and try again."

3. Check for unsupported file formats:
   - If user provides only `.docx`, `.xlsx`, `.pdf`, or similar: stop. Report "Unsupported file types. This skill processes .md and .txt files only."

4. Determine digest date:
   - If user specifies a date → use that date in output filename
   - If not specified → use today's date (YYYY-MM-DD format)

### Step 2: Read and Parse Files

1. Read each file in turn and extract:
   - **Project or area name:** inferred from filename, H1/H2 heading, or leading section header
   - **Status indicator:** on track / at risk / blocked — detected from keywords ("blocked", "delayed", "at risk", "completed", "done", "✅", "⚠️", "🔴") or inferred from context
   - **Key updates:** bullet points, sentences describing progress, decisions, or changes
   - **Action items:** tasks with any mention of owner name and/or due date
   - **Blockers:** sentences or bullets mentioning dependencies, blockers, or unresolved issues

2. Handle empty or sparse files:
   - If a file is empty or contains only headings with no body content: skip it; note in digest footer as "Files with no updates: [filename]"
   - If a file has content but no structured indicators: include as raw notes under the filename; add note "No structured status found — raw content included"

### Step 3: Group and Deduplicate

1. Group extracted content by project or area:
   - Use project name from file heading if available
   - Use filename (without extension) as fallback project name

2. Identify cross-cutting signals across all files:
   - Recurring blockers (same blocker mentioned in 2+ files)
   - Action items with no identified owner
   - Action items with no due date
   - Projects with "blocked" status

3. Flag possible duplicate projects:
   - If two file headings look similar (e.g., "Project Alpha" and "Alpha Q2"): group under a shared section and add note "[Possible duplicates — verify manually]"
   - Do not silently merge

4. Check for large input:
   - If 20+ files or total content exceeds ~10,000 words: add a note at digest header: "Large input: [N] files processed. Review for completeness."

### Step 4: Check for Existing Output File

1. Check if `weekly-digest-[date].md` already exists in the working directory:
   - If yes: ask user — "File weekly-digest-[date].md already exists. Overwrite or save as weekly-digest-[date]-v2.md?"
   - Wait for response before writing

### Step 5: Write Digest

1. Write `weekly-digest-YYYY-MM-DD.md` using the Output Format below
2. Populate all sections; mark any empty section explicitly (e.g., "No blockers reported")
3. Report in chat: "Digest written: weekly-digest-[date].md — [N] files processed, [N] projects, [N] action items"

---

## Output Format

```markdown
# Weekly Digest — [Date]

**Compiled from:** [N] files | **Projects covered:** [N] | **Action items:** [N]
[Note if large input: "Large input: N files — review for completeness"]

---

## Summary

[2–4 sentences: overall week health, key progress, main risks or blockers]

---

## Projects

### [Project / Area Name]
- **Status:** ✅ On track / ⚠️ At risk / 🔴 Blocked
- **Updates:** [key progress points, 1–3 bullets]
- **Action items:** [owner] — [action] by [date or TBD]
- **Blockers:** [if any; "None" if clear]

### [Next Project...]

---

## Cross-Cutting Action Items

| Owner | Action | Due | Source File |
|-------|--------|-----|-------------|
| [name or TBD] | [action description] | [date or TBD] | [filename.md] |

---

## Risks & Blockers

- [Blocker or risk description — source: filename.md]
- [Recurring blocker flagged across N files]

---

## Files Processed

Files included: [list]
Files with no updates: [list, or "None"]
[Possible duplicates: [list, or omit if none]]
```

**Field rules:**
- Status: use ✅ / ⚠️ / 🔴 based on detected keywords; default to ✅ if no risk signals found
- Action items: include owner when mentioned; use "TBD" if no owner identified; flag "No owner" items in Cross-Cutting section
- Summary: write from extracted content — do not invent progress or add assumptions

---

## Edge Cases

1. **Empty or heading-only files:** Skip; note in "Files with no updates" section
2. **No structured status indicators:** Include raw content; add note "No structured status found"
3. **Possible duplicate project names:** Group together; add "[Possible duplicates — verify manually]" note
4. **20+ files or 10,000+ words total:** Proceed; add "Large input" note at digest header
5. **Digest file already exists:** Ask user before overwriting

---

## Negative Cases

- **No files found:** Stop. Report "No .md or .txt files found at [path]."
- **Invalid file path:** Stop. Report "File not found: [path]."
- **Only unsupported file formats:** Stop. Report "Unsupported file types. Convert to .md or .txt first."
