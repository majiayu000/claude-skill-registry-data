---
name: morning-standup-brief-generator
description: "Compile local notes, tasks, and project files into a structured standup brief — no connectors required. Use when preparing for morning standup, daily sync, or team check-in. Triggers: 'morning standup brief', 'daily brief', 'prepare me for standup', 'подготовь меня к стендапу', 'дейли бриф', 'утренний бриф'."
version: 1.0.0
---

# Morning Standup Brief Generator

This skill compiles local notes, task files, and project documents into a structured daily standup brief in the format: **Yesterday / Today / Blockers / Questions**. It works entirely from local files — no MCP connectors, external APIs, or technical setup required.

**Input:**
- Path to a working directory (or Cowork session folder) containing `.md` and/or `.txt` files

**Output:**
- Standup brief displayed in chat
- File `standup-brief-YYYY-MM-DD.md` saved to the working directory

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check if the user has provided a working directory path.
   - If no path is provided and no Cowork session folder is active: stop and report: "Please provide the path to your working folder. Example: /Users/yourname/work-notes/"
   - If path is provided but does not exist: report "Folder not found: [path]. Please check the path and try again."

2. Check for readable files (`.md` and `.txt`) in the directory.
   - If the folder exists but contains no `.md` or `.txt` files: report "No readable files found (.md, .txt). Add notes or task files to the folder and try again."

3. Check if a `standup-brief-YYYY-MM-DD.md` file for today's date already exists.
   - If it exists: ask "A standup brief for today already exists. Overwrite it?"
   - If user confirms: proceed. If user declines: stop cleanly.

### Step 2: Discover and Filter Files

1. List all `.md` and `.txt` files in the directory (non-recursive; top level only).
2. Apply time filter: prioritize files **modified in the last 48 hours**.
   - If no files modified in last 48 hours: include all files and note "No recent changes found — using all files in folder."
   - If more than 20 files match: limit to those modified in the last 48 hours and notify: "Found [N] files — filtered to [M] recently modified (last 48h)."
3. Build a list of files to process. For each file, note its name and modification date.

### Step 3: Extract Task Signals

Read each selected file and extract the following:

1. **Completed items** (for Yesterday section):
   - Lines containing `- [x]`, `[x]`, `✓`, `DONE`, `COMPLETED`
   - Include the item text (trim markers)

2. **Open tasks** (for Today section):
   - Lines containing `- [ ]`, `[ ]`, `TODO`, `#task`, `#todo`
   - Order by earliest deadline if dates are present (e.g., `(due YYYY-MM-DD)`, `by [date]`)

3. **Blockers** (for Blockers section):
   - Lines containing `BLOCKER`, `BLOCKED`, `#blocked`, `waiting on`, `waiting for`, `depends on`, `stuck`
   - Also: open tasks with no progress markers that appear in multiple files or are repeated

4. **Questions / Awaiting response** (for Questions section):
   - Lines containing `?`, `ASK`, `#question`, `waiting for [name]`, `@[name]`, `ожидаю`, `вопрос:`

**Edge Cases:**
- If a file contains no structured task markers: extract bullet points and short sentences as candidate items; mark section as `(extracted from notes — no formal task markers found)`.
- If a file contains mixed languages (EN + RU): process all markers in both languages; output in the dominant language of the file content.

### Step 4: Prioritize and Deduplicate

1. Remove duplicate items (same text appearing in multiple files — keep once).
2. Sort Today items:
   - Items with explicit deadlines first (nearest deadline at top)
   - Then remaining open tasks in order of file appearance
3. Limit sections to reasonable length:
   - Yesterday: max 7 items
   - Today: max 7 items
   - Blockers: list all (no cap)
   - Questions: list all (no cap)
4. If a section has no items: write `— none` under that section header.

### Step 5: Compose and Output Brief

1. Build the standup brief using the Output Format template below.
2. Insert today's date (YYYY-MM-DD) in the title.
3. Add a footer line listing all source files processed.
4. Display the full brief in chat.
5. Save as `standup-brief-YYYY-MM-DD.md` in the working directory.
   - Confirm save with: "Brief saved to: [path]/standup-brief-YYYY-MM-DD.md"

---

## Output Format

```markdown
# Standup Brief — YYYY-MM-DD

## Yesterday (Done)
- [completed item 1]
- [completed item 2]

## Today (Plan)
- [open task 1]
- [open task 2]

## Blockers
- [blocker 1]
— none (if no blockers found)

## Questions / Awaiting Response
- [question or pending action 1]
— none (if nothing pending)

---
*Generated: YYYY-MM-DD | Sources: [file1.md, file2.md, ...]*
```

**Field rules:**
- Each item is one line, starting with `- `
- No sub-bullets (keep scannable for standup format)
- Completed items: state what was finished, not the task description alone
- Today items: actionable verb + object (e.g., "Review PR #42", "Send status update to Alex")
- Blockers: name the blocker and who/what is blocking
- Questions: include the recipient if known (e.g., "Awaiting answer from @Maria on API spec")

---

## Negative Cases

- **No path provided + no active Cowork folder:** Stop. Report: "Please provide the path to your working folder."
- **Folder not found at path:** Stop. Report: "Folder not found: [path]. Check the path and retry."
- **Folder is empty (no .md/.txt):** Stop. Report: "No readable files (.md, .txt) found in [path]. Add notes or task files first."
- **All files are binary or unreadable:** Skip unreadable files silently; if all files are unreadable, report: "Could not read any files in [path]. Files may be in unsupported formats."
- **Today's brief already exists (user declines overwrite):** Stop cleanly. Report: "Keeping existing brief at [path]/standup-brief-YYYY-MM-DD.md."
