---
name: manuscript-writing
description: Use when writing systematic review manuscript sections following PRISMA 2020 guidelines. Covers abstract, introduction, methods, results, and discussion drafting for medical journals. Invoke for academic writing assistance.
---

# Manuscript Writing Skill

This skill guides PRISMA 2020-compliant systematic review manuscript writing.

## When to Use

Invoke this skill when the user:
- Asks to write a manuscript section
- Needs help with methods or results
- Wants to draft an abstract
- Mentions PRISMA 2020 guidelines
- Needs academic writing assistance

## PRISMA 2020 Structure

### Required Sections

| Section | PRISMA Items |
|---------|--------------|
| Title | #1 |
| Abstract | #2 |
| Introduction | #3-4 |
| Methods | #5-17 |
| Results | #18-23 |
| Discussion | #24-27 |
| Other | #28-32 (funding, registration, etc.) |

---

## Title

Format: "[Intervention] for [Population]: A Systematic Review and Meta-Analysis"

Example:
> "Decompressive Craniectomy for Malignant Middle Cerebral Artery Infarction: A Systematic Review and Meta-Analysis of Randomized Controlled Trials"

---

## Abstract (Structured)

### Format (250-300 words)

```markdown
**Background:** [1-2 sentences on clinical context and knowledge gap]

**Objective:** [Clear statement of review aim using PICO]

**Methods:** [Databases, dates, eligibility, outcomes, risk of bias tool, synthesis method]

**Results:** [Number of studies and participants, main findings with effect estimates and 95% CIs, heterogeneity, certainty of evidence]

**Conclusions:** [Clinical implications, future research needs]

**Registration:** [PROSPERO number]
```

### Example

> **Background:** Decompressive craniectomy (DC) may improve outcomes in malignant MCA infarction, but the balance of benefits and harms remains uncertain.
>
> **Objective:** To evaluate the effects of DC versus medical management on mortality and functional outcomes in patients with malignant MCA infarction.
>
> **Methods:** We searched PubMed, Embase, and Cochrane Library through December 2024. We included RCTs comparing DC to medical management in adults with malignant MCA infarction. Two reviewers independently assessed risk of bias using RoB 2 and extracted data. We pooled results using random-effects meta-analysis and assessed certainty using GRADE.
>
> **Results:** We included 7 RCTs (n=488 patients). DC reduced mortality at 12 months (OR 0.35, 95% CI 0.21-0.58; I²=23%; moderate certainty) but increased survival with severe disability (mRS 5: OR 2.45, 95% CI 1.15-5.23). The probability of favorable outcome (mRS 0-3) was similar between groups (OR 1.15, 95% CI 0.65-2.03; low certainty).
>
> **Conclusions:** DC reduces mortality in malignant MCA infarction but may increase survival with severe disability. Patient values and goals of care should guide treatment decisions.
>
> **Registration:** PROSPERO CRD42024123456

---

## Introduction

### Structure (400-600 words)

**Paragraph 1: Clinical Context**
- Disease burden and prevalence
- Current treatment landscape
- Clinical significance

**Paragraph 2: Knowledge Gap**
- Conflicting evidence
- Limitations of previous studies
- What is unknown

**Paragraph 3: Rationale and Objectives**
- Why this review is needed
- Clear statement of objectives (PICO)

### Language Tips

- Use present tense for established facts
- Use past tense for specific studies
- Avoid jargon; define abbreviations

---

## Methods

### Eligibility Criteria (#5-6)

```markdown
## Eligibility Criteria

### Population
Adults (≥18 years) with [condition]

### Intervention
[Intervention] defined as [definition]

### Comparator
[Comparator] including [types]

### Outcomes
**Primary:** [Primary outcome] at [timepoint]
**Secondary:** [List secondary outcomes]

### Study Designs
[RCTs, cohort studies, etc.]

### Exclusions
- [Exclusion 1]
- [Exclusion 2]
```

### Information Sources (#7-8)

```markdown
## Information Sources

We searched the following databases from inception to [date]:
- MEDLINE via PubMed
- Embase
- Cochrane Central Register of Controlled Trials

We also searched:
- ClinicalTrials.gov for ongoing trials
- Reference lists of included studies
- [Grey literature sources]
```

### Search Strategy (#8)

```markdown
## Search Strategy

The complete search strategy was developed with a medical librarian (Supplementary Appendix 1). The PubMed search combined terms for:
1. Population: [MeSH terms and keywords]
2. Intervention: [MeSH terms and keywords]
3. Study design filter: Cochrane Highly Sensitive Search Strategy
```

### Selection and Data Collection (#9-12)

```markdown
## Study Selection

Two reviewers (XX, YY) independently screened titles and abstracts using Covidence. Full texts were assessed against eligibility criteria. Disagreements were resolved by discussion or a third reviewer (ZZ). We contacted authors for clarification when needed.

## Data Extraction

We extracted data using a piloted form including:
- Study characteristics (design, country, setting)
- Participant characteristics (age, sex, diagnosis criteria)
- Intervention details (technique, timing)
- Outcomes (events, means, effect estimates)

For missing data, we contacted authors and used methods described in the Cochrane Handbook.
```

### Risk of Bias (#13-14)

```markdown
## Risk of Bias Assessment

Two reviewers independently assessed risk of bias using:
- RoB 2 for randomized trials
- Newcastle-Ottawa Scale for observational studies

We assessed bias at the study level for each outcome. Disagreements were resolved by discussion.
```

### Synthesis Methods (#15-17)

```markdown
## Statistical Analysis

We performed meta-analysis using the `meta` package in R (version 4.3). For binary outcomes, we calculated odds ratios (OR) with 95% confidence intervals using the Mantel-Haenszel method with DerSimonian-Laird random-effects.

We assessed heterogeneity using I² statistic:
- <25%: Low
- 25-50%: Moderate
- 50-75%: Substantial
- >75%: Considerable

We assessed publication bias using funnel plots and Egger's test (if ≥10 studies).

We assessed certainty of evidence using GRADE, considering risk of bias, inconsistency, indirectness, imprecision, and publication bias.
```

---

## Results

### Study Selection (#18)

```markdown
## Study Selection

Our search identified 1,245 records. After removing 312 duplicates, we screened 933 titles and abstracts, excluding 856. We assessed 77 full texts, excluding 62 (reasons in Supplementary Table 1). We included 15 studies in the review and 12 in meta-analysis (Figure 1: PRISMA Flow Diagram).
```

### Study Characteristics (#19)

```markdown
## Study Characteristics

The 15 included studies (n=2,345 patients) were published between 2007 and 2023 (Table 1). Eight studies were RCTs and seven were observational cohorts. Studies were conducted in Europe (n=8), Asia (n=5), and North America (n=2). Mean patient age ranged from 52 to 68 years. Follow-up ranged from 6 to 24 months.
```

### Synthesis Results (#21)

```markdown
## Mortality

Twelve studies (n=1,890 patients) reported mortality. DC was associated with reduced mortality compared to medical management (OR 0.35, 95% CI 0.21-0.58; I²=23%, τ²=0.12; Figure 2). The prediction interval ranged from 0.15 to 0.82.

### Subgroup Analysis

The effect did not differ significantly by:
- Age (<60 vs ≥60 years): interaction p=0.34
- Timing (<24h vs ≥24h): interaction p=0.51
- Study design (RCT vs cohort): interaction p=0.12
```

### Reporting Numbers

**Always include:**
- Number of studies and participants
- Effect estimate with 95% CI
- P-value or statement of significance
- I² and interpretation
- Certainty of evidence (GRADE)

Example:
> "DC reduced mortality (OR 0.35, 95% CI 0.21-0.58; p<0.001; 12 studies, n=1,890; I²=23%; moderate certainty)."

---

## Discussion

### Structure (800-1200 words)

**Paragraph 1: Summary of Main Findings**
- Restate key results without repeating statistics
- Relate to objectives

**Paragraph 2: Comparison with Previous Evidence**
- How do findings compare to prior reviews?
- What is new or different?

**Paragraph 3: Strengths**
- Comprehensive search
- Rigorous methodology
- Large sample size

**Paragraph 4: Limitations**
- Study-level limitations
- Review-level limitations
- Certainty of evidence limitations

**Paragraph 5: Clinical Implications**
- What do findings mean for practice?
- GRADE-informed language

**Paragraph 6: Research Implications**
- What questions remain?
- What study designs are needed?

### GRADE Language for Conclusions

| Certainty | Language |
|-----------|----------|
| High | "X reduces Y" |
| Moderate | "X probably reduces Y" |
| Low | "X may reduce Y" |
| Very Low | "We are uncertain whether X reduces Y" |

---

## Tables

### Table 1: Study Characteristics

| Study | Country | Design | N | Age | Male (%) | Intervention | Follow-up |
|-------|---------|--------|---|-----|----------|--------------|-----------|
| Smith 2020 | USA | RCT | 120 | 58±12 | 55 | DC | 12 mo |

### Table 2: Risk of Bias Summary

| Study | D1 | D2 | D3 | D4 | D5 | Overall |
|-------|----|----|----|----|-----|---------|
| Smith 2020 | + | ? | + | + | + | ? |

(+ = Low risk, ? = Some concerns, - = High risk)

### Table 3: GRADE Summary of Findings

| Outcome | Studies | Participants | Effect (95% CI) | Certainty | Interpretation |
|---------|---------|--------------|-----------------|-----------|----------------|
| Mortality | 12 | 1,890 | OR 0.35 (0.21-0.58) | ⊕⊕⊕◯ Moderate | DC probably reduces mortality |
