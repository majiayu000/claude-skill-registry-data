---
name: qa-detect-orientation
section: responsiveness
description: "Detects layout breakage in landscape orientation on mobile/tablet — swaps viewport dimensions and scans for overflow, cut-off content, and unusable navigation."
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
---

## How the orchestrator runs this (resize + ONE probe call)

🚨 **This skill is EXECUTABLE but `partial`:** the detection logic is a single in-page probe, but landscape orientation requires a REAL viewport swap that `browser_evaluate` cannot do. The orchestrator wraps the probe in a resize:

## MCP steps (resize only)

**Step 4 (restore) is mandatory — run it even if the probe call errors.**

1. `orig = browser_evaluate(() => ({ w: window.innerWidth, h: window.innerHeight }))` — save `{w, h}`.
2. `browser_resize(width=orig.h, height=orig.w)` — swap dimensions (portrait → landscape).
3. `browser_wait_for(time=400)` — let CSS media queries settle.
4. `result = browser_evaluate(<the async function in "## Interactive Probe" below>)` — collect `findings[]`.
5. `browser_resize(width=orig.w, height=orig.h)` — **RESTORE original orientation.**
6. `browser_wait_for(time=200)`.

If `browser_resize` is unavailable in the active MCP session, emit zero findings and set `screenshotSkipReason="viewport resize unsupported"` — do not run the probe at the portrait viewport. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const out = [];
  const sel = el => { const id = el.id ? `#${el.id}` : ''; return (el.tagName.toLowerCase() + id).slice(0, 120); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const vw = window.innerWidth;
  const vh = window.innerHeight;

  // 1. Horizontal overflow in landscape
  if (document.documentElement.scrollWidth > vw + 2) {
    out.push({ skill: 'qa-detect-orientation', issueType: 'landscapeOverflow', severity: 'high', selector: 'html',
      description: `Horizontal overflow in landscape orientation (${vw}×${vh}) — scrollWidth ${document.documentElement.scrollWidth}px`,
      bbox: { x: 0, y: 0, w: 200, h: 80 } });
  }

  // 2. Fixed headers/banners covering too much vertical space (landscape is short)
  let fixedCount = 0;
  for (const el of document.querySelectorAll('header, nav, [class*="sticky"], [class*="fixed"]')) {
    if (fixedCount >= 10) break;
    const style = getComputedStyle(el);
    if (style.position !== 'fixed' && style.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (r.height > vh * 0.40) {
      fixedCount++;
      out.push({ skill: 'qa-detect-orientation', issueType: 'landscapeFixedTooTall', severity: 'high', selector: sel(el),
        description: `Fixed/sticky ${sel(el)} is ${Math.round((r.height/vh)*100)}% of landscape viewport height — leaves little room for content`,
        bbox: bb(el) });
    }
  }

  // 3. Modals/dialogs that don't fit landscape viewport
  for (const el of document.querySelectorAll('[role="dialog"], [aria-modal="true"], .modal, .dialog')) {
    if (out.length >= 15) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.height > vh + 4) {
      out.push({ skill: 'qa-detect-orientation', issueType: 'landscapeModalTooTall', severity: 'high', selector: sel(el),
        description: `Modal ${sel(el)} (${Math.round(r.height)}px tall) overflows landscape viewport (${vh}px) — buttons may be unreachable`,
        bbox: bb(el) });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| landscapeOverflow | high | "Horizontal overflow in landscape orientation" |
| landscapeFixedTooTall | high | "Fixed element occupies >40% of landscape height" |
| landscapeModalTooTall | high | "Modal taller than landscape viewport — buttons unreachable" |

## Notes on this conversion
- The detection logic (the old `scanLandscape` probe) is now a single async `browser_evaluate` call. Same checks, same issueTypes.
- Marked `executable: partial` because landscape requires a REAL `browser_resize` (swap width/height) that `browser_evaluate` cannot perform — the orchestrator resizes, calls the probe once, then restores. The `captureOrientation` step is inlined into MCP step 1.
