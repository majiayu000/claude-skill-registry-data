---
name: qa-form-flow
section: interactive
description: "Consolidated form-flow skill. Owns multi-step wizards (Next validation, Back data preservation, step indicator) AND conditional fields (toggle reveals/hides fields, no stuck states, revealed fields interactive). Replaces 2 overlapping skills. Runs as ONE in-page async probe (no AI hand-driving)."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
cacheVersion: "1.0.0"
ownership: "exclusive: any bug about wizard navigation, multi-step forms, or conditional field show/hide belongs to this skill"
replaces:
  - qa-test-form-wizard
  - qa-test-form-conditional
requires: [hasForms]
---
# qa-form-flow — Consolidated Form Flow Skill

Single skill owning wizard navigation and conditional-field behavior.

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it click-by-click with separate `browser_click` / `browser_type` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function discovers the wizard AND conditional toggles, drives Next/Back, fills marker values, activates/deactivates toggles, asserts each result, and returns `findings[]` — all inside the page, in one round-trip. It does its own waits via in-page `setTimeout` promises, so there is **no AI reasoning between clicks**. It **self-skips** (returns `[]`) when neither a wizard nor any toggle is present. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields. The probe resets the wizard to step 1 and restores every toggle before returning.

## What it checks (5 issue types)

### Wizard
| issueType | severity | catches |
|---|---|---|
| `wizardNextNoValidation` | high | Wizard advances to next step without validating current step's required fields |
| `wizardBackLosesData` | high | Clicking Back loses data entered in previous step |
| `wizardNoStepIndicator` | medium | Multi-step form has no visible step indicator (or indicator doesn't reflect current step) |

### Conditional fields
| issueType | severity | catches |
|---|---|---|
| `conditionalFieldReadOnly` | medium | Toggling control reveals fields that are disabled or read-only |
| `conditionalFieldStuck` | medium | Deactivating control didn't hide previously-revealed fields |

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-form-flow' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };

  const stepIndicators = () => [...document.querySelectorAll('[role="tablist"] [role="tab"], .stepper [class*="step"], [class*="wizard"] [class*="step"], ol[class*="step"] > li, [data-step]')];
  const activeStepIdx = () => stepIndicators().findIndex(s => s.getAttribute('aria-selected') === 'true' || s.getAttribute('aria-current') === 'step' || /active|current|selected/i.test(s.className));
  const visibleStep = () => document.querySelector('[role="tabpanel"]:not([hidden]), [aria-hidden="false"][role="tabpanel"], [class*="step-content"]:not([hidden]), [data-step][aria-current="step"]') || document.querySelector('form') || document.body;
  const stepFingerprint = () => { const v = visibleStep(); return v.innerHTML.length + ':' + v.querySelectorAll('input,select,textarea').length; };
  const hasUnfilledRequired = () => [...visibleStep().querySelectorAll('[required], [aria-required="true"]')].some(el => { if (!vis(el)) return false; if (el.type === 'checkbox') return !el.checked; return !el.value || el.value.trim() === ''; });
  const findBtn = re => [...document.querySelectorAll('button, input[type="submit"], a[role="button"]')].find(b => { const t = (b.innerText || b.value || '').toLowerCase().trim(); return re.test(t) && !b.disabled && vis(b); });
  const visibleFieldCount = () => [...document.querySelectorAll('input, select, textarea')].filter(el => { if (el.type === 'hidden' || el.type === 'submit' || el.type === 'button') return false; return vis(el); }).length;

  // ── DISCOVERY ──
  const indicators = stepIndicators().filter(vis);
  const nextBtn = findBtn(/^(next|continue|proceed|step\s*\d)/);
  const isWizard = !!nextBtn && indicators.length >= 2;
  const toggles = [];
  for (const c of [...document.querySelectorAll('input[type="checkbox"]:not([disabled]), input[type="radio"]:not([disabled])')].filter(vis).slice(0, 3))
    toggles.push({ el: c, type: c.type });
  for (const s of [...document.querySelectorAll('select:not([disabled])')].filter(s => s.options.length >= 2 && vis(s)).slice(0, 2))
    toggles.push({ el: s, type: 'select', secondValue: s.options[1].value });
  const limitedToggles = toggles.slice(0, 4);

  if (!isWizard && limitedToggles.length === 0) return [];

  // ── WIZARD TESTS ──
  if (isWizard) {
    // step indicator reflects current step?
    const hasActive = stepIndicators().some(s => s.getAttribute('aria-selected') === 'true' || s.getAttribute('aria-current') === 'step' || /active|current|selected/i.test(s.className));
    if (!hasActive)
      add({ issueType: 'wizardNoStepIndicator', severity: 'medium', selector: sel(indicators[0]), bbox: bb(indicators[0]), description: 'Multi-step form has step elements but none reflects the current step (no active/aria-current marker).', evidence: { stepCount: indicators.length } });

    // Next-without-validation: if current step has unfilled required, clicking Next should NOT advance
    const hadRequired = hasUnfilledRequired();
    const stepBefore = activeStepIdx();
    const fpBefore = stepFingerprint();
    nextBtn.click(); await sleep(500);
    const advanced = activeStepIdx() !== stepBefore || stepFingerprint() !== fpBefore;
    if (advanced && hadRequired)
      add({ issueType: 'wizardNextNoValidation', severity: 'high', selector: sel(nextBtn), bbox: bb(nextBtn), description: "Wizard advanced to the next step while the current step still had unfilled required fields.", evidence: { stepBefore: stepBefore + 1 } });

    // Back preserves data: fill markers on current step, Next, Back, verify markers survive
    const fillInputs = () => [...visibleStep().querySelectorAll('input[type="text"], input[type="email"], textarea')].filter(vis);
    const fi = fillInputs();
    let markerCount = 0;
    for (let i = 0; i < Math.min(fi.length, 4); i++) { if (!fi[i].value) { setNative(fi[i], `argusM${i}`); markerCount++; } }
    if (markerCount > 0) {
      const n2 = findBtn(/^(next|continue|proceed|step\s*\d)/);
      if (n2) {
        n2.click(); await sleep(500);
        const back = findBtn(/^(back|previous|prev|step\s*back)/);
        if (back) {
          back.click(); await sleep(500);
          const after = fillInputs();
          let lost = 0;
          for (let i = 0; i < Math.min(after.length, 4); i++) { if (!String(after[i].value || '').includes(`argusM${i}`)) lost++; }
          if (lost > 0)
            add({ issueType: 'wizardBackLosesData', severity: 'high', selector: sel(back), bbox: bb(back), description: 'Clicking Back lost data entered on the previous step.', evidence: { lost, filled: markerCount } });
        }
      }
    }
    // reset wizard to step 1 (best-effort)
    for (let i = 0; i < 5; i++) { const b = findBtn(/^(back|previous|prev)/); if (!b) break; try { b.click(); await sleep(250); } catch (_) { break; } }
  }

  // ── CONDITIONAL TOGGLE TESTS (max 4) ──
  const activate = t => { if (t.type === 'select') { t.el.value = t.secondValue; t.el.dispatchEvent(new Event('change', { bubbles: true })); } else { if (!t.el.checked) t.el.click(); } };
  const deactivate = t => { if (t.type === 'select') { if (t.el.options[0]) { t.el.value = t.el.options[0].value; t.el.dispatchEvent(new Event('change', { bubbles: true })); } } else { if (t.el.checked) t.el.click(); } };
  for (const t of limitedToggles) {
    const baseline = visibleFieldCount();
    activate(t); await sleep(400);
    const afterActivate = visibleFieldCount();
    if (afterActivate === baseline) { deactivate(t); await sleep(200); continue; } // no conditional behavior
    if (afterActivate > baseline) {
      // revealed fields interactive?
      const stuck = [...document.querySelectorAll('input, select, textarea')].filter(el => { if (el.type === 'hidden' || el.type === 'submit' || el.type === 'button') return false; return vis(el) && (el.disabled || el.readOnly) && !el.hasAttribute('data-allow-readonly'); });
      if (stuck.length > 0)
        add({ issueType: 'conditionalFieldReadOnly', severity: 'medium', selector: sel(t.el), bbox: bb(t.el), description: 'Toggling this control revealed fields that are disabled or read-only.', evidence: { stuckCount: stuck.length, sample: stuck[0].name || stuck[0].id || 'unknown' } });
      // deactivate hides them?
      deactivate(t); await sleep(400);
      if (visibleFieldCount() !== baseline)
        add({ issueType: 'conditionalFieldStuck', severity: 'medium', selector: sel(t.el), bbox: bb(t.el), description: "Deactivating this control did not hide the previously-revealed fields — they stay stuck on screen.", evidence: { baseline, afterDeactivate: visibleFieldCount() } });
    } else {
      deactivate(t); await sleep(200);
    }
  }

  return out;
}
```

## Migration
```toml
[detectors]
qa-form-flow              = true
qa-test-form-wizard       = false
qa-test-form-conditional  = false
```

## Notes on this conversion
- Replaces the old multi-probe orchestrator flow (discover + 7 helper probes driven across many MCP round-trips) with ONE in-page async probe. Same 5 issueTypes, same checks.
- The original per-probe helpers (`discoverFlowControls`, `captureStepFingerprint`, `fillStepWithMarkers`, `checkMarkersStillPresent`, `checkStepIndicator`, `snapshotFieldCount`, `checkRevealedFieldsInteractive`, `resetWizard`, `resetToggles`) are inlined as in-page helper functions inside the single probe.
- Wizard reset and toggle restore run at the end of the probe so the page is clean for the next skill.
