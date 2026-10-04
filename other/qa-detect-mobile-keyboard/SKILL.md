---
name: qa-detect-mobile-keyboard
section: responsiveness
description: "Detects layout that breaks when the on-screen keyboard appears AND inputs with wrong type/inputmode that show the wrong keyboard on mobile (QWERTY instead of numpad, etc.). Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: [mobile]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasInputs]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_wait_for` MCP steps. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function (1) passively scans every input for a wrong `type`/`inputmode` vs its label/placeholder semantics, then (2) focuses the lowest visible input in-page (`el.focus()`), waits with an in-page `setTimeout` promise so any scroll-into-view JS runs, and measures whether the input sits in the simulated keyboard zone or is covered by a fixed bottom bar — all inside the page, in one round-trip. There is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when the page has no usable inputs. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe blurs the focused input before returning.

**Detection-only note:** an in-page probe cannot summon a real on-screen keyboard (that requires a physical device / real OS soft-keyboard). The keyboard-overlap and scroll-into-view checks are therefore *static heuristics* — they measure the input's position against a simulated keyboard zone (lower 40% of the viewport) and detect fixed bottom bars that would compound real-keyboard occlusion. This is the same approximation the old prose flow used; no real-device step is added.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-mobile-keyboard' }, o));
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── (1) PASSIVE: wrong mobile keyboard ──
  const heuristics = [
    { test: /phone|tel|mobile|cell|fax/i,              expectedType: 'tel',    expectedInputmode: 'tel',     label: 'phone number' },
    { test: /email|e-mail/i,                            expectedType: 'email',  expectedInputmode: 'email',   label: 'email address' },
    { test: /zip|postal|postcode/i,                     expectedType: 'text',   expectedInputmode: 'numeric', label: 'ZIP/postal code' },
    { test: /card.?num|credit.?card|debit.?card/i,      expectedType: 'text',   expectedInputmode: 'numeric', label: 'card number' },
    { test: /cvv|cvc|security.?code/i,                  expectedType: 'text',   expectedInputmode: 'numeric', label: 'CVV' },
    { test: /\bamount\b|\bprice\b|\bcost\b|\bqty\b|\bquantity\b|\bage\b|\bpin\b/i, expectedType: 'number', expectedInputmode: 'numeric', label: 'numeric value' },
    { test: /\bsearch\b/i,                              expectedType: 'search', expectedInputmode: 'search',  label: 'search field' },
  ];
  for (const input of document.querySelectorAll('input[type="text"], input:not([type])')) {
    if (out.length >= 10) break;
    const r = input.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || input.disabled || input.readOnly) continue;
    const labelEl = input.labels && input.labels[0];
    const labelText = ((labelEl && (labelEl.innerText || labelEl.textContent)) || input.getAttribute('aria-label') || input.getAttribute('placeholder') || input.name || '').toLowerCase();
    if (!labelText) continue;
    const currentType = (input.type || 'text').toLowerCase();
    const currentInputmode = (input.getAttribute('inputmode') || '').toLowerCase();
    const sel = input.id ? `#${input.id}` : (input.name ? `[name="${input.name}"]` : 'input');
    for (const h of heuristics) {
      if (!h.test.test(labelText)) continue;
      if (currentType !== h.expectedType && currentInputmode !== h.expectedInputmode)
        add({ issueType: 'wrongMobileKeyboard', severity: 'medium', selector: sel, bbox: bb(input), description: `"${labelText}" field uses type="${currentType}" without inputmode="${h.expectedInputmode}" — mobile users see QWERTY instead of the ${h.expectedInputmode} keyboard.`, evidence: { currentType, expectedInputmode: h.expectedInputmode } });
      break;
    }
  }

  // ── (2) pick the lowest visible input, focus it ──
  const inputs = [...document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="search"], textarea')]
    .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled && !el.readOnly; });
  if (inputs.length === 0) return out; // self-skip the interaction part (passive findings still returned)

  inputs.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  const target = inputs[inputs.length - 1];
  const targetSel = target.id ? `#${target.id}` : (target.name ? `[name="${target.name}"]` : target.tagName.toLowerCase());
  const initialTop = Math.round(target.getBoundingClientRect().top);

  try { target.focus(); target.dispatchEvent(new FocusEvent('focus', { bubbles: false })); } catch (_) {}
  await sleep(400);

  const vh = window.innerHeight;
  const r = target.getBoundingClientRect();
  const currentTop = Math.round(r.top);
  const keyboardTop = vh * 0.6;
  const inKeyboardZone = r.bottom > keyboardTop;
  const didScrollIntoView = Math.abs(currentTop - initialTop) > 8;

  // fixed/sticky bottom bar overlapping the input
  let coveredByBottomFixed = false, coveringSelector = '';
  for (const c of document.querySelectorAll('[class*="bottom"], [class*="footer"], [class*="tab-bar"], [class*="sticky"], [class*="fixed"]')) {
    const cs = getComputedStyle(c);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const cr = c.getBoundingClientRect();
    if (cr.height === 0) continue;
    if (cr.bottom > vh - 4 && cr.top > vh - 200 && cr.top < r.bottom && cr.bottom > r.top) {
      coveredByBottomFixed = true; coveringSelector = c.id ? `#${c.id}` : c.tagName.toLowerCase(); break;
    }
  }
  const visualViewportAvailable = !!window.visualViewport;

  if (coveredByBottomFixed)
    add({ issueType: 'inputHiddenByBottomBar', severity: 'high', selector: targetSel, bbox: bb(target), description: `Focused input is overlapped by a fixed bottom bar (${coveringSelector}) — keyboard would cover even more of the input on a real device.`, evidence: { coveringSelector } });
  if (inKeyboardZone && !didScrollIntoView)
    add({ issueType: 'inputInKeyboardZoneNoScroll', severity: 'medium', selector: targetSel, bbox: bb(target), description: 'Focused input sits in the lower 40% of the viewport and the page did not scroll it into view — on a real device the keyboard hides it.', evidence: { initialTop, currentTop, vh } });
  if (!visualViewportAvailable)
    add({ issueType: 'noVisualViewportHandling', severity: 'low', selector: targetSel, bbox: bb(target), description: 'Site does not appear to use the visualViewport API — cannot dynamically respond to keyboard appearance.', uncertain: true, evidence: {} });

  // ── RESTORE: blur ──
  try { target.blur(); document.body.focus(); } catch (_) {}

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| wrongMobileKeyboard | medium | '"{label}" field uses type="{t}" without inputmode="{mode}" — mobile users see QWERTY instead of the correct keyboard' |
| inputHiddenByBottomBar | high | "Focused input is overlapped by a fixed bottom bar — keyboard would cover even more of the input on real device" |
| inputInKeyboardZoneNoScroll | medium | "Focused input sits in the lower 40% of the viewport and the page did not scroll it into view — on real device the keyboard hides it" |
| noVisualViewportHandling | low | "Site does not appear to use the visualViewport API — cannot dynamically respond to keyboard appearance" |

## Notes on this conversion
- This replaces the old multi-probe orchestrator flow (passive scan → findInput → browser_click → wait → measure → blur) with ONE in-page async probe. Same checks, same issueTypes — the orchestrator makes a **single** `browser_evaluate` call instead of ~5 MCP steps.
- Focus is applied via in-page `el.focus()` instead of `browser_click`, and scroll-into-view is detected by comparing the input's top before vs after focus (the old flow carried `initialPosition` across two probes; here it is captured and compared inside one function). The on-screen-keyboard occlusion checks remain static heuristics — a real soft keyboard cannot be summoned in-page; that limitation existed in the prose version too and no real-device MCP step was ever part of this skill.
