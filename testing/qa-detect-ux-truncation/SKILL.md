---
name: qa-detect-ux-truncation
section: visual
description: "Detects content truncation that hides information from users: table header text cut mid-word ('Reg', 'Nan', 'Clas'), cell content clipped to a single character, button text ellipsised, breadcrumb item truncated. Goes beyond a11y — catches readability failures."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `headerTextTruncatedMidWord` | high | Table header cell shows ellipsised / clipped text mid-word ("Reg…", "Clas…", "Nan…") — column name not readable |
| `cellContentTruncatedToCharacter` | high | Body cell displays only 1-2 characters of likely-longer content AND `scrollWidth > clientWidth + 2` |
| `buttonTextEllipsised` | medium | Button text is visually truncated (overflow:hidden + ellipsis) — action label unclear |
| `breadcrumbItemTruncated` | low | Breadcrumb item shows ellipsis — path becomes unreadable |
| `inputValueClippedNoExpand` | low | Text input has value longer than visible width, no horizontal scroll, no auto-grow |
| `tabLabelTruncated` | medium | Tab label clipped — user can't tell which tab is which |
| `cardSubtitleTruncated` | medium | Stat card subtitle like "Liv…" truncated — metric context lost, card meaning becomes ambiguous |
| `tableCellNumericTruncated` | high | Numeric/amount column (Paid, Fee, Balance, Amount…) shows truncated values like "2,…" or "1,3…" — full value hidden on narrow/mobile viewport |

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
  // Returns true if element is visually truncated (text content wider than container)
  function isClipped(el) {
    if (!el) return false;
    // scrollWidth > clientWidth means text overflows
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) return true;
    // Or computed text-overflow: ellipsis on overflow: hidden parent
    return false;
  }
  // Detect "mid-word truncation": text ends in a partial word (last char is alpha,
  // not a sentence-ending punctuation, AND ellipsis applied)
  function isMidWordTruncation(el) {
    const cs = getComputedStyle(el);
    if (cs.textOverflow !== 'ellipsis' && cs.overflow !== 'hidden') return false;
    if (el.scrollWidth <= el.clientWidth + 2) return false;
    const txt = (el.innerText || '').trim();
    if (txt.length < 2) return false;
    const lastChar = txt[txt.length - 1];
    // If ends with letter (no punctuation), it's a mid-word cut
    return /[a-zA-Z]/.test(lastChar);
  }
  const out = [];

  // ── 1. Table header text truncated mid-word ──────────────────────────
  let headerFlagged = 0;
  const headerCells = document.querySelectorAll('th, [role="columnheader"]');
  for (const h of headerCells) {
    if (headerFlagged >= 4) break;
    if (!visible(h)) continue;
    const r = h.getBoundingClientRect();
    if (r.width < 12) continue;  // collapsed entirely — different bug
    const text = (h.innerText || '').trim();
    if (text.length < 2) continue;
    if (isMidWordTruncation(h) || (isClipped(h) && text.length <= 5 && /[a-z]$/i.test(text))) {
      headerFlagged++;
      out.push({
        issueType: 'headerTextTruncatedMidWord', severity: 'high',
        selector: sel(h), bbox: bb(h),
        description: `Column header "${text}" appears truncated mid-word at ${r.width.toFixed(0)}px wide (scroll ${h.scrollWidth}px). Users can't tell what the column means.`
      });
    }
  }

  // ── 2. Body cell truncated to a single character ─────────────────────
  let cellFlagged = 0;
  const tables = [...document.querySelectorAll('table, [role="table"], [role="grid"]')].filter(visible);
  for (const tbl of tables.slice(0, 4)) {
    if (cellFlagged >= 3) break;
    const bodyCells = [...tbl.querySelectorAll('tbody td, [role="cell"]')].filter(visible);
    for (const c of bodyCells.slice(0, 30)) {
      if (cellFlagged >= 3) break;
      if (!visible(c)) continue;
      const r = c.getBoundingClientRect();
      if (r.width < 12 || r.height < 16) continue;
      const text = (c.innerText || '').trim();
      // Heuristic: 1-2 visible chars AND scrollWidth is much greater than clientWidth
      if (text.length >= 1 && text.length <= 2 && c.scrollWidth > c.clientWidth + 8 && r.width < 60) {
        cellFlagged++;
        out.push({
          issueType: 'cellContentTruncatedToCharacter', severity: 'high',
          selector: sel(c), bbox: bb(c),
          description: `Body cell shows only "${text}" (${text.length} char) at ${r.width.toFixed(0)}px wide, scrollWidth ${c.scrollWidth}px. Content clipped to single character — column too narrow.`
        });
      }
    }
  }

  // ── 3. Button text ellipsised ─────────────────────────────────────────
  let btnFlagged = 0;
  const btns = document.querySelectorAll('button, a.btn, [role="button"], input[type="button"], input[type="submit"]');
  for (const b of btns) {
    if (btnFlagged >= 3) break;
    if (!visible(b)) continue;
    if (isMidWordTruncation(b)) {
      btnFlagged++;
      const t = (b.innerText || b.value || '').trim();
      out.push({
        issueType: 'buttonTextEllipsised', severity: 'medium',
        selector: sel(b), bbox: bb(b),
        description: `Button text "${t.slice(0, 30)}" is ellipsised at ${b.clientWidth}px wide (full text ${b.scrollWidth}px). Action label unclear.`
      });
    }
  }

  // ── 4. Breadcrumb item truncated ─────────────────────────────────────
  let crumbFlagged = 0;
  const crumbs = document.querySelectorAll('.breadcrumb a, .breadcrumb span, .breadcrumb li, [class*="breadcrumb"] a, [role="navigation"][aria-label*="breadcrumb" i] a, nav[aria-label*="breadcrumb" i] *');
  for (const c of crumbs) {
    if (crumbFlagged >= 2) break;
    if (!visible(c)) continue;
    if (isMidWordTruncation(c)) {
      crumbFlagged++;
      const t = (c.innerText || '').trim();
      out.push({
        issueType: 'breadcrumbItemTruncated', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Breadcrumb item "${t.slice(0, 30)}" is truncated. Path becomes unreadable.`
      });
    }
  }

  // ── 5. Input value clipped without scroll or expansion ───────────────
  let inputFlagged = 0;
  const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="search"], input[type="url"], input[type="tel"], input:not([type])');
  for (const inp of inputs) {
    if (inputFlagged >= 3) break;
    if (!visible(inp)) continue;
    const v = (inp.value || '').trim();
    if (v.length < 4) continue;
    if (inp.scrollWidth > inp.clientWidth + 4 && inp.clientWidth > 20) {
      // Check if focusing reveals the rest (most inputs allow scroll on focus)
      const cs = getComputedStyle(inp);
      if (cs.overflow === 'hidden' || cs.textOverflow === 'ellipsis') {
        inputFlagged++;
        out.push({
          issueType: 'inputValueClippedNoExpand', severity: 'low',
          selector: sel(inp), bbox: bb(inp),
          description: `Input value "${v.slice(0, 40)}..." is clipped at ${inp.clientWidth}px (full ${inp.scrollWidth}px) with overflow:hidden — users can't see the full value.`
        });
      }
    }
  }

  // ── 6. Tab label truncated ────────────────────────────────────────────
  let tabFlagged = 0;
  const tabs = document.querySelectorAll('[role="tab"], .nav-tabs a, .mat-tab-label, .tab-button');
  for (const t of tabs) {
    if (tabFlagged >= 3) break;
    if (!visible(t)) continue;
    if (isMidWordTruncation(t)) {
      tabFlagged++;
      const txt = (t.innerText || '').trim();
      out.push({
        issueType: 'tabLabelTruncated', severity: 'medium',
        selector: sel(t), bbox: bb(t),
        description: `Tab label "${txt.slice(0, 30)}" is truncated at ${t.clientWidth}px. Users can't distinguish between tabs.`
      });
    }
  }

  // ── 7. Stat card subtitle truncated ─────────────────────────────────────
  // Catches subtitles like "Liv..." (truncation of "Living", "Live count", etc.)
  // inside stat/summary cards. The subtitle provides metric context — truncation
  // makes the card ambiguous (e.g. "3. Liv..." — Liv... what?).
  let subtitleFlagged = 0;
  const CARD_SEL2 = '[class*="stat"],[class*="kpi"],[class*="summary-card"],[class*="metric"],[class*="widget-card"],[class*="count-card"],[class*="overview-card"],[class*="overview-item"],.card';
  for (const card of document.querySelectorAll(CARD_SEL2)) {
    if (subtitleFlagged >= 4) break;
    if (!visible(card)) continue;
    const candidates = [...card.querySelectorAll('span,p,small,[class*="subtitle"],[class*="sub-label"],[class*="caption"],[class*="meta"],[class*="desc"],[class*="hint"]')]
      .filter(el => {
        if (!visible(el)) return false;
        const t = (el.innerText || '').trim();
        return t.length >= 2 && t.length <= 60;
      });
    for (const el of candidates) {
      if (subtitleFlagged >= 4) break;
      const cs = getComputedStyle(el);
      const clippedByOverflow = (cs.overflow === 'hidden' || cs.overflowX === 'hidden') && el.scrollWidth > el.clientWidth + 3;
      const clippedByEllipsis = cs.textOverflow === 'ellipsis' && el.scrollWidth > el.clientWidth + 3;
      const endsAbruptly = /[a-zA-Z]$/.test((el.innerText || '').trim());
      if ((clippedByOverflow || clippedByEllipsis) && endsAbruptly) {
        subtitleFlagged++;
        const t = (el.innerText || '').trim();
        out.push({ issueType:'cardSubtitleTruncated', severity:'medium', selector:sel(el), bbox:bb(el),
          description:`Stat card subtitle "${t.slice(0,30)}" is truncated (content ${el.scrollWidth}px > container ${el.clientWidth}px). Subtitle provides metric context — truncation makes the card ambiguous. Increase card width or shorten the subtitle copy.` });
      }
    }
  }

  // ── 8. Numeric/amount column truncated on narrow/mobile viewport ────────
  // Catches "2,..." "1,3..." patterns where currency/count values are cut off.
  // Fires when ≥ 2 cells in the same column are visually truncated AND the column
  // header or cell content indicates numeric/financial data.
  let numericTruncFlagged = 0;
  const NUMERIC_HDR = /paid|fee|amount|balance|total|price|cost|salary|budget|revenue|income|expense|tax|deposit|pending|credit|debit|qty|quantity|count|score|rate|percent|pkr|usd|eur|gbp|\$/i;
  const tables3 = [...document.querySelectorAll('table, [role="table"], [role="grid"]')].filter(visible);
  for (const tbl of tables3.slice(0, 4)) {
    if (numericTruncFlagged >= 3) break;
    const hdrCells = [...tbl.querySelectorAll('thead th, thead [role="columnheader"], [role="row"]:first-child [role="columnheader"]')].filter(visible);
    const bRows = [...tbl.querySelectorAll('tbody tr, [role="rowgroup"]:not(:first-child) [role="row"]')].filter(visible);
    if (bRows.length < 2) continue;
    for (let ci = 0; ci < hdrCells.length; ci++) {
      if (numericTruncFlagged >= 3) break;
      const hdrText = (hdrCells[ci].innerText || '').trim();
      // Require numeric-sounding header OR detect from cell content
      let truncCells = [], numericCells = 0, sampled = 0;
      for (const row of bRows.slice(0, 6)) {
        const cells = [...row.querySelectorAll('td, [role="cell"]')];
        const cell = cells[ci];
        if (!cell || !visible(cell)) continue;
        sampled++;
        const cellText = (cell.innerText || '').trim();
        const cs = getComputedStyle(cell);
        // Numeric content heuristic: has digits with commas/dots (e.g. "2,850", "1,375")
        if (/^\d[\d,.\s]*$/.test(cellText) || /\d{1,3}(?:,\d{3})+/.test(cellText)) numericCells++;
        // Truncation detection — two cases:
        //   A) CSS text-overflow:ellipsis with scrollWidth > clientWidth
        const cssTruncated = cs.textOverflow === 'ellipsis' && cell.scrollWidth > cell.clientWidth + 2;
        //   B) JS-injected literal ellipsis ("2,..." "1,3…") — Angular/PrimeNG pattern
        const literalTruncated = /[.,]\.\.\.$|…$|\.\.\.$/.test(cellText) || cellText.endsWith('...');
        //   C) title attribute differs from visible text (framework sets full value as tooltip)
        const titleVal = (cell.getAttribute('title') || '').trim();
        const titleDiffers = titleVal.length > 0 && titleVal !== cellText && titleVal.length > cellText.length;
        if (cssTruncated || literalTruncated || titleDiffers) {
          truncCells.push(cellText.slice(0, 20));
        }
      }
      // Fire if: ≥ 2 truncated AND (numeric header OR ≥ 2 numeric cells)
      const isNumericCol = NUMERIC_HDR.test(hdrText) || numericCells >= 2;
      if (sampled >= 2 && truncCells.length >= 2 && isNumericCol) {
        numericTruncFlagged++;
        out.push({
          issueType: 'tableCellNumericTruncated', severity: 'high',
          selector: sel(hdrCells[ci]), bbox: bb(hdrCells[ci]),
          description: `Column "${hdrText}" shows truncated numeric values (${truncCells.slice(0,3).map(v=>`"${v}"`).join(', ')}) at ${Math.round(hdrCells[ci].getBoundingClientRect().width)}px wide. Amounts are cut off on this viewport — use horizontal scroll, responsive column hiding, or compact number format (e.g. "2.8K").`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 4 header + 3 cell + 3 button + 2 breadcrumb + 3 input + 3 tab + 4 subtitle + 3 numeric = max ~21
- Self-skips: page with no tables/buttons/breadcrumbs returns []
- The `headerTextTruncatedMidWord` catches "Reg", "Nan", "Clas" headers from your Students page
- The `cellContentTruncatedToCharacter` catches "B", "C", "M" body cells from your Students page
