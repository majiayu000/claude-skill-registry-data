---
name: qa-detect-overflow-controls
section: responsiveness
description: "Detects tab strips, segmented controls, and button groups whose children overflow horizontally without a visible scroll affordance"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasScrollContainers]
---

## What it checks

Horizontal control strips (tabs, segmented buttons, breadcrumbs, toolbars) often overflow at narrow widths. If the container has neither `overflow-x: auto` nor a visible scroll affordance (arrows, indicators), users have no way to reach controls past the right edge.

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const out = [];

  // Candidates: containers that look like horizontal control strips
  const candidates = document.querySelectorAll(
    '[role="tablist"], ' +
    '[class*="tab-list"], [class*="tabs"]:not(table):not(tr), [class*="tab-bar"], ' +
    '[class*="segmented"], [role="group"][aria-label*="segment" i], ' +
    '[class*="button-group"], [class*="btn-group"], ' +
    '[class*="breadcrumb"], [aria-label*="breadcrumb" i], ' +
    '[class*="toolbar"], [role="toolbar"]'
  );

  for (const el of candidates) {
    if (out.length >= 10) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;

    // Does its content overflow?
    const overflows = el.scrollWidth > el.clientWidth + 2;
    if (!overflows) continue;

    const style = getComputedStyle(el);
    const hasScrollX = style.overflowX === 'auto' || style.overflowX === 'scroll';

    // Has a visible scroll affordance? (next/prev arrows, gradient indicators)
    const hasArrow = !!el.querySelector(
      '[aria-label*="next" i], [aria-label*="prev" i], [aria-label*="scroll" i], ' +
      '[class*="scroll-arrow"], [class*="scroll-indicator"], [class*="chevron"]'
    );

    if (!hasScrollX && !hasArrow) {
      out.push({
        issueType: 'overflowControlsNoScroll',
        severity: 'high',
        selector: sel(el),
        description: `Control strip ${sel(el)} overflows (scrollWidth ${el.scrollWidth}px > clientWidth ${el.clientWidth}px) and has neither overflow-x:auto nor a visible scroll arrow — items past the right edge are unreachable`,
        bbox: bb(el)
      });
    } else if (hasScrollX && !hasArrow) {
      // Has scroll but no visual indicator — users don't know they can scroll
      out.push({
        issueType: 'overflowControlsNoIndicator',
        severity: 'low',
        selector: sel(el),
        description: `Control strip ${sel(el)} is scrollable but has no visible indicator (arrow, gradient) — users may not realize there are more items`,
        bbox: bb(el)
      });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| overflowControlsNoScroll | high | "Tab/segmented control strip overflows with no scroll-x and no scroll arrow — items past the right edge unreachable" |
| overflowControlsNoIndicator | low | "Scrollable control strip has no visible scroll indicator — users may miss hidden items" |
