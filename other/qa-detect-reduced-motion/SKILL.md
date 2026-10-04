---
name: qa-detect-reduced-motion
section: accessibility
description: "WCAG 2.3.3 — detects animations/transitions that are not gated by @media (prefers-reduced-motion: reduce). Vestibular-disorder users get sick from motion."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasAnimations, hasTransitions]
---

## What it checks

WCAG 2.3.3 (Animation from Interactions): if the site has any animation or transition over ~5 seconds OR uses parallax / autoplay video, it must respect `prefers-reduced-motion: reduce`. Sites with no reduced-motion handling whatsoever fail accessibility.

The probe scans stylesheets for animation/transition rules and checks whether any are wrapped in `@media (prefers-reduced-motion: reduce)` (or its inverse, `(prefers-reduced-motion: no-preference)`).

## Probe (browser_evaluate)

```js
() => {
  const out = [];
  let totalAnimRules = 0;
  let reducedMotionRules = 0;
  let hasReducedMotionMediaQuery = false;
  const sampleSelectors = [];

  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (_) { continue; }
    if (!rules) continue;
    const walk = (rulesList, inReducedMotion) => {
      for (const r of rulesList) {
        if (r.type === CSSRule.MEDIA_RULE) {
          const mediaText = r.conditionText || '';
          const isReducedMotion = /prefers-reduced-motion\s*:\s*reduce/i.test(mediaText);
          const isNoPreference = /prefers-reduced-motion\s*:\s*no-preference/i.test(mediaText);
          if (isReducedMotion || isNoPreference) hasReducedMotionMediaQuery = true;
          walk(r.cssRules || [], inReducedMotion || isReducedMotion);
          continue;
        }
        if (r.type === CSSRule.STYLE_RULE && r.style) {
          const hasAnim = r.style.animation || r.style.animationName ||
                          r.style.transition || r.style.transitionProperty;
          if (!hasAnim) continue;
          totalAnimRules++;
          if (inReducedMotion) reducedMotionRules++;
          if (sampleSelectors.length < 5) sampleSelectors.push(r.selectorText.slice(0, 80));
        }
      }
    };
    walk(rules, false);
  }

  // No animations at all → nothing to flag
  if (totalAnimRules === 0) return out;

  // Site has animations but ZERO reduced-motion media queries → WCAG 2.3.3 failure
  if (!hasReducedMotionMediaQuery) {
    out.push({
      issueType: 'noReducedMotionSupport',
      severity: 'medium',
      selector: 'stylesheet',
      description: `${totalAnimRules} CSS rules use animation/transition but no @media (prefers-reduced-motion: reduce) media query exists anywhere in the stylesheets — WCAG 2.3.3 violation. Vestibular-disorder users will experience motion sickness. Sample selectors: ${sampleSelectors.slice(0,3).join(' | ')}`,
      bbox: { x: 0, y: 0, w: 200, h: 60 }
    });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| noReducedMotionSupport | medium | "Stylesheet has animations but no @media (prefers-reduced-motion: reduce) — WCAG 2.3.3 violation" |
