---
name: research-folder-synthesizer
description: "Synthesize a folder of mixed local files (articles, notes, excerpts) into a structured thematic report with key findings and gaps. Use when consolidating research before writing a report, PRD, or strategy doc. Triggers: 'synthesize my research folder', 'research synthesis', 'turn my notes into a report', 'синтезируй папку с исследованиями', 'синтез ресёрча', 'сведи файлы в отчёт'."
version: 1.0.0
---

# Research Folder Synthesizer

This skill synthesizes a folder of heterogeneous local files (markdown notes, plain-text articles, research excerpts) into a structured thematic report. It clusters ideas across files, surfaces key findings and contradictions, and produces a single `research-synthesis.md` ready to use as a foundation for reports, PRDs, or strategy documents.

**Input:**
- A folder path or list of local file paths (`.md`, `.txt`, plain text)
- Optional: a focus question or research angle to guide thematic clustering

**Output:**
- `research-synthesis.md` — structured markdown with executive summary, named themes, key findings, contradictions/gaps, and source index

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user has provided a folder path or a list of files.
   - If nothing provided: stop and report — "No files found. Provide a folder path or paste file contents directly."

2. Attempt to read all files at the provided path.
   - Log each file name and detected type (`.md`, `.txt`, or plain text) in the report preamble.
   - Skip unreadable files (binary, images, etc.); add them to a "Skipped files" list — do not stop the pipeline.
   - If all files are unreadable: stop and report — "No readable text found. Provide `.md`, `.txt`, or plain-text files."

3. If only one file is provided: note that cross-source comparison will be unavailable; proceed with single-source synthesis.

4. If >20 files: note that depth per file will be reduced for brevity; proceed.

**Negative Cases:**
- Folder path not provided or folder empty → stop with clear message (Step 1.1).
- All files unreadable → stop with clear message (Step 1.2).
- User provides a URL instead of local files → clarify: "This skill works with local files. Paste the text directly or save it as a `.txt` file first."

---

### Step 2: Extract Content from Each File

1. Read each accessible file fully.

2. For each file, extract:
   - **Main claims** — central arguments or conclusions the source makes.
   - **Data points** — specific facts, numbers, quotes, or named entities.
   - **Notable phrases** — distinctive language worth preserving in attribution.

3. If the user provided a focus question, flag which files directly address it.

4. Build an internal per-file summary (not shown in output, used in Steps 3–4).

---

### Step 3: Identify Cross-File Themes

1. Compare per-file summaries and cluster related ideas.
   - Group by shared topic, argument direction, or domain.
   - Assign a short descriptive label to each cluster (e.g., "Market sizing", "User pain points", "Competitive landscape").

2. Aim for 2–5 themes; merge closely related clusters.

3. For each theme, note which files contribute and what they each say.

**Edge Case:**
- If files cover entirely unrelated topics with no clear overlap: create one theme per topic; note in the executive summary that the research collection is heterogeneous.

---

### Step 4: Detect Contradictions and Gaps

1. Within each theme, look for:
   - **Contradictions** — two sources making conflicting claims about the same fact or trend.
   - **Gaps** — topics implied by the research question or by some sources but absent from all others.

2. Log each contradiction as: "[Source A] says X; [Source B] says Y."

3. Log each gap as: "[Topic] not addressed in any source."

4. If neither contradictions nor gaps are found: write "No contradictions detected across sources."

---

### Step 5: Assemble and Write Report

1. Compose the report following the Output Format below.

2. Write the executive summary last (after themes and findings are complete).

3. Save the report as `research-synthesis.md` in the working directory.

4. Confirm the save path to the user.

---

## Output Format

```
# Research Synthesis: [topic or folder name]
**Date:** YYYY-MM-DD
**Files processed:** N
**Skipped files:** N (or "none")
**Focus question:** [question or "none"]

---

## Executive Summary
[3–5 sentences covering: scope of research, main conclusion, and key tension across sources]

---

## Themes

### Theme 1: [Label]
[2–4 sentences. Key claim derived from this theme. Supporting sources listed.]
**Sources:** file-a.md, file-b.txt

### Theme 2: [Label]
[2–4 sentences.]
**Sources:** file-c.md

---

## Key Findings
- [Finding 1] *(Source: file-a.md)*
- [Finding 2] *(Source: file-b.txt)*
...

---

## Contradictions & Gaps
- **Contradiction:** [Description] — file-a.md says X; file-b.txt says Y.
- **Gap:** [Topic area] not addressed in any source.
*(Or: "No contradictions detected across sources.")*

---

## Source Index
| File | Type | Main Topic | Language |
|------|------|------------|----------|
| file-a.md | Markdown | UX research | EN |
| file-b.txt | Plain text | Competitor notes | RU |

---

## Skipped Files
- image.png — unreadable format
*(Or omit section if no files were skipped)*
```

**Field rules:**
- Executive summary: 3–5 sentences; no bullet points.
- Theme labels: 2–5 words, title case, descriptive.
- Key findings: one concrete, specific statement per bullet; always attributed to a source.
- Contradictions/gaps: always present; state "none" explicitly if clean.

---

## Edge Cases

1. **Files in multiple languages (e.g., EN + RU mix):** Detect predominant language for the report; note language of each file in the source index; do not translate source content.
2. **Single file provided:** Produce internal theme clustering from that file alone; note "Cross-source comparison unavailable — only one file processed."
3. **Very large folder (>20 files):** Process all; condense per-file summary to 3 key points max; add a note that depth is reduced.
4. **User provides focus question:** Weight and flag content relevant to the question in each theme section; add a "Focus Answer" paragraph after the executive summary.

---

## Negative Cases

- Folder path not provided or folder is empty → "No files found. Provide a folder path or paste file contents directly." Stop.
- All files are unreadable (binary, images only) → "No readable text found. Provide `.md`, `.txt`, or plain-text files." Stop.
- User asks to synthesize a URL or web page → "This skill works with local files. Paste the text directly or save it as a `.txt` file first." Stop.
