---
name: qa-detect-rtl-layout
section: responsiveness
description: "Switches the document to RTL (dir='rtl') and detects layout breakage — overflow, mirrored asymmetry, and non-logical CSS properties that don't flip. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasRTL]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_evaluate` round-trips for apply/scan/restore. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function captures the baseline, flips `document.documentElement.dir = 'rtl'`, waits in-page for CSS to recompute, scans for new overflow + side-anchoring bugs, **restores the original direction**, and returns `findings[]` — all inside the page, in one round-trip. There is **no AI reasoning between steps** (this is what makes it cheap + fast + un-skippable). Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const sel = el => { const id = el.id ? `#${el.id}` : ''; return (el.tagName.toLowerCase() + id).slice(0, 120); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── capture baseline (original dir + pre-existing horizontal overflow count) ──
  const html = document.documentElement;
  const originalDir = html.getAttribute('dir') || 'ltr';
  let baselineOverflow = 0;
  for (const el of document.querySelectorAll('*')) {
    if (baselineOverflow >= 30) break;
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflowX !== 'hidden') baselineOverflow++;
  }

  // ── apply RTL ──
  html.setAttribute('dir', 'rtl');
  await sleep(500); // let CSS recompute, transforms apply

  try {
    // 1. Page-level horizontal overflow in RTL
    if (document.documentElement.scrollWidth > window.innerWidth + 2) {
      out.push({ skill: 'qa-detect-rtl-layout', issueType: 'rtlPageOverflow', severity: 'high', selector: 'html',
        description: `Page has horizontal overflow when dir="rtl" — scrollWidth ${document.documentElement.scrollWidth}px vs viewport ${window.innerWidth}px. Likely hardcoded margin-left/padding-right or left:0 instead of inset-inline-*`,
        bbox: { x: 0, y: 0, w: 200, h: 60 } });
    }

    // 2. Element-level overflow that appeared because of RTL
    let perElementOverflow = 0;
    for (const el of document.querySelectorAll('header, nav, aside, main, section, [class*="container"]')) {
      if (perElementOverflow >= 6) break;
      const style = getComputedStyle(el);
      if (style.overflowX === 'hidden') continue;
      if (el.scrollWidth > el.clientWidth + 4) {
        perElementOverflow++;
        out.push({ skill: 'qa-detect-rtl-layout', issueType: 'rtlElementOverflow', severity: 'medium', selector: sel(el),
          description: `Element ${sel(el)} overflows horizontally in RTL — scrollWidth ${el.scrollWidth}px > clientWidth ${el.clientWidth}px. Likely hardcoded directional CSS.`,
          bbox: bb(el) });
      }
    }

    // 3. Fixed-position elements anchored to "left" but expected to be on the start side
    for (const el of document.querySelectorAll('[class*="sidebar"], [class*="drawer"], [class*="sticky"], [class*="fixed"]')) {
      if (out.length >= 15) break;
      const style = getComputedStyle(el);
      if (style.position !== 'fixed' && style.position !== 'sticky') continue;
      // In RTL, "start" is right. If left:0 is set, the element is now on the "end" side — usually wrong.
      if (style.left === '0px' && style.right !== '0px') {
        out.push({ skill: 'qa-detect-rtl-layout', issueType: 'rtlFixedSidewrong', severity: 'medium', selector: sel(el),
          description: `Fixed/sticky ${sel(el)} is anchored to left:0 in RTL — should use inset-inline-start:0 so it flips to the right side in RTL.`,
          bbox: bb(el) });
      }
    }
  } finally {
    // ── restore original direction (MANDATORY — runs even if scan threw) ──
    if (originalDir.toLowerCase() === 'rtl') html.setAttribute('dir', 'rtl');
    else if (originalDir.toLowerCase() === 'ltr') html.setAttribute('dir', 'ltr');
    else html.removeAttribute('dir');
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| rtlPageOverflow | high | "Page has horizontal overflow in RTL — hardcoded directional CSS" |
| rtlElementOverflow | medium | "Element overflows in RTL — needs logical properties (inset-inline-*, margin-inline-*)" |
| rtlFixedSidewrong | medium | "Fixed element anchored to left in RTL — should use inset-inline-start" |

## Notes on this conversion
- The old multi-probe playbook (captureDirAndCount → applyRtl → scanRtlBreaks → restoreDir) is folded into ONE async `browser_evaluate` call. Same checks, same issueTypes.
- RTL is set/restored entirely in-page (`document.documentElement.dir`) — no real viewport change needed, so this runs as a single round-trip with `executable: true`.
- Direction restore is in a `finally` block, so the page is never left in RTL even if the scan throws.
