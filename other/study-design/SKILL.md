---
name: study-design
description: >
  Design a research study. Use when the user says "study design", "design my research",
  "what research method should I use", "how do I test this hypothesis", "research plan",
  "methodology section", "experimental design", "survey design", "qualitative study design",
  "how to structure my study", "sample size", "data collection plan", or needs to
  plan how to test a research question or hypothesis - even if they don't explicitly say "study design".
---

## Overview

Based on **Research Design** (Creswell & Creswell, 6th ed.) and **Research Methods in Education** (Cohen, Manion & Morrison, 8th ed.). A study design is the architectural plan for a research project: it specifies how data will be collected, from whom, by what method, and how conclusions will be drawn. Creswell's rule: the research question determines the method. Do not choose a method first and then fit the question to it.

The test: given only this study design document, could a different researcher conduct the same study and expect to produce comparable results?

## Workflow

### Step 1: Choose the research paradigm

Select based on what the research question is asking:

| Question type | Paradigm | Example |
|--------------|----------|---------|
| "How much / how many / does X cause Y?" | Quantitative | "Does intervention X reduce anxiety scores?" |
| "How / why / what is the experience of?" | Qualitative | "How do nurses experience burnout?" |
| "What is the scope AND the depth of?" | Mixed methods | "How prevalent is X, and why does it occur?" |

**Quantitative**: produces numbers, statistical significance, generalizable findings
**Qualitative**: produces meaning, interpretation, transferable insights
**Mixed**: both, in sequence or concurrently

### Step 2: Select the research design

**Quantitative designs:**
- **RCT (randomized controlled trial)**: strongest causal inference, participants randomly assigned to conditions
- **Quasi-experimental**: manipulation without randomization, useful when randomization is impractical
- **Survey/correlational**: measures relationships without manipulation
- **Longitudinal**: same participants measured over time
- **Cross-sectional**: one-time measurement across groups

**Qualitative designs:**
- **Phenomenology**: lived experience of a phenomenon
- **Grounded theory**: generate theory from data (no pre-existing theory)
- **Case study**: deep examination of a bounded case
- **Ethnography**: cultural practices through immersion
- **Narrative inquiry**: stories as primary data

**Choose based on:**
1. Can you manipulate the IV? → experimental / quasi-experimental
2. Are you exploring or confirming? → qualitative vs. quantitative
3. Do you need causal claims or descriptive claims?

### Step 3: Define the sample

```
Population: [full group you want findings to apply to]
Sampling strategy: [how you will select participants]
  Quantitative options: random sampling, stratified random, cluster
  Qualitative options: purposive, snowball, maximum variation, theoretical

Inclusion criteria: [who qualifies to participate]
Exclusion criteria: [who is excluded and why]

Sample size:
  Quantitative: calculated via power analysis
    Effect size (Cohen's d or f): [estimated from prior literature]
    Power (1-β): 0.80 (standard) or 0.90 (preferred)
    Alpha (α): 0.05
    Required N per group: [result from power calculation]
    Planned N: [required N + 15-20% buffer for attrition]

  Qualitative: determined by saturation
    Starting N: [e.g. 8-12 for phenomenology, 20-30 for grounded theory]
    Saturation criterion: [stop when 3 consecutive interviews add no new themes]

Recruitment: [how will you find participants?]
Incentive: [compensation, if any]
```

### Step 4: Document the procedure

Write the study procedure step-by-step, as a protocol:

```
Timeline: [total duration of study - e.g. 12 weeks]

Pre-study:
  1. [IRB/ethics approval - required before data collection]
  2. [Participant recruitment and screening]
  3. [Informed consent process]
  4. [Baseline measures collected]

Intervention/treatment (if applicable):
  - Group A (experimental): [exact description of what participants receive]
  - Group B (control): [exact description - active control or waitlist?]
  - Duration: [N sessions / N weeks]
  - Fidelity check: [how you verify the intervention was delivered as planned]

Data collection:
  - Time points: [T1 = baseline, T2 = post-intervention, T3 = 3-month follow-up]
  - Method: [survey / interview / observation / physiological measure / etc.]
  - Instrument: [name of validated scale or instrument]
  - Administration: [online / in-person / phone / researcher-administered]
  - Duration per session: [estimated time burden on participant]
```

### Step 5: Specify measures and instruments

For each variable being measured:

```
Variable: [DV or other key variable]
Instrument: [name, author, year]
Validity evidence: [what populations has this been validated with?]
Reliability: [Cronbach's α or test-retest r - cite source]
Scale: [e.g. 7-point Likert, 0-100 continuous, binary]
Scoring: [how to compute the score from items]
Interpretation: [higher scores = more/less of what?]
```

For qualitative:
```
Data type: [semi-structured interview / focus group / document / observation field notes]
Interview guide: [list of 5-8 main questions - attach as appendix]
Recording: [audio recorded with consent / field notes / etc.]
```

### Step 6: Specify analysis plan

Write this before collecting data. Pre-registration prevents HARKing (Hypothesizing After Results are Known).

**Quantitative:**
```
Primary analysis:
  Hypothesis: [restate H₁]
  Statistical test: [t-test / ANOVA / regression / chi-square / etc.]
  Rationale: [why this test for this data structure]
  Significance threshold: α = 0.05 (or pre-specified)
  Effect size: [Cohen's d / η² / r - will be reported regardless of significance]

Secondary analyses: [list]
Handling missing data: [listwise deletion / multiple imputation / etc.]
Outlier policy: [defined in advance: ±3 SD removed / winsorized / etc.]
Software: [R / SPSS / Stata / Python]
```

**Qualitative:**
```
Analysis method: [thematic analysis / IPA / grounded theory coding / etc.]
Coding process: [open → axial → selective coding / inductive → deductive]
Trustworthiness strategies:
  - Member checking: [participants review interpretations]
  - Peer debriefing: [second coder reviews sample]
  - Reflexivity: [researcher positionality statement]
  - Thick description: [sufficient detail for transferability judgments]
Inter-rater reliability: [if applicable - Cohen's κ target ≥ 0.70]
```

### Step 7: Address ethical considerations

```
Risk level: [minimal / low / medium / high]
Key risks to participants: [list]
Mitigations: [list]
IRB status: [pending / approved - include protocol number if approved]
Informed consent: [how obtained and documented]
Data storage: [encrypted / anonymized / access controls]
Data retention: [how long kept and then how destroyed]
Conflicts of interest: [none / disclose if any]
```

## Anti-Patterns

**1. Method chosen before question**
Bad: "I want to do a survey" before the research question is formed.
Good: Identify what you need to know, then select the method that answers it most reliably.

**2. No power analysis for quantitative work**
Bad: "We'll recruit 50 people."
Good: Power analysis using prior literature's effect size, α = 0.05, power = 0.80, gives required N, then add buffer for attrition.

**3. Analysis plan written after seeing data**
Bad: Exploratory analysis, then framing findings as confirmatory.
Good: Pre-register the primary hypothesis and analysis plan. Distinguish confirmatory from exploratory findings in the paper.

**4. Instrument without validity evidence**
Bad: "We made a 5-question survey."
Good: Use validated instruments with published reliability and validity data for the relevant population. If a novel instrument is required, include pilot validation steps.

## Quality Checklist

- [ ] Research paradigm matches the research question
- [ ] Study design type named and justified
- [ ] Inclusion/exclusion criteria specified
- [ ] Sample size justified (power analysis for quantitative, saturation plan for qualitative)
- [ ] Procedure is step-by-step and replicable
- [ ] Every measured variable has a named instrument with reliability and validity evidence
- [ ] Analysis plan written before data collection (pre-registered if possible)
- [ ] Missing data, outlier, and multiple comparison policies defined in advance
- [ ] Ethical risks identified with mitigations
- [ ] IRB/ethics review status noted
