---
name: portfolio-project-overlay-tabs
description: "Use when changing the project detail overlay (the atlas 'island') in the D:/AlexMollard portfolio - ProjectCaseStudy, TechSpecs or ProjectMedia, the case-study tabs, tab focus or Escape handling, image zoom, tabs wrapping on mobile, an event listener in the case-study template that never fires - or when a project detail view reads as word vomit."
---

# Project detail overlay — D:/AlexMollard

Astro 6 + Tailwind v4 static portfolio. One page: `src/pages/index.astro`.

## Architecture (the trap)

Each project card renders `ProjectCaseStudy.astro`, whose entire output is a
`<template class="atlas-island-template">`. Opening a card does:

```js
islandContent.innerHTML = '';
islandContent.appendChild(template.content.cloneNode(true));
```

Consequences:
- **No inline listeners in the template** — they are cloned, not bound. All
  interactivity must be event delegation on `#atlas-island-content`, declared in
  the `<script is:inline>` at the bottom of `index.astro`.
- `id` collisions across cards are safe: `<template>.content` is an inert
  DocumentFragment, so duplicate ids only exist once in the live document.
- The template is cloned fresh on every open, so server-rendered initial state
  (e.g. `hidden` on inactive tab panels, `aria-selected` on the first tab) is the
  reset — no JS init needed on open.

## Layout: tabs, not one long column

Content volume is the real problem (AetherCore: 9 paragraph-length features,
8 metrics, role/problem/5 approach bullets/4 outcomes, 4 body paragraphs).
Current structure:

- `.case-study-head` — eyebrow, title, chips, repository link, `role="tablist"`.
  Sticky only from `@media (min-width: 768px)`; static on mobile so it does not
  eat ~290px of an 844px viewport. Tabs `flex-wrap: wrap` (horizontal scroll
  hides the last tab on a 390px screen with no affordance).
- `.case-study-panel[data-case-panel]` — one per tab, inactive ones carry the
  `hidden` attribute; `[hidden] { display: none }` must be explicit because
  Tailwind display utilities would otherwise win.
- Tabs computed in frontmatter and filtered by `show`, so projects without
  approach/notes/media do not get empty tabs. Label flips `Approach`→`Notes`
  when only the markdown body exists.
- `hasNotes` is passed from `index.astro` as `Boolean(project.body?.trim())` —
  the component cannot measure `<Content />`.
- Two-column grids are conditional (`splitOverview`, `splitStory`): a single
  populated column must span full width, not sit at half width.

Shell is `bg-surface` so `.case-study-block` (`bg-raised`) reads as raised.
`.atlas-island-shell` is a flex column; `.atlas-island-scroll` is
`flex:1; min-height:0; overflow-y:auto`.

**Never `features.join(' • ')`.** Long feature/metric arrays render as
`.case-study-list` bullets in a 2-column grid.

## Verification loop (headless, no guessing)

```
npm run dev            # background job; localhost:4321
```

Drive with the browser tool, `#aethercore` is the AetherCore spotlight card:

```js
await page.click('#aethercore .case-study-toggle');
// per tab: click [data-case-tab="technical"], then measure
sc.scrollHeight - sc.clientHeight   // overflow per panel; target ~0
```

Checks that have caught real defects:
- overflow per tab at 1600×1000 (pre-fix: one ~4000px scroll)
- `document.activeElement.dataset.caseTab` after open (focus lands on tab)
- ArrowRight → `aria-selected` + focused + only one panel unhidden
- click an `img` → `#atlas-image-preview` shown; Escape closes preview first,
  second Escape closes the island, focus returns to `.case-study-toggle`,
  `body.atlas-island-open` removed
- 390×844: `rail.scrollWidth - rail.clientWidth === 0`, all tabs inside the rail,
  `documentElement.scrollWidth - clientWidth === 0`
- sticky: set `islandContent.scrollTop = 180`, head `getBoundingClientRect().top`
  must not move (only valid at ≥768px width)

Finish with `npm run build` (catches Astro/TS prop errors; ~3s), then stop the dev job
and re-run these checks on `npm run preview` before claiming anything: the dev server is
for iterating, claims come from the built site.

## Toggle label contract

Card buttons carry `data-closed-label` (`Read case study` / `More Info`);
open sets text to `Opened`, `closeIsland()` restores from the dataset. Any
rewrite of the open/close handlers must keep both halves.
