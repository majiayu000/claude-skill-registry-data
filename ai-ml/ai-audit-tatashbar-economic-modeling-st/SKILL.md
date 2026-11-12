---
name: ai-audit
description: "Audits AI/ML/LLM components: benchmarks, leakage, calibration, explainability, bias, red-team, confidentiality, monitoring."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /ai-audit — AI Audit

**Category:** Validation & QA · **Primary agent:** `model-risk-governance-specialist`

Audits AI/ML/LLM components: benchmarks, leakage, calibration, explainability, bias, red-team, confidentiality, monitoring.

Arguments: `$ARGUMENTS`

## Purpose
Audit an AI, machine-learning or LLM component before it is used in analysis or advice: whether its evaluation is honest (no leakage, fair benchmarks), whether its uncertainty is calibrated and stable, whether what it learned makes economic sense, whether it performs fairly across country groups, whether it resists red-team attacks, and whether confidentiality and human oversight are in place. The output is a verdict that can block release.

**Use it when** any AI component (forecaster, classifier, solver, RL policy, LLM pipeline, RAG system) is about to be used in production or published work.

**Do not use it when** the component is a traditional econometric or structural model (`/validate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Experiment log
   - Model code
   - Evaluation card
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `model-risk-governance-specialist` — primary agent; coordinates the work and integrates results
- `ai-ethics-fairness-specialist` — Reviews AI ethics and fairness
- `llm-red-team-specialist` — Red-teams LLM systems
- `interpretable-ml-specialist` — Makes AI models explainable
- `model-validation-specialist` — Performs independent model validation

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Depth | light review, full audit | Effort and assurance |
| Benchmarks | simple econometric models, previous version | Bar for added value |
| Fairness groups | country groups, income levels, regions | Disaggregated results |
| LLM tests | factuality sets, injection, leakage, version regression | Security coverage |

## Workflow
1. Check data splits for leakage and benchmark fairness
   - Time-aware splits; preprocessing fitted on training data only; benchmarks given equal tuning effort
2. Check calibration, uncertainty and stability across seeds, windows and versions
3. Review explainability and economic plausibility of learned relationships
   - Flag counterintuitive relationships for economic review
4. Review bias by country group and income level; for LLMs run the red-team harness
5. Review confidentiality and human-oversight design; define monitoring

## Checkpoints with the user
- After scope: confirm depth and benchmarks
- Before the verdict: review conditions and owners

## Common pitfalls
- Accepting reported scores without rerunning
- Benchmarks tuned less carefully than the AI model
- Average performance hiding failures for some groups
- Oversight that exists only on paper

## Output
`validation/<model>/ai-audit.md`

The audit report covers leakage, benchmarks, calibration, stability, plausibility, fairness, red-team results, confidentiality and oversight, with findings, conditions, owners and the verdict.

## Gate / verdict
- Verdict: PASS / PASS WITH CONDITIONS / FAIL; failures block release
- Every finding cites evidence and has an owner

## Suggested next steps
- `/validate-model`
- `/model-risk-review`
