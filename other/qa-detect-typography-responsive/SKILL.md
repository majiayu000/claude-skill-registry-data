---
name: qa-detect-typography-responsive
section: visual
description: "Closes the responsive/legibility typography gaps not covered by qa-detect-typography(-advanced): font appropriateness per viewport, fluid (clamp/vw) type scaling, justified-without-hyphens rivers, text over background images without a scrim, px sizing that ignores user font-size preference, and missing tabular figures in numeric tables."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

# qa-detect-typography-responsive

## What it checks (the gaps the other two typography skills don't)
| issueType | severity | what it catches |
|---|---|---|
| `bodyTextTooSmallForViewport` | medium | Body/paragraph text < 15px on mobile/tablet (≤1024px) — cramped reading; <16px also triggers iOS focus-zoom |
| `justifiedNoHyphens` | low | `text-align: justify` without `hyphens: auto` → uneven spacing ("rivers"), worst in narrow columns |
| `textOverImageNoScrim` | medium | Text over a background image with no `text-shadow` and no overlay/scrim → legibility depends on the photo (judgment → escalates) |
| `noFluidType` | low | No font-size rule uses `clamp()`/`vw` → type is fixed-step across breakpoints, never scales smoothly (judgment → escalates) |
| `pxFontSizingDominant` | low | Page-wide font sizes are mostly `px` (not `rem`) → text won't grow when a user raises their browser default size (WCAG 1.4.4) |
| `tabularFiguresMissing` | low | Numeric table columns lack `font-variant-numeric: tabular-nums` → digits misalign (judgment → escalates) |

Ownership: this skill OWNS these 6 issue types; the other typography skills own size/line-height/font-loading/contrast/hierarchy. No overlap.

This is a `viewportSensitive` skill — `bodyTextTooSmallForViewport` is judged at each viewport; the static checks self-dedup across viewports (Step 5.4 dedup). Deterministic asserts run on Haiku; the three judgment-y types set `uncertain: true` so the orchestrator escalates only those to Sonnet (`escalation_model`).

## Self-skip
Skip if the page has fewer than 2 paragraphs of real text AND no `<table>` (nothing to assess).

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const vw = innerWidth;
  const isMobile = vw <= 768;
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };

  const paras = [...document.querySelectorAll('p, li, td')]
    .filter(el => el.innerText && el.innerText.trim().length > 30 && vis(el)).slice(0, 30);

  // 1. body text too small for mobile/tablet readability
  if (vw <= 1024) {
    for (const el of paras.slice(0, 8)) {
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs && fs < 15) {
        out.push({ issueType: 'bodyTextTooSmallForViewport', severity: 'medium', selector: sel(el),
          description: `Body text is ${fs}px at ${vw}px viewport — below the ~16px comfortable reading size for ${isMobile ? 'mobile' : 'tablet'}.`, bbox: bb(el) });
        break;
      }
    }
  }

  // 2. justified without hyphenation
  for (const el of paras) {
    const cs = getComputedStyle(el);
    if (cs.textAlign === 'justify' && (cs.hyphens || cs.webkitHyphens) !== 'auto') {
      out.push({ issueType: 'justifiedNoHyphens', severity: 'low', selector: sel(el),
        description: `Justified text without hyphens:auto — produces uneven word spacing ("rivers"), worst on narrow columns. Add hyphens:auto (and lang on <html>).`, bbox: bb(el) });
      break;
    }
  }

  // 3. text over a background image with no shadow/overlay
  for (const el of paras.slice(0, 12)) {
    const cs = getComputedStyle(el);
    const bg = cs.backgroundColor;
    if (!(bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')) continue;
    if (cs.textShadow && cs.textShadow !== 'none') continue;
    let p = el.parentElement, depth = 0, imgBg = false;
    while (p && depth < 5) {
      if ((getComputedStyle(p).backgroundImage || '').includes('url(')) { imgBg = true; break; }
      p = p.parentElement; depth++;
    }
    if (imgBg) {
      out.push({ issueType: 'textOverImageNoScrim', severity: 'medium', selector: sel(el), uncertain: true,
        description: `Text sits over a background image with no text-shadow or overlay/scrim — legibility depends on the image and can fail. Add a semi-opaque overlay or text-shadow.`, bbox: bb(el) });
      break;
    }
  }

  // 4 & 5. stylesheet scan: fluid type + px dominance
  let usesFluid = false, pxRules = 0, remRules = 0;
  try {
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch { continue; }
      if (!rules) continue;
      for (const rule of rules) {
        const v = (rule.style && rule.style.fontSize) ? rule.style.fontSize.trim() : '';
        if (!v) continue;
        if (/clamp\(|\dvw|\dvmin|\dvmax/.test(v)) usesFluid = true;
        if (/\d(px)$/.test(v)) pxRules++;
        else if (/\d(rem|em)$/.test(v)) remRules++;
      }
    }
  } catch (_) {}
  if (!usesFluid && (pxRules + remRules) > 5) {
    out.push({ issueType: 'noFluidType', severity: 'low', selector: 'stylesheet', uncertain: true,
      description: `No font-size uses clamp()/vw — type is fixed-step across breakpoints (no smooth fluid scaling). Consider clamp() for headings.` });
  }
  if (pxRules >= 5 && pxRules >= remRules * 2) {
    out.push({ issueType: 'pxFontSizingDominant', severity: 'low', selector: 'stylesheet',
      description: `${pxRules} font-size rules use px vs ${remRules} rem/em — px text won't scale when a user raises their browser's default font size (WCAG 1.4.4). Prefer rem.` });
  }

  // 6. tabular figures missing in numeric tables
  for (const table of [...document.querySelectorAll('table')].slice(0, 5)) {
    const numCells = [...table.querySelectorAll('td')]
      .filter(td => /^[\s$€£¥]*[\d][\d,.\-%\s]*$/.test((td.innerText || '').trim())).slice(0, 12);
    if (numCells.length >= 4 && !/tabular-nums/.test(getComputedStyle(numCells[0]).fontVariantNumeric || '')) {
      out.push({ issueType: 'tabularFiguresMissing', severity: 'low', selector: sel(table), uncertain: true,
        description: `Numeric columns don't use font-variant-numeric: tabular-nums — digits have uneven widths so numbers don't right-align cleanly.`, bbox: bb(table) });
      break;
    }
  }

  return out;
}
```

## Notes
- `textOverImageNoScrim`, `noFluidType`, `tabularFiguresMissing` carry `uncertain: true` — they're heuristics, so only those escalate to Sonnet for a yes/no, keeping cost low.
- Orphan detection (a heading/line stranded at the bottom of a column) is intentionally NOT included — it needs render-flow context that a static probe can't judge reliably without false positives.
- `bodyTextTooSmallForViewport` self-gates to ≤1024px so it never fires on desktop.
