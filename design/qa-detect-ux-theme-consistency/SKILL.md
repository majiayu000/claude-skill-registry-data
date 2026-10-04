---
name: qa-detect-ux-theme-consistency
section: visual
description: "Detects color/theme mismatches: focus ring color doesn't match site primary, link color drifts from theme, accent/hover colors break visual identity, mix of blue/purple/teal across same UI surface. Catches the 'why does this part look like a different website' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it catches — 7 issue types

| issueType | severity | What |
|---|---|---|
| `focusRingThemeMismatch` | medium | Input/button `:focus` outline/border color is far (HSL Δhue > 30°) from the site's primary theme color — looks like a different design system (your Provinces page bug: purple focus on blue theme) |
| `primaryButtonColorVariance` | medium | Multiple buttons styled as primary have different background colors — pick one |
| `linkColorOffTheme` | low | Inline link color is HSL hue far from theme primary — visual inconsistency |
| `themePrimaryUndefined` | low | No clear theme primary color detectable (every button/header uses a different color) |
| `accentColorMixed` | low | UI uses 3+ distinct saturated accent colors on same screen (visual noise) |
| `statusColorMisused` | low | Element uses status semantic color (red/green/yellow) for a non-status purpose (e.g. action button in red on a non-destructive action) |
| `themeBgInconsistent` | low | Page sections use noticeably different background tones (e.g. `#f8fafc` vs `#ffffff` vs `#f0f0f0`) without semantic meaning |

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

  // ── Helpers: parse rgb / rgba, convert to HSL ─────────────────────────
  function parseRGB(s) {
    if (!s) return null;
    const m = s.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)/);
    if (!m) return null;
    const [r, g, b] = [+m[1], +m[2], +m[3]];
    const a = m[4] !== undefined ? +m[4] : 1;
    return { r, g, b, a };
  }
  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s = 0; const l = (max + min) / 2;
    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = ((g - b) / d + (g < b ? 6 : 0)); break;
        case g: h = ((b - r) / d + 2); break;
        case b: h = ((r - g) / d + 4); break;
      }
      h *= 60;
    }
    return { h, s: s * 100, l: l * 100 };
  }
  function hueDelta(h1, h2) {
    const d = Math.abs(h1 - h2) % 360;
    return d > 180 ? 360 - d : d;
  }
  function isSaturatedColor(rgb) {
    if (!rgb) return false;
    if (rgb.a < 0.5) return false;
    const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    return hsl.s > 30 && hsl.l > 20 && hsl.l < 80;
  }

  // ── Detect site's primary theme color ─────────────────────────────────
  // Sample 8-12 saturated buttons/headers — most common hue = primary
  const candidates = [];
  const sources = document.querySelectorAll('button, .btn, .button, .badge, thead, th, .navbar, header, [role="banner"]');
  for (const el of sources) {
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    const bg = parseRGB(cs.backgroundColor);
    if (isSaturatedColor(bg)) {
      const hsl = rgbToHsl(bg.r, bg.g, bg.b);
      candidates.push({ hsl, hue: Math.round(hsl.h / 10) * 10, rgb: bg, el });
    }
    if (candidates.length >= 40) break;
  }

  let themePrimary = null;
  if (candidates.length >= 2) {
    // Bin hues to nearest 10°, find dominant
    const bins = new Map();
    for (const c of candidates) {
      const bin = c.hue;
      if (!bins.has(bin)) bins.set(bin, []);
      bins.get(bin).add ? bins.get(bin).push(c) : bins.get(bin).push(c);
    }
    let topHue = null, topCount = 0;
    for (const [bin, arr] of bins) {
      if (arr.length > topCount) { topCount = arr.length; topHue = bin; }
    }
    if (topCount >= 2) {
      // Average the dominant-bin colors
      const dom = bins.get(topHue);
      const avgH = dom.reduce((s, c) => s + c.hsl.h, 0) / dom.length;
      const avgS = dom.reduce((s, c) => s + c.hsl.s, 0) / dom.length;
      const avgL = dom.reduce((s, c) => s + c.hsl.l, 0) / dom.length;
      themePrimary = { h: avgH, s: avgS, l: avgL, count: topCount };
    } else {
      // No dominant theme — every button a different color
      out.push({
        issueType: 'themePrimaryUndefined', severity: 'low', selector: 'body',
        description: `Sampled ${candidates.length} saturated buttons/headers but no dominant hue (top bin had only ${topCount}). No clear theme primary — visual identity broken.`
      });
    }
  }

  // ── 1. Focus ring theme mismatch ──────────────────────────────────────
  if (themePrimary) {
    let focusFlagged = 0;
    // Sample inputs / focusable elements — look for explicit focus color rules
    for (const sheet of document.styleSheets) {
      if (focusFlagged >= 3) break;
      let rules;
      try { rules = sheet.cssRules; } catch (_) { continue; }
      if (!rules) continue;
      for (const r of rules) {
        if (focusFlagged >= 3) break;
        if (r.type !== CSSRule.STYLE_RULE) continue;
        if (!r.selectorText || !/:focus/.test(r.selectorText)) continue;
        const st = r.style;
        // Look for outline-color, border-color, box-shadow with a color
        const colorProps = ['outlineColor', 'borderColor', 'borderTopColor', 'borderLeftColor', 'boxShadow', 'caretColor'];
        for (const prop of colorProps) {
          const val = st[prop];
          if (!val) continue;
          const m = val.match(/rgba?\(\d+,\s*\d+,\s*\d+(?:,\s*[\d.]+)?\)|#[0-9a-fA-F]{3,8}/);
          if (!m) continue;
          let rgb;
          if (m[0].startsWith('#')) {
            const hex = m[0].slice(1);
            const full = hex.length === 3 ? hex.split('').map(c => c + c).join('') : hex.slice(0, 6);
            rgb = { r: parseInt(full.slice(0,2),16), g: parseInt(full.slice(2,4),16), b: parseInt(full.slice(4,6),16), a: 1 };
          } else {
            rgb = parseRGB(m[0]);
          }
          if (!rgb || !isSaturatedColor(rgb)) continue;
          const focusHsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
          const delta = hueDelta(focusHsl.h, themePrimary.h);
          if (delta > 30) {
            focusFlagged++;
            out.push({
              issueType: 'focusRingThemeMismatch', severity: 'medium',
              selector: r.selectorText.slice(0, 100),
              description: `Focus color hue ${Math.round(focusHsl.h)}° differs from site theme primary hue ${Math.round(themePrimary.h)}° by ${Math.round(delta)}°. Focus ring (rgb ${rgb.r},${rgb.g},${rgb.b}) looks like a different design system than the theme primary.`
            });
            break;
          }
        }
      }
    }
  }

  // ── 2. Primary button color variance ──────────────────────────────────
  if (themePrimary) {
    // Find buttons styled as "primary" by class name pattern OR by similar color profile
    const primaryBtns = [...document.querySelectorAll('button.primary, button.btn-primary, button.mat-primary, [class*="primary"]')].filter(visible);
    const colorBins = new Map();
    for (const b of primaryBtns) {
      const cs = getComputedStyle(b);
      const bg = parseRGB(cs.backgroundColor);
      if (!isSaturatedColor(bg)) continue;
      const hsl = rgbToHsl(bg.r, bg.g, bg.b);
      const bin = Math.round(hsl.h / 5) * 5;
      colorBins.set(bin, (colorBins.get(bin) || 0) + 1);
    }
    if (colorBins.size >= 2) {
      const hues = [...colorBins.keys()].sort();
      const maxDelta = hueDelta(hues[0], hues[hues.length - 1]);
      if (maxDelta > 15) {
        out.push({
          issueType: 'primaryButtonColorVariance', severity: 'medium', selector: 'body',
          description: `Primary buttons use ${colorBins.size} distinct hues (Δ ${Math.round(maxDelta)}°). Pick one primary color and apply consistently.`
        });
      }
    }
  }

  // ── 3. Link color off theme ───────────────────────────────────────────
  if (themePrimary) {
    const links = [...document.querySelectorAll('a[href]')].filter(visible).slice(0, 30);
    let linkFlagged = 0;
    const linkColors = new Map();
    for (const a of links) {
      if (a.querySelector('button, svg, img')) continue;   // not text link
      const cs = getComputedStyle(a);
      const fg = parseRGB(cs.color);
      if (!fg || !isSaturatedColor(fg)) continue;
      const hsl = rgbToHsl(fg.r, fg.g, fg.b);
      const bin = Math.round(hsl.h / 10) * 10;
      linkColors.set(bin, (linkColors.get(bin) || 0) + 1);
    }
    if (linkColors.size > 0) {
      const dominantLink = [...linkColors.entries()].sort((a, b) => b[1] - a[1])[0][0];
      const delta = hueDelta(dominantLink, themePrimary.h);
      if (delta > 40) {
        out.push({
          issueType: 'linkColorOffTheme', severity: 'low', selector: 'a',
          description: `Inline-link color hue ~${Math.round(dominantLink)}° differs from theme primary ~${Math.round(themePrimary.h)}° by ${Math.round(delta)}°. Links visually disconnected from site identity.`
        });
      }
    }
  }

  // ── 4. Accent colors mixed ────────────────────────────────────────────
  if (candidates.length >= 5) {
    const uniqueHueBins = new Set();
    for (const c of candidates) uniqueHueBins.add(c.hue);
    if (uniqueHueBins.size >= 4) {
      out.push({
        issueType: 'accentColorMixed', severity: 'low', selector: 'body',
        description: `UI shows ${uniqueHueBins.size} distinct saturated hues on screen: ${[...uniqueHueBins].slice(0, 6).join('°, ')}°. Consolidate accents — typical UI uses ≤ 2 primary + 3-4 semantic (success/warn/error/info).`
      });
    }
  }

  // ── 5. Status semantic colors misused ─────────────────────────────────
  // Red (hue 0-15 or 345-360) and green (90-150) are semantic in UI:
  // - red on a non-destructive action is misleading
  // - green on a non-success action is misleading
  let statusMisusedFlagged = 0;
  const interactives = document.querySelectorAll('button, a.btn, [role="button"]');
  const NON_DESTRUCTIVE_LABELS = /\b(save|submit|continue|next|ok|apply|create|update|approve|done|finish|send)\b/i;
  const NON_SUCCESS_LABELS = /\b(cancel|delete|remove|discard|back|previous|close)\b/i;
  for (const el of interactives) {
    if (statusMisusedFlagged >= 3) break;
    if (!visible(el)) continue;
    const text = (el.innerText || el.value || '').trim();
    if (!text) continue;
    const cs = getComputedStyle(el);
    const bg = parseRGB(cs.backgroundColor);
    if (!isSaturatedColor(bg)) continue;
    const hsl = rgbToHsl(bg.r, bg.g, bg.b);
    const isRed = hsl.h < 20 || hsl.h > 340;
    const isGreen = hsl.h > 90 && hsl.h < 160;
    if (isRed && NON_DESTRUCTIVE_LABELS.test(text)) {
      statusMisusedFlagged++;
      out.push({
        issueType: 'statusColorMisused', severity: 'low', selector: sel(el), bbox: bb(el),
        description: `Confirmative action "${text.slice(0, 30)}" uses red (hue ${Math.round(hsl.h)}°) — red is reserved for destructive actions. Confusing color semantics.`
      });
    } else if (isGreen && NON_SUCCESS_LABELS.test(text)) {
      statusMisusedFlagged++;
      out.push({
        issueType: 'statusColorMisused', severity: 'low', selector: sel(el), bbox: bb(el),
        description: `Destructive/cancel action "${text.slice(0, 30)}" uses green (hue ${Math.round(hsl.h)}°) — green is reserved for success/confirm.`
      });
    }
  }

  // ── 6. Background tone inconsistency across sections ──────────────────
  const sections = [...document.querySelectorAll('main, section, .section, [role="main"], body > div')]
    .filter(visible).slice(0, 8);
  const bgTones = new Map();
  for (const s of sections) {
    const cs = getComputedStyle(s);
    const bg = parseRGB(cs.backgroundColor);
    if (!bg || bg.a < 0.5) continue;
    // Skip pure black / dark surfaces (dark mode)
    if (bg.r < 30 && bg.g < 30 && bg.b < 30) continue;
    // Only flag "near-white" variations (off-white tones)
    if (bg.r > 220 && bg.g > 220 && bg.b > 220 && bg.r < 256) {
      const key = `${bg.r},${bg.g},${bg.b}`;
      bgTones.set(key, (bgTones.get(key) || 0) + 1);
    }
  }
  if (bgTones.size >= 3) {
    out.push({
      issueType: 'themeBgInconsistent', severity: 'low', selector: 'body',
      description: `Page sections use ${bgTones.size} different off-white backgrounds: ${[...bgTones.keys()].slice(0, 4).join(' | ')}. Pick one neutral background tone.`
    });
  }

  return out;
}
```

## Notes

- Bounded: max ~12 findings per cell
- Self-skips: page with no saturated buttons/headers (very plain pages) returns []
- Theme detection: requires 2+ buttons/badges/headers with similar saturated colors to establish a primary
- The `focusRingThemeMismatch` is the EXACT bug from the user's Provinces screenshot — purple focus (~270° hue) on a blue theme (~210° hue), Δ = ~60°
- Cross-origin stylesheets are gracefully skipped via try/catch
