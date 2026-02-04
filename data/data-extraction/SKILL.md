---
name: data-extraction
description: Use when extracting structured data from medical research PDFs, parsing study characteristics, patient demographics, outcomes, and results. Invoke for systematic review data collection from papers.
---

# Data Extraction Skill

This skill guides structured data extraction from research papers for systematic reviews.

## When to Use

Invoke this skill when the user:
- Asks to extract data from a PDF
- Needs study characteristics pulled
- Wants patient demographics collected
- Requests outcome data extraction
- Mentions "data extraction" or "data collection"

## Data Elements to Extract

### 1. Study Identification

| Field | Description | Example |
|-------|-------------|---------|
| study_id | FirstAuthorYear format | "Smith2023" |
| pmid | PubMed ID | "37654321" |
| doi | Digital Object Identifier | "10.1001/jamasurg.2023.1234" |
| title | Full article title | "..." |

### 2. Study Characteristics

| Field | Description | Values |
|-------|-------------|--------|
| year | Publication year | 2020 |
| country | Study location | "USA", "Japan" |
| study_design | Design type | "RCT", "Retrospective cohort" |
| multicenter | Single/multi | true/false |
| study_period | Enrollment dates | "2015-2020" |

### 3. Patient Demographics

| Field | Format | Notes |
|-------|--------|-------|
| sample_size | Integer | Total N |
| age_mean | Number | Mean age |
| age_sd | Number | Standard deviation |
| age_median | Number | If no mean |
| age_iqr | [Q1, Q3] | Interquartile range |
| male_percent | 0-100 | Percentage male |

### 4. Clinical Characteristics (Neurosurgery)

Common scales and measures:
- **GCS** (Glasgow Coma Scale): 3-15
- **GOS** (Glasgow Outcome Scale): 1-5
- **mRS** (modified Rankin Scale): 0-6
- **NIHSS** (NIH Stroke Scale): 0-42
- **Hunt-Hess**: I-V
- **Fisher Grade**: 1-4
- **WHO Grade**: I-IV (tumors)

### 5. Intervention Details

```yaml
intervention:
  name: "Decompressive craniectomy"
  type: "Surgical"
  technique: "Unilateral frontotemporoparietal"
  timing: "Within 48 hours"
  details: "Bone flap ≥12cm diameter"
```

### 6. Outcome Data

#### Binary Outcomes (events/total)

```yaml
outcomes:
  - name: "Mortality"
    type: "binary"
    timepoint: "30 days"
    intervention:
      events: 12
      total: 50
    control:
      events: 25
      total: 52
```

#### Continuous Outcomes (mean ± SD)

```yaml
outcomes:
  - name: "Length of stay"
    type: "continuous"
    timepoint: "discharge"
    intervention:
      mean: 14.5
      sd: 6.2
      n: 50
    control:
      mean: 18.3
      sd: 7.1
      n: 52
```

#### Effect Estimates

```yaml
effect_estimate:
  measure: "OR"  # OR, RR, HR, MD, SMD
  value: 0.65
  ci_lower: 0.42
  ci_upper: 0.98
  p_value: 0.038
```

## Extraction Principles

### DO:
1. Extract **only explicitly stated data**
2. Record the **exact numbers** from the paper
3. Note **units** (mg, mm, days, months)
4. Specify **timepoints** for each outcome
5. Flag **unclear or ambiguous** values with "?"
6. Document **page numbers** for key data

### DON'T:
1. Calculate or derive values (unless necessary)
2. Assume missing data
3. Interpret unclear statements
4. Mix timepoints within outcomes

## Quality Checks

After extraction, verify:
- [ ] Sample sizes sum correctly across groups
- [ ] Event counts ≤ total participants
- [ ] Percentages add to ~100%
- [ ] CIs contain the point estimate
- [ ] P-values align with CI (crossing 1 for OR/RR)

## Common Issues

### Converting Median/IQR to Mean/SD

When only median and IQR reported:
```
Mean ≈ Median (for symmetric distributions)
SD ≈ IQR / 1.35 (for normal distributions)
```

### Extracting from Figures

- Use WebPlotDigitizer for graph data
- Note "extracted from figure" in comments
- Estimate uncertainty

### Missing Control Group (Single-Arm)

For case series without controls:
```yaml
outcomes:
  - name: "Mortality"
    type: "binary"
    timepoint: "in-hospital"
    single_arm:
      events: 15
      total: 100
```

## Output Format

Use YAML format for structured extraction:

```yaml
study_id: "Smith2023"
pmid: "37654321"
doi: "10.1001/jamasurg.2023.1234"
year: 2023
country: "USA"
study_design: "Retrospective cohort"
sample_size: 150

patient_demographics:
  age_mean: 58.3
  age_sd: 12.4
  male_percent: 62

intervention:
  name: "Decompressive craniectomy"
  type: "Surgical"

outcomes:
  - name: "Mortality"
    type: "binary"
    timepoint: "30 days"
    intervention:
      events: 12
      total: 75
    control:
      events: 18
      total: 75

notes: "Single-center study. High crossover rate (15%)."
```

## Validation

After extraction, use the `validate_extraction` tool to check against schema:
```
mcp__neuroresearch__validate_extraction(data, schema_type="study")
```
