---
name: estimate-var
description: "Estimates VAR/SVAR/VECM models with diagnostics, identification and impulse responses."
---
<!-- Generated from .claude/skills/estimate-var/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /estimate-var — Estimate VAR

**Category:** Estimation · **Primary agent:** `var-vecm-specialist`

Estimates VAR/SVAR/VECM models with diagnostics, identification and impulse responses.

Arguments: whatever the user wrote after the command name.

## Purpose
Estimate a VAR, structural VAR or VECM with the specification choices made explicitly, diagnostics reported, identification stated and tested, and impulse responses shown with honest uncertainty bands. The output is a set of results whose conclusions survive an alternative identification or specification.

**Use it when** dynamic interactions among a few macro variables matter, structural shocks must be identified from data, or cointegration relations are of interest.

**Do not use it when** the goal is forecasting many variables (`/estimate-bvar`), when responses at long horizons with external instruments are needed (`/local-projections`), or when the shock series is the deliverable (`/identify-shocks`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Data sheet
   - Identification scheme
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `var-vecm-specialist` — primary agent; coordinates the work and integrates results
- `shock-identification-specialist` — Identifies structural shocks
- `data-quality-seasonal-specialist` — Ensures data quality

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Specification | levels, differences, VECM | Long-run information and inference |
| Lag length | information criteria, residual tests | Dynamics and degrees of freedom |
| Identification | recursive, sign restrictions, long-run, external instruments, heteroskedasticity | What the shocks mean |
| Inference | bootstrap, Bayesian, robust bands for set identification | Honest uncertainty |
| Sample | full, post-break, excluding outliers | Stability |

## Workflow
1. Test integration order and cointegration; choose lag length and deterministic terms
2. Estimate the reduced form; run stability and residual diagnostics
   - Roots, serial correlation, heteroskedasticity, normality; parameter stability tests
3. Apply identification and compute IRFs, FEVD with bands
   - State the economic justification for each restriction
4. Run robustness under an alternative identification or specification

## Checkpoints with the user
- After specification: confirm variables, sample and deterministic terms
- After identification: confirm restrictions are defensible

## Common pitfalls
- Recursive orderings without justification
- Sign restrictions reported as point identification
- Ignoring structural breaks
- Over-reading forecast-error variance decompositions

## Output
`docs/models/<name>/var-results.md`; code and settings in `models/econometrics/<name>/`

The results document reports specification tests, diagnostics, identification, IRFs and FEVD with bands, and robustness; code and settings allow exact rerun. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Stability and residual tests reported
- Robustness to identification shown
- Identification restrictions are justified economically
- Set-identified results are reported as sets

## Suggested next steps
- `/validate-model`
- `/scenario-analysis`
