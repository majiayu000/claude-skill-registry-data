---
name: qa-detect-reflow
section: responsiveness
description: "WCAG 1.4.10 — detects content that requires horizontal scroll at 320px, fixed-width elements, non-shrinking tables, and oversized images. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: [mobile]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with a `browser_resize` + separate scan. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

WCAG 1.4.10 (Reflow) requires content to be presentable at 320 CSS pixels wide without horizontal scrolling. This skill is `applyOn: [mobile]`, so it already runs on a small viewport. Rather than do a real `browser_resize(320, 568)` (a costly extra round-trip that perturbs every later skill in the cell), the probe measures everything against the **320px reflow threshold in-page**: it flags fixed-width / non-shrinking / oversized elements whose geometry would force horizontal scroll at 320px, plus any actual page-level horizontal scroll at the current mobile width. It returns `findings[]` in one round-trip and changes no DOM/viewport state. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const out = [];
  const VP = 320; // WCAG 1.4.10 reflow threshold
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // 1. Page-level horizontal scroll — primary reflow violation.
  //    Flag if the document already overflows the current (mobile) viewport,
  //    OR if its content box is wider than the 320px reflow threshold.
  const docW = document.documentElement.scrollWidth;
  if (docW > Math.max(VP, window.innerWidth) + 2) {
    out.push({ skill: 'qa-detect-reflow', issueType: 'reflowHorizontalScroll', severity: 'high', selector: 'html',
      description: `Page content is ${docW}px wide and exceeds the 320px reflow threshold — requires horizontal scroll at 320px viewport (WCAG 1.4.10 Reflow violation)`,
      bbox: { x: 0, y: 0, w: Math.min(320, window.innerWidth), h: Math.min(80, window.innerHeight) } });
  }

  // 2. Tables that won't fit 320px (fixed/non-shrinking content wider than 320)
  for (const tbl of document.querySelectorAll('table')) {
    if (out.length >= 15) break;
    const r = tbl.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (tbl.scrollWidth > VP + 2) {
      out.push({ skill: 'qa-detect-reflow', issueType: 'tableNotResponsive', severity: 'high', selector: sel(tbl),
        description: `Table ${sel(tbl)} has ${Math.round(tbl.scrollWidth)}px of content and won't fit a 320px viewport — wrap in overflow-x:auto container or use stacked-row pattern`,
        bbox: bb(tbl) });
    }
  }

  // 3. Images that exceed 320px without a responsive max-width (likely missing max-width:100%)
  for (const img of document.querySelectorAll('img')) {
    if (out.length >= 15) break;
    const r = img.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const natural = img.naturalWidth || 0;
    const effWidth = Math.max(r.width, natural);
    if (effWidth > VP + 2) {
      const style = getComputedStyle(img);
      const responsive = style.maxWidth === '100%' || style.maxWidth.includes('%') || style.width.includes('%');
      if (!responsive) {
        out.push({ skill: 'qa-detect-reflow', issueType: 'imageNotResponsive', severity: 'medium', selector: sel(img),
          description: `Image ${sel(img)} is ${Math.round(effWidth)}px and lacks a relative max-width — overflows a 320px viewport. Add max-width:100% or use srcset/picture`,
          bbox: bb(img) });
      }
    }
  }

  // 4. Block elements with an AUTHOR-SET fixed px width that ACTUALLY overflows.
  //
  //    ROOT-CAUSE FIX: getComputedStyle(el).width returns the *resolved used*
  //    width in px for EVERY block element, so `width:100%` on a 360px viewport
  //    reports "360px" — endsWith('px') does NOT mean the author set a fixed
  //    width. We must read the element's OWN inline/declared width and confirm
  //    it is a non-relative px (or absolute) value, AND that it does not shrink
  //    (max-width that caps it), AND that it actually causes horizontal overflow
  //    the user hits, AND that it is rendered (not in a closed drawer), AND that
  //    it is not inside an intentionally horizontally-scrollable container.
  const REL = /(%|vw|vmin|vmax|auto|calc)/i;       // relative/fluid → not a fixed-width defect
  const isRenderedR = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || s.visibility === 'collapse') return false;
    if (parseFloat(s.opacity || '1') === 0) return false;
    if (el.closest('[aria-hidden="true"],[hidden],[inert]')) return false;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    if (r.right <= 0 || r.bottom <= 0) return false;   // off-canvas (closed drawer)
    return true;
  };
  // True if el sits inside a container that scrolls horizontally on purpose.
  const inScrollContainer = (el) => {
    let p = el.parentElement;
    while (p && p !== document.documentElement) {
      const ox = getComputedStyle(p).overflowX;
      if (ox === 'auto' || ox === 'scroll') return true;
      p = p.parentElement;
    }
    return false;
  };
  const blockTags = ['div', 'section', 'article', 'header', 'footer', 'main', 'nav', 'aside', 'form', 'fieldset'];
  for (const el of document.querySelectorAll(blockTags.join(','))) {
    if (out.length >= 20) break;
    const style = getComputedStyle(el);

    // (a) Author actually declared a fixed, non-relative width.
    //     Prefer the inline style; fall back to the cascaded declaration only
    //     when it is clearly a fixed px (not a resolved % / auto / calc).
    const declared = (el.style && el.style.width) ? el.style.width : '';
    const minW = style.minWidth || '';
    let fixedPx = 0;
    if (declared && declared.endsWith('px') && !REL.test(declared)) {
      fixedPx = parseFloat(declared);
    } else if (minW.endsWith('px') && !REL.test(minW) && parseFloat(minW) > VP + 2) {
      // A min-width larger than the reflow threshold also prevents shrinking.
      fixedPx = parseFloat(minW);
    }
    if (!fixedPx || fixedPx <= VP + 2) continue;

    // (b) A max-width that caps the element at/under 320px means it DOES shrink → not a defect.
    const maxW = style.maxWidth || '';
    if (maxW && maxW !== 'none' && (maxW.includes('%') || (maxW.endsWith('px') && parseFloat(maxW) <= VP + 2))) continue;

    // (c) Must be visible to a real user.
    if (!isRenderedR(el)) continue;

    // (d) Must ACTUALLY cause horizontal overflow the user hits: its right edge
    //     extends past the current viewport, OR its used width still exceeds 320px
    //     AND the page itself overflows horizontally.
    const r = el.getBoundingClientRect();
    const overflowsViewport = r.right > window.innerWidth + 2;
    const widerThanReflow = r.width > VP + 2 && document.documentElement.scrollWidth > window.innerWidth + 2;
    if (!overflowsViewport && !widerThanReflow) continue;

    // (e) Exempt content inside an intentionally horizontal-scroll container.
    if (inScrollContainer(el)) continue;

    out.push({ skill: 'qa-detect-reflow', issueType: 'fixedWidthOverflow', severity: 'medium', selector: sel(el),
      description: `Element ${sel(el)} has an author-set fixed width (${declared || minW}) of ${Math.round(fixedPx)}px exceeding the 320px reflow threshold and overflows the viewport — convert to %, rem, em, or use max-width`,
      bbox: bb(el) });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| reflowHorizontalScroll | high | "Page requires horizontal scroll at 320px width — WCAG 1.4.10 violation" |
| tableNotResponsive | high | "Table {selector} overflows 320px viewport — wrap in overflow-x:auto or use stacked rows" |
| imageNotResponsive | medium | "Image {selector} too wide at 320px — add max-width:100% or srcset" |
| fixedWidthOverflow | medium | "Element {selector} has fixed px width exceeding 320px — use relative units" |

## Notes on this conversion
- The old `captureOriginalSize → browser_resize(320) → scanReflow → browser_resize(restore)` flow is folded into ONE async `browser_evaluate` call. Per the conversion brief, reflow is measured against the 320px threshold **in-page using the existing (mobile) viewport** rather than doing a real resize — checking fixed-width / non-shrinking / oversized geometry that would force horizontal scroll at 320px. Same issueTypes.
- `applyOn: [mobile]` — runs only on the mobile viewport cell. No viewport state is changed, so it does not perturb downstream skills.
- The orchestrator already has native-viewport overflow detection via `qa-detect-overflow`; this skill is specifically the 320px reflow gate.
