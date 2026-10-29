---
name: biomed-study-appraiser
description: >-
  Critically appraise biomedical studies, including clinical trials,
  observational studies, animal experiments, in vitro work, case reports, and
  longitudinal studies. Use when evaluating whether a paper's design, controls,
  statistics, endpoints, population, and biological model support its claims.
  Emphasizes bias, confounding, reproducibility, translational relevance, and
  clinical applicability.
---

# Biomedical Study Appraiser

Critically evaluate a biomedical paper, trial record, case report, cohort study,
animal experiment, or in vitro study. The output should distinguish what the
data directly show from what the authors infer.

## Step 0: Inputs

Use the paper, DOI, PMID, trial registry record, PDF, abstract, or user-provided
excerpt. If the full text is not available, say so and limit confidence.

When the user has not specified the appraisal target, ask for the study or claim
to evaluate.

## Step 1: Extract Study Facts

Record:

- Citation, year, journal/preprint server, DOI/PMID/trial ID.
- Study type and design.
- Population/model: humans, animal species/strain, cell line, organoid, tissue, ex vivo system.
- Sample size and power calculation.
- Inclusion/exclusion criteria.
- Intervention/exposure and comparator/control.
- Dose, route, timing, duration, and follow-up.
- Primary and secondary endpoints.
- Statistical methods.
- Funding, sponsor, and conflicts of interest.

## Step 2: Internal Validity

Assess whether the study design supports the causal or mechanistic claim:

- Randomization and allocation concealment.
- Blinding of participants, clinicians, investigators, and outcome assessors.
- Control group quality.
- Baseline balance.
- Attrition, missing data, and analysis population.
- Multiple testing and endpoint switching.
- Confounding and adjustment strategy.
- Appropriateness of statistical model.
- Effect size, confidence intervals, and clinical/practical significance.
- Reproducibility of methods and availability of data/code/protocol.

For animal studies, also check randomization, blinding, litter/cage effects,
sex balance, strain choice, housing conditions, and humane endpoints.

For in vitro studies, also check cell line identity, passage number,
contamination/mycoplasma control, physiologic dose range, replicate structure,
and assay specificity.

## Step 3: External Validity

Assess whether the result generalizes:

- Does the population match the claimed clinical population?
- Is the disease stage comparable?
- Are dose, route, timing, and duration realistic?
- Are endpoints clinically meaningful or merely surrogate/mechanistic?
- Are animal or cell models known to reproduce the human biology?
- Are there sex, age, ancestry, comorbidity, or medication-interaction limits?
- Are safety outcomes measured long enough and broadly enough?

## Step 4: Claim-by-Claim Audit

List each major claim and classify it:

- Directly supported.
- Partially supported.
- Mechanistically plausible but not established.
- Unsupported by the presented data.
- Contradicted or weakened by the presented data.

For each claim, cite the exact result, endpoint, figure/table, or registry field
when available.

## Step 5: Output

Use this structure:

```markdown
# Study Appraisal: [Citation]

## Study Snapshot
| Field | Details |
|------|---------|
| Study type | |
| Population/model | |
| Sample size | |
| Intervention/exposure | |
| Comparator/control | |
| Primary endpoint | |
| Follow-up | |

## What the Data Directly Show
[Concrete findings with effect sizes where available.]

## Strengths
[Design features that increase credibility.]

## Major Limitations
[Design, statistical, endpoint, bias, and model limitations.]

## Bias and Confounding Risks
[Specific risks, not generic warnings.]

## Translational or Clinical Relevance
[Human relevance, dose realism, endpoint relevance, safety.]

## Claim-by-Claim Assessment
| Claim | Supported? | Reason |
|------|------------|--------|

## Confidence Rating
[High / Moderate / Low / Very low] with one paragraph justification.
```

## Standards

- Never let the abstract substitute for the methods and results.
- Treat preclinical studies as preclinical, even when mechanistically strong.
- Treat uncontrolled human studies as hypothesis-generating unless the effect is unusually clear and alternative explanations are weak.
- Report null and adverse findings with the same care as positive findings.
- If a study is underpowered, say which conclusions are especially unstable.
