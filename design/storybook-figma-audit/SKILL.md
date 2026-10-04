---
name: storybook-figma-audit
description: >-
  Use when sweeping a whole component suite or showcase board against its Figma masters — before a
  release, after a design revision, or when several components are suspected of drift — and the
  output has to be a categorized, prioritized bug list rather than a single-component fix.
---

# Storybook Figma parity audit

## Profile keys consumed

- `capabilities.figma`
- `capabilities.storybook`
- `capabilities.visual_testing`
- `make.storybook_build`
- `make.test_visual`
- `architecture.source_root`

## Overview

A suite-wide parity audit is a different job from implementing one component against its design: it
sweeps every story and showcase tile, separates broken behaviour from wrong pixels, and reports
recurring root causes so one fix closes many findings.

## When to use

- A component library, showcase board, or story set needs verifying against Figma masters.
- A design revision landed and several components are suspected of drift.
- A pre-release check for accumulated implementation-versus-design divergence.
- Findings must be triaged and prioritized, not just listed.
- Not for: building or restyling one component against its design — that is a single-component
  parity task; and not for pixel diffing between commits, which the visual regression suite does.

## Applicability gate

The audit needs a Figma reference and a story surface. Skip it with a recorded note when
`capabilities.figma` is `false` (no design master to audit against) or when
`capabilities.storybook` is `false` (no story surface to sweep); when the target mapped by
`make.storybook_build` is `null`, skip the story-build step with a recorded note and audit the
running app's routes instead. When `capabilities.visual_testing` is `false` or `make.test_visual`
maps to `null`, skip the "record this as a baseline" follow-up and rely on the screenshot pairs
captured for the report.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — Storybook is configured (a `.storybook/main.ts` plus a Storybook start target)
  but carries few stories, and the visual specs screenshot the running app rather than stories, so
  the audit runs over the app routes plus whatever stories exist.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — per-component
  stories exist under the components tree, but the visual specs target the production app, so the
  sweep is story-by-story in Storybook.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  component library with a showcase board directory, plus a Storybook-driven Playwright suite with
  chromium baselines run by the target mapped by `make.test_visual`.

## Procedure

1. **Map each component to its design.** Record the Figma frame and node id per state, list every
   story and showcase tile variant (breakpoints; rest, hover, active, focus, open, error, disabled),
   and note which design tokens the component is supposed to consume.
2. **Verify each state against the master.** Read the numbers out of Figma's inspect mode rather
   than estimating them. Compare spacing, size, position, radius and shadow geometry (blur, spread,
   offset); colours including backgrounds and text, against tokens rather than eyeballed hex;
   typography family, weight, size, line-height and anti-aliasing; and interactive behaviour —
   click, hover, focus, disabled, error — including the transition between states.
3. **Categorize every finding** as functional (behaviour broken), visual parity (styling or geometry
   wrong), micro-deviation (under about 2px, documented but not always fixed), or verified-clean
   (record it, so a later change that breaks it is a visible regression).
4. **Prioritize** functional bugs first, then high-contrast visual issues, then micro-deviations.
   Anything that blocks a user action outranks everything cosmetic.
5. **Look for shared root causes** across findings before fixing anything — see below. One story
   template or one theme override usually explains several rows.
6. **Report** as a table of component, issue, Figma node id, rendered value versus spec value, and
   severity, with a screenshot pair as evidence per row.

## Recurring root causes

- **Controlled component with no handler in the story.** A story passing a static `value` with no
  change handler makes every click a guaranteed no-op, and the component has no uncontrolled mode to
  fall back on. Wrap the story in local state, or give the component a default-value path.
- **Showcase tiles pass static props.** A tile rendering with an empty collection and no handler
  still opens the real picker or menu, then discards the result — the component is fine, the tile is
  not.
- **Popup styling applied at the wrong slot.** For MUI `Autocomplete`, option rules reach the popup
  only through the `listbox` slot override (`'& .MuiAutocomplete-option'` nested inside it), which
  out-specifies the built-in option rule; styling the option slot directly loses. Selected and
  focused option backgrounds (`Mui-selected`, `Mui-focused`) need that override explicitly.
- **Showcase layout artifacts read as bugs.** A tile's `sx` may force one size on the field but not
  on an overlay or an internal element. Re-check at a real viewport before filing.
- **Overlay alignment.** Ghost-completion text and caret overlays need coordinates, font family and
  font size identical to the input they sit on, or they drift only at some sizes.

## Common mistakes

- Filing pixel bugs before fixing the functional ones — a component that cannot be operated cannot
  be judged visually.
- Auditing against a stale node id or renamed layer — re-resolve the node before trusting a diff.
- Fixing each finding in isolation when one story template or theme override caused several.
- Leaving verified-clean components out of the report, so nothing detects their later regression.
- Judging a mobile finding from a shrunken desktop tile instead of a real small viewport.
