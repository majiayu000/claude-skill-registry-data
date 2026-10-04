---
name: jobs-to-be-done-extractor
description: "Extract JTBD statements from custdev transcripts and interview notes. Synthesizes multiple md/txt files into a prioritized JTBD map with evidence quotes and frequency counts. Use when converting custdev notes to structured jobs, preparing for roadmap sessions, synthesizing interview patterns. Triggers: 'extract jobs to be done', 'JTBD from interviews', 'синтез custdev заметок', 'извлеки JTBD из интервью'."
version: 1.0.0
---

# Jobs-to-be-Done Extractor

This skill reads a folder of custdev transcripts and interview notes (md or txt files) and extracts structured Jobs-to-be-Done (JTBD) statements with evidence quotes and cross-file frequency counts. Output is a prioritized JTBD map with confidence labels ready for roadmap and prioritization work.

**Input:**
- Folder with custdev files (.md or .txt) — transcripts, interview notes, open-ended survey responses

**Output:**
- Markdown JTBD map with ranked statements, evidence quotes, source references, and a Patterns & Gaps section

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate and Read Input Files

1. Ask the user to point to the folder containing custdev files (if not already provided).
2. List all .md and .txt files in the folder.
   - If no files found: stop. Report: "No input files found. Point me to a folder with custdev transcripts or notes (md or txt)."
   - If files found: report count — "Reading N files from [folder]."
3. Read each file sequentially.
   - If a file is empty or unreadable: skip it, note filename — "Skipped: [filename] — empty or unreadable." Continue with remaining files.
4. If only 1 file found: note — "Single source — frequency analysis not applicable. All statements treated as low-confidence."
5. If more than 15 files found: warn — "Large file set — review may take longer. Consider running on a subset for faster iteration." Then proceed with processing all files.

### Step 2: Extract User Motivation Signals

1. For each file, identify sentences or passages that contain:
   - Explicit user goals ("I want to...", "I need to...", "I'm trying to...")
   - Recurring frustrations or pain points ("it's hard to...", "I hate when...", "I always have to...")
   - Workarounds the user performs to achieve a goal
   - Desired outcomes ("it would be great if...", "I wish I could...")
   - Direct quotes about motivations or context

2. Tag each extracted signal with: source filename + quote text.

3. For files that are raw interview transcripts with interleaved Q&A:
   - Focus on respondent turns (lines after "A:", "R:", or natural speaker markers)
   - Skip interviewer questions and facilitator notes
   - Note in output if transcript structure was ambiguous

**Edge Cases:**
- Mixed-language files (EN + RU): extract signals in the original language of each file; note "Mixed-language input detected" in the output Notes section.
- Files with only metadata, headers, or empty bullets: flag the file — "No extractable user signals found in [filename]." Continue with other files.
- Quantitative-only files (numeric ratings only, no open-ended text): flag — "Quantitative data only in [filename]; skipping." Continue.

### Step 3: Cluster Signals into JTBD Statements

1. Group extracted signals by underlying motivation (not surface-level wording).
2. For each cluster, formulate a JTBD statement in canonical format:
   `When [situation], I want to [motivation], so I can [outcome].`
3. Select the most representative quote from each source file for the Evidence section.
4. Aim for 3–10 JTBD statements total. If signals are very homogeneous, combine into fewer; if very diverse, keep distinct.

### Step 4: Calculate Frequency and Assign Confidence

1. For each JTBD statement, count:
   - Number of distinct source files containing supporting signals
   - Total number of supporting quotes across all files
2. Assign confidence label:
   - **High**: signals from 3+ distinct files
   - **Medium**: signals from exactly 2 files
   - **Low**: signals from only 1 file
3. Sort JTBD statements by file count (descending). Ties broken by quote count.

### Step 5: Identify Patterns and Gaps

1. **Recurring themes**: topics or motivations mentioned in 3 or more files — list with filenames.
2. **Single-source signals**: signals appearing in only 1 file — list as potential blind spots worth further research.

### Step 6: Format and Output JTBD Map

1. Produce the full JTBD map in the Output Format defined below.
2. Validate all sections are populated (or note "None identified" if applicable).

---

## Output Format

Respond with a markdown JTBD map using this structure:

```
## JTBD Map — [folder name or date]

### Jobs-to-be-Done

| # | JTBD Statement | Frequency | Confidence | Sources |
|---|----------------|-----------|------------|---------|
| 1 | When [situation], I want to [motivation], so I can [outcome]. | N files / M quotes | High | file-a.md, file-b.md, … |
| 2 | When [situation], I want to [motivation], so I can [outcome]. | 2 files / 3 quotes | Medium | file-c.md, file-d.md |
| 3 | When [situation], I want to [motivation], so I can [outcome]. | 1 file / 1 quote | Low | file-e.md |

---

### Evidence

**JTBD #1 — [short label]**
- "[Direct quote from user]" — file-a.md
- "[Direct quote from user]" — file-b.md

**JTBD #2 — [short label]**
- "[Direct quote from user]" — file-c.md

---

### Patterns & Gaps

**Recurring themes (3+ files):**
- [Theme]: present in file-a.md, file-b.md, file-c.md

**Single-source signals (potential blind spots):**
- [Signal] — file-e.md only

---

### Notes
- Total files processed: N
- Files skipped (if any): [filename — reason]
- Confidence scale: High = 3+ files, Medium = 2 files, Low = 1 file
```

**Field rules:**
- JTBD statements must follow canonical format: `When [situation], I want to [motivation], so I can [outcome].`
- Evidence quotes must be verbatim (or near-verbatim paraphrase if transcript is not verbatim) with source filename
- Confidence label is determined solely by file count, not quote count
- Patterns & Gaps section is always present even if empty (note "None identified")

---

## Negative Cases

- No folder provided or no files found → Stop. Report: "No input files found. Point me to a folder with custdev transcripts or notes (md or txt)."
- All files are empty or unreadable → Stop after processing. Report: "No extractable content found in any provided file. Verify file contents and try again."
- All files contain only quantitative data (numeric ratings, no text) → Report: "Files appear to contain only quantitative data. JTBD extraction requires qualitative text — interview notes, quotes, or open-ended responses."
- Zero user signals extracted after reading all files → Report: "No user motivation signals found. Ensure files contain interview notes or direct user quotes, not just metadata or headers."
