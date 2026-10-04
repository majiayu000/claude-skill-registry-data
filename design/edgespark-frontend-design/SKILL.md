---
name: edgespark-frontend-design
description: Design and redesign EdgeSpark frontends with distinctive, production-grade visual direction instead of generic AI-looking UI. Use when building or polishing landing pages, marketing sites, dashboards, auth flows, portfolios, product surfaces, or reusable frontend sections in EdgeSpark, especially when the task mentions design quality, aesthetics, typography, color, layout, motion, art direction, or making the UI feel more premium and original.
---

# EdgeSpark Frontend Design

Use this skill to turn safe, average UI into deliberate visual design with strong hierarchy, clearer art direction, and higher content quality.

Consult [design-principles.md](references/design-principles.md) for doctrine, asset strategy, implementation details, and anti-patterns. Load the sections relevant to your task.

## Design Stack

Apply the design standard in layers instead of relying on one vague "make it modern" pass:

1. Start with the base web system: context-first framing, 12-column structure, 8-point spacing, semantic tokens, responsive behavior, and WCAG 2.1 AA contrast.
2. Add the aesthetic lift: softer neutral or premium palettes, asymmetrical composition, dramatic typography contrast, generous whitespace, refined textures, and stronger motion direction.
3. Enforce the anti-generic bans from the reference before shipping.

This layering is what prevents the model from drifting into safe but mediocre frontend output.

## Workflow

### 1. Frame the design

Before touching code, derive:

- user goal
- audience
- primary tasks
- key content types
- success metric
- emotional tone
- one unforgettable visual move
- visual thesis: one sentence describing mood, material, and energy
- content plan: hero, support, detail, final CTA when the task is a landing page or marketing surface
- interaction thesis: 2-3 specific motion ideas that change the feel of the page

Give each section one job, one dominant visual idea, and one primary takeaway or action.

Choose a concrete direction instead of a vague "modern" target. Pick an extreme that fits the product, such as editorial, luxury, industrial, playful, organic, brutalist, or retro-futuristic.
Map a minimal user journey and reflect it in layout, hierarchy, and copy.

### 2. Diagnose weak UI before changing it

For redesign work, inspect the current UI and answer:

- are the colors visually fatiguing, cheap-looking, or too vibrant
- is the layout overly traditional, symmetrical, or monotonous
- what modern design elements are missing
- does the page feel static and need motion to come alive
- what is the current brand positioning and intended emotional experience

### 3. Rebuild from the reference, not from habit

Load only the sections you need from [design-principles.md](references/design-principles.md):

- `Layout And Spacing`
- `Typography`
- `Color`
- `Visual Treatments`
- `Motion And Interaction`
- `Landing Pages`
- `Apps`
- `Content Authenticity`
- `Visual Asset Role`
- `Utility Copy For Product UI`
- `Responsive And Accessibility Baseline`
- `Execution Style`
- `Optimization Order`
- `Anti-Patterns`
- `Litmus Checks`

### 4. Follow the non-negotiables

- Start with composition, not components.
- Prefer CSS animations by default. Use Motion or Framer Motion for React, driven by animation tokens.
- Use intersection observers for scroll-triggered entry rather than ad hoc scroll listeners.
- Default to proactive real-image search for visual surfaces. Use placeholders only in the narrow cases listed in the reference.
- Support token-based light and dark modes when the product needs both.
- Match implementation complexity to the chosen direction instead of flattening every design into the same safe template.

### 5. Validate the finish

- Confirm mobile and desktop behavior.
- Confirm WCAG 2.1 AA contrast and visible interactive states.
- Confirm that motion, typography, color, and imagery all align with the chosen direction.
- Confirm that the result passes the anti-pattern check in the reference.

## EdgeSpark Use

Use this skill for the design layer. Pair it with [building-edgespark-apps](../building-edgespark-apps/SKILL.md) when the task also needs EdgeSpark-specific implementation guidance.
