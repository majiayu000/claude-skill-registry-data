---
name: industry-trend-brief
description: "Turn a folder of articles and industry clippings into a weekly trend signals brief for your product team. Use when preparing for planning sessions or roadmap reviews. Triggers: 'industry trend brief', 'trend signals from articles', 'тренд-бриф из статей', 'создай brief по трендам'."
version: 1.0.0
---

# Industry Trend Brief

This skill reads a folder of saved articles, excerpts, and text fragments and synthesizes them into a concise weekly trend signals brief for product teams. No web access required — fully file-based, designed for Cowork.

**Input:**
- Folder path containing articles or text fragments (md or txt files)

**Output:**
- Markdown response with executive summary, 3–5 ranked theme sections, and "What to Watch" list

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user provided a folder path.
   - If no path given: stop and respond: "Provide the path to a folder containing articles or text fragments in md or txt format."

2. Scan the folder for md and txt files.
   - If folder is empty or does not exist: stop and respond: "No readable files found at the provided path. Add md or txt files with article content and try again."
   - Skip any non-text files (PDF, DOCX, images); log skipped filenames: "Skipped [filename] — unsupported format."
   - Report the number of readable files found: "Found N files: [list filenames]."

3. If any file is shorter than 50 words: include it but flag as "weak signal — limited context."

### Step 2: Extract Signals from Each File

1. For each md/txt file, extract:
   - **Topic:** What is the article or fragment about? (1–3 word label)
   - **Key claims or data points:** Specific facts, statistics, or observations stated
   - **Signal type:** Classify as one of — trend, market shift, opportunity, risk, behavioral change

2. If a file contains no substantive content (only navigation fragments, boilerplate, or advertisement text with no body): skip and log: "Skipped [filename] — no substantive content found."

3. If all files are skipped due to no content: stop and respond: "No substantive content found for trend extraction. Ensure files contain article text, not page fragments or boilerplate."

### Step 3: Group Signals into Themes

1. Cluster related signals across files into named themes.
   - Example: signals about AI tools, AI cost reduction, and AI adoption → theme "AI Adoption Acceleration"
   - Deduplicate: if multiple files say the same thing, count as one signal with multiple sources

2. If all files cover a single topic: create one deep-dive theme section instead of multiple; add note: "All content covers one theme — single-topic brief generated."

### Step 4: Rank Themes by Signal Strength

1. For each theme, assign a signal strength rating:
   - **High** — mentioned in 3+ files OR contains a specific data point (stat, survey result, named company move)
   - **Medium** — mentioned in 2 files OR described as emerging trend by source
   - **Low (What to Watch)** — mentioned in 1 file, no supporting data; move to "What to Watch" section

2. Sort themes: High → Medium. Low-strength signals go to the "What to Watch" closing list.

3. Check for recency signals: look for date mentions, phrases like "this week", "this quarter", "recently launched", "just announced." If found, note recency in the theme section. If signals appear to be from different time periods, add note: "Some content may be outdated — review source dates."

### Step 5: Synthesize and Output Brief

1. Write an executive summary (1–2 sentences) capturing the dominant story across all files.

2. For each High/Medium theme (max 5), write a theme section with:
   - Theme name
   - Signal strength: High / Medium
   - Key signals (bullet list), each with source filename in parentheses
   - One-sentence product team takeaway: what this means for decisions, roadmap, or positioning

3. Write a "What to Watch" list of Low-strength signals (emerging, single-source, weak evidence).

4. Output the complete brief using the format defined in Output Format below.

---

## Output Format

Respond with this structure:

```
## Industry Trend Brief — [today's date or "this week"]

Processed [N] files. Identified [M] themes.

**Summary:** [1–2 sentence overview of the most significant signals across all files]

---

### Theme 1: [Theme Name]
**Signal strength:** High
**Key signals:**
- [Signal description] *(Source: filename.md)*
- [Signal description] *(Source: filename.md)*
**Takeaway for product team:** [1 sentence — what this means for product decisions]

### Theme 2: [Theme Name]
**Signal strength:** Medium
**Key signals:**
- [Signal description] *(Source: filename.md)*
**Takeaway for product team:** [1 sentence]

[Repeat for up to 5 themes]

---

### What to Watch
- [Weak or emerging signal 1] *(Source: filename.md)*
- [Weak or emerging signal 2] *(Source: filename.md)*

---
*Brief generated from [N] files. [M] themes identified. Review source files for full context.*
```

---

## Edge Cases

1. **Non-readable files in folder (PDF, DOCX, images):** Skip silently; list skipped filenames in the opening line. Process only md/txt files.
2. **Very short files (<50 words):** Include in processing; flag signal as "weak signal — limited context" in the theme output.
3. **All files cover a single topic:** Generate a single-topic deep-dive theme section; note: "All content covers one theme — single-topic brief generated."
4. **Mixed time signals (some clearly old, some recent):** Note recency in affected theme sections. Add a closing note if multiple time periods detected.

---

## Negative Cases

- If no folder path provided: Stop. "Provide the path to a folder containing articles or text fragments in md or txt format."
- If folder is empty or no md/txt files found: Stop. "No readable files found at the provided path. Add md or txt files with article content and try again."
- If all files contain no substantive content: Stop. "No substantive content found for trend extraction. Ensure files contain article text, not page fragments or boilerplate."
