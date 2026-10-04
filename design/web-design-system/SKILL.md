---
name: web-design-system
description: Extract, create, or refine an implementation-ready design system for a website or web app. Use when an agent needs semantic tokens, component anatomy, variants, interaction states, responsive rules, accessibility defaults, or consistency improvements grounded in an existing frontend codebase.
---

# Web Design System

Build the smallest system that makes the product more coherent. Favor semantic contracts that components can use over a large inventory of decorative values.

## Choose the Mode

- **Extract** when the product is visually coherent but undocumented.
- **Reconcile** when multiple patterns conflict.
- **Create** when a new product has no established UI language.
- **Extend** when a feature needs states or components the system lacks.

## Workflow

1. Inspect the framework, CSS strategy, theme files, primitives, component library, icon set, and representative screens.
2. Inventory repeated values and patterns. Separate intentional variation from accidental drift.
3. Map raw values to semantic roles before changing code. Example: `blue-600` -> `action-primary`, not "replace every blue."
4. Define the minimum token layers:
   - foundations: color, type, spacing, radius, border, shadow, motion;
   - semantic tokens: background, surface, text, border, action, focus, and status;
   - component tokens only where a component genuinely needs them.
5. Specify component anatomy, variants, sizes, and state behavior. Include content constraints, not only appearance.
6. Define responsive behavior and density rules without inventing device-specific duplicates.
7. Encode accessibility defaults: semantic elements, names, labels, focus-visible, keyboard behavior, contrast, errors, target size, and reduced motion.
8. Implement inside the existing styling mechanism. Avoid parallel token systems.
9. Migrate one representative component or screen and remove superseded values when safe.
10. Verify light/dark themes, core states, narrow/wide layouts, and at least one realistic content stress case.

## System Rules

- Name tokens by purpose, not by current appearance.
- Keep primitive escape hatches available, but make the correct path easier.
- Do not force every region into a card.
- Do not encode status through color alone.
- Keep component APIs small; prefer composition over variant explosions.
- Preserve established patterns unless they harm usability, accessibility, or maintainability.
- Document decisions where future contributors would otherwise recreate the inconsistency.

## Delivery Contract

Provide:

1. **Mode and audit** - what exists, what conflicts, and what remains.
2. **Token map** - existing value -> semantic role -> implementation location.
3. **Component contract** - anatomy, variants, states, content limits, responsive behavior.
4. **Migration slice** - at least one real component when code changes are requested.
5. **Verification evidence** - themes, states, viewports, and exceptions tested.

## Reference

Read [references/token-checklist.md](references/token-checklist.md) while defining or auditing tokens and component states.
