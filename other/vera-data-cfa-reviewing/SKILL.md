---
name: vera-data-cfa-reviewing
description: >-
  Runs the CFA pipeline: collect indicator structure, check basic
  identification and estimator requirements, fit a primary CFA model, and
  report fit indices plus standardized loadings with a recommendation block for
  full SEM analysis. Trigger when the user asks for CFA, confirmatory factor
  analysis, measurement model testing, latent factor validation, factor
  loading assessment, construct validity, scale validation, measurement
  invariance check, or psychometric evaluation. Does not cover full structural
  path modeling (use vera-data-path-reviewing) or longitudinal change modeling
  (use vera-data-growth-reviewing).
allowed-tools: Read, Bash, Write, Edit
---

# CFA Testing — Identification, Primary Fit, Recommendation

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Decision Tree](#decision-tree)
- [Required Inputs](#required-inputs)
- [Code Structure](#code-structure)
- [Reporting Standards](#reporting-standards)
- [Method Status](#method-status)
- [Minimal Smoke Test](#minimal-smoke-test)


Open-source skill.

## Scope Boundary

Use this skill when:
- The main goal is a confirmatory measurement model for named latent constructs.
- A first-pass CFA with identification, estimator choice, and global fit reporting is the right checkpoint before validity or invariance work.

Do not use this skill when:
- The question is primarily about structural paths or mediation; use `vera-data-path-reviewing`.
- The focus is longitudinal change modeling across waves; use `vera-data-growth-reviewing`.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured SEM input summary |
| Diagnose | Check Measurement Setup | Main Agent | `workflow/step02-check-measurement-setup.md` | Prior step output | Identification + estimator decision |
| Test | Run Primary Cfa | Main Agent | `workflow/step03-run-primary-cfa.md` | Prior step output | Initial CFA fit + recommendation block |

## Decision Tree

```
1. CHECK MODEL FORM
   ├── Reflective latent factors with named indicators → CFA path
   └── Structural relations without clear latent blocks → recommend sem-full

2. CHECK ESTIMATOR
   ├── Continuous, roughly normal indicators → ML / MLR
   ├── Continuous, non-normal indicators → robust ML
   └── Ordinal indicators → WLSMV / DWLS

3. CHECK IDENTIFICATION
   ├── Each factor has 3+ indicators → standard identification
   ├── 2 indicators → require theory + equality/variance constraints
   └── 1 indicator → do not fit as free CFA factor without extra constraints
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Latent constructs** | Factor names and theoretical meaning |
| **Indicators** | Which observed variables load on each factor |
| **Scale type** | Continuous, ordinal/Likert, binary indicators |
| **Grouping variable** | Optional; for later invariance testing |
| **Sample size** | Final analytic N and missing-data context |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Measurement Setup Checks
PART 2: Primary CFA Fit
PART 3: Recommendation Block
```

## Reporting Standards

1. Always report `chi-square`, `df`, `CFI`, `TLI`, `RMSEA`, and `SRMR`
2. Report standardized loadings with SE or CI when available
3. Say "fit was acceptable / borderline / poor" rather than "good" without context
4. Identification problems must be stated explicitly, never silently patched
5. Ends with a recommendation block for reliability/validity,
   invariance, and alternative-model comparison
6. **Fit-index thresholds**: CFI / TLI ≥ 0.90 (≥ 0.95 preferred); RMSEA ≤ 0.08 (≤ 0.06 preferred);
   SRMR ≤ 0.08. For ordinal/categorical indicators with DWLS/WLSMV, report robust (scaled/adjusted)
   versions of CFI, TLI, and RMSEA.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Measurement setup checks, estimator choice, identification triage, initial CFA fit, fit-index reporting, standardized loadings |
| Implemented downstream in `vera-data-cfa-generating` | Reliability / validity summaries, invariance testing, alternative-model comparison, MI review, manuscript assembly |
| Out of scope in this open-source baseline | Structural SEM, longitudinal SEM, and any latent-variable family not named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-cfa-reviewing` on a small 2-factor CFA example with 3 indicators per factor and continuous indicators. Produce the standard baseline artifacts and recommendation block."

Next step: Invoke `vera-data-cfa-generating` from this skillset
to run the full pipeline (reliability/validity, invariance testing, alternative-model comparison,
manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
