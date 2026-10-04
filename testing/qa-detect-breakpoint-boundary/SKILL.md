---
name: qa-detect-breakpoint-boundary
section: responsiveness
description: "Detects layout breakage at common CSS breakpoint boundaries (767px, 1023px, 1279px) — widths bugs typically hide between standard test viewports."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
---

## How the orchestrator runs this (resize + ONE probe call per boundary)

🚨 **This skill is EXECUTABLE but `partial`:** the detection logic is a single in-page probe, but each boundary needs a REAL viewport resize that `browser_evaluate` cannot do. Bugs hide at the exact pixel where CSS media queries fire; standard viewports (390/820/1440) skip these. The orchestrator resizes to each boundary and calls the probe once per boundary.

## MCP steps (resize only)

**Step 3 (restore) is mandatory even if any probe call errors** — otherwise the page is left at a wrong size for downstream skills.

1. `orig = browser_evaluate(() => ({ w: window.innerWidth, h: window.innerHeight }))` — save `{w, h}`.
2. For each `boundary` in `[767, 1023, 1279]`:
   a. `browser_resize(width=boundary, height=720)`
   b. `browser_wait_for(time=400)` — media queries settle
   c. `result = browser_evaluate(<the async function in "## Interactive Probe" below>, { width: boundary })` — collect `findings[]`
3. `browser_resize(width=orig.w, height=orig.h)` — **RESTORE original viewport.**
4. `browser_wait_for(time=200)`.

If `browser_resize` is unavailable in the active MCP session, emit zero findings and set `screenshotSkipReason="viewport resize unsupported"`. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Interactive Probe (browser_evaluate, async) — args: { width }

```js
async ({ width }) => {
  const out = [];
  const W = width || window.innerWidth;
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // 1. Horizontal scroll at boundary
  if (document.documentElement.scrollWidth > W + 2) {
    out.push({ skill: 'qa-detect-breakpoint-boundary', issueType: 'breakpointOverflow', severity: 'high', selector: 'html',
      description: `Horizontal overflow at ${W}px boundary — scrollWidth ${document.documentElement.scrollWidth}px (page-level)`,
      bbox: { x: 0, y: 0, w: Math.min(W, window.innerWidth), h: 80 } });
  }

  // 2. Elements cut off at right edge of viewport
  let cutCount = 0;
  for (const el of document.querySelectorAll('header, nav, button, a, input, [role="button"], [class*="card"], [class*="menu"]')) {
    if (cutCount >= 12) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > W + 2 && r.left < W) {
      cutCount++;
      out.push({ skill: 'qa-detect-breakpoint-boundary', issueType: 'breakpointElementCutOff', severity: 'medium', selector: sel(el),
        description: `Element ${sel(el)} extends past ${W}px viewport edge at this breakpoint (right edge ${Math.round(r.right)}px)`,
        bbox: bb(el) });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| breakpointOverflow | high | "Horizontal overflow at {width}px breakpoint boundary" |
| breakpointElementCutOff | medium | "Element {selector} cut off at {width}px boundary" |

## Notes on this conversion
- The old `captureOriginalSize` + per-boundary `scanBoundary` is folded so detection is ONE async `browser_evaluate` call (per boundary). Same checks, same issueTypes.
- Marked `executable: partial` because each boundary requires a REAL `browser_resize` that `browser_evaluate` cannot perform — the orchestrator resizes to 767/1023/1279, calls the probe once per width, then restores. The capture step is inlined into MCP step 1.
