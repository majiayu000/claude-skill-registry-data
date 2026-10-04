---
name: vera-data-growth-reviewing
description: >-
  Longitudinal SEM skill for latent growth and change. Collects wave
  structure, checks whether a growth/change model is identified, fits an
  initial linear growth or latent change specification, and reports fit plus
  trajectory parameters with a recommendation block. Trigger when the user
  asks for latent growth models, growth curves in SEM, latent change score
  models, longitudinal latent trajectories, growth curve modeling, LGM, LCSM,
  trajectory analysis, or change over time in SEM. Does not handle cross-
  sectional CFA (use vera-data-cfa-reviewing) or non-longitudinal structural
  models (use vera-data-path-reviewing).
allowed-tools: Read, Bash, Write, Edit
---

# Longitudinal Change Testing — Initial Growth / Change Fit

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Decision Tree](#decision-tree)
- [Required Inputs](#required-inputs)
- [Code Structure](#code-structure)
- [Reporting Standards](#reporting-standards)
- [Method Status](#method-status)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Failure Modes](#failure-modes)


Open-source skill.

## Scope Boundary

Use this skill when:
- The goal is a latent growth or latent change baseline for repeated measurements across waves.
- A first-pass longitudinal SEM checkpoint is needed before nonlinear or multigroup extensions.

Do not use this skill when:
- The data are cross-sectional CFA or non-longitudinal SEM; use the corresponding SEM skill.
- The design is a high-frequency observed time series rather than longitudinal SEM.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured longitudinal SEM summary |
| Diagnose | Check Longitudinal Setup | Main Agent | `workflow/step02-check-longitudinal-setup.md` | Prior step output | Wave/identification decision |
| Test | Run Primary Model | Main Agent | `workflow/step03-run-primary-model.md` | Prior step output | Initial LGM/LCSM fit + recommendation |

## Decision Tree

```
1. CHECK TIME STRUCTURE
   ├── 3+ waves of same construct → latent growth candidate
   ├── adjacent change focus → latent change score candidate
   └── only 2 waves → limited change model; report cautiously

2. CHECK MEASUREMENT
   ├── repeated observed score only → basic growth/change SEM
   └── latent construct per wave → recommend invariance-aware model

3. CHECK TRAJECTORY FORM
   ├── theory supports linear change → linear growth first
   └── theory suggests curvature → recommend nonlinear/basis model
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Repeated measure** | Variable name measured at each wave |
| **Time points** | Number of waves, spacing (equal/unequal), time coding |
| **Model type** | Latent growth (LGM) vs latent change score (LCSM) |
| **Scale type** | Continuous, ordinal/Likert indicators per wave |
| **Time-invariant covariates** | Optional predictors of intercept/slope |
| **Sample size** | Final analytic N, attrition pattern |

## Code Structure

```
PART 0: Setup & Data Loading (wide or long format)
PART 1: Longitudinal Setup Checks (waves, identification, estimator)
PART 2: Primary Growth/Change Model Fit (intercept, slope, fit indices)
PART 3: Recommendation Block
```

## Reporting Standards

1. Always report `chi-square`, `df`, `CFI`, `TLI`, `RMSEA`, and `SRMR`
2. Report mean and variance of intercept and slope factors
3. Report intercept-slope covariance/correlation
4. If covariates included: report their effects on intercept and slope
5. Only 2 waves: state limitation explicitly ("minimal identification")
6. Ends with recommendation block for nonlinear growth,
   piecewise models, time-varying covariates, and class-based trajectories
7. **Fit-index thresholds**: CFI / TLI ≥ 0.90 (≥ 0.95 preferred); RMSEA ≤ 0.08 (≤ 0.06 preferred);
   SRMR ≤ 0.08. For ordinal indicators with DWLS/WLSMV, report robust variants.
8. **Measurement invariance (if repeated latent constructs across waves)**: test the standard sequence
   configural → metric (equal loadings) → scalar (equal intercepts) → strict (equal residual variances).
   Report ΔCFI < 0.010 and ΔRMSEA < 0.015 as thresholds for invariance at each step. Halt invariance
   comparison at the first level that fails and note the partial-invariance status.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Wave-structure checks, initial LGM / LCSM fit, intercept / slope summaries, invariance-aware recommendation triggers |
| Implemented downstream in `vera-data-growth-generating` | Nonlinear trajectories, latent-basis and change-score variants, multigroup growth, parallel-process extensions, manuscript assembly |
| Out of scope in this open-source baseline | Cross-sectional SEM, CFA-only work, and longitudinal families not explicitly named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-growth-reviewing` on a 3-wave repeated-measure example with equal spacing and continuous indicators. Produce the standard baseline artifacts and recommendation block."

Next step: Invoke `vera-data-growth-generating` from this skillset
to run the full pipeline (nonlinear trajectories, latent-basis/change-score variants, multigroup growth,
parallel-process models, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared
handoff contract.

## Failure Modes

- If only 2 waves: fit basic change model but warn about minimal identification
- If model does not converge: suggest simpler specification (intercept-only)
- If cross-sectional CFA structure detected: redirect to `vera-data-cfa-reviewing`
- If non-longitudinal structural model: redirect to `vera-data-path-reviewing`
