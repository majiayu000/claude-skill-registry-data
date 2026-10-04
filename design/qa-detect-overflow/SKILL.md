---
name: qa-detect-overflow
section: responsiveness
description: "Detects horizontal content overflow on any element"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it checks
- `horizontalOverflow` — container `scrollWidth > clientWidth` by ≥ 20px: element causes horizontal page scroll
- `badgeClippedAtEdge` — badge/pill/status chip whose right edge exceeds the visible boundary of its nearest scrollable ancestor — text is cut off ("PEND" instead of "PENDING") at initial scroll position
- `tableLastColumnClipped` — table with horizontal overflow where the rightmost column (action buttons, status badges) is already partially hidden at scroll position 0 — users don't know to scroll right

Small component-internal deltas (< 20px) from CSS framework toggles, MDC components,
Bootstrap buttons, etc. are intentionally ignored — they do not cause visible page scroll.

## Probe (browser_evaluate)
```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.')
      : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // Returns true if any ancestor (up to <html>) clips overflow-x,
  // meaning the user will never see this element's overflow as horizontal scroll.
  const ancestorClips = el => {
    let node = el.parentElement;
    while (node && node !== document.documentElement) {
      const ox = getComputedStyle(node).overflowX;
      if (ox === 'hidden' || ox === 'clip') return true;
      node = node.parentElement;
    }
    return false;
  };

  for (const el of document.querySelectorAll('*')) {
    if (out.length >= 20) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;

    // Skip elements that clip their own overflow
    const ox = getComputedStyle(el).overflowX;
    if (ox === 'hidden' || ox === 'clip') continue;

    // Require a meaningful delta — ignore tiny CSS-framework internal layout noise
    // (e.g. MDC switch track, Bootstrap toggle at 26px vs 20px).
    // 20px minimum catches real container overflows while skipping component math.
    const delta = el.scrollWidth - el.clientWidth;
    if (delta < 20) continue;

    // Skip if a parent clips the overflow — user never sees horizontal scroll
    if (ancestorClips(el)) continue;

    out.push({
      issueType: 'horizontalOverflow',
      severity: 'high',
      selector: sel(el),
      description: `Horizontal overflow on ${sel(el)}: scrollWidth ${el.scrollWidth}px > clientWidth ${el.clientWidth}px`,
      bbox: bb(el)
    });
  }
  // 2. badgeClippedAtEdge — badge/pill/status chip whose rendered right edge exceeds
  // the visible right boundary of its nearest scrollable ancestor.
  // E.g. a table has overflow-x:auto; inside, a "PENDING" status badge renders at
  // x=420 but the container visible width is 380px — badge shows as "PEND" (clipped).
  // This is distinct from horizontalOverflow: the badge IS within the scroll content
  // width but is visually cut at the initial (unscrolled) viewport position.
  const BADGE_SEL = '.badge,[class*="badge"],[class*="status-badge"],[class*="status-pill"],[class*="status-chip"],[class*="pill"],[class*="chip"],[class*="tag-badge"],[class*="label-chip"],[class*="p-tag"],[class*="p-badge"]';
  const findScrollAncestor = el => {
    let node = el.parentElement;
    while (node && node !== document.documentElement) {
      const ox = getComputedStyle(node).overflowX;
      if (ox === 'auto' || ox === 'scroll') return node;
      node = node.parentElement;
    }
    return null;
  };
  let badgeFlagged = 0;
  for (const badge of document.querySelectorAll(BADGE_SEL)) {
    if (badgeFlagged >= 5 || out.length >= 20) break;
    const br = badge.getBoundingClientRect();
    if (br.width === 0 || br.height === 0) continue;
    const scrollAncestor = findScrollAncestor(badge);
    const rightBoundary = scrollAncestor
      ? scrollAncestor.getBoundingClientRect().right
      : window.innerWidth;
    // Badge is clipped if its right edge extends past the visible container right edge
    if (br.right > rightBoundary + 2) {
      badgeFlagged++;
      const badgeText = (badge.innerText || '').trim();
      out.push({
        issueType: 'badgeClippedAtEdge', severity: 'high',
        selector: sel(badge),
        description: `Status badge "${badgeText}" is clipped at the container's right edge (badge right=${Math.round(br.right)}px, container visible right=${Math.round(rightBoundary)}px, clipped by ${Math.round(br.right - rightBoundary)}px). Users see truncated text ("PEND" instead of "PENDING"). Fix: ensure the table column has min-width large enough for the badge, or add a horizontal scroll indicator so users know to scroll right.`,
        bbox: bb(badge)
      });
    }
  }

  // 3. tableLastColumnClipped — table with horizontal overflow where the LAST column
  // (rightmost — typically Actions or Status) is partially or fully hidden at scroll
  // position 0 (before user scrolls). Users don't know the column exists.
  // Distinct from horizontalOverflow: this specifically flags tables where the hidden
  // content is an important column, not just container-level overflow counting.
  let tableColFlagged = 0;
  const TABLE_SEL = 'table,[role="table"],[role="grid"],[class*="p-datatable"],[class*="datatable"],[class*="data-table"],[class*="ag-root"],[class*="table-wrapper"]';
  for (const table of document.querySelectorAll(TABLE_SEL)) {
    if (tableColFlagged >= 3 || out.length >= 20) break;
    const tr = table.getBoundingClientRect();
    if (tr.width === 0) continue;
    // Only flag if the table actually has meaningful horizontal overflow
    if (table.scrollWidth <= table.clientWidth + 5) continue;
    // Find the nearest scroll container (may be the table itself or a wrapper)
    const scrollEl = (() => {
      const ox = getComputedStyle(table).overflowX;
      if (ox === 'auto' || ox === 'scroll') return table;
      const parent = table.parentElement;
      if (parent) {
        const pox = getComputedStyle(parent).overflowX;
        if (pox === 'auto' || pox === 'scroll') return parent;
      }
      return null;
    })();
    if (!scrollEl) continue;
    const containerRight = scrollEl.getBoundingClientRect().right;
    // Find the last rendered column header
    const headers = [...table.querySelectorAll('thead th, thead [role="columnheader"], [class*="p-column-header"]:first-child ~ [class*="p-column-header"]')];
    const lastTh = headers[headers.length - 1];
    if (!lastTh) continue;
    const lhr = lastTh.getBoundingClientRect();
    if (lhr.right > containerRight + 5) {
      tableColFlagged++;
      const colName = (lastTh.innerText || '').trim().slice(0, 30) || 'last column';
      out.push({
        issueType: 'tableLastColumnClipped', severity: 'high',
        selector: sel(table),
        description: `Table column "${colName}" (rightmost — typically Actions/Status) is clipped at scroll position 0: column right=${Math.round(lhr.right)}px, container visible right=${Math.round(containerRight)}px. Users don't know to scroll right and can't see action buttons or status badges. Add a scroll shadow/fade on the right edge to signal hidden content.`,
        bbox: bb(lastTh)
      });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| horizontalOverflow | high | "Horizontal overflow on {selector}: scrollWidth {sw}px > clientWidth {cw}px" |
| badgeClippedAtEdge | high | "Status badge '{text}' clipped at container right edge (badge={N}px, boundary={N}px, clipped by {N}px)" |
| tableLastColumnClipped | high | "Table column '{col}' (rightmost) is clipped at scroll position 0 — users don't know to scroll right" |
