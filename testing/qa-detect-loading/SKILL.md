---
name: qa-detect-loading
section: performance
description: "Detects loading spinners stuck 3s after networkidle, blank pages, and 404/error content even when HTTP returned 200 (SPA routing failures)"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
preWait: 3000
---

## What it checks
- `stuckSpinner` — loading indicators still visible 3s after networkidle
- `blankPage` — page body text < 20 chars after load
- `http404Content` — page title or H1/H2 contains "404"/"not found"/"page doesn't exist"/"oops" patterns AND body has < 500 chars (SPA route resolved to error content despite HTTP 200)

## Orchestrator note
Call `browser_wait_for(time=3000)` after the cell's navigation completes, BEFORE running the probe.

## Probe (browser_evaluate)
```js
() => {
  const sel = el => {
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '';
    return (el.tagName.toLowerCase() + (el.id?`#${el.id}`:'') + cls).slice(0,120);
  };
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const q = '[class*="spinner"],[class*="loading"],[role="progressbar"],.skeleton,[class*="skeleton"],[class*="shimmer"],[aria-busy="true"],[data-testid*="loading"],[data-testid*="spinner"]';
  for (const el of document.querySelectorAll(q)) {
    if (out.length >= 10) break;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    out.push({ issueType:'stuckSpinner', severity:'high', selector:sel(el),
      description:'Loading indicator/spinner/skeleton still visible 3s after networkidle', bbox: bb(el) });
  }
  const text = (document.body.innerText || '').trim();
  if (text.length < 20) {
    out.push({ issueType:'blankPage', severity:'critical', selector:null,
      description:`Page appears blank — only ${text.length} chars of text content after load` });
  }

  // http404Content — SPA showing error content despite HTTP 200
  const title = (document.title || '').toLowerCase();
  const h1 = (document.querySelector('h1')?.innerText || '').toLowerCase();
  const h2 = (document.querySelector('h2')?.innerText || '').toLowerCase();
  const errorPattern = /\b404\b|not\s+found|page\s+(doesn'?t|does\s+not)\s+exist|oops|something\s+went\s+wrong|page\s+not\s+available/;
  const titleMatch = errorPattern.test(title);
  const h1Match = errorPattern.test(h1);
  const h2Match = errorPattern.test(h2);
  if ((titleMatch || h1Match || h2Match) && text.length < 500) {
    const matched = [
      titleMatch ? `title="${title.slice(0,60)}"` : '',
      h1Match ? `h1="${h1.slice(0,60)}"` : '',
      h2Match ? `h2="${h2.slice(0,60)}"` : ''
    ].filter(Boolean).join(', ');
    out.push({ issueType:'http404Content', severity:'high', selector:null,
      description:`Page shows error content despite HTTP 200 (SPA route resolved to error): ${matched}, body=${text.length} chars` });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| stuckSpinner | high | "Loading indicator/spinner/skeleton still visible 3s after networkidle" |
| blankPage | critical | "Page appears blank — only {len} chars of text content after load" |
| http404Content | high | "Page shows 404/error content despite HTTP 200 (SPA error route)" |
