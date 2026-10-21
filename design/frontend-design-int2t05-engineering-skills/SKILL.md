---
name: frontend-design
description: Design or improve an interface and validate its rendered behavior. Triggers on "frontend", "组件设计".
---

# Frontend Design

## When to use

- Design or improve an interface and validate its rendered behavior.

**Not for:** image-to-code for reference fidelity; design-research for existing visuals.

## Steps

1. Identify users, core flow, design system, framework and viewports; do not fabricate personas or usability results.

2. Define hierarchy, layout, typography, spacing and color from the brief and existing system rather than universal color formulas.

3. Specify relevant loading, empty, error, focus, disabled and success states, keyboard access and responsive behavior.

4. Implement when authorized, run the interface and inspect screenshots and interactions; create a design report only when its consumer and path are agreed.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/design/DESIGN.md`, `docs/design/frontend-audit.md` or `docs/research/ux-research.md` only for corresponding requested work.

## Verify

- Critical flows work at target viewports and with keyboard input; visual claims use actual renders.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [design-principles.md](../../../references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, minimize cognitive load, design every state, accessibility non-optional, consistency from systems)
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [product-icon.md](../../../references/product-icon.md) — generating a product icon / favicon as SVG (mature brand references, restrained geometry and small-size checks)
- [references/styles.md](references/styles.md) — 21 UI styles with effect specs (shadows, blur, radius)
- [references/palettes.md](references/palettes.md) — 12 palette directions by product type
- [references/font-pairings.md](references/font-pairings.md) — 31 font pairings across 10 personality categories
- [references/ux-guidelines.md](references/ux-guidelines.md) — 232 UX guidelines across 10 priority categories + pre-delivery checklist
- [references/apple-hig.md](references/apple-hig.md) — Apple HIG routing table + quick-reference specs
- [references/brief-inference.md](references/brief-inference.md) — design-read protocol + 3 dials (variance, motion, density) + design-system selection map
- [references/anti-tells.md](references/anti-tells.md) — forbidden AI patterns + pre-flight check matrix
- [references/motion-system.md](references/motion-system.md) — motion token scale, easing catalog, choreography patterns, scroll-animation skeletons
- [references/design-tokens.md](references/design-tokens.md) — token tiers, naming convention, scales (spacing, radius, elevation, z-index)
- [references/component-anatomy.md](references/component-anatomy.md) — compound components, slot architecture, variant axes, composition patterns
- [references/state-management.md](references/state-management.md) — client vs server state, store/cache selection, state machines, optimistic updates, derived state, normalization
- [references/design-foundations.md](references/design-foundations.md) — design theory in one place: Perception & Gestalt, Cognitive Laws (Hick's, Fitts's, Miller, Tesler, Von Restorff), Color (HSB, schemes, 70:25:5), Typography (anatomy, rhythm, scale), Hierarchy & Layout (F/Z patterns, squint/5-second tests, CRAP), Usability Heuristics (Nielsen 10, Norman, Rams), Information Architecture (4 elements, card sorting, labeling)
- [references/state-design.md](references/state-design.md) — four states (loading/error/empty/partial), skeleton screens, empty-state design, error recovery
- [references/material-design.md](references/material-design.md) — Material 3 color/type/elevation/state-layer roles, M3 vs M2, when Material vs HIG vs custom
- [references/ux-research.md](references/ux-research.md) — user interviews, personas, journey maps, empathy maps, usability testing (5-user rule, think-aloud)
- [references/visual-direction.md](references/visual-direction.md) — shared web visual-direction engine for imagegen (web mode) and image-to-code (variation axes, hero scale, composition anchors, anti-slop)
- [references/design-system-audit.md](references/design-system-audit.md) — token coverage vs hardcoded values audit, component variant/state/a11y documentation, systematic extension patterns
