---
name: qa-detect-sticky-scroll
section: responsiveness
description: "Tests sticky elements during scroll: they remain pinned, do not overlap content, and do not detach. Scrolls the page, captures state, restores. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasStickyHeader, hasStickyElements]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_evaluate` (scroll) / `browser_wait_for` MCP steps. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function records each sticky/fixed element's baseline position, scrolls the page down (via in-page `window.scrollTo`), waits with an in-page `setTimeout` promise, re-measures, asserts pin/detach behavior, scrolls back to the top, and returns `findings[]` — all inside the page, in one round-trip. There is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when the page has no sticky/fixed elements. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores scroll position (back to 0) and removes its tracking attributes before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-sticky-scroll' }, o));
  const sel = el => { if (!el) return null; const id = el.id ? '#' + el.id : ''; return (el.tagName.toLowerCase() + id).slice(0, 120); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── capture baseline sticky/fixed elements ──
  const baseline = [];
  const all = document.querySelectorAll('header, nav, aside, [class*="sticky"], [class*="fixed"], [class*="navbar"]');
  for (const el of all) {
    const style = getComputedStyle(el);
    if (style.position !== 'sticky' && style.position !== 'fixed') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    el.setAttribute('data-argus-sticky', String(baseline.length));
    baseline.push({ idx: baseline.length, el, selector: sel(el), initialTop: Math.round(r.top), initialBottom: Math.round(r.bottom), position: style.position });
    if (baseline.length >= 6) break;
  }

  // ── self-skip if no sticky/fixed elements ──
  if (baseline.length === 0) {
    for (const el of document.querySelectorAll('[data-argus-sticky]')) { try { el.removeAttribute('data-argus-sticky'); } catch (_) {} }
    return [];
  }

  // page must actually be scrollable for this test to be meaningful
  const maxScroll = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight) - window.innerHeight;
  if (maxScroll < 50) {
    for (const el of document.querySelectorAll('[data-argus-sticky]')) { try { el.removeAttribute('data-argus-sticky'); } catch (_) {} }
    return [];
  }

  const origScroll = window.scrollY;

  // ── scroll down ──
  window.scrollTo({ top: Math.min(800, maxScroll), behavior: 'instant' });
  await sleep(450);

  // ── re-measure each baseline sticky element ──
  for (const b of baseline) {
    const el = document.querySelector(`[data-argus-sticky="${b.idx}"]`);
    if (!el) continue;
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const stillVisible = r.bottom > 0 && r.top < window.innerHeight;
    const detachedFromTop = style.position === 'sticky' && r.top < -2 && !el.closest('[style*="overflow:hidden"]');
    if (detachedFromTop)
      add({ issueType: 'stickyDetachedOnScroll', severity: 'high', selector: b.selector, bbox: bb(el), description: `position:sticky element ${b.selector} scrolled off-screen instead of pinning — ancestor probably has overflow:hidden or transform.`, evidence: { initialTop: b.initialTop, newTop: Math.round(r.top) } });
    if (style.position === 'fixed' && !stillVisible)
      add({ issueType: 'fixedDetachedOnScroll', severity: 'high', selector: b.selector, bbox: bb(el), description: `position:fixed element ${b.selector} is no longer visible after scroll — likely a transformed ancestor breaking the fixed-positioning context.`, evidence: { initialTop: b.initialTop, newTop: Math.round(r.top) } });
  }

  // ── RESTORE: scroll back + remove tracking attrs ──
  window.scrollTo({ top: origScroll, behavior: 'instant' });
  await sleep(200);
  for (const el of document.querySelectorAll('[data-argus-sticky]')) { try { el.removeAttribute('data-argus-sticky'); } catch (_) {} }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| stickyDetachedOnScroll | high | "position:sticky element {selector} scrolled off-screen instead of pinning — ancestor probably has overflow:hidden or transform" |
| fixedDetachedOnScroll | high | "position:fixed element {selector} is no longer visible after scroll — likely a transformed ancestor breaking the fixed-positioning context" |

## Notes on this conversion
- This replaces the old multi-probe orchestrator flow (capture → scroll MCP → wait → re-measure → restore MCP → cleanup) with ONE in-page async probe. Same checks, same issueTypes — the orchestrator makes a **single** `browser_evaluate` call instead of 6 MCP steps, so the skill is cheap, fast, and cannot be partially skipped (the restore can't be silently dropped).
- Scrolling is done via in-page `window.scrollTo` + an in-page `setTimeout` promise wait — no real browser-level events are needed, so this is fully executable. The probe self-skips when there are no sticky/fixed elements OR when the page is not scrollable.
