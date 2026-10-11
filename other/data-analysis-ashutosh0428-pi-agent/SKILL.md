---
name: data-analysis
description: Analyse a dataset like a data scientist — profile it, find the signal, explain it.
trigger: when the user uploads a CSV/TSV/Excel file or asks to analyse / explore data
---
## When to use
The user uploaded a data file (`.csv` / `.tsv` / `.xlsx`) or asks you to analyse,
explore, or do EDA on a dataset.

## How
1. `update_plan` with the steps (profile → interpret → recommend → optional deck).
2. Call **`analyze_data`** with the file `path` (and `target` if the user named a
   target column). Always run the tool — never guess at the data.
3. Read the report, then explain like a data scientist, in this order:
   - **What it is** — rows, columns, what each column represents.
   - **Quality** — missingness, likely outliers, dtype problems.
   - **Signal** — the strongest correlations / relationships to the target, and
     what they plausibly mean.
   - **Recommendations** — concrete next steps (cleaning, features, a model
     family worth trying).
4. If the user wants a presentation, pass the findings to `make_slides`.

## Avoid
- Inventing numbers — every figure must come from the `analyze_data` output.
- Pasting the raw report back; synthesise it into insight.
- Claiming causation from correlation.

## Done well
A short, structured read a stakeholder grasps in a minute: what the data says,
what's trustworthy, and what to do next — every claim grounded in the tool's
real numbers.
