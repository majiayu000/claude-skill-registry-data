---
name: qa-detect-typography-advanced
section: visual
description: "Real typography DEFECTS only (trimmed 2026-06-09 to remove cosmetic/opinion noise): failed web fonts, real WCAG contrast failures, tofu/replacement glyphs, mixed-content (blocked) fonts, and missing/invalid html lang. The ~37 best-practice nitpicks (font-display, preload, baseline-grid, rhythm, payload, widow/measure, px-sizing, etc.) were removed because they are advisories, not bugs."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
---
## What it catches — 5 REAL defect types only

| issueType | severity | What — and why it's a real defect (not an opinion) |
|---|---|---|
| `webFontFailed` | high | A declared `@font-face` file failed to load → users see the wrong (fallback) font. Objectively broken. |
| `contrastFail` | high | Real WCAG 2.1 luminance ratio below 4.5:1 (normal) / 3:1 (large). Measured, not guessed — accessibility failure. |
| `tofuGlyph` | high | Visible `□` / `�` replacement characters rendering on the page (font missing the glyph). Broken text. |
| `mixedContentFont` | high | HTTPS page references an `http://` font URL — the browser BLOCKS it, so the font silently never loads. |
| `missingHtmlLang` | medium | `<html>` has no `lang` — breaks screen-reader pronunciation, hyphenation, and quote glyphs (WCAG 3.1.1). |

**Removed as noise (2026-06-09):** `syntheticWeight`, `noFontDisplay`, `noGenericFallback`, `tooManyFontFamilies`, `missingH1`/`multipleH1` (covered by `qa-detect-a11y` → `noH1`), `headingSkip`, `linkNoDecoration`, `fontSizePxBased`, `allCapsBodyCopy`, `italicOnlyEmphasis`, `invalidHtmlLang`, `deepHeadingHierarchy`, `h2MissingInHierarchy`, `emptyTextElement`, `extremeLetterSpacing`, `wallOfText`, `unstyledPullQuote`, `tooManyFontSizes`, `noFontPreload`, `corsFontPreloadMissing`, `unreadableTextShadow`, `fontPayloadCount`, `fontPayloadHeavy`, `fallbackMetricMismatch`, `fontFileNotSubsetted`, `inconsistentRhythm`, `measureTooLong`, `measureTooShort`, `baselineGridOff`, `widowLine`, `noOpticalSizing`, `variableFont*`, `languageFontMismatch`, `fontDisplayBlock`, `unusedFontWeight`, `iconFontAsWebFont`, `ellipsisNoOverflow`. These are best-practice advisories, not defects — they were flooding the bug tracker with false positives.

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = [];
  const TEXT_SEL = 'p, span, a, li, td, th, label, button, h1, h2, h3, h4, h5, h6, div';
  const sample = [...document.querySelectorAll(TEXT_SEL)]
    .filter(el => el.innerText && el.innerText.trim().length > 5)
    .filter(visible)
    .slice(0, 40);

  // 1. Web font load failures (real: wrong font renders)
  try {
    for (const ff of document.fonts) {
      if (ff.status === 'error') {
        out.push({ issueType:'webFontFailed', severity:'high', selector:`@font-face[${ff.family}]`,
          description:`Web font "${ff.family}" (${ff.weight} ${ff.style}) failed to load — users see a system fallback font instead.` });
      }
    }
  } catch (_) {}

  // 2. Real WCAG contrast ratio (verbatim luminance math — measured, not guessed)
  const lin = c => { c /= 255; return c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
  const lum = (r,g,b) => 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
  const parseRgb = s => { const m = s.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/); return m ? [+m[1], +m[2], +m[3]] : null; };
  // effBg walks ancestors for a SOLID, OPAQUE background color. Crucially, if any ancestor in the
  // chain carries a background-image / gradient (which we cannot read pixel colors from), the real
  // background is INDETERMINATE → return null so the caller SKIPS rather than fabricating white.
  // Returning a hard-coded white fallback was the root cause of the contrast false positives:
  // text over images/gradients/transparent surfaces was measured against an invented white bg.
  const effBg = el => {
    let cur = el;
    while (cur && cur !== document.documentElement) {
      const cs = getComputedStyle(cur);
      // text painted over an image/gradient — can't compute a real ratio, bail as indeterminate.
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const rgb = parseRgb(cs.backgroundColor);
      const am = cs.backgroundColor.match(/rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\)/);
      const alpha = am ? parseFloat(am[1]) : 1;
      if (rgb && alpha > 0.5) return rgb;
      cur = cur.parentElement;
    }
    // reached the root with no solid bg found — check the root itself, else indeterminate.
    const rootCs = getComputedStyle(document.documentElement);
    if (rootCs.backgroundImage && rootCs.backgroundImage !== 'none') return null;
    const rootRgb = parseRgb(rootCs.backgroundColor);
    if (rootRgb) return rootRgb;
    const bodyRgb = document.body ? parseRgb(getComputedStyle(document.body).backgroundColor) : null;
    return bodyRgb || null;   // null === indeterminate → skip, never fabricate white
  };
  // WCAG 1.4.3 exempts disabled controls and pure-decorative text. A placeholder is allowed to be
  // low-contrast (it's a hint, not content). Detect these and skip.
  const isExempt = el => {
    if (el.disabled) return true;
    if (el.closest && el.closest('[disabled], [aria-disabled="true"], fieldset:disabled')) return true;
    const cs = getComputedStyle(el);
    if (cs.cursor === 'not-allowed') return true;
    if (cs.pointerEvents === 'none') return true;   // decorative / non-interactive overlay text
    if (cs.userSelect === 'none' && el.getAttribute('aria-hidden') === 'true') return true;
    if (el.getAttribute('aria-hidden') === 'true') return true;  // decorative, not announced
    return false;
  };
  let cFails = 0;
  for (const el of sample) {
    if (cFails >= 5) break;
    if (el.children.length > 0) continue;          // leaf text only
    if (isExempt(el)) continue;                    // WCAG: disabled / decorative text exempt
    const txt = (el.innerText || '').trim();
    if (txt.length < 3) continue;
    const cs = getComputedStyle(el);
    // skip effectively-invisible text (already covered by visibility filter, but guard opacity/clip).
    if (+cs.opacity < 0.1) continue;
    const fg = parseRgb(cs.color);
    if (!fg) continue;
    // foreground alpha < 1 (e.g. rgba(...,0.4)) means semi-transparent text composited over an
    // unknown surface — ratio isn't reliably computable, skip rather than over-report.
    const fgAlpha = (cs.color.match(/rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\)/) || [])[1];
    if (fgAlpha !== undefined && parseFloat(fgAlpha) < 0.9) continue;
    const bg = effBg(el);
    // INDETERMINATE background (image/gradient/transparent-to-root) → cannot compute a real ratio.
    // Skip, never fabricate a white background. This kills the "white-on-image" false positives.
    if (!bg) continue;
    // belt-and-suspenders: exact fg===bg means the bg resolution collapsed — skip the artifact.
    if (fg[0] === bg[0] && fg[1] === bg[1] && fg[2] === bg[2]) continue;
    const L1 = lum(...fg), L2 = lum(...bg);
    const ratio = (Math.max(L1,L2)+0.05) / (Math.min(L1,L2)+0.05);
    const fs = parseFloat(cs.fontSize) || 16;
    const bold = (parseInt(cs.fontWeight) || 400) >= 700;
    const isLarge = fs >= 24 || (fs >= 18.66 && bold);
    const min = isLarge ? 3.0 : 4.5;
    if (ratio < min) {
      cFails++;
      out.push({ issueType:'contrastFail', severity:'high', selector:sel(el), bbox:bb(el),
        description:`WCAG contrast ${ratio.toFixed(2)}:1 is below the ${min}:1 minimum for ${isLarge?'large':'normal'} text "${txt.slice(0,40)}". color=${cs.color} bg=rgb(${bg.join(',')}).` });
    }
  }

  // 3. Tofu / replacement glyphs (real: broken text)
  let tofu = 0;
  for (const el of sample) {
    if (tofu >= 3) break;
    if (el.children.length > 0) continue;
    const txt = el.innerText || '';
    if (/[�□]/.test(txt) || / ?\uE0[0-9A-F]{2}/.test(txt)) {
      tofu++;
      out.push({ issueType:'tofuGlyph', severity:'high', selector:sel(el), bbox:bb(el),
        description:`Replacement / tofu glyph (□ or �) rendering in "${txt.replace(/[�□]/g,'[?]').slice(0,40)}" — the font is missing this character.` });
    }
  }

  // 4. Mixed-content fonts (real: browser blocks the font on HTTPS)
  if (location.protocol === 'https:') {
    let mixed = 0;
    for (const sheet of document.styleSheets) {
      if (mixed >= 2) break;
      let rules; try { rules = sheet.cssRules; } catch (_) { continue; }
      if (!rules) continue;
      for (const r of rules) {
        if (mixed >= 2) break;
        if (r.type === CSSRule.FONT_FACE_RULE && r.style) {
          const src = r.style.getPropertyValue('src') || '';
          if (/url\(\s*['"]?http:\/\//i.test(src)) {
            mixed++;
            out.push({ issueType:'mixedContentFont', severity:'high', selector:'@font-face',
              description:`@font-face on this HTTPS page references an http:// font URL — the browser blocks it, so the font never loads.` });
          }
        }
      }
    }
  }

  // 5. Missing html lang (real: a11y — pronunciation/hyphenation)
  const htmlLang = document.documentElement.getAttribute('lang');
  if (!htmlLang || !htmlLang.trim()) {
    out.push({ issueType:'missingHtmlLang', severity:'medium', selector:'html',
      description:`<html> has no lang attribute — screen readers can't pick the right voice, and hyphenation/quote glyphs break (WCAG 3.1.1).` });
  }

  return out;
}
```

## Notes

- **Trimmed 2026-06-09** from 43 → 5 issue types. Every remaining type is an objective, measurable defect, not a best-practice opinion.
- Bounded: ≤5 contrast + ≤3 tofu + ≤2 mixed-content + webfont + lang = max ~12 findings/cell.
- Self-skips: a page with no text returns `[]`.
- Contrast uses real relative-luminance math (WCAG 2.1), resolving the effective background up the ancestor chain.
