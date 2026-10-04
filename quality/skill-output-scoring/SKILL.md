---
name: skill-output-scoring
description: Score agent skill outputs with a rubric. Use when Codex is asked to evaluate a skill output, compare outputs, apply a quality rubric, summarize reviewer scoring, or decide whether a skill output is good enough to promote.
license: MIT
---

# Skill Output Scoring

## Core Workflow

1. Identify the output, scenario, target artifact, and scoring rubric.
2. Score each criterion with brief evidence, not just a number.
3. Separate output quality from prompt quality and missing context.
4. Call out blockers before averages.
5. Compare baseline and skill-enabled scores when both exist.
6. Recommend keep, revise, split, merge, defer, or retire based on the score and
   risks.

## Safety Rules

- Do not average away high-risk failures.
- Do not treat polished writing as correctness.
- Do not score claims as correct without evidence or source material.
- Escalate when the output affects production, security, legal, finance,
  employment, medical, compliance, or customer commitments.

## Deliverable Shape

For scoring reports, provide:

- Scenario and artifact
- Rubric used
- Score table
- Blockers
- Improvements and regressions
- Confidence level
- Decision recommendation

## References

- Read `references/skill-output-scoring-checklist.md` when scoring or comparing
  agent skill outputs.
