---
name: model-spec
description: "Writes the model specification: equations, timing, closures, steady state, shocks, observables and known limitations."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /model-spec — Model Spec

**Category:** Scoping & Design · **Primary agent:** `modeling-methodology-specialist`

Writes the model specification: equations, timing, closures, steady state, shocks, observables and known limitations.

Arguments: `$ARGUMENTS`

## Purpose
Write the model specification: the complete, unambiguous statement of what will be built — notation, timing, units, every equation and closure, steady state, shocks, observables, parameters, identification concerns and known limitations. The output is the document the code is checked against, so that the build and validation have a single source of truth.

**Use it when** a model brief is approved and building is about to start, or an existing model needs a written specification.

**Do not use it when** the model class is still undecided (`/select-model-class`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - docs/models/<name>/model-brief.md
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `modeling-methodology-specialist` — primary agent; coordinates the work and integrates results
- `open-economy-dsge-specialist` — Builds small open-economy DSGE models
- `semi-structural-gap-modeler` — Builds quarterly projection and semi-structural gap models
- `deep-learning-architect` — Designs deep learning architectures for macro-financial data

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Notation | studio conventions, literature conventions | Consistency with documentation |
| Timing | end-of-period stocks, beginning-of-period stocks | Code correctness |
| Detail | core model only, with extensions as optional bricks | Modularity |
| AI models | architecture, loss and training data in place of equations | What is specified |

## Workflow
1. Select the specialists for the model class and have them draft section by section
2. Define notation, timing conventions and units; list all equations and the closure
   - Keep a notation register used by all later documents
3. Derive the steady state and the log-linearization (or the architecture and loss for AI models)
   - Verify derivations symbolically for medium and large models
4. List shocks, observables, parameters and identification concerns
5. State known limitations and non-purposes
   - Identify which parts can be lego bricks with declared interfaces

## Checkpoints with the user
- After the equation list: confirm mechanisms and closure
- After shocks and observables: confirm identification concerns

## Common pitfalls
- Timing ambiguities left for coders to resolve
- Equations without units
- Missing closure conditions
- Limitations omitted

## Output
`docs/models/<name>/model-spec.md`

The specification contains the notation register, equations with units and timing, closure, steady state, shocks, observables, parameters, identification concerns and limitations.

## Gate / verdict
- Every endogenous variable has an equation; counts of equations and unknowns match
- Steady state is derived or the computation approach is stated
- Timing conventions and units are stated for every variable
- A notation register is included

## Suggested next steps
- `/calibration-plan`
- `/data-requirements`
