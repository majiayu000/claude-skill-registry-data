---
name: frontend-quality-guardrails
description: Use when building, modifying, or reviewing frontend UI where text overflow, layout, responsiveness, accessibility, and visual polish must be verified.
---

# Frontend Quality Guardrails

## Overview

Use this skill as a frontend quality gate for UI implementation and review. It covers long text, overflow, wrapping, truncation, alignment, spacing, responsive behavior, component states, accessibility, internationalization, visual polish, project-level code review, browser screenshot verification, and common UI style pitfalls.

Treat every UI as hostile to perfect content. Assume labels, names, URLs, IDs, prices, translated strings, user input, errors, table cells, badges, breadcrumbs, tabs, and button text can be longer than the mockup.

Prefer small, local CSS/layout fixes over broad rewrites. Preserve the existing design system, component API, tokens, spacing scale, and framework conventions unless the user asks for a redesign.

## When to Use

Use this skill when building, modifying, or reviewing frontend UI where layout quality matters, especially:

- Long text, URLs, IDs, translated strings, form errors, labels, table cells, cards, tabs, breadcrumbs, or badges may overflow.
- The task touches HTML, CSS, React, Vue, Svelte, Next.js, Tailwind, shadcn/ui, Ant Design, forms, tables, dashboards, modals, drawers, navigation, or responsive layouts.
- The user asks to polish UI, fix overflow, improve alignment, review frontend code, validate browser screenshots, or avoid frontend style pitfalls.

## Do not use

Do not use this skill as the primary guide for:

- Backend-only, CLI-only, database-only, or infrastructure tasks with no visible UI.
- Full brand identity creation, illustration, logo design, or image generation.
- Pixel-perfect implementation from a provided screenshot when a dedicated image-to-code or design reproduction skill is available.
- Accessibility audits that require formal WCAG scoring beyond implementation-level guardrails.

## Instructions

Apply the workflow below as a guardrail layer on top of the project's existing frontend conventions. For simple changes, use the core checklist only. For deeper work, load the relevant reference file from the Deep References section.

## Workflow

1. Inspect the existing UI conventions before editing:
   - Identify the framework, styling system, component library, breakpoints, typography scale, spacing tokens, and icon library.
   - Reuse existing components and utility classes.
   - Do not introduce a new design system for a localized fix.

2. Identify text risk surfaces:
   - User names, organization names, file names, paths, slugs, UUIDs, hashes, tokens, URLs, emails, phone numbers.
   - Headings, card titles, table cells, nav items, tabs, breadcrumbs, filters, chips, badges, tooltips, toasts, dialogs.
   - Form labels, placeholders, help text, validation errors, empty states, loading text.
   - Translated strings and CJK/Latin mixed content.

3. Define the intended behavior for each text container:
   - Wrap: content can take multiple lines without breaking layout.
   - Clamp: content is visually limited but full value is available elsewhere.
   - Truncate: content is shortened with ellipsis for compact repeated UI.
   - Scroll: content is intentionally scrollable, usually code, logs, tables, or panels.
   - Resize: layout adapts to content, but within stable min/max bounds.

4. Implement the smallest robust fix:
   - Add missing `min-width: 0` or `min-height: 0` in flex/grid children.
   - Add explicit `max-width`, `overflow-wrap`, `text-overflow`, `line-clamp`, or scroll behavior where needed.
   - Avoid changing parent layout unless the parent is the source of the overflow.

5. Verify with adversarial content and viewports:
   - Test narrow mobile, tablet, desktop, and wide desktop.
   - Test long unbroken strings, long natural language, CJK text, mixed CJK/English, URLs, empty values, and dense lists.
   - Use browser screenshots or DOM inspection for visual changes when feasible.

## Deep References

Load these reference files when the task needs deeper coverage:

- [code-review-checklist.md](references/code-review-checklist.md): use before editing or reviewing React, Vue, Svelte, HTML/CSS, component-library usage, stateful UI, forms, tables, or existing project code.
- [visual-standards.md](references/visual-standards.md): use when creating, redesigning, polishing, or critiquing visual style, density, hierarchy, color, radius, shadow, typography, and interaction states.
- [browser-verification.md](references/browser-verification.md): use after visible UI changes, before final response, or when debugging layout/overflow/responsive issues with browser automation, screenshots, console logs, and viewport checks.

## Text Overflow Rules

Use wrapping when users must read the content inline:

```css
.wrap-text {
  overflow-wrap: anywhere;
  word-break: normal;
  hyphens: auto;
}
```

Use truncation only when space is intentionally compact and the full value is still accessible:

```css
.truncate-one-line {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

For compact names or titles in repeated UI, prefer one-line ellipsis with full text available on hover and keyboard focus through the project's Tooltip/title pattern. Do not only "protect layout" by clipping text; the user must still be able to inspect the complete value.

Use multi-line clamping for cards, summaries, and search results:

```css
.clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

Use scroll for logs, code, long tables, and raw technical values:

```css
.scroll-panel {
  min-width: 0;
  min-height: 0;
  overflow: auto;
}
```

Avoid these traps:

- Do not rely on `overflow: hidden` alone; it hides bugs and can make content inaccessible.
- Do not apply `white-space: nowrap` to containers that may receive translated text.
- Do not use `word-break: break-all` as the default for readable prose; use `overflow-wrap: anywhere` for long unbroken tokens.
- Do not truncate form errors, critical warnings, prices, dates, or destructive action labels.
- Do not place ellipsis on inline elements without a constrained width and block/inline-block/flex behavior.
- Do not clamp text without considering keyboard focus, screen readers, and access to full content.

## Flex And Grid Pitfalls

Always check `min-width: 0` for flex/grid children that contain text:

```css
.row {
  display: flex;
}

.row__content {
  min-width: 0;
  flex: 1;
}
```

Use `minmax(0, 1fr)` in CSS Grid when columns contain long content:

```css
.grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
}
```

Guard against layout shifts:

- Give avatars, icons, buttons, table columns, and thumbnails stable dimensions.
- Use `flex: none` for icons and fixed controls next to flexible text.
- Use `gap` rather than margin hacks for repeated horizontal/vertical rhythm.
- Avoid percentage widths that combine with padding and cause overflow.
- Set `box-sizing: border-box` if the project does not already do it globally.
- Use `min-height: 0` on nested flex/grid panels that need internal scrolling.

## Alignment And Spacing

Align by visual role, not by accidental DOM order:

- Align labels and values consistently within forms, detail panels, tables, and cards.
- Align icons with text using `inline-flex`, `align-items: center`, and a stable `gap`.
- Keep icon-only buttons square and centered.
- Keep mixed icon/text controls baseline-balanced; avoid icons floating above text.
- Use the project spacing scale; do not invent one-off margins unless necessary.
- Preserve vertical rhythm between headings, body text, controls, and section boundaries.
- Do not center-align long paragraphs, tables, form labels, or dense operational UI.
- Use right alignment only for numeric values that users compare in columns.
- Use tabular numbers for metrics, prices, timers, and aligned numeric columns when available.

Prefer:

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
```

## Typography

Keep type readable and stable:

- Do not scale font size directly with viewport width.
- Avoid negative letter spacing unless the existing design system explicitly uses it.
- Use sufficient line-height for CJK and mixed-language text.
- Avoid oversized headings inside compact cards, sidebars, toolbars, tables, and modals.
- Keep button labels short but do not make them cryptic.
- Use semantic heading order even when visual size differs.
- Use font weights sparingly; hierarchy should also come from size, spacing, color, and layout.
- Test text expansion from localization; English to German, Russian, Vietnamese, Chinese, Japanese, and Korean can stress width/height differently.

Recommended starting points:

- Body text: line-height around `1.45` to `1.7`, depending on density.
- UI labels: line-height around `1.2` to `1.4`.
- Dense tables: maintain legibility before optimizing for row count.

## Responsive Layout

Design for real breakpoints, not only one desktop width:

- Check `320px`, `375px`, `768px`, `1024px`, `1280px`, and one wide desktop size when feasible.
- Avoid fixed widths that exceed small screens.
- Use `max-width: 100%` for media and text containers.
- Ensure sticky headers, sidebars, bottom bars, and floating controls do not cover content.
- Use horizontal scrolling only for content that naturally needs it, such as large tables, timelines, code, or comparison matrices.
- Keep tap targets at least roughly `44px` high/wide on mobile unless the app's dense UI standard intentionally differs.
- Ensure viewport units account for mobile browser chrome; prefer modern units like `svh`, `dvh`, or project-supported fallbacks when relevant.

For mobile:

- Stack forms and filter bars when horizontal density becomes brittle.
- Let primary actions remain reachable without covering inputs.
- Make modals fit within viewport height with internal scrolling.
- Avoid hover-only affordances.

## Component-Specific Checks

### Buttons And Controls

- Prevent label overflow with `min-width: 0` on text spans inside flexible buttons.
- Keep loading states the same size as idle states.
- Keep destructive, disabled, focus, hover, pressed, and selected states visually distinct.
- Do not hide focus outlines unless replacing them with accessible focus styles.
- Use icons for familiar tool actions when an icon library exists, with accessible labels or tooltips.

### Forms

- Keep labels visible when possible; placeholders are not labels.
- Let validation errors wrap and remain close to the field.
- Avoid layout jump when errors appear; reserve space only if the project pattern supports it.
- Ensure long option labels in selects, radio groups, checkboxes, and comboboxes wrap or truncate intentionally.
- Support autofill, disabled, readonly, required, invalid, loading, and success states.
- Do not make input text smaller than surrounding UI in a way that harms readability.

### Tables And Data Grids

- Decide per column: fixed width, flexible width, wrap, truncate, or horizontal scroll.
- Keep important identifiers readable; if truncated, provide copy or full-value access.
- Align numbers right and text left.
- Use sticky headers/columns only when they do not create clipping or z-index issues.
- Test empty, one-row, many-row, loading, error, and filtered states.
- Avoid putting complex cards inside every table cell unless the product pattern already does it.

### Cards And Lists

- Give repeated items stable structure and consistent action placement.
- Clamp summaries, not critical titles, unless full titles are available on hover/focus/detail.
- Keep badges from pushing primary content out of view.
- Ensure hover/focus styles do not resize cards.
- Avoid nested cards unless the design system explicitly uses them.

### Navigation, Tabs, And Breadcrumbs

- Test long route names and translated labels.
- Use overflow menus, scrollable tab lists, wrapping breadcrumbs, or truncation intentionally.
- Keep the active state visible when labels truncate.
- Ensure keyboard navigation remains usable.

### Modals, Drawers, Popovers, Tooltips

- Keep headers and footers stable while body content scrolls.
- Prevent popovers from clipping against viewport edges.
- Do not put critical content only in hover tooltips.
- Let dialogs handle long titles, long errors, and dense forms.
- Ensure escape, outside click, focus trap, and return focus behavior match the library pattern.

### Images, Avatars, And Media

- Set explicit aspect ratios or dimensions to prevent layout shifts.
- Use `object-fit` deliberately.
- Provide alt text for meaningful images and empty alt for decorative images.
- Test missing, slow, broken, and very large images.
- Do not crop product/person/content images so aggressively that users cannot inspect them.

## CSS And Styling Pitfalls

Avoid fragile CSS:

- Do not fix overflow by adding random `z-index`, `position: absolute`, or negative margins.
- Do not use `height: 100vh` for app shells without accounting for mobile viewport behavior.
- Do not set `overflow: hidden` on high-level layout containers unless clipping is intentional.
- Do not use global selectors that alter unrelated components.
- Do not introduce color, radius, shadow, or spacing values outside existing tokens without reason.
- Do not make text unreadable by relying on low contrast placeholder, muted, disabled, or secondary colors.
- Do not put important content behind transparent overlays or decorative layers.
- Do not let hover borders change element size; use transparent borders or shadows.
- Do not animate layout properties when transform/opacity can achieve the same effect.

Prefer robust CSS primitives:

- `box-sizing: border-box`
- `min-width: 0`
- `min-height: 0`
- `max-width: 100%`
- `overflow-wrap: anywhere`
- `text-wrap: balance` only for headings where supported and not required for correctness
- `contain`, `content-visibility`, or virtualization only when performance need is real

## Tailwind Notes

Use Tailwind utilities intentionally:

- Add `min-w-0` to flex/grid text children.
- Use `truncate` only with a constrained width.
- Use `break-words` for readable wrapping and `break-all` only for technical tokens when acceptable.
- Use `line-clamp-*` for summaries when the plugin/support exists.
- Use `overflow-x-auto` around wide tables, not on the whole page.
- Use `shrink-0` for icons/avatars and `flex-1 min-w-0` for text.
- Avoid long arbitrary-value chains when a token or existing component class exists.

Common patterns:

```tsx
<div className="flex min-w-0 items-center gap-2">
  <Icon className="size-4 shrink-0" aria-hidden="true" />
  <span className="min-w-0 truncate">Very long label</span>
</div>
```

```tsx
<div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
  <p className="min-w-0 break-words">Long readable content</p>
  <button className="shrink-0">Action</button>
</div>
```

## Component Library Notes

When using a component library:

- Read the local wrapper component before changing usage.
- Prefer library-supported props for size, status, disabled, placement, overflow, and accessibility.
- Do not override internals with brittle selectors unless there is no public API.
- For Ant Design, check `Table` column width, `ellipsis`, `scroll.x`, `Tooltip`, `Form.Item` help text, `Select` option rendering, and `Typography.Text` ellipsis behavior.
- For shadcn/ui, preserve Radix accessibility behavior and component composition; fix layout with wrapper classes before rewriting primitives.
- For MUI/Chakra/Headless UI, prefer documented slot props, style props, or composition points.

## Accessibility And Semantics

Keep UI usable beyond the happy path:

- Preserve visible focus and logical tab order.
- Use semantic elements for buttons, links, headings, lists, tables, forms, and landmarks.
- Provide accessible names for icon-only controls.
- Do not rely on color alone for errors, warnings, active states, or status.
- Ensure truncated content has an accessible path to the full value when the full value matters.
- Ensure tooltips are reachable or nonessential.
- Respect reduced motion for large or repeated animations.
- Keep contrast sufficient for normal, muted, disabled, hover, selected, and error text.

## Internationalization And Content Variability

Plan for text expansion and writing differences:

- Avoid hard-coded pixel heights for text containers that may translate.
- Do not concatenate translated fragments when grammar may differ.
- Check pluralization and variable interpolation.
- Avoid layout assumptions based on English word boundaries.
- Ensure CJK text, RTL text, diacritics, emoji, and long numbers do not break the layout.
- Use `dir`, logical CSS properties, or library RTL support when the app supports RTL.

## Visual Polish Checks

Before finishing a UI change, scan for:

- Text overlapping icons, badges, images, inputs, or adjacent sections.
- Content clipped by rounded corners, sticky bars, drawers, or hidden overflow.
- Cards or rows changing size on hover.
- Inconsistent icon sizes or stroke weights.
- Mismatched border radius within the same component group.
- Shadows or borders that make nested surfaces look accidental.
- Uneven spacing between repeated items.
- Empty states that look like broken loading states.
- Loading skeletons that do not match final layout dimensions.
- Disabled states with insufficient contrast or unclear affordance.
- Toasts, dropdowns, menus, and popovers hidden behind headers or modals.

## Required Test Content

When practical, verify with these strings:

```text
This is a normal sentence that should wrap naturally without breaking the layout.
SuperLongUnbrokenOrganizationNameWithNoSpacesAndManyCharacters1234567890
https://example.com/a/very/long/path/with/query?search=frontend-layout-overflow-and-wrapping
UserLocaleLongTextWithoutSpacesMixedWithAsciiABCDEFGHIJKLMN1234567890
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Also test:

- Empty string
- Single character
- Very long translated label
- Long number or currency value
- Long validation error
- Multiple badges or tags
- Missing image/avatar
- Loading and error states

## Verification Checklist

Do not mark the task complete until these are true for the changed surface:

- No horizontal page overflow unless intentionally required.
- No text overlaps adjacent UI.
- Long text wraps, clamps, truncates, or scrolls according to the intended behavior.
- Full critical content remains accessible.
- Flex/grid children with text have appropriate `min-width: 0` or `min-height: 0`.
- Mobile and desktop layouts remain usable.
- Loading, empty, error, disabled, hover, focus, selected, and dense-data states are covered when relevant.
- The change follows existing design tokens and component patterns.
- The UI is verified visually when a browser or screenshot workflow is available.

## Response Pattern

When reporting work done with this skill:

- Mention the specific overflow/layout risks addressed.
- Mention the verification performed.
- Call out any remaining UI risk, untested viewport, or state that could not be checked.
