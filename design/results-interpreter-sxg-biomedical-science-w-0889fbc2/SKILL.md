---
name: results-interpreter
description: Analyze CSV data files and interpret figures to generate the Results section. Fifth step of biomedical-science-writer workflow. Requires scope.md, data/ folder with CSVs, and figures/ folder with images.
---

# Results Interpreter

Analyzes data files and interprets figures to generate structured notes and draft the Results section with proper statistical reporting.

## Critical Principle: No Silent Assumptions

**NEVER make assumptions about data without user confirmation.**

When encountering ambiguity, STOP and ask the user before proceeding. It is better to ask too many questions than to misinterpret data. The user's research depends on accurate interpretation.

### When to Pause and Ask

**ALWAYS ask the user when you encounter:**

1. **Unclear column meanings**
   - Column names are abbreviated or cryptic (e.g., "grp1", "val_a", "x1")
   - Units are not specified (is this mm, cm, seconds, days?)
   - Multiple possible interpretations exist

2. **Ambiguous group definitions**
   - What does "Group A" vs "Group B" represent?
   - Which group is the control/reference?
   - Are these treatment arms, time points, or subpopulations?

3. **Uncertain statistical context**
   - P-values without knowing which test was used
   - Effect sizes without knowing the direction expected
   - Multiple comparison situations unclear

4. **Data-scope mismatch**
   - Data doesn't match what scope.md described
   - Fewer/more variables than expected
   - Sample sizes don't align with expectations

5. **Figure interpretation uncertainty**
   - Axes labels are unclear or missing
   - Color coding isn't explained
   - Statistical annotations are ambiguous (*, **, ***)

6. **Missing context**
   - Primary vs secondary outcomes unclear
   - Exclusion criteria not evident from data
   - Time points or visit structure unknown

### How to Ask Clarifying Questions

Format questions clearly with context:

```
I need clarification before interpreting the data:

**File**: results.csv
**Issue**: Column "grp" contains values 0 and 1, but I'm unsure what these represent.

**Question**: What do the group values mean?
- 0 = [?]
- 1 = [?]
- Which is the reference/control group?

**Why this matters**: This determines how I report the direction of effects (e.g., "Group A was higher than Group B" vs the reverse).
```

### Log All Assumptions

If the user confirms an interpretation, document it in `notes/data-analysis.md`:

```markdown
## Clarifications Received

| Question | User Response | Date |
|----------|---------------|------|
| What does grp=0 mean? | Control group (no treatment) | [date] |
| Units for "time" column? | Days since enrollment | [date] |
```

## Prerequisites

- `scope.md` must exist
- `notes/code-analysis.md` should exist (provides context on what analyses were run)
- `notes/irb-summary.md` may exist (provides expected sample size, endpoints for validation)
- `notes/irb-scope-comparison.md` may exist (explains any scope differences)
- `data/` folder with CSV/Excel files
- `figures/` folder with PNG/JPG images

## Workflow

```
[Read scope.md, code-analysis.md, and notes/irb-summary.md]
     │
     ▼
[Inventory Data Files] ─── List all CSVs and columns
     │
     ▼
[CHECKPOINT: Ask Clarifying Questions] ─── STOP if any ambiguity
     │                                       └── Document responses
     ▼
[Validate Against IRB] ─── Check sample size, endpoints match expectations
     │
     ▼
[Analyze Data Files] ─── Parse CSVs, extract statistics
     │
     ▼
[Interpret Figures] ─── View and describe each figure
     │
     ▼
[CHECKPOINT: Verify Interpretations] ─── Confirm with user
     │
     ▼
[Cross-Reference] ─── Match data to figures to findings
     │
     ▼
[Generate notes/data-analysis.md]
     │
     ▼
[BIOSTATISTICIAN REVIEW] ─── Validate statistical reporting
     │                        └── skills/biostatistician/SKILL.md
     ▼
[Draft Results] ─── drafts/results.md (with statistical sign-off)
```

## Step 1: Read Context

From `scope.md`:
- Key findings (what results are expected)
- Research question (what to emphasize)

From `notes/code-analysis.md`:
- Statistical tests used (how to interpret p-values)
- Variables analyzed (what columns to look for)

## Step 2: Analyze Data Files

### 2a. Inventory Data Files

```bash
ls -la data/*.csv data/*.xlsx 2>/dev/null
```

### 2b. Initial Data Scan

For each data file, perform an initial scan WITHOUT interpretation:

```python
import pandas as pd
df = pd.read_csv('data/results.csv')
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Sample values per column:")
for col in df.columns:
    print(f"  {col}: {df[col].unique()[:5]}")
```

---

## Step 3: CHECKPOINT — Clarifying Questions

**STOP HERE if there is ANY ambiguity.**

Before interpreting any data, present findings to the user and ask clarifying questions.

### Required Clarification Template

Present this to the user:

```markdown
## Data Clarification Needed

I've scanned your data files. Before interpreting, I need to confirm my understanding.

### Files Found

| File | Rows | Columns |
|------|------|---------|
| results.csv | 156 | 12 |
| demographics.csv | 156 | 8 |

### Questions About: results.csv

**Columns I understand:**
- `patient_id` — unique identifier
- `age` — patient age (years, I assume?)

**Columns I need clarification on:**

1. **Column: `grp`** (values: 0, 1)
   - What do these values represent?
   - Which is the control/reference group?

2. **Column: `outcome_val`**
   - What does this measure?
   - What are the units?
   - Is higher better or worse?

3. **Column: `p_val`**
   - Which statistical test produced these p-values?
   - Were these corrected for multiple comparisons?

### Questions About: Figures

1. **figure1.png** — appears to be a box plot
   - What groups are being compared?
   - What's on the y-axis?

### Questions About: Overall Analysis

1. Which finding is the PRIMARY outcome for this paper?
2. Are there any data points I should exclude (e.g., outliers, failed QC)?
3. Is there anything unusual about this dataset I should know?

**Please answer these questions before I proceed with interpretation.**
```

### Wait for User Response

Do NOT proceed until the user has answered ALL clarifying questions.

If the user says "just figure it out" or similar, respond:

> "I want to make sure I interpret your data correctly. Making assumptions could lead to errors in the manuscript that might be difficult to catch later. Could you please clarify [specific question]?"

### Document All Clarifications

After receiving answers, record them:

```markdown
## Clarifications Log

**File**: results.csv
**Date**: [timestamp]

| Item | Question | User Response |
|------|----------|---------------|
| grp column | What do 0 and 1 mean? | 0 = control, 1 = treatment |
| grp column | Which is reference? | 0 (control) is reference |
| outcome_val | What does it measure? | Tumor volume in mm³ |
| outcome_val | Higher = better/worse? | Lower is better (tumor shrinkage) |
| p_val | Which test? | Mann-Whitney U, not corrected |
| figure1.png | What's compared? | Treatment vs control tumor volume |
| Primary outcome | Which is primary? | Tumor volume change at week 8 |
```

---

## Step 3b: Validate Against IRB (If IRB Exists)

**Skip this step if `notes/irb-summary.md` does not exist.**

After clarifying data questions, validate that the actual results align with IRB expectations.

### IRB Validation Checklist

```markdown
## IRB Results Validation

**IRB Document**: [from irb-summary.md]
**Scope Comparison**: [from irb-scope-comparison.md]

### Sample Size Check

| Aspect | IRB Expected | Actual Data | Status |
|--------|--------------|-------------|--------|
| Total N | [from IRB] | [from data] | ✓/✗ |
| Control group | [from IRB] | [from data] | ✓/✗ |
| Treatment group | [from IRB] | [from data] | ✓/✗ |

**If actual < expected**: Reference irb-scope-comparison.md for explanation
**If actual > expected**: Unusual - ask user for clarification

### Endpoints Check

| IRB Endpoint | Present in Data? | Column Name | Notes |
|--------------|------------------|-------------|-------|
| [primary endpoint] | ✓/✗ | [column] | |
| [secondary endpoint 1] | ✓/✗ | [column] | |
| [secondary endpoint 2] | ✓/✗ | [column] | |

**Missing endpoints**: Check irb-scope-comparison.md - may be intentionally out of scope
**Extra endpoints**: Exploratory analyses - note as such in Results
```

### If Significant Discrepancies

If you find discrepancies NOT explained by `notes/irb-scope-comparison.md`:

```
I found a discrepancy between expected and actual data:

**IRB Expected Sample Size**: N = 500
**Actual Data**: N = 312

This wasn't documented in the scope comparison.
Could you explain this difference? (e.g., enrollment ongoing, exclusions, data subset)
```

Document all validations in `notes/data-analysis.md`.

---

## Step 4: Analyze Data Files (Post-Clarification)

**Only proceed after Steps 3 and 3b are complete.**

### 4a. Parse Each Data File

For each CSV:

```python
import pandas as pd
df = pd.read_csv('data/results.csv')
print(df.shape)
print(df.columns.tolist())
print(df.describe())
print(df.head())
```

### 4b. Identify Result Types

Scan columns for statistical output patterns:

| Column Pattern | Result Type | How to Report |
|----------------|-------------|---------------|
| `mean`, `sd`, `se` | Descriptive | mean ± SD |
| `p`, `pval`, `p_value` | Significance | p = 0.XXX |
| `ci_lower`, `ci_upper`, `ci_95_*` | Confidence interval | (95% CI: X–Y) |
| `auc`, `auroc` | Discrimination | AUC = 0.XX |
| `accuracy`, `precision`, `recall`, `f1` | Classification | metric = 0.XX |
| `coef`, `beta`, `or`, `hr` | Effect size | OR = X.X, β = X.X |
| `n`, `count` | Sample size | (n = X) |
| `r`, `rho`, `correlation` | Correlation | r = 0.XX |
| `t`, `t_stat` | T-statistic | t = X.XX |
| `chi2`, `chi_square` | Chi-square | χ² = X.XX |

### 4c. Extract Key Statistics

For each data file, extract:

**Demographics/Baseline (if present):**
- Sample sizes per group
- Age, sex distributions
- Key baseline characteristics

**Primary Outcomes:**
- Main comparison statistics
- Effect sizes
- P-values and CIs

**Secondary Outcomes:**
- Supporting statistics
- Subgroup analyses

## Step 5: Interpret Figures

### 5a. View Each Figure

```bash
ls figures/*.png figures/*.jpg figures/*.svg
```

For each figure, examine the image and identify:

### 5b. Figure Type Recognition

| Figure Type | Visual Cues | What to Report |
|-------------|-------------|----------------|
| Box plot | Boxes with whiskers | Medians, IQRs, group differences |
| Violin plot | Symmetric distributions | Distribution shape, medians |
| Bar chart | Rectangular bars | Proportions, counts |
| Scatter plot | Points in 2D | Correlation, trend, outliers |
| ROC curve | Curved line with diagonal | AUC, sensitivity/specificity |
| Kaplan-Meier | Step function | Survival rates, median survival |
| Heatmap | Color grid | Correlation patterns, clusters |
| Forest plot | Points with CIs | Effect sizes across subgroups |
| Confusion matrix | 2x2 or NxN grid | TP, FP, TN, FN rates |

### 5c. Match Figures to Data

Cross-reference figures with data files:
- Which CSV produced which figure?
- Do the statistics match?
- Any discrepancies to flag?

---

## Step 6: CHECKPOINT — Verify Interpretations

**Before finalizing, present your interpretation to the user for verification.**

### Interpretation Summary for User Review

```markdown
## Please Verify My Interpretation

Before I write the Results section, please confirm these interpretations are correct:

### Primary Finding

I interpret the primary finding as:
> "[Treatment group] showed [direction] [outcome] compared to [control]
> ([statistic] vs [statistic], p = [value])"

**Is this correct?** [Yes / No / Needs adjustment]

### Secondary Findings

1. [Secondary finding interpretation]
2. [Secondary finding interpretation]

**Are these correct?** [Yes / No / Needs adjustment]

### Figure Interpretations

| Figure | My Interpretation | Correct? |
|--------|-------------------|----------|
| Figure 1 | Shows [description] | [ ] |
| Figure 2 | Shows [description] | [ ] |

### Sample Sizes

- Total analyzed: [n]
- Group A: [n]
- Group B: [n]
- Excluded: [n]

**Do these match your expectations?** [Yes / No]

### Anything I Missed?

Is there anything important about these results that I haven't captured?
```

### If User Identifies Errors

If the user corrects any interpretation:
1. Thank them for the correction
2. Update the clarifications log
3. Re-analyze the affected data
4. Present revised interpretation for confirmation

---

## Step 7: Generate Data Analysis Notes

Create `notes/data-analysis.md`:

```markdown
# Data Analysis Notes

**Analyzed**: [timestamp]

## Data Files Processed

| File | Rows | Columns | Contents |
|------|------|---------|----------|
| results.csv | 156 | 12 | Main statistical results |
| demographics.csv | 156 | 8 | Patient characteristics |

## Study Population

- **Total enrolled**: [n]
- **Excluded**: [n] ([reasons])
- **Final cohort**: [n]

### Demographics

| Characteristic | Overall (n=X) | Group A (n=X) | Group B (n=X) | p-value |
|----------------|---------------|---------------|---------------|---------|
| Age, mean ± SD | XX ± XX | XX ± XX | XX ± XX | X.XXX |
| Male, n (%) | XX (XX%) | XX (XX%) | XX (XX%) | X.XXX |

## Primary Outcome

**Finding**: [description]

| Metric | Group A | Group B | Difference | p-value |
|--------|---------|---------|------------|---------|
| [outcome] | XX ± XX | XX ± XX | XX (95% CI: XX–XX) | X.XXX |

**Interpretation**: [what this means]

## Secondary Outcomes

### [Outcome 2]
[Statistics and interpretation]

### [Outcome 3]
[Statistics and interpretation]

## Figures

### Figure 1: [Title]
- **File**: figures/figure1.png
- **Type**: [box plot, ROC curve, etc.]
- **Shows**: [description]
- **Key observation**: [main takeaway]

### Figure 2: [Title]
- **File**: figures/figure2.png
- **Type**: [type]
- **Shows**: [description]
- **Key observation**: [takeaway]

## Statistical Summary

| Analysis | Test | Statistic | p-value | Interpretation |
|----------|------|-----------|---------|----------------|
| Primary | t-test | t = X.XX | 0.XXX | Significant/NS |
| Secondary | Mann-Whitney | U = XXX | 0.XXX | Significant/NS |

## Consistency Check

- [x] Demographics match reported sample size
- [x] Statistics align with scope.md key findings
- [x] Figures match data file values
- [ ] [Any discrepancies noted]

---

## Clarifications Log

| Date | Item | Question | User Response |
|------|------|----------|---------------|
| [date] | grp column | What do 0 and 1 mean? | 0 = control, 1 = treatment |
| [date] | outcome_val | Units? | mm³ |
| [date] | Primary outcome | Which is primary? | Tumor volume at week 8 |

---

## Assumptions Made

**None** — All interpretations were confirmed with user before proceeding.

(If any assumptions were made with user's consent, document them here with justification)
```

## Step 8: Biostatistician Review

**Before drafting Results, invoke the biostatistician agent for statistical review.**

Read `skills/biostatistician/SKILL.md` and execute Phase 3 (Results Section Review):

1. **Verify statistical reporting** — Check all statistics are formatted correctly
2. **Validate p-values** — Ensure proper formatting (p = 0.043, not p = .043)
3. **Check effect sizes** — Confirm effect sizes reported with CIs
4. **Cross-check with Methods** — Verify Results matches Methods description
5. **Flag common errors** — Identify interpretation issues

### Biostatistician Results Checkpoint

```markdown
## Statistical Reporting Review

| Statistic | Format OK? | Value Plausible? | CI Included? |
|-----------|------------|------------------|--------------|
| Primary outcome | ✓/✗ | ✓/✗ | ✓/✗ |
| Secondary outcomes | ✓/✗ | ✓/✗ | ✓/✗ |
| P-values | ✓/✗ | N/A | N/A |

**Issues Found**:
- [ ] None
- [ ] [List any issues]

**Statistical Sign-Off**: [ ] Approved for Results drafting
```

**Do NOT proceed to Results draft until biostatistician approves.**

If issues identified:
1. Correct statistical formatting
2. Add missing effect sizes or CIs
3. Flag interpretation concerns for user

---

## Step 9: Draft Results Section

**Only proceed after user has verified interpretations in Step 6 AND biostatistician sign-off in Step 8.**

Create `drafts/results.md`:

```markdown
# Results

## Study Population

[First paragraph ALWAYS describes the cohort]

A total of [n] patients were included in the analysis. [Exclusions if any]. The final cohort consisted of [n] patients (mean age XX ± XX years, XX% male). Baseline characteristics are summarized in Table 1.

## Primary Outcome

[Main finding with full statistics]

[Outcome] was significantly [higher/lower] in [Group A] compared to [Group B] (XX ± XX vs XX ± XX, p = X.XXX; Figure 1). The mean difference was XX (95% CI: XX–XX).

## Secondary Outcomes

### [Outcome 2]

[Description with statistics]

### [Outcome 3]

[Description with statistics]

## Model Performance (if applicable)

The [model type] achieved an AUC of X.XX (95% CI: X.XX–X.XX) for [classification task] (Figure X). At the optimal threshold, sensitivity was XX% and specificity was XX%.

## Subgroup Analyses (if applicable)

[Subgroup findings]

---

## Figure Legends

**Figure 1.** [Title]. [Description of what is shown]. [Statistical annotation explanation if needed]. Abbreviations: [list].

**Figure 2.** [Title]. [Description].

## Tables

**Table 1.** Baseline characteristics of the study population.

| Characteristic | Overall (n=X) | Group A (n=X) | Group B (n=X) | p-value |
|----------------|---------------|---------------|---------------|---------|
| Age, years | | | | |
| Male sex, n (%) | | | | |

---

## Results Checklist

- [ ] Study population described first
- [ ] Primary outcome reported with full statistics
- [ ] All p-values formatted correctly (p = 0.XXX or p < 0.001)
- [ ] Confidence intervals included for key findings
- [ ] All figures referenced in text
- [ ] All tables referenced in text
- [ ] No interpretation (saved for Discussion)
```

## Statistical Reporting Guidelines

### P-values
- p = 0.043 (not p = .043)
- p < 0.001 (not p = 0.000)
- p = 0.12 (report exact, even if NS)

### Confidence Intervals
- 95% CI: 1.23–4.56 (en-dash, not hyphen)
- Include for all key effect sizes

### Descriptive Statistics
- Normal: mean ± SD
- Non-normal: median (IQR) or median (Q1–Q3)
- Categorical: n (%)

### Decimal Places
- Percentages: 1 decimal (62.5%)
- P-values: 3 decimals or < 0.001
- Correlations: 2 decimals (r = 0.45)
- AUC: 2 decimals (0.87)

## Output

Save to:
- `notes/data-analysis.md` - Detailed analysis (includes clarifications log)
- `drafts/results.md` - Results section draft (with biostatistician approval)

Return to parent skill with summary:
- Data files analyzed: [n]
- Figures interpreted: [n]
- Primary finding confirmed: [yes/no]
- Biostatistician status: [approved / revisions needed]
- Statistical issues: [list if any]
- Results word count: [n]
