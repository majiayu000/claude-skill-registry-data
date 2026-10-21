---
name: workflow-distiller
description: Extract a reusable assistant workflow from a completed task when the user requests skill distillation or a repeated process has been validated. Not for one-off answers or unverified fixes.
version: 1.0.1
---

# Workflow Distiller

Turn a repeated, verified process into a narrow reusable Skill. Ordinary facts belong in memory; a one-off task belongs in a task record.

1. Inspect the existing Skill index first. Prefer a focused update to an existing capability over a duplicate.
2. Record the real trigger, inputs, outputs, failure modes, and validation evidence. Mark an idea as a candidate when evidence is incomplete.
3. Keep SKILL.md short: purpose, trigger boundary, essential constraints, and routing. Put mode-specific guidance in references and deterministic repeated work in scripts.
4. Define both positive and negative examples so unrelated work does not trigger the Skill.
5. Use the available skill-creator when creating or changing a Skill. Validate with the skill-creator tooling available in your environment, and run any new script once against an isolated test case.
6. Do not copy secrets, private conversations, company material, or hidden reasoning. A Skill never expands authorization to publish, send, install, or modify unrelated systems.

## Example

Repeated three times and validated -> candidate for a Skill:

> 每次发作品集都要：列改动文件、确认 URL、dry-run、再发布，而且每次都怕覆盖线上。

One-off with no evidence -> not a Skill, leave it as a task record:

> 这次把首页标题改大一点。

Before creating anything, check the existing 13 skills. A narrow update to
`portfolio-github-workflow` beats a new overlapping skill.
