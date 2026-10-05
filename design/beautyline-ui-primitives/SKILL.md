---
name: beautyline-ui-primitives
description: >-
  Tailwind layout, Section wrapper, shared Button, cn() merging, and global
  CSS tokens for the Beautyline webapp. Use when building or restyling UI,
  marketing sections, cards, headings, spacing, colors, or new pages.
---

# Beautyline: UI primitives

## Stack

- **Tailwind CSS v4** with tokens in `src/styles/global.css` (`:root`, `@theme`).
- **Class merging**: `cn()` from `@/lib/utils` (clsx + tailwind-merge). Prefer `cn('base', className)` for components that accept `className`.

## Layout shell

- **Sections**: Use `Section` from `@/components/Section` for vertical page bands. Override with `className` (outer `<section>`) and `containerClassName` (inner wrapper — max-width, flex, gaps). Defaults include min-height and padding — override when a block must be shorter (e.g. `min-h-0`).
- **Headings**: Section titles that should match the brand use the utility **`.heading-brand`** (purple + Raleway). Do not hardcode `#8B66A9` for those titles if the utility fits.

## Colors and surfaces

- Prefer **semantic tokens** already mapped in Tailwind theme: `bg-muted`, `text-secondary`, ring utilities like `ring-black/5`, and **`primary`** / **`secondary`** / **`purple`** where the design uses brand colors.
- Source of truth for hex values lives in **`src/styles/global.css`** — extend there if you introduce a new brand token rather than scattering one-off hex in JSX.

## Components

- **Buttons**: Prefer `Button` from `@/components/shared/Button` (`variant`: `primary` | `secondary` | `outline`, `size`: `sm` | `md` | `lg`). Use raw `<button>` only when extending native behavior in a primitive or when Button is inappropriate.
- **Images**: Prefer `next/image` with explicit dimensions or `fill` where the layout already establishes size.
- **Links**: Prefer `next/link` for internal routes; `<a>` for external URLs.

## Spacing rhythm

Marketing sections commonly use responsive padding/gaps aligned with **`Section`** defaults (`py-12 md:py-16 lg:py-20` on the outer section unless overridden). New blocks should visually match sibling sections unless the design deliberately breaks rhythm.
