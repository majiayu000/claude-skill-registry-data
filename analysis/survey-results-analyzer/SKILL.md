---
name: survey-results-analyzer
description: "Analyze survey CSV files and extract quantitative frequencies, qualitative themes, and Top-3 insights. No Python required — Cowork-native. Use when reviewing Google Forms/Typeform/SurveyMonkey exports, preparing stakeholder reports, or turning raw survey data into actionable findings. Triggers: 'analyze survey results', 'survey results analyzer', 'проанализируй результаты опроса', 'анализ опроса'."
version: 1.0.0
---

# Survey Results Analyzer

This skill analyzes survey result files (CSV) and produces a structured markdown report with frequency distributions, open-ended response themes, and a synthesized Top-3 insights summary. It works in two modes simultaneously — quantitative (close-ended questions) and qualitative (open-ended responses) — without requiring any Python or data analysis background.

**Input:**
- CSV file with survey data (one row per respondent, first row = headers), provided as an attachment or via workspace folder path

**Output:**
- `survey-analysis-{filename}.md` — structured markdown report saved to the workspace folder

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian — including all section headers, labels, key findings, and insight text in the generated report
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate and Load the CSV File

1. Check that the user provided a CSV file (attachment or file path in workspace folder)
   - If no file provided: stop and return: "Please attach a CSV file with survey results or provide the file path in your workspace folder."

2. Read the file and validate structure:
   - Confirm first row is headers (column names / question text)
   - Confirm at least 2 columns exist
   - Confirm at least 1 data row exists
   - If file is not parseable as CSV (merged cells, missing headers, non-comma delimiter): return "File could not be parsed as a survey CSV. Check that it has a single header row and comma-separated values."
   - If only 1 column detected: return "Only one column detected — need at least two columns (questions) to produce a meaningful analysis."

3. Count respondents (N = number of data rows)
   - If N < 5: proceed but flag with a warning (see Edge Cases)

### Step 2: Classify Column Types

For each column in the CSV:

1. **Close-ended detection** — column is close-ended if values match any of:
   - Binary: yes/no, true/false, 0/1, agree/disagree
   - Numeric scale: all values are integers in range 1–5 or 1–10 (Likert scale)
   - Text labels representing a scale: "Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree" (map to 1–5)
   - Multiple choice: limited set of distinct text values (≤ 8 unique values for N ≥ 10)

2. **Open-ended detection** — column is open-ended if values are free-form text (high variety, average length > 5 words)

3. **Unclassifiable columns** — skip and note in report as "Column skipped: could not classify type"

**Edge Cases:**
- Mixed numeric + text values in a Likert column: treat as text-label Likert if labels are recognizable scale terms; otherwise treat as open-ended
- Column with >8 unique values but short responses (1–3 words each): treat as multiple choice
- Language detection per column not required — process all text as-is

### Step 3: Quantitative Analysis (Close-Ended Columns)

For each close-ended column:

1. **Multiple choice / binary columns:**
   - Compute response count and percentage for each distinct value
   - Identify the dominant answer (highest % with label)
   - Sort by frequency descending

2. **Likert scale columns (numeric 1–5 or 1–10):**
   - Map text labels to numeric if needed (see Step 2); if mapping was applied, add a note in the report under that column: "Note: text labels mapped to numeric scale (Strongly agree=5 … Strongly disagree=1)"
   - Compute mean (rounded to 1 decimal)
   - Compute distribution: count and % for each scale point
   - Flag if mean < 2.5 (negative sentiment) or > 4.0 (strong positive)

3. **Key finding per column:** write one sentence summarizing the main signal (e.g., "67% of respondents cited cost as the top concern")

### Step 4: Qualitative Analysis (Open-Ended Columns)

For each open-ended column:

1. Read all non-empty responses
2. Extract recurring keywords and phrases (manual semantic grouping — do not use code):
   - Group responses by shared topic/theme (e.g., "speed", "pricing", "UX")
   - Count how many responses belong to each theme
   - Compute theme frequency as % of total non-empty responses
3. Identify outlier responses: unique mentions that don't fit any theme (flag if ≥ 2 respondents share the same outlier)
4. Assign theme names (descriptive, 1–3 words each)
5. List representative example quotes (1–2 per theme, verbatim, shortened to ≤ 15 words if long)

**Edge Cases:**
- Responses in mixed languages: group themes per language; note "EN themes" and "RU themes" separately
- Very short responses (1–2 words): group by exact match or semantic similarity
- All responses are unique (no themes emerge): note "No recurring themes found — responses are highly varied"

### Step 5: Synthesize Top-3 Insights

1. Review all quantitative key findings and qualitative themes across all columns
2. Select the 3 most significant findings based on:
   - Statistical prominence (dominant choices, extreme Likert means)
   - Cross-column patterns (theme appears in both qualitative and quantitative columns)
   - Potential impact on decisions (high-frequency pain, strong positive signal, or unexpected outlier with meaningful pattern)
3. For each insight:
   - Write a 1-sentence finding statement
   - Include supporting evidence (% or theme frequency)
   - Add 1-sentence implication ("This suggests...")

### Step 6: Generate and Save Report

1. Compose the markdown report using the Output Format template below
2. Save as `survey-analysis-{original-filename}.md` in the workspace folder
3. Confirm file saved and print path to user

---

## Output Format

```markdown
# Survey Analysis: {filename}

**Date:** YYYY-MM-DD  
**Respondents:** N  
**Questions analyzed:** X (Y quantitative, Z qualitative)

> ⚠️ Small sample size warning: N={n} respondents — treat findings as directional only.
> (Include only if N < 5)

---

## Summary Table

| # | Question | Type | Key Finding |
|---|----------|------|-------------|
| 1 | [Column header] | Likert 1–5 | Mean: 4.2 — predominantly positive |
| 2 | [Column header] | Multiple choice | 67% chose "Cost" as top concern |
| 3 | [Column header] | Open-ended | 3 themes: Speed (40%), UX (35%), Price (25%) |

---

## Quantitative Analysis

### [Column header]

**Type:** Multiple choice  
- Option A: 67% (N=20)
- Option B: 20% (N=6)
- Option C: 13% (N=4)

**Key finding:** 67% of respondents cited cost as the primary concern.

---

### [Column header]

**Type:** Likert 1–5  
**Mean:** 4.2 / 5

| Score | Count | % |
|-------|-------|---|
| 5 ⭐ | 12 | 40% |
| 4 ⭐ | 9 | 30% |
| 3 ⭐ | 6 | 20% |
| 2 ⭐ | 2 | 7% |
| 1 ⭐ | 1 | 3% |

**Key finding:** Strong positive satisfaction — 70% rated 4 or 5.

---

## Qualitative Analysis

### [Column header]

**Responses analyzed:** N (X empty responses excluded)

| Theme | Frequency | % | Example quote |
|-------|-----------|---|---------------|
| Speed / Performance | 12 | 40% | "loads too slowly for daily use" |
| UX / Interface | 10 | 33% | "hard to find the filters" |
| Pricing | 8 | 27% | "too expensive for small teams" |

**Outliers (unique mentions):** "Missing Notion integration" — mentioned by 2 respondents.

---

## Top-3 Insights

### 1. [Insight title]

**Finding:** [One-sentence statement with supporting evidence: X% or N respondents]  
**Implication:** This suggests [actionable interpretation for the team].

### 2. [Insight title]

**Finding:** [One-sentence statement]  
**Implication:** This suggests [actionable interpretation].

### 3. [Insight title]

**Finding:** [One-sentence statement]  
**Implication:** This suggests [actionable interpretation].

---

*Generated by survey-results-analyzer · {date}*
```

---

## Negative Cases

- **No file provided:** Return "Please attach a CSV file with survey results or provide the file path in your workspace folder."
- **File is not parseable CSV:** Return "File could not be parsed as a survey CSV. Check that it has a single header row and comma-separated values."
- **Only 1 column detected:** Return "Only one column detected — need at least two columns (questions) to produce a meaningful analysis."
- **All columns unclassifiable:** Return "Could not classify any columns as close-ended or open-ended. Check that columns contain actual response data."
- **File is completely empty (headers only, no data rows):** Return "No survey responses found. The file has headers but no data rows."
