---
name: figma-design-review-before-code
description: >-
  Use when a component's Figma design must be reviewed BEFORE any code exists — a new UI component,
  a design handoff, a spec artifact, or a request to review a design against the existing
  components. Symptoms include no implementation file yet, only a Figma node id or a spec markdown,
  and open questions about semantics, accessible names, alt text, disabled states, or state
  variants. Not the implementation-parity gate run against code that already exists.
---

# Figma design review before code

## Profile keys consumed

- `capabilities.figma`
- `architecture.source_root`
- `architecture.component_prefix`

The design extraction runs through the Figma MCP server, gated by `capabilities.figma`: skip the
review with a recorded capability-absent note when `capabilities.figma` is `false`, and ask the
design owner for the intended contract instead of inventing it from memory.

## Overview

A pre-implementation review extracts the **binding contracts** a design imposes — document
structure, accessible-name source, decorative-vs-informative imagery, interaction boundaries — by
reading the Figma design next to the closest already-shipped component. It deliberately stops short
of pixels: sizing and spacing parity belong to implementation-time verification.

## When to use

- A new component is specified in Figma or in a spec artifact and no source file exists yet.
- A design handoff needs its accessibility and semantics contract settled before a story is opened.
- A reviewer asks whether a design fits the existing component precedents.
- Not for: verifying an already-written component against Figma (that is implementation parity
  work), or tuning shadows, radii and spacing.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — precedents under the source root's prefixed component folders
  (`architecture.source_root` plus `architecture.component_prefix`, e.g. `src/components/ui-*`),
  spec artifacts under `specs/<slug>/`; the tracked `figma-design-check` skill is the sibling gate.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — precedents under the
  source root's `components` folder, spec artifacts under `specs/<slug>/`; the same tracked
  `figma-design-check` skill applies.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  precedents under the source root's prefixed component folders, spec artifacts under
  `specs/implementation-artifacts/`; no tracked repository skill, so the review is the only gate.

## Procedure

1. Locate the design: a Figma file key plus node id, or the linked spec artifact. Never review from
   a screenshot or from memory.
2. Record the anatomy and the full state set the design ships — typically Rest, Hover, Active,
   Disabled — plus any loading or empty variant.
3. Read the closest precedent component in full: its `index.tsx` for document structure and ARIA,
   its type-only file for the prop contract — a sibling `types.ts` in the Next.js and
   component-library shapes, a grouped `types/<component>/` folder under the source root in the
   React SPA shape — and its spec artifact for decisions already argued.
4. Compare and write findings under four headings only:
   - **Structure** — is the root a native `button`, a link, or a non-interactive element? Native
     semantics beat a `role` unless the design makes that impossible.
   - **Accessible name** — where does it come from (text content, `aria-label`, an adjacent field
     label)? Is one guaranteed in every state?
   - **Imagery** — each icon or image is decorative (`aria-hidden`, empty `alt`) or informative (a
     described alternative). Say which, per node.
   - **Interaction** — clickable region boundaries, focus order, and how disabled is expressed.
     On a native form control — `button`, `input`, `select`, `textarea`, `fieldset` — the native
     `disabled` attribute is the correct expression: it blocks activation and, on an input, stops
     the value being submitted. `aria-disabled` is for a custom or non-native control (a `div` or
     `span` widget, a link) that has no native `disabled` to set: it keeps the control focusable so
     focus is never dropped mid-interaction, and the handler must reject activation itself. Reach
     for `aria-disabled` on a native control only when the design requires the disabled state to
     stay focusable, and then the same handler-side rejection applies.
5. Return the findings as text. Write no files during a review — no probes, no reports, no scratch
   output; a review that edits the working tree is no longer a review.

## Precedent rules

- Compare only against components in the same repository, not external libraries: the point is
  consistency with what already ships.
- If the design brief and the Figma extraction disagree on a value, the brief is authoritative and
  the disagreement is itself a finding.
- Flag a contract as blocking only when it changes the DOM the implementation must emit. Colour,
  radius and shadow deltas are notes, not blockers.
- Confirm that type — size, weight, line-height — resolves to a named design token rather than a raw
  value. A token that does not exist is a contract finding; measuring the rendered pixels is not.

## Common mistakes

- Measuring pixels — that is implementation-time parity work and buries the contracts.
- Reviewing from a screenshot — state variants and layer names carry the contract, and a raster
  loses both.
- Writing a report file — findings belong in the reply; a stray file corrupts the working tree.
- Naming a `role` before checking whether a native element already carries it.
- Ignoring the Disabled variant — it is where the accessible name and focus behaviour usually break.
