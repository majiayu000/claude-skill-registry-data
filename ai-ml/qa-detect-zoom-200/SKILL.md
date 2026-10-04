---
name: qa-detect-zoom-200
section: responsiveness
description: "WCAG 1.4.4 — verifies text and layout remain functional at 150% zoom (OS Display Scale approximation) and 200% zoom. Detects overflow, clipped text, and inaccessible content at both zoom levels. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive the two zoom passes with separate `browser_evaluate` round-trips. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function runs BOTH passes in-page: it sets `document.body.style.zoom = '1.5'`, waits, scans (150% — OS Display Scale approximation), resets, then sets `'2'`, waits, scans (200% — WCAG 1.4.4), and **resets zoom** before returning `findings[]` — all inside the page, in one round-trip. The zoom reset is guaranteed via `finally`, so no downstream skill runs at the wrong zoom. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const selFn = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0, 120);
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── Visibility guard: an element is only a real defect if a sighted user
  //    can actually see it. Skip display:none / visibility:hidden / opacity:0 /
  //    aria-hidden / inert / off-canvas drawers / collapsed navs (rect entirely
  //    outside the viewport box on left/top, i.e. translated/positioned away).
  const isRendered = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || s.visibility === 'collapse') return false;
    if (parseFloat(s.opacity || '1') === 0) return false;
    if (el.closest('[aria-hidden="true"],[hidden],[inert]')) return false;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    // Off-canvas: rect lies wholly to the left of, or above, the viewport
    // (the classic closed-drawer / collapsed-sidebar / hidden-menu pattern).
    if (r.right <= 0 || r.bottom <= 0) return false;
    // Drawer/menu ancestor that is collapsed via transform off the left edge.
    let p = el;
    while (p && p !== document.body) {
      const ps = getComputedStyle(p);
      const t = ps.transform;
      if (t && t !== 'none') {
        const pr = p.getBoundingClientRect();
        // Ancestor translated entirely (or almost entirely) off-screen left → collapsed drawer.
        if (pr.right <= 1) return false;
      }
      p = p.parentElement;
    }
    return true;
  };

  // Does the page actually have a horizontal scrollbar the user can/ must use?
  const pageScrolls = () => document.documentElement.scrollWidth > window.innerWidth + 4;

  const scanAtZoom = (label) => {
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const is200 = label === '200%';
    const hasHScroll = pageScrolls();

    // 1. Horizontal scroll at zoom
    if (document.documentElement.scrollWidth > vw + 4) {
      out.push({ skill: 'qa-detect-zoom-200', issueType: 'zoomOverflow', severity: 'high', selector: 'html',
        description: `Page requires horizontal scrolling at ${label} zoom${is200 ? ' — WCAG 1.4.4 violation' : ' (OS Display Scale approximation)'}. scrollWidth ${document.documentElement.scrollWidth}px vs viewport ${vw}px`,
        bbox: { x: 0, y: 0, w: 200, h: 80 } });
    }

    // 2. Fixed OVERLAY that covers the main content and blocks interaction.
    //    A tall fixed/sticky element is only a defect if it (a) is rendered,
    //    (b) overlaps the viewport CENTER (i.e. sits over content, not a normal
    //    full-height side rail), and (c) is itself NOT internally scrollable
    //    (a scrollable panel doesn't block access to its own content).
    let fixedCount = 0;
    const cx = vw / 2, cy = vh / 2;
    for (const el of document.querySelectorAll('*')) {
      if (fixedCount >= 10) break;
      const style = getComputedStyle(el);
      if (style.position !== 'fixed' && style.position !== 'sticky') continue;
      if (!isRendered(el)) continue;                 // visibility guard
      const r = el.getBoundingClientRect();
      if (r.height <= vh * 0.5) continue;            // must be oversized
      // Must actually sit over the content center (an overlay), not be a side rail.
      const coversCenter = r.left <= cx && r.right >= cx && r.top <= cy && r.bottom >= cy;
      if (!coversCenter) continue;
      // Internally scrollable panels (modals, drawers with their own scroll) are not "blocking".
      const scrollableSelf = (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight + 4;
      if (scrollableSelf) continue;
      fixedCount++;
      out.push({ skill: 'qa-detect-zoom-200', issueType: 'zoomFixedElementOversized', severity: 'high', selector: selFn(el),
        description: `Fixed/sticky ${selFn(el)} occupies ${Math.round((r.height/vh)*100)}% of viewport and overlays page content at ${label} zoom — blocks content access`,
        bbox: bb(el) });
    }

    // 3. Interactive elements pushed offscreen to the right AND truly unreachable.
    //    Only a real WCAG 1.4.4 defect if the element is rendered (not in a closed
    //    drawer/collapsed nav), its LEFT edge is past the right viewport edge, AND
    //    the page provides NO horizontal scroll to reach it. If the page scrolls
    //    horizontally that is already reported by zoomOverflow (#1) — not double-counted here.
    // An element is "off-screen" only because its whole PANEL (off-canvas settings drawer,
    // sidebar, modal, dropdown, collapse) is parked off-screen in its CLOSED state — it opens
    // on demand, so the control IS reachable. That is NOT a zoom defect. isRendered() doesn't
    // catch it because the element has size + visibility; the giveaway is that a PANEL ANCESTOR
    // is itself entirely off-screen / hidden. Skip those. (Fixes the settingSidebar toggle
    // false positives — closed-drawer contents flagged as "unreachable at zoom".)
    const inClosedPanel = (node) => {
      for (let a = node.parentElement; a && a !== document.body; a = a.parentElement) {
        const acs = getComputedStyle(a);
        if (a.getAttribute('aria-hidden') === 'true' || a.hasAttribute('hidden') ||
            acs.display === 'none' || acs.visibility === 'hidden') return true;
        if (/offcanvas|drawer|sidebar|settingsidebar|side-?panel|slide|\bmodal\b|\bfade\b|dropdown|collapse|popover/i.test((a.className || '').toString())) {
          const ar = a.getBoundingClientRect();
          if (ar.width === 0 || ar.left > vw - 4 || ar.right < 4) return true;   // panel itself parked off-screen / closed
        }
      }
      return false;
    };
    let offCount = 0;
    for (const el of document.querySelectorAll('button, a, input, [role="button"]')) {
      if (offCount >= 15) break;
      if (!isRendered(el)) continue;                 // visibility guard
      const r = el.getBoundingClientRect();
      const clippedRight = r.left > vw - 4;          // left edge at/past right viewport edge
      if (!clippedRight) continue;
      if (inClosedPanel(el)) continue;               // 🚫 closed off-canvas drawer/panel → reachable when opened, not a zoom defect
      if (hasHScroll) continue;                       // reachable via horizontal scroll → not unreachable
      offCount++;
      out.push({ skill: 'qa-detect-zoom-200', issueType: 'zoomElementUnreachable', severity: 'medium', selector: selFn(el),
        description: `Interactive element sits at x=${Math.round(r.left)}px (past the ${vw}px right edge) at ${label} zoom and the page offers no horizontal scroll — unreachable`,
        bbox: bb(el) });
    }
  };

  const prevZoom = document.body.style.zoom || '';
  try {
    // Pass 1 — 150% zoom (OS Display Scale approximation)
    document.body.style.zoom = '1.5';
    await sleep(400);
    scanAtZoom('150%');
    document.body.style.zoom = prevZoom;
    await sleep(200);

    // Pass 2 — 200% zoom (WCAG 1.4.4)
    document.body.style.zoom = '2';
    await sleep(500);
    scanAtZoom('200%');
  } finally {
    // ── reset zoom (MANDATORY — runs even if a scan threw) ──
    document.body.style.zoom = prevZoom;
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| zoomOverflow | high | "Page requires horizontal scroll at {label} zoom — WCAG 1.4.4 violation / OS Display Scale issue" |
| zoomFixedElementOversized | high | "Fixed/sticky element covers >50% of viewport at {label} zoom — blocks content access" |
| zoomElementUnreachable | medium | "Interactive element offscreen at {label} zoom" |

**Note:** 150% pass approximates Windows Display Settings at 125–150% scale. Issues appearing only at 150% (not 200%) are severity `medium` — they affect enterprise users but not strict WCAG compliance.

## Notes on this conversion
- The old multi-probe playbook (applyZoom → scanAtZoom → resetZoom, twice) is folded into ONE async `browser_evaluate` call that runs both passes in-page. Same checks, same issueTypes.
- Zoom is applied/reset via `document.body.style.zoom` entirely in-page — no real browser zoom or resize is needed, so this runs as a single round-trip with `executable: true`.
- Zoom reset is in a `finally` block, so the page is never left zoomed even if a scan throws.
