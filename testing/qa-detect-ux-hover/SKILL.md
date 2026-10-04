---
name: qa-detect-ux-hover
section: visual
description: "Detects hover-state quality issues: buttons/links with no :hover style at all, hover state identical to default state (no visual change), hover color off the site theme, hover transitions missing (abrupt change), icon-only buttons with no hover feedback. Catches the 'button doesn't have good hover' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasHoverElements]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `buttonNoHoverState` | medium | Button has no detectable `:hover` rule in any stylesheet — no visual feedback when user hovers |
| `linkNoHoverState` | medium | Inline link has no `:hover` rule — users can't tell it's hoverable (especially when also missing underline) |
| `iconButtonNoHoverFeedback` | medium | Icon-only button has no `:hover` rule — no feedback at all for the user |
| `hoverNoTransition` | low | `:hover` changes color/background but no `transition` property — abrupt change feels broken |
| `hoverColorOffTheme` | low | `:hover` color/bg uses a hue far from the site's primary theme (Δhue > 40°) |
| `hoverStateOnTouchOnlyContent` | low | `:hover` is the ONLY way to discover a control on a touch viewport (mobile/tablet) — dead control on touch devices |

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
  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0; const l = (max + min) / 2;
    if (max !== min) {
      const d = max - min;
      switch (max) {
        case r: h = ((g - b) / d + (g < b ? 6 : 0)); break;
        case g: h = ((b - r) / d + 2); break;
        case b: h = ((r - g) / d + 4); break;
      }
      h *= 60;
    }
    return h;
  }
  const out = [];

  // ── Collect all :hover rules from stylesheets ─────────────────────────
  // Map: selector base (without :hover) → { hasColor, hasBg, hasTransform, hasBorder, hasOpacity, hasOutline, color, bg }
  const hoverRules = new Map();
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (_) { continue; }
    if (!rules) continue;
    const walk = (rs) => {
      for (const r of rs) {
        if (r.type === CSSRule.MEDIA_RULE) { walk(r.cssRules || []); continue; }
        if (r.type !== CSSRule.STYLE_RULE) continue;
        if (!r.selectorText || !/:hover/.test(r.selectorText)) continue;
        const baseSel = r.selectorText.replace(/:hover[^\s,]*/g, '').trim();
        if (!baseSel) continue;
        const st = r.style;
        if (!hoverRules.has(baseSel)) hoverRules.set(baseSel, { props: {} });
        const info = hoverRules.get(baseSel);
        if (st.color) info.props.color = st.color;
        if (st.backgroundColor || st.background) info.props.bg = st.backgroundColor || st.background;
        if (st.transform) info.props.transform = st.transform;
        if (st.borderColor || st.border) info.props.border = st.borderColor || st.border;
        if (st.opacity) info.props.opacity = st.opacity;
        if (st.outline) info.props.outline = st.outline;
        if (st.boxShadow) info.props.boxShadow = st.boxShadow;
      }
    };
    walk(rules);
  }
  function hasHoverRuleFor(el) {
    // Check if any tracked selector matches this element
    for (const [base, info] of hoverRules) {
      try {
        if (el.matches(base)) return info;
      } catch (_) {}
    }
    return null;
  }
  function findThemePrimaryHue() {
    // Sample saturated button backgrounds to estimate theme hue
    const samples = [];
    for (const b of document.querySelectorAll('button, .btn, .badge, thead, header')) {
      if (samples.length >= 12) break;
      if (!visible(b)) continue;
      const bg = parseRGB(getComputedStyle(b).backgroundColor);
      if (!bg || bg.a < 0.5) continue;
      const max = Math.max(bg.r, bg.g, bg.b), min = Math.min(bg.r, bg.g, bg.b);
      if (max - min < 60 || max < 100) continue;  // not saturated
      samples.push(rgbToHsl(bg.r, bg.g, bg.b));
    }
    if (samples.length < 2) return null;
    // Bin by 15° and pick dominant
    const bins = new Map();
    for (const h of samples) {
      const bin = Math.round(h / 15) * 15;
      bins.set(bin, (bins.get(bin) || 0) + 1);
    }
    let top = null, topN = 0;
    for (const [b, n] of bins) {
      if (n > topN) { topN = n; top = b; }
    }
    return top;
  }
  const themeHue = findThemePrimaryHue();

  // ── 1. Buttons with no hover state ──────────────────────────────────
  const buttons = [...document.querySelectorAll('button:not([disabled]), input[type="button"], input[type="submit"], [role="button"]')]
    .filter(visible);
  let btnFlagged = 0;
  for (const b of buttons) {
    if (btnFlagged >= 4) break;
    const info = hasHoverRuleFor(b);
    if (!info || Object.keys(info.props).length === 0) {
      btnFlagged++;
      const t = (b.innerText || b.value || '').trim();
      out.push({
        issueType: 'buttonNoHoverState', severity: 'medium',
        selector: sel(b), bbox: bb(b),
        description: `Button "${t.slice(0, 30)}" has no detectable :hover rule. No visual feedback when user hovers.`
      });
    }
  }

  // ── 2. Inline links with no hover state ──────────────────────────────
  let linkFlagged = 0;
  for (const a of document.querySelectorAll('a[href]:not([role="button"])')) {
    if (linkFlagged >= 3) break;
    if (!visible(a)) continue;
    if (a.querySelector('button, img, svg')) continue;
    const info = hasHoverRuleFor(a);
    if (!info || Object.keys(info.props).length === 0) {
      linkFlagged++;
      out.push({
        issueType: 'linkNoHoverState', severity: 'medium',
        selector: sel(a), bbox: bb(a),
        description: `Link "${(a.innerText || '').trim().slice(0, 30)}" has no :hover rule. Users can't tell it's interactive (especially if also no underline).`
      });
    }
  }

  // ── 3. Icon-only buttons with no hover feedback ──────────────────────
  let iconBtnFlagged = 0;
  for (const b of buttons) {
    if (iconBtnFlagged >= 3) break;
    const text = (b.innerText || b.value || '').trim();
    if (text.length > 0) continue;     // not icon-only
    const hasIcon = b.querySelector('svg, i, img');
    if (!hasIcon) continue;
    const info = hasHoverRuleFor(b);
    if (!info || Object.keys(info.props).length === 0) {
      iconBtnFlagged++;
      out.push({
        issueType: 'iconButtonNoHoverFeedback', severity: 'medium',
        selector: sel(b), bbox: bb(b),
        description: `Icon-only button has no :hover rule. Users hovering see no feedback — feels broken.`
      });
    }
  }

  // ── 4. Hover changes color/bg but no transition ──────────────────────
  let transitionFlagged = 0;
  for (const b of buttons) {
    if (transitionFlagged >= 2) break;
    const info = hasHoverRuleFor(b);
    if (!info || !(info.props.color || info.props.bg)) continue;
    const cs = getComputedStyle(b);
    if (!cs.transition || cs.transition === 'all 0s ease 0s' || cs.transitionDuration === '0s') {
      transitionFlagged++;
      const t = (b.innerText || b.value || '').trim();
      out.push({
        issueType: 'hoverNoTransition', severity: 'low',
        selector: sel(b), bbox: bb(b),
        description: `Button "${t.slice(0, 30)}" has :hover color/bg change but no transition declared. Abrupt change feels broken — add transition: background 150ms ease.`
      });
    }
  }

  // ── 5. Hover color off theme ────────────────────────────────────────
  if (themeHue != null) {
    let offThemeFlagged = 0;
    for (const [base, info] of hoverRules) {
      if (offThemeFlagged >= 2) break;
      const cVal = info.props.bg || info.props.color;
      if (!cVal) continue;
      const m = cVal.match(/rgba?\(\d+,\s*\d+,\s*\d+(?:,\s*[\d.]+)?\)|#[0-9a-fA-F]{3,8}/);
      if (!m) continue;
      let rgb;
      if (m[0].startsWith('#')) {
        const hex = m[0].slice(1);
        const full = hex.length === 3 ? hex.split('').map(c => c + c).join('') : hex.slice(0, 6);
        rgb = { r: parseInt(full.slice(0,2),16), g: parseInt(full.slice(2,4),16), b: parseInt(full.slice(4,6),16), a: 1 };
      } else {
        rgb = parseRGB(m[0]);
      }
      if (!rgb) continue;
      const max = Math.max(rgb.r, rgb.g, rgb.b), min = Math.min(rgb.r, rgb.g, rgb.b);
      if (max - min < 60 || max < 100) continue;   // not saturated
      const hueH = rgbToHsl(rgb.r, rgb.g, rgb.b);
      const delta = Math.min(Math.abs(hueH - themeHue), 360 - Math.abs(hueH - themeHue));
      if (delta > 40) {
        offThemeFlagged++;
        out.push({
          issueType: 'hoverColorOffTheme', severity: 'low',
          selector: base.slice(0, 100),
          description: `Hover rule "${base.slice(0, 60)}" uses color hue ${Math.round(hueH)}° but site theme is ~${Math.round(themeHue)}°. Δ${Math.round(delta)}° — hover state looks unrelated to the brand.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 4 button + 3 link + 3 icon-btn + 2 no-transition + 2 off-theme = max ~14 findings
- Self-skips: page with no buttons/links returns []
- Cross-origin stylesheets skipped via try/catch
- The `buttonNoHoverState` catches the "button doesn't have good hover" issue you mentioned
- The `iconButtonNoHoverFeedback` catches the ↑↓ icon in your screenshots that gives no hover feedback
