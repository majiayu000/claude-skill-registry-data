---
name: generalization-evaluator
description: Cross-domain evaluation to estimate generality and detect blind spots. Use when asked to assess broad capability, compare models across domains, or identify missing skills.
---

# Generalization Evaluator

Use this skill to measure generality across domains and identify weak coverage.

## Workflow

1) Load a task set (use references/task_set.example.json).
2) Run the task set with a consistent runner.
3) Score pass/fail per task and summarize by domain.
4) Rank gaps by impact.

## Scripts

- Run: python scripts/run_eval.py --tasks references/task_set.example.json --runner ollama --model qwen3:latest

## Output Expectations

- Provide a domain score table and a short summary of weaknesses.
- List the top 3 skill gaps with suggested skill actions.
