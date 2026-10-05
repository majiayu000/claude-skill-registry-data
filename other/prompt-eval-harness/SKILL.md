---
name: prompt-eval-harness
description: Build a constrained prompt evaluation harness with rubric, test cases, adversarial cases, prompt variants, scoring, failure analysis, evidence confidence, and final recommendation. Adapted from TerminalSkills prompt-tester; never replaces prompts or governance automatically.
---

# prompt-eval-harness

Source repo: https://github.com/TerminalSkills/skills
Source path: skills/prompt-tester/SKILL.md
Source commit: b12ada7710427e475de9ab5d864562f1ecfb6f62
Local adaptation note: Adapted from a general prompt testing workflow into a governance-safe evaluation harness. It supports structured scoring and recommendations, but does not automatically replace prompts, AGENTS instructions, or production behavior.

## Purpose

Evaluate prompt or instruction variants with explicit evidence rather than preference.

Use for AI feature prompts, agent instructions, review prompts, classification prompts, extraction prompts, or policy wording where output quality must be compared across cases.

## Activation

Use when the user asks to test, compare, score, harden, or evaluate prompts, system prompts, rubrics, agent instructions, or prompt variants.

Do not activate when the user only asks for a simple rewrite and does not need evaluation.

## Required Harness

Create or report:

```text
Evaluation goal:
Rubric:
Test cases:
Adversarial cases:
Prompt variants:
Scoring method:
Results:
Failure analysis:
Final recommendation:
Evidence confidence:
```

Rubric requirements:
- Criteria with weights or priority order.
- Expected output format when relevant.
- Explicit failure conditions.

Test case requirements:
- Normal cases.
- Edge cases.
- Adversarial cases.
- At least one case that tests instruction conflict or ambiguity when relevant.

Scoring requirements:
- Score each variant against the same rubric.
- Track false positives, false negatives, format failures, hallucinations, missing evidence, and brittle behavior when relevant.
- State evidence confidence as High, Medium, or Low with a reason.

## Workflow

1. Define what good output means before comparing variants.
2. Build test cases and adversarial cases.
3. Compare prompt variants against the same cases.
4. Record failures and likely causes.
5. Recommend a winner, a merge, or no-change.
6. Preserve the distinction between evaluation result and implementation approval.

## Forbidden actions

- Do not automatically replace prompts, system prompts, AGENTS instructions, project instructions, or production configs.
- Do not edit AGENTS, update CONTEXT.md, create ADR, publish, deploy, git push, or run setup.
- Do not treat a small eval as proof of production readiness.
- Do not use post-hoc rubric changes to make a preferred prompt win.
- Do not hide failed cases from the final recommendation.

## Stop conditions

Stop or downgrade confidence when:
- The prompt goal is undefined.
- No expected outputs or scoring rubric can be stated.
- The available cases are too few or too homogeneous for a defensible recommendation.
- Running the evaluation would require unavailable models, credentials, private data, or external systems.
- The user asks for prompt replacement but has not explicitly approved implementation.

## Output Pattern

```text
Prompt Eval Harness
Goal:
Rubric:
Cases:
Variants:
Scores:
Failure analysis:
Recommendation:
Implementation status: recommendation only; no prompt replacement performed
Evidence confidence:
```
