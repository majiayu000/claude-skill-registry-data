---
name: jira-spike
description: "Create or refine Jira Spike tickets in Jira Markup. Use when the user wants a Spike, research ticket, investigation ticket, technical exploration, discovery work, research question, or SDD-ready Spike input."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# Jira Spike

## Scope

Use this skill only to generate Jira Spike ticket content. A Spike is research work that answers a question, explores uncertainty, and produces evidence for a later decision.

This skill outputs Jira Markup in chat only. It does not create Jira issues through the Jira API.

## Operating Rules

- Quick Creation is the default mode.
- Refinement activates only when explicitly requested by the user.
- SDD-ready is a variant of Refinement, not a third mode.
- Do not ask for Jira ticket type.
- Do not mention sibling skills or suggest alternatives.
- Trust that the selected skill type is intentional.
- Follow the user's language during conversation.
- Generate the final Jira ticket in English by default unless the user explicitly requests another artifact language.
- Final ticket must be a single Jira Markup code block.
- Omit empty sections and placeholders.
- Use `Assumptions and TBD` only for real unresolved non-blocking gaps.
- Quick Creation may ask only when missing information blocks Title, Description, or Objective.
- Quick Creation blocking questions must be direct interrogative questions ending with `?` or using Spanish `¿...?` when the conversation language is Spanish.
- In Quick Creation, include Acceptance Criteria or Implementation Notes only if the user explicitly provided useful content for those sections.
- Refinement asks one question at a time, waits for the user, and does not generate until an explicit generation request.
- Ask open-ended Quick Creation and Refinement questions directly in normal chat. Add `Recommendation: ...` only when it helps the user respond.
- Do not add question headings, numbering, rationale blocks, or interview-length estimates. Use the `question` tool only for a closed confirmation or enumerated choice.
- If refining an existing ticket, preserve useful existing content and improve only missing/unclear parts.
- When refining an existing ticket, include a brief change summary before the final ticket, outside the Jira block.
- Codebase exploration applies only to Refinement / SDD-ready when it can answer factual questions or validate assumptions; not to Quick Creation by default unless explicitly requested.
- Codebase exploration is light by default (search/read a few relevant files); deep exploration requires explicit confirmation.
- Evidence Summary is required before the Jira block when exploration happened or the output makes technical/factual claims. It must include Reviewed, Found, Evidence, Confidence, Unverified. Confidence levels: High, Medium, Low.
- These skills only generate Jira Markup content; they do not create Jira issues through the Jira API.

## Modes

### Quick Creation

Use Quick Creation unless the user explicitly asks for refinement. Load `assets/quick-creation-template.md` before generating.

Generate directly when the user provided enough information for:

- Title
- Description
- Objective

Ask only one blocking question if any of those three cannot be inferred safely. Keep the lead-in minimal before the Jira block.

### Refinement

Use Refinement only when the user explicitly asks to refine, improve, complete, add detail, clarify, make developer-ready, add acceptance criteria, or equivalent Spanish intent such as refinar, mejorar, completar, agregar detalle, hacer mas claro, dejar listo para dev, or anadir criterios de aceptacion.

Use SDD-ready Refinement when the user explicitly asks for listo para SDD, preparalo para SDD, para usarlo en SDD, SDD-ready, ready for SDD, prepare for SDD, as SDD input, or equivalent phrasing.

Load `assets/refinement-template.md` before generating. Ask one question at a time using this minimal shape:

```markdown
[Direct interrogative question?]

Recommendation: [Short suggested answer when useful.]
```

Omit the recommendation line when it adds no value.

Do not generate until the user explicitly asks to generate, create, print, or finalize the ticket.

## Spike Refinement Guidance

Required refined sections:

- Title
- Research Question
- Context
- Scope
- Expected Deliverable

Optional refined sections:

- Acceptance Criteria
- Implementation Notes
- Test Notes
- Open Questions
- Assumptions and TBD

Acceptance Criteria should be evidence or deliverable bullets by default. Use Given/When/Then only when it fits naturally.

Implementation Notes must stay investigatory: areas to inspect, constraints, known risks, dependencies, or SDD inputs. They must not assume the solution, prescribe architecture, list subtasks, or become a step-by-step build plan.

Open Questions are especially useful for SDD-ready output when unresolved decisions affect scope, design, or acceptance.

## Evidence Summary

When required, place this before the Jira block:

Evidence Summary
Reviewed: Files, docs, or sources reviewed.
Found: Facts discovered.
Evidence: Specific references.
Confidence: High | Medium | Low
Unverified: Claims or assumptions not validated.

If no exploration happened and no technical or factual claims are made, omit the Evidence Summary.
