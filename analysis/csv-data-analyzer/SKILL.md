---
name: csv-data-analyzer
description: "Analyze CSV files with business data through a dialogue-based flow — no code, no Python, no plugins. Profiles dataset structure, asks what you want to understand, then delivers numbered insights and a plain-language interpretation. Use when analyzing sales exports, task lists, survey results, CRM data, or any CSV file. Triggers: 'analyze my CSV', 'analyze this CSV file', 'help me understand this data', 'what insights can you find in this spreadsheet', 'проанализируй CSV', 'разбери мой файл данных', 'что в этом CSV', 'помоги понять данные из таблицы'."
version: 1.0.0
---

# CSV Data Analyzer

This skill analyzes CSV files with business data for non-technical users through a conversational question flow — without code, formulas, or external tools. Claude reads the CSV directly, profiles its structure, asks one clarifying question about your goal, and delivers numbered insights with a plain-language interpretation.

**Input:**
- A CSV file accessible in the Cowork workspace (uploaded or in the selected folder)

**Output:**
- Markdown response with: dataset profile, numbered key insights, data snapshot table, plain-language interpretation, and follow-up suggestions

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Locate and Read the CSV File

1. Identify the CSV file from the user's message
   - If a file path or filename is provided: use it directly
   - If no path given: look for a CSV file in the Cowork workspace folder
   - If no CSV file found: stop and report — "I don't see a CSV file. Please upload the file or confirm it's in your selected Cowork folder, then try again."

2. Read the file content as plain text
   - If the file cannot be parsed as CSV (binary, corrupted, wrong format): stop and report — "This file doesn't appear to be a valid CSV. Please check the file format and try again."

### Step 2: Profile the Dataset

1. Count rows and columns (exclude the header row from row count)
   - If only 1 row exists (header only, no data): stop and report — "This CSV has no data rows — only headers. Please check the file and try again with a populated dataset."

2. Identify column names from the first row
   - If no header row detected (all rows look like data rows): assign generic names Column 1, Column 2, … and note: "I couldn't detect column headers — I'll use generic names."

3. Infer data type for each column: numeric, text, date, or boolean
   - If a column contains mixed types (numbers and text): note the inconsistency; treat column as text; recommend cleaning before numeric analysis

4. Check for empty/null cells per column
   - If a column has >30% empty cells: flag it as sparse and exclude from numeric analysis; include in profile with a note

5. If file has >500 rows: use a representative sample (first 200 rows + last 50 rows); note the sampling and warn — "File has {N} rows — analysis is based on a sample. Results may not reflect the full dataset."

### Step 3: Present Profile and Ask Clarifying Question

1. Output a brief dataset profile (2–3 lines):
   - Row count, column count, column names with types, notable issues (sparse columns, mixed types, date range if detected)

2. Ask one focused clarifying question:
   - "What would you like to understand — summary statistics, trends over time, top/bottom items, comparisons between groups, or something else?"
   - Do not proceed to analysis until user answers

### Step 4: Perform Analysis

Based on the user's answer, select the appropriate analysis mode:

- **Summary statistics:** min, max, average, median for numeric columns; value counts for text columns; date range if dates present
- **Trends over time:** group by date column; show values per period (day/week/month); identify direction (increasing/decreasing/flat)
- **Top/bottom items:** sort by a numeric column; show top 5 and bottom 5; calculate gap between them
- **Comparisons between groups:** group by a categorical column; aggregate a numeric column per group; highlight largest/smallest group
- **Custom goal:** if user's answer doesn't match the above modes, ask one follow-up to clarify which column(s) to focus on

**Edge Case — Ambiguous column reference:** If the user's goal involves a concept not directly named in the column headers (e.g., "show me churn" but no "churn" column), ask: "Which column represents [concept] in your data?" before proceeding.

Perform analysis using natural-language reasoning. No code execution required.

### Step 5: Format and Output Results

1. Output results using the Output Format structure (see below)
2. Populate Key Insights with 3–5 numbered findings in plain language
3. Include a Data Snapshot table: top 5–10 rows or the aggregated result (whichever is more informative)
4. Write Interpretation: 2–3 sentences explaining what the numbers mean in business terms

### Step 6: Offer Follow-Up Directions

1. Ask: "Anything else you'd like to explore in this data?"
2. Offer 2–3 concrete follow-up directions based on what was found (e.g., "Drill into the top-performing group", "Compare this period vs. last period", "Find outliers in [column]")
3. If user confirms done: close with a one-line summary of the session findings

---

## Output Format

```
### Dataset Profile
- **Rows:** {N}  |  **Columns:** {M}
- **Columns:** {col1 (numeric)}, {col2 (text)}, {col3 (date)}, …
- **Notable:** {any sparse columns, mixed types, date range, or sampling note}

### Key Insights
1. [Most significant finding — plain language, 1–2 sentences]
2. [Second finding]
3. [Third finding]
4. [Fourth finding, if applicable]
5. [Fifth finding, if applicable]

### Data Snapshot
| {Col1} | {Col2} | {Col3} |
|--------|--------|--------|
| …      | …      | …      |
*(Top 5–10 rows or aggregated result)*

### Interpretation
[2–3 sentences explaining what these numbers mean for the user's context — written for a business audience, not a data audience]

---
**What would you like to explore next?**
- [Follow-up direction 1]
- [Follow-up direction 2]
- [Follow-up direction 3]
```

---

## Negative Cases

- **No CSV file:** Stop with message — "I don't see a CSV file. Please upload the file or confirm it's in your selected Cowork folder, then try again."
- **Invalid file format:** Stop with message — "This file doesn't appear to be a valid CSV. Please check the file format and try again."
- **Empty dataset (header only):** Stop with message — "This CSV has no data rows — only headers. Please check the file and try again with a populated dataset."
- **Request for charts or visual output:** Explain — "I can't generate charts in this mode, but I can give you a detailed text summary and a data table you can paste into Excel or Sheets to visualize."
