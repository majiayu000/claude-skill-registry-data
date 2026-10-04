---
name: qa-detect-modal-viewport-fit
section: responsiveness
description: "Tests open modals / dialogs: verify they fit within the viewport height, action buttons (Submit/Cancel) are reachable, and content scrolls internally rather than the modal overflowing. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasModals, hasDrawer]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_wait_for` / `browser_press_key` MCP steps. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function detects an already-open modal OR finds a modal trigger and clicks it in-page (waiting with an in-page `setTimeout` promise), measures whether the modal fits the viewport height, whether its action footer is reachable, and whether content overflows — then, if it opened the modal itself, dismisses it — all inside the page, in one round-trip. There is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when no modal is open and no trigger can be found. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe dismisses any modal it opened (Escape + body click) and removes its tracking attributes before returning. A modal that was already open on arrival is left open (it is the cell's state, not ours to close).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-modal-viewport-fit' }, o));

  const detectOpenModal = () => {
    const candidates = document.querySelectorAll(
      '[role="dialog"][aria-modal="true"]:not([aria-hidden="true"]), ' +
      '[role="alertdialog"]:not([aria-hidden="true"]), .modal.show, .modal[class*="open"], ' +
      '[data-state="open"][role="dialog"], mat-dialog-container, ' +
      '.cdk-overlay-container [role="dialog"]:not([aria-hidden="true"]), .cdk-overlay-pane mat-dialog-container'
    );
    for (const c of candidates) {
      const r = c.getBoundingClientRect();
      const style = getComputedStyle(c);
      if (r.width > 100 && r.height > 100 && style.display !== 'none' && style.visibility !== 'hidden') return c;
    }
    return null;
  };
  const findTrigger = () => {
    const buttons = [...document.querySelectorAll('button, [role="button"], a[role="button"]')]
      .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled; });
    for (const b of buttons) {
      if (b.hasAttribute('data-modal-trigger') || b.hasAttribute('data-dialog-trigger')) return b;
      const ac = b.getAttribute('aria-controls') || '';
      if (ac && /modal|dialog/i.test(ac)) return b;
      const txt = (b.innerText || '').trim().toLowerCase();
      if (/^(open|view|details|edit|settings|preferences|new|add)$/i.test(txt) && b.offsetWidth > 0) return b;
    }
    return null;
  };
  const dismiss = () => {
    try { document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true })); } catch (_) {}
    try { document.body.click(); } catch (_) {}
  };

  // ── obtain a modal: already-open, else open one ──
  let modal = detectOpenModal();
  let openedHere = false;
  if (!modal) {
    const trigger = findTrigger();
    if (!trigger) return []; // self-skip
    try { trigger.click(); } catch (_) { return []; }
    await sleep(500);
    modal = detectOpenModal();
    if (!modal) return []; // gave up — self-skip
    openedHere = true;
  }

  // ── measure fit ──
  const r = modal.getBoundingClientRect();
  const vh = window.innerHeight, vw = window.innerWidth;
  const modalSel = modal.id ? '#' + modal.id : (modal.tagName.toLowerCase() + (/dialog/i.test(modal.getAttribute('role') || '') ? '[role="dialog"]' : ''));
  const bbox = { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };

  const innerScrollers = [...modal.querySelectorAll('*')].filter(el => {
    const s = getComputedStyle(el);
    return (s.overflowY === 'auto' || s.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
  });
  const hasInternalScroll = innerScrollers.length > 0;
  const tooTall = r.height > vh + 4;

  const footer = modal.querySelector(
    'mat-dialog-actions, .modal-footer, [class*="modal-footer"], [class*="dialog-footer"], ' +
    '[class*="actions"]:last-child, [class*="buttons"]:last-child, .cdk-overlay-pane mat-dialog-actions'
  );
  let footerOffscreen = false;
  if (footer) { const fr = footer.getBoundingClientRect(); footerOffscreen = fr.bottom > vh + 2 || fr.top > vh; }

  const modalStyle = getComputedStyle(modal);
  const minWidth = parseFloat(modalStyle.minWidth) || 0;
  const modalTooWideForViewport = minWidth > vw * 0.95 && vw < 480;

  let contentOverflowsModal = false;
  const modalBody = modal.querySelector('[class*="modal-body"],[class*="dialog-body"],[class*="modal-content"] > div, [class*="dialog-content"] > div');
  if (modalBody && modalBody.scrollWidth > modalBody.clientWidth + 10) contentOverflowsModal = true;

  if (tooTall && !hasInternalScroll)
    add({ issueType: 'modalTooTallNoScroll', severity: 'high', selector: modalSel, bbox, description: `Modal height ${Math.round(r.height)}px exceeds viewport ${vh}px and has no internal scroll — content below the fold is unreachable.`, evidence: { modalHeight: Math.round(r.height), vh } });
  if (footerOffscreen)
    add({ issueType: 'modalFooterUnreachable', severity: 'high', selector: modalSel, bbox, description: 'Modal action footer (Submit/Cancel buttons) is below the viewport — users cannot click them without scrolling outside the modal.', evidence: { vh } });
  if (modalTooWideForViewport)
    add({ issueType: 'modalTooWideForViewport', severity: 'medium', selector: modalSel, bbox, description: `Modal has min-width:${minWidth}px which exceeds viewport width ${vw}px — content will overflow or be clipped on mobile.`, evidence: { minWidth, vw } });
  if (contentOverflowsModal)
    add({ issueType: 'modalContentOverflows', severity: 'medium', selector: modalSel, bbox, description: 'Modal body content overflows its container — internal content has fixed width wider than the modal itself.', evidence: {} });

  // ── RESTORE: dismiss only if WE opened it ──
  if (openedHere) { dismiss(); await sleep(300); }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| modalTooTallNoScroll | high | "Modal height {h}px exceeds viewport {vh}px and has no internal scroll — content below the fold is unreachable" |
| modalFooterUnreachable | high | "Modal action footer (Submit/Cancel buttons) is below the viewport — users cannot click them without scrolling outside the modal" |
| modalTooWideForViewport | medium | "Modal has min-width:{minWidth}px which exceeds viewport width {vw}px — content will overflow or be clipped on mobile" |
| modalContentOverflows | medium | "Modal body content overflows its container — internal content has fixed width wider than the modal itself" |

## Notes on this conversion
- This replaces the old multi-probe orchestrator flow (detectOpenModal → findTrigger → browser_click + wait → detectOpenModal → measure → browser_press_key → cleanup) with ONE in-page async probe. Same checks, same issueTypes — the orchestrator makes a **single** `browser_evaluate` call instead of up to 7 MCP steps.
- The modal is opened via in-page `trigger.click()` and dismissed via in-page Escape/body-click — no real browser-level events required, so this is fully executable. A modal that was already open when the probe ran is left open (it belongs to the cell's prior state); only a modal the probe itself opened is dismissed.
