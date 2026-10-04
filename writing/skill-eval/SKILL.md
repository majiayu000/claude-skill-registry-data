---
name: skill-eval
description: Test a pipeline stage's skill file by running the stage WITH and WITHOUT the skill on the same input, comparing outputs, and proposing skill edits. Ryan Law principle 3 — recursive self-improvement. Run after any board complaint about a stage, and monthly per core stage.
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Skill Eval

Skill files bloat over time, and bloated skills get ignored by the model. Frontier models are often good at a task with a one-line prompt; every rule in a skill must EARN its place by measurably improving output. This skill finds the rules that don't.

## Invocation

```
/skill-eval <stage> "<test keyword>"     # e.g. /skill-eval outline "ai sexting apps"
```

Core stages worth evaluating: `research`, `outline`, `draft`, `quality-check`, `verify-claims`.

## Process

1. **Set up the eval workspace:** `.runs/evals/{stage}-{slug}-{date}/` with `with_skill/` and `without_skill/` subfolders.
2. **Prepare inputs.** The stage's normal inputs must exist for the test keyword (run upstream stages first if missing). Copy them into both subfolders so the two runs see identical inputs.
3. **Run WITH the skill** (Agent dispatch): brief = the stage's normal orchestrator brief, output redirected into `with_skill/`.
4. **Run WITHOUT the skill** (Agent dispatch): brief = a single paragraph stating the goal in plain language (e.g. "Create the best possible outline for an article targeting '<keyword>' using the research dossier at <path>. Output to without_skill/."), with NO reference to the skill file. Same inputs, same output format requirement.
5. **Compare** (Agent dispatch, fresh judge): give the judge both outputs (anonymized as A/B, randomized order), the stage's purpose, and the research dossier. Ask: which is better and why; what specifically did the winner do that the loser didn't; which skill-file rules visibly shaped the better output; which rules appear to have had NO effect.
6. **Propose edits.** Based on the judgment:
   - Rules that drove quality → keep, maybe promote earlier in the file
   - Rules with no visible effect → propose deletion (shorter skills comply better)
   - Failure modes the bare run avoided but the skill run hit → the skill is CAUSING harm there; rewrite that rule
   - Failure modes both runs hit → missing rule; propose an addition (with the concrete example from this eval)
7. **Write the report** to `.runs/evals/{stage}-{slug}-{date}/report.md`: verdict, evidence, proposed skill diff (as a fenced diff block). **Do not auto-apply** — skill edits are reviewed by the operator (or the EO agent under its charter) before landing.

## Output

`.runs/evals/{stage}-{slug}-{date}/report.md` + the two output folders.

## Cadence

- After any board/editor complaint that names a stage.
- Monthly per core stage (rotate one per week).
- After swapping a data provider or example set — the optimal skill changes when the inputs change.
