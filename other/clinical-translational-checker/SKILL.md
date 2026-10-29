---
name: clinical-translational-checker
description: >-
  Check whether biomedical claims based on animal studies, cell experiments,
  molecular mechanisms, or biomarkers have credible human clinical support. Use
  when evaluating translational relevance, clinical trials, dose realism,
  endpoints, safety, regulatory status, and whether evidence is animal-only,
  preliminary human, or clinically established.
---

# Clinical Translational Checker

Determine whether a biomedical claim has crossed from mechanism, animal work,
or biomarker association into credible human clinical evidence. This skill is
especially important when a result sounds compelling but may be based only on
cell culture, animal models, surrogate endpoints, or uncontrolled observations.

## Step 0: Identify the Claim

Rewrite the claim precisely:

```text
[Exposure/intervention/molecule/mechanism] causes/improves/predicts [outcome]
in [human population/context] at [dose/timing/duration].
```

Classify the claim:

- Therapeutic efficacy.
- Safety/toxicity.
- Diagnostic biomarker.
- Prognostic biomarker.
- Mechanistic pathway.
- Disease causation.
- Risk association.

## Step 1: Locate the Evidence Tier

Assign the highest currently supported tier:

1. Guideline or regulatory accepted clinical use.
2. Replicated, adequately powered RCTs with clinical endpoints.
3. Human interventional evidence with limitations.
4. Human observational evidence.
5. Human biomarker or surrogate evidence.
6. Animal evidence.
7. Ex vivo, organoid, in vitro, biochemical, or computational evidence.
8. Hypothesis/speculation only.

Record whether higher-tier evidence is absent, negative, unpublished, ongoing,
terminated, or inconsistent.

## Step 2: Check Clinical Trials

For interventions, drugs, supplements, devices, or biomarkers, check trial
registries and regulatory sources when possible:

- Trial phase and design.
- Enrollment target and actual enrollment.
- Status: recruiting, completed, terminated, withdrawn, unknown.
- Primary completion date and whether results are posted.
- Primary and secondary endpoints.
- Comparator and blinding.
- Population and inclusion/exclusion criteria.
- Safety monitoring and adverse events.

Flag completed trials without published results or registry results.

## Step 3: Evaluate Translation Barriers

Check:

- Dose: clinically achievable or supraphysiologic?
- Route: same as proposed human use?
- Timing: prevention, acute treatment, chronic treatment, or reversal?
- Endpoint: clinical outcome, validated surrogate, exploratory biomarker, or assay artifact?
- Population: relevant age, disease stage, sex, comorbidity, and background therapy?
- Model: does animal/cell model reproduce the human pathology?
- Species differences: receptor expression, metabolism, immune response, lifespan, microbiome, pharmacokinetics.
- Safety: duration, off-target effects, adverse events, drug interactions, toxicity margins.
- Reproducibility: independent replication and negative studies.

## Step 4: Translation Rating

Use one of these labels:

- Clinically established.
- Clinically supported but incomplete.
- Preliminary human evidence.
- Human association only.
- Mechanistic/animal evidence only.
- In vitro evidence only.
- Unsupported.
- Contradicted by stronger clinical evidence.

## Step 5: Output

Use this structure:

```markdown
# Translational Evidence Check: [Claim]

## Precise Claim
[Rewritten claim.]

## Translation Rating
[One label with short justification.]

## Highest Evidence Tier Found
[Tier and sources.]

## Human Clinical Evidence
[Trials, cohorts, case studies, safety data, regulatory/guideline status.]

## Preclinical and Mechanistic Evidence
[Animal, in vitro, ex vivo, biochemical evidence.]

## Translation Barriers
| Barrier | Assessment |
|--------|------------|
| Dose realism | |
| Route/timing | |
| Endpoint relevance | |
| Model/species fit | |
| Safety | |
| Replication | |

## Trial and Regulatory Status
[Registered trials, results availability, approvals, warnings.]

## Bottom Line
[What can and cannot be claimed clinically.]
```

## Standards

- Say "animal-only" or "in vitro only" when that is the case.
- Do not upgrade a claim because the mechanism is elegant.
- Treat biomarker movement as distinct from clinical benefit.
- Treat safety as part of translation, not an afterthought.
- If no clinical trials exist, state that plainly and avoid clinical efficacy language.
