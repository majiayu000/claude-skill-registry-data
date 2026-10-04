---
name: qa-detect-hover-touch
section: responsiveness
description: "Detects :hover CSS rules that aren't wrapped in @media (hover: hover) — on touch devices these styles get 'stuck' after a tap, leaving buttons/links highlighted indefinitely"
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: false
requires: [hasHoverElements]
---

## What it checks

On touch devices, CSS `:hover` styles trigger on tap and remain stuck until the user taps somewhere else — a button stays "hovered" looking pressed after the user already moved on. The fix is to wrap hover rules in `@media (hover: hover)` so they only apply to devices with real hover capability.

This skill scans the document's stylesheets for `:hover` rules that are NOT inside such a media query.

## Probe (browser_evaluate)

```js
() => {
  const out = [];
  let totalHoverRules = 0;
  let unwrappedHoverRules = 0;
  const samples = [];

  // Walk all loaded stylesheets
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (_) {
      // Cross-origin sheets throw — skip silently
      continue;
    }
    if (!rules) continue;

    // Recursive walker: looks inside @media queries to determine wrapping context
    const walkRules = (rulesList, mediaContext) => {
      for (const r of rulesList) {
        if (r.type === CSSRule.MEDIA_RULE) {
          // Check if this @media condition implies hover-capable device
          const mediaText = r.conditionText || '';
          const hoverCapable = /\(\s*hover\s*:\s*hover\s*\)/i.test(mediaText) ||
                                /\(\s*pointer\s*:\s*fine\s*\)/i.test(mediaText) ||
                                /\(\s*any-hover\s*:\s*hover\s*\)/i.test(mediaText);
          walkRules(r.cssRules || [], hoverCapable || mediaContext);
          continue;
        }
        if (r.type === CSSRule.STYLE_RULE && r.selectorText && r.selectorText.includes(':hover')) {
          totalHoverRules++;
          if (!mediaContext) {
            unwrappedHoverRules++;
            if (samples.length < 5) {
              samples.push(r.selectorText.slice(0, 200));
            }
          }
        }
      }
    };
    walkRules(rules, false);
  }

  if (totalHoverRules === 0) return out;

  const ratio = unwrappedHoverRules / totalHoverRules;
  // Emit one finding per page if a meaningful number of hover rules are unwrapped
  if (unwrappedHoverRules >= 5) {
    out.push({
      issueType: 'hoverStylesStuckOnTouch',
      severity: 'medium',
      selector: 'stylesheet',
      description: `${unwrappedHoverRules} of ${totalHoverRules} (${Math.round(ratio*100)}%) :hover rules are not wrapped in @media (hover: hover) — on touch devices these styles stick after a tap. Sample selectors: ${samples.slice(0,3).join(', ')}`,
      bbox: { x: 0, y: 0, w: 200, h: 60 }
    });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| hoverStylesStuckOnTouch | medium | "{N} :hover rules not wrapped in @media (hover: hover) — buttons stay 'stuck' looking pressed after a tap on touch devices" |
