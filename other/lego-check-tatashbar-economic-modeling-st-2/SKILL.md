---
name: lego-check
description: "Checks a lego model: all studs connected or stubbed, no duplicate providers, slots filled, units and frequencies consistent, identities verifiable, simultaneous blocks listed."
argument-hint: "[manifest path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /lego-check — Lego Check

**Category:** Lego (Modular Models) · **Primary agent:** `model-validation-specialist`

Checks a lego model: all studs connected or stubbed, no duplicate providers, slots filled, units and frequencies consistent, identities verifiable, simultaneous blocks listed.

Arguments: `$ARGUMENTS`

## Purpose
Check that a lego model is wired correctly and that the manifest tells the truth about the code: every stud connected or stubbed, no duplicate providers, every slot filled once, units and frequencies consistent, timing as declared, identities holding numerically, and simultaneous blocks listed. The output is a verdict that blocks release while bricks are unvalidated or stale.

**Use it when** after any change to a lego model, before a forecast round or release, or when results look inconsistent.

**Do not use it when** the brick-level economic validation is needed (`/validate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - A model.lego.json manifest
   - The model code or specification (to compare the declared ports with what is implemented)
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `model-validation-specialist` — primary agent; coordinates the work and integrates results
- `modeling-methodology-specialist` — Chooses methods and architecture across model families, sets code and data standards, and resolves technical trade-offs between traditional, structural and AI approaches
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Workflow
1. Run `python tools/lego.py check <manifest>` and report errors, warnings and notes
2. Compare the manifest with the code: every declared provided variable exists in the code with that unit; no variable crosses a brick boundary without being declared
3. Check timing: lagged joints are really lagged in the code; same-period joints sit in a simultaneous block that the solver handles jointly
4. Check frequencies: each brick on a different frequency has a declared bridge, and the bridge is implemented and tested
5. Check identities: each declared accounting identity holds numerically in a run, not only on paper
   - Recount each brick's elements from its code (`python tools/lego.py elements <manifest> <brick> --from-mod <file>`) and compare with the declared counts; explain any non-square brick and mark constraints verified only after a run confirms them
6. List bricks that are unvalidated or stale and block release until they are validated

## Checkpoints with the user
- After the tool output: review errors before the manifest-to-code comparison

## Common pitfalls
- Trusting the manifest without reading the code
- Undeclared variables passed between bricks through global state
- Identities checked symbolically but not in a run
- Bridges declared but not tested

## Output
`(conversation); optionally validation/<model>/lego-check.md`

The check report lists tool errors and warnings, manifest-to-code findings, timing and frequency results, identity residuals and brick validation status.

## Gate / verdict
- Verdict: PASS / PASS WITH CONDITIONS / FAIL / NOT ASSESSED (if the code is absent, the manifest-to-code comparison is NOT ASSESSED)
- Identity residuals from an actual run are reported
- Declared element counts match the code, or the difference is explained

## Suggested next steps
- `/validate-model`
- `/model-release`
