---
name: qa-detect-breakpoint-edge
section: responsiveness
description: "Detects layout bugs at exact CSS breakpoint boundaries by extracting the page's actual @media values and probing at (boundary - 1px) vs (boundary + 1px). Catches CSS transitions that work at 390px and 1440px but break at 767/768 or 1023/1024."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: true
executable: partial
cacheVersion: "1.0.0"
ownership: "exclusive: any finding about layout breakage AT or NEAR a media-query boundary belongs to this skill"
---

# qa-detect-breakpoint-edge — Breakpoint Boundary Testing

Single skill that catches the most common class of responsive bug: CSS that works at typical viewports (390, 768, 1440) but breaks at the transition (767, 1024). The viewport changes themselves require MCP `browser_resize` (a real browser-level operation), so this skill is `executable: partial`: **every measurement and the entire diff are done by ONE in-page probe**; only the resizes between measurements are MCP calls.

## How the orchestrator runs this (probe does ALL measurement + diff; MCP does only the resizes)

🚨 **This skill's measurement and comparison logic is a single in-page probe — do NOT hand-write diff logic in the orchestrator.** The only MCP calls are `browser_resize` (browser-level, cannot run in-page) and the `browser_wait_for` between them. Flow:

1. **One** `browser_evaluate` call with `mode:'detect'` → returns the page's actual breakpoints. If empty → **self-skip**.
2. For each breakpoint B (cap 6): `browser_resize(B-1)` → wait → `browser_evaluate(mode:'snapshot')` → `browser_resize(B+1)` → wait → `browser_evaluate(mode:'snapshot')`.
3. **One** `browser_evaluate` call with `mode:'diff'` passing both snapshots back in → returns `findings[]` for that breakpoint (the WHOLE diff runs in-page; the orchestrator just collects findings).
4. `browser_resize(original)` → wait — **MANDATORY restore**.

Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields. The diff logic lives entirely inside the probe so the orchestrator never reasons about layout — it only relays snapshots and findings.

## What it checks (3 issue types)

| Issue type | Severity | What it catches |
|---|---|---|
| `breakpointEdgeBreaks` | high | Layout/overflow finding appears at breakpoint+1px that wasn't at breakpoint-1px |
| `breakpointTransitionShift` | medium | Element position shifts by > 100px between boundary-1 and boundary+1 (CLS at breakpoint) |
| `breakpointMissingMatch` | low | Page has elements with viewport-dependent styles but no @media query found in CSS (likely inline / JS-based — fragile) |

## Self-skip conditions

- Run on desktop viewport only (this skill DRIVES the resize; it doesn't run per viewport).
- Self-skip if `mode:'detect'` returns zero breakpoints (static layout, no media queries).
- Self-skip if `browser_resize` MCP tool is not available (Bash fallback mode).

## MCP steps (resize only)

Resizing the viewport is the only operation that cannot run inside `browser_evaluate`. Per breakpoint B:

```
a. browser_resize({ width: B - 1, height: 800 })
b. browser_wait_for({ time: 600 })          // allow reflow + JS resize handlers
c. minus = browser_evaluate(probe, { mode: 'snapshot' })
d. browser_resize({ width: B + 1, height: 800 })
e. browser_wait_for({ time: 600 })
f. plus  = browser_evaluate(probe, { mode: 'snapshot' })
g. findings = browser_evaluate(probe, { mode: 'diff', minus, plus, boundary: B })
```

After all breakpoints: `browser_resize({ width: original.width, height: original.height })` + `browser_wait_for({ time: 500 })`. Restoration is non-negotiable — the next skill expects the original viewport.

## Interactive Probe (browser_evaluate)

One probe, three modes (`detect` / `snapshot` / `diff`). The orchestrator passes `{mode, ...}` as the argument. `detect` and `diff` are synchronous in-page; `snapshot` reads the current (already-resized) viewport.

```js
(arg) => {
  const mode = (arg && arg.mode) || 'detect';
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0, 120);

  if (mode === 'detect') {
    const breakpoints = new Set();
    const containerQueries = new Set();
    let inaccessibleSheets = 0;
    const walkRules = (rules) => {
      for (const rule of rules) {
        if (rule.type === CSSRule.MEDIA_RULE) {
          for (const m of (rule.conditionText || '').matchAll(/(min|max)-width\s*:\s*(\d+)px/g)) breakpoints.add(parseInt(m[2]));
          if (rule.cssRules) walkRules(rule.cssRules);
        } else if (rule.type === CSSRule.SUPPORTS_RULE && rule.cssRules) {
          walkRules(rule.cssRules);
        } else if ((rule.constructor && rule.constructor.name === 'CSSContainerRule') || rule.type === 11) {
          containerQueries.add(rule.conditionText || rule.containerName || 'unnamed');
        }
      }
    };
    for (const sheet of document.styleSheets) {
      try { walkRules(sheet.cssRules); } catch (_) { inaccessibleSheets++; }
    }
    const sorted = [...breakpoints].sort((a, b) => a - b).slice(0, 6);
    return { breakpoints: sorted, containerQueries: [...containerQueries], inaccessibleSheets, totalFound: breakpoints.size };
  }

  if (mode === 'snapshot') {
    const out = { findings: [], positions: {}, vw: innerWidth, vh: innerHeight };
    for (const el of document.querySelectorAll('main, section, header, footer, nav, [class*="container"], [class*="content"]')) {
      if (out.findings.length >= 15) break;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const style = getComputedStyle(el);
      if (style.overflowX === 'hidden' || style.overflowX === 'scroll' || style.overflowX === 'auto') continue;
      if (el.scrollWidth > el.clientWidth + 2) out.findings.push({ type: 'overflow', sel: sel(el), scrollW: el.scrollWidth, clientW: el.clientWidth });
    }
    for (const el of document.querySelectorAll('h1, h2, header, nav, main, footer, button[type="submit"], .cta, .btn-primary')) {
      if (Object.keys(out.positions).length >= 30) break;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      out.positions[sel(el)] = { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
    }
    return out;
  }

  if (mode === 'diff') {
    const { minus, plus, boundary: B } = arg;
    const findings = [];
    const add = o => findings.push(Object.assign({ skill: 'qa-detect-breakpoint-edge', breakpoint: B }, o));
    if (!minus || !plus) return findings;
    const minusOverflows = new Set((minus.findings || []).filter(f => f.type === 'overflow').map(f => f.sel));
    for (const f of (plus.findings || [])) {
      if (f.type === 'overflow' && !minusOverflows.has(f.sel))
        add({ issueType: 'breakpointEdgeBreaks', severity: 'high', selector: f.sel, bbox: null, description: `Overflow on ${f.sel} appears at viewport ${B + 1}px but not at ${B - 1}px — CSS breakpoint transition broken (scrollWidth ${f.scrollW}px > clientWidth ${f.clientW}px).`, evidence: { scrollW: f.scrollW, clientW: f.clientW } });
    }
    for (const [s, plusBox] of Object.entries(plus.positions || {})) {
      const minusBox = (minus.positions || {})[s];
      if (!minusBox) continue;
      const dx = Math.abs(plusBox.x - minusBox.x), dy = Math.abs(plusBox.y - minusBox.y);
      if (dx > 100 || dy > 100)
        add({ issueType: 'breakpointTransitionShift', severity: 'medium', selector: s, bbox: plusBox, description: `Element ${s} shifts by (Δx=${dx}px, Δy=${dy}px) between viewport ${B - 1}px and ${B + 1}px — visible layout jump at breakpoint.`, evidence: { dx, dy } });
    }
    return findings;
  }

  return [];
}
```

If `mode:'detect'` returns zero breakpoints but the page clearly has viewport-dependent styles (rare — fluid/JS-driven), the orchestrator may emit one `breakpointMissingMatch` (low) for the route.

## Hard rules

1. **MUST restore original viewport before exit** — even on partial failure. The next skill expects `cell.viewport.width × cell.viewport.height`.
2. **Cap at 6 breakpoints** — if the page defines more, test only the 6 smallest.
3. **600 ms wait between resize and snapshot** — less risks catching transitional state; more is wasteful.
4. **Run on desktop cell only** — this skill drives all viewports internally.
5. **Self-skip if no @media rules.**

## Notes on this conversion
- Marked `executable: partial`: viewport resizing is a genuine browser-level operation that `browser_evaluate` cannot perform, so the resizes stay as MCP `browser_resize` steps. **Everything else — breakpoint discovery, per-viewport measurement, and the full minus-vs-plus diff — is now done by ONE in-page probe with three modes**, so the orchestrator no longer hand-codes the comparison (the old version had a `diffSnapshots` JS function the orchestrator ran itself; it now runs in-page via `mode:'diff'`). Same 3 issueTypes preserved.
- The resize-only MCP loop is unavoidable and is documented under "## MCP steps (resize only)". The probe is self-contained for detection, snapshotting, and diffing.
