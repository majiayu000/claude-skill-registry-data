---
name: qa-detect-ux-card-usage
section: visual
description: "Detects illogical use of the card pattern: a giant card containing only a single small input (your Search-only card), card with > 70% empty space relative to content, cards nested 3+ levels deep, card with substantial content but no heading, card heading separated from content by big gap."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasCards]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `cardOverContaining` | medium | Card is > 200px wide / 60px tall but contains only ONE small interactive element (single input, single button) with no other meaningful content — wasted screen space (your Search-in-card screenshot) |
| `cardMostlyEmpty` | medium | Card has > 70% empty area inside (content occupies < 30% of card area). Indicates wrong card boundary or missing content |
| `cardNestedTooDeep` | low | Cards nested 3+ levels deep — visual depth confusion |
| `cardWithoutTitle` | low | Card > 300px tall with substantial content but no `<h1>-<h6>`, no `.card-title`, no aria-label — users can't tell what the card is for |
| `cardTitleSeparatedByLargeGap` | low | Card has a heading but heading is > 32px away from following content — visually disconnected |
| `cardActionsNotInFooter` | low | Card has primary action buttons (Save/Submit/etc.) placed in mid-card body rather than at the bottom/footer — non-standard layout |

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
  const out = [];

  const cardSel = '.card, .panel, .mat-card, [class*="card"]:not([class*="card-header"]):not([class*="card-body"]):not([class*="card-footer"]):not([class*="card-title"]), [class*="panel"]:not([class*="panel-header"]):not([class*="panel-body"]), .surface, .tile, .box';
  let cards = [...document.querySelectorAll(cardSel)].filter(visible);
  // Outermost only
  cards = cards.filter((c, i, arr) => !arr.some(o => o !== c && o.contains(c) && o !== document.body));

  // ── 1. Over-containing card (single small element) ──────────────────
  let overFlagged = 0;
  for (const c of cards) {
    if (overFlagged >= 3) break;
    const r = c.getBoundingClientRect();
    if (r.width < 200 || r.height < 60) continue;
    // Count meaningful descendants
    const interactives = [...c.querySelectorAll('input:not([type="hidden"]), select, textarea, button, a[href], [role="button"]')].filter(visible);
    const textBlocks = [...c.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li')].filter(t => visible(t) && (t.innerText || '').trim().length > 4);
    // Single interactive + < 1 substantial text block + card area > 20000px²
    if (interactives.length === 1 && textBlocks.length === 0 && r.width * r.height > 20000) {
      const single = interactives[0];
      const sr = single.getBoundingClientRect();
      // Element occupies < 30% of card area
      if (sr.width * sr.height < r.width * r.height * 0.3) {
        overFlagged++;
        const inpType = single.tagName === 'INPUT' ? (single.type || 'text') : single.tagName.toLowerCase();
        out.push({
          issueType: 'cardOverContaining', severity: 'medium',
          selector: sel(c), bbox: bb(c),
          description: `Card is ${r.width.toFixed(0)}×${r.height.toFixed(0)}px (${Math.round(r.width*r.height)}px²) but holds only ONE small ${inpType} element (${sr.width.toFixed(0)}×${sr.height.toFixed(0)}px). Drop the card wrapper or place the element inline.`
        });
      }
    }
  }

  // ── 2. Card mostly empty ─────────────────────────────────────────────
  let emptyFlagged = 0;
  for (const c of cards) {
    if (emptyFlagged >= 2) break;
    const r = c.getBoundingClientRect();
    if (r.width < 200 || r.height < 100) continue;
    // A chart/graph IS the content — donut/bar/line charts render data on a <canvas>
    // or <svg> with little text/DOM, so the area-of-text heuristic wrongly reads them
    // as "empty". Skip any card that contains a chart, map, or media canvas.
    if (c.querySelector('canvas, svg, [class*="chart" i], [class*="graph" i], [class*="plot" i], [id*="chart" i], .apexcharts-canvas, .highcharts-container, [class*="echart" i], [class*="recharts" i], video, iframe')) continue;
    const cardArea = r.width * r.height;
    // CONTENT-COUNT heuristic (replaces the noisy text-area-ratio that wrongly
    // flagged data cards like "Recent Activity" — a populated list IS content even
    // when spread out with whitespace). Only a GENUINELY near-empty card is a bug:
    // the lone-search-box-in-a-giant-card case this check was built for.
    const textLen = (c.innerText || '').replace(/\s+/g, ' ').trim().length;
    const contentUnits = [...c.querySelectorAll('input, select, textarea, button, a, p, h1, h2, h3, h4, h5, h6, table, tr, li, img, svg, canvas, span, strong, b')]
      .filter(el => visible(el) && ((el.innerText || el.alt || el.value || '').trim().length > 1
        || ['IMG', 'SVG', 'CANVAS', 'INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName))).length;
    // Flag ONLY when the card is large AND has almost no real content:
    // very little text (≤ 25 chars, i.e. ~a label or a single control) AND ≤ 2 content units.
    if (cardArea > 60000 && textLen <= 25 && contentUnits <= 2) {
      emptyFlagged++;
      out.push({
        issueType: 'cardMostlyEmpty', severity: 'medium',
        selector: sel(c), bbox: bb(c),
        description: `Card is ${Math.round(r.width)}×${Math.round(r.height)}px but holds almost no content (${textLen} chars of text, ${contentUnits} content element${contentUnits === 1 ? '' : 's'}). Shrink the card to fit its content or add meaningful content.`
      });
    }
  }

  // ── 3. Cards nested too deep ────────────────────────────────────────
  let nestFlagged = 0;
  const allCardsInDoc = [...document.querySelectorAll(cardSel)].filter(visible);
  for (const c of allCardsInDoc) {
    if (nestFlagged >= 2) break;
    let depth = 0;
    let cur = c;
    while (cur) {
      const parent = cur.parentElement;
      if (!parent) break;
      if (parent.matches(cardSel) && visible(parent)) depth++;
      cur = parent;
    }
    if (depth >= 3) {
      nestFlagged++;
      out.push({
        issueType: 'cardNestedTooDeep', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Card is nested ${depth + 1} levels deep inside other cards. Flatten the structure — repeated card chrome creates visual confusion.`
      });
    }
  }

  // ── 4. Card without title ───────────────────────────────────────────
  let noTitleFlagged = 0;
  for (const c of cards) {
    if (noTitleFlagged >= 3) break;
    const r = c.getBoundingClientRect();
    if (r.height < 300 || r.width < 200) continue;
    // Has a heading or labelled title?
    const heading = c.querySelector('h1, h2, h3, h4, h5, h6, .card-title, [class*="title"], [class*="header"], legend');
    const ariaLabel = c.getAttribute('aria-label') || c.getAttribute('aria-labelledby');
    if (heading && visible(heading) && (heading.innerText || '').trim().length > 2) continue;
    if (ariaLabel) continue;
    // Substantial content inside?
    const text = (c.innerText || '').trim();
    if (text.length < 50) continue;
    noTitleFlagged++;
    out.push({
      issueType: 'cardWithoutTitle', severity: 'low',
      selector: sel(c), bbox: bb(c),
      description: `Card is ${r.width.toFixed(0)}×${r.height.toFixed(0)}px with ${text.length} chars of content but has no heading (h1-h6, .card-title) and no aria-label. Users can't tell what the card represents.`
    });
  }

  // ── 5. Title separated from content by large gap ────────────────────
  let gapFlagged = 0;
  for (const c of cards) {
    if (gapFlagged >= 2) break;
    const heading = c.querySelector('h1, h2, h3, h4, h5, h6, .card-title, [class*="title"]');
    if (!heading || !visible(heading)) continue;
    // Find next sibling content
    let next = heading.nextElementSibling;
    while (next && (!visible(next) || (next.innerText || '').trim().length === 0)) {
      next = next.nextElementSibling;
    }
    if (!next) continue;
    const hr = heading.getBoundingClientRect();
    const nr = next.getBoundingClientRect();
    const gap = nr.top - hr.bottom;
    if (gap > 32) {
      gapFlagged++;
      out.push({
        issueType: 'cardTitleSeparatedByLargeGap', severity: 'low',
        selector: sel(heading), bbox: bb(heading),
        description: `Card title "${(heading.innerText || '').trim().slice(0, 30)}" is ${gap.toFixed(0)}px above its content. Visually disconnected — reduce margin to 12-16px.`
      });
    }
  }

  // ── 6. Card actions placed mid-body (not at footer) ─────────────────
  let actionFlagged = 0;
  for (const c of cards) {
    if (actionFlagged >= 2) break;
    const r = c.getBoundingClientRect();
    if (r.height < 200) continue;
    const actionBtns = [...c.querySelectorAll('button, [role="button"]')].filter(b => {
      if (!visible(b)) return false;
      const txt = (b.innerText || b.value || '').trim().toLowerCase();
      return /^(save|submit|update|create|delete|cancel|apply|confirm|continue|next|previous|search|reset|clear)$/i.test(txt);
    });
    if (actionBtns.length < 2) continue;
    // Are they in the top half of the card?
    const cardMid = r.top + r.height / 2;
    const cardBottom = r.bottom;
    const actionsAvgY = actionBtns.reduce((s, b) => s + b.getBoundingClientRect().top, 0) / actionBtns.length;
    if (actionsAvgY < cardMid && cardBottom - actionsAvgY > 80) {
      actionFlagged++;
      out.push({
        issueType: 'cardActionsNotInFooter', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Card has ${actionBtns.length} primary action buttons in the top half (avg y=${actionsAvgY.toFixed(0)}, card bottom=${cardBottom.toFixed(0)}). Convention: place primary actions at the card footer.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~14 findings per cell
- Self-skips: page with no cards returns []
- The `cardOverContaining` catches your Search-bar-in-its-own-card screenshot
- The `cardMostlyEmpty` catches cards padded out with whitespace for no content reason
