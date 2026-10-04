---
name: skill-update
description: "Upgrade an existing Codex skill through a structured loop: inspect, compare, improve, validate, test, and finalize with evidence for future reuse."
---

# Skill Update

Use this skill when a current skill is good enough to be useful but not good enough for the task in front of you.

The goal is not to rewrite for style. The goal is to increase task performance, preserve what already works, and leave behind a better reusable skill.

## When to use

Use when:
- a named skill exists but lacks context the task clearly needs
- a skill solves part of the problem but misses important workflow steps
- a skill has stale assumptions, weak validation, or poor output structure
- repeated work suggests the skill should be improved instead of worked around again

Do not use when:
- there is no existing skill to update
- the change is only cosmetic
- the task is faster to solve directly than to improve the skill

## Inputs

Gather these before editing:
- target skill path
- current user task
- observed gap or failure mode
- one or more reference sources that should improve the skill
- validation method for the updated skill

## Core workflow

1. Inspect the old skill.
Read the target `SKILL.md` and only the minimum linked references or scripts needed to understand how it currently works.

2. Compare it against the real task.
Write down where the current skill helps, where it is incomplete, and what future tasks of the same kind would still fail.

3. Build an improvement delta.
Decide what to keep, what to tighten, what to delete, and what new references or scripts should be added.

4. Update the skill.
Improve the `SKILL.md` first. Add or update `references/`, `scripts/`, or `assets/` only when they materially improve execution.

5. Validate before finalizing.
Run the local skill validator. If the skill adds executable workflow pieces, run a small task-focused smoke check that proves the updated instructions are usable.

6. Compare old versus new.
Use the self-improvement loop and synthesis mindset:
- what did the old skill do
- what does the new skill do better
- what task class does this now cover that it did not cover before

7. Finalize with evidence.
Leave behind:
- the updated skill
- a short change summary
- the validation result
- any rollback note if the skill was narrowed or re-scoped

## Required outputs

Always produce these artifacts in your working notes or final report:
- target skill updated
- reason for the update
- validation evidence
- old vs new capability summary
- future reuse note

## Quality bar

A good skill update:
- keeps the original skill recognizable
- improves execution on the present task
- reduces future ambiguity
- avoids bloating the skill with general advice
- includes a real validation step, not just confidence

## Composition guidance

When useful, combine this skill with:
- `scbe-self-improvement-skill-management` for approval, validation, and documentation discipline
- `skill-synthesis` for comparing the target skill against adjacent skills and borrowing only the parts that actually help

## Minimal update template

Use this checklist each time:
- identify the task gap
- inspect the current skill
- inspect one or two high-value references
- patch the skill
- validate the skill
- summarize the delta

Do not finalize a skill update without validation.
