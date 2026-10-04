---
name: retro-pattern-analyzer
description: "Analyze sprint retrospective files and surface recurring pain points, unresolved action items, and positive patterns across sprints. Use when preparing quarterly reviews or identifying systemic issues. Triggers: 'analyze retro files', 'retro pattern analysis', 'find recurring issues in retrospectives', 'проанализируй ретро', 'паттерны в ретроспективах'."
version: 1.0.0
---

# Retro Pattern Analyzer

This skill analyzes retrospective files from multiple sprints and produces a structured report identifying recurring pain points, unresolved action items, and stable positive patterns. It reads `.md` and `.txt` files, normalizes different retro formats, and outputs `retro-patterns-YYYY-MM-DD.md`.

**Input:**
- 2 or more retrospective files in `.md` or `.txt` format
- Optional: folder path or list of file paths
- Optional: focus area (e.g., "technical issues only", "delivery problems")

**Output:**
- `retro-patterns-YYYY-MM-DD.md` — structured report with three blocks: recurring pains, unresolved action items, positive patterns

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that at least 2 files are provided
   - If only 1 file provided: stop. Report: "Pattern analysis requires at least 2 retrospective files. Please provide a second file or folder path."
   - If folder path given: list all `.md` and `.txt` files in the folder; if fewer than 2 found, stop with same message

2. Check each file is readable
   - If any file is unreadable or path does not exist: skip that file, report: "File [name] not found or unreadable — excluded from analysis."
   - Continue with remaining files if at least 2 remain

3. If optional focus area provided: note it; use it to filter themes in Step 3

### Step 2: Parse Retrospective Files

1. For each file, identify structural sections using keyword detection:
   - **What went wrong / Problems / Improvements / Minuses / Keep Stop Start** → `went-wrong` bucket
   - **What went well / Strengths / Positives / Pluses** → `went-well` bucket
   - **Action items / Next steps / TODOs / Agreements** → `actions` bucket
   - **Russian equivalents:** Что мешало / Проблемы / Минусы → `went-wrong`; Что помогло / Плюсы → `went-well`; Договорённости / Задачи → `actions`

2. Extract all bullet points or numbered items from each section
   - One item per line/bullet
   - Strip formatting markers (-, *, [ ], ✓)
   - Preserve the source file name as sprint identifier (use filename or date found in file header)

3. If file has no recognizable section headers:
   - Process entire file as free-text
   - Attempt keyword-based classification per line
   - Prepend note in report: "File [name] had no standard structure — classified by keywords"

4. Determine chronological order:
   - Use date in filename (e.g., `retro-2026-03-15.md`) if present
   - Else use date found in first line of file
   - Else use file modification date
   - Sort sprints chronologically from oldest to newest

### Step 3: Identify Patterns

1. **Normalize themes:** Group items that describe the same issue using semantic similarity
   - Examples: "deployment takes too long" + "slow deploys" + "release process slow" → one theme: "slow release / deployment"
   - Aim for 5–12 distinct themes across all files; merge closely related items

2. **Count theme frequency:** For each theme, record which sprint files it appears in
   - Threshold for "recurring": appears in ≥2 sprint files

3. **Calculate trend** for each recurring theme:
   - `↑ growing` — appears in 2+ consecutive recent sprints and not in early sprints
   - `↓ resolving` — appeared in early sprints but not in the 2 most recent
   - `→ stable` — appears consistently or non-consecutively without clear trend

4. **Identify unresolved action items:**
   - For each item in `actions` bucket of sprint N: check if the same or similar issue appears in `went-wrong` of sprint N+1 or later
   - If yes → mark as unresolved; record which sprint it was raised and which sprint it reappeared

5. **Identify positive patterns:**
   - Themes appearing in `went-well` across ≥2 sprints → stable positive pattern
   - Record frequency

6. **Apply focus filter** if provided: keep only themes matching the focus area keyword

**Edge Cases:**
- File with 50+ items: process all items, but group into max 10 themes plus an "Other" bucket for less frequent items
- Only 2 files (minimum set): process normally; add note in report: "Analysis based on 2 sprints — patterns are preliminary"
- Mixed languages (EN + RU files): detect per-file, normalize to report language (majority-language file wins)
- Multiple retro formats in one set: normalize to went-well/went-wrong/actions before pattern matching

### Step 4: Generate Report

1. Use the output template structure (see Output Format below)
2. Fill three blocks:
   - **Recurring Pains:** themes from `went-wrong` with frequency ≥2, sorted by frequency descending
   - **Unresolved Action Items:** actions raised in one sprint that reappeared in a later sprint
   - **Stable Positive Patterns:** themes from `went-well` with frequency ≥2
3. If a block has no entries: write "None identified in this set of sprints"
4. Add metadata header: list sprint files analyzed, total item count processed, generation date

### Step 5: Save Output

1. Write file as `retro-patterns-YYYY-MM-DD.md` (today's date)
2. Save to the folder where the retro files are located, or to the working directory if mixed paths were provided
3. Confirm: "Report saved as retro-patterns-[date].md — [N] themes identified across [N] sprints."

---

## Output Format

```markdown
# Retro Pattern Analysis
**Sprints analyzed:** [list of file names / date range]
**Total items processed:** [N] across [N] files
**Generated:** YYYY-MM-DD

---

## 🔴 Recurring Pains (went-wrong, ≥2 sprints)

| Theme | Sprints | Frequency | Trend |
|-------|---------|-----------|-------|
| [theme 1] | S1, S2, S4 | 3/4 | ↑ growing |
| [theme 2] | S2, S3 | 2/4 | → stable |

## 🔁 Unresolved Action Items

| Action Item | Raised in | Reappeared in | Status |
|-------------|-----------|---------------|--------|
| [action 1] | S2 | S3, S4 | unresolved |

## ✅ Stable Positive Patterns (went-well, ≥2 sprints)

| Theme | Sprints | Frequency |
|-------|---------|-----------|
| [theme] | S1, S3, S4 | 3/4 |

---
*Generated by retro-pattern-analyzer · [date]*
```

**Field rules:**
- Theme names: concise, 3–7 words, plain language
- Frequency format: `N/total` (e.g., 3/5 means appeared in 3 of 5 sprints)
- Trend: one of `↑ growing`, `↓ resolving`, `→ stable`
- Sprint identifiers: use filename or inferred date label

---

## Negative Cases

- Only 1 file provided → stop, ask for a second file. Do not produce partial report.
- File does not contain any recognizable retrospective content (no went-well/went-wrong/actions signals at all) → skip file, warn user, continue with remaining files.
- All provided files are unreadable or non-existent → stop. Report each missing path.
- Folder path does not exist → stop. Report the path and ask user to verify.
