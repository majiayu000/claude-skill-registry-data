---
name: biomed-evidence-synthesizer
description: >-
  Synthesize biomedical evidence across multiple studies, including randomized
  trials, observational cohorts, case reports, animal models, in vitro
  experiments, longitudinal studies, and meta-analyses. Use when comparing
  conflicting results, grading evidence strength, identifying replication,
  evaluating clinical relevance, and forming cautious conclusions from the
  totality of evidence.
---

# Biomedical Evidence Synthesizer

Integrate multiple biomedical studies into a balanced conclusion. Use this when
the user has several papers, mixed evidence, conflicting results, or a broad
question that requires weighing clinical, observational, animal, and mechanistic
data together.

## Step 0: Frame the Evidence Question

Write the question as:

```text
In [population/context], does [exposure/intervention/mechanism] affect
[endpoint/outcome], compared with [control/comparator], over [time scale]?
```

If needed, split one broad question into mechanistic, efficacy, safety, and
translation subquestions.

## Step 1: Build the Evidence Table

Group studies by type:

- Systematic reviews and meta-analyses.
- Randomized controlled trials.
- Nonrandomized interventional studies.
- Prospective cohorts.
- Retrospective cohorts and case-control studies.
- Case reports and case series.
- Animal studies.
- Ex vivo, organoid, in vitro, biochemical, and computational studies.
- Trial registry records and regulatory reviews.

For each study, extract:

- Population/model.
- Exposure/intervention and comparator.
- Dose, route, timing, duration, and follow-up.
- Endpoint type: clinical, surrogate, biomarker, mechanistic, safety.
- Effect direction and magnitude.
- Statistical uncertainty.
- Main limitations.

## Step 2: Compare Studies

Check whether studies are actually asking the same question. Differences that
often explain disagreement:

- Disease subtype or stage.
- Age, sex, comorbidities, baseline risk, and concomitant therapies.
- Species, strain, tissue, cell line, or model system.
- Dose, formulation, route, timing, and treatment duration.
- Acute versus chronic exposure.
- Primary versus secondary endpoints.
- Surrogate versus clinical endpoints.
- Adjustment for confounding.
- Follow-up length.
- Publication bias, selective outcome reporting, and sponsor effects.

## Step 3: Grade the Body of Evidence

Assess:

- Consistency: are effects in the same direction?
- Replication: independent groups, populations, and methods.
- Precision: sample size, uncertainty intervals, event counts.
- Directness: does evidence answer the actual clinical or mechanistic question?
- Bias risk: randomization, blinding, confounding, attrition, selective reporting.
- Dose-response and temporal relationship.
- Biological plausibility without over-weighting mechanism.
- Safety and adverse event evidence.

Use these conclusion labels:

- Clinically established.
- Clinically supported but incomplete.
- Promising but preliminary.
- Mechanistically plausible but clinically unproven.
- Mixed or inconclusive.
- Unsupported.
- Contradicted by stronger evidence.

## Step 4: Resolve Conflicts

When studies disagree, do not average them rhetorically. Identify whether the
conflict is likely due to:

- Study quality.
- Different populations or models.
- Different endpoints.
- Different doses or timing.
- Chance, underpowering, or multiple testing.
- Confounding or bias.
- Real biological heterogeneity.

Say which explanation is most plausible and why.

## Step 5: Output

Use this structure:

```markdown
# Evidence Synthesis: [Question]

## Bottom Line
[One cautious paragraph with evidence grade.]

## Evidence by Study Type
[Short summary grouped by evidence type.]

## Cross-Study Comparison
| Study | Type | Population/Model | Exposure | Endpoint | Result | Key Limitation |
|------|------|------------------|----------|----------|--------|----------------|

## Areas of Agreement
[Findings replicated or directionally consistent.]

## Areas of Conflict
[Contradictions and plausible explanations.]

## Human Clinical Relevance
[Whether evidence reaches human clinical endpoints.]

## Safety Evidence
[Known adverse events, missing safety data, follow-up limitations.]

## Most Plausible Interpretation
[Reasoned synthesis, not a vote count.]

## What Would Change the Conclusion
[Specific future study designs, endpoints, or missing data.]
```

## Standards

- Weight stronger designs more heavily, but do not ignore consistent lower-level evidence.
- Do not equate mechanistic coherence with clinical proof.
- Do not bury heterogeneity; explain it.
- Treat unpublished completed trials and terminated trials as important signals when relevant.
- Keep causality claims proportional to design quality.
