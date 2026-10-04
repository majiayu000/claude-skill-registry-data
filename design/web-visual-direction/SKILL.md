---
name: web-visual-direction
description: Define a distinctive, implementable visual direction for websites and web apps. Use when an agent must establish or repair art direction, typography, color, composition, imagery, density, motion, or the first-screen impression before substantial frontend implementation.
---

# Web Visual Direction

Turn an ambiguous brief into one coherent visual system. Make choices that fit the product and can survive implementation; do not produce a mood-board-shaped list of adjectives.

## Workflow

1. Inspect the product brief and existing code, brand assets, screenshots, content, component library, and constraints. Preserve intentional brand equity.
2. State the audience, their immediate task, and the feeling the interface should create in one sentence each.
3. Choose one visual thesis with a useful tension, such as "editorial authority with operational speed." Explain why it fits.
4. Select two or three relevant references. Extract principles - rhythm, contrast, framing, density - not surface decoration or copyrighted layouts.
5. Decide the composition before styling details:
   - identify the first viewport's focal point;
   - define the grid, content width, density, and section rhythm;
   - decide what intentionally breaks the grid, if anything.
6. Define implementation-ready rules for typography, color, surfaces, borders, imagery, icons, and motion.
7. Express the direction as a small token set and component implications. Reuse the project's existing styling system.
8. Implement one representative viewport or component when implementation is in scope.
9. Verify the direction at mobile and desktop widths. Remove choices that weaken comprehension, hierarchy, performance, or accessibility.

## Decision Rules

- Lead with the real product, work, place, person, object, or outcome.
- Prefer a memorable structural idea over decorative effects.
- Match density to the job: operational interfaces are compact; narrative brand pages can breathe.
- Use typography with a reason. Do not ban or choose a font only because it is fashionable.
- Use cards for meaningful grouping, not as the default container for every sentence.
- Treat gradients, glass, grain, glow, and oversized type as tools, not proof of design quality.
- Keep motion purposeful and respect reduced-motion preferences.
- Do not fabricate brand assets, customer logos, metrics, or product screenshots.

## Delivery Contract

Return or implement:

1. **Visual thesis** - one sentence.
2. **Reference principles** - what to borrow and what to avoid.
3. **Direction spec** - composition, type, palette, surfaces, imagery, icons, and motion.
4. **Token sketch** - named values or mappings compatible with the codebase.
5. **Responsive intent** - what changes at narrow and wide widths.
6. **Proof** - screenshot or inspected viewport when browser access exists.

## Reference

Read [references/site-archetypes.md](references/site-archetypes.md) when the product type should materially change the direction.
