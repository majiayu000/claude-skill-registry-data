---
name: responsive-layout
category: frontend
description: Use when you build or change a layout, page, section, navigation, table, form or image - mobile-first rules, breakpoints and the overflow traps.
source: pbakaus/impeccable (Apache-2.0), vercel-labs/web-interface-guidelines (MIT), ibelick/ui-skills (MIT), nextlevelbuilder/ui-ux-pro-max-skill (MIT), adapted
---

# Responsive Layout

## Overview

Every layout is designed at 360px first, then widened. Desktop-first layouts that get "patched down" with `max-*:` overrides are where almost every overflow bug comes from, because the narrow case was never actually built — it was reverse-engineered from the wide one under time pressure.

**Core principle:** Build the 360px layout first, make it correct, then add `md:`/`lg:` to use the extra space. Never write desktop styles first and patch down.

## Rules

- Unprefixed Tailwind utilities are the phone layout. `sm:` (640) `md:` (768) `lg:` (1024) `xl:` (1280) `2xl:` (1536) add capability upward — they never subtract it.
- Breakpoints follow Tailwind's default scale; pick one by where *your content* breaks (a nav that collapses, a table that gets cramped), not by matching a specific device.
- Never `max-*:` as the primary layout strategy — it means the base case is the wrong one.

## Layout primitives

- **Container**: `mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8` for page content; narrower for prose (`max-w-prose` / `max-w-3xl`) in marketing sections.
- **Section rhythm**: `py-12 md:py-16 lg:py-24` — more space grows with viewport, it doesn't appear from nothing at `md`.
- **Grid recipes**: `grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3` for card/list grids; `grid-cols-[repeat(auto-fit,minmax(min(100%,16rem),1fr))]` when the item count is unknown and a fixed column count would leave gaps or force scroll (ui-guard's allow-listed arbitrary value).
- **Flex rows that wrap**: `flex flex-wrap gap-2` for chip/tag/button rows — never a fixed-height row that clips.
- **Sidebars**: stack below `lg` (`flex flex-col lg:flex-row`), sidebar full-width on phone, fixed-width only at `lg:` and up.
- **Container queries**: an organism placed in genuinely different-width contexts (a dashboard grid cell vs. a full-width page) sizes off its own box — `@container` on the wrapper, `@md:`/`@lg:` on the organism — instead of the page's breakpoints; the viewport can be 1440px while the card is 300px wide.

## Overflow trap catalogue

Each trap below was reproduced in a real browser at 360–1440px and its fix confirmed clean.

| Symptom | Cause | Fix |
|---|---|---|
| Flex/grid item refuses to shrink, pushes siblings off-screen | Flex/grid items default to `min-width: auto`; a `truncate`/`whitespace-nowrap` descendant sets that item's min-content to its full unbroken width | `min-w-0` on the item that holds the text (not just the text itself); `shrink-0` on siblings that must stay fixed |
| Page scrolls sideways with no single element flagged as overflowing | A long word or URL with no space for the browser to wrap on — the block keeps its layout width while the text spills out of it, so `browser_set_viewport` reports that the page scrolls horizontally but names no overflowing element. Search the page for long unbroken strings | `break-words` (`overflow-wrap: anywhere`) on the text node; never `break-all` (it breaks mid-word even when wrapping wasn't needed) |
| A panel is too wide below some breakpoint | A literal pixel width (`w-[600px]`) | `w-full` + a `max-w-*` cap so it still has a ceiling on wide screens |
| Image forces horizontal scroll | Something overrides Tailwind v4's own preflight, which already sets `img, video { max-width: 100%; height: auto }` — a stray `max-w-none`, a reset library, or a hard inline `maxWidth` | Give the image `w-full h-auto max-w-full`, explicit `width`/`height` attributes (prevents CLS), and `object-cover` + `aspect-*` when it fills a fixed box. A bare `<img>` with no extra classes does **not** overflow by default in Tailwind v4 — if one does, something upstream overrides preflight |
| A row of buttons/chips runs off the right edge | `whitespace-nowrap` on the row instead of letting items wrap | `flex flex-wrap gap-2` — wrap the row, don't force it onto one line |
| A decorative shape (blob, ring, gradient) pokes past the viewport edge even on desktop | An absolutely-positioned decoration with a negative offset (`-right-10`) and no clip on its own stacking context | `overflow-x-clip` on the **section** that owns the decoration, never on `body` (that breaks every `position: sticky` on the page) |
| Full-bleed section overflows as soon as it's not a direct child of `body` | `w-screen` (100vw) ignores every ancestor's padding/offset — it ties to the viewport, not the nearest positioned parent, so it overflows the moment it's nested inside anything with horizontal padding | `w-full` (ties to the parent instead); reach for `w-screen` only with a negative-margin bleed technique on a direct full-width wrapper, and test it |
| `grid-cols-3` (or any fixed count) is unusable at 360px | Short, wrapping text in a 3-up grid just looks cramped — it does **not** overflow by itself. It becomes an actual overflow once any cell holds one long unbreakable token (a code snippet, a slug, a username): grid items default to `min-width: auto` too, so that one cell's min-content can force the whole track wider than the viewport | `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3` (mobile-first column count) **and** `min-w-0 break-words` on every cell, so neither the column count nor a stray long token can force the overflow |
| A data table forces the whole page to scroll sideways | The `<table>` laid out directly in the page flow, no scroll boundary around it | Wrap it in its own `overflow-x-auto` (table keeps `min-w-*` so columns stay legible; the wrapper — not the page — scrolls), or replace it with stacked cards below `md` for simpler tables. Comparison/pricing tables: cards below `md`, or a sticky first column. A scroll wrapper is keyboard-reachable: `tabIndex={0}`, `role="region"` and an `aria-label` naming the table (axe `scrollable-region-focusable` fails without it). The page-level horizontal-scroll check correctly stays clean here — the *wrapper* scrolls, the page does not |
| 100vh content gets cut off under mobile browser chrome | `h-screen`/`100vh` is measured before the address bar collapses, so content sits behind it | `min-h-dvh` (never `h-screen`) |
| Long compound words (German, Turkish) blow out a heading's line | No wrap/hyphenation hint, and the heading's container is width-constrained | `text-balance` on the heading, `hyphens-auto` with the correct `lang` on the element |

## Typography responsiveness

- Step heading sizes per breakpoint: `text-3xl md:text-5xl` rather than one fixed size. If the design calls for continuous scaling, do it through a token-defined `clamp()`, not an ad hoc one in a className.
- `<input>`/`<textarea>` text stays ≥16px (`text-base`) on phone — smaller triggers iOS's auto-zoom on focus, which is its own kind of layout break.

## Navigation

- ≥5 top-level links collapse below `md` into a menu button (`aria-expanded`, `aria-controls`) opening a Radix Dialog/Sheet or disclosure panel; it closes on link click and `Escape`.
- Sticky header: `sticky top-0 z-20` (`z-20` is the sticky-header band of the fixed z-scale: 10 raised · 20 sticky header · 30 dropdown · 40 overlay · 50 modal/toast). Anchored sections under it need `scroll-mt-20` (or whatever matches the header's height) so `#section` links don't land underneath it.
- Fixed/sticky bars respect `env(safe-area-inset-*)` so they don't sit under a notch or home indicator.
- Mobile menu requirements: trigger button with `aria-expanded`/`aria-controls`, Radix Dialog/Sheet for the panel (focus trap and body scroll lock come free), closes on link click and `Escape`.

## Touch

- Targets ≥44×44px on phone (`min-h-11 min-w-11` or padding to reach it), ≥24px on desktop.
- ≥8px between adjacent targets so a miss-tap doesn't hit the neighbor.
- No hover-only functionality — anything a mouse user reaches by hovering needs a tap-accessible equivalent; gate hover-only *niceties* behind `@media (hover: hover)` so touch devices don't get a stuck hover state.
- `touch-action: manipulation` on interactive elements removes the ~300ms double-tap-to-zoom delay.

## Images & media

- Responsive sourcing: `srcset`/`sizes`, or `<picture>` with art-directed breakpoints, so phones don't download the desktop asset.
- `loading="lazy"` below the fold; the hero/LCP image stays eager.
- `aspect-*` (or explicit `width`/`height`) reserves the box before the image loads, preventing layout shift.

## Worked Example

A pricing comparison section, written desktop-first, has three overflow bugs:

```tsx
// ❌ desktop-first: three columns, a fixed-width badge, and a long plan name that doesn't wrap
<section className="grid grid-cols-3 gap-6 p-8">
  {plans.map(plan => (
    <div key={plan.id} className="border p-6">
      <div className="flex gap-2">
        <h3 className="font-semibold">{plan.name}</h3>
        <span className="whitespace-nowrap rounded bg-primary px-2 py-1 text-primary-foreground">
          Most popular
        </span>
      </div>
      <div className="w-[280px] mt-4">{plan.description}</div>
    </div>
  ))}
</section>
```

Bug 1: `grid-cols-3` with no mobile step — three ~110px columns at 360px. Bug 2: the `h3` + `whitespace-nowrap` badge are flex siblings with no `min-w-0`, so a long plan name pushes the badge (and the row) past the viewport edge. Bug 3: `w-[280px]` is wider than the phone viewport itself.

```tsx
// ✅ mobile-first: one column on phone, badge wraps with the title, fluid width
<section className="grid grid-cols-1 gap-6 p-4 sm:grid-cols-2 lg:grid-cols-3 lg:p-8">
  {plans.map(plan => (
    <div key={plan.id} className="border p-6">
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        <h3 className="min-w-0 break-words font-semibold">{plan.name}</h3>
        <span className="shrink-0 rounded bg-primary px-2 py-1 text-primary-foreground">
          Most popular
        </span>
      </div>
      <div className="mt-4 w-full max-w-sm">{plan.description}</div>
    </div>
  ))}
</section>
```

## Common Mistakes

- Starting a layout at 1440px and adding `max-*:`/media-query patches to make it survive at 360px.
- `w-screen` on anything that isn't a direct, unpadded child of `body`.
- Fighting Tailwind v4's image preflight with `max-w-none` instead of sizing the image on purpose.
- `grid-cols-N`/`flex` rows with no mobile step, found only when real (long) content is dropped in.
- `overflow-x-clip`/`hidden` on `body` to "fix" an overflow instead of finding and fixing the element causing it.

## Red Flags

- Any unprefixed `grid-cols-2`/`grid-cols-3`/`grid-cols-4` on a page-level grid.
- `w-[`, `h-screen`, or `w-screen` anywhere in the diff.
- A flex/grid item holding `truncate` or `whitespace-nowrap` text with no `min-w-0` on an ancestor in the same flex/grid context.
- A `<table>` with no `overflow-x-auto` wrapper and no stacked-card fallback.
- A component never rendered with a long/realistic string before hand-off.
