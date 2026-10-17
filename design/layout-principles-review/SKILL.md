---
name: layout-principles-review
description: Reviews an existing layout, mockup, screenshot, wireframe, or described design direction through emphasis, contrast, balance, hierarchy, alignment, repetition, and flow. Use when a design feels weak, confusing, busy, flat, or unbalanced and the user wants design-level recommendations without implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to provided design artifacts, screenshots, documents, or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: designers-frontend-developers-and-product-teams
  tags:
    - layout
    - design-review
    - visual-hierarchy
    - emphasis
    - contrast
    - balance
    - alignment
    - repetition
    - flow
    - composition
  status: draft
  side_effects: none
---

# Layout Principles Review

## Purpose

Review a visual layout as a composition: whether it communicates its message, establishes an intentional focal point, distributes visual weight deliberately, and guides attention through content in a useful order. Explain the evidence and recommend design-level changes; do not implement them.

## When to use this skill

Use this skill when:

- The user asks to critique a page, interface, dashboard, article, portfolio, landing page, mockup, screenshot, or wireframe.
- A design feels busy, generic, weak, flat, confusing, or unbalanced.
- The user wants to assess hierarchy, focal points, visual flow, composition, or the relative emphasis of elements.
- The user wants recommendations before implementation, without CSS or component code.

Do not use this skill when:

- The user primarily wants fresh concepts or several alternative compositions; use a design-direction skill.
- The primary task is implementation, accessibility compliance, usability research, conversion optimization, or motion-system design.
- There is no existing or described composition to review.

## Inputs to inspect

Inspect the smallest useful set of available evidence:

- Screenshot, rendered page, mockup, wireframe, Figma export, PDF, or design specification.
- Page purpose, audience, primary message, primary action, and content priorities.
- Multiple variants, when the user wants a comparison.
- Relevant copy or component structure only when it affects visual hierarchy.

Prioritize direct visual evidence. If only a written concept is available, label observations as inferred risks rather than observed defects. Do not assume unseen interactions.

## Review principles

Assess only the principles that yield useful findings. State when a principle is working well.

| Principle | Review question |
|---|---|
| Emphasis | What attracts attention first, and should it? |
| Contrast | Are meaningful differences visible without making everything loud? |
| Hierarchy | Does visual importance match content importance and reading order? |
| Balance | Is visual weight deliberately distributed, including whitespace? |
| Alignment | Do shared anchors create intentional relationships and order? |
| Repetition | Do recurring treatments create cohesion without flattening hierarchy? |
| Flow | Does attention move through the intended message, proof, and action? |

Consider scale, value, color, position, imagery, density, isolation, whitespace, grouping, shape, and directional cues together. A small high-contrast element can outweigh a much larger quiet one.

## Workflow

1. Establish the design objective from supplied context. Record the purpose, audience, primary message, primary action, and any assumptions. Do not invent business goals.
2. Identify the intended focal point and the observed focal point. Explain the evidence behind the observed result; a mismatch is usually a high-value finding.
3. Trace the likely visual path—for example, headline → image → supporting proof → action—and compare it with the desired communication order. Identify skipped information, dead ends, and competing elements.
4. Review emphasis, contrast, hierarchy, balance, alignment, repetition, and flow where relevant. Diagnose before prescribing: observation → effect → recommendation.
5. Identify interactions and tradeoffs between principles, such as strong consistency that weakens hierarchy or expressive asymmetry that remains balanced.
6. Separate what to preserve from what to change. Do not turn a review into an unnecessary redesign.
7. Prioritize findings:
   - **High:** primary message, focal point, major hierarchy, flow, comprehension, primary action, or severe imbalance.
   - **Medium:** section hierarchy, alignment, rhythm, repetition, consistency, or secondary emphasis.
   - **Low:** polish, subtle spacing relationships, minor rhythm, or decorative consistency.
8. Recommend changes at the design level. Explain what should be more or less prominent, separated, aligned, repeated, restrained, or removed—and why. Prefer reducing competing treatments before adding new ones.
9. Conclude with the three-question test: does the layout attract, work, and organize?

## Review rules

- Tie each critique to visible or supplied evidence, not personal taste.
- Do not equate symmetry with balance; judge visual weight, including whitespace.
- Do not equate consistency with hierarchy; intentional deviations can create emphasis.
- Do not maximize every principle. Contrast, whitespace, scale, color, and repetition must support communication.
- Preserve intentional experimental or expressive choices when the message remains recoverable.
- For highly minimal layouts, treat empty space as an active choice rather than a gap to fill.
- Mention obvious visual accessibility concerns only when they materially affect composition. Route detailed WCAG, semantic, keyboard, ARIA, or focus review to a dedicated accessibility skill.
- If motion is central to the supplied design, note its effect on attention and sequence, but do not design or implement a motion system.
- Do not provide CSS values, utility classes, component code, or implementation instructions.

## Input-specific guidance

### Screenshot or rendered page

Use direct visual evidence. Review focal point, weight, hierarchy, alignment, whitespace, repetition, section transitions, and flow. Do not infer hidden states or interactions.

### Wireframe

Focus on structure, grouping, sequence, emphasis, balance, and flow. Do not over-critique visual styling that has not been designed.

### Described layout

Use conditional language such as “this direction risks” or “if these elements receive equal visual weight.” Clearly distinguish the stated concept from any inferred risk.

### Multiple variants

Apply the same principles to each. Identify the strongest hierarchy, flow, composition, message communication, distinctiveness, and restraint; then make a reasoned recommendation if the user asks for one.

## Output format

Return:

```md
# Layout Review

## Verdict

**Overall:** Strong / Strong with refinements / Promising but structurally unclear / Needs hierarchy revision / Needs composition revision / Needs fundamental rethink

<Brief evidence-led summary.>

## Design objective

- **Purpose:** ...
- **Primary message:** ...
- **Primary action:** ...
- **Audience:** ...
- **Assumptions:** ...

## Focal point and visual pathway

- **Intended focal point:** ...
- **Observed focal point:** ...
- **Assessment:** Match / Partial / Conflict
- **Likely path:** 1. ... 2. ... 3. ...

## What already works

- ...

## Findings

### <Finding title>

**Priority:** High / Medium / Low  
**Principles:** ...

**Observation:** ...

**Effect:** ...

**Recommendation:** ...

## Principle review

| Principle | Assessment | Main observation |
|---|---|---|
| Emphasis | Strong / Mixed / Weak | ... |
| Contrast | Strong / Mixed / Weak | ... |
| Hierarchy | Strong / Mixed / Weak | ... |
| Balance | Strong / Mixed / Weak | ... |
| Alignment | Strong / Mixed / Weak | ... |
| Repetition | Strong / Mixed / Weak | ... |
| Flow | Strong / Mixed / Weak | ... |

## Keep / Change / Avoid

### Keep

- ...

### Change

- ...

### Avoid

- ...

## Priority actions

1. ...
2. ...
3. ...

## Final test

- **Does it attract?** Yes / Partially / No — ...
- **Does it work?** Yes / Partially / No — ...
- **Does it organize?** Yes / Partially / No — ...
```

## Quality bar

The review is complete only when:

- The objective is identified or assumptions are explicit.
- The actual or likely focal point and visual path are considered.
- Findings cite evidence, affected principles, and a reasoned design-level recommendation.
- Successful decisions are preserved alongside problems.
- Findings are prioritized without inflating aesthetic preferences into critical defects.
- The conclusion evaluates whether the layout attracts, works, and organizes.
- The response contains no implementation code or unsupported claims about user goals.

## Related skills

- `layout-art-direction` for a broader art-direction plan or implementation-aware composition work.
- `editorial-digital-designer` for an expressive editorial layout direction.
- `conversion-creative-director` when persuasion and commercial action are central.
- `motion-experience-director` when motion is part of the visual experience.
- `visual-responsive-accessibility-audit` for a detailed accessibility and responsive review.
