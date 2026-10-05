---
name: legal-diagram-redraw
description: Use for editable redraw of supplied legal diagrams without changing asserted facts from approved user facts and assets; unlike $make-infographic (relationship 0.67), choose this when the stated specialized output and preservation contract are required; choose $make-infographic for its generic final-media contract.
---
# Legal Diagram Redraw

## Catalog

- Display name: Legal Diagram Redraw
- Text category: yes
- Categories: Text
- Status: Planning route only
- Route label: Agent-authored structured brief
- Tone: blue
- Short description: Editable redraw of supplied legal diagrams without changing asserted facts.
## What this skill does

- Freezes the request, approved facts, source assets, constraints, and acceptance checks.
- Produces one structured brief for: editable redraw of supplied legal diagrams without changing asserted facts.
- Preserves user-approved facts and assets; flags unknowns rather than inventing them.

## How to use

Provide the desired outcome, source material, audience, format, fixed facts/assets, and any must-not-change constraints. This Skill plans and validates; it does not claim an unverified provider execution route.

#### Example

```text
Create a editable redraw of supplied legal diagrams without changing asserted facts from my approved source material. Preserve the named facts and clearly identify every assumption.
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
- Downstream use: $make-infographic or another verified Atom selected by Router intent matching
