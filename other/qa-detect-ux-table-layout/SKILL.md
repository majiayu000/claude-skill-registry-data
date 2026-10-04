---
name: qa-detect-ux-table-layout
section: visual
description: "Catches table layout UX bugs: header bar narrower than container (dead space on the right), header doesn't align with body columns, last column has header but no body cells, Actions column empty in every row, missing sticky header on long tables. Catches the 'why is there empty space at the end of my table' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasTables]
---

## What it catches — 7 issue types

| issueType | severity | What |
|---|---|---|
| `tableHeaderShortOfContainer` | medium | Table header bar is narrower than its container by > 16px — visible dead space on the right (your Departments page bug) |
| `tableLastColumnHasNoCells` | medium | Table has a trailing header column but ZERO matching body cells — phantom column |
| `tableHeaderBodyWidthMismatch` | low | Table header row total width differs from body row total width by > 8px — columns visually drift |
| `tableActionsColumnEmpty` | low | Header has "Actions" / "Operations" column but no row contains action buttons/icons |
| `tableNoStickyHeader` | low | Table with > 20 visible rows has no sticky header — users scroll past column labels |
| `tableNoZebraStriping` | low | Table with > 8 rows uses no alternating row background (zebra striping) — eye loses position |
| `tableEmptyHeaderCell` | low | Table has a header cell with no text, no aria-label, no icon — phantom column header |

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
  let containerFlagged = 0, phantomColFlagged = 0, widthFlagged = 0,
      actionsFlagged = 0, stickyFlagged = 0, zebraFlagged = 0, emptyHdrFlagged = 0;

  for (const tbl of tables.slice(0, 5)) {
    // ── 1. Header bar shorter than container ──────────────────────────────
    if (containerFlagged < 3) {
      const head = tbl.querySelector('thead, [role="rowgroup"]:first-child') || tbl.querySelector('thead');
      const headRow = head ? head.querySelector('tr, [role="row"]') : tbl.querySelector('tr:first-child, [role="row"]:first-child');
      if (headRow && visible(headRow)) {
        const headR = headRow.getBoundingClientRect();
        // Find the parent wrapper (often .table-wrapper or the immediate parent)
        const wrap = tbl.closest('.table-wrapper, .table-container, .table-responsive, .data-table, .mat-table-container') || tbl.parentElement;
        if (wrap && visible(wrap)) {
          const wrapR = wrap.getBoundingClientRect();
          // Only flag if there's significant unused space on the right
          const deadSpace = wrapR.right - headR.right;
          if (deadSpace > 16 && headR.width < wrapR.width * 0.95) {
            containerFlagged++;
            out.push({
              issueType: 'tableHeaderShortOfContainer', severity: 'medium',
              selector: sel(tbl), bbox: bb(tbl),
              description: `Table header is ${headR.width.toFixed(0)}px wide but container is ${wrapR.width.toFixed(0)}px (${deadSpace.toFixed(0)}px dead space on right). Either expand columns to fill, or shrink container — current layout looks broken/cut.`
            });
          }
        }
      }
    }

    // ── 2 + 3. Last column has no cells / header-body width mismatch ─────
    const headerCells = [...tbl.querySelectorAll('thead th, thead [role="columnheader"], [role="row"]:first-child > [role="columnheader"]')].filter(visible);
    const bodyRows = [...tbl.querySelectorAll('tbody tr, [role="rowgroup"]:not(:first-child) [role="row"]')].filter(visible);
    if (headerCells.length > 0 && bodyRows.length > 0) {
      // 2. Trailing header with zero body cells in that column
      if (phantomColFlagged < 2) {
        const lastHdr = headerCells[headerCells.length - 1];
        const lastHdrR = lastHdr.getBoundingClientRect();
        // Count how many body rows have a cell in the last column's X range
        let cellsInLastCol = 0;
        for (const row of bodyRows.slice(0, 10)) {
          const cells = [...row.querySelectorAll('td, [role="cell"], [role="gridcell"]')];
          if (cells.length === 0) continue;
          const lastCell = cells[cells.length - 1];
          const cellR = lastCell.getBoundingClientRect();
          // Cell sits under the last header (overlap > 50% of header width)
          const overlap = Math.min(cellR.right, lastHdrR.right) - Math.max(cellR.left, lastHdrR.left);
          if (overlap > lastHdrR.width * 0.5) cellsInLastCol++;
        }
        if (cellsInLastCol === 0) {
          phantomColFlagged++;
          const lastHdrText = (lastHdr.innerText || '').trim().slice(0, 40);
          out.push({
            issueType: 'tableLastColumnHasNoCells', severity: 'medium',
            selector: sel(lastHdr), bbox: bb(lastHdr),
            description: `Header column "${lastHdrText}" exists but no body row has a cell underneath it. Phantom column — either populate it or remove the header.`
          });
        }
      }

      // 3. Header total width vs body row width
      if (widthFlagged < 2) {
        const headRow = headerCells[0].parentElement;
        const firstBodyRow = bodyRows[0];
        if (headRow && firstBodyRow) {
          const hr = headRow.getBoundingClientRect();
          const br = firstBodyRow.getBoundingClientRect();
          const widthDiff = Math.abs(hr.width - br.width);
          if (widthDiff > 8 && Math.min(hr.width, br.width) > 100) {
            widthFlagged++;
            out.push({
              issueType: 'tableHeaderBodyWidthMismatch', severity: 'low',
              selector: sel(tbl), bbox: bb(tbl),
              description: `Header row width ${hr.width.toFixed(0)}px vs body row width ${br.width.toFixed(0)}px (${widthDiff.toFixed(0)}px drift). Columns visually misaligned.`
            });
          }
        }
      }
    }

    // ── 4. Actions column has no buttons ─────────────────────────────────
    if (actionsFlagged < 2 && headerCells.length > 0 && bodyRows.length > 0) {
      const actionsHdr = headerCells.find(h => /^(actions?|operations?|do|controls?)$/i.test((h.innerText || '').trim()));
      if (actionsHdr) {
        const actHdrR = actionsHdr.getBoundingClientRect();
        let actionsFound = 0;
        for (const row of bodyRows.slice(0, 10)) {
          const cells = [...row.querySelectorAll('td, [role="cell"]')];
          for (const c of cells) {
            const cellR = c.getBoundingClientRect();
            const overlap = Math.min(cellR.right, actHdrR.right) - Math.max(cellR.left, actHdrR.left);
            if (overlap > actHdrR.width * 0.5) {
              if (c.querySelector('button, a, [role="button"], svg, i')) actionsFound++;
              break;
            }
          }
        }
        if (actionsFound === 0) {
          actionsFlagged++;
          out.push({
            issueType: 'tableActionsColumnEmpty', severity: 'low',
            selector: sel(actionsHdr), bbox: bb(actionsHdr),
            description: `"Actions" column header exists but no row contains action buttons / icons. Empty column.`
          });
        }
      }
    }

    // ── 5. Long table without sticky header ──────────────────────────────
    if (stickyFlagged < 2 && bodyRows.length > 20) {
      const head = tbl.querySelector('thead');
      if (head) {
        const cs = getComputedStyle(head);
        const pos = cs.position;
        if (pos !== 'sticky' && pos !== 'fixed') {
          stickyFlagged++;
          out.push({
            issueType: 'tableNoStickyHeader', severity: 'low',
            selector: sel(tbl), bbox: bb(tbl),
            description: `Table with ${bodyRows.length} rows has no sticky/fixed header. Users scroll past column labels and lose context.`
          });
        }
      }
    }

    // ── 6. Long table without zebra striping ─────────────────────────────
    if (zebraFlagged < 2 && bodyRows.length > 8) {
      const r0 = bodyRows[0];
      const r1 = bodyRows[1];
      if (r0 && r1) {
        const bg0 = getComputedStyle(r0).backgroundColor;
        const bg1 = getComputedStyle(r1).backgroundColor;
        // Identical AND not transparent → no striping
        if (bg0 === bg1 && !/(transparent|rgba\(.*,\s*0\))/i.test(bg0)) {
          zebraFlagged++;
          out.push({
            issueType: 'tableNoZebraStriping', severity: 'low',
            selector: sel(tbl), bbox: bb(tbl),
            description: `Table with ${bodyRows.length} rows has uniform row background (${bg0}). Add nth-child striping for readability.`
          });
        }
      }
    }

    // ── 7. Empty header cell (no text, no aria-label, no icon) ───────────
    if (emptyHdrFlagged < 2) {
      for (const h of headerCells) {
        const text = (h.innerText || '').trim();
        const ariaLabel = (h.getAttribute('aria-label') || '').trim();
        const hasIcon = !!h.querySelector('svg, i, img');
        if (text.length === 0 && ariaLabel.length === 0 && !hasIcon) {
          emptyHdrFlagged++;
          out.push({
            issueType: 'tableEmptyHeaderCell', severity: 'low',
            selector: sel(h), bbox: bb(h),
            description: `Empty table header cell — no text, no aria-label, no icon. Phantom column with no purpose.`
          });
          break;
        }
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 3 header-container + 2 phantom + 2 width-drift + 2 actions + 2 sticky + 2 zebra + 2 empty-hdr = max ~15 findings
- Self-skips: page with no tables returns []
- The `tableHeaderShortOfContainer` is the EXACT bug from the user's Departments screenshot (red box on right side of header)
- Viewport-sensitive: layout issues manifest differently at mobile/tablet/desktop widths
