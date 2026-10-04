---
name: vera-data-path-generating
description: >-
  Full SEM analysis skill. Extends the initial structural model with indirect
  effects, alternative-path comparison, multigroup testing, residual review,
  and manuscript-ready methods/results. Trigger after vera-data-path-reviewing completes and its PART 0–2
  artifacts are present (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those
  artifacts, halts and prompts the user to run testing first or supply equivalent PART 0–2 code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Full SEM Analyzing — Structural Paths, Indirect Effects, Manuscript

Open-source skill.

Read `reference/specs/output-variation-protocol.md` before every generation.

## Workflow

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional tests | Run Additional Tests | Main Agent | `workflow/step04-run-additional-tests.md` | Prior step output | Indirect/residual diagnostics |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | Multigroup SEM |
| Modeling | Fit Models | Main Agent | `workflow/step06-fit-models.md` | Prior step output | Alternative structural models |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | Cross-model synthesis |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if not already provided during testing:
- Target discipline and journal (for reporting conventions — APA 7th, Structural Equation Modeling style, etc.)
- Research question / hypothesis (directional path predictions)
- Grouping variable (for multigroup invariance testing)
- Mediation structure (which paths are hypothesized as indirect)
- Estimator preference if deviating from testing-skill default (ML, MLR, WLSMV, DWLS)

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/              ← lavaan/semopy parameter tables, fit-index tables (Markdown + CSV)
├── figures/             ← path diagram, residual plots, multigroup comparison plots (PNG, 300 DPI)
├── references.bib
├── code.R               ← Style-varied lavaan script
└── code.py              ← Style-varied semopy script (optional)
```

## Key References (read before generation)

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation layers |
| `reference/specs/code-style-variation.md` | Seven-dimension code style diversity |
| `reference/patterns/sentence-bank.md` | 4–6 phrasings per result type |
| `reference/rules/reporting-standards.md` | Hard rules for SEM reporting |

## Reporting Standards

Same as vera-data-path-reviewing, plus:
- **Indirect effects**: always report with bias-corrected bootstrap 95% CI (≥ 5000 draws). Do not rely on Sobel z.
- **Direct / indirect / total**: report all three; when direct becomes non-significant after accounting for the indirect path, describe as "consistent with partial/full mediation" rather than proof of causality.
- **Multigroup**: report the Δχ², Δdf, Δp, ΔCFI for each invariance step (configural → metric → structural).
- **Alternative models**: compare with χ² difference test (nested) or AIC/BIC (non-nested); interpret ΔAIC > 10 as strong preference.
- **Under MLR / Satorra–Bentler scaled estimators**: Δχ² MUST be computed using the **scaled difference statistic** (Satorra & Bentler 2001), not by subtracting the two scaled χ² values. Simple subtraction of Satorra–Bentler-adjusted χ² gives a biased test. Use `lavaan::lavTestLRT(fit1, fit2, method="satorra.bentler.2001")` (or 2010 variant for negative corrections). Report the scaled difference T_d, df, p. This applies to ALL nested-model comparisons, including measurement-invariance steps.
- **Modification indices**: only apply when theoretically justified; report which MIs were accepted and which rejected.
- **Standardized path coefficients**: β with SE or CI; asterisks for significance levels discouraged — report exact p.

## Cross-Skill Interface

```
Method Unit Contract:
├── code_r           → .R script (style-varied, lavaan)
├── code_python      → .py script (style-varied, semopy, optional)
├── methods_md       → methods.md (varied structure)
├── results_md       → results.md (varied phrasing)
├── tables/          → Markdown + CSV
├── figures/         → PNGs 300 DPI (varied layout)
├── references_bib   → .bib with cited references
└── comparison       → cross-model narrative (in results.md)
```

Invoked directly after `vera-data-path-reviewing` or orchestrated by `vera-data-application-pipelining`.
