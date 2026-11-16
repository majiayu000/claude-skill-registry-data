---
name: skill-authoring
description: Create a portable Agent Skill with clear activation criteria and a focused procedure. Use when adding or revising a SKILL.md in this collection or another compatible library.
---

# Skill Authoring

A skill should encode a repeatable capability, not restate generic assistant behavior.

1. Define one task, its user value, activation triggers, and cases where it should not run.
2. Read the target Agent Skills specification and the host's skill-discovery rules.
3. Write concise YAML frontmatter with a unique lowercase hyphenated `name` matching the folder and a specific `description` explaining when to use it.
4. Structure the body as an operational workflow: inputs, steps, decision points, outputs, safety limits, and definition of done.
5. Use progressive disclosure. Put only essential instructions in `SKILL.md`; move substantial references, examples, or scripts into clearly named subfolders.
6. Avoid hidden dependencies, broad permissions, unbounded network activity, and instructions to bypass safety controls.
7. Add positive and negative trigger examples and a validation/evaluation plan.
8. Check overlap with existing skills before adding another.

Write for multiple compatible agents; do not assume a vendor-specific tool exists. Attribute adapted material and verify the license of each upstream file. Do not copy whole skills or introduce generated project clutter.
