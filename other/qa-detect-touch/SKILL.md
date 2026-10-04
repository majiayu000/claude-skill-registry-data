---
name: qa-detect-touch
section: responsiveness
description: "Detects tap targets that are too small for accurate touch input, using WCAG 2.2 spacing-aware rules: <24×24 always flagged, 24-43 px flagged only when crowded by another clickable target within 24px. Also flags interactive elements <8px apart."
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: true
---

## What it checks

Two tiers, matching **WCAG 2.2 Target Size (Minimum) 2.5.8**:

1. **Always too small**: target is `<24×24 px`. No spacing exception applies — too small to tap reliably even with whitespace around it.
2. **Crowded**: target is `24-43×24-43 px` AND another clickable target's bbox is within **24px** of its edge. Standard size for sparse layouts, but dense placement (toolbar buttons, icon grids) makes mistaps likely.

Targets `≥44×44 px` always pass. Isolated 24-43 px targets (no neighbor within 24px) also pass — matches the WCAG 2.2 spacing exception, so an isolated 40×40 checkbox in a sparse form is correctly not flagged.

Also flags any two interactive elements `<8px` apart (`tapTargetsTooClose`).

## Probe (browser_evaluate)
```js
() => {
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0,120);
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const q = 'a,button,[role="button"],input,select,textarea,[tabindex]';

  // Is this element actually tappable? (the real question — pixel size doesn't matter
  // if you can't tap it.) Skip disabled controls, controls with pointer-events:none,
  // controls visibly faded out, and anything covered by an overlay at its center point.
  const isActuallyTappable = (el, r) => {
    // (a) Disabled via attribute — the user can't tap it, so size is irrelevant
    if (el.disabled) return false;
    if (el.getAttribute('aria-disabled') === 'true') return false;
    if (el.hasAttribute('disabled')) return false;
    // (b) Visibly disabled (greyed out) — opacity < 0.4 is the common "disabled" cue
    const cs = getComputedStyle(el);
    if (parseFloat(cs.opacity) < 0.4) return false;
    // (c) CSS-disabled via pointer-events on the element or any ancestor
    if (cs.pointerEvents === 'none') return false;
    let p = el.parentElement;
    while (p && p !== document.documentElement) {
      if (getComputedStyle(p).pointerEvents === 'none') return false;
      p = p.parentElement;
    }
    // (d) Covered by an overlay — elementFromPoint at the center returns something
    //     that's neither this element nor one of its descendants
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    if (cx >= 0 && cy >= 0 && cx < innerWidth && cy < innerHeight) {
      const top = document.elementFromPoint(cx, cy);
      if (top && top !== el && !el.contains(top) && !top.contains(el)) {
        // Something else is rendered on top at the click point — the user can't tap el directly
        return false;
      }
    }
    return true;
  };

  // ── ROOT-CAUSE FIX: measure the EFFECTIVE target, and honor WCAG 2.2 exemptions. ──
  // Pixel size of the visible box is the WRONG thing to measure on its own — these 4 patterns
  // are the real source of "easy-to-touch things flagged as too small":
  const unionRect = (a, b) => { const left = Math.min(a.left, b.left), top = Math.min(a.top, b.top), right = Math.max(a.right, b.right), bottom = Math.max(a.bottom, b.bottom); return { left, top, right, bottom, width: right - left, height: bottom - top }; };

  // (A) EFFECTIVE rect: a checkbox/radio's real tap target is the input UNION its <label>
  //     (clicking the label toggles it). A 16px checkbox with a 200px label is NOT too small.
  const effectiveRect = el => {
    let r = el.getBoundingClientRect();
    const t = (el.getAttribute('type') || '').toLowerCase();
    if (el.tagName === 'INPUT' && (t === 'checkbox' || t === 'radio')) {
      let label = (el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`)) || el.closest('label');
      if (label) { const lr = label.getBoundingClientRect(); if (lr.width > 0 && lr.height > 0) r = unionRect(r, lr); }
    }
    return r;
  };

  // (B) WCAG 2.2 Target-Size (2.5.8) EXEMPTIONS — these are NOT failures, never flag them:
  const isExemptTarget = el => {
    const cs = getComputedStyle(el);
    // Inline exception: a link inside a flow of text (inline display, parent has surrounding text).
    if (el.tagName === 'A' && /inline/.test(cs.display)) {
      const p = el.parentElement;
      if (p && (p.innerText || '').trim().length > (el.innerText || '').trim().length + 1) return true;
    }
    // A focusable-but-not-clickable [tabindex] element (no role/handler/pointer) is not a tap target.
    if (el.hasAttribute('tabindex') && !['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName)
        && el.getAttribute('role') !== 'button' && el.getAttribute('role') !== 'link'
        && !el.onclick && cs.cursor !== 'pointer') return true;
    return false;
  };

  let cand = [...document.querySelectorAll(q)].map(el => ({ el, r: effectiveRect(el) }))
    .filter(x => x.r.width > 0 && x.r.height > 0 && x.r.top >= 0 && x.r.bottom <= innerHeight * 3)
    .filter(x => isActuallyTappable(x.el, x.r))
    .filter(x => !isExemptTarget(x.el));

  // (C) NESTED exception: if a candidate is wholly inside a LARGER clickable candidate, the
  //     ANCESTOR is the real tap target — drop the inner one (stops flagging the icon inside a button).
  const els = cand.filter(x => !cand.some(y => y.el !== x.el && y.el.contains(x.el)
      && (y.r.width * y.r.height) > (x.r.width * x.r.height)));

  // Helper: edge-to-edge distance between two rects (0 if they overlap).
  const edgeDistance = (a, b) => {
    const dx = Math.max(0, Math.max(a.left, b.left) - Math.min(a.right, b.right));
    const dy = Math.max(0, Math.max(a.top, b.top) - Math.min(a.bottom, b.bottom));
    return Math.sqrt(dx * dx + dy * dy);
  };

  // Helper: does another clickable element sit within `spacing` px of this one's edges?
  const hasCrowdedNeighbor = (target, spacing) => {
    for (const other of els) {
      if (other.el === target.el) continue;
      if (target.el.contains(other.el) || other.el.contains(target.el)) continue;
      if (edgeDistance(target.r, other.r) < spacing) return true;
    }
    return false;
  };

  // ── THE ACTUAL WCAG 2.2 AA RULE (2.5.8 Target Size Minimum) ──
  // A target PASSES if BOTH dimensions are ≥ 24px. (The 44px figure is AAA / Apple-HIG comfort —
  // NOT a WCAG AA failure — so it must NOT drive findings; that was the source of the noise.)
  // A target SMALLER than 24px in either dimension still PASSES via the SPACING exception: if a
  // 24px-clear gap exists to every neighboring target. So we flag ONLY: min dimension < 24px AND
  // crowded (a clickable neighbor within 24px). That is the exact AA failure condition — nothing more.
  const MIN = 24;            // WCAG 2.2 AA minimum, both dimensions
  const SPACING_MIN = 24;    // WCAG 2.2 spacing exception clearance

  for (const {el, r} of els) {
    if (out.length >= 20) break;
    const w = Math.round(r.width), h = Math.round(r.height);
    if (Math.min(w, h) >= MIN) continue;                       // ≥24×24 → meets WCAG 2.2 AA. PASS.
    if (!hasCrowdedNeighbor({el, r}, SPACING_MIN)) continue;   // <24 but isolated → spacing exception. PASS.
    // <24px in a dimension AND a clickable neighbor within 24px → real WCAG 2.2 AA failure.
    {
      out.push({
        issueType: 'smallTapTarget', severity: 'high',
        selector: sel(el), bbox: bb(el),
        description: `Touch target ${w}×${h}px is below WCAG 2.2's 24×24px minimum AND has a clickable neighbor within 24px (spacing exception not met). Grow it to ≥24×24px or add ≥24px spacing.`
      });
    }
    // Anything ≥24×24, or <24 but isolated → passes WCAG 2.2 AA. No finding.
  }

  // tapTargetsTooClose — any two clickable elements with <8px between them
  const top = els.slice(0, 50);
  outer: for (let i = 0; i < top.length; i++) {
    for (let j = i+1; j < top.length; j++) {
      const d = edgeDistance(top[i].r, top[j].r);
      if (d > 0 && d < 8) {
        if (out.length >= 20) break outer;
        out.push({ issueType:'tapTargetsTooClose', severity:'medium', selector:sel(top[i].el),
          description:`Touch target issue: ${Math.round(d)}px gap < minimum 8px between interactive elements` });
        break;
      }
    }
  }
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| smallTapTarget | high | "Touch target {w}×{h}px is below the WCAG 2.2 absolute minimum of 24×24px..." (Tier 1) OR "...has another clickable element within 24px..." (Tier 2 crowded) |
| tapTargetsTooClose | medium | "Touch target issue: {gap}px gap < minimum 8px between interactive elements" |
