---
name: responsive
description: "Use to make an existing desktop-oriented UI work on mobile and tablet, or to fix overflow, wrapping, clipping, or cramped layouts at narrow widths. Not for new UI, use ui for that."
---

# Responsive

Take a desktop layout and make it work at every width. Audit in this order: page shell, navigation, text and forms, overflow, then the component patterns.

## Steps

1. Look at the desktop layout. Find overflow, wrapping, clipping, cramped areas, desktop-only navigation, tables, forms, pagination, stat grids, and divider-separated layouts.
2. Apply mobile-first classes and breakpoint-specific layout changes.
3. Use container queries where a component's layout depends on the space it's given, not the viewport.
4. Check mobile, tablet, and desktop.
5. Run the project's format, lint, typecheck, and tests if it has them.

## Page shell and breakpoints

- Every layout adapts from mobile to desktop. Use `sm:`, `md:`, `lg:` and so on to change grid columns, spacing, font sizes, and visibility.
- Multi-column desktop layouts, sidebars, secondary nav, filter panels, collapse to one column on small screens. A mobile menu, a disclosure, or another compact pattern. Never shrunken columns.
- Use `min-h-dvh`, `min-h-svh`, or `min-h-lvh`. Never `min-h-screen`.

## Navigation and pagination

- Every app has a mobile navigation menu below `lg`, whether the desktop nav is in a header or a sidebar. A dialog or disclosure panel with a hamburger. Hide header nav with `hidden lg:flex`, sidebar nav with `hidden lg:block`, and the mobile toggle and menu at desktop widths with `lg:hidden`.
- Horizontal menus, tabs, tab bars, pill navs, never overflow their parent. Scroll horizontally when items don't fit.
- When pagination has both page numbers and previous and next, hide the page numbers on mobile.

## Text, forms, and touch targets

- Body text, subheadings, form controls, and icons are larger on mobile and scale down at `sm:`. Write the mobile size as the default and the desktop size with `sm:`. `text-2xl/8 sm:text-xl/8`, `text-base/7 sm:text-sm/6`, `text-lg/6 sm:text-sm/6`, `size-5 sm:size-4`, `py-2.5 sm:py-1.5`. This covers body text, subheadings, stat values, labels, badges, buttons, select and input padding, and icons. Not h1s. Page titles stay the same or get smaller on mobile.
- Body and paragraph text is at least `text-base` (16px) on mobile. Never `text-xs`. `text-sm` only at `sm:` or above, so `text-base/7 sm:text-sm/6`, never a bare `text-sm/6` for body copy.
- If a text input's font is under `16px`, add `max-sm:text-base/{lh}` to lift it to 16px on mobile.
- Checkboxes, radios, and toggles are larger on mobile. `size-5 sm:size-4` for checkboxes and radios, `w-11 sm:w-9` for toggles.
- Small and icon buttons meet the 48x48px touch target. Make the button `relative` and add a direct child `<span class="absolute top-1/2 left-1/2 size-[max(100%,3rem)] -translate-1/2 pointer-fine:hidden" aria-hidden="true" />` when the visual button is smaller.
- Never fix a cramped heading group by constraining the wrapper with `max-w-*` or `max-lg:max-w-*`. Constrain each text element with `max-w-[*ch]`.

## Overflow and flexible sizing

- Add `min-w-0` to any flex child that has to shrink below its content. Fluid content beside a fixed sidebar, truncated labels, a flexible input beside a fixed button.
- Add `shrink-0` to any flex child that must not compress. Icons, SVGs, images, logos, avatars, fixed-size controls.
- Tables scroll horizontally when the columns won't fit. Wrap in an outer `overflow-x-auto whitespace-nowrap` div with negative margins matching the container, and an inner `inline-block min-w-full align-middle` div with matching horizontal padding.
- Table headings never wrap. `whitespace-nowrap` on every `<th>`.

## Component patterns

- Use container queries, `@container`, for anything whose layout depends on available space rather than the viewport. Dashboard widgets, feature cards, pricing tiers, testimonial grids.
- Put the `@container` element as close to the responsive content as you can. A direct wrapper around the items. Never a page-level container.
- Dashboard widgets use container queries, not media queries. Truncate stat and metric card titles so they never wrap.
- Divider-separated grids get reconfigured at every breakpoint where the column count changes. Reset first and last item padding, drop vertical dividers when collapsing to one column, add horizontal dividers between rows.
- Wrapped logo clouds stay balanced at every breakpoint. Use a grid or layout that avoids an uneven last row like `5+1`.
- Pricing card emphasis uses breakpoint-scoped grid rows and columns. Below that breakpoint the cards stack normally.
- Image and screenshot border radius uses `min()` with viewport units instead of a fixed `rounded-*`. `rounded-[min(1vw,12px)]`.

## Check

Narrow, medium, and desktop all work. Mobile navigation exists and desktop navigation is hidden below `lg`. Tables, tabs, pagination, form controls, stat grids, and divider grids all behave on a narrow screen.
