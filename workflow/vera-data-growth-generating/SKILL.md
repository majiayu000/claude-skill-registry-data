---
name: vera-data-growth-generating
description: >-
  Full longitudinal SEM skill for latent growth and change models.
  Extends the initial fit with nonlinear trajectories, latent-basis and
  change-score variants, subgroup comparisons, parallel-process models when
  available, and manuscript-ready output. Trigger after vera-data-growth-reviewing completes and its
  PART 0–2 artifacts are present (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without
  those artifacts, halts and prompts the user to run testing first or supply equivalent PART 0–2 code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Longitudinal Change Analyzing — Full Growth / Change Pipeline

Open-source skill.

Read `reference/specs/output-variation-protocol.md` before every generation.

## Workflow

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional tests | Run Additional Tests | Main Agent | `workflow/step04-run-additional-tests.md` | Prior step output | Nonlinear/change diagnostics |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | Multigroup growth/change |
| Modeling | Fit Models | Main Agent | `workflow/step06-fit-models.md` | Prior step output | Alternative growth/change models |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | Cross-trajectory synthesis |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |
