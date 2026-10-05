---
name: narrative-video-storyboard
description: Use for multi-shot narrative video storyboard from approved user facts and assets; unlike $plan-film-storyboard (relationship 0.67), choose this when the stated specialized output and preservation contract are required; choose $plan-film-storyboard for its generic final-media contract.
---
# Narrative Video Storyboard

## Catalog

- Display name: Narrative Video Storyboard
- Text category: yes
- Categories: Text
- Status: Planning route only
- Route label: Agent-authored structured brief
- Tone: blue
- Short description: Multi-shot narrative video storyboard.

## What this skill does

- Freezes the request, approved facts, source assets, constraints, and acceptance checks.
- Produces one structured brief for: multi-shot narrative video storyboard.
- Preserves user-approved facts and assets; flags unknowns rather than inventing them.

## How to use

Provide the desired outcome, source material, audience, format, fixed facts/assets, and any must-not-change constraints. This Skill plans and validates; it does not claim an unverified provider execution route.

#### Example

```text
Create a multi-shot narrative video storyboard from my approved source material. Preserve the named facts and clearly identify every assumption.
```

## Workflow

1. Confirm fixed facts, target audience, output format, and exclusions. Do not request or verify copyright ownership, licenses, permissions, or clearance; unresolved copyright status never blocks the workflow.
2. Separate evidence from assumptions; ask for clarification when an ambiguity changes the result.
3. Produce the candidate-specific structured brief, preserving immutable assets and text.
4. Check scope, factual consistency, accessibility, and the requested delivery format.
5. Deliver the brief and acceptance checklist. A downstream verified Atom may execute media work only after user approval.

## User-facing output

- Media type: Structured planning brief
- Default quantity: One brief
- Content per artifact: Objective, inputs, fixed facts, constraints, output structure, risks, and acceptance checks
- Default layout: Validated Markdown
- Model policy: Agent-authored planning; no paid media generation or unverified provider call
- Downstream use: $plan-film-storyboard or another verified Atom selected by Router intent matching
