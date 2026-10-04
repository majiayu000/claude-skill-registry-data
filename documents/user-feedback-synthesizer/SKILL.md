---
name: user-feedback-synthesizer
description: "Synthesize user interview transcripts and feedback files into a prioritized insight report with themes, quotes, and open questions. Use when analyzing batches of user interviews, support tickets, or survey responses. Triggers: 'synthesize feedback', 'analyze user interviews', 'user feedback report', 'синтезируй фидбек', 'разбери транскрипты', 'отчёт по фидбеку'."
version: 1.0.0
---

# User Feedback Synthesizer

This skill reads a set of user interview transcripts, support tickets, and survey feedback files (`.md`, `.txt`, `.csv`) and generates a structured insight report: recurring themes ranked by frequency, supporting quotes as evidence, prioritized insights, and open questions. Output is saved as `feedback-insights-YYYY-MM-DD.md`.

**Input:**
- Folder path or list of `.md` / `.txt` / `.csv` files containing user feedback
- Optional: research question or focus area (e.g., "focus on onboarding pain points")
- Optional: output format preference (brief / detailed)

**Output:**
- `feedback-insights-YYYY-MM-DD.md` — structured report with Executive Summary, Themes, Prioritized Insights, Evidence Bank, Open Questions

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian and use Russian labels for all structured outputs (table headers, signal types, section titles, status messages)
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

**Russian output labels:**
- Signal types: Проблема (Pain), Желание (Desire), Похвала (Compliment), Путаница (Confusion)
- Section titles: Выводы (Executive Summary), Темы (Themes), Приоритизированные Идеи (Prioritized Insights), Открытые Вопросы (Open Questions), Обработанные Файлы (Files Processed)
- Table headers: Приоритет (Priority), Идея (Insight), Тема (Theme), Источники (Sources)
- Notes: use Russian equivalents for all standard notes ("Обнаружены противоречивые сигналы" for split signals, "Обработано [N] файлов" for file counts, etc.)

---

## Instructions

### Step 1: Validate Input

1. Determine input source from the user's message:
   - Folder path → scan all `.md`, `.txt`, and `.csv` files in that folder
   - List of files → use those files directly
   - No path provided → scan the current working directory for `.md`, `.txt`, and `.csv` files

2. Verify files exist and are readable:
   - If no files found at path: stop. Report "No .md, .txt, or .csv files found at [path]. Provide a folder path or list of files to process."
   - If a specific file path does not exist: stop. Report "File not found: [path]. Check the path and try again."

3. Check for unsupported formats:
   - If user provides only `.docx`, `.xlsx`, `.pdf`, or similar: stop. Report "Unsupported file types. This skill processes .md, .txt, and .csv files only. Convert files first."

4. Check for empty files:
   - If all files are empty: stop. Report "All provided files are empty. Add feedback content and try again."
   - If some files are empty: note them; skip during processing; include in "Files with no signals" list.

5. Note research question if provided; if not provided, add note "No focus area specified — synthesizing all themes found".

6. If fewer than 3 files: add note "Pattern detection is limited with fewer than 3 sources — findings may reflect individual opinions rather than trends."

### Step 2: Read and Extract Signals

1. For `.md` and `.txt` files:
   - Read full content
   - Extract atomic feedback signals: problems, desires, complaints, compliments, questions, feature requests
   - For each signal: record text, approximate location (filename, section/line), and signal type

2. For `.csv` files:
   - Read header row to identify content columns (look for headers containing: "comment", "feedback", "response", "text", "answer", "note", "message")
   - Treat each non-header row as a separate feedback item
   - If no obvious content column found: use all non-ID, non-timestamp columns; record the column names used in the output under "Files Processed" section (note: "CSV columns processed: [list]")
   - Treat each row as equivalent to one feedback source item

3. Signal types to identify:
   - **Pain** — user expresses a problem, friction, or complaint
   - **Desire** — user expresses a wish, need, or feature request
   - **Compliment** — user expresses satisfaction or positive experience
   - **Confusion** — user expresses uncertainty, misunderstanding, or asks "why" / "how"

4. Extract verbatim quotes for high-signal sentences (surprising, specific, or emotionally charged phrases)

### Step 3: Cluster Signals into Themes

1. Group extracted signals into named themes:
   - A theme = a topic that appears in 2+ signals across the dataset
   - Name each theme with a clear, descriptive label (e.g., "Onboarding complexity", "Missing export feature")
   - Assign dominant signal type to each theme (Pain / Desire / Compliment / Confusion)

2. Count per theme:
   - **Source count**: number of distinct files mentioning this theme
   - **Mention count**: total number of signals mapped to this theme

3. Handle conflicting signals:
   - If theme has both Pain and Compliment signals: flag as "split signal" in output
   - Include both perspectives in the theme description

4. Single-source signals:
   - If a signal appears in only 1 file: do not create a standalone theme
   - Instead, group under a "Minor signals" section in Open Questions

### Step 4: Rank Themes

1. Sort themes by **source count** (number of distinct files) — descending
2. Secondary sort: by mention count — descending
3. Include all themes with source count ≥ 2 in the main Themes section
4. Single-source themes move to Open Questions

### Step 5: Select Evidence Quotes

1. For each top theme (up to top 7):
   - Select 1–2 representative verbatim quotes
   - Prefer quotes that are: specific, emotionally expressive, or particularly clear
   - Record source filename for each quote

2. Do not paraphrase or summarize quotes — use exact text from the source file

### Step 6: Build Prioritized Insights

1. Convert top themes into actionable insight statements:
   - Insight = a clear statement of what users need, experience, or believe
   - Format: "[Signal type]: [User segment / context] [verb phrase] [specific problem or need]"
   - Example: "Pain: Users lose context when navigating between dashboard tabs"

2. Assign priority:
   - **High** — theme appears in 3+ source files
   - **Medium** — theme appears in exactly 2 source files
   - **Low** — theme appears in 1 file (listed in Open Questions, not Insights table)

### Step 7: Identify Open Questions

1. Collect:
   - Single-source signals (potentially important but unconfirmed)
   - Conflicting signals where both perspectives exist
   - Gaps: topics that are conspicuously absent (e.g., "no feedback on pricing despite pricing page focus")
   - Questions raised by the data but not answerable from current sources

2. Format as actionable research questions where possible:
   - "Is [X] a widespread issue or limited to [segment]?"
   - "Does [observed behavior] apply to new users only?"

### Step 8: Check Output File and Write

1. Determine output date:
   - Use today's date in YYYY-MM-DD format

2. Check if `feedback-insights-[date].md` already exists in working directory:
   - If yes: ask user — "File feedback-insights-[date].md already exists. Overwrite or save as feedback-insights-[date]-v2.md?"
   - Wait for response before writing

3. Write `feedback-insights-YYYY-MM-DD.md` using the Output Format below

4. Report in chat: "Insights saved: feedback-insights-[date].md — [N] files processed, [N] themes identified, [N] insights"

---

## Output Format

See `templates/feedback-insights-template.md` for the complete output file structure.

Summary of sections:

```markdown
# Feedback Insights — [Date]

**Sources:** [N] files | **Signals extracted:** [N] | **Themes identified:** [N]
[Note: large input / limited sources / language mix / focus area — if applicable]

---

## Executive Summary
[3–5 sentences: main findings, top 2–3 themes, overall signal health]

---

## Themes
### 1. [Theme Name] — [N] sources, [N] mentions
- **Signal type:** Pain / Desire / Compliment / Confusion [/ Split signal]
- **Description:** [what users say about this theme, 1–3 sentences]
- **Evidence:**
  - "[Verbatim quote]" — [source-file.md]

### 2. [Theme Name] — [N] sources, [N] mentions
...

---

## Prioritized Insights

| Priority | Insight | Theme | Sources |
|----------|---------|-------|---------|
| High     | [insight statement] | [Theme] | [N] files |

---

## Open Questions
- [Research question or knowledge gap]

---

## Files Processed
Files included: [list]
Files with no signals: [list, or "None"]
[Split signals flagged: [list, or omit]]
```

**Field rules:**
- Themes: ranked by source count (distinct files), not total mentions
- Quotes: verbatim from source files; never paraphrased
- Insights: specific actionable statements, not generic observations
- Priority: High ≥ 3 files | Medium = 2 files | Low = 1 file (→ Open Questions)

---

## Edge Cases

1. **Fewer than 3 source files** — process normally; add note about limited pattern detection
2. **CSV with no obvious content column** — use all non-ID/timestamp columns; note column names used
3. **Mixed-language files (EN + RU)** — process both; group by theme regardless of language; note mix in output
4. **Split signals (conflicting opinions on same topic)** — include both; flag theme as "Split signal"
5. **Very large input (50+ files or 20,000+ words)** — process all; add header note: "Large input: [N] files"
6. **No focus area provided** — proceed with open synthesis; add note in output header
7. **Output file already exists** — ask user before overwriting

---

## Negative Cases

- **No files found at path:** Stop. Report "No .md, .txt, or .csv files found at [path]."
- **Unsupported file types only (.docx, .pdf, .xlsx):** Stop. Report "Unsupported file types. Convert to .md, .txt, or .csv first."
- **All files empty:** Stop. Report "All provided files are empty."
