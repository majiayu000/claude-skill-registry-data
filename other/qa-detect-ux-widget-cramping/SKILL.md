---
name: qa-detect-ux-widget-cramping
section: visual
description: "Detects widget/card header layout breakdown — title text wrapping mid-phrase ('June' + '2026' on separate lines), toolbar buttons overlapping the title vertically, controls cut off at the widget's right edge, header controls wrapping into multiple rows because they don't fit. Catches the 'this widget toolbar is squashed and stuff is overflowing' bug class (your Calendar widget screenshot)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasCards, hasKPICards, hasDashboardTiles]
---

## What it catches — 4 issue types

| issueType | severity | What |
|---|---|---|
| `widgetTitleWraps` | medium | A widget header title (e.g. "June 2026") wraps onto 2+ lines because the toolbar buttons crowd it out — title text height > 1.5× line-height |
| `widgetToolbarOverlapsTitle` | high | Toolbar control buttons (next/prev/today/month/week) bounding-box overlaps the widget title's bounding-box — controls visually sit on top of the title |
| `widgetControlClippedByContainer` | high | A widget header control (button/select) has its right edge cut off (right > container.right - 4px) and the container has `overflow: hidden` or content is visibly truncated — control is unreachable |
| `widgetHeaderControlsWrapped` | medium | Widget header children (title + N buttons) wrap onto 2+ rows because horizontal space is too tight — header height > 1.5× typical-row-height AND children appear at multiple Y positions |

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
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const rectOverlap = (a, b) => !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
  const out = [];

  // Find widget headers — common patterns
  const widgetContainers = [
    '.card', '[class*="card"]', '.panel', '[class*="panel"]',
    '.widget', '[class*="widget"]',
    '[class*="calendar"]', '[class*="chart"]', '[class*="dashboard-item"]', '[class*="dashboard-card"]',
    '[data-widget]'
  ];
  const candidates = new Set();
  for (const s of widgetContainers) {
    for (const el of document.querySelectorAll(s)) {
      if (!visible(el)) continue;
      // Skip nested matches — only keep outermost cards
      if ([...candidates].some(c => c.contains(el))) continue;
      // Remove any candidate this one contains
      for (const c of [...candidates]) if (el.contains(c)) candidates.delete(c);
      candidates.add(el);
    }
  }

  let titleWrapFlagged = 0;
  let overlapFlagged = 0;
  let clippedFlagged = 0;
  let wrappedFlagged = 0;

  for (const card of candidates) {
    if (titleWrapFlagged >= 3 && overlapFlagged >= 3 && clippedFlagged >= 3 && wrappedFlagged >= 3) break;
    const cr = card.getBoundingClientRect();
    if (cr.width < 120 || cr.height < 80) continue;

    // Locate the header region inside this card
    const headerEl = card.querySelector(
      '.card-header, .panel-header, .widget-header, header, ' +
      '[class*="header"], [class*="Header"], [class*="toolbar"], [class*="Toolbar"]'
    );
    const header = headerEl && visible(headerEl) && headerEl.getBoundingClientRect().width > 40
      ? headerEl
      : null;
    // If no explicit header, treat the first row of children as the header
    const scope = header || card;

    // Identify a title element in scope: h1-h4, [class*="title"], the largest-font text element near top
    let title = scope.querySelector('h1, h2, h3, h4, [class*="title"], [class*="Title"], [class*="heading"]');
    if (title && !visible(title)) title = null;
    // Identify control buttons in scope (next/prev/today/view-switch etc.) — children that are NOT title
    const allControls = [...scope.querySelectorAll('button, [role="button"], select, [class*="btn"], [class*="nav-arrow"], [class*="navArrow"], [class*="view-switch"], [class*="toggle"]')]
      .filter(visible)
      .filter(b => title ? !title.contains(b) && !b.contains(title) : true);

    // ── 1. widgetTitleWraps — title text wraps to multiple lines ───────
    if (title && titleWrapFlagged < 3) {
      const tr = title.getBoundingClientRect();
      const cs = getComputedStyle(title);
      const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
      const lineCount = lh > 0 ? Math.round(tr.height / lh) : 1;
      const txt = (title.innerText || '').trim();
      // Only flag short titles (≤ 30 chars) that wrap — long titles wrapping is fine
      if (lineCount >= 2 && txt.length > 0 && txt.length <= 30) {
        titleWrapFlagged++;
        out.push({
          issueType: 'widgetTitleWraps', severity: 'medium',
          selector: sel(title), bbox: bb(title),
          description: `Widget title "${txt}" wraps onto ${lineCount} lines (${tr.height.toFixed(0)}px tall, line-height ${lh.toFixed(0)}px). Short titles shouldn't wrap — toolbar buttons are crowding it out. Move buttons below the title or shorten/abbreviate the title text. (Your Calendar widget: "June" + "2026" split across two lines.)`
        });
      }
    }

    // ── 2. widgetToolbarOverlapsTitle — control bbox overlaps title bbox ────
    if (title && allControls.length >= 1 && overlapFlagged < 3) {
      const tr = title.getBoundingClientRect();
      let overlappingCtl = null;
      for (const ctl of allControls) {
        const cr2 = ctl.getBoundingClientRect();
        // Require true rect overlap AND ctl isn't an obvious child/sibling sitting below
        if (rectOverlap(tr, cr2) && cr2.top < tr.bottom - 4 && cr2.bottom > tr.top + 4) {
          // Skip if they're side-by-side (overlap is just a 1-2px touch)
          const overlapW = Math.min(tr.right, cr2.right) - Math.max(tr.left, cr2.left);
          if (overlapW > 8) { overlappingCtl = ctl; break; }
        }
      }
      if (overlappingCtl) {
        overlapFlagged++;
        const txt = (title.innerText || '').trim().slice(0, 24);
        const btn = (overlappingCtl.innerText || overlappingCtl.value || overlappingCtl.getAttribute('aria-label') || 'control').trim().slice(0, 20);
        out.push({
          issueType: 'widgetToolbarOverlapsTitle', severity: 'high',
          selector: sel(overlappingCtl), bbox: bb(overlappingCtl),
          description: `Widget control "${btn}" visually overlaps the title "${txt}" — bounding boxes intersect by >8px. Toolbar layout broken: controls and title competing for the same space. (Your Calendar widget: "month" button overlapping the title row.)`
        });
      }
    }

    // ── 3. widgetControlClippedByContainer — control cut off at card right edge ────
    if (allControls.length >= 1 && clippedFlagged < 3) {
      const cardCs = getComputedStyle(card);
      const cardClipsX = cardCs.overflowX === 'hidden' || cardCs.overflowX === 'clip' ||
                         cardCs.overflow === 'hidden' || cardCs.overflow === 'clip';
      for (const ctl of allControls) {
        const cr2 = ctl.getBoundingClientRect();
        // Control's right edge is past the card's right edge (clipped)
        if (cr2.right > cr.right + 1) {
          if (cardClipsX) {
            // Truly clipped
            clippedFlagged++;
            const btn = (ctl.innerText || ctl.value || ctl.getAttribute('aria-label') || 'control').trim().slice(0, 20);
            out.push({
              issueType: 'widgetControlClippedByContainer', severity: 'high',
              selector: sel(ctl), bbox: bb(ctl),
              description: `Widget control "${btn}" extends past the right edge of its container (control.right=${cr2.right.toFixed(0)}px, container.right=${cr.right.toFixed(0)}px) and the container clips overflow — the control is partially or fully invisible to users. (Your Calendar widget: "week" button cut off at the right edge.)`
            });
            break;
          } else {
            // Not clipped but still spilling — let qa-detect-overflow handle it
          }
        } else if (cr2.right > cr.right - 4 && cr2.width >= 30) {
          // Control's right edge is FLUSH with container right (zero margin) — likely about to clip on small viewports
          // Don't flag this — only flag actual clipping
        }
      }
    }

    // ── 4. widgetHeaderControlsWrapped — header content forced onto multiple rows ────
    if (header && wrappedFlagged < 3) {
      const headerChildren = [...header.children].filter(visible);
      if (headerChildren.length >= 2) {
        // Group children by their Y center — multiple distinct rows = wrapping
        const rows = new Map();
        for (const c of headerChildren) {
          const r = c.getBoundingClientRect();
          if (r.width < 8 || r.height < 8) continue;
          const yCenter = Math.round((r.top + r.bottom) / 2 / 8) * 8; // 8px bins
          if (!rows.has(yCenter)) rows.set(yCenter, []);
          rows.get(yCenter).push(c);
        }
        if (rows.size >= 2) {
          // Header occupies 2+ rows — but maybe that's intentional (subtitle below title)
          // Heuristic: only flag if the header is "trying to be" a single-row toolbar with title + multiple controls
          const hasTitle = !!title;
          const ctlCount = allControls.length;
          if (hasTitle && ctlCount >= 2) {
            const hr = header.getBoundingClientRect();
            wrappedFlagged++;
            out.push({
              issueType: 'widgetHeaderControlsWrapped', severity: 'medium',
              selector: sel(header), bbox: bb(header),
              description: `Widget header has ${ctlCount} controls + title across ${rows.size} rows (header height ${hr.height.toFixed(0)}px). Controls wrap because they don't fit horizontally. Convert the toolbar to a responsive overflow menu or stack controls intentionally below the title.`
            });
          }
        }
      }
    }
  }

  return out;
}
```

## Notes

- Self-skips: pages with no widget-like cards return [] immediately
- Bounded: max 3 + 3 + 3 + 3 = 12 findings per cell
- Catches the Calendar widget pattern from your screenshot: title wrapping, "month" overlapping the title, "week" clipped, "today" on a separate row
- Complements `qa-detect-ux-overlap` (page-level overlaps) by focusing on WITHIN-WIDGET layout failures
- Complements `qa-detect-ux-toolbar-consistency` which checks consistency between toolbars, not layout breakdown within one
