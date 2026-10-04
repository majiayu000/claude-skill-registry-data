---
name: vera-data-cfa-generating
description: >-
  Full CFA skill for measurement-model evaluation. Extends the initial
  CFA fit with reliability, convergent/discriminant validity, alternative-model
  comparison, modification-index review, subgroup invariance testing, and
  manuscript-ready methods/results. Trigger after vera-data-cfa-reviewing completes and its PART 0–2
  artifacts are present (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those
  artifacts, halts and prompts the user to run testing first or supply equivalent PART 0–2 code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# CFA Analyzing — Full Measurement Model & Manuscript

Open-source skill.

Read `reference/specs/output-variation-protocol.md` before every generation.

## Workflow

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional tests | Run Additional Tests | Main Agent | `workflow/step04-run-additional-tests.md` | Prior step output | Reliability + validity code/prose |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | Measurement invariance code/prose |
| Modeling | Fit Models | Main Agent | `workflow/step06-fit-models.md` | Prior step output | Alternative CFA models |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | Cross-model synthesis |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if missing:
- target discipline / journal style
- whether theory allows correlated residuals or cross-loadings
- planned grouping variable for invariance
- whether ordinal indicators should force a categorical estimator

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/
├── figures/
├── references.bib
├── code.R
└── code.py
```

## Key References

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation |
| `reference/specs/code-style-variation.md` | Code style diversity |
| `reference/patterns/sentence-bank.md` | SEM wording variants |
| `reference/rules/reporting-standards.md` | CFA reporting rules |
