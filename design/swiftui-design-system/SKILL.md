---
name: swiftui-design-system
description: "Refine SwiftUI hierarchy, typography, color, SF Symbols, materials, Liquid Glass, animation, charts, and consistent native-feeling components using Apple HIG principles."
---

# Visual language, materials, and motion

## Inputs

Identify the product task, primary and secondary actions, platform, appearances, accessibility settings, design constraints, and exact availability of any new visual API.

## Rules

- **DES-001 — Make hierarchy purposeful.** Use prominence, spacing, type, and placement to communicate the workflow rather than decorate every element equally.
- **DES-002 — Keep native surfaces native by default.** Let system controls and chrome adapt; customize only where the product benefits and behavior remains intact.
- **DES-003 — Use materials by role.** Reserve Liquid Glass primarily for the functional control/navigation layer; avoid stacking decorative glass over content.
- **DES-004 — Motion communicates state.** Scope animations to intended changes, preserve identity, and provide reduced-motion behavior.
- **DES-005 — Validate the entire component.** Typography, symbol, fill, foreground, target size, disabled/focus/pressed states, and localization form one contract.

## Workflow

1. Identify the screen's immediate purpose and remove competing emphasis.
2. Prefer semantic text styles, colors, symbol roles, and spacing derived from actual composition.
3. Map repeated surfaces and share components for repeated semantics; preserve context-specific actions and data authority.
4. Adopt new visual APIs behind correct availability checks with a coherent fallback.
5. Inspect rendered states across appearances, sizes, and accessibility settings.

## Verify

Check hierarchy, content legibility behind materials, light/dark appearances, larger text, contrast/transparency settings, reduced motion, symbol availability, and interrupted animations. Do not treat a first-party screenshot as public-API evidence.

## Output

Return the design rationale, reusable component boundaries, version fallback, and rendered evidence or remaining review steps.

## References

Read the [playbook](references/design-patterns.md) for decisions, failure cases, and source links.

For glass, charts, and motion as semantic components, read the [focused reference](references/glass-charts-and-motion.md).
