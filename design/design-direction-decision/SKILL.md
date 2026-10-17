---
name: design-direction-decision
description: Compare two or more design directions and recommend the strongest one using explicit, project-specific criteria. Use when choosing between concepts, layouts, mockups, screenshots, or art-direction proposals without implementing them.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to provided design artifacts, screenshots, documents, or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: designers-frontend-developers-product-teams-and-creative-directors
  tags:
    - design-direction
    - design-decision
    - design-review
    - comparison
    - layout
    - art-direction
    - visual-hierarchy
    - composition
  status: draft
  side_effects: none
---

# Design Direction Decision

## Purpose

Compare viable design directions and make an unambiguous, evidence-led recommendation. Select the direction that best solves the actual communication problem—not the one that is newest, most elaborate, or personally preferred. A controlled hybrid is valid only when one direction remains the clear base.

## When to use this skill

Use this skill when:

- The user asks which of two or more concepts, mockups, screenshots, layouts, or art-direction proposals should move forward.
- A team needs a design decision with rationale, tradeoffs, and a clear record of what to retain or reject.
- Several creative proposals optimize different things, such as product clarity, brand expression, or distinction.
- The user wants to combine the strongest parts of several directions without writing implementation code.

Do not use this skill when:

- There is only one design and the request is for critique or improvement.
- The design problem, audience, or primary message is still too unclear to evaluate alternatives fairly.
- The request is to generate concepts, audit accessibility, run user research, assess technical feasibility, or implement a selected design.
- The alternatives differ only in minor implementation details.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- Two or more distinguishable directions: screenshots, mockups, wireframes, Figma exports, visual references, or written proposals.
- The page or experience purpose, audience, primary message, primary action, desired perception, brand guidance, content requirements, and constraints.
- Relevant copy, content structure, and existing visual language where available.

State assumptions rather than inventing missing context. If the alternatives are too incomplete to distinguish, say exactly what is missing and give a provisional recommendation only when evidence supports one.

## Decision principles

- Reduce uncertainty. Do not conclude that every option is equally good when evidence supports a choice.
- Evaluate each direction against the same criteria, weighted for the actual objective.
- Prefer message clarity, hierarchy, composition, audience fit, and coherent identity over decorative novelty.
- Separate concept strength from execution maturity. A rough direction can have the better underlying idea.
- Keep the recommendation at the design-decision level. Do not write code, edit files, or turn the result into implementation tasks.

## Workflow

1. **Frame the decision.** Name the page, experience, or concept being selected and list neutral labels for each alternative. For example: “A — Editorial Grid,” “B — Product-Led Interface,” and “C — Experimental Spatial.”
2. **Establish the objective.** Record purpose, audience, primary message, primary action, desired perception, content requirements, constraints, and stated assumptions.
3. **Weight the criteria.** Identify a small set of critical criteria and any secondary criteria. Use the default criteria below only when relevant:
   - message clarity and visual hierarchy;
   - visual flow and composition;
   - audience and brand fit;
   - distinction and cohesion;
   - restraint, content compatibility, and conceptual scalability;
   - complexity versus communication value.
4. **Understand each direction on its own terms.** For each alternative, describe its core idea, focal point, composition strategy, visual character, primary strength, and primary risk before judging it.
5. **Compare fairly.** Apply the same weighted criteria to every direction. Use qualitative ratings such as Strong, Good, Mixed, and Weak when a matrix clarifies the decision; do not fabricate numerical precision.
6. **Find decisive differences.** Focus on differences that materially affect the objective. Eliminate options that fail a non-negotiable requirement rather than spending equal attention on them.
7. **Set non-negotiables.** State the properties the final direction must preserve, such as immediate product clarity, one dominant CTA, asymmetric composition, or a strong typographic identity.
8. **Choose a primary direction.** State one recommendation. For a hybrid, name one dominant base and borrow only one to three specific ideas that reinforce it; name the ideas that must not carry forward.
9. **Explain the tradeoff.** Say why the winning direction best serves the critical criteria and what its limitations are. If two directions optimize different goals, surface the strategic choice directly.
10. **Define the selected direction.** End with a concise, non-implementation design-direction statement that can guide later work.

## Comparison methods

Use the lightest method that produces a confident result:

- **Direct comparison:** for two clearly distinct directions; compare only the criteria that decide the choice.
- **Qualitative matrix:** for three or more developed alternatives; use it to organize evidence, not to manufacture an objective score.
- **Elimination:** when an option conflicts with a clear non-negotiable.
- **Base plus borrow:** when one direction has the strongest structure and another offers one or two compatible, exceptional ideas.

## Hybrid and confidence rules

A hybrid must have one dominant parent direction and one to three explicitly defined borrowed ideas. Do not recommend taking layout, typography, colors, imagery, navigation, and motion from different directions without proving they share a visual logic.

Use confidence when it adds decision value:

- **High:** the objective and alternatives are clear, and one performs materially better.
- **Medium:** two directions are close or the recommendation depends on stated assumptions.
- **Low:** important content or direction detail is missing. Explain the uncertainty, then make a provisional choice if possible.

## Output format

Return:

```md
# Design Direction Decision

## Recommendation

**Choose:** Direction B — <name>
**Confidence:** High | Medium | Low

<Two to four sentences explaining the decision.>

## Decision context

- **Purpose:** ...
- **Audience:** ...
- **Primary message:** ...
- **Primary action:** ...
- **Desired perception:** ...
- **Assumptions:** ...

## What matters most

**Critical criteria:** ...
**Secondary criteria:** ...

## Directions

### A — <name>

- **Core idea:** ...
- **Primary strength:** ...
- **Primary risk:** ...

<Repeat for each direction.>

## Comparison

| Criterion | A | B | C |
|---|---|---|---|
| <critical criterion> | ... | ... | ... |

## Why the recommendation wins

1. ...
2. ...
3. ...

## Tradeoffs

- Choosing this direction means accepting: ...
- This is preferable because: ...

## Preserve, borrow, and reject

- **Preserve:** ...
- **Borrow selectively:** ...
- **Do not carry forward:** ...

## Final direction

> <One to three sentences defining the chosen design direction.>

## Next design questions

1. ...
```

For a simple two-option choice, omit the matrix and use concise sections for why each option is stronger, what to retain, what to avoid, and the final direction.

## Quality bar

The task is complete only when:

- At least two directions were compared.
- The objective is explicit or assumptions are clearly labeled.
- The decisive criteria are appropriate to the project and consistently applied.
- The primary recommendation is unambiguous and supported by evidence.
- Major tradeoffs are acknowledged.
- Useful ideas from losing directions are preserved selectively, while incompatible ideas are explicitly rejected.
- A hybrid has one dominant parent direction.
- The final direction is concise, actionable for later design work, and contains no implementation code.

## Edge cases

- **Very similar directions:** focus on material differences in message, hierarchy, flow, identity, or scalability; do not manufacture distinctions.
- **Uneven polish:** assess concept strength separately from execution maturity.
- **Different strategic goals:** state the conditional choice (for example, A for brand distinction; B for immediate product comprehension) and recommend the best fit for the stated brief.
- **No clear winner:** identify the unresolved question, explain how each answer would change the decision, and provide the best current provisional recommendation.
- **Accessibility or feasibility concern:** record the design-level risk and recommend a dedicated accessibility or technical review when it could affect the decision; do not perform either specialist review here.

## Related skills

- `ui-design-direction-builder` — creates a coherent direction before alternatives exist.
- `layout-art-direction` — reviews or develops the composition of a specific layout.
- `editorial-digital-designer` — explores editorial composition and typographic systems.
- `experimental-web-art-director` — develops bold concepts within usability and feasibility constraints.
- `creative-technologist` — evaluates feasibility of ambitious browser experiences.
