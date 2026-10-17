---
name: design-review-orchestrator
description: Routes a non-coding design review through the smallest useful sequence of framing, critique, exploration, specialist perspectives, and direction selection. Use when a broad or uncertain design request needs one coherent recommendation rather than implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to supplied briefs, screenshots, design artifacts, and related skills or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: designers-frontend-developers-product-teams-and-creative-directors
  tags:
    - design-review
    - orchestration
    - design-direction
    - design-strategy
    - layout
    - creative-direction
    - decision-making
  status: draft
  side_effects: none
---

# Design Review Orchestrator

## Purpose

Turn a broad, vague, or contested design request into a proportionate review process and one defensible design recommendation. Select only the skills and stages that add decision value; do not turn the review into code or an implementation plan.

## When to use this skill

Use this skill when:

- A user asks for a comprehensive design review, redesign process, design workshop, or coordinated use of design skills.
- An existing page, mockup, or concept feels generic, weak, unclear, or difficult to improve decisively.
- Several perspectives or alternatives need to be reconciled into one direction.
- The user is unsure whether the work needs framing, critique, exploration, or a decision.

Do not use this skill when:

- One focused request is already covered by a specialist skill, such as a layout critique or a decision between developed directions.
- The user wants frontend implementation, CSS, technical architecture, a dedicated accessibility audit, or copywriting.
- There is no design question beyond a small local correction.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- The request, desired outcome, audience, primary message or action, constraints, and stated preferences.
- Existing screenshots, mockups, wireframes, reference sites, design-system guidance, content, or repository evidence.
- Existing candidate directions and prior review notes.

State consequential assumptions. Do not invent brand, audience, or business objectives that would change the recommendation.

## Workflow

1. **Diagnose the decision.** Determine whether the main need is framing, critique, exploration, a specialist lens, comparison, or a combination. Identify the decision the process must enable.
2. **Select the smallest route.** Use the patterns below as guides, skipping stages that would only repeat settled work:
   - Unclear brief or purpose: `design-problem-framer`.
   - Existing composition with a known concern: `layout-principles-review`.
   - No viable alternatives: `layout-direction-explorer`.
   - Two or more developed alternatives: `design-direction-decision`.
3. **Add specialist perspectives only for a material tension.** Choose at most the lenses that answer an unresolved question:
   - distinctiveness or a predictable concept: `provocative-concept-director`;
   - typography, rhythm, or content-heavy composition: `editorial-digital-designer`;
   - signal reduction, restraint, or identity coherence: `minimalist-brand-director`;
   - offer clarity, trust, or calls to action: `conversion-creative-director`;
   - time, feedback, or experiential pacing: `motion-experience-director`;
   - an ambitious interaction whose feasibility affects the direction: `creative-technologist`.
4. **Keep perspectives independent.** Give each selected specialist the same design frame and evidence. Record its unique insight, tradeoff, and any assumption; do not present separate personas as a final answer.
5. **Challenge and converge.** Compare the viable directions against purpose, audience, message clarity, hierarchy, fit, distinctiveness, and constraints. Separate a strong concept from a polished execution. If a tradeoff remains unresolved, name it rather than averaging conflicting advice.
6. **Choose and bound the recommendation.** Recommend one primary direction. A hybrid is valid only when it has a clear base and one to three reinforcing elements borrowed from another direction. State what to preserve, change, reject, and investigate next.
7. **Stop before implementation.** Return a design decision or a clear next design workflow. Do not write code, create files, modify tokens, or create an implementation backlog unless separately requested.

## Orchestration rules

- Move from understanding to exploration only when the design frame is sufficient to judge alternatives.
- Critique an existing design before replacing it; preserve elements that serve the objective.
- Use divergence to create meaningfully different options, not cosmetic variations.
- Do not call every available specialist or extend the process after a clear winner emerges.
- When related skills are unavailable, apply the relevant reasoning directly and disclose that no separate skill was invoked.
- Treat accessibility, responsiveness, and feasibility as constraints when they affect the direction, but route detailed audits or technical planning to their dedicated workflows.

## Output format

Return:

```md
# Design Review

## Current state

- **Decision needed:** ...
- **Evidence reviewed:** ...
- **Assumptions:** ...

## Workflow selected

1. <skill or analytical stage> — <why it is needed>
2. ...

## Diagnosis

- **What works:** ...
- **Main problems:** ...
- **Decisive constraints:** ...

## Specialist perspectives

- **<lens>:** <unique insight and tradeoff>

## Directions considered

- **A — <name>:** <strength and risk>
- **B — <name>:** <strength and risk>

## Recommendation

**Choose:** <primary direction>
**Confidence:** High | Medium | Low

<Why this direction best meets the decision criteria.>

## Preserve, change, and avoid

- **Preserve:** ...
- **Change:** ...
- **Avoid:** ...

## Remaining design questions

1. ...

## Next phase

<The next design workflow, or state that the decision is ready for separate implementation planning.>
```

For a small request, use a compact version containing the diagnosis, selected route, recommendation, preserve/change/avoid guidance, and next phase.

## Quality bar

The task is complete only when:

- The selected workflow is proportional to the uncertainty and impact of the decision.
- Each included specialist or stage has a distinct purpose.
- The recommendation is singular, evidence-led, and explicit about tradeoffs and uncertainty.
- The result distinguishes reviewed evidence from assumptions and does not claim unavailable skills were invoked.
- The response ends with a design decision or a justified next design step, not an open-ended list of ideas or implementation work.

## Edge cases

- **One existing design, no stated goal:** frame the problem first; give only provisional critique where the objective is unknown.
- **Several screenshots:** compare only those solving the same problem; separate unrelated concepts before deciding.
- **Strong disagreement:** expose the strategic choice and weight it against the project objective rather than averaging perspectives.
- **Reference sites:** extract transferable principles, not a derivative visual recipe.
- **Accessibility or technical risk:** flag the design-level implication and recommend the appropriate dedicated review; do not present it as a completed audit.

## Related skills

- `design-problem-framer`
- `layout-principles-review`
- `layout-direction-explorer`
- `design-direction-decision`
- `creative-direction-orchestrator`
- `provocative-concept-director`
- `editorial-digital-designer`
- `minimalist-brand-director`
- `conversion-creative-director`
- `motion-experience-director`
- `creative-technologist`
