---
name: code-review
description: "Reviews model and pipeline code for correctness, numerical soundness, reproducibility and standards compliance."
argument-hint: "[path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /code-review — Code Review

**Category:** Validation & QA · **Primary agent:** `python-julia-engineer`

Reviews model and pipeline code for correctness, numerical soundness, reproducibility and standards compliance.

Arguments: `$ARGUMENTS`

## Purpose
Review model and pipeline code for what matters in economic modeling: does it implement the specification correctly (equations, timing, units), is it numerically sound, can it be reproduced, and is it tested? The output is a list of findings by severity with concrete fixes.

**Use it when** model code, data pipelines or analysis scripts change, before validation, or when results look suspicious.

**Do not use it when** a full independent validation is required (`/validate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Code at path
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `python-julia-engineer` — primary agent; coordinates the work and integrates results
- `numerical-methods-specialist` — Specializes in numerical methods
- `reproducibility-engineer` — Guarantees reproducibility

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Scope | whole model, changed files, specific function | Effort |
| Depth | read-through, read plus test runs, partial re-implementation | Assurance |
| Standards | `.claude/rules/` for the path, project conventions | Criteria |

## Workflow
1. Read the code against the spec and `.claude/rules/` for the path
   - Equation-by-equation comparison with the specification; timing of stocks
2. Check numerics: tolerances, conditioning, units, timing conventions
3. Check reproducibility: seeds, versions, hard-coded paths and parameters
4. Check tests: coverage of identities, steady state and edge cases
5. List findings by severity with concrete fixes

## Checkpoints with the user
- After scope: confirm files and depth
- After findings: agree fixes and owners

## Common pitfalls
- Reviewing style while missing equation errors
- Ignoring unit and scale conventions
- Accepting tests that only check that code runs
- Missing silent failures (solver exits treated as convergence)

## Output
`validation/code-reviews/<name>.md`

The review lists findings by severity, with file and line, the problem, its consequence and the fix.

## Gate / verdict
- No hard-coded parameters or paths in model code; tests exist for identities
- Every finding states its consequence and a concrete fix

## Suggested next steps
- `/validate-model`
