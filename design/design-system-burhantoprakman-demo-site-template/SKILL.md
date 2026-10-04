---
name: design-system
description: Use when building, editing, or reviewing any page or component on this site - anything that produces markup or CSS. Covers the token system, the component library, when to build something new, and the layout rules. Trigger on requests to add a page, add a section, change styling, adjust spacing or colour, or make something "look better".
---

# Design system

## The one rule

Use what exists. This site has a small component library on purpose. A page
that introduces its own spacing, its own colours, or its own card style breaks
the consistency the template exists to provide.

## Tokens

`src/design/tokens.json` is the source of truth. `src/styles/tokens.css` is
generated from it by `npm run tokens` — never edit the CSS directly.

Every value in a component comes from a variable:

| Need | Variable |
|---|---|
| Text colour | `--color-ink`, `--color-ink-muted` |
| Backgrounds | `--color-paper`, `--color-paper-sunk`, `--color-accent-soft` |
| Borders | `--color-rule` |
| Links, primary action | `--color-accent` |
| Warnings only | `--color-signal` |
| Font size | `--size-xs` … `--size-3xl` |
| Spacing | `--space-1` … `--space-24` |
| Corner radius | `--radius-sm`, `--radius-md` |
| Column widths | `--layout-measure`, `--layout-content`, `--layout-wide` |

If a value you need is not in the scale, use the nearest one. Do not invent
`padding: 13px`.

## Components

Read `src/pages/kitchen-sink.astro` for the current inventory. At time of
writing:

- `BaseLayout` — every page starts here. Takes `title` and `description`.
- `Hero` — one per page, at the top. `headline` plus optional `standfirst`.
- `Section` — the main building block. `title`, `width` (`content` | `wide`),
  `sunk` to tint the background.
- `Callout` — `note` or `warning`. For things a reader would otherwise miss.
- `CodeBlock` — `lang` or `file` label.
- `ComparisonTable` — `columns`, `rows`, and a required `caption`.
- `Figure` — wraps a diagram or screenshot, requires a `caption`.
- `Steps` — numbered sequence. Only when the content really is a sequence.
- `CallToAction` — `primary` or `secondary`.

## Building something new

Only when nothing above fits. Then:

1. Put it in `src/components/` as a `.astro` file with a typed `Props`
   interface and a doc comment per prop.
2. Style it in the component's own `<style>` block, scoped, using tokens only.
3. Add a case to `kitchen-sink.astro`.
4. Tell the person you added a component and why nothing existing worked.

## Layout

- Running text stays within `--layout-measure` (68ch). Do not widen it.
- Sections handle their own vertical rhythm. Do not add margins between them.
- Test at 375px wide. Tables scroll horizontally; nothing else should.

## What not to do

- No new colours outside the token file
- No page-level `<style>` blocks
- No decorative gradients, drop shadows, or hover animations on every card
- No all-caps eyebrow labels above headings
- No numbered markers unless the content is a sequence
