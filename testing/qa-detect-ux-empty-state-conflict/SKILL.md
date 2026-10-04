---
name: qa-detect-ux-empty-state-conflict
section: visual
description: "Detects the 'system says no results but shows old results anyway' bug class — empty-state toast/banner saying 'Record Not Found' / 'No data' visible at the same time as result cards, rows, or list items still rendered; pagination active during empty state; the same empty-state toast rendered multiple times stacked. Catches your Students filter screenshot bug where 'Record Not Found' toast appeared but the previous RIDA NASIR card stayed visible."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasTables, hasEmptyState]
---

## What it catches — 4 issue types

| issueType | severity | What |
|---|---|---|
| `emptyStateMessageWithVisibleResults` | high | An empty-state message ("No record found", "No data", "0 results", "Nothing here") is visible while result items (cards, table rows, list items) are ALSO visible on the same page. After a filter returned 0 records the previous results should clear. (Your Students screenshot: "Record Not Found" toast with RIDA NASIR card still showing.) |
| `paginationVisibleWithEmptyState` | medium | Pagination controls (page numbers, Next/Prev) are visible while an empty-state message is also visible — pagination is meaningless without data. (Your screenshot: "1" page indicator shown even with "Record Not Found".) |
| `duplicateToastSimultaneous` | medium | Two or more visible toasts share identical text — the system fired the same notification multiple times instead of de-duplicating. (Your screenshot: two stacked "Record Not Found" toasts.) |
| `emptyStateInWrongLocation` | low | Empty-state message appears as a top-right toast/alert when it should be inline in the result area, OR appears inline when results actually exist (stale empty-state) |

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
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.1) return false;
    const r = el.getBoundingClientRect();
    return r.width > 4 && r.height > 4;
  };
  const out = [];

  // Empty-state text patterns (case-insensitive, allow trailing punctuation)
  const emptyRe = /^(record\s*not\s*found|no\s*record(s)?\s*(found|available)?|no\s*data(\s*found)?|no\s*results?(\s*found)?|nothing\s*(found|here)|0\s*results?|empty\s*list|not\s*found)\.?!?$/i;
  const isEmptyText = t => emptyRe.test((t || '').trim());

  // 1) Collect all visible toasts/alerts/snackbars on the page
  const toastSel = '[role="alert"], [role="status"], [class*="toast"], [class*="Toast"], [class*="snackbar"], [class*="Snackbar"], [class*="notification"], [class*="Notification"], .alert, .Alert';
  const toasts = [...document.querySelectorAll(toastSel)]
    .filter(visible)
    .filter(el => {
      // Toasts must be reasonably small (banners or pop-ups), not whole page sections
      const r = el.getBoundingClientRect();
      return r.width < window.innerWidth * 0.7 && r.height < 200;
    });

  // 2) Find empty-state messages — could be in a toast, a banner, or inline text
  const emptyStateEls = [];
  // (a) Toasts whose text matches empty-state pattern
  for (const t of toasts) {
    const txt = (t.innerText || '').trim();
    // Toast often includes close button "×" — scan EACH line plus the whole text
    const lines = txt.split(/\n/).map(s => s.trim()).filter(Boolean);
    // Match line whose substantive part (after stripping × and close labels) is an empty-state phrase
    const matchedLine = lines.find(line => {
      const cleaned = line.replace(/^\s*[×x✕✖✗]\s*/i, '').replace(/\s*[×x✕✖✗]\s*$/i, '').replace(/\s*close\s*$/i, '').trim();
      return isEmptyText(cleaned) || /not\s*found|no\s*record|no\s*data|no\s*results?|nothing\s*found/i.test(cleaned.slice(0, 60));
    });
    // Also try the whole text as a fallback (handles single-line toasts)
    const wholeMatches = /not\s*found|no\s*record|no\s*data|no\s*results?|nothing\s*found/i.test(txt.slice(0, 100));
    if (matchedLine || wholeMatches) {
      const display = matchedLine || txt.replace(/[×x✕✖✗\s]+/g, ' ').trim();
      emptyStateEls.push({ el: t, text: display, kind: 'toast' });
    }
  }
  // (b) Inline empty-state messages (h2/h3/p inside a result region with empty-state phrase)
  const inlineCandidates = document.querySelectorAll(
    '[class*="empty"], [class*="Empty"], [class*="no-data"], [class*="noData"], [class*="no-results"], [class*="noResults"], [class*="not-found"], [class*="notFound"], ' +
    '.result-area p, .results p, [class*="result"] > p, [class*="list"] > p'
  );
  for (const el of inlineCandidates) {
    if (!visible(el)) continue;
    const txt = (el.innerText || '').trim();
    if (txt.length > 0 && txt.length < 80 && (isEmptyText(txt) || /no\s*record|no\s*data|no\s*results?|not\s*found/i.test(txt))) {
      emptyStateEls.push({ el, text: txt, kind: 'inline' });
    }
  }

  // 3) Look at result-area candidates (cards, table rows, list items in the MAIN area)
  // Identify the main content area (skip nav/sidebar/header)
  const main = document.querySelector('main, [role="main"], .main-content, .content-area, [class*="main-content"]') || document.body;
  const resultSel = [
    '.card', '[class*="card"]:not([class*="card-header"]):not([class*="card-title"])',
    'tbody tr',
    '[role="row"]:not([role="rowheader"])',
    'li[class*="item"]', 'li[class*="row"]',
    '[class*="list-item"]', '[class*="ListItem"]',
    '[class*="result-item"]', '[class*="resultItem"]',
    '[class*="record"]', '[class*="Record"]'
  ].join(', ');
  const resultItems = [...main.querySelectorAll(resultSel)]
    .filter(visible)
    .filter(el => {
      // Filter out tiny items, headers, footers, sidebar elements
      const r = el.getBoundingClientRect();
      if (r.width < 80 || r.height < 30) return false;
      // Skip items inside a known sidebar/nav
      if (el.closest('nav, aside, [class*="sidebar"], [class*="Sidebar"], header, [class*="navbar"], [role="navigation"]')) return false;
      // Skip items inside the empty-state toast itself
      if (emptyStateEls.some(e => e.el === el || e.el.contains(el) || el.contains(e.el))) return false;
      // Skip empty containers (must have some text content)
      const txt = (el.innerText || '').trim();
      return txt.length > 0;
    });

  // Deduplicate nested result-items: only keep outermost
  const dedupedResults = [];
  for (const el of resultItems) {
    if (dedupedResults.some(o => o.contains(el))) continue;
    // Remove anything we previously added that this one contains
    for (let i = dedupedResults.length - 1; i >= 0; i--) {
      if (el.contains(dedupedResults[i])) dedupedResults.splice(i, 1);
    }
    dedupedResults.push(el);
  }

  // ── 1. emptyStateMessageWithVisibleResults ──────────────────────────
  if (emptyStateEls.length >= 1 && dedupedResults.length >= 1) {
    const msg = emptyStateEls[0];
    const sampleResult = dedupedResults[0];
    const sampleText = (sampleResult.innerText || '').trim().slice(0, 40).replace(/\s+/g, ' ');
    out.push({
      issueType: 'emptyStateMessageWithVisibleResults', severity: 'high',
      selector: sel(msg.el), bbox: bb(msg.el),
      description: `Empty-state message "${msg.text.slice(0, 40)}" (${msg.kind}) is visible while ${dedupedResults.length} result item(s) remain rendered, e.g. "${sampleText}". After an empty-result response, the previous result list should clear OR the empty-state message should not fire. This is the stale-data-after-empty-filter bug. (Your Students filter screenshot.)`
    });
  }

  // ── 2. paginationVisibleWithEmptyState ──────────────────────────────
  if (emptyStateEls.length >= 1) {
    const paginationSel = '.pagination, [class*="pagination"], [class*="Pagination"], nav[aria-label*="page" i], [role="navigation"][aria-label*="page" i]';
    const paginations = [...document.querySelectorAll(paginationSel)]
      .filter(visible)
      .filter(p => {
        const txt = (p.innerText || '').trim();
        // Real pagination contains digit page-numbers or Next/Prev
        return /\d/.test(txt) || /next|prev|previous|first|last|»|«/i.test(txt);
      });
    if (paginations.length >= 1) {
      out.push({
        issueType: 'paginationVisibleWithEmptyState', severity: 'medium',
        selector: sel(paginations[0]), bbox: bb(paginations[0]),
        description: `Pagination is visible while an empty-state message ("${emptyStateEls[0].text.slice(0, 30)}") is also shown. Pagination should hide when there are no results. (Your Students screenshot: "1" page indicator with "Record Not Found" toast.)`
      });
    }
  }

  // ── 3. duplicateToastSimultaneous ───────────────────────────────────
  if (toasts.length >= 2) {
    const textBuckets = new Map();
    for (const t of toasts) {
      const txt = (t.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80);
      if (txt.length < 3) continue;
      // Normalize: drop trailing × / close-button artifacts
      const norm = txt.replace(/\s*×\s*$/, '').replace(/\s*close\s*$/i, '').trim();
      if (!textBuckets.has(norm)) textBuckets.set(norm, []);
      textBuckets.get(norm).push(t);
    }
    let dupFlagged = 0;
    for (const [txt, group] of textBuckets) {
      if (dupFlagged >= 2) break;
      if (group.length >= 2) {
        dupFlagged++;
        out.push({
          issueType: 'duplicateToastSimultaneous', severity: 'medium',
          selector: sel(group[0]), bbox: bb(group[0]),
          description: `${group.length} simultaneous toasts share the same message: "${txt.slice(0, 50)}". The system fired the same notification multiple times. De-duplicate by text within a 1-2 second window, or suppress re-emit while the prior toast is still visible. (Your Students screenshot: two stacked "Record Not Found" toasts.)`
        });
      }
    }
  }

  // ── 4. emptyStateInWrongLocation ────────────────────────────────────
  // If the empty-state ONLY appears as a top-right toast and never inline in the result area
  // when results genuinely should be empty, that's a UX miss — the result area should show its own empty state.
  // Heuristic: empty-state toast present, no results visible, AND no inline empty-state in the main area.
  if (emptyStateEls.length >= 1 && dedupedResults.length === 0) {
    const onlyToast = emptyStateEls.every(e => e.kind === 'toast');
    // Look for an inline empty-state UI inside the main area: an SVG/icon + heading saying "No data"
    const inlineEmptyUI = main.querySelector(
      '[class*="empty-state"], [class*="emptyState"], [class*="no-data"], [class*="noData"], [class*="no-results"]'
    );
    if (onlyToast && !inlineEmptyUI) {
      const t = emptyStateEls[0];
      out.push({
        issueType: 'emptyStateInWrongLocation', severity: 'low',
        selector: sel(t.el), bbox: bb(t.el),
        description: `Empty-state appears only as a top-right toast ("${t.text.slice(0, 30)}") with no inline empty-state in the result area. Toasts disappear after a few seconds — users who miss them are left with a blank screen and no explanation. Show an inline "No records match these filters" message in the result area.`
      });
    }
  }

  return out;
}
```

## Notes

- Self-skips: pages with no toasts AND no inline empty-state messages return []
- Bounded: 1 stale-results + 1 pagination + 2 duplicate toasts + 1 wrong-location = max ~5 findings per cell
- Catches your Students filter screenshot's three concurrent bugs: (a) stale result card, (b) pagination with no data, (c) two stacked duplicate toasts
- Complements `qa-detect-ux-toast-notification` (which checks toast content quality) by focusing on toast vs page-state conflict
- The `emptyStateMessageWithVisibleResults` is the highest-value: catches the actual stale-data bug class — users see a "no results" message but think the visible row IS the result
