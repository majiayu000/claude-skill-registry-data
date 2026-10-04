---
name: qa-detect-dark-mode
section: visual
description: "Detects whether the site respects prefers-color-scheme. No dark-mode handling = jarring white flash for dark-mode users"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasThemeToggle, hasDarkModeActive, hasPrefersColorScheme]
---

## What it checks

Modern OSes default to dark mode and users expect sites to follow. If the site:
- Has no `@media (prefers-color-scheme: dark)` rules anywhere
- AND no `<meta name="color-scheme" content="dark light">` declaration
- AND no explicit theme toggle widget present

… then dark-mode users see a blinding white page. The probe scans for at least one of these signals.

## Probe (browser_evaluate)

```js
() => {
  const out = [];

  // 1. Walk stylesheets looking for prefers-color-scheme media queries
  let hasDarkModeMedia = false;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (_) { continue; }
    if (!rules) continue;
    const walk = (rs) => {
      for (const r of rs) {
        if (r.type === CSSRule.MEDIA_RULE) {
          if (/prefers-color-scheme/i.test(r.conditionText || '')) hasDarkModeMedia = true;
          walk(r.cssRules || []);
        }
      }
    };
    walk(rules);
    if (hasDarkModeMedia) break;
  }

  // 2. Check for <meta name="color-scheme">
  const meta = document.querySelector('meta[name="color-scheme" i]');
  const hasColorSchemeMeta = !!meta && meta.getAttribute('content') &&
                              /dark/i.test(meta.getAttribute('content'));

  // 3. Check for `color-scheme:` on :root / html
  const rootColorScheme = getComputedStyle(document.documentElement).colorScheme || '';
  const hasRootColorScheme = /dark/i.test(rootColorScheme);

  // 4. Check for a theme-toggle widget on the page
  const hasToggle = !!document.querySelector(
    '[aria-label*="dark mode" i], [aria-label*="theme" i], ' +
    'button[class*="theme"], button[class*="dark-mode"], ' +
    '[data-testid*="theme"], [data-testid*="dark-mode"]'
  );

  if (!hasDarkModeMedia && !hasColorSchemeMeta && !hasRootColorScheme && !hasToggle) {
    out.push({
      issueType: 'noDarkModeSupport',
      severity: 'low',
      selector: 'html',
      description: 'No @media (prefers-color-scheme), no <meta color-scheme>, no CSS color-scheme on :root, and no theme-toggle widget — dark-mode OS users see a fully white page with no preference detection.',
      bbox: { x: 0, y: 0, w: 200, h: 60 }
    });
  } else if (hasToggle && !hasDarkModeMedia && !hasColorSchemeMeta && !hasRootColorScheme) {
    out.push({
      issueType: 'darkModeManualOnly',
      severity: 'low',
      selector: 'html',
      description: 'A theme-toggle widget exists but no prefers-color-scheme detection — first-time visitors with dark-mode OS still see white until they click the toggle.',
      bbox: { x: 0, y: 0, w: 200, h: 60 }
    });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| noDarkModeSupport | low | "No dark-mode handling at all — dark-mode OS users see a fully white page" |
| darkModeManualOnly | low | "Theme toggle exists but no prefers-color-scheme auto-detection" |
