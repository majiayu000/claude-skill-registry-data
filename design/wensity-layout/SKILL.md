---
name: wensity-layout
description: >-
  Lay out web UI with a spacing scale, clear grouping, alignment, grids,
  containers, tables and responsive structure that holds from 320px phones
  to wide desktops. Use when creating a page, section, form or dashboard
  layout, or when changing spacing, alignment, grids, containers or
  responsive behavior in React, Next.js, Tailwind CSS or CSS: spacing feels
  random, cramped or too loose, things do not line up, a layout breaks on
  mobile, or the user mentions padding, margins, gaps, grid, whitespace,
  density or responsive design. Skip it for edits that leave layout
  untouched.
---

# Wensity Layout

Layout is how a page tells people what matters and what belongs together,
before they read a word. Good layout comes from three habits: a fixed
spacing scale, grouping by distance, and one alignment system. This skill
sets all three up and covers responsive structure.

If the project already has a spacing scale and container widths, use them.

## 1. The spacing scale

Use a 4px base. Every margin, padding and gap comes from this list:

| Token | px | Typical use |
| --- | --- | --- |
| 1 | 4 | icon to label, tight inline gaps |
| 2 | 8 | inside a control, between a label and its input |
| 3 | 12 | between items in a dense list, button padding y |
| 4 | 16 | card padding (compact), gap between related controls, mobile page gutter |
| 5 | 20 | button padding x (large) |
| 6 | 24 | card padding, gap between form fields |
| 8 | 32 | between groups inside a section |
| 10 | 40 | between a section heading and its content (large) |
| 12 | 48 | section padding on mobile |
| 16 | 64 | between sections in an app, section padding on tablet |
| 20 | 80 | |
| 24 | 96 | section padding on desktop marketing pages |
| 32 | 128 | hero padding, the space around one big statement |

Tailwind's default scale already follows a 4px base (`p-4` is 16px), so use
its steps and do not invent `p-[13px]`. Odd values are allowed only for
optical corrections you checked in the render (an icon that looks off by 1px).

## 2. Group by distance

The single most important layout rule: **space inside a group is smaller
than space between groups.** A label sits 8px from its input; the next field
sits 24px away. A card's title sits 8px above its text; the next card sits
24px away. When inner and outer spacing are equal, everything floats apart
and nothing reads as a group.

- Aim for a ratio of about 1 to 2 or 1 to 3 between inner and outer gaps.
- **More space above a heading than below it.** The heading belongs to the
  content after it. Typical: 48px above a section heading, 16px below.
- **Spacing before boxes.** Group with distance first. Add a border, divider
  or background only when distance is not enough (dense tables, toolbars,
  content on busy backgrounds). A box around every group makes a page heavy.
- **Use `gap` for siblings** (`flex gap-4`, `grid gap-6`) instead of margins on
  children. It keeps spacing in one place and avoids stray margin at the
  ends of a list.

## 3. Rhythm, not sameness

A page where every section has 96px padding, a centered heading and a grid of
three items has no rhythm. Vary density on purpose:

- Alternate dense sections (feature grids, tables, logos) with open ones (one
  statement, one large image).
- Let important sections take more space. Space is how you spend attention.
- Repeat a layout only when the content is truly the same kind of thing.

## 4. Alignment

- **One start edge.** Headings, paragraphs, buttons and images in a section
  share the same starting line. Most "something looks off" complaints are
  two edges a few pixels apart.
- **Align to the start by default** (`text-align: start`, which is left in
  English and right in Arabic or Hebrew). Center only short, standalone
  content: a hero headline, a single CTA block, an empty state. Forms,
  tables, lists and long text align to the start.
- **Align numbers to the end** in tables and stat columns.
- **Align to text, not boxes.** An icon next to a label aligns with the
  label's cap height or center, not the top of the line box. In flex rows,
  `items-center` for single lines; `items-start` plus a small top margin on
  the icon for multi-line text.
- **Optical adjustments:** play icons, arrows and round shapes look off
  center when centered mathematically. Nudge by 1 to 2px after you see it.

## 5. Containers and widths

| Container | Max width | Use |
| --- | --- | --- |
| Prose | 65ch (about 640 to 720px) | articles, docs, long paragraphs |
| Narrow | 560 to 640px | forms, sign-in, focused tasks, a centered hero statement |
| Content | 1120 to 1280px | most marketing sections and app pages |
| Wide | 1440 to 1600px | dashboards, galleries, editors |
| Full bleed | 100% | backgrounds, images, product shots that should touch the edges |

- **Page gutter:** 16px on phones, 24px on tablets, 32 to 48px on desktop.
  Keep it consistent: one gutter value per breakpoint for the whole site.
- **Separate background from content width.** A section's background can run
  full bleed while its content stays in the content container.
- **Do not let text run full width** on wide screens. Images and grids can
  grow; paragraphs cannot.

## 6. Grids

- **12 columns** for marketing layouts gives you halves, thirds, quarters and
  asymmetric splits (7 and 5, 8 and 4). Asymmetric splits look more designed
  than 6 and 6.
- **Auto-filling grids for cards** so the column count follows the space:

```css
.cards { display: grid; gap: 24px; grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)); }
```

  The `min(100%, 280px)` stops overflow on screens narrower than 280px.
  `auto-fill` keeps card width steady when there are only one or two cards;
  `auto-fit` stretches the few cards to fill the row. Pick on purpose.
- **Let flexible tracks shrink.** Grid and flex children refuse to shrink
  below their content by default, which is why long text or a wide table
  overflows a dashboard. Use `minmax(0, 1fr)` for flexible tracks and
  `min-width: 0` (Tailwind `min-w-0`) on flex children that hold text:

```css
.app-shell { display: grid; grid-template-columns: 16rem minmax(0, 1fr); }
.row > .text { min-width: 0; }
```

- **Equal heights only for equal content.** Cards in one row stretch to the
  tallest by default in grid. Fine for a set of plans; wrong when one card is
  clearly the featured one.
- **Bento grids:** vary tile sizes by importance, keep one gap value, and give
  every tile a real piece of content. Empty decorative tiles look like a
  template.
- **Use subgrid** (`grid-template-rows: subgrid`) when cards in a row need
  their titles, bodies and buttons to line up with each other.

## 7. Responsive structure

Design mobile first, then add structure as space grows.

- **Breakpoints follow content, not devices.** Add one where the layout
  starts to look wrong. Tailwind's `sm 640`, `md 768`, `lg 1024`, `xl 1280`
  are fine defaults.
- **Restructure, do not just shrink.** On mobile, a three-column feature grid
  becomes one column, side-by-side text and image stack with the image
  second (or first if it carries the message), a table becomes a list of
  cards or scrolls horizontally inside its own container, a sidebar becomes
  a drawer.
- **Container queries for components** that appear in different widths (a
  card in a sidebar and in a main column):

```css
.card-wrap { container-type: inline-size; }
@container (min-width: 480px) { .card { grid-template-columns: 160px 1fr; } }
```

  In Tailwind v4: `@container` on the parent and `@md:grid-cols-2` on the child.
- **Scale spacing with the screen.** Section padding: 48px mobile, 64px
  tablet, 96px desktop. Gaps can step from 16 to 24 to 32.
- **Viewport height:** use `min-h-dvh` (or `100dvh`), not `h-screen` (`100vh`),
  for full-height layouts. `100vh` is taller than the visible area on mobile
  browsers with a toolbar, so content hides under it.
- **Safe areas** on phones with notches: `padding-bottom:
  env(safe-area-inset-bottom)` on fixed bottom bars, with
  `viewport-fit=cover` in the viewport meta tag.
- **Right-to-left languages:** use logical properties (`margin-inline-start`,
  `padding-inline`, `inset-inline-end`; Tailwind `ms-*`, `pe-*`, `start-*`)
  instead of left and right, and test with `dir="rtl"`. Mirror directional
  icons (back arrows, chevrons), not logos or every icon.
- **No horizontal page scroll, ever.** Check at 320px. The usual causes are a
  fixed width, a long word or URL, a `w-screen` element (which includes the
  scrollbar width), or a negative margin.

## 8. Tables

- **Header row** in the label role, sticky (`position: sticky; top: 0`) when
  the table scrolls, on a tinted surface or with a stronger bottom border.
- **Row height by density:** 36px compact, 44px default, 52px comfortable.
  Offer a toggle when users differ.
- **Rows separated by hairline dividers or by zebra tint, not both.**
- **Numbers end-aligned with `tabular-nums`;** text start-aligned; status
  and actions in the last columns.
- **Wide tables on mobile:** scroll horizontally inside their own container
  (`overflow-x: auto`) with the first column sticky, or switch to a stacked
  card per row. Never let a table push the page sideways.
- **Empty, loading and error states** live inside the table frame, keeping
  the header so the user knows what will appear.

## 9. Density

Match density to how often the screen is used:

- **Marketing and onboarding:** open. Few items per screen, generous space,
  large type.
- **Daily-use app screens:** compact. Rows of 36 to 44px, 8 to 12px gaps,
  14px text. People who use a screen every day want to see more at once.
- **Tables and data tools:** dense, with a density toggle if users differ.
- Do not mix densities within one panel.

## 10. Touch targets and hit areas

- **44 by 44px target** for anything tappable on touch screens, even if the
  visible icon is 16px. (WCAG 2.2 AA requires at least 24 by 24px; 44 is the
  comfortable size.) Grow the hit area with padding, or with an invisible
  pseudo-element centered on the control so the layout does not change:

```css
.icon-btn { position: relative; }
.icon-btn::before {
  content: ""; position: absolute; left: 50%; top: 50%;
  width: max(100%, 44px); height: max(100%, 44px);
  transform: translate(-50%, -50%);
}
```

- At least 8px between separate tap targets so a thumb does not hit two.

## 11. Layering

Keep a small z-index scale and use only these values:

```css
:root { --z-dropdown: 10; --z-sticky: 20; --z-overlay: 30; --z-modal: 40; --z-toast: 50; --z-tooltip: 60; }
```

Native `<dialog>` opened with `showModal()` and elements with the `popover`
attribute render in the browser's top layer, above every z-index, so they
need none. `z-index: 9999` means the stacking is not understood. Fix the stacking
context (often a stray `transform`, `filter` or `isolation` on a parent)
instead of raising the number.

## 12. Sticky and fixed elements

- Sticky headers: keep them short (56 to 64px), and give them a background
  (solid or blurred) only once the page scrolls under them, so the top of the
  page stays clean.
- Add `scroll-margin-top` equal to the header height on anchored headings so
  in-page links do not land under the header.
- Fixed bottom bars on mobile need the safe-area padding above and must not
  cover the last content on the page; pad the page bottom by the bar's height.

## 13. Check before you finish

- [ ] Every spacing value is on the 4px scale.
- [ ] Space inside groups is clearly smaller than space between them.
- [ ] More space above headings than below.
- [ ] One start edge per section; numbers end-aligned in tables.
- [ ] Flexible tracks use `minmax(0, 1fr)`; text children can shrink.
- [ ] Paragraphs capped at about 65ch, even on wide screens.
- [ ] Layout restructures on mobile instead of just shrinking.
- [ ] No horizontal scroll at 320px; full-height sections use `dvh`.
- [ ] Touch targets at least 44px (never under 24px).
- [ ] z-index values come from the scale.
- [ ] Squint test: the most important thing and the groups are clear with
      the details blurred.
