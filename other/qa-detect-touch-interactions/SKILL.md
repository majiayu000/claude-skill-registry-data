---
name: qa-detect-touch-interactions
section: responsiveness
description: "Dispatches real TouchEvent (touchstart/touchend) on elements that have hover-only handlers, to detect controls that work with mouse but not with touch. Tests tap, double-tap-to-zoom suppression, swipe gestures. Runs as ONE in-page async probe."
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: false
interactive: true
executable: true
cacheVersion: "1.0.0"
ownership: "exclusive: any bug related to touch-event handling (vs mouse-event handling) belongs to this skill"
requires: [hasDragDrop, hasToggleSwitches, hasRangeSlider]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate find/state/dispatch/recheck MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds up to 8 interactive targets, captures each element's state, dispatches a genuine `TouchEvent` (touchstart/touchend) sequence, waits in-page, re-checks state, then checks viewport-meta/touch-action policy and tests horizontal-scroll containers with a synthetic swipe — returning `findings[]` in one round-trip. It does its own waits via in-page `setTimeout` promises, so there is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when the page has no interactive elements or the browser lacks `TouchEvent`/`Touch` constructors. The probe closes any menus it opened before returning, leaving the page clean for the next skill. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

Run on **mobile/tablet only** (the orchestrator gates `applyOn: [mobile, tablet]`). Never dispatches on submit/delete/logout controls — the probe filters them out.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-touch-interactions' }, o));
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // self-skip if TouchEvent unsupported
  if (typeof window.TouchEvent === 'undefined' || typeof window.Touch === 'undefined') return [];

  const stateOf = el => {
    const adjacent = el.parentElement ? [...el.parentElement.children].filter(c => c !== el) : [];
    const expandedSiblings = adjacent.filter(s => { const r = s.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (s.getAttribute('aria-expanded') === 'true' || /open|active|expanded|show/i.test(s.className)); });
    return JSON.stringify({ ariaExpanded: el.getAttribute('aria-expanded'), classList: el.className, visibleSiblings: expandedSiblings.length, scrollY: window.scrollY });
  };

  const tap = el => {
    const r = el.getBoundingClientRect();
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const t = new Touch({ identifier: 1, target: el, clientX: x, clientY: y, pageX: x, pageY: y, screenX: x, screenY: y, radiusX: 10, radiusY: 10, force: 1 });
    el.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [t], targetTouches: [t], changedTouches: [t] }));
    el.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [t] }));
  };

  // ── find targets (skip dangerous controls) ──
  const targets = [];
  for (const el of document.querySelectorAll('button, a, [role="button"], [onclick], [onmouseover], [data-toggle], summary, label[for]')) {
    if (targets.length >= 8) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const txt = (el.innerText || '').toLowerCase();
    if (el.type === 'submit' || /delete|remove|destroy|logout|sign\s*out|submit|save/i.test(txt)) continue;
    const className = (el.className && typeof el.className === 'string') ? el.className : '';
    const tag = el.tagName;
    // A genuine HOVER-REVEAL behavior means JS hover listeners (onmouseover/onmouseenter) OR a
    // CSS class that names hover. A class merely containing "hover" is weak — require an actual
    // JS hover handler OR a clearly hover-driven menu/dropdown class for it to count as hover-only-suspect.
    const jsHover = !!el.onmouseover || !!el.onmouseenter;
    const hoverClass = /(hover[-_]?(menu|dropdown|reveal|trigger)|dropdown[-_]?hover|menu[-_]?hover)/i.test(className);
    // A CLICK / TOUCH / KEYBOARD equivalent means the control ALSO works without hover:
    //  - real semantic link/button (native activation on tap)
    //  - explicit onclick / [onclick]
    //  - keyboard-activatable (tabindex + role=button/link/menuitem, native interactive el)
    const isRealLinkOrButton = (tag === 'A' && el.hasAttribute('href')) || tag === 'BUTTON' || tag === 'SUMMARY';
    const role = el.getAttribute('role');
    const keyboardActivatable = el.hasAttribute('tabindex') && ['button','link','menuitem','tab'].includes(role || '');
    const hasClickEquivalent = !!el.onclick || el.hasAttribute('onclick') || isRealLinkOrButton || keyboardActivatable;
    targets.push({
      el,
      hasHoverHandler: jsHover || hoverClass,
      hasTouchHandler: !!el.ontouchstart || !!el.ontouchend,
      hasClickEquivalent,
      hasClickHandler: !!el.onclick || el.hasAttribute('onclick') || tag === 'BUTTON' || tag === 'A'
    });
  }
  if (targets.length === 0) return [];

  // ── test each target with a real tap ──
  for (const t of targets) {
    const before = stateOf(t.el);
    tap(t.el);
    await sleep(300);
    const after = stateOf(t.el);
    // hoverOnlyMenu — ONLY a defect when the control reveals on hover AND has NO click/touch/keyboard
    // equivalent. A nav item that opens its submenu on BOTH hover and click is NOT a defect; a real
    // <a href>/<button> activates on tap natively, so "no observed state change" from our heuristic
    // stateOf() is not proof it's dead — require a genuine absence of any touch-reachable path.
    if (t.hasHoverHandler && !t.hasTouchHandler && !t.hasClickEquivalent && after === before)
      add({ issueType: 'hoverOnlyMenu', severity: 'high', selector: sel(t.el), bbox: bb(t.el), description: 'Element reveals on hover but has no click/touch/keyboard equivalent and did not respond to a real touchstart/touchend tap — hover-only, invisible to mobile/touch users.', evidence: { hasHoverHandler: true, hasTouchHandler: false, hasClickEquivalent: false } });
    else if (t.hasClickHandler && !t.hasTouchHandler && after === before)
      add({ issueType: 'touchEventIgnored', severity: 'high', selector: sel(t.el), bbox: bb(t.el), description: 'Element has a click handler but nothing changed on a real touch tap, and touchend did not bubble to click on this app.', evidence: { hasClickHandler: true } });
  }

  // ── viewport meta + touch-action policy ──
  const meta = document.querySelector('meta[name="viewport"]');
  const metaContent = meta ? (meta.getAttribute('content') || '') : '';
  const hasWidthDevice = /width\s*=\s*device-width/.test(metaContent);
  if (!hasWidthDevice)
    add({ issueType: 'tapDelayDetected', severity: 'low', selector: 'meta[name="viewport"]', description: 'No viewport meta with width=device-width — legacy 300ms tap delay likely affects every tap.', evidence: { metaContent } });

  let blockedCount = 0, interactiveSeen = 0;
  for (const el of document.querySelectorAll('button, a, [role="button"]')) {
    interactiveSeen++;
    const s = getComputedStyle(el);
    if (s.touchAction === 'manipulation' || s.touchAction === 'none') blockedCount++;
    if (interactiveSeen > 20) break;
  }
  if (interactiveSeen > 0 && blockedCount === interactiveSeen)
    add({ issueType: 'doubleTapZoomBlocked', severity: 'medium', selector: 'body', description: 'All sampled interactive elements set touch-action: manipulation/none — legitimate double-tap-to-zoom is blocked everywhere.', evidence: { blockedCount, interactiveSeen } });

  // ── horizontal-scroll containers: synthetic swipe ──
  const carousels = [];
  for (const el of document.querySelectorAll('*')) {
    if (carousels.length >= 5) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.width > innerWidth * 0.5) continue;
    const s = getComputedStyle(el);
    if (s.overflowX !== 'scroll' && s.overflowX !== 'auto') continue;
    if (el.scrollWidth <= el.clientWidth + 5) continue;
    carousels.push(el);
  }
  for (const el of carousels) {
    const r = el.getBoundingClientRect();
    const startX = r.left + r.width * 0.8, endX = r.left + r.width * 0.2, y = r.top + r.height / 2;
    const mk = x => new Touch({ identifier: 1, target: el, clientX: x, clientY: y, pageX: x, pageY: y, force: 1 });
    const before = el.scrollLeft;
    el.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [mk(startX)], targetTouches: [mk(startX)], changedTouches: [mk(startX)] }));
    el.dispatchEvent(new TouchEvent('touchmove', { bubbles: true, cancelable: true, touches: [mk((startX + endX) / 2)], targetTouches: [mk((startX + endX) / 2)], changedTouches: [mk((startX + endX) / 2)] }));
    el.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [mk(endX)] }));
    await sleep(200);
    if (el.scrollLeft === before)
      add({ issueType: 'swipeNotHandled', severity: 'medium', selector: sel(el), bbox: bb(el), description: 'Horizontally-overflowing container did not scroll after a synthetic swipe — touch users cannot navigate this carousel/strip.', evidence: { scrollWidth: el.scrollWidth, clientWidth: el.clientWidth } });
  }

  // ── cleanup: close any menus opened during tapping ──
  for (const el of document.querySelectorAll('[aria-expanded="true"]')) { try { el.setAttribute('aria-expanded', 'false'); } catch (_) {} }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| hoverOnlyMenu | high | Menu opens on mouseenter but does NOT open on touchstart — invisible to mobile users |
| touchEventIgnored | high | Button has click handler but no touchend handler, and touchend doesn't bubble to click on this app |
| doubleTapZoomBlocked | medium | Page sets `touch-action: manipulation` everywhere, blocking legitimate double-tap-to-zoom |
| tapDelayDetected | low | App has 300ms tap delay because no `viewport` meta tag with `width=device-width` |
| swipeNotHandled | medium | Element has `overflow-x: scroll` content but no swipe handler — touch users can't navigate carousel |

## Hard rules

1. **Never dispatch on form submit / delete / logout buttons** — the probe filters targets by type/text before tapping.
2. **Mandatory cleanup** — opened menus are closed (`aria-expanded="false"`) before the probe returns.
3. **Mobile/tablet only** — desktop touch testing is theoretical.
4. **300 ms wait between dispatch and recheck** — allows JS handlers to update the DOM.

## Notes on this conversion
- This replaces the old ~30-call flow (find → per-target state/dispatch/wait/recheck → policy → swipe → cleanup) with ONE async `browser_evaluate`. All inter-step waits are now in-page `setTimeout` promises, so there is **no AI reasoning between dispatches**.
- All 5 issueTypes preserved.
- Detection of hover handlers remains HEURISTIC (no way to inspect attached listeners) — false negatives possible, same as before.
- `TouchEvent`/`Touch` constructors are supported in Playwright Chromium/Firefox/WebKit; the probe self-skips if unavailable.
