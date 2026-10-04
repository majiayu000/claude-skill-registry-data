---
name: retention-cohort-interpreter
description: "Interpret cohort retention tables into plain-language diagnosis: curve health, drop-off points, benchmark comparison, and next steps. Use when reviewing weekly/monthly retention data, preparing investor updates, or diagnosing churn. Triggers: 'analyze retention cohort', 'interpret cohort table', 'diagnose retention drop', 'проанализируй таблицу удержания', 'интерпретируй когортный анализ', 'диагностируй отвал по когортам'."
version: 1.0.0
---

# Retention Cohort Interpreter

This skill interprets cohort retention tables for product managers and analysts, translating raw retention data into actionable plain-language diagnostics. Paste any cohort table (CSV or markdown) and receive a structured report: curve health assessment, key drop-off windows, industry benchmark comparison, hypotheses, and prioritized next steps.

**Input:**
- Cohort retention table (pasted as CSV, markdown table, or space-separated numbers; rows = cohorts, columns = time periods, values = % retained or user counts)
- Optional: product type (mobile app / SaaS / marketplace / consumer), cohort definition, current goal context

**Output:**
- Structured markdown report with sections: Curve Health, Key Drop-off Points, Benchmark Comparison, Hypotheses, Recommended Next Steps

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate and Parse Input

1. Check that a retention table is provided
   - If no table provided (description only, or question without data): stop and report: "Retention table required. Paste your cohort data as a CSV, markdown table, or plain numbers with headers."

2. Identify table structure
   - Rows = cohorts (signup week/month, acquisition channel, or similar)
   - Columns = time periods (D1, D7, D30 or Week 1, Week 2, etc.)
   - Values = retention % (0–100 or 0–1 scale) or absolute user counts

3. Validate structure
   - If single row or single column: stop and report: "Table structure not recognized. Expected: rows = cohorts, columns = time periods, values = retention % or user counts."
   - If non-numeric cell values (excluding headers): stop with same message

4. Detect value type
   - If values > 100 or the table clearly shows descending absolute counts (not percentages): treat as absolute counts; convert each value to % relative to the period-0 (first column) value for that cohort; note conversion in the output

5. Detect scale
   - If all values ≤ 1.0 (e.g., 0.45, 0.22): treat as 0–1 scale; multiply by 100 for display; note this assumption

### Step 2: Compute Curve Descriptors

1. For each cohort row, identify the retention value at key benchmark periods:
   - For daily products: D1, D7, D30 (or closest available periods)
   - For weekly/monthly products: W1, W4, W12 or M1, M3, M6

2. Compute period-over-period deltas for each cohort:
   - Drop = value[period N] − value[period N+1]
   - Identify the 2–3 largest drops across all cohorts

3. Check for curve flattening (asymptotic floor):
   - If last 2–3 periods show drops < 2 pp: note as "curve is flattening — long-term floor likely around X%"

4. Compute average retention across cohorts for each time period (if multiple cohorts)

**Edge Cases:**
- If table has only 2–3 time periods: perform analysis on available data; add flag: "Limited periods — trends may not be conclusive. Consider extending observation window."
- If some cells are blank: skip missing cells; add flag: "Missing values in periods [X] may affect trend reliability."
- If one cohort has dramatically different values (outlier): flag it explicitly; separate its analysis from the aggregate trend

### Step 3: Select Benchmark

1. Determine product type from user input, context clues, or column naming:
   - "D1, D7, D30" → likely mobile/consumer app
   - "Week 1, Week 4" or "M1, M3" → likely SaaS or B2B
   - If user stated product type explicitly: use that

2. Apply appropriate benchmark ranges:
   - **Mobile / Consumer app:** D1 ≥ 40% = good; D7 ≥ 20% = good; D30 ≥ 10% = good
   - **B2C SaaS:** M1 ≥ 60% = good; M3 ≥ 40% = good; M6 ≥ 30% = good
   - **B2B SaaS:** M1 ≥ 75% = good; M3 ≥ 65% = good; M6 ≥ 55% = good
   - **Marketplace / Consumer platform:** M1 ≥ 50% = good; M3 ≥ 30% = good

3. Compare curve to benchmark at a representative mid-period (e.g., D30 or M3)
   - State whether curve is above / at / below benchmark

### Step 4: Diagnose Curve Health

1. Assign overall health label based on combined criteria:
   - **Healthy:** Curve meets or exceeds benchmark at key periods AND flattens above a meaningful floor
   - **Needs Work:** Curve is 10–30% below benchmark at key periods OR shows no sign of flattening
   - **Critical:** Curve is >30% below benchmark at key periods OR drops to near-zero before expected floor

2. Write 1–2 sentence narrative explaining the label, referencing specific data points

### Step 5: Generate Hypotheses

1. Identify the dominant churn window (the period with the largest average drop across cohorts)

2. Generate exactly 3 hypotheses specific to that window:
   - Each hypothesis must be actionable and testable (not generic)
   - Link each hypothesis to a mechanism (e.g., onboarding gap, feature discovery failure, competitive alternative, habit loop not formed)

3. Order hypotheses from most likely (based on pattern) to exploratory

### Step 6: Compile and Output Report

1. Assemble the full report using the Output Format below
2. Ensure all sections are populated; do not leave any section empty
3. If prediction of future retention is requested without historical basis: add note: "Forecasting requires more historical data. The analysis above is based on observed trends only."

---

## Negative Cases

- **No data provided:** Stop with "Retention table required. Paste your cohort data as CSV, markdown, or plain numbers with headers."
- **Malformed table (single row/column, non-numeric):** Stop with "Table structure not recognized. Expected: rows = cohorts, columns = time periods, values = retention % or user counts."
- **Prediction request without data:** Decline forecast, explain requirement for historical data; continue with analysis of what was provided.

---

## Output Format

Structured markdown response:

```markdown
## Cohort Retention Diagnosis

**Product type:** [detected or stated]
**Cohorts analyzed:** [N]
**Periods covered:** [e.g., D1–D30 or W1–W12]
**Note:** [Any flags: scale conversion, missing values, limited periods — or omit if none]

---

### Curve Health: [Healthy / Needs Work / Critical]

[1–2 sentences summarizing overall pattern with specific data points]

---

### Key Drop-off Points

| Period | Avg Retention | Drop vs Previous | Severity |
|--------|---------------|------------------|----------|
| [e.g., D1→D7] | X% | -Y pp | High / Medium / Low |
| [e.g., D7→D30] | X% | -Y pp | High / Medium / Low |

---

### Benchmark Comparison

- **Reference:** [product type] — typical [key period] retention: X%–Y%
- **Your curve:** [above / at / below] benchmark at [key period]: Z%
- [1 sentence interpretation]

---

### Hypotheses for Primary Churn Window ([period])

1. **[Hypothesis 1 — most likely]:** [Specific, actionable explanation + mechanism]
2. **[Hypothesis 2]:** [Specific, actionable explanation + mechanism]
3. **[Hypothesis 3 — exploratory]:** [Specific, actionable explanation + mechanism]

---

### Recommended Next Steps

1. [Specific investigation or experiment — tied to Hypothesis 1]
2. [Data cut or segment analysis to run]
3. [Stakeholder conversation or metric to instrument]
```
