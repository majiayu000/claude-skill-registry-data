---
name: qa-detect-css-compat
section: visual
description: "Scans CSS stylesheets for properties with known cross-browser compatibility gaps: missing vendor prefixes, Safari-specific traps, Firefox layout quirks, and properties without fallbacks"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it checks

Detects CSS written assuming a single browser engine. Catches patterns where Chrome renders correctly but Firefox/Safari silently fail or produce different output — without needing to actually run in those browsers.

- `missingWebkitBackdropFilter` — `backdrop-filter` used without `-webkit-backdrop-filter` (Safari < 15.4 requires prefix)
- `missingWebkitTextSizeAdjust` — `-webkit-text-size-adjust` absent from html/body (iOS Safari auto-inflates text on orientation change)
- `overscrollBehaviorNoFallback` — `overscroll-behavior` used without acknowledgement (not supported Safari < 16 — bouncing/pulldown can't be controlled)
- `cssVariableNoFallback` — `var(--x)` used in a critical property (color, font-size, display) with no fallback value — if the variable is undefined the property is invalid in all browsers
- `gapOnFlexNoFallback` — `gap` used on a flex container without a `margin` fallback (Safari < 14.1 ignored gap on flex, not grid)
- `aspectRatioNoFallback` — `aspect-ratio` used without a `padding-bottom` fallback wrapper (Safari < 15 / older Android WebView)
- `missingTouchAction` — interactive non-button elements (`[draggable]`, custom sliders, carousels) have no `touch-action` property — causes 300ms tap delay or conflicts with scroll in some browsers

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const issues = new Map(); // type → first occurrence description

  // Scan all accessible stylesheets
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = [...sheet.cssRules]; } catch (_) { continue; } // CORS-blocked = skip
    for (const rule of rules) {
      if (!rule.style) continue;
      const css = rule.cssText || '';
      const style = rule.style;

      // 1. backdrop-filter without -webkit-backdrop-filter
      if (/\bbackdrop-filter\s*:/.test(css) && !/-webkit-backdrop-filter\s*:/.test(css)) {
        if (!issues.has('missingWebkitBackdropFilter'))
          issues.set('missingWebkitBackdropFilter', `backdrop-filter used in "${rule.selectorText || 'unknown'}" without -webkit-backdrop-filter — Safari < 15.4 will ignore it (modal/glassmorphism blur won't render)`);
      }

      // 2. gap on flex container without margin fallback
      if (/\bgap\s*:/.test(css) || style.gap) {
        const sel = rule.selectorText || '';
        // Check if this selector's elements are flex containers
        let el;
        try { el = document.querySelector(sel); } catch (_) {}
        if (el) {
          const display = getComputedStyle(el).display;
          if ((display === 'flex' || display === 'inline-flex') && !issues.has('gapOnFlexNoFallback')) {
            // Check if any margin fallback exists in same rule
            if (!/\bmargin\b/.test(css)) {
              issues.set('gapOnFlexNoFallback', `gap used on flex container "${sel.slice(0,60)}" without margin fallback — Safari < 14.1 ignored flex gap; older devices will have no spacing between flex items`);
            }
          }
        }
      }

      // 3. CSS custom property without fallback in critical properties
      const criticalProps = ['color', 'font-size', 'display', 'background-color', 'border'];
      for (const prop of criticalProps) {
        const val = style.getPropertyValue(prop) || '';
        if (/var\(--[^,)]+\)/.test(val) && !/var\(--[^,)]+,\s*[^)]+\)/.test(val)) {
          if (!issues.has('cssVariableNoFallback'))
            issues.set('cssVariableNoFallback', `var() used for "${prop}" in "${(rule.selectorText || '').slice(0,60)}" with no fallback value — if the custom property is undefined, the element becomes invisible/unstyled in all browsers`);
          break;
        }
      }

      // 4. aspect-ratio without padding-bottom wrapper
      if (/\baspect-ratio\s*:/.test(css) && !issues.has('aspectRatioNoFallback')) {
        issues.set('aspectRatioNoFallback', `aspect-ratio property used in "${(rule.selectorText || '').slice(0,60)}" — Safari < 15 and older Android WebView don't support it. Add a padding-bottom fallback wrapper for older device support.`);
      }
    }
  }

  // 5. -webkit-text-size-adjust on html/body (cannot reliably read from computed style)
  const htmlStyle = document.documentElement.getAttribute('style') || '';
  const bodyStyle = document.body.getAttribute('style') || '';
  // Check via stylesheet for html/body rules
  let hasTextSizeAdjust = false;
  let hasWebkitTextSizeAdjust = false;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = [...sheet.cssRules]; } catch (_) { continue; }
    for (const rule of rules) {
      if (!rule.selectorText || !/^html|^body/.test(rule.selectorText.trim())) continue;
      const css = rule.cssText || '';
      if (/text-size-adjust/.test(css)) hasTextSizeAdjust = true;
      if (/-webkit-text-size-adjust/.test(css)) hasWebkitTextSizeAdjust = true;
    }
  }
  if (hasTextSizeAdjust && !hasWebkitTextSizeAdjust) {
    issues.set('missingWebkitTextSizeAdjust', 'text-size-adjust set on html/body without -webkit-text-size-adjust — iOS Safari will auto-inflate text on orientation change, causing layout shifts');
  }

  // 6. overscroll-behavior usage (Safari < 16 unsupported)
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = [...sheet.cssRules]; } catch (_) { continue; }
    for (const rule of rules) {
      if (!rule.cssText) continue;
      if (/overscroll-behavior/.test(rule.cssText) && !issues.has('overscrollBehaviorNoFallback')) {
        issues.set('overscrollBehaviorNoFallback', `overscroll-behavior used in "${(rule.selectorText||'').slice(0,60)}" — Safari < 16 does not support this property. Pull-to-refresh and scroll chaining cannot be controlled on older iPhones.`);
      }
    }
  }

  // 7. touch-action missing on draggable/interactive custom elements
  const draggables = document.querySelectorAll('[draggable="true"], [class*="slider"], [class*="carousel"], [class*="swipe"]');
  for (const el of draggables) {
    if (out.length + issues.size >= 15) break;
    const s = getComputedStyle(el);
    const ta = s.touchAction || s.getPropertyValue('touch-action') || '';
    if (!ta || ta === 'auto') {
      const sel = `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : '')}`.slice(0,80);
      if (!issues.has('missingTouchAction'))
        issues.set('missingTouchAction', `Draggable/interactive element "${sel}" has no touch-action property — causes 300ms tap delay in some browsers and conflicts with native scroll on iOS`);
    }
  }

  // Convert map to findings (one finding per issue type — stylesheet issues have no bbox)
  for (const [issueType, description] of issues) {
    out.push({ issueType, severity: 'low', selector: 'css', description, bbox: { x: 0, y: 0, w: 0, h: 0 } });
  }
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| missingWebkitBackdropFilter | low | "backdrop-filter used without -webkit-backdrop-filter — Safari < 15.4 won't render blur/glass effects" |
| missingWebkitTextSizeAdjust | low | "text-size-adjust on html/body without -webkit- prefix — iOS Safari auto-inflates text on orientation change" |
| overscrollBehaviorNoFallback | low | "overscroll-behavior used — Safari < 16 ignores it; pull-to-refresh/scroll chaining uncontrollable on older iPhones" |
| cssVariableNoFallback | low | "var(--x) used for critical property without fallback — element breaks silently if variable undefined" |
| gapOnFlexNoFallback | low | "gap on flex container without margin fallback — Safari < 14.1 had no flex gap support" |
| aspectRatioNoFallback | low | "aspect-ratio used without padding-bottom fallback — Safari < 15 / older Android WebView unsupported" |
| missingTouchAction | low | "Draggable element has no touch-action — 300ms tap delay or scroll conflict on mobile browsers" |

**Note:** All findings are `low` severity — these are cross-browser compatibility risks, not definite failures. They indicate that Firefox/Safari users *may* experience degraded rendering even though Chrome renders correctly. Verify each finding against your browser support matrix before filing a ticket.
