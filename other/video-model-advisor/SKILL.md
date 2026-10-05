---
name: video-model-advisor
description: Use for evidence-bounded recommendation among verified video routes from approved user facts and assets; unlike $generate-video (relationship 0.67), choose this when the stated specialized output and preservation contract are required; choose $generate-video for its generic final-media contract.
---
# Video Model Advisor

## Catalog

- Display name: Video Model Advisor
- Text category: yes
- Categories: Text
- Status: Planning route only
- Route label: Agent-authored structured brief
- Tone: blue
- Short description: Evidence-bounded recommendation among verified video routes.

## What this skill does

- Freezes the request, approved facts, source assets, constraints, and acceptance checks.
- Produces one structured brief for: evidence-bounded recommendation among verified video routes.
- Preserves user-approved facts and assets; flags unknowns rather than inventing them.

## How to use

Provide the desired outcome, source material, audience, format, fixed facts/assets, and any must-not-change constraints. This Skill plans and validates; it does not claim an unverified provider execution route.

#### Example

```text
Create a evidence-bounded recommendation among verified video routes from my approved source material. Preserve the named facts and clearly identify every assumption.
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
- Downstream use: $generate-video or another verified Atom selected by Router intent matching
