---
name: aria-label-split-text-rendering
description: >-
  Use when one text value is rendered across two or more elements for styling — a typed prefix in
  one ink and the completion in another, a highlighted search match, a two-tone label — and a
  getByRole query for an option by its visible name fails, an accessible name comes back with an
  extra or missing space, or a review flags the accessible name of a listbox row or custom control.
---

# aria-label for split text rendering

## Profile keys consumed

- `architecture.source_root`
- `framework.ui`

## Overview

The accessible name of an element with no explicit label is computed from its contents, and the
algorithm joins each child element's text with a space. Splitting one word or phrase across two
elements for styling therefore produces a name that does not match the visible text. Give the
container an explicit `aria-label` carrying the whole, unsplit value.

## When to use

- An autocomplete, search, or select option renders the typed prefix and the completion as separate
  elements.
- A test cannot find a control by its visible name, or finds it under a name with a stray space.
- Any component splits a single value for colour, weight, or emphasis.
- Not for: text that is genuinely two separate pieces of content (a title plus a description); those
  want real structure, not a flattened label.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — the rule holds for any component, but no listbox or autocomplete option
  renderer exists today; the nearest live cases are labelled form controls.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — same; the shared
  components barrel under `architecture.source_root` ships no option renderer.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — the
  shared option renderer under the field-controls directory of `architecture.source_root` applies it
  for the search and multi-select listboxes, and its unit tests query by the full option name.

## Core pattern

```ts
// Broken: two runs, so the name-from-contents algorithm joins them with a space.
<li role="option">
  <span style={headInk}>{head}</span>
  <span style={tailInk}>{tail}</span>
</li>

// Fixed: the row carries the whole value, and `pre` keeps the real separator.
React.createElement(
  'li',
  { ...optionProps, 'aria-label': label },
  <Box component="span" sx={{ color: headInk, whiteSpace: 'pre' }}>{head}</Box>,
  <Box component="span" sx={{ color: tailInk, whiteSpace: 'pre' }}>{tail}</Box>
);
```

Two details make the fix complete:

- **`whiteSpace: 'pre'` on each run.** A listbox row is usually `display: flex`, so each run is a
  flex item that trims its own leading and trailing whitespace. A space that falls on the split
  boundary disappears and the two words render glued together.
- **`React.createElement` rather than a JSX spread.** `react/jsx-props-no-spreading` is an error in
  the React SPA and component-library shapes with a short exception list that does not include a
  bare `li`, so the prop bag a component library hands the renderer is passed as an explicit object.
  That satisfies the rule at the source instead of suppressing it. The `Box` wrapper above is the
  `framework.ui` primitive; use whatever styled primitive the configured UI library provides.

## Verification

Assert the name, not the markup: `getByRole('option', { name: '<full value>' })` must resolve, and
the rendered text content must equal the same string. Both must pass — a matching `aria-label` with
a broken visible split is still a mismatch between what is seen and what is announced.

In review, the shape to spot is any element carrying a role whose name comes from contents and which
holds more than one text-bearing child; check that its label names the whole value.

## Common mistakes

- Adding `aria-label` to one of the runs instead of the container — the container's name is still
  computed from contents.
- Writing an `aria-label` that paraphrases the value; WCAG 2.5.3 Label in Name requires the
  accessible name to contain the visible text.
- Fixing the space with a `&nbsp;` or a literal space element instead of `whiteSpace: 'pre'`, which
  changes the visible text and re-breaks the name.
- Leaving the label static when the runs come from a dynamic value — derive both from the same bound
  value so they cannot drift.
