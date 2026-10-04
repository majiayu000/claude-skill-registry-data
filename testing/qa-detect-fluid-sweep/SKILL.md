---
name: qa-detect-fluid-sweep
section: responsiveness
description: "Resize-sweeps the page across a range of widths (incl. in-between 600/900/1100 and extremes 320/1920) to catch fluid-layout breaks that only happen BETWEEN standard breakpoints"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: true
---

# qa-detect-fluid-sweep

## What it checks
Layout breakage at widths that aren't a standard device size and aren't a declared `@media` breakpoint — where fluid (flex/grid/%) layouts silently overflow or collapse. Existing breakpoint skills only test AT `@media` edges; this sweeps the continuum, including the **in-between widths people actually use** (600, 900, 1100) and the **extremes** (320 smallest phone, 1920 large desktop) that aren't in the cell matrix.

**Interactive** (uses `browser_resize`) and **runs once per route** (`viewportSensitive: false` → leader cell only) — it tests all widths itself, so it doesn't need to run on every viewport cell. Deterministic overflow comparison → Haiku.

## Self-skip
Never self-skips on a normal page; skip only on error/empty pages.

## Orchestrator flow
1. Record the cell's original `{width, height}`.
2. For each `w` in `[320, 360, 414, 600, 768, 900, 1100, 1280, 1440, 1920]`:
   - `browser_resize(w, 900)`
   - `browser_wait_for({ time: 300 })`
   - run `probe.overflowAt` → `{ overflow, worst }`
   - record `{ w, overflow, worst }`
3. `browser_resize` back to the cell's original size.
4. For each width with `overflow > 4`:
   - `w` ∈ {600, 900, 1100} (a non-standard, non-device width) → `fluidOverflowAtWidth` (high) — the layout breaks at a width with no breakpoint protecting it.
   - `w` ∈ {320, 1920} (extreme not in the cell matrix) → `fluidOverflowAtExtreme` (high for 320, medium for 1920).
   - other widths → `fluidOverflowAtWidth` (medium).
   - Collapse adjacent widths that share the same `worst` selector into ONE finding spanning the range (e.g. "overflows from 600–900px on `div.table-wrap`").
5. **Wrap-jump (optional):** if a flex/grid container's child count per visible row changes by >1 between two adjacent widths AND overflow appears at the lower one → include as evidence (the wrap point is the break).

## Probe (browser_evaluate)
```js
// probe.overflowAt — page overflow + worst offending element at the current width
() => {
  const de = document.documentElement;
  const vw = de.clientWidth;
  const overflow = de.scrollWidth - vw;
  let worst = null, max = vw + 4;
  if (overflow > 4) {
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.overflowX === 'hidden' || cs.position === 'fixed') continue;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > max) {
        max = r.right;
        const cls = (typeof el.className === 'string' && el.className.trim())
          ? '.' + el.className.trim().split(/\s+/)[0] : '';
        worst = el.tagName.toLowerCase() + cls;
      }
    }
  }
  return { overflow: Math.round(overflow), worst };
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| fluidOverflowAtWidth | high | Layout overflows at {w}px (an in-between width with no @media breakpoint): {worst} extends {overflow}px past the viewport |
| fluidOverflowAtExtreme | high | Layout overflows at 320px (smallest phones): {worst} overflows {overflow}px |
| fluidOverflowAtExtreme | medium | Layout overflows at 1920px (large desktop): {worst} overflows {overflow}px |

## Notes
- Run once per route (leader cell) — the sweep covers all widths internally, so enabling it does NOT multiply cell count by viewport.
- This complements `qa-detect-breakpoint-edge` (tests AT @media edges) by testing the gaps between them.
- Always restore the original viewport in step 3 so later skills on the leader cell see the expected size.
