---
name: jade-core-evaluator
description: >-
  Classifies JADE migration skills as experimental/candidate/official using reproducible evidence
  from pipeline run artifacts. Use after a complete migration run to assess skill quality.
---

# JADE Skill Matrix Evaluator

## Objective
Classify each pipeline skill as `draft`, `experimental`, `candidate`, or `official` based on run evidence.

## Scoring dimensions
- contract compliance (adherence to SKILL.md constraints)
- reproducibility (deterministic outputs across runs)
- gate pass rate (rule pipeline pass %)
- artifact completeness (all expected files present+valid)
- failure handling quality (graceful degradation on missing data)

## Classification thresholds
- `< 50%` aggregate → `draft`
- `50-69%` → `experimental`
- `70-89%` → `candidate`
- `>= 90%` → `official`

## Inputs
- artifacts from full run (00-run-config.json, 05-rule-queue.json, rule-status.json, per-rule batch artifacts)

## Outputs
- artifacts/10-skill-matrix.json

Use `scripts/evaluate_skills.py` to execute.
