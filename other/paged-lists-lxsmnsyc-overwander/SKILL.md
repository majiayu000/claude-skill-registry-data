---
name: paged-lists
description: >
  Any list that can grow without bound is paged, never drawn whole.
  Lists of rows page at LIST_PAGE (20) through createPager from
  src/components/styled/pager.tsx; grids of squares page at their grid
  size (BOX_SIZE for the pokemon box, GRID_SIZE for the item tray).
  Applies whenever rendering a collection whose length the player
  controls.
---

# Paged lists

A `For` over a whole collection is a bug waiting for the player who
accumulates: battles, bids, friends and gifts all grow forever, and a
fixed grid handed more entries than it draws silently hides the rest.

## The pager

`createPager(items, size, unit?)` in `src/components/styled/pager.tsx`
owns the whole pattern: the page signal, the slice, the arrow controls,
and the clamp that pulls the page back when the list shrinks under the
reader (a search narrowed, a row settled). Use it instead of a local
`page`/`setPage` pair.

`size` is a number or an accessor. Pass an accessor wherever the player
can change how much fits on a page, or the last row of every page goes
missing when they do.

```tsx
const paged = createPager(() => rows(), LIST_PAGE);
// …
<For each={paged.shown()}>{(row) => …}</For>
{paged.controls()}
```

- `paged.shown()` is the slice to render.
- `paged.controls()` draws `‹ Page x of y ›` only when there is more
  than one page — render it unconditionally after the list.
- The third argument names the unit: boxes of pokemon say `'Box'`.

## Sizes

- Lists of text rows: `LIST_PAGE` (20), exported next to the pager.
- The pokemon box: `boxSizeOf(settings().boxColumns)`. The player sets
  the box five, six or eight wide, so its page is an accessor rather
  than the `BOX_SIZE` constant, which is only the default six by five.
- The item tray pages itself at `GRID_SIZE` inside `ItemGrid`; do not
  page around it.

## Grids of squares

Pokemon squares get their furniture from `CatchGrid`
(`src/components/catches/CatchGrid.tsx`) — search, box paging and
empty states over a bare `CatchBox` — the way items get theirs from
`ItemGrid`. Feed it `{ square, caught }` entries; pass `bare` when the
caller narrows with its own search, or `search`/`onSearch` when the
query also drives a store read. Never hand a raw `CatchBox` an
unpaged list.

## Never truncate silently

A component with a fixed number of slots (`CatchBox` draws exactly
`BOX_SIZE` squares) must be fed a page, not the whole list: entries
past the last slot are not drawn, not announced, and not reachable.
