---
name: qa-detect-dropdown-viewport-clip
section: responsiveness
description: "Tests dropdown / tooltip / autocomplete menus: open each, verify the popup is not clipped at the right or bottom edge of the viewport. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasDropdownMenus]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_wait_for` / `browser_press_key` MCP steps. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds dropdown/menu/tooltip triggers near the right or bottom edge of the viewport, clicks each one in-page, waits with an in-page `setTimeout` promise, locates the opened popup (including Angular Material CDK overlays attached to `document.body`), measures whether it is clipped past the viewport edge, then dismisses it — all inside the page, in one round-trip. There is **no AI reasoning between clicks**. It **self-skips** (returns `[]`) when no edge-near triggers exist. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe dismisses every popup it opened (Escape + body click) and removes its tracking attributes before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-dropdown-viewport-clip' }, o));
  const vw = window.innerWidth, vh = window.innerHeight;

  const findPopup = (trigger) => {
    const controls = trigger.getAttribute('aria-controls');
    let popup = controls ? document.getElementById(controls) : null;
    if (!popup) {
      const candidates = document.querySelectorAll(
        '[role="menu"]:not([hidden]), [role="listbox"]:not([hidden]), ' +
        '[role="tooltip"]:not([aria-hidden="true"]), [class*="popover"]:not([aria-hidden="true"]), ' +
        '[class*="dropdown-menu"]:not([hidden]), [data-state="open"], ' +
        '.cdk-overlay-container .mat-select-panel, .cdk-overlay-container .mat-autocomplete-panel, ' +
        '.cdk-overlay-container mat-menu, .cdk-overlay-container [role="listbox"], .cdk-overlay-pane'
      );
      for (const c of candidates) {
        const r = c.getBoundingClientRect();
        const style = getComputedStyle(c);
        if (r.width > 30 && r.height > 20 && style.display !== 'none' && style.visibility !== 'hidden') { popup = c; break; }
      }
    }
    return popup;
  };
  const dismiss = () => {
    try { document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true })); } catch (_) {}
    try { document.body.click(); } catch (_) {}
  };

  // ── find edge-near triggers ──
  const triggers = [];
  const candidates = [...document.querySelectorAll(
    '[aria-haspopup="menu"], [aria-haspopup="listbox"], [aria-haspopup="true"], ' +
    'button[aria-expanded="false"], [data-toggle="dropdown"], [data-toggle="tooltip"], ' +
    '[class*="dropdown-toggle"], [class*="menu-button"], button[data-tooltip], [data-popover]'
  )].filter(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') return false;
    return true;
  });
  for (const el of candidates) {
    if (triggers.length >= 4) break;
    const r = el.getBoundingClientRect();
    const nearRight = r.left > vw * 0.65;
    const nearBottom = r.top > vh * 0.65;
    if (!nearRight && !nearBottom) continue;
    el.setAttribute('data-argus-clip', String(triggers.length));
    triggers.push({ el, edgeKind: nearRight ? 'right' : 'bottom', selector: el.id ? '#' + el.id : `[data-argus-clip="${triggers.length}"]` });
  }

  // ── self-skip if no edge-near triggers ──
  if (triggers.length === 0) return [];

  // ── open each, measure, dismiss ──
  for (const t of triggers.slice(0, 3)) {
    try { t.el.click(); } catch (_) { continue; }
    await sleep(400);
    const popup = findPopup(t.el);
    if (popup) {
      const r = popup.getBoundingClientRect();
      const bbox = { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
      const overhangRight = Math.max(0, Math.round(r.right - vw));
      const overhangBottom = Math.max(0, Math.round(r.bottom - vh));
      if (r.right > vw + 2)
        add({ issueType: 'dropdownClippedRight', severity: 'high', selector: t.selector, bbox, description: `Dropdown/popup opens past the right viewport edge by ${overhangRight}px — options unreadable or unclickable.`, evidence: { overhangRight, vw } });
      if (r.bottom > vh + 2)
        add({ issueType: 'dropdownClippedBottom', severity: 'high', selector: t.selector, bbox, description: `Dropdown/popup opens past the bottom viewport edge by ${overhangBottom}px — options unreadable or unclickable.`, evidence: { overhangBottom, vh } });
    }
    dismiss();
    await sleep(250);
  }

  // ── RESTORE: dismiss anything still open + remove tracking attrs ──
  dismiss();
  for (const el of document.querySelectorAll('[data-argus-clip]')) { try { el.removeAttribute('data-argus-clip'); } catch (_) {} }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| dropdownClippedRight | high | "Dropdown/popup opens past the right viewport edge by {overhangRight}px — options unreadable or unclickable" |
| dropdownClippedBottom | high | "Dropdown/popup opens past the bottom viewport edge by {overhangBottom}px — options unreadable or unclickable" |

## Notes on this conversion
- This replaces the old multi-probe orchestrator flow (findTriggers → per-trigger browser_click + wait + measure + Escape → closeAllPopups) with ONE in-page async probe. Same checks, same issueTypes — the orchestrator makes a **single** `browser_evaluate` call instead of ~12 MCP steps, so the skill is cheap, fast, and cannot be partially skipped.
- Dropdowns are opened via in-page `element.click()` and the popup is located the same way the old `measureOpenedPopup` did (including CDK overlays in `document.body`). No real browser-level events are required, so this is fully executable. Self-skips when there are no triggers within 35% of the right/bottom viewport edges.
