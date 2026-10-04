---
name: patpat-skill
description: Create or revise a reusable agent skill with precise triggering, progressive disclosure, and behavioral proof. Use when adding a SKILL.md workflow or changing a skill's routing contract.
---

# Patpat Skill

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [smallest safe change](../patpat-loop/principles/smallest-safe-change.md), and [encode lessons](../patpat-loop/principles/encode-lessons.md). Apply the [skill change playbook](../patpat-loop/playbooks/skill-change.md).

Inspect existing skills, host constraints, and repository conventions before editing. A learn pass must wait for approval and edit existing files only: no new SKILL.md and no *-mode mint. Do not mint a personal `*-mode` skill from learn. Give the skill one distinct responsibility. Make its description discriminate between prompts that should and should not trigger it. Write imperative operational instructions and move detailed procedures into directly linked references only when they reduce entrypoint context.

Reuse repository-native scripts and patterns. Do not depend on undocumented host behavior, duplicate generic model knowledge, or add optional files without an immediate use.

Run structural validation after every change. Apply [`patpat-eval`](../patpat-eval/SKILL.md) when behavior, routing, or a description changes. Do not promote a skill because its prose appears complete.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
