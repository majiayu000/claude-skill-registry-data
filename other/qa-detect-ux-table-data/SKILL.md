---
name: qa-detect-ux-table-data
section: visual
description: "Detects table data-quality UX problems: excessive empty space below a small row count, reverse-ordered Sr#/ID columns (7 at top, 1 at bottom), columns that are empty in every visible row, sort indicators on only some columns. Catches the 'why does this table look broken' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasTables]
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `tableExcessiveEmptySpace` | medium | Table container has > 60% empty vertical space below the last visible row (table looks broken — sparse data in a large fixed-height container) — your Districts page bug |
| `tableSerialColumnReversed` | medium | Sr#/ID column shows descending numbers (7,6,5,...,1) when scrolled top-to-bottom. Users expect ascending in serial/index columns. |
| `tableColumnAllEmpty` | low | Visible column has no content (empty string / dash / placeholder) in every row across the visible range — your Clusters Description column |
| `tableSortIndicatorInconsistent` | low | Some column headers have sort indicators (↑↓ icons), others don't — users assume non-indicator columns aren't sortable when they actually are (or vice versa) |
| `tableActionButtonsTooClose` | medium | Edit/Delete action icons in same row are < 8px apart — misclick risk |

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

  const tables = [...document.querySelectorAll('table, [role="table"], [role="grid"]')].filter(visible);
  let emptySpaceFlagged = 0, reverseFlagged = 0, emptyColFlagged = 0,
      sortFlagged = 0, actionFlagged = 0;

  for (const tbl of tables.slice(0, 4)) {
    const bodyRows = [...tbl.querySelectorAll('tbody tr, [role="rowgroup"]:not(:first-child) [role="row"]')].filter(visible);
    const headerCells = [...tbl.querySelectorAll('thead th, thead [role="columnheader"], [role="row"]:first-child > [role="columnheader"]')].filter(visible);

    // ── 1. Excessive empty space below table content ─────────────────────
    if (emptySpaceFlagged < 2 && bodyRows.length > 0) {
      // Find the container wrapper that the table lives in
      const wrap = tbl.closest('.table-wrapper, .table-container, .table-responsive, .data-table, .mat-table-container, .card-body, [class*="table-wrap"]') || tbl.parentElement;
      if (wrap && visible(wrap)) {
        const wrapR = wrap.getBoundingClientRect();
        const lastRow = bodyRows[bodyRows.length - 1];
        const lastR = lastRow.getBoundingClientRect();
        const usedHeight = lastR.bottom - wrapR.top;
        const totalHeight = wrapR.height;
        if (totalHeight > 200 && usedHeight > 0) {
          const emptyRatio = (totalHeight - usedHeight) / totalHeight;
          // Excessive: > 60% empty AND empty area > 200px
          const emptyPx = totalHeight - usedHeight;
          if (emptyRatio > 0.6 && emptyPx > 200 && bodyRows.length <= 5) {
            emptySpaceFlagged++;
            out.push({
              issueType: 'tableExcessiveEmptySpace', severity: 'medium',
              selector: sel(wrap), bbox: bb(wrap),
              description: `Table container is ${Math.round(totalHeight)}px tall but only ${Math.round(usedHeight)}px used (${Math.round(emptyPx)}px empty, ${Math.round(emptyRatio*100)}%). Either shrink container to fit content, or fill with placeholder/empty state.`
            });
          }
        }
      }
    }

    // ── 2. Sr#/ID column reverse-ordered ─────────────────────────────────
    if (reverseFlagged < 2 && bodyRows.length >= 3 && headerCells.length > 0) {
      // Find an index/serial column by header text
      let serialColIdx = -1;
      for (let i = 0; i < headerCells.length; i++) {
        const txt = (headerCells[i].innerText || '').trim().toLowerCase();
        if (/^(sr\.?#?|s\.?no|serial|#|id|index)$/i.test(txt) || /^(sr\.?\s*#|s\.?\s*no\.?)$/i.test(txt)) {
          serialColIdx = i;
          break;
        }
      }
      if (serialColIdx >= 0) {
        const numbers = [];
        for (const row of bodyRows.slice(0, 10)) {
          const cells = [...row.querySelectorAll('td, [role="cell"]')];
          if (!cells[serialColIdx]) continue;
          const n = parseInt((cells[serialColIdx].innerText || '').trim(), 10);
          if (Number.isFinite(n)) numbers.push(n);
        }
        if (numbers.length >= 3) {
          // Check descending: every pair n[i] > n[i+1]
          let descending = true, ascending = true;
          for (let i = 1; i < numbers.length; i++) {
            if (numbers[i] >= numbers[i-1]) descending = false;
            if (numbers[i] <= numbers[i-1]) ascending = false;
          }
          if (descending && !ascending) {
            reverseFlagged++;
            out.push({
              issueType: 'tableSerialColumnReversed', severity: 'medium',
              selector: sel(headerCells[serialColIdx]), bbox: bb(headerCells[serialColIdx]),
              description: `Sr#/ID column shows descending values (${numbers.slice(0, 5).join(', ')}...). Users expect ascending (1, 2, 3,…) when scrolling top-to-bottom. Reverse the sort or remove the serial column.`
            });
          }
        }
      }
    }

    // ── 3. Visible column has no content in any row ──────────────────────
    if (emptyColFlagged < 3 && bodyRows.length >= 3 && headerCells.length > 0) {
      for (let colIdx = 0; colIdx < headerCells.length; colIdx++) {
        if (emptyColFlagged >= 3) break;
        const hdrTxt = (headerCells[colIdx].innerText || '').trim().toLowerCase();
        if (/^(actions?|operations?|edit|delete)$/i.test(hdrTxt)) continue;   // action columns naturally have icons not text
        // Sample up to 8 rows
        let emptyCount = 0, sampled = 0;
        for (const row of bodyRows.slice(0, 8)) {
          const cells = [...row.querySelectorAll('td, [role="cell"]')];
          if (!cells[colIdx]) continue;
          sampled++;
          const cellTxt = (cells[colIdx].innerText || '').replace(/\s+/g, '').trim();
          const hasContent = cellTxt.length > 0 && cellTxt !== '-' && cellTxt !== '—' && cellTxt !== 'N/A' && cellTxt !== '--';
          const hasIcon = !!cells[colIdx].querySelector('svg, img, i.fa, i.material-icons');
          if (!hasContent && !hasIcon) emptyCount++;
        }
        if (sampled >= 3 && emptyCount === sampled) {
          emptyColFlagged++;
          out.push({
            issueType: 'tableColumnAllEmpty', severity: 'low',
            selector: sel(headerCells[colIdx]), bbox: bb(headerCells[colIdx]),
            description: `Column "${hdrTxt || 'unnamed'}" is empty in all ${sampled} visible rows. Either populate it, show a placeholder (dash), or remove the column.`
          });
        }
      }
    }

    // ── 4. Sort indicator inconsistency ──────────────────────────────────
    if (sortFlagged < 2 && headerCells.length >= 3) {
      let withIndicator = 0, withoutIndicator = 0;
      for (const h of headerCells) {
        const hasSortIcon = !!h.querySelector('svg, [class*="sort"], [class*="arrow"], .mat-sort-header-arrow');
        const ariaSort = h.getAttribute('aria-sort');
        const dataSort = h.getAttribute('data-sortable') || h.getAttribute('data-sort');
        const textChevron = /[▲▼↑↓↕⇅⬍]/.test((h.innerText || ''));
        if (hasSortIcon || ariaSort || dataSort === 'true' || dataSort === '' || textChevron) {
          withIndicator++;
        } else {
          // Exclude Actions / Status columns by name
          const t = (h.innerText || '').trim().toLowerCase();
          if (!/^(actions?|operations?|status)$/i.test(t)) withoutIndicator++;
        }
      }
      if (withIndicator >= 2 && withoutIndicator >= 1) {
        sortFlagged++;
        out.push({
          issueType: 'tableSortIndicatorInconsistent', severity: 'low',
          selector: sel(tbl), bbox: bb(tbl),
          description: `${withIndicator} columns have sort indicators, ${withoutIndicator} similar data columns don't. Mark all sortable columns OR add aria-sort="none" to unsortable ones — currently ambiguous.`
        });
      }
    }

    // ── 5. Action buttons too close (misclick risk) ──────────────────────
    if (actionFlagged < 3 && bodyRows.length > 0) {
      for (const row of bodyRows.slice(0, 5)) {
        if (actionFlagged >= 3) break;
        const actions = [...row.querySelectorAll('button, a, [role="button"], svg[onclick], i[onclick]')]
          .filter(visible);
        if (actions.length < 2) continue;
        // Check pairs in the same row
        for (let i = 1; i < actions.length; i++) {
          const a = actions[i-1].getBoundingClientRect();
          const b = actions[i].getBoundingClientRect();
          if (Math.abs(a.top - b.top) > 12) continue;   // not same line
          const gap = b.left - a.right;
          if (gap >= 0 && gap < 8) {
            actionFlagged++;
            out.push({
              issueType: 'tableActionButtonsTooClose', severity: 'medium',
              selector: sel(row), bbox: bb(row),
              description: `Adjacent action controls in same row are ${gap.toFixed(0)}px apart. Misclick risk — increase gap to ≥ 8px (WCAG 2.5.5 spacing).`
            });
            break;
          }
        }
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 2 empty-space + 2 reverse + 3 empty-col + 2 sort + 3 action-gap = max ~12 findings
- Self-skips: page with no tables returns []
- The `tableExcessiveEmptySpace` is the EXACT bug from your Districts screenshot (1 row, hundreds of px of dead space below)
- The `tableSerialColumnReversed` is the EXACT bug from your Clusters screenshot (Sr# = 7 at top descending to 1 at bottom)
- The `tableColumnAllEmpty` catches the Description column being blank for all rows in your Clusters page
