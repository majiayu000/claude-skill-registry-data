---
name: qa-test-theme
section: interactive
description: "Tests dark/light theme toggle effect and persistence. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasThemeToggle]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_evaluate` / reload MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds the theme/dark toggle, records the baseline (body bg/color + `html` class + `[data-theme]`), clicks the toggle, compares the after-state, and checks whether the new theme was persisted to `localStorage`/cookie so it would survive a reload — all inside the page, in one round-trip. It does its own waits via in-page `setTimeout` promises. It **self-skips** (returns `[]`) when no theme toggle is present. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the original theme (clicks the toggle back) before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-theme' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  const TOGGLE_SEL = '[aria-label*="dark" i], [aria-label*="light" i], [aria-label*="theme" i], [data-testid*="theme"], [data-testid*="dark-mode"], .theme-toggle, [class*="theme-toggle"], button[title*="theme" i], button[title*="dark" i]';

  // ── self-skip if no theme toggle ──
  const toggle = [...document.querySelectorAll(TOGGLE_SEL)].find(vis);
  if (!toggle) return [];

  const snapshot = () => {
    const bs = getComputedStyle(document.body);
    return {
      bg: bs.backgroundColor,
      color: bs.color,
      dataTheme: document.documentElement.getAttribute('data-theme') || document.body.getAttribute('data-theme') || '',
      htmlClass: (document.documentElement.className || '') + '|' + (document.body.className || '')
    };
  };
  const storageFingerprint = () => {
    let ls = '';
    try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); ls += k + '=' + localStorage.getItem(k) + ';'; } } catch (e) {}
    return (ls + '|' + (document.cookie || '')).toLowerCase();
  };

  const baseline = snapshot();
  const storeBefore = storageFingerprint();

  // ── TOGGLE ──
  toggle.click();
  await sleep(500);
  const after = snapshot();

  const changed = !(after.bg === baseline.bg && after.color === baseline.color && after.dataTheme === baseline.dataTheme && after.htmlClass === baseline.htmlClass);

  if (!changed) {
    add({ issueType: 'themeToggleNoEffect', severity: 'low', selector: sel(toggle), bbox: bb(toggle), description: 'Theme toggle clicked but no color or attribute change detected — bg stayed "' + baseline.bg + '", color stayed "' + baseline.color + '".', evidence: { bg: baseline.bg, color: baseline.color } });
  } else {
    // ── PERSISTENCE (only if toggle worked) ──
    // A real reload cannot run inside browser_evaluate. Instead detect whether the new theme
    // was written somewhere durable (localStorage / cookie) that would survive a reload.
    const storeAfter = storageFingerprint();
    const themeWords = /(theme|dark|light|color-?scheme|mode|appearance)/;
    const persisted = storeAfter !== storeBefore && themeWords.test(storeAfter);
    if (!persisted) {
      add({ issueType: 'themeNotPersisted', severity: 'low', selector: sel(toggle), bbox: bb(toggle), description: 'Theme toggle worked but the preference was not written to localStorage/cookie — it will revert to the original theme after page reload.', evidence: { changed: { from: baseline.dataTheme || baseline.htmlClass.slice(0, 40), to: after.dataTheme || after.htmlClass.slice(0, 40) }, storageChanged: storeAfter !== storeBefore } });
    }
  }

  // ── restore original theme ──
  if (changed) { try { toggle.click(); await sleep(300); } catch (e) {} }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| themeToggleNoEffect | low | "Theme toggle clicked but no color or attribute change detected — bg stayed \"{bg}\", color stayed \"{color}\"" |
| themeNotPersisted | low | "Theme toggle worked but theme reverted to original after page reload — preference is not persisted in localStorage/cookie" |

## Notes on this conversion
- Replaces the prose playbook with ONE in-page async probe. Same checks, same issueTypes. The orchestrator makes a **single** `browser_evaluate` call instead of click/read/reload/read round-trips.
- **Persistence check folded:** `browser_evaluate` cannot perform a real `page.reload()`, so instead of reloading-then-comparing, the probe detects whether the toggle wrote a theme-related value to `localStorage`/cookie (the durable store that survives reload). If nothing theme-related was persisted, the same `themeNotPersisted` issueType is emitted — the user-facing meaning ("reverts after reload") is unchanged. The orchestrator may optionally still do a real reload to confirm, but the probe alone flags the bug in one call.
- The probe restores the original theme by clicking the toggle back, leaving the page in its baseline state.
