---
name: vera-data-path-reviewing
description: >-
  Structural equation modeling skill. Collects latent constructs and
  path structure, checks identification and estimator requirements, fits one
  primary SEM, and reports global fit plus key structural paths with a
  recommendation block for advanced analyses. Trigger when the user asks
  for SEM, latent path analysis, full structural equation modeling, path
  coefficients, structural paths, mediation model, latent variable model,
  causal SEM, direct and indirect effects, or path diagram. Does not handle
  CFA-only models (use vera-data-cfa-reviewing) or longitudinal growth models
  (use vera-data-growth-reviewing).
allowed-tools: Read, Bash, Write, Edit
---

# Full SEM Testing — Initial Structural Model

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
- The model includes both a measurement component and structural paths among latent and/or observed variables.
- A first-pass SEM fit is needed before indirect-effect bootstrapping, multigroup comparison, or model revision.

Do not use this skill when:
- The task is CFA-only without structural paths; use `vera-data-cfa-reviewing`.
- The core question is longitudinal growth / change; use `vera-data-growth-reviewing`.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured SEM summary |
| Diagnose | Check Model Setup | Main Agent | `workflow/step02-check-model-setup.md` | Prior step output | Identification + estimator decision |
| Test | Run Primary Sem | Main Agent | `workflow/step03-run-primary-sem.md` | Prior step output | Initial SEM fit + recommendation |

## Decision Tree

```
1. CHECK MEASUREMENT COMPONENT
   ├── latent factors specified → SEM path
   └── only observed variables → consider path analysis, but keep SEM framing explicit

2. CHECK STRUCTURAL COMPONENT
   ├── direct paths only → baseline SEM
   ├── mediation present → label indirect paths for later testing
   └── multigroup / longitudinal / nonlinear elements → recommend specialized SEM skills

3. CHECK ESTIMATOR
   ├── continuous indicators → ML / MLR
   └── categorical indicators → WLSMV / DWLS
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Latent constructs** | Factor names, theoretical meaning, indicators per factor |
| **Structural paths** | Which latent/observed variables predict which |
| **Mediators** | Any indirect paths (X → M → Y) |
| **Scale type** | Continuous, ordinal/Likert, binary indicators |
| **Grouping variable** | Optional; for later multi-group comparison |
| **Sample size** | Final analytic N and missing-data context |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Model Setup Checks (identification, estimator)
PART 2: Primary SEM Fit (global fit + structural coefficients)
PART 3: Recommendation Block
```

## Reporting Standards

1. Always report `chi-square`, `df`, `CFI`, `TLI`, `RMSEA`, and `SRMR`
2. Report standardized path coefficients with SE or CI
3. Report R-squared for endogenous latent variables
4. Identification problems must be stated explicitly, never silently patched
5. Mediation paths: label but do not test significance (recommend full analysis)
6. Ends with recommendation block for mediation testing,
   multi-group analysis, model modification, and indirect effect bootstrapping
7. **Fit-index thresholds**: CFI / TLI ≥ 0.90 (≥ 0.95 preferred); RMSEA ≤ 0.08 (≤ 0.06 preferred);
   SRMR ≤ 0.08. For ordinal/categorical indicators with DWLS/WLSMV, report robust variants.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Structural-model setup checks, initial SEM fit, global fit reporting, key path reporting, mediation-path labeling |
| Implemented downstream in `vera-data-path-generating` | Indirect-effect bootstrapping, multigroup SEM, alternative-path comparison, residual review, manuscript assembly |
| Out of scope in this open-source baseline | Longitudinal growth SEM and latent-model families not explicitly named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-path-reviewing` on a small mediation-style SEM with two latent factors and one structural path chain. Produce the standard baseline artifacts and recommendation block."

Next step: Invoke `vera-data-path-generating` from this skillset
to run the full pipeline (indirect-effect bootstrap CIs, multi-group SEM, alternative-path comparison,
manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.

## Failure Modes

- If model does not converge: report non-convergence, suggest simplifying structure
- If outcome type is CFA-only (no structural paths): redirect to `vera-data-cfa-reviewing`
- If longitudinal growth structure detected: redirect to `vera-data-growth-reviewing`
