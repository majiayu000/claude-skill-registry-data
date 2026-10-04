---
name: qa-detect-ux-affordance
section: visual
description: "Detects affordance UX failures: clickable elements that don't look clickable, hover-only revealed actions (dead on mobile/touch), missing focus indicators, cursor:default on interactives, text inputs without visible borders. Catches the 'I didn't know I could click that' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasActionButtons, hasDragDrop, hasToggleSwitches]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `clickableNoCursor` | medium | Element with click handler (button/[role=button]/[onclick]) has `cursor: default` or `cursor: text` — doesn't signal clickability |
| `linkNotStyledAsLink` | medium | Inline `<a>` inside body text has no underline, no distinct color, no clear affordance — invisible to users |
| `inputNoVisibleBorder` | medium | Visible text input has `border: none` AND no `border-bottom` AND no `box-shadow` — invisible as an input |
| `interactiveNoFocusVisible` | medium | Focusable element has explicit `outline: none` AND no `:focus` ring detected via box-shadow — keyboard users can't see focus |
| `hoverOnlyControl` | medium | Clickable element only visually distinguishes itself on `:hover` (rest state matches body) — completely dead on touch devices |
| `ambiguousClickArea` | low | Container with click handler has children that look more clickable than the container itself (nested buttons) |

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
  const out = [];

  // ── 1. Clickable with non-pointer cursor ──────────────────────────────
  let cursorFlagged = 0;
  const clickables = document.querySelectorAll('button:not([disabled]), a[href], [role="button"]:not([aria-disabled="true"]), [onclick]');
  for (const el of clickables) {
    if (cursorFlagged >= 4) break;
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.cursor === 'default' || cs.cursor === 'text' || cs.cursor === 'auto') {
      cursorFlagged++;
      out.push({
        issueType: 'clickableNoCursor', severity: 'medium',
        selector: sel(el), bbox: bb(el),
        description: `Clickable ${el.tagName.toLowerCase()} has cursor: ${cs.cursor}. Add cursor: pointer so users know they can click it.`
      });
    }
  }

  // ── 2. Inline links not styled as links ───────────────────────────────
  let linkFlagged = 0;
  for (const a of document.querySelectorAll('a[href]')) {
    if (linkFlagged >= 3) break;
    if (!visible(a)) continue;
    if (!a.parentElement) continue;
    // Only inline links inside paragraphs / body text
    const parentTag = a.parentElement.tagName.toLowerCase();
    if (!['p', 'span', 'li', 'td'].includes(parentTag)) continue;
    if (a.querySelector('button, img, svg')) continue;   // not text link
    const text = (a.innerText || '').trim();
    if (text.length < 2 || text.length > 50) continue;
    const cs = getComputedStyle(a);
    const parentCs = getComputedStyle(a.parentElement);
    const hasUnderline = cs.textDecorationLine && cs.textDecorationLine.includes('underline');
    const hasDistinctColor = cs.color !== parentCs.color;
    const hasBoldWeight = parseInt(cs.fontWeight) > parseInt(parentCs.fontWeight);
    if (!hasUnderline && !hasDistinctColor && !hasBoldWeight) {
      linkFlagged++;
      out.push({
        issueType: 'linkNotStyledAsLink', severity: 'medium',
        selector: sel(a), bbox: bb(a),
        description: `Inline link "${text.slice(0, 30)}" has no underline, no distinct color, no weight difference from surrounding text. Users can't see it's a link (WCAG 1.4.1).`
      });
    }
  }

  // ── 3. Inputs with no visible border ──────────────────────────────────
  let inputFlagged = 0;
  const textInputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="number"], input[type="search"], input[type="tel"], input[type="url"], input[type="password"], input:not([type]), textarea');
  for (const inp of textInputs) {
    if (inputFlagged >= 4) break;
    if (!visible(inp)) continue;
    if (inp.disabled || inp.readOnly) continue;
    const cs = getComputedStyle(inp);
    const hasTopBorder = parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none' && cs.borderTopColor !== 'rgba(0, 0, 0, 0)';
    const hasBotBorder = parseFloat(cs.borderBottomWidth) > 0 && cs.borderBottomStyle !== 'none' && cs.borderBottomColor !== 'rgba(0, 0, 0, 0)';
    const hasLeftBorder = parseFloat(cs.borderLeftWidth) > 0 && cs.borderLeftStyle !== 'none' && cs.borderLeftColor !== 'rgba(0, 0, 0, 0)';
    const hasBoxShadow = cs.boxShadow && cs.boxShadow !== 'none';
    const bgDistinct = cs.backgroundColor !== getComputedStyle(inp.parentElement || document.body).backgroundColor;
    if (!hasTopBorder && !hasBotBorder && !hasLeftBorder && !hasBoxShadow && !bgDistinct) {
      inputFlagged++;
      out.push({
        issueType: 'inputNoVisibleBorder', severity: 'medium',
        selector: sel(inp), bbox: bb(inp),
        description: `Input has no border, no box-shadow, no distinct background. Users can't see it's an input field.`
      });
    }
  }

  // ── 4. Focusable elements with no focus indicator ─────────────────────
  let focusFlagged = 0;
  const focusables = document.querySelectorAll('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"]), [role="button"], [role="link"]');
  for (const el of focusables) {
    if (focusFlagged >= 4) break;
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.outlineStyle === 'none' && cs.outlineWidth === '0px') {
      // Try to detect :focus styles via a sheet scan
      let hasFocusStyle = false;
      for (const sheet of document.styleSheets) {
        if (hasFocusStyle) break;
        let rules;
        try { rules = sheet.cssRules; } catch (_) { continue; }
        if (!rules) continue;
        for (const r of rules) {
          if (hasFocusStyle) break;
          if (r.type !== CSSRule.STYLE_RULE) continue;
          if (!r.selectorText) continue;
          if (/:focus(?:-visible)?/.test(r.selectorText) && el.matches(r.selectorText.split(':focus')[0] || '*')) {
            // It has some focus rule; check if it provides outline / box-shadow / border
            const st = r.style;
            if ((st.outline && st.outline !== 'none') ||
                (st.boxShadow && st.boxShadow !== 'none') ||
                st.borderColor || st.borderWidth) {
              hasFocusStyle = true;
            }
          }
        }
      }
      if (!hasFocusStyle) {
        focusFlagged++;
        out.push({
          issueType: 'interactiveNoFocusVisible', severity: 'medium',
          selector: sel(el), bbox: bb(el),
          description: `${el.tagName.toLowerCase()} has outline: none and no detectable :focus / :focus-visible style. Keyboard users see no focus indicator (WCAG 2.4.7).`
        });
      }
    }
  }

  // ── 5. Hover-only revealed control (dead on touch) ────────────────────
  // Detect rules where the rest-state has visibility: hidden or opacity: 0
  // and the :hover state reveals it. Sample a few common patterns.
  let hoverFlagged = 0;
  const hoverCandidates = document.querySelectorAll('[class*="hover"], .show-on-hover, .reveal-on-hover, .hover-reveal');
  for (const el of hoverCandidates) {
    if (hoverFlagged >= 2) break;
    const cs = getComputedStyle(el);
    if (cs.opacity === '0' || cs.visibility === 'hidden' || cs.display === 'none') {
      // Element is rest-hidden. Its parent likely has :hover rule to show it.
      const parent = el.parentElement;
      if (parent) {
        // Heuristic: if the element CAN be focused or has interactive descendants → flag
        const hasInteractive = el.querySelector('button, a, input, [role="button"]') || el.matches('button, a, input, [role="button"]');
        if (hasInteractive) {
          hoverFlagged++;
          out.push({
            issueType: 'hoverOnlyControl', severity: 'medium',
            selector: sel(parent), bbox: bb(parent),
            description: `Interactive control inside .${el.className.split(/\s+/)[0]} is hidden at rest and revealed on hover. Touch devices have no hover — control is unreachable on mobile/tablet.`
          });
        }
      }
    }
  }

  // ── 6. Ambiguous click area (nested clickables) ───────────────────────
  let ambigFlagged = 0;
  const containers = document.querySelectorAll('[onclick]:not(button):not(a), .clickable-card, .card[onclick], tr[onclick], [role="button"]:not(button)');
  for (const c of containers) {
    if (ambigFlagged >= 3) break;
    if (!visible(c)) continue;
    const innerInteractives = c.querySelectorAll('button, a[href], [role="button"]');
    if (innerInteractives.length >= 1) {
      ambigFlagged++;
      out.push({
        issueType: 'ambiguousClickArea', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Container ${c.tagName.toLowerCase()} has click handler AND ${innerInteractives.length} nested button/link. Click on inner element triggers BOTH handlers — unpredictable behavior.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: 4 cursor + 3 link + 4 input + 4 focus + 2 hover + 3 ambig = max ~20 findings
- Self-skips: page with no interactives returns []
- `interactiveNoFocusVisible` is the highest-impact for keyboard accessibility
- `hoverOnlyControl` is the highest-impact for mobile UX (dead on touch)
