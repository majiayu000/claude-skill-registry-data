---
name: safe-learning-governance
description: Use when a user asks an AI agent to learn, improve continuously, capture repeated mistakes, update rubrics, promote lessons, review stale rules, or build a self-improvement loop without broad memory rewrites.
---

# Safe Learning Governance

Improve from evidence without turning every observation into a permanent rule.

## Evidence Tiers

- `observation`: one event or screenshot.
- `pattern`: repeated evidence across runs or tasks.
- `lesson`: validated pattern with scope and counterexamples.
- `stable rule`: only after repeated success and explicit promotion.

## Learning Steps

1. Record the evidence.
2. Identify the failure or improvement pattern.
3. Check for counterexamples.
4. Define scope.
5. Propose a lesson.
6. Verify on a future task before promoting.

## Stop Rules

Stop before broad memory rewrite, deleting old lessons, overriding project truth, or changing runtime behavior from a lesson alone.

## Output

Return:

- evidence;
- pattern;
- proposed lesson;
- confidence;
- scope limit;
- next verification.
