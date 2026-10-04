---
name: qa-detect-typography
section: visual
description: "Detects small fonts, tight line-height, clipped text, oversized headings on mobile, and unbreakable long words causing overflow"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it checks
- `smallFont` — font-size < 10px (genuinely too small). NOTE: WCAG has NO minimum font size; 10–11px secondary text (table cells, captions, labels) is normal and readable, so it is NOT flagged. Only < 10px — which is hard to read for most users — is reported, at LOW severity (advisory, not a WCAG violation).
- `tightLineHeight` — line-height / font-size < 1.2 (and font >= 10px)
- `textClipped` — element with overflow:hidden where scrollHeight > clientHeight + 4
- `oversizedHeading` — H1/H2 font-size > 36px on mobile (≤768px viewport)
- `longWordNoBreak` — leaf text element with word ≥25 chars causing overflow, without word-break/overflow-wrap

## Probe (browser_evaluate)
```js
() => {
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0,120);
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const vw = innerWidth;
  const isMobile = vw <= 768;
  const q = 'p,span,a,li,td,th,label,button,h1,h2,h3,h4,h5,h6,div';

  for (const el of document.querySelectorAll(q)) {
    if (out.length >= 20) break;
    if (!el.innerText || !el.innerText.trim()) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const s = getComputedStyle(el);
    const fs = parseFloat(s.fontSize);
    const lh = parseFloat(s.lineHeight);

    // Structural exemption: icon-font glyphs (Material Icons / FontAwesome — the "text" is a
    // ligature rendered as an icon) and aria-hidden decorative text are NOT readable content.
    // Flagging them as "small font" is a false positive regardless of px. Skip them.
    const fam = (s.fontFamily || '').toLowerCase();
    const decorative = el.getAttribute('aria-hidden') === 'true'
      || /icon|material|fontawesome|fa-|glyph/.test(fam);

    // 1. smallFont — WCAG has NO minimum font size. 10-11px is normal, readable secondary text.
    //    Only flag < 10px (genuinely too small) on REAL readable text, at LOW severity (advisory).
    if (!decorative && fs < 10) {
      out.push({ issueType:'smallFont', severity:'low', selector:sel(el),
        description:`Text on ${sel(el)} is ${fs}px — below 10px is hard to read for most users (advisory; not a WCAG minimum).`, bbox: bb(el) });
    } else if (lh && lh/fs < 1.2
               // line-height ONLY matters when text WRAPS to 2+ lines. A single-line element
               // (button, label, icon, the "···" kebab menu, table cell, badge) has no line
               // below to crowd, so a tight ratio is harmless — do NOT flag it.
               && el.clientHeight >= lh * 1.8                                   // renders as ≥ ~2 lines (actually wraps)
               && !el.closest('button, a, label, th, summary, [role="button"], [role="menuitem"], [role="tab"], [contenteditable], [class*="btn"], [class*="badge"], [class*="chip"], [class*="tag"], [class*="icon"], [class*="action"], [class*="kebab"], [class*="menu"]')
               && !/^H[1-6]$/.test(el.tagName)                                  // headings use tight line-height by design
               && getComputedStyle(el).cursor !== 'pointer'                     // clickable controls aren't body text
               && (el.innerText || '').trim().split(/\s+/).length >= 8) {        // a real sentence, not a 1–3 word label/glyph
      // 2. tightLineHeight — multi-line body/paragraph text only (single-line UI is exempt)
      out.push({ issueType:'tightLineHeight', severity:'low', selector:sel(el),
        description:`Typography issue on ${sel(el)}: line-height/font-size = ${(lh/fs).toFixed(2)} < 1.2 on multi-line text`, bbox: bb(el) });
    }

    // 3. textClipped — actual text being cut, not just container overflow.
    //    Real clip patterns:
    //      a) horizontal: white-space:nowrap + text-overflow:ellipsis|clip
    //         AND scrollWidth > clientWidth (text wider than container).
    //      b) vertical:   -webkit-line-clamp: N AND scrollHeight > clientHeight
    //         (text has more lines than allowed).
    //    Skip containers (any element with non-inline element children) — overflow on
    //    containers is layout overflow (sidebar menu, card stack, toast animation),
    //    NOT text being cut. Also skip <div> unless its only children are inline
    //    formatting elements (span/b/i/em/strong/u/sup/sub/br/mark/code/small).
    const INLINE_OK = new Set(['SPAN','I','EM','STRONG','B','U','SUP','SUB','BR','MARK','CODE','SMALL','A','LABEL']);
    const isTextLeaf = el.children.length === 0 ||
      [...el.children].every(c => INLINE_OK.has(c.tagName));
    const isDivContainer = el.tagName === 'DIV' && !isTextLeaf;
    if (isTextLeaf && !isDivContainer) {
      const ws = s.whiteSpace;
      const to = s.textOverflow;
      const ovf = s.overflow;
      // (a) horizontal ellipsis/clip
      const horizCss = (ws === 'nowrap') && (to === 'ellipsis' || to === 'clip') &&
                       (ovf === 'hidden' || ovf === 'clip');
      const horizClipped = horizCss && el.scrollWidth > el.clientWidth + 2;
      // (b) vertical line-clamp
      const clampN = parseInt(s.webkitLineClamp || s.lineClamp || '0', 10) || 0;
      const vertCss = clampN > 0 && (ovf === 'hidden' || ovf === 'clip');
      const vertClipped = vertCss && el.scrollHeight > el.clientHeight + 2;
      if (horizClipped || vertClipped) {
        const dir = horizClipped ? 'horizontally' : `to ${clampN} line(s)`;
        out.push({ issueType:'textClipped', severity:'low', selector:sel(el),
          description:`Text in ${sel(el)} is clipped ${dir} (content ${horizClipped ? `${el.scrollWidth}px wide vs ${el.clientWidth}px container` : `${el.scrollHeight}px tall vs ${el.clientHeight}px container`}). If this is intentional truncation, add a title attribute so the full text is reachable on hover.`,
          bbox: bb(el) });
      }
    }

    // 4. oversizedHeading — H1/H2 with fontSize > 36px on mobile
    if (isMobile && (el.tagName === 'H1' || el.tagName === 'H2') && fs > 36) {
      out.push({ issueType:'oversizedHeading', severity:'medium', selector:sel(el),
        description:`${el.tagName} font-size ${fs}px exceeds 36px on mobile (viewport=${vw}px)`, bbox: bb(el) });
    }

    // 5. longWordNoBreak — leaf elements with a very long word that ACTUALLY
    //    overflows its container. A long word that fits (there's room, or it wraps,
    //    or the container scrolls) is NOT a defect, so we require the word's own
    //    rendered width to exceed the element's content box. We also:
    //      - require the element to be genuinely visible (not hidden/offscreen),
    //      - exempt code/pre/<a> URL displays and elements that opt into horizontal
    //        scrolling (overflow-x:auto|scroll) — breaking there would be WRONG.
    if (el.children.length === 0) {
      const text = el.innerText || '';
      const words = text.split(/\s+/);
      const longWord = words.find(w => w.length >= 25);
      // visibility: must be on-screen and not visibility:hidden / opacity:0
      const visible = r.width > 1 && r.height > 1 &&
        s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.01 &&
        r.bottom > 0 && r.right > 0 && r.top < innerHeight && r.left < vw;
      // exemptions: code/pre/URL-display elements, and containers that opt into
      // horizontal scrolling (the long word is meant to scroll, not break).
      const tag = el.tagName;
      const inCodeOrPre = tag === 'CODE' || tag === 'PRE' ||
        !!el.closest('code,pre,kbd,samp,[class*="code" i],[class*="mono" i],[class*="url" i],[class*="hash" i],[class*="token" i]');
      const scrolls = s.overflowX === 'auto' || s.overflowX === 'scroll' ||
        s.overflow === 'auto' || s.overflow === 'scroll';
      if (longWord && visible && !inCodeOrPre && !scrolls) {
        const wb = s.wordBreak;
        const ow = s.overflowWrap || s.wordWrap;
        const allowsBreak = wb === 'break-all' || wb === 'break-word' ||
          ow === 'anywhere' || ow === 'break-word';
        if (!allowsBreak) {
          // Measure the long word's actual rendered width and compare to the
          // element's CONTENT box width (clientWidth minus horizontal padding).
          let wordW = 0;
          try {
            const cv = document.createElement('canvas').getContext('2d');
            cv.font = `${s.fontStyle} ${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
            wordW = cv.measureText(longWord).width;
          } catch (_) {}
          const padL = parseFloat(s.paddingLeft) || 0;
          const padR = parseFloat(s.paddingRight) || 0;
          const contentW = el.clientWidth - padL - padR;
          // REQUIRE real overflow: element actually scrolls horizontally AND the
          // single long word is wider than the content box (so the word — not some
          // sibling/padding — is what overflows). 4px tolerance for sub-pixel rounding.
          const elOverflows = el.scrollWidth > el.clientWidth + 4;
          const wordOverflows = wordW > contentW + 4;
          if (elOverflows && wordOverflows && contentW > 0) {
            out.push({ issueType:'longWordNoBreak', severity:'medium', selector:sel(el),
              description:`Long word "${longWord.slice(0,30)}${longWord.length>30?'…':''}" (${longWord.length} chars, ~${Math.round(wordW)}px) overflows its ${Math.round(contentW)}px container with no word-break/overflow-wrap set`, bbox: bb(el) });
          }
        }
      }
    }
  }

  // 6. allCapsMicroLabel — ALL CAPS text at very small size (≤13px).
  // Double readability penalty: all-caps removes ascender/descender variation AND
  // tiny size reduces legibility. Common pattern in stat card labels: "TOTAL STUDENTS".
  for (const el of document.querySelectorAll('span,p,label,div,h1,h2,h3,h4,h5,h6')) {
    if (out.length >= 20) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const text = (el.innerText || '').trim();
    if (text.length < 3 || text.length > 60) continue;
    const s = getComputedStyle(el);
    const fs = parseFloat(s.fontSize);
    if (fs > 13) continue;
    const isUpperTransform = s.textTransform === 'uppercase';
    const isAllCapsText = text === text.toUpperCase() && /[A-Z]/.test(text);
    if (isUpperTransform || isAllCapsText) {
      out.push({ issueType:'allCapsMicroLabel', severity:'medium', selector:sel(el),
        description:`All-caps label "${text.slice(0,30)}" at ${fs}px — both small font and all-caps hurt readability. Use normal-case with font-weight:600 instead of all-caps, or increase font-size to ≥14px.`,
        bbox: bb(el) });
    }
  }

  // 7. metaLabelLowContrast — meta/sync/timestamp text that is both small AND light-colored.
  // "Last synced: 8h ago" style labels tell users if data is stale — if styled with
  // light gray at 10–11px they become nearly invisible on white backgrounds.
  const META_PATTERN = /\b(sync(ed?|ing)?|last\s+(sync|update|refresh)|ago|updated?|refresh(ed)?|stale|live|online|offline)\b/i;
  for (const el of document.querySelectorAll('span,p,small,div,label')) {
    if (out.length >= 20) break;
    const text = (el.innerText || '').trim();
    if (!META_PATTERN.test(text) || text.length > 80) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const s = getComputedStyle(el);
    const fs = parseFloat(s.fontSize);
    if (fs > 13) continue;
    const cm = (s.color || '').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (cm) {
      const lum = (0.299 * +cm[1] + 0.587 * +cm[2] + 0.114 * +cm[3]) / 255;
      if (lum > 0.55) {
        out.push({ issueType:'metaLabelLowContrast', severity:'medium', selector:sel(el),
          description:`Meta/sync label "${text.slice(0,40)}" is ${fs}px with light color (luminance ${lum.toFixed(2)}) — low contrast on white background. Increase font-size or darken text color for readability.`,
          bbox: bb(el) });
      }
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| smallFont | medium | "Typography issue on {sel}: {fontSize}px < 12px" |
| tightLineHeight | low | "Typography issue on {sel}: line-height/font-size = {ratio} < 1.2" |
| textClipped | low | "Typography issue on {sel}: Text clipped by overflow:hidden" |
| oversizedHeading | medium | "{tag} font-size {fs}px exceeds 36px on mobile" |
| longWordNoBreak | medium | "Long word ({n} chars) overflows container, no word-break/overflow-wrap" |
| allCapsMicroLabel | medium | "All-caps label '{text}' at {fs}px — both small size and all-caps hurt readability" |
| metaLabelLowContrast | medium | "Meta/sync label '{text}' is {fs}px with light color (luminance {n}) — low contrast on white background" |
