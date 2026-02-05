---
name: risk-of-bias
description: Use when assessing risk of bias or study quality. Covers RoB 2 for RCTs, Newcastle-Ottawa Scale for cohorts, ROBINS-I for non-randomized interventions, and QUADAS-2 for diagnostic studies. Invoke for quality assessment.
---

# Risk of Bias Assessment Skill

This skill guides risk of bias and study quality assessment for systematic reviews.

## When to Use

Invoke this skill when the user:
- Asks to assess risk of bias
- Needs quality assessment of studies
- Mentions RoB 2, NOS, ROBINS-I, or QUADAS-2
- Wants to evaluate study quality
- Needs a risk of bias table or plot

## Tool Selection

| Study Design | Assessment Tool |
|--------------|-----------------|
| Randomized Controlled Trial | **RoB 2** (Cochrane) |
| Cohort study | **Newcastle-Ottawa Scale** |
| Case-control study | **Newcastle-Ottawa Scale** |
| Non-randomized intervention | **ROBINS-I** |
| Diagnostic accuracy study | **QUADAS-2** |

---

## RoB 2 (Cochrane Risk of Bias 2)

For **randomized controlled trials**.

### Domains

| Domain | Key Questions |
|--------|---------------|
| **D1: Randomization** | Was allocation sequence random? Was it concealed? Were there baseline imbalances? |
| **D2: Deviations from intervention** | Were participants/personnel aware of assignment? Were there deviations? Was analysis appropriate? |
| **D3: Missing outcome data** | Was outcome data complete? Could missingness depend on outcome? |
| **D4: Outcome measurement** | Was the method appropriate? Could assessment be influenced by knowledge of intervention? |
| **D5: Selection of reported result** | Was the result pre-specified? Were multiple analyses performed? |

### Judgments

- **Low risk**: No concerns in this domain
- **Some concerns**: Some concern but not definitely high risk
- **High risk**: Definitely high risk in this domain

### Overall Judgment

```
If ALL domains are "Low risk" → Overall: Low risk
If ANY domain is "High risk" → Overall: High risk
Otherwise → Overall: Some concerns
```

### R Code for Visualization

```r
library(robvis)

# Prepare data
rob_data <- data.frame(
  Study = c("Smith 2020", "Jones 2021", "Brown 2022"),
  D1 = c("Low", "Some concerns", "Low"),
  D2 = c("Low", "Low", "High"),
  D3 = c("Low", "Low", "Low"),
  D4 = c("Some concerns", "Low", "Low"),
  D5 = c("Low", "Low", "Low"),
  Overall = c("Some concerns", "Some concerns", "High")
)

# Traffic light plot
png("rob_traffic_light.png", width=1000, height=600, res=150)
rob_traffic_light(rob_data, tool = "ROB2")
dev.off()

# Summary plot
png("rob_summary.png", width=800, height=400, res=150)
rob_summary(rob_data, tool = "ROB2")
dev.off()
```

---

## Newcastle-Ottawa Scale (NOS)

For **observational studies** (cohort and case-control).

### Cohort Studies (max 9 stars)

**Selection (max 4 stars)**
| Item | Criteria | Stars |
|------|----------|-------|
| Representativeness of exposed | Truly representative or somewhat representative | 1 |
| Selection of non-exposed | Same community as exposed | 1 |
| Ascertainment of exposure | Secure record or structured interview | 1 |
| Outcome not present at start | Yes | 1 |

**Comparability (max 2 stars)**
| Item | Criteria | Stars |
|------|----------|-------|
| Controls for confounders | For most important factor | 1 |
| | For additional factor | 1 |

**Outcome (max 3 stars)**
| Item | Criteria | Stars |
|------|----------|-------|
| Assessment of outcome | Independent blind or record linkage | 1 |
| Adequate follow-up length | Sufficient for outcome | 1 |
| Adequacy of follow-up | ≥80% complete or dropout analysis | 1 |

### Quality Categories

```
7-9 stars: High quality
4-6 stars: Moderate quality
0-3 stars: Low quality
```

---

## ROBINS-I

For **non-randomized studies of interventions**.

### Domains

| Domain | Focus |
|--------|-------|
| **Confounding** | Baseline confounding |
| **Selection** | Selection into the study |
| **Classification** | Classification of interventions |
| **Deviations** | Deviations from intended interventions |
| **Missing data** | Missing outcome data |
| **Measurement** | Measurement of outcomes |
| **Reporting** | Selection of reported result |

### Judgments

- **Low risk**: Comparable to well-performed RCT
- **Moderate risk**: Sound for non-randomized study
- **Serious risk**: Important problems
- **Critical risk**: Study too problematic to provide evidence
- **No information**: Insufficient information

### Overall Judgment

```
If ALL domains are "Low" → Overall: Low risk
If highest is "Moderate" → Overall: Moderate risk
If ANY domain is "Serious" → Overall: Serious risk
If ANY domain is "Critical" → Overall: Critical risk
```

---

## QUADAS-2

For **diagnostic accuracy studies**.

### Domains

| Domain | Risk of Bias | Applicability |
|--------|--------------|---------------|
| **Patient Selection** | Was a consecutive/random sample used? Was case-control design avoided? Did the study avoid inappropriate exclusions? | Do included patients match review question? |
| **Index Test** | Was the index test interpreted without knowledge of reference standard? Was a threshold pre-specified? | Is the test applicable to the review question? |
| **Reference Standard** | Is the reference standard likely to correctly classify the condition? Was it interpreted without knowledge of index test? | Is the reference standard applicable? |
| **Flow and Timing** | Was there appropriate interval between tests? Did all patients receive the reference standard? Did all patients receive the same reference standard? Were all patients included in the analysis? | - |

---

## Output Format

### Risk of Bias Table

```yaml
risk_of_bias:
  - study_id: "Smith2023"
    tool: "RoB2"
    domains:
      D1_randomization: "Low"
      D2_deviations: "Some concerns"
      D3_missing_data: "Low"
      D4_measurement: "Low"
      D5_reporting: "Low"
    overall: "Some concerns"
    support: "Blinding of outcome assessors unclear"
```

### Summary Reporting

```markdown
## Risk of Bias Assessment

We used the Cochrane RoB 2 tool for randomized trials.

**Summary:**
- Low risk: 5 studies (45%)
- Some concerns: 4 studies (36%)
- High risk: 2 studies (18%)

**Key concerns:**
- Outcome assessment blinding unclear in 4 studies
- Per-protocol analysis without addressing deviations in 2 studies
```

---

## Best Practices

1. **Two reviewers**: Independent assessment
2. **Pilot testing**: Calibrate on 2-3 studies
3. **Support quotes**: Document rationale with paper quotes
4. **Domain-level**: Report each domain, not just overall
5. **Sensitivity analysis**: Exclude high risk studies

## Integration with Meta-Analysis

```r
# Subgroup by risk of bias
forest(ma, subgroup = rob_overall,
       subgroup.levels = c("Low", "Some concerns", "High"))

# Sensitivity: low risk only
ma_low <- update(ma, subset = rob_overall == "Low")
summary(ma_low)
```
