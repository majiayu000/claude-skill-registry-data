---
name: ui-implement
description: Implement one UI page from an approved generated design, a user-provided design artifact, or an authorized existing website, then iteratively refine it through matched-viewport screenshot comparison.
---

# UI Implement

Implement one page at a time and refine it against an approved visual reference.
The reference may come from a generated design, a user-provided design artifact,
or an authorized existing website. All three modes converge on the same
implementation, screenshot, and comparison loop.

## Choose the Reference Source

Read the page name, current issue, acceptance criteria, target route, required
states, and desktop and mobile viewports. Then use one mode:

### Generated Design

Use `design/panels.png` as the cross-page design overview and
`design/<page-name>-reference.png` as the page's full-resolution visual target.
Store authorized artwork, textures, icons, or images required by the
implementation under `design/assets/`. Recreate ordinary surfaces, gradients,
controls, text, and layout in code.

If the page name or reference cannot be identified, ask for it before
implementing. Do not substitute another page or invent a missing design.

### Provided Design

Use a user-provided Figma frame or export, screenshot, mockup, or design-system
specification as the visual target. Identify which artifact applies to each
page, viewport, and state. If dimensions, responsive behavior, interactions, or
states are not defined, ask for the missing requirements rather than inferring
them from an unrelated platform or viewport.

Save approved visual artifacts as `design/<page-name>-reference.png`, adding
viewport or state suffixes when multiple references would otherwise collide.
Do not overwrite an existing reference without confirmation. Treat a design
system as implementation guidance; capture or export a complete page reference
before visual comparison when it does not include one.

### Existing Website

Require the target URL, permitted pages or flows, required states, target route,
viewports, and whether branding, text, imagery, fonts, and other assets may be
reused.

1. Open each permitted page with browser or Chrome DevTools tooling at every
   required viewport and capture its full reference screenshot.
2. Inspect the DOM, accessibility tree, and computed styles to measure
   structure, dimensions, spacing, typography, colors, borders, radii, shadows,
   stacking, breakpoints, and overflow behavior.
3. Observe required navigation, focus order, keyboard behavior, hover states,
   transitions, loading behavior, and responsive changes.
4. Save approved captures as `design/<page-name>-reference.png`, adding viewport
   or state suffixes when needed. Ask before replacing an existing reference.

Use an existing authenticated browser session only when the user authorizes
access. Do not ask the user to expose credentials or bypass authentication,
paywalls, CAPTCHAs, access controls, or other restrictions.

Treat inspected markup and styles as measurements, not source code to copy. Do
not transfer proprietary text, logos, imagery, fonts, or other protected assets
unless the user confirms they may be reused. Otherwise preserve the requested
structure and behavior with original content and assets without creating a
confusingly identical branded result.

## Implement

1. Inspect the existing project structure, styling system, shared components,
   and commands before editing.
2. Identify the target platform, route or screen, viewport, content, states,
   and interactions from the issue and page reference.
3. Implement all text, forms, buttons, icons, navigation, and other controls in
   code. Use files from `design/assets/` only for authorized visual assets that
   the implementation actually requires.
4. Recreate the page reference closely without redesigning or improvising
   unless required information is absent. Preserve established project
   conventions and reuse appropriate existing components.
5. Keep functional behavior, responsiveness, and accessibility requirements
   authoritative when they require a justified visual difference.

## Compare and Refine

1. Run the app using its existing development workflow in the appropriate
   browser or simulator at the target viewport.
2. Capture a screenshot of the implemented page.
3. Compare the complete rendered page with the matching page, viewport, and
   state reference.
4. Identify and correct differences in layout, spacing, typography, colors,
   gradients, controls, borders, radius, shadows, icons, imagery, alignment,
   padding, hierarchy, and image cropping.
5. Capture a new screenshot and compare again after each refinement.
6. Continue until the page satisfies its visual, functional, responsive, and
   accessibility acceptance criteria. Do not stop after the first
   implementation.

Treat the reference as a strict target, but do not require literal pixel
equality where browser or simulator rendering, authorized content changes,
responsive behavior, or accessibility creates a justified difference. Stop if
further similarity would require missing access, unauthorized assets,
unspecified behavior, or a requirements violation, and report the blocker or
remaining differences.

## Verify and Report

Run the relevant project checks after implementation and the repository's
required completion check before declaring the page complete. Summarize the
implemented page, comparison iterations, verification results, and any
remaining justified differences. Do not commit, push, or open a pull request
unless the user requests those actions.
