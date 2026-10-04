---
name: qa-detect-ux-overlap
section: visual
description: "Detects visible elements that physically overlap each other on screen — toolbar buttons sitting on top of table headers, calendar text collision, modal partially behind another modal, sticky banner covering content. Catches the 'why are these two things on top of each other' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `elementsOverlapping` | high | Two visible, non-decorative elements have bbox intersection > 30% of the smaller element's area, with neither being an explicit child of the other (your Students-page toolbar buttons sitting ON TOP of the table header) |
| `textCollisionBetweenSiblings` | high | Two sibling text elements have bbox intersection AND their visible text overlaps in screen pixels (your Calendar widget where "S M T W..." headers crash into each other) |
| `gridCellContentCrashed` | high | Grid/calendar cells (`[role="gridcell"]`, `.day`, `.fc-`) with computed width < 30px AND text content longer than 1 char — content can't fit |
| `stickyCoversContent` | medium | Position-sticky/fixed element covers > 20% of an element below it in z-order at scroll position 0 |
| `dialogStackOverlap` | medium | Two `[role="dialog"]` elements are open at the same time AND bboxes overlap — second dialog partially hidden |

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = [];

  // ── Geometry helpers ──────────────────────────────────────────────────
  function intersect(a, b) {
    const x = Math.max(a.left, b.left);
    const y = Math.max(a.top, b.top);
    const r = Math.min(a.right, b.right);
    const bt = Math.min(a.bottom, b.bottom);
    if (r <= x || bt <= y) return null;
    return { area: (r - x) * (bt - y), w: r - x, h: bt - y };
  }
  function area(r) { return r.width * r.height; }

  // ── 1. Elements overlapping (toolbar over table, etc.) ────────────────
  // Pick clusters that commonly overlap inappropriately: toolbar buttons,
  // floating action elements, and table headers.
  const toolbars = [...document.querySelectorAll('.toolbar, [class*="toolbar"], .actions-bar, [class*="action-bar"], .page-actions, [class*="header-actions"]')].filter(visible);
  const tables = [...document.querySelectorAll('table, [role="table"], [role="grid"]')].filter(visible);
  let overlapFlagged = 0;
  for (const t of toolbars) {
    if (overlapFlagged >= 3) break;
    const tr = t.getBoundingClientRect();
    for (const tbl of tables) {
      const head = tbl.querySelector('thead, [role="rowgroup"]:first-child, tr:first-child');
      if (!head) continue;
      const hr = head.getBoundingClientRect();
      const i = intersect(tr, hr);
      if (i && i.area > Math.min(area(tr), area(hr)) * 0.3) {
        overlapFlagged++;
        out.push({
          issueType: 'elementsOverlapping', severity: 'high',
          selector: sel(t), bbox: bb(t),
          description: `Toolbar/actions container overlaps the table header by ${i.w.toFixed(0)}×${i.h.toFixed(0)}px (${Math.round(i.area/Math.min(area(tr),area(hr))*100)}% of smaller). Action buttons sit on top of header text.`
        });
        break;
      }
    }
  }

  // Also check page-header / breadcrumb action buttons against stat cards / content panels below.
  // Pattern: "Refresh Sync" button in the page header overlaps the "ORPHAN STUDENTS" card.
  // Caused by insufficient header bottom-padding, card top-margin, or absolute-positioned buttons.
  if (overlapFlagged < 3) {
    const headerBtns = [...document.querySelectorAll(
      'header button, [class*="page-header"] button, [class*="page-title"] button, ' +
      '[class*="breadcrumb"] button, [class*="title-bar"] button, [class*="topbar"] button, ' +
      '.page-header [role="button"], [class*="header-right"] button, [class*="header-action"] button'
    )].filter(visible);
    const cards = [...document.querySelectorAll(
      '[class*="card"], [class*="stat-card"], [class*="overview-card"], [class*="kpi"], ' +
      '[class*="metric"], [class*="widget-card"], [class*="summary-card"], [class*="count-card"]'
    )].filter(visible);
    for (const btn of headerBtns) {
      if (overlapFlagged >= 3) break;
      const br = btn.getBoundingClientRect();
      for (const card of cards) {
        const cr = card.getBoundingClientRect();
        // Card must be BELOW the button (not the button's own container)
        if (btn.closest('[class*="card"]') === card) continue;
        if (cr.top < br.top) continue;
        const i = intersect(br, cr);
        if (i && i.area > 30) {
          overlapFlagged++;
          out.push({
            issueType: 'elementsOverlapping', severity: 'high',
            selector: sel(btn), bbox: bb(btn),
            description: `Page header button "${(btn.innerText || btn.getAttribute('aria-label') || '').trim().slice(0, 30)}" overlaps card/panel below it by ${i.w.toFixed(0)}×${i.h.toFixed(0)}px. Button appears "attached" to the card. Fix: increase header bottom-padding or card top-margin, or constrain button height.`
          });
          break;
        }
      }
    }
  }

  // Also check floating action elements (FAB, sticky-action) against main content
  if (overlapFlagged < 3) {
    const floats = [...document.querySelectorAll('.fab, .floating-button, [class*="floating"], [class*="fab"], [class*="action-button"]')].filter(visible);
    const mains = [...document.querySelectorAll('main, [role="main"], .main-content, .content')].filter(visible);
    for (const f of floats) {
      if (overlapFlagged >= 3) break;
      const fr = f.getBoundingClientRect();
      // Float overlapping a button/link in main content
      for (const m of mains) {
        const inner = [...m.querySelectorAll('button, a[href], input')].filter(visible);
        for (const inn of inner.slice(0, 30)) {
          const ir = inn.getBoundingClientRect();
          const i = intersect(fr, ir);
          if (i && i.area > area(ir) * 0.4) {
            overlapFlagged++;
            out.push({
              issueType: 'elementsOverlapping', severity: 'high',
              selector: sel(f), bbox: bb(f),
              description: `Floating element ${sel(f)} overlaps interactive control ${sel(inn)} by ${i.w.toFixed(0)}×${i.h.toFixed(0)}px. User can't click the underlying control.`
            });
            break;
          }
        }
      }
    }
  }

  // ── 2. Text collision between siblings ────────────────────────────────
  // Group containers: scan all elements with multiple visible text children, look
  // for sibling pairs whose visible text bboxes intersect (e.g. day headers
  // crashed into each other in a calendar with narrow columns).
  let textCollideFlagged = 0;
  const containers = document.querySelectorAll('[role="row"], thead tr, .calendar, .fc-day-header, .day-grid, [class*="grid-header"]');
  for (const c of containers) {
    if (textCollideFlagged >= 3) break;
    if (!visible(c)) continue;
    const children = [...c.children].filter(visible);
    if (children.length < 2) continue;
    for (let i = 1; i < children.length; i++) {
      const a = children[i-1].getBoundingClientRect();
      const b = children[i].getBoundingClientRect();
      const ix = intersect(a, b);
      if (ix && ix.w > 4 && children[i-1].innerText && children[i].innerText) {
        // Strings collide on screen
        textCollideFlagged++;
        out.push({
          issueType: 'textCollisionBetweenSiblings', severity: 'high',
          selector: sel(c), bbox: bb(c),
          description: `Adjacent siblings overlap horizontally by ${ix.w.toFixed(0)}px (children "${(children[i-1].innerText||'').trim().slice(0, 20)}" and "${(children[i].innerText||'').trim().slice(0, 20)}"). Text content collides on screen.`
        });
        break;
      }
    }
  }

  // ── 3. Grid cells crashed (calendar widget bug) ──────────────────────
  let gridCellFlagged = 0;
  const gridCells = document.querySelectorAll('[role="gridcell"], .day, td.day, .fc-day, [class*="datepicker-day"], [class*="calendar-day"]');
  for (const cell of gridCells) {
    if (gridCellFlagged >= 1) break;
    if (!visible(cell)) continue;
    const r = cell.getBoundingClientRect();
    const txt = (cell.innerText || '').trim();
    if (r.width < 30 && txt.length >= 1 && r.height > 16) {
      gridCellFlagged++;
      const grid = cell.closest('[role="grid"], .calendar, .datepicker, .fc-view');
      out.push({
        issueType: 'gridCellContentCrashed', severity: 'high',
        selector: sel(grid || cell), bbox: bb(grid || cell),
        description: `Grid/calendar cells rendered at ${r.width.toFixed(0)}px wide — text content "${txt.slice(0, 10)}" cannot fit. Widget is collapsed below usable minimum.`
      });
    }
  }

  // ── 4. Sticky covers content ──────────────────────────────────────────
  let stickyFlagged = 0;
  const stickies = [...document.querySelectorAll('*')].filter(el => {
    if (!visible(el)) return false;
    const cs = getComputedStyle(el);
    return (cs.position === 'sticky' || cs.position === 'fixed') &&
           el.getBoundingClientRect().height > 24;
  }).slice(0, 6);
  for (const s of stickies) {
    if (stickyFlagged >= 2) break;
    const sr = s.getBoundingClientRect();
    // Look for content sitting directly behind sticky element
    const candidates = document.elementsFromPoint(sr.left + sr.width / 2, sr.top + sr.height / 2);
    for (const c of candidates) {
      if (c === s || s.contains(c) || c.contains(s)) continue;
      if (!visible(c)) continue;
      const cr = c.getBoundingClientRect();
      const i = intersect(sr, cr);
      if (i && i.area > area(cr) * 0.2 && (c.innerText || '').trim().length > 5) {
        stickyFlagged++;
        out.push({
          issueType: 'stickyCoversContent', severity: 'medium',
          selector: sel(s), bbox: bb(s),
          description: `Sticky/fixed element ${sel(s)} covers > 20% of content element ${sel(c)} ("${(c.innerText||'').trim().slice(0, 30)}"). Add scroll-margin-top on linked content or adjust offsets.`
        });
        break;
      }
    }
  }

  // ── 5. Dialog stack overlap ──────────────────────────────────────────
  const dialogs = [...document.querySelectorAll('[role="dialog"]:not([hidden]), dialog[open]')].filter(visible);
  if (dialogs.length >= 2) {
    for (let i = 0; i < dialogs.length - 1; i++) {
      const a = dialogs[i].getBoundingClientRect();
      const b = dialogs[i+1].getBoundingClientRect();
      const ix = intersect(a, b);
      if (ix && ix.area > Math.min(area(a), area(b)) * 0.2) {
        out.push({
          issueType: 'dialogStackOverlap', severity: 'medium',
          selector: sel(dialogs[i+1]), bbox: bb(dialogs[i+1]),
          description: `Two dialogs open and overlapping by ${ix.w.toFixed(0)}×${ix.h.toFixed(0)}px. Stack/replace pattern broken — close the first before opening the second.`
        });
        break;
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 3 toolbar/header overlap + 3 text collision + 1 grid crash + 2 sticky + 1 dialog = max ~10
- Self-skips: page with no toolbars/tables/grids/dialogs returns []
- The `elementsOverlapping` catches toolbar vs table headers, FAB vs content, AND header buttons vs stat cards
- The `gridCellContentCrashed` catches your calendar widget where columns are < 30px
