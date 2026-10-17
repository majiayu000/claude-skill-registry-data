---
name: ux-ui-design
description: Design user flows and interfaces — tokens, component specs, states, and accessibility — before implementation.
version: 1
triggers: ux, ui design, design tokens, user flows, interface design, accessibility design
category: Engineering & code
blurb: Design user flows and interfaces — tokens, component specs, states and accessibility — before building.
archetype: knowledge
example: Design the flow and screens for this feature.
---

# UX / UI Design — the designer seat

Design the experience: flows, visual system, and every control's states. Output is implementation-ready specs, not mood boards.

## When to use
- Any user-facing page, app, dashboard, or tool.
- Redesigns, new flows, or new components.
- Usability/accessibility review passes.

## Method
1. **Flows first**: primary journeys as step diagrams; each step carries one intent.
2. **Information hierarchy**: primary/secondary/tertiary per screen; content before decoration.
3. **Design tokens**: color, type scale, spacing, radius, elevation — single source (`tokens.css` or JSON).
4. **Component inventory**: inputs, buttons, cards, tables, nav, lists — each with purpose, variants, and **all states**: default / hover / active / disabled / focus / loading / error.
5. **Accessibility**: WCAG AA contrast, keyboard reachable, labels on all fields, visible focus, reduced motion respected.
6. **Microcopy**: buttons say what they do; errors say how to fix; empty states say what to do next.
7. **Critique**: compare against the brief and the domain's conventions; cut decoration that doesn't orient.

## Artifacts
- Flow diagrams, token definitions, component specs, per-screen state matrix.

## Quality gates
- [ ] Every interactive element has defined states (none missing, none decorative-only).
- [ ] Empty, loading, and error states designed for every data surface.
- [ ] Contrast + keyboard checks noted per screen.
- [ ] Microcopy reviewed for clarity.

## Red lines
- No placeholder lorem shipped; no dead controls.
- Never trade accessibility for aesthetics (or vice versa).

## Related
`frontend-engineering` (implementation) · `product-requirements` (stories) · `technical-writing` (copy standards).
