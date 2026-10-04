---
name: qa-test-states
section: interactive
description: "Tests empty state and error state. Empty state runs as ONE in-page async probe (no-match search + empty-state UI check). Error state stays MCP because it needs a real reload after installing a 500 fetch interceptor."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
---
# QA Test — Empty State & Error State

## How the orchestrator runs this

🚨 **The empty-state test is an EXECUTABLE in-page probe — do NOT hand-drive it.** Make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The probe finds a search/filter input, types a no-match term, waits for the debounce, checks for empty-state UI vs. a data container that still shows < 2 rows, returns `findings[]` for `missingEmptyState`, and clears the search before returning. It **self-skips** (returns `[]`) when there is no search/filter input.

The **error-state** test is the HONEST EXCEPTION: it installs a `fetch`/`XHR` interceptor that forces `/api/` calls to 500, then needs a **real page reload** (`browser_navigate` to the same URL) so the app re-fetches through the interceptor. A page-context probe cannot reload itself, so error-state stays MCP (steps below).

## Interactive Probe (browser_evaluate, async) — empty state

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-states' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };

  // find a search/filter input
  const input = [...document.querySelectorAll(
    'input[type="search"], input[placeholder*="search" i], input[placeholder*="filter" i], ' +
    'input[formcontrolname*="search" i], input[aria-label*="search" i], ' +
    '[class*="search-input"] input, mat-form-field input[placeholder*="search" i]'
  )].find(el => vis(el) && !el.disabled);
  if (!input) return []; // no search/filter — self-skip

  // type a no-match term
  input.focus();
  setNative(input, 'xxxxxxxxxx_no_match_empty_test');
  await sleep(1000); // debounce + results update

  // check for empty-state UI
  const emptySelectors = ['[data-testid*="empty"]', '.empty-state', '[class*="no-results"]', '[class*="empty"]', '[class*="zero-state"]', '[class*="empty-state"]', '[aria-label*="no results" i]', '[class*="not-found"]'];
  const hasEmptyState = emptySelectors.some(s => { const el = document.querySelector(s); return el && vis(el); });

  const dataContainer = document.querySelector('table, mat-table, [role="grid"], [class*="list-container"]');
  const rows = dataContainer ? [...dataContainer.querySelectorAll('tr:not(:first-child), mat-row, [role="row"]:not([role="columnheader"])')].filter(r => r.getBoundingClientRect().height > 0) : [];

  if (!hasEmptyState && dataContainer && rows.length < 2)
    add({ issueType: 'missingEmptyState', severity: 'low', selector: sel(dataContainer), bbox: bb(dataContainer), description: 'No empty-state UI shown when search returns zero results', evidence: { note: 'searched for non-existent term, no empty-state UI shown', rowCount: rows.length } });

  // clear search
  input.focus();
  setNative(input, '');
  input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  await sleep(500);

  return out;
}
```

## MCP steps (for error state only — needs a real reload)

```
1. browser_evaluate(probe.installErrorInterceptor)   // wraps fetch + XHR → 500 for /api/, /graphql, /rest/
2. browser_navigate({ url: baseUrl + cell.route, waitUntil: 'domcontentloaded', timeout: 10000 })
3. browser_wait_for(time = 2000)                       // allow framework error handlers to fire
4. errorCheck = browser_evaluate(probe.checkErrorStateUI)
5. If !errorCheck.hasErrorState AND !errorCheck.hasRetryOption → emit missingErrorState (medium)
     evidence: { note: 'API intercepted to return 500, no error UI shown to user' }
6. RESTORE (mandatory): browser_evaluate(probe.removeErrorInterceptor)
   browser_navigate({ url: baseUrl + cell.route, waitUntil: 'domcontentloaded', timeout: 10000 })
   browser_wait_for(time = 800)
```

```js
// probe.installErrorInterceptor
() => {
  if (window.__argusErrorInterceptor) return { alreadyInstalled: true };
  const origFetch = window.fetch;
  window.fetch = async function(...args) {
    const url = (typeof args[0] === 'string' ? args[0] : (args[0] && args[0].url) || '');
    if (/\/api\/|\/graphql|\/rest\//.test(url)) {
      return new Response(JSON.stringify({ error: 'Internal Server Error', status: 500 }), { status: 500, headers: { 'Content-Type': 'application/json' } });
    }
    return origFetch.apply(this, args);
  };
  const OrigXHR = window.XMLHttpRequest;
  class InterceptedXHR extends OrigXHR {
    open(method, url, ...args) { this._argusUrl = url; return super.open(method, url, ...args); }
    send(...args) {
      if (this._argusUrl && /\/api\/|\/graphql|\/rest\//.test(this._argusUrl)) {
        setTimeout(() => {
          Object.defineProperty(this, 'status', { value: 500 });
          Object.defineProperty(this, 'readyState', { value: 4 });
          Object.defineProperty(this, 'responseText', { value: JSON.stringify({ error: 'Internal Server Error' }) });
          this.dispatchEvent(new Event('readystatechange'));
          this.dispatchEvent(new Event('load'));
        }, 100);
        return;
      }
      return super.send(...args);
    }
  }
  window.XMLHttpRequest = InterceptedXHR;
  window.__argusErrorInterceptor = { origFetch, OrigXHR };
  return { installed: true };
}
```

```js
// probe.checkErrorStateUI
() => {
  const errorSelectors = ['[role="alert"]', '[data-testid*="error"]', '.error-state', '[class*="error-state"]', '[class*="error-message"]', '[class*="api-error"]', 'mat-error', '.alert-danger', 'snack-bar-container[class*="error"]', '[class*="http-error"]', '[class*="server-error"]'];
  const hasErrorState = errorSelectors.some(sel => {
    return [...document.querySelectorAll(sel)].some(el => {
      const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
      if (r.width === 0 || s.display === 'none') return false;
      const txt = (el.innerText || '').toLowerCase();
      return txt.length > 3 && !/success|info/i.test(txt);
    });
  });
  const hasRetryOption = !!document.querySelector('button[class*="retry"], button[class*="try-again"], [aria-label*="retry" i], [aria-label*="try again" i]');
  const bodyText = (document.body.innerText || '').toLowerCase().slice(0, 800);
  const hasErrorText = /\b(something went wrong|error loading|failed to load|server error|unable to|please try again|oops)\b/.test(bodyText);
  return { hasErrorState: hasErrorState || hasErrorText, hasRetryOption };
}
```

```js
// probe.removeErrorInterceptor — mandatory restore
() => {
  if (!window.__argusErrorInterceptor) return { wasInstalled: false };
  window.fetch = window.__argusErrorInterceptor.origFetch;
  window.XMLHttpRequest = window.__argusErrorInterceptor.OrigXHR;
  delete window.__argusErrorInterceptor;
  return { removed: true };
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| missingEmptyState | low | "No empty state UI shown when search returns zero results" |
| missingErrorState | medium | "No error state shown when API returns 500 — page silently fails without user feedback" |

## Hard rules
1. **NEVER use `page.route()`** — raw Playwright API, unavailable in MCP. Use `probe.installErrorInterceptor` fetch wrapper instead.
2. **NEVER use `page.reload()`** — use `browser_navigate({url: sameUrl, waitUntil: 'domcontentloaded'})`.
3. **Mandatory cleanup** — `probe.removeErrorInterceptor` MUST run before exit so subsequent skills get real API responses.
4. **Only intercept `/api/`, `/graphql/`, `/rest/`** — don't intercept static assets (CSS, JS, images).

## Notes on this conversion
- Empty-state (1 of 2 issueTypes) folded into ONE in-page async probe; the old `findSearchOrFilter` / `checkEmptyStateUI` / `clearSearch` helper probes are inlined and the `data-argus-search-input` attribute is no longer needed (the probe holds the element reference directly).
- Error-state (`missingErrorState`) stays MCP-driven (`executable: partial`) because forcing the app to re-fetch through the 500 interceptor requires a real `browser_navigate` reload that a page-context probe cannot perform.
