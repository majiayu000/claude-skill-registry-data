---
name: ui-design-guidance
description: Canonical overlay for graphical UI or frontend redesign, polish-heavy implementation, and deep UX review; use `ui-guidance` for routine changes. Compose with matching implementation guidance when visual direction, accessibility, interaction, responsive behavior, forms, navigation, or data presentation need stronger discipline.
---

# UI Design Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill when the change touches graphical
UI or web frontend code.

This is the stronger UI overlay in this repo.
Prefer it over `ui-guidance` when the task is redesign-heavy, polish-heavy, or
needs explicit UX review beyond basic UI hygiene.

Choose activity independently from visual direction. A review request is
read-only unless the user also asks for remediation; preserve versus redesign
describes the intended product direction, not permission to edit files.

## When to use

- the repo includes graphical UI or web frontend code
- the task asks for UI implementation, redesign, beautification, styling, or
  frontend polish
- the task changes how a feature looks, feels, moves, or is interacted with
- the work includes new pages, components, forms, navigation, responsive layout,
  animation, or charts/data display
- the task asks for UX review or quality improvement, not just visual changes
- the change touches web views, desktop UI, embedded panels, dashboards, pages,
  landing screens, or rendering layers

## Not for

- terminal UIs; use the matching terminal-framework guidance
- pure data visualization or plotting libraries without product-interface work
- backend-only changes with no UI surface

## Core workflow

1. Read the touched UI files and nearby components first.
2. Choose the activity:
   - implementation when the user asks to build, change, redesign, or remediate
     the UI
   - review when the user asks for findings, critique, or release assessment;
     report evidence without editing or requiring findings to be fixed
3. Determine the visual direction:
   - preserve mode when the repo already has a clear design language and the
     user did not ask for redesign
   - redesign mode when the user explicitly wants a new visual direction or the
     current UI is intentionally being reworked
4. In preserve mode, derive tokens, spacing, interaction patterns, breakpoints,
   and component structure from the nearest existing screens or components.
5. In redesign mode, choose one intentional direction before coding: define
   the interface purpose, audience, tone, and the visual idea that should make
   the surface coherent. Read
   [references/redesign-aesthetics.md](references/redesign-aesthetics.md) only
   when the task needs deeper aesthetic direction.
6. For deep implementation or review, evaluate priorities in this order:
   - accessibility
   - interaction and feedback
   - layout and responsiveness
   - typography and color clarity
   - forms, navigation, and data presentation when they apply
7. For implementation, build real working UI code that fits the chosen
   direction:
   - preserve mode should feel native to the repo
   - redesign mode should feel distinctive, cohesive, and production-grade
   - UX remediation should strengthen usability without drifting away from the
     repo's design language unless redesign is requested
8. For review, report prioritized findings with the affected interaction,
   evidence, likely user impact, and validation gaps; do not modify code.
9. Verify accessibility, keyboard behavior, responsive layout stability, and
   visual output with the strongest evidence the repo supports.
10. When the repo lacks UI docs or automated checks, record the fallback
   evidence: files inspected, viewport sizes tested, and screenshots or manual
   checks used.

## Decision rules

- Preserve the existing design language unless the task explicitly calls for
  redesign.
- Accessibility, layout stability, and responsive behavior are part of done,
  not follow-up work.
- UI changes must not bypass the repo's build, test, or review hygiene.
- Match implementation complexity to the visual goal. Refined minimalism needs
  precision and restraint; bold maximalism needs deliberate structure and
  stronger visual systems.
- Before adding a new visual element, search for a similar existing element and
  reuse its patterns unless redesign mode justifies divergence.
- Prefer concise, durable heuristics over giant style catalogs. Use repo
  context first, not generic design-library sprawl.

## UX priorities

### 1. Accessibility

- interactive elements must be keyboard-navigable
- icon-only controls need labels
- visible focus states must remain intact
- color cannot be the only carrier of meaning
- reduced-motion preferences should be respected when animation is present

### 2. Interaction and feedback

- touch and click targets should be comfortably hittable
- loading, success, and error states must be explicit
- primary interactions must not depend on hover alone
- destructive or async actions need clear user feedback

### 3. Layout and responsiveness

- layout must stay stable across supported viewports
- avoid horizontal scroll and fragile fixed-width assumptions
- spacing should follow the repo's existing scale or the nearest local pattern
- fixed or overlay UI should not obscure essential content

### 4. Typography and color

- body text should remain readable without tiny type or weak contrast
- use semantic tokens or shared variables instead of scattered one-off values
- hierarchy should come from spacing, weight, scale, and contrast, not color
  alone

### 5. Forms, navigation, and data

- inputs need visible labels and local error messages
- navigation state and back-path should be predictable
- charts and data views must remain readable without relying on color alone
- empty, loading, and error states should explain what the user can do next

## Validation

For implementation, a UI change is done when, in addition to the base
implementation skill's validation:

- visual output matches the existing design language or the requested redesign
- interactive elements are keyboard-navigable and labeled appropriately
- layout is stable across supported viewports or the nearest documented
  fallbacks
- forms, navigation, and feedback states are explicit where they apply
- the evidence names the files, screenshots, snapshots, or manual checks used
  when automated UI verification is absent

For review, completion means the findings are prioritized, evidence-backed,
and explicit about user impact and unverified behavior. Unfixed findings do not
make the review incomplete.
