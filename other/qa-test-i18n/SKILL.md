---
name: qa-test-i18n
section: interactive
description: "Tests language switcher effect and checks for untranslated key strings. Runs as ONE in-page async probe (no AI hand-driving) — finds a switcher, captures baseline text, switches locale, compares. Self-skips when no switcher is present."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasLanguageSwitcher, hasRTL, hasI18nAttributes]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it click-by-click with separate `browser_click` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds the language switcher, captures a baseline of visible text, opens the switcher, picks the first non-active option, drives it (native `<select>` change, real `click()` on option items, or expand-then-click for dropdown menus), waits for change detection via in-page `setTimeout` promises, then compares before/after text and scans for untranslated key strings — all inside the page, in one round-trip. There is **no AI reasoning between clicks**. It **self-skips** (returns `[]`) when no language switcher is present. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the original language (re-selects the original option) before returning where possible.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-i18n' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const snapshotText = () => [...document.querySelectorAll('h1, h2, nav, main p, button, label')].map(e => (e.innerText || '').replace(/\s+/g, ' ').trim()).filter(Boolean).join(' ').slice(0, 500);

  // ── find a language switcher ──
  const langRe = /^(en|fr|de|es|zh|ja|pt|it|nl|ru|ar|hi|ko|english|français|francais|deutsch|español|espanol|中文|日本語)$/i;
  // 1) native <select> for language
  const langSelect = [...document.querySelectorAll('select')].find(s => vis(s) && (/lang|locale/i.test((s.getAttribute('name') || '') + ' ' + (s.getAttribute('aria-label') || '') + ' ' + (s.id || '')) || [...s.options].filter(o => langRe.test((o.textContent || '').trim())).length >= 2));
  // 2) explicit switcher container / control
  const switcherCtrl = [...document.querySelectorAll('[aria-label*="language" i], [data-testid*="lang"], .language-switcher, [class*="locale-switcher"], [class*="lang-switch"]')].find(vis)
    || [...document.querySelectorAll('button, a')].find(el => vis(el) && langRe.test((el.textContent || '').trim()));

  if (!langSelect && !switcherCtrl) return []; // self-skip — no language switcher

  const before = snapshotText();

  // ── drive the switch ──
  let switched = false;
  if (langSelect && langSelect.options.length >= 2) {
    const cur = langSelect.value;
    const alt = [...langSelect.options].find(o => o.value !== cur && !o.disabled);
    if (alt) {
      langSelect.value = alt.value;
      langSelect.dispatchEvent(new Event('change', { bubbles: true }));
      switched = true;
      await sleep(900);
    }
  } else if (switcherCtrl) {
    // open the switcher (it may be a dropdown trigger)
    switcherCtrl.click();
    await sleep(400);
    const option = [...document.querySelectorAll('option:not([selected]), .language-option:not(.active), [role="option"]:not([aria-selected="true"]), [role="menuitem"], [class*="lang"] a, [class*="locale"] li')]
      .find(o => vis(o) && langRe.test((o.textContent || '').trim()) && (o.textContent || '').trim().toLowerCase() !== (switcherCtrl.textContent || '').trim().toLowerCase());
    if (option) { option.click(); switched = true; await sleep(900); }
  }

  if (switched) {
    const after = snapshotText();
    if (before.length > 20 && before === after)
      add({ issueType: 'languageSwitchNoEffect', severity: 'medium', selector: sel(langSelect || switcherCtrl), bbox: bb(langSelect || switcherCtrl), description: 'Switching language did not change any visible UI text — language switcher has no effect.', evidence: { sample: before.slice(0, 120) } });

    // ── untranslated keys (only meaningful after a switch) ──
    const body = document.body.innerText || '';
    const keyMatches = (body.match(/\b[a-z][a-z0-9_]*\.[a-z][a-z0-9_.]{3,}\b/g) || [])
      .concat(body.match(/\{\{[^}]+\}\}/g) || [])
      .filter(m => !/https?:|\.(px|em|rem|vh|vw|com|net|org|io|html|js|css|png|jpg|svg)\b/i.test(m));
    const uniq = [...new Set(keyMatches)];
    if (uniq.length > 3)
      add({ issueType: 'untranslatedKeys', severity: 'medium', selector: 'body', bbox: bb(document.body), description: `After language switch, ${uniq.length} untranslated key strings visible: ${uniq.slice(0, 5).join(', ')}`, evidence: { count: uniq.length, examples: uniq.slice(0, 5) } });

    // ── restore original language (best-effort) ──
    if (langSelect) {
      try { langSelect.value = langSelect.options[0].value; langSelect.dispatchEvent(new Event('change', { bubbles: true })); await sleep(400); } catch (_) {}
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| languageSwitchNoEffect | medium | "Switching language did not change any visible UI text — language switcher has no effect" |
| untranslatedKeys | medium | "After language switch, {n} untranslated key strings visible: {examples}" |

## Notes on this conversion
- Fully in-page (`executable: true`). The old prose playbook (find switcher → click → wait `domcontentloaded` → compare) is now ONE async probe. Same checks, same issueTypes — single `browser_evaluate` call instead of multiple AI-driven MCP steps.
- Self-skips (returns `[]`) when no language switcher exists, so it costs nothing on the vast majority of pages.
- If a particular app routes the locale change through a full page navigation that `click()` cannot trigger in-page, the switch simply registers as "no in-page effect"; the probe is conservative and only flags `languageSwitchNoEffect` when baseline text was non-trivial (>20 chars) and identical after the switch.
