---
name: qa-detect-viewport-parity
section: responsiveness
description: "Detects features/columns/actions present on desktop but silently dropped on mobile/tablet (lost functionality, not just relocated into a drawer)"
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: true
interactive: true
---

# qa-detect-viewport-parity

## What it checks
Whether the **set of features** a user can reach shrinks on a smaller viewport. A responsive layout may *move* things (sidebar → hamburger, columns → cards) — that's fine. The bug is when a feature is **gone**: a table column, a filter, a primary action, a nav destination that exists on desktop and simply isn't reachable on mobile/tablet.

This is an **interactive** skill — it uses `browser_resize` to compare the current viewport against desktop within the same cell. Deterministic set‑difference → Haiku. Ambiguous (only secondary items missing) → `uncertain: true` → Sonnet escalation.

## Self-skip
Skip (no findings) if the page has fewer than 4 interactive features total (nothing meaningful to compare) or is an error/empty page.

## Orchestrator flow
1. **Small-viewport inventory** (current cell viewport = mobile or tablet): run `probe.inventory` → `invSmall`.
2. **Reveal the drawer** so relocated items don't count as missing: if a mobile-nav toggle exists (`[aria-label*="menu" i], button.hamburger, [class*="hamburger"], [class*="menu-toggle"], button[aria-controls]`), `browser_click` it, wait 400ms, run `probe.inventory` again, merge into `invSmall`, then close it (`browser_press_key Escape`).
3. **Desktop inventory:** `browser_resize(1440, 900)`, wait 500ms, run `probe.inventory` → `invDesktop`.
4. **Restore:** `browser_resize` back to the cell's original width/height.
5. **Diff:** `missing = invDesktop.filter(x => !invSmall.includes(x))`.
   - `missing` contains a **column** (`col:` prefix) or a primary action (`btn:` with add/create/save/submit/export/filter/search/download) → `featureHiddenOnSmallViewport` (high).
   - `missing` has ≥1 other interactive item → `featureHiddenOnSmallViewport` (medium).
   - `missing` is only 1–2 clearly-secondary items (footer link, "print") → emit with `uncertain: true` (let Sonnet decide if it's intentional).
   - `missing` empty → clean (no finding).
   Include the missing labels in the description.

## Probe (browser_evaluate)
```js
// probe.inventory — a stable signature of reachable features at the current width
() => {
  const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase().slice(0, 50);
  const visible = el => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return (r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none') || cs.position === 'fixed';
  };
  const out = new Set();
  // interactive actions + nav destinations
  document.querySelectorAll('a[href], button, [role=button], [role=link], [role=menuitem], [role=tab]').forEach(el => {
    if (!visible(el)) return;
    const name = norm(el.getAttribute('aria-label') || el.textContent || el.getAttribute('title'));
    if (name.length >= 2 && name.length <= 50 && !/^[\d\s.,/-]+$/.test(name)) out.add('btn:' + name);
  });
  // form fields
  document.querySelectorAll('input:not([type=hidden]), select, textarea').forEach(el => {
    if (!visible(el)) return;
    const name = norm(el.getAttribute('aria-label') || el.getAttribute('name') || el.getAttribute('placeholder'));
    if (name.length >= 2) out.add('field:' + name);
  });
  // table columns
  document.querySelectorAll('th, [role=columnheader]').forEach(el => {
    if (!visible(el)) return;
    const name = norm(el.textContent);
    if (name.length >= 1) out.add('col:' + name);
  });
  return [...out].sort();
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| featureHiddenOnSmallViewport | high | A table column or primary action available on desktop is not reachable on {viewportClass}: {missing labels} |
| featureHiddenOnSmallViewport | medium | Feature(s) available on desktop are missing on {viewportClass} (not in the mobile menu either): {missing labels} |

## Notes
- The drawer-merge step (2) is what prevents false positives from items that simply moved into the hamburger menu.
- `uncertain: true` routes the borderline "is this intentional responsive hiding?" call to the escalation model.
- Cross-viewport comparison is contained within ONE cell via resize — no cross-cell state needed.
