---
name: qa-detect-adaptive-state
section: visual
description: "Simulates adaptive media states (prefers-color-scheme: dark, prefers-reduced-motion: reduce, forced-colors: active, prefers-contrast: more) within a single cell via browser_evaluate + matchMedia event synthesis. Detects bugs in each adaptive state without spawning separate cells."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: true
executable: partial
cacheVersion: "1.0.0"
ownership: "exclusive: any bug specific to dark mode, reduced motion, forced colors, or high contrast adaptive states belongs to this skill"
---

# qa-detect-adaptive-state — Adaptive State Matrix Testing

Tests 4 adaptive states (dark mode, reduced motion, forced colors, high contrast) within a single cell instead of spawning 4× the cells. Uses CSS injection + `matchMedia` event synthesis to flip states, runs probes per state, and restores at end.

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate simulate/snapshot/restore MCP steps per state. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function captures a baseline, then sequentially: injects each adaptive state's CSS approximation (dark, reduced-motion, forced-colors, high-contrast), waits with an in-page `setTimeout` promise so CSS settles, snapshots, compares, and removes the injected style — all inside the page, in one round-trip. There is **no AI reasoning between states**. It **self-skips** (returns `[]`) when the page uses no `prefers-*` CSS rules. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields. The probe removes **all** injected style tags and data attributes before returning (idempotent restore).

### Why `executable: partial`

`browser_evaluate` runs **inside** the page and cannot change the browser's real media-feature emulation. So the four states are approximated with injected CSS + synthetic `matchMedia` `change` events — this catches apps that listen for the media-query change or that key off `color-scheme`, and it deterministically exercises reduced-motion/forced-colors/high-contrast rules. It does **not** flip the OS-level media features themselves.

For a *true* browser-level pass (only if the orchestrator wants maximal fidelity for `prefers-color-scheme` / `forced-colors`), the MCP layer can emulate the feature before calling this probe — see "## MCP steps (optional, true emulation)". The probe works standalone without it.

## What it checks (8 issue types)

### Dark mode (2)
| Issue type | Severity | What it catches |
|---|---|---|
| `darkModeContrastFail` | high | Text contrast drops below WCAG AA in dark mode |
| `darkModeMissingStyles` | medium | Page uses `prefers-color-scheme: dark` query but some elements don't update (mixed light/dark) |

### Reduced motion (2)
| Issue type | Severity | What it catches |
|---|---|---|
| `motionIgnoresReducedPref` | high | Animations still play when prefers-reduced-motion is active |
| `parallaxOnReducedMotion` | medium | Parallax scrolling still active despite preference |

### Forced colors (2)
| Issue type | Severity | What it catches |
|---|---|---|
| `forcedColorsBreaksLayout` | high | Layout breaks in Windows High Contrast Mode (forced-colors: active) |
| `forcedColorsTextInvisible` | high | Text becomes invisible due to color: transparent or background-based text-color |

### High contrast (2)
| Issue type | Severity | What it catches |
|---|---|---|
| `highContrastFocusInvisible` | medium | Focus ring becomes invisible in high-contrast mode |
| `highContrastIconBroken` | medium | Icon (using CSS color or background-image) becomes invisible |

## Self-skip conditions

- Skip if the page has 0 elements using `prefers-*` CSS rules (no adaptive design — nothing to test).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-adaptive-state' }, o));
  const sel = el => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '')).slice(0, 120);
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── self-skip: does the page define any prefers-* media rules? ──
  // Track EACH adaptive feature independently — a page with only
  // prefers-reduced-motion rules must NOT trigger the dark-mode / forced-colors
  // contrast checks (those would synthesize a state the app never actually renders).
  let usesPrefers = false, usesDarkScheme = false, usesForcedColors = false, usesContrast = false;
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.type === CSSRule.MEDIA_RULE) {
          const ct = (rule.conditionText || '');
          if (/prefers-/i.test(ct)) usesPrefers = true;
          if (/prefers-color-scheme\s*:\s*dark/i.test(ct)) usesDarkScheme = true;
          if (/forced-colors\s*:\s*active/i.test(ct)) usesForcedColors = true;
          if (/prefers-contrast/i.test(ct)) usesContrast = true;
        }
      }
    } catch (_) {}
  }
  if (!usesPrefers) return [];

  const parse = c => { const m = (c || '').match(/(\d+(?:\.\d+)?)/g) || []; return m.map(Number).slice(0, 3); };
  const luminance = ([r, g, b]) => { const a = [r, g, b].map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]; };
  const contrast = (color, bg, fontSize, fontWeight) => {
    const L1 = luminance(parse(color)), L2 = luminance(parse(bg));
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const isLargeText = fontSize >= 24 || (fontSize >= 18.66 && parseInt(fontWeight) >= 700);
    return { ratio, aaPass: isLargeText ? ratio >= 3 : ratio >= 4.5 };
  };
  const sampleTexts = () => {
    const res = []; let count = 0;
    for (const el of document.querySelectorAll('p, h1, h2, h3, button, a, span, label')) {
      if (count >= 10) break;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const txt = (el.innerText || '').trim();
      if (txt.length < 3) continue;
      const style = getComputedStyle(el);
      let bgEl = el, bg = 'rgb(255, 255, 255)';
      while (bgEl) { const bs = getComputedStyle(bgEl); if (bs.backgroundColor && bs.backgroundColor !== 'rgba(0, 0, 0, 0)' && bs.backgroundColor !== 'transparent') { bg = bs.backgroundColor; break; } bgEl = bgEl.parentElement; }
      res.push({ el, sel: sel(el), color: style.color, bg, fontSize: parseFloat(style.fontSize), fontWeight: style.fontWeight });
      count++;
    }
    return res;
  };
  const overflowCount = () => {
    let n = 0;
    for (const el of document.querySelectorAll('main, section, header, footer, nav, [class*="container"]')) {
      const s = getComputedStyle(el);
      if (s.overflowX === 'hidden' || s.overflowX === 'scroll' || s.overflowX === 'auto') continue;
      if (el.scrollWidth > el.clientWidth + 2) n++;
    }
    return n;
  };
  const longRunningAnimations = () => {
    const anims = document.getAnimations ? document.getAnimations() : [];
    return anims.filter(a => {
      if (a.playState !== 'running' || !a.effect) return false;
      const dur = a.effect.getTiming ? a.effect.getTiming().duration : 0;
      return typeof dur === 'number' && dur > 10;
    }).length;
  };
  const parallaxCount = () => [...document.querySelectorAll('*')].filter(el => { const s = getComputedStyle(el); return s.backgroundAttachment === 'fixed' || (s.transform !== 'none' && /translate3d|translateZ/.test(s.transform)); }).length;
  const injectStyle = (id, css) => { if (document.getElementById(id)) return; const s = document.createElement('style'); s.id = id; s.textContent = css; document.head.appendChild(s); };
  const removeStyle = id => { const s = document.getElementById(id); if (s) s.remove(); };
  const dispatchMQ = q => { try { const mq = window.matchMedia(q); mq.dispatchEvent(new MediaQueryListEvent('change', { matches: true, media: q })); } catch (_) {} };

  // ── baseline ──
  const baseOverflow = overflowCount();

  // ── (1) DARK MODE ──
  // GATE: only test dark-mode contrast if the app ACTUALLY implements dark mode via
  // `@media (prefers-color-scheme: dark)`. If it does not, flipping the media query
  // synthesizes a state the user never sees — flagging its contrast is a false positive
  // (we'd just be re-measuring the real LIGHT theme and mislabeling it "dark mode").
  if (usesDarkScheme) {
    // Capture the REAL colors before flipping, so we can verify the flip actually changed them.
    const beforeSamples = sampleTexts().map(t => ({ key: t.sel, color: t.color, bg: t.bg }));
    document.documentElement.setAttribute('data-theme', 'dark');
    document.documentElement.setAttribute('data-argus-dark', '1');
    // Use a real prefers-color-scheme emulation hook (color-scheme on root) AND dispatch the MQ
    // so apps that key off either path respond. We still verify a color actually changed below.
    injectStyle('argus-dark-mode', ':root { color-scheme: dark; }');
    dispatchMQ('(prefers-color-scheme: dark)');
    await sleep(500);
    let anyColorChanged = false;
    const afterSamples = sampleTexts();
    for (const t of afterSamples) {
      const prev = beforeSamples.find(b => b.key === t.sel);
      if (prev && (prev.color !== t.color || prev.bg !== t.bg)) { anyColorChanged = true; break; }
    }
    // Only flag contrast failures if the app genuinely re-themed (colors changed). If nothing
    // changed, the app's dark-mode rules didn't apply to these elements — measuring the unchanged
    // light colors and calling them a "dark mode" failure would be a false positive.
    if (anyColorChanged) {
      for (const t of afterSamples) {
        const prev = beforeSamples.find(b => b.key === t.sel);
        // Skip elements whose colors did NOT change — they're still showing the light theme.
        if (prev && prev.color === t.color && prev.bg === t.bg) continue;
        // Skip when bg couldn't be resolved (fell back to white) AND fg is also white — artifact.
        const cc = parse(t.color), bgc = parse(t.bg);
        if (cc.length === 3 && bgc.length === 3 && cc[0] === bgc[0] && cc[1] === bgc[1] && cc[2] === bgc[2]) continue;
        const c = contrast(t.color, t.bg, t.fontSize, t.fontWeight);
        if (!c.aaPass)
          add({ issueType: 'darkModeContrastFail', severity: 'high', selector: t.sel, bbox: bb(t.el), description: `Text contrast ${Math.round(c.ratio * 100) / 100}:1 fails WCAG AA in dark mode.`, evidence: { ratio: Math.round(c.ratio * 100) / 100, color: t.color, bg: t.bg } });
      }
    }
    document.documentElement.removeAttribute('data-theme');
    document.documentElement.removeAttribute('data-argus-dark');
    removeStyle('argus-dark-mode');
  }

  // ── (2) REDUCED MOTION ──
  injectStyle('argus-reduced-motion', '*, *::before, *::after { animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; transition-duration: 0.001ms !important; scroll-behavior: auto !important; }');
  dispatchMQ('(prefers-reduced-motion: reduce)');
  await sleep(300);
  const stillAnimating = longRunningAnimations();
  const stillParallax = parallaxCount();
  if (stillAnimating > 0)
    add({ issueType: 'motionIgnoresReducedPref', severity: 'high', selector: 'document', description: `${stillAnimating} animation(s) still running despite prefers-reduced-motion: reduce — JS-driven animations ignore the preference.`, evidence: { animationCount: stillAnimating } });
  if (stillParallax > 0)
    add({ issueType: 'parallaxOnReducedMotion', severity: 'medium', selector: 'document', description: `${Math.min(stillParallax, 10)} parallax/transform element(s) still active despite prefers-reduced-motion: reduce.`, evidence: { parallaxCount: Math.min(stillParallax, 10) } });
  removeStyle('argus-reduced-motion');

  // ── (3) FORCED COLORS ──
  injectStyle('argus-forced-colors', '* { background-image: none !important; box-shadow: none !important; } *:focus { outline: 2px solid ButtonText !important; } img, svg { opacity: 1 !important; }');
  await sleep(500);
  if (overflowCount() > baseOverflow)
    add({ issueType: 'forcedColorsBreaksLayout', severity: 'high', selector: 'document', description: `Layout overflow appears under forced-colors (Windows High Contrast Mode) that was not present normally (${baseOverflow} → ${overflowCount()} overflowing containers).`, evidence: { baseOverflow, forcedOverflow: overflowCount() } });
  // `forcedColorsTextInvisible` only makes sense as a REAL defect when the element genuinely
  // renders text-color === its OWN explicitly-set background (e.g. background-clip:text, or a
  // color that collapses to the bg). The previous logic compared color to a bg that FELL BACK to
  // white when no solid ancestor bg existed — so any white text over an image/gradient/transparent
  // surface read as "white === white" and was falsely flagged. Require the element's OWN computed
  // backgroundColor to be a solid color equal to its text color (a true self-coloured invisible
  // element), not the walked-up fallback. This is the only state that stays invisible under
  // forced-colors, since forced-colors overrides bg but background-clip:text / same-color text
  // still collapse.
  for (const t of sampleTexts()) {
    const ownStyle = getComputedStyle(t.el);
    const ownBg = ownStyle.backgroundColor;
    // skip if the element has no solid own background (transparent / image-backed) — indeterminate.
    if (!ownBg || ownBg === 'rgba(0, 0, 0, 0)' || ownBg === 'transparent') continue;
    const cc = parse(t.color), bgc = parse(ownBg);
    if (cc.length === 3 && bgc.length === 3 && cc[0] === bgc[0] && cc[1] === bgc[1] && cc[2] === bgc[2])
      add({ issueType: 'forcedColorsTextInvisible', severity: 'high', selector: t.sel, bbox: bb(t.el), description: 'Text color equals its own background under forced-colors — text becomes invisible.', evidence: { color: t.color, bg: ownBg } });
  }
  removeStyle('argus-forced-colors');

  // ── (4) HIGH CONTRAST ──
  injectStyle('argus-high-contrast', '* { filter: contrast(200%) !important; } *:focus { outline: 3px solid #ff0 !important; outline-offset: 2px !important; }');
  await sleep(500);
  // focus ring visibility: focus a focusable element and check outline
  const focusable = [...document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]')].find(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled; });
  if (focusable) {
    try { focusable.focus(); } catch (_) {}
    await sleep(100);
    const fs = getComputedStyle(focusable);
    const outlineW = parseFloat(fs.outlineWidth) || 0;
    const noRing = (fs.outlineStyle === 'none' || outlineW < 1) && (parseFloat(fs.boxShadow) ? false : fs.boxShadow === 'none');
    if (noRing)
      add({ issueType: 'highContrastFocusInvisible', severity: 'medium', selector: sel(focusable), bbox: bb(focusable), description: 'Focus indicator is not visible in high-contrast mode (no outline and no box-shadow on the focused element).', evidence: { outlineStyle: fs.outlineStyle, outlineWidth: fs.outlineWidth } });
    try { focusable.blur(); } catch (_) {}
  }
  // icon broken: icon-ish elements that became transparent
  for (const ic of [...document.querySelectorAll('[class*="icon"], i, svg')].slice(0, 20)) {
    const r = ic.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const ics = getComputedStyle(ic);
    if ((ics.color === 'rgba(0, 0, 0, 0)' || ics.color === 'transparent') && (ics.backgroundImage === 'none')) {
      add({ issueType: 'highContrastIconBroken', severity: 'medium', selector: sel(ic), bbox: bb(ic), description: 'Icon relies on a CSS color/background-image that becomes invisible in high-contrast mode.', evidence: { color: ics.color } });
      break;
    }
  }
  removeStyle('argus-high-contrast');

  // ── FINAL RESTORE (idempotent) ──
  document.documentElement.removeAttribute('data-theme');
  document.documentElement.removeAttribute('data-argus-dark');
  for (const id of ['argus-dark-mode', 'argus-reduced-motion', 'argus-forced-colors', 'argus-high-contrast']) removeStyle(id);

  return out;
}
```

## MCP steps (optional, true emulation)

The probe above approximates each state with injected CSS and works standalone. If the orchestrator wants real browser-level media emulation for `prefers-color-scheme` / `forced-colors` (higher fidelity for the dark-mode + forced-colors checks), wrap the single `browser_evaluate` call like this — otherwise skip this section entirely:

```
1. (optional) emulate prefers-color-scheme: dark at the browser level, then re-run only the dark-mode portion
2. browser_evaluate(<the probe above>)   // runs all 4 states with CSS approximation
3. (optional) clear any browser-level emulation
```

This is **not required**; the probe self-contains its own simulation and restore. The `partial` marker reflects only that true OS-level media-feature flipping is outside `browser_evaluate`'s reach.

## Hard rules

1. **Mandatory final restore** — page returns to normal state before exit (the probe removes all injected style tags + data attributes; idempotent).
2. **NEVER persist matchMedia override** — synthetic events only fire while active; on resize/navigation the browser resets.
3. **500 ms wait per state** — allow CSS transitions to settle before snapshot.

## Notes on this conversion
- This replaces the old 6-step orchestrator flow (baseline → per-state simulate/wait/snapshot/compare/restore → final cleanup, ~14 MCP calls) with ONE in-page async probe that runs all 4 states, does the WCAG contrast math in-page, and self-restores. Same 8 issueTypes preserved.
- Marked `executable: partial` (not `true`) because `browser_evaluate` cannot flip real OS media features — the four states are CSS/matchMedia approximations (as the original probes already were). The optional MCP-emulation wrapper is the only part that needs browser-level calls, and it is not required for the probe to run.
- Existing shallower skills (`qa-detect-dark-mode`, `qa-detect-reduced-motion`, `qa-detect-forced-colors`) are not deprecated — they check for CSS-rule presence; this skill flips state and tests behavior.
