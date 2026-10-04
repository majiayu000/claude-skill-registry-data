---
name: byte-review
description: Review a product, implementation, plan, or deliverable for material issues and readiness. Use when the user asks for review, audit, critique, quality assessment, or what should change next.
---

# Byte Review

Review the actual artifact and evidence. Choose review dimensions based on what
could realistically make the result wrong, harmful, confusing, or incomplete.

## Method

- Establish the intended behavior and scope.
- Check relevant active lessons for repeated mistakes.
- Inspect relevant code, files, runtime behavior, tests, or sources.
- Prioritize concrete findings by impact and confidence.
- Distinguish confirmed defects from risks, preferences, and missing evidence.
- Recommend changes that materially improve the outcome.

Possible lenses include product fit, UX, correctness, architecture,
maintainability, security, privacy, performance, testing, market evidence, and
delivery readiness. Do not simulate a meeting or force every role to comment.

For code review, lead with actionable findings tied to precise locations. For a
product review, lead with the decision or highest-impact gap. If there are no
material findings, say so and note meaningful verification limits.

Write a review artifact only when it will be tracked or used for later iteration.
Do not require a verdict schema, a fixed number of findings, or a Byte OS state
transition.

When review evidence confirms a reusable mistake, false completion claim, or
requirement misunderstanding, update the matching `.byte-os/LESSONS.md` entry
with evidence and a prevention rule, not blame.

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
