---
name: tw-refine
description: Refine an existing skill in place with minimal diffs. Trigger when asked to improve a skill's trigger description/frontmatter, workflow text, metadata, scripts/references/assets; also for requests to iterate, refactor, rename, or fix a skill using usage/session-mining evidence (for example from /tw-seq).
---

# Refine

## Overview

Refine a target skill by turning evidence into minimal, validated in-place updates.

## Inputs

- Target skill name or path
- Improvement signals (user feedback, session mining notes, errors, missing steps)
- Constraints (minimal diff, required tooling)

## Example Prompts

- "Refine the docx skill to tighten triggers."
- "Add a small script to the pdf skill."
- "Use session-mining notes to refine the gh skill's workflow."

## Workflow (Double Diamond)

### Discover

- Read the target skill's `SKILL.md` and any `scripts/`, `references/`, or `assets/`.
- Collect evidence from usage: confusion points, missing steps, bad triggers, or stale metadata.
- If no example prompts are provided, synthesize 2-3 realistic prompts that should trigger the skill.

### Define

- Write a one-line problem statement and 2-3 success criteria.
- Choose the smallest change set that addresses the evidence.
- Record explicit constraints (minimal diffs, required tooling).

### Develop

- List candidate updates: frontmatter description, workflow steps, new resources.
- Prefer minimal-incision improvements; only add resources when they are repeatedly reused or required for determinism.

### Deliver

- Implement the chosen changes directly in the target skill.
- Keep SKILL.md frontmatter compliant for the target skill (name/description only unless the skill explicitly needs allowed-tools).
- If adding scripts, run a representative sample to confirm behavior.

## Output Checklist

- Updated `SKILL.md` with accurate triggers and clear workflow
- New or modified resources (scripts/references/assets) if justified
