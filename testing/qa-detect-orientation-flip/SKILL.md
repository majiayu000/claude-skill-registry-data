---
name: qa-detect-orientation-flip
section: responsiveness
description: "Tests TRUE orientation rotation via browser_resize (swap width/height). Detects layout bugs that appear in landscape, state loss across rotation, and missing orientationchange event handling."
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: false
interactive: true
executable: partial
cacheVersion: "1.0.0"
ownership: "exclusive: any bug related to portrait↔landscape rotation belongs to this skill"
---

# qa-detect-orientation-flip — Real Orientation Rotation Testing

Tests orientation rotation by actually swapping viewport width and height mid-cell, not just checking meta tags. Catches the bugs only real users on rotating devices experience.

## How the orchestrator runs this (resize + 2 probe calls)

🚨 **This skill is EXECUTABLE but `partial`:** a TRUE rotation requires a REAL `browser_resize` (swap width/height) that `browser_evaluate` cannot do, and a portrait-vs-landscape comparison spans the resize. So the in-page logic is reduced to TWO probes:
- `probe.portraitSnapshot` (async) — snapshots portrait state, fills a state-loss marker, returns the snapshot to pass back in.
- `probe.landscapeScanAndDiff` (async) — runs in landscape, scans, diffs against the portrait snapshot it receives, clears the marker, and returns `findings[]`.

## What it checks (4 issue types)

| Issue type | Severity | What it catches |
|---|---|---|
| `landscapeOverflow` | high | Layout produces NEW overflow in landscape that didn't exist in portrait |
| `landscapeContentHidden` | high | Primary CTA or critical content drops below the (narrower) viewport in landscape |
| `orientationLosesState` | high | Form data, scroll position, modal state, or session lost after rotation |
| `orientationNoHandler` | low | Page declares orientation-dependent CSS but doesn't listen to `orientationchange`/`resize` events (broken JS on rotation) |

## Self-skip conditions

- Skip if cell.viewportClass is "desktop" (orientation is mobile/tablet concern).
- Skip if `browser_resize` MCP tool unavailable.
- Skip if cell is auth-gated AND session is fragile (first-run setup verification).

## MCP steps (resize only)

**Step 4 (restore) is mandatory — run it even if a probe call errors.**

1. `portrait = browser_evaluate(probe.portraitSnapshot)` — snapshots portrait state + fills the `argusRotate` marker. Save the returned object.
2. Flip to landscape:
   a. `browser_resize({ width: cell.viewport.height, height: cell.viewport.width })` — swap (e.g. 390×844 → 844×390).
   b. `browser_wait_for({ time: 600 })` — allow CSS reflow + orientationchange handlers.
3. `result = browser_evaluate(probe.landscapeScanAndDiff, portrait)` — scans landscape, diffs vs portrait, clears the marker, returns `findings[]`.
4. Restore portrait (MANDATORY):
   a. `browser_resize({ width: cell.viewport.width, height: cell.viewport.height })`.
   b. `browser_wait_for({ time: 500 })`.

Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Probes (browser_evaluate)

```js
// probe.portraitSnapshot — snapshot portrait state + plant the state-loss marker
async () => {
  const sel = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '');
  const snap = { vw: innerWidth, vh: innerHeight, orientation: innerWidth > innerHeight ? 'landscape' : 'portrait', overflowing: [], primaryCTA: null };

  // Overflow elements
  for (const el of document.querySelectorAll('main, section, header, footer, nav, [class*="container"]')) {
    if (snap.overflowing.length >= 12) break;
    const style = getComputedStyle(el);
    if (style.overflowX === 'hidden' || style.overflowX === 'scroll' || style.overflowX === 'auto') continue;
    if (el.scrollWidth > el.clientWidth + 2) snap.overflowing.push(sel(el));
  }

  // Primary CTA position
  const cta = document.querySelector('button[type="submit"], a.cta, .btn-primary, [class*="primary-button"]');
  if (cta) {
    const r = cta.getBoundingClientRect();
    snap.primaryCTA = { selector: sel(cta), top: Math.round(r.top), bottom: Math.round(r.bottom), visible: r.top < innerHeight };
  }

  // Plant state-loss marker into first text input
  const input = document.querySelector('input[type="text"], input[type="email"], textarea');
  if (input) {
    input.value = 'argusRotate' + Date.now();
    input.dispatchEvent(new Event('input', { bubbles: true }));
    snap.formValue = input.value;
    snap.formSelector = input.id ? '#' + input.id : (input.name || sel(input));
  } else {
    snap.formValue = null;
  }

  snap.scroll = { x: window.scrollX, y: window.scrollY };

  // Does the page declare orientation-dependent CSS?
  snap.hasOrientationCSS = false;
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.type === CSSRule.MEDIA_RULE && /orientation/i.test(rule.conditionText)) { snap.hasOrientationCSS = true; break; }
      }
    } catch (_) {}
    if (snap.hasOrientationCSS) break;
  }
  return snap;
}
```

```js
// probe.landscapeScanAndDiff — args: portrait snapshot from probe.portraitSnapshot
async (portrait) => {
  portrait = portrait || {};
  const out = [];
  const sel = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '');
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // Synthesize orientationchange in case browser_resize didn't fire it
  window.dispatchEvent(new Event('orientationchange'));
  window.dispatchEvent(new Event('resize'));
  await new Promise(r => setTimeout(r, 400));

  const vw = innerWidth, vh = innerHeight;
  const portraitOverflow = new Set(portrait.overflowing || []);

  // 1. NEW overflow in landscape not present in portrait
  for (const el of document.querySelectorAll('main, section, header, footer, nav, [class*="container"]')) {
    if (out.length >= 12) break;
    const style = getComputedStyle(el);
    if (style.overflowX === 'hidden' || style.overflowX === 'scroll' || style.overflowX === 'auto') continue;
    if (el.scrollWidth > el.clientWidth + 2) {
      const tag = sel(el);
      if (!portraitOverflow.has(tag)) {
        out.push({ skill: 'qa-detect-orientation-flip', issueType: 'landscapeOverflow', severity: 'high', selector: tag,
          description: `Element ${tag} overflows horizontally in landscape but not in portrait — rotation introduces new overflow (scrollWidth ${el.scrollWidth}px > clientWidth ${el.clientWidth}px).`,
          bbox: bb(el) });
      }
    }
  }

  // 2. Primary CTA dropped below the (shorter) landscape viewport
  const cta = document.querySelector('button[type="submit"], a.cta, .btn-primary, [class*="primary-button"]');
  if (cta && portrait.primaryCTA && portrait.primaryCTA.visible) {
    const r = cta.getBoundingClientRect();
    if (r.top >= vh) {
      out.push({ skill: 'qa-detect-orientation-flip', issueType: 'landscapeContentHidden', severity: 'high', selector: sel(cta),
        description: `Primary CTA ${sel(cta)} was visible in portrait but sits below the landscape viewport (top ${Math.round(r.top)}px ≥ ${vh}px) after rotation.`,
        bbox: bb(cta) });
    }
  }

  // 3. State loss — first form value changed across rotation
  const input = document.querySelector('input[type="text"], input[type="email"], textarea');
  const landscapeFormValue = input ? input.value : null;
  if (portrait.formValue != null && landscapeFormValue !== portrait.formValue) {
    out.push({ skill: 'qa-detect-orientation-flip', issueType: 'orientationLosesState', severity: 'high', selector: portrait.formSelector || (input ? sel(input) : 'form'),
      description: `Form input lost its value across rotation — portrait="${portrait.formValue}" landscape="${landscapeFormValue}". App likely re-mounts components on orientationchange.`,
      bbox: input ? bb(input) : { x: 0, y: 0, w: 0, h: 0 } });
  }

  // 4. Orientation CSS declared but no resize/orientation handler took effect
  if (portrait.hasOrientationCSS) {
    const mq = window.matchMedia('(orientation: landscape)');
    if (!mq.matches && innerWidth > innerHeight) {
      out.push({ skill: 'qa-detect-orientation-flip', issueType: 'orientationNoHandler', severity: 'low', selector: 'html',
        description: `Page declares @media(orientation:…) CSS but matchMedia did not report landscape after rotation — orientation handling may be broken.`,
        bbox: { x: 0, y: 0, w: 120, h: 40 } });
    }
  }

  // Clear the marker so it doesn't persist into the next skill
  if (input && /^argusRotate/.test(input.value || '')) {
    input.value = '';
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }

  return out;
}
```

## Hard rules

1. **Mandatory restore** — viewport returns to portrait before exit (MCP step 4). Next skill expects cell.viewport.
2. **Clear form marker on exit** — `probe.landscapeScanAndDiff` clears the `argusRotate` string; it must not persist.
3. **Skip on desktop cells** — orientation is mobile/tablet only.
4. **600 ms wait after resize** — allows CSS reflow + JS resize handlers to fire.

## Notes on this conversion

- The old 7-probe playbook is folded into TWO async `browser_evaluate` probes: `portraitSnapshot` (snapshot + plant marker) and `landscapeScanAndDiff` (scan + diff + clear). Same 4 issueTypes.
- Marked `executable: partial` because the rotation requires a REAL `browser_resize` (swap width/height) that `browser_evaluate` cannot perform, and the portrait→landscape comparison spans that resize — so two probe calls bracket the single MCP resize.
- `qa-detect-orientation` only checks the meta tag — a different bug class; both should run.
- The `argusRotate` marker is intentional — distinctive so it can be detected and cleared.
