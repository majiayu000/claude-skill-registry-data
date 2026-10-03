---
name: bmad-method
description: Use when the user needs help choosing, sequencing, or running Compass BMAD skills across planning, docs, solutioning, implementation, or polyrepo routing.
---

# BMAD Method

## When to Use

Use this skill when the user:

- asks what BMAD skill or workflow to run next
- wants to move between roadmap, phase, and implementation work
- needs workspace or polyrepo routing guidance
- wants to understand how planning, docs, and BMAD fit together

## Instructions

1. Start with `_bmad/BMAD-workflow.md` for the high-level flow.
2. Use `_bmad/_config/skill-manifest.csv` plus `references/command-catalog.md` to choose the correct skill.
3. Distinguish workspace coordination from repo-local delivery before recommending a skill.
4. Prefer the smallest skill that moves the user forward without skipping required gates.
5. When routing is ambiguous, recommend `/bmad-help` or the exact BMAD skill that fits the current phase.
6. Skills are auto-generated from the `_bmad/` skill tree at build time; the skill manifest is the source of truth for available skills.

## References

- Read `references/command-catalog.md` when you need the current shipped skill surface.
- Read `_bmad/tools/automation/README.md` only if the user asks for automation or orchestration.
