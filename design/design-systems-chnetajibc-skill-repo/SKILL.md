---
name: design-systems
description: "Design systems: typography, spacing, contrast, tokens, shadcn/Tailwind patterns. Generate system first, then supplement with searches."
---

# design-systems

System first, screens second: tokens and primitives before one-off styles.
## Inspection

Audit current tokens, primitives, and off-system one-offs; count duplications of the same visual job.

## Decision rules

Tokens before screens; primitives before pages; extend the system instead of bypassing it; kill near-duplicate components by merging.


## Activate when

- Starting UI work, defining tokens/themes, or auditing visual consistency.

## Do NOT activate for

- Library choice mechanics (see ui-libraries); single-component design (see component-design).

## Procedure

1. Generate the system first: type scale, spacing scale, color tokens (light/dark), radii, shadows, motion tokens — reasoned from product type, not defaults.
2. Primitives over pages: buttons, inputs, cards, modals, tables built on tokens; pages compose primitives.
3. Enforce: no raw hex/spacing outside tokens; no default-palette look; new variants extend the system, not bypass it.
4. Verify: token coverage audit, dark-mode pass, contrast check, component inventory against the system.

## References
- Style/palette research via official component docs (registry: `../../research/documentation-search/references/framework-registry.yaml` — tailwind, shadcn, radix, mui); library mechanics: `../ui-libraries/`.

## Failure modes

Raw hex/spacing outside tokens; default-palette look; three button variants doing one job; dark mode as afterthought.

## Escalation

Library mechanics → frontend/ui-libraries; layout → frontend/responsive-design.
