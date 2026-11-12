---
name: quick-model
description: "Fast path for a small model or back-of-envelope analysis: minimal spec, minimal checks, clear 'not for publication' label."
argument-hint: "[question]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /quick-model — Quick Model

**Category:** Scoping & Design · **Primary agent:** `semi-structural-gap-modeler`

Fast path for a small model or back-of-envelope analysis: minimal spec, minimal checks, clear 'not for publication' label.

Arguments: `$ARGUMENTS`

## Purpose
Answer an urgent, narrow question with the smallest model that can answer it, in hours rather than weeks, with minimal but real checks, and with an unmistakable label that the result is exploratory. The output is a short note that says what was done, what it shows, how fragile it is, and what would be needed to make it publishable.

**Use it when** a decision-maker needs an order of magnitude quickly, or a team wants to test whether a fuller model is worth building.

**Do not use it when** the result will be published or used in formal advice without promotion (`/model-brief`, `/validate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - User question
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `semi-structural-gap-modeler` — primary agent; coordinates the work and integrates results
- `financial-programming-specialist` — Builds financial programming frameworks

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Model | back-of-envelope accounting, small gap model, reduced-form elasticities, existing lego set | Speed versus structure |
| Inputs | published elasticities, quick estimates | Reliability |
| Uncertainty | ranges from alternative inputs | Honesty of the answer |

## Workflow
1. Ask the single most decision-relevant question and the time budget
2. Pick the smallest suitable model and write a half-page spec
   - Reuse an existing lego set where one fits
3. Build and run with at least two internal consistency checks
   - Show a range from alternative key inputs
4. Label output 'exploratory — not validated' and list what would be needed to promote it

## Checkpoints with the user
- After the question: confirm the decision and time budget
- Before delivery: confirm the label and caveats

## Common pitfalls
- Quick results quoted later as validated
- A single number without a range
- Scope creep beyond the time budget

## Output
`docs/models/<name>/quick-note.md`; code in `models/<family>/<name>/`

The quick note states the question, model, inputs, checks, range of results, caveats and the promotion path. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Output is labelled exploratory; promotion requires `/model-brief` and `/validate-model`
- Results are shown as a range from alternative key inputs

## Suggested next steps
- `/model-brief`
- `/scenario-analysis`
