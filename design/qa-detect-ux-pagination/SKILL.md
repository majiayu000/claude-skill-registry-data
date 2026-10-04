---
name: qa-detect-ux-pagination
section: visual
description: "Detects pagination UX gaps: large table (488 rows total) with only 10-20 rows per page and no rows-per-page selector to increase the limit, pagination component without 'X total' count, page number buttons overflow the visible area, first/last page buttons missing. Catches the 'I have 488 students but the pager only shows 10 at a time' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasPagination]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `paginationNoPageSizeSelector` | medium | Table has pagination AND > 100 total rows but no visible "rows per page" selector — users stuck with default page size (your Students page: 488 total, 11 per page, no resize control) |
| `paginationNoTotalCount` | low | Pagination is present but no "X total" / "showing 1-10 of 488" indicator visible — users have no sense of dataset size |
| `paginationPageNumbersOverflow` | medium | Visible page numbers cause horizontal overflow (e.g. 20+ page buttons all visible at once instead of `1 2 3 ... 20`) |
| `paginationNoFirstLastButtons` | low | Pagination has prev/next but no first/last buttons on a large dataset (> 5 pages) — slow navigation |
| `paginationNoActivePageIndicator` | medium | Current page button has no visible distinguishing style from other page buttons — user can't tell which page they're on |
| `paginationOutsideOfContainer` | low | Pagination control sits outside the table's visual container — looks disconnected |

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

  // Find paginators
  const paginators = [...document.querySelectorAll(
    '[class*="paginat" i], .pagination, [role="navigation"][aria-label*="paginat" i], mat-paginator, .ngx-pagination, .ng-paginator'
  )].filter(visible);

  if (paginators.length === 0) return out;

  for (const pag of paginators.slice(0, 2)) {
    // Try to extract total count from body text near paginator
    let totalCount = null;
    const totalEl = pag.parentElement || pag.closest('table, .table, .data-grid, main, [role="main"]');
    const totalText = (totalEl ? totalEl.innerText : '').trim();
    const totalMatch = totalText.match(/(\d{1,3}(?:,\d{3})+|\d{3,})\s*(?:total|records|results|items|entries|rows)/i) ||
                      totalText.match(/of\s+(\d{1,3}(?:,\d{3})+|\d{3,})/i);
    if (totalMatch) totalCount = parseInt(totalMatch[1].replace(/,/g, ''), 10);

    // ── 1. No rows-per-page selector for large dataset ──────────────────
    if (totalCount && totalCount > 100) {
      const pageSizeSelector = pag.querySelector('select, [role="combobox"], [class*="page-size"], [class*="rows-per-page"], [aria-label*="per page" i], [aria-label*="page size" i]') ||
                              (totalEl && totalEl.querySelector('select, [class*="page-size"], [class*="rows-per-page"], [aria-label*="per page" i]'));
      if (!pageSizeSelector || !visible(pageSizeSelector)) {
        out.push({
          issueType: 'paginationNoPageSizeSelector', severity: 'medium',
          selector: sel(pag), bbox: bb(pag),
          description: `Table has ${totalCount} total rows but no visible "rows per page" selector. Users can't increase the page size — add 10/25/50/100 options.`
        });
      }
    }

    // ── 2. No total count display ───────────────────────────────────────
    if (!totalCount) {
      out.push({
        issueType: 'paginationNoTotalCount', severity: 'low',
        selector: sel(pag), bbox: bb(pag),
        description: `Paginator has no visible "X total" / "showing 1-10 of N" count. Users have no sense of dataset size.`
      });
    }

    // ── 3. Page numbers overflow ────────────────────────────────────────
    const pageButtons = [...pag.querySelectorAll('button, a, [role="button"]')]
      .filter(b => visible(b) && /^[0-9]+$/.test((b.innerText || '').trim()));
    if (pageButtons.length >= 8) {
      // Are they overflowing horizontally?
      const pagR = pag.getBoundingClientRect();
      const rightmost = Math.max(...pageButtons.map(b => b.getBoundingClientRect().right));
      const leftmost = Math.min(...pageButtons.map(b => b.getBoundingClientRect().left));
      const totalNumbersWidth = rightmost - leftmost;
      // Ellipsis present? Look for "..." in any sibling
      const hasEllipsis = (pag.innerText || '').includes('...') || (pag.innerText || '').includes('…') ||
                         pag.querySelector('[class*="ellipsis"], [class*="dots"]');
      if (!hasEllipsis && totalNumbersWidth > pagR.width * 0.7) {
        out.push({
          issueType: 'paginationPageNumbersOverflow', severity: 'medium',
          selector: sel(pag), bbox: bb(pag),
          description: `Paginator shows ${pageButtons.length} page-number buttons all at once (taking ${totalNumbersWidth.toFixed(0)}px). Use truncation pattern: "1 2 3 ... 20" with ellipsis.`
        });
      }
    }

    // ── 4. No first/last buttons on large dataset ──────────────────────
    if (totalCount && totalCount > 100) {
      const firstBtn = pag.querySelector('[aria-label*="first" i], [class*="first-page"]') ||
        [...pag.querySelectorAll('button')].find(b => /^(\s*[⏮«]\s*|first)$/i.test((b.innerText||'').trim()));
      const lastBtn = pag.querySelector('[aria-label*="last" i], [class*="last-page"]') ||
        [...pag.querySelectorAll('button')].find(b => /^(\s*[⏭»]\s*|last)$/i.test((b.innerText||'').trim()));
      if (!firstBtn && !lastBtn) {
        // Also check icon buttons positioned at extreme ends
        const allBtns = [...pag.querySelectorAll('button')].filter(visible);
        if (allBtns.length >= 4) {
          out.push({
            issueType: 'paginationNoFirstLastButtons', severity: 'low',
            selector: sel(pag), bbox: bb(pag),
            description: `Large paginator (${totalCount} rows) has no First/Last page buttons. Users have to click Next many times to reach the end.`
          });
        }
      }
    }

    // ── 5. Active page indicator missing/subtle ────────────────────────
    if (pageButtons.length >= 2) {
      // Find active button (.active, .selected, aria-current, etc.)
      const active = pageButtons.find(b => {
        const cls = (b.className || '').toString();
        return /\b(active|selected|current|is-active|router-link-active)\b/.test(cls) ||
               b.getAttribute('aria-current') === 'page' ||
               b.getAttribute('aria-current') === 'true';
      });
      if (!active) {
        out.push({
          issueType: 'paginationNoActivePageIndicator', severity: 'medium',
          selector: sel(pag), bbox: bb(pag),
          description: `Pagination has page numbers but no .active / .selected / aria-current item. User can't tell which page they're on.`
        });
      }
    }

    // ── 6. Paginator outside of table container ────────────────────────
    const nearestTable = document.querySelector('table, [role="table"], [role="grid"]');
    if (nearestTable && visible(nearestTable)) {
      const tableWrap = nearestTable.closest('.table-wrapper, .table-container, .card, .panel') || nearestTable.parentElement;
      if (tableWrap && !tableWrap.contains(pag)) {
        const tr = tableWrap.getBoundingClientRect();
        const pr = pag.getBoundingClientRect();
        // Significant horizontal disconnect: pagination's center is far from table's center
        const tableCx = tr.left + tr.width / 2;
        const pagCx = pr.left + pr.width / 2;
        if (Math.abs(tableCx - pagCx) > tr.width * 0.3) {
          out.push({
            issueType: 'paginationOutsideOfContainer', severity: 'low',
            selector: sel(pag), bbox: bb(pag),
            description: `Pagination control sits outside the table's container — visually disconnected from the data it paginates.`
          });
        }
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 6 issue types × up to 2 paginators = max ~12 findings per cell
- Self-skips: page with no paginator returns []
- The `paginationNoPageSizeSelector` catches your Students page: 488 total rows, only 11 visible per page, no way to change page size
- Detection of `totalCount` uses regex on nearby text — matches `"488 total"`, `"showing 1-10 of 488"`, etc.
