---
name: prompt-enhancement
description: Prompt engineering and task-specification skill for improving prompts, agent instructions, system messages, evaluation prompts, coding-agent tasks, multi-step workflows, and LLM output reliability. Use when rewriting vague prompts, adding constraints, reducing ambiguity, improving safety, creating reusable prompt templates, or converting goals into actionable agent instructions.
---

# Prompt Enhancement

## Operating Rules

- Preserve the user's intent; do not over-constrain creative or exploratory tasks.
- Separate objective, context, inputs, constraints, output format, and verification criteria.
- Make implicit assumptions explicit when they affect outcome quality.
- Prefer testable instructions over personality-heavy wording.

## Workflow

1. Diagnose the prompt for missing context, ambiguous goals, conflicting constraints, and weak success criteria.
2. Rewrite into a direct task with ordered steps and clear boundaries.
3. Add output format only when structure improves usability.
4. Add examples sparingly; use examples that demonstrate edge cases, not just happy paths.
5. Include a short rationale when the user needs to understand tradeoffs.

## Prompt Template

```text
Objective: <what outcome is required>
Context: <facts, files, audience, constraints>
Inputs: <data the model should use>
Process: <important reasoning or execution steps>
Output: <format, length, tone, artifacts>
Validation: <how to check correctness>
Boundaries: <what to avoid or ask before doing>
```

