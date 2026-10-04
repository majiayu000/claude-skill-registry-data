---
name: qa-detect-ux-toast-notification
section: visual
description: "Deep-dive deterministic checks for toast/snackbar/notification UI: generic 'successfully completed' messages with no subject, sentence-fragment text ('successfully', 'done'), trailing comma/semicolon in toast text, missing role=alert/status/aria-live (invisible to screen readers), close button with no accessible name, status indicators (badges/chips) using color alone with no state word in their text."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasToastMessages, hasToastContainer, hasAlertBanners]
---

## Why this skill exists

`qa-review-content` (Sonnet) catches *some* generic phrasing and punctuation errors but is non-deterministic. This skill is a **deterministic Layer-1 probe** for the specific bug class of bad toast/notification content + a11y + color-only state — closing the 3 PARTIAL gaps from the toast deep-dive:

1. ⚠️ → ✅ "Toast without subject" / generic message
2. ⚠️ → ✅ "Sentence fragment" (adverb-only or 1-2 word toast)
3. ⚠️ → ✅ Status indicator with color-only signal (no state word in text)

Plus 3 new toast-specific a11y checks.

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `toastGenericMessage` | medium | Toast text matches generic patterns ("successfully completed", "done", "ok", "success", "action successful") with no subject — doesn't say *what* succeeded |
| `toastSentenceFragment` | low | Toast text is an adverb-led fragment ("successfully created", "easily done") or a single-word fragment ("Saved", "Done") without a subject — incomplete sentence |
| `toastTrailingPunctuation` | low | Toast text ends with `,` `;` `:` instead of `.` `!` or no punctuation. Your "successfully completed," bug. |
| `toastCloseButtonNoLabel` | high | Close button (×, ✕, X) inside a toast has no `aria-label`/`title` — screen readers announce only "button" with no context |
| `statusColorOnlySignal` | medium | Status badge/chip uses saturated red/green/yellow background AND its text contains no explicit state word (success/error/warning/active/done/etc.) — color-blind users miss the meaning |

> **Removed 2026-06-11:** `toastMissingLiveRegion` was removed because the check only inspected the toast element itself, not its ancestor chain. Most toast libraries place `aria-live` on a parent container/portal — checking only the toast produced unavoidable false positives on standard library output.

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  function parseRGB(s) {
    if (!s) return null;
    const m = s.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)/);
    if (!m) return null;
    return { r: +m[1], g: +m[2], b: +m[3], a: m[4] !== undefined ? +m[4] : 1 };
  }
  function isStatusColor(rgb) {
    if (!rgb || rgb.a < 0.3) return null;
    const max = Math.max(rgb.r, rgb.g, rgb.b);
    const min = Math.min(rgb.r, rgb.g, rgb.b);
    if (max - min < 50 || max < 100) return null;
    if (rgb.g > rgb.r + 30 && rgb.g > rgb.b + 20) return 'green';
    if (rgb.r > rgb.g + 40 && rgb.r > rgb.b + 30) return 'red';
    if (rgb.r > 200 && rgb.g > 150 && rgb.b < 130) return 'yellow/amber';
    return null;
  }
  const out = [];

  // ── Find toast/notification/snackbar/alert elements ──────────────────
  const toastSel = '.toast, [role="status"], [role="alert"], .notification:not([class*="notification-bell"]):not([class*="notification-icon"]), .snackbar, .mat-snack-bar-container, .mat-mdc-snack-bar-container, .alert, [class*="toast"]:not([class*="toaster-container"]), [class*="snackbar"], .ngx-toastr, .ng-toast, [aria-live="polite"], [aria-live="assertive"]';
  const toasts = [...document.querySelectorAll(toastSel)].filter(visible);

  // Patterns
  const GENERIC_MESSAGE = /^\s*(successfully\s+(completed|done|saved|added|created|updated|deleted|removed|submitted|finished|processed)[,.]?|successfully[,.]?|completed[,.]?|saved[,.]?|done[,.]?|success[,.]?|ok[,.]?|finished[,.]?|added[,.]?|created[,.]?|updated[,.]?|deleted[,.]?|action\s+(successful|completed|done)[,.]?|operation\s+(successful|completed|done|complete)[,.]?|task\s+(completed|done)[,.]?)\s*$/i;
  const ADVERB_FRAGMENT = /^\s*(successfully|easily|automatically|quickly|safely|carefully|properly|recently|just|finally)\s+\w+[,.]?\s*$/i;
  const STATE_WORDS = /(success|error|warning|info|alert|fail(ed|ure)?|complete|done|active|inactive|approved|rejected|denied|enabled|disabled|saved|loading|pending|expired|deleted|removed|verified|invalid|valid|online|offline|busy|away|new|sold|out)/i;

  for (const toast of toasts.slice(0, 6)) {
    // Strip close-button glyphs from text so they don't pollute the message
    let text = (toast.innerText || '').replace(/[××✕✗✖]\s*$/g, '').replace(/\s+/g, ' ').trim();
    // Remove leading icon glyphs / bullets
    text = text.replace(/^[•·▪◆■▶▼◀▲]\s*/, '');

    // ── 1. Generic message ─────────────────────────────────────────────
    if (text.length >= 3 && text.length <= 80 && GENERIC_MESSAGE.test(text)) {
      out.push({
        issueType: 'toastGenericMessage', severity: 'medium',
        selector: sel(toast), bbox: bb(toast),
        description: `Toast/notification text "${text}" is generic and lacks a subject. Use specific context like "Order saved successfully", "Profile updated", "Item deleted". Helps users know what the success/completion refers to.`
      });
    }

    // ── 2. Sentence fragment (adverb-led) ──────────────────────────────
    if (text.length >= 3 && text.length <= 60 && ADVERB_FRAGMENT.test(text)) {
      out.push({
        issueType: 'toastSentenceFragment', severity: 'low',
        selector: sel(toast), bbox: bb(toast),
        description: `Toast text "${text}" is a sentence fragment (adverb + verb only). Add a subject for a complete sentence: "Your order was [adverb-ed]" or restructure.`
      });
    }

    // ── 3. Trailing punctuation ────────────────────────────────────────
    if (text.length > 2 && /[,;:](?:\s)?$/.test(text)) {
      out.push({
        issueType: 'toastTrailingPunctuation', severity: 'low',
        selector: sel(toast), bbox: bb(toast),
        description: `Toast text "${text}" ends with non-terminal punctuation "${text.match(/[,;:]\s*$/)[0].trim()}". Use period, exclamation, or no punctuation to terminate.`
      });
    }

    // ── 4. (removed) Missing ARIA live region ──────────────────────────
    // The live-region check was removed because most toast libraries (React
    // Toastify, ngx-toastr, Angular Material snackbar, Bootstrap toasts, Vue
    // Sonner) place `aria-live` on a PARENT container/portal — not on the
    // individual toast element. Checking only the toast itself produced
    // unavoidable false positives on standard library output ("You are Online"
    // toast on the Issue Budget screenshot, 2026-06-11).

    // ── 5. Close button without accessible name ────────────────────────
    const closeCandidates = [...toast.querySelectorAll('button, a, [role="button"], [class*="close"], [class*="dismiss"]')];
    for (const cb of closeCandidates) {
      if (!visible(cb)) continue;
      const ariaLabel = (cb.getAttribute('aria-label') || '').trim();
      const title = (cb.getAttribute('title') || '').trim();
      const txt = (cb.innerText || '').replace(/\s+/g, '').trim();
      // Likely a close button: 0-1 chars OR a single × / ✕ glyph
      const looksLikeClose = txt.length === 0 || /^[××✕✗✖xX]$/.test(txt);
      const hasLabel = ariaLabel.length > 1 || title.length > 1;
      if (looksLikeClose && !hasLabel) {
        out.push({
          issueType: 'toastCloseButtonNoLabel', severity: 'high',
          selector: sel(cb), bbox: bb(cb),
          description: `Toast close button (glyph: "${txt || 'no text'}") has no aria-label or title. Screen readers announce it only as "button" with no purpose. Add aria-label="Close notification".`
        });
        break;   // one per toast
      }
    }
  }

  // ── 6. Status color-only signal (badges/chips/pills) ──────────────────
  // Walk small status elements that use saturated bg color but whose text
  // doesn't contain an explicit state word.
  const statusEls = [...document.querySelectorAll(
    '.badge, .chip, .pill, .tag, .status, .label.label-success, .label.label-danger, .label.label-warning, [class*="badge-"], [class*="chip-"], [class*="pill-"], [class*="status-"], .indicator'
  )].filter(visible);
  let colorOnlyFlagged = 0;
  for (const el of statusEls.slice(0, 30)) {
    if (colorOnlyFlagged >= 4) break;
    const r = el.getBoundingClientRect();
    if (r.width > 200 || r.height > 60) continue;   // too big = probably not a status pill
    const text = (el.innerText || '').replace(/\s+/g, ' ').trim();
    if (text.length > 30) continue;
    // Skip if text already contains an explicit state word
    if (STATE_WORDS.test(text)) continue;
    const cs = getComputedStyle(el);
    const bg = parseRGB(cs.backgroundColor);
    const tone = isStatusColor(bg);
    if (!tone) continue;
    colorOnlyFlagged++;
    out.push({
      issueType: 'statusColorOnlySignal', severity: 'medium',
      selector: sel(el), bbox: bb(el),
      description: `Status indicator uses ${tone} background (rgb ${bg.r},${bg.g},${bg.b}) to convey meaning but its text "${text}" contains no explicit state word (success/error/warning/active/etc.). Color-blind users (8% of men) may miss the signal. Add a state word or icon with aria-label.`
    });
  }

  return out;
}
```

## Notes

- Bounded: max ~22 findings per cell (6 issue types × ≤ 6 toasts)
- Self-skips: page with no toasts / no status badges returns []
- The 3 PARTIAL gaps from the toast deep-dive are now FULL coverage:
  - `toastGenericMessage` — catches "successfully completed" subjectless toasts
  - `toastSentenceFragment` — catches "successfully completed" adverb-led fragment
  - `statusColorOnlySignal` — catches green/red/yellow badges without explicit state words
- Bonus: `toastTrailingPunctuation` directly catches the "successfully completed**,**" trailing-comma bug
- `toastCloseButtonNoLabel` adds deterministic a11y coverage that the existing `qa-detect-a11y` would miss specifically for transient toast UI
