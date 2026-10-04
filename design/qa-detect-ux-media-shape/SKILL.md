---
name: qa-detect-ux-media-shape
section: visual
description: "Detects inconsistencies in image/avatar/media visuals on the same page: avatars mixing circle / square / rounded shapes, images in same grid with different aspect ratios (16:9 + 4:3 + square), some images bordered/shadowed and others not, logo rendered at different sizes across the page."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasImages, hasVideo, hasAvatars]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `avatarShapeMixed` | medium | Avatars on same page use 2+ shapes (circle, square, rounded) — pick one |
| `avatarSizeInconsistent` | low | Avatars in the same context (header, list row, comment thread) have widths/heights differing by > 20% |
| `imageAspectRatioMixed` | low | 3+ images in same grid/list have noticeably different aspect ratios (cropped vs full vs squished) |
| `imageDecorationMixed` | low | Some images bordered/shadowed, others not — inconsistent visual treatment in same group |
| `logoSizeInconsistent` | low | Same logo (identical `src`) rendered at noticeably different sizes (> 20% delta) in different page locations |
| `imageWithoutDimension` | low | `<img>` with no explicit `width`/`height` attributes (or `aspect-ratio` CSS) — causes layout shift when loading |

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

  // ── 1 + 2. Avatars ─────────────────────────────────────────────────
  const avatars = [...document.querySelectorAll(
    '.avatar, [class*="avatar"], .profile-pic, [class*="profile-pic"], [class*="user-pic"], [aria-label*="avatar" i], img[class*="rounded-circle"], img[class*="avatar"]'
  )].filter(visible);

  if (avatars.length >= 2) {
    const shapes = avatars.map(a => {
      const cs = getComputedStyle(a);
      const r = a.getBoundingClientRect();
      const radius = parseFloat(cs.borderTopLeftRadius) || 0;
      const minDim = Math.min(r.width, r.height);
      let shape = 'rect';
      if (radius >= minDim / 2 - 1) shape = 'circle';
      else if (radius > 8) shape = 'rounded';
      return { el: a, shape, width: r.width, height: r.height };
    });
    const shapeSet = new Set(shapes.map(s => s.shape));
    if (shapeSet.size >= 2) {
      const counts = {};
      for (const s of shapes) counts[s.shape] = (counts[s.shape] || 0) + 1;
      out.push({
        issueType: 'avatarShapeMixed', severity: 'medium', selector: 'body',
        description: `Page mixes avatar shapes: ${Object.entries(counts).map(([k,v]) => `${v} ${k}`).join(', ')}. Pick ONE shape (circle is the strongest convention).`
      });
    }
    // Size variance
    const widths = shapes.map(s => s.width);
    const wDelta = Math.max(...widths) - Math.min(...widths);
    if (widths.length >= 3 && wDelta > Math.max(...widths) * 0.2 && wDelta > 6) {
      out.push({
        issueType: 'avatarSizeInconsistent', severity: 'low', selector: 'body',
        description: `Avatars rendered at sizes ${Math.round(Math.min(...widths))}-${Math.round(Math.max(...widths))}px (${Math.round(wDelta/Math.max(...widths)*100)}% variance). Use 2-3 fixed avatar sizes (e.g. 24/32/48px).`
      });
    }
  }

  // ── 3. Image aspect ratio mix in same grid ────────────────────────
  const grids = [...document.querySelectorAll('.grid, [class*="grid"], .image-grid, .gallery, [class*="gallery"], .card-grid, .row')].filter(visible);
  let arFlagged = 0;
  for (const grid of grids) {
    if (arFlagged >= 2) break;
    const imgs = [...grid.querySelectorAll('img')].filter(visible).filter(i => {
      const r = i.getBoundingClientRect();
      return r.width > 50 && r.height > 50;
    });
    if (imgs.length < 3) continue;
    const ratios = imgs.map(i => {
      const r = i.getBoundingClientRect();
      return Math.round((r.width / r.height) * 100) / 100;
    });
    const bins = new Set();
    for (const r of ratios) {
      let bucket = 'other';
      if (Math.abs(r - 1) < 0.1) bucket = 'square';
      else if (r >= 1.3 && r <= 1.4) bucket = '4:3';
      else if (r >= 1.7 && r <= 1.8) bucket = '16:9';
      else if (r >= 0.55 && r <= 0.65) bucket = '9:16';
      else if (r >= 1.45 && r <= 1.55) bucket = '3:2';
      else bucket = `~${r}`;
      bins.add(bucket);
    }
    if (bins.size >= 3) {
      arFlagged++;
      out.push({
        issueType: 'imageAspectRatioMixed', severity: 'low',
        selector: sel(grid), bbox: bb(grid),
        description: `Grid has ${imgs.length} images with ${bins.size} distinct aspect ratios: ${[...bins].slice(0, 4).join(', ')}. Use object-fit:cover + one fixed aspect-ratio for uniform look.`
      });
    }
  }

  // ── 4. Image decoration mix (border/shadow) ──────────────────────
  let decFlagged = 0;
  for (const grid of grids) {
    if (decFlagged >= 1) break;
    const imgs = [...grid.querySelectorAll('img')].filter(visible);
    if (imgs.length < 3) continue;
    let bordered = 0, shadowed = 0, plain = 0;
    for (const i of imgs) {
      const cs = getComputedStyle(i);
      const hasBorder = parseFloat(cs.borderTopWidth) > 0 && cs.borderTopColor !== 'rgba(0, 0, 0, 0)';
      const hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
      if (hasBorder) bordered++;
      else if (hasShadow) shadowed++;
      else plain++;
    }
    const distinctTreatments = [bordered, shadowed, plain].filter(n => n > 0).length;
    if (distinctTreatments >= 2 && (bordered + shadowed + plain) >= 3) {
      decFlagged++;
      out.push({
        issueType: 'imageDecorationMixed', severity: 'low',
        selector: sel(grid), bbox: bb(grid),
        description: `Grid mixes image treatments: ${bordered} bordered, ${shadowed} shadowed, ${plain} plain. Apply one decoration to all images in the group.`
      });
    }
  }

  // ── 5. Logo size inconsistency (same src, different size) ────────
  const imgGroups = new Map();   // src → [el, el, ...]
  for (const img of document.querySelectorAll('img[src]')) {
    if (!visible(img)) continue;
    const src = img.getAttribute('src');
    if (!src || src.startsWith('data:')) continue;
    if (!imgGroups.has(src)) imgGroups.set(src, []);
    imgGroups.get(src).push(img);
  }
  let logoFlagged = 0;
  for (const [src, els] of imgGroups) {
    if (logoFlagged >= 1) break;
    if (els.length < 2) continue;
    const widths = els.map(e => e.getBoundingClientRect().width);
    const wMax = Math.max(...widths), wMin = Math.min(...widths);
    if (wMax > 0 && (wMax - wMin) / wMax > 0.2 && wMax - wMin > 12) {
      logoFlagged++;
      const filename = src.split('/').pop().split('?')[0];
      out.push({
        issueType: 'logoSizeInconsistent', severity: 'low',
        selector: sel(els[0]), bbox: bb(els[0]),
        description: `Same image "${filename}" rendered at ${els.length} different sizes: ${Math.round(wMin)}-${Math.round(wMax)}px. Standardize logo size (typically 32/40/48px in headers).`
      });
    }
  }

  // ── 6. Image without explicit dimension (CLS risk) ────────────────
  let dimFlagged = 0;
  for (const img of document.querySelectorAll('img')) {
    if (dimFlagged >= 4) break;
    if (!visible(img)) continue;
    const w = img.getAttribute('width');
    const h = img.getAttribute('height');
    const cs = getComputedStyle(img);
    const ar = cs.aspectRatio || '';
    if (!w && !h && (!ar || ar === 'auto')) {
      dimFlagged++;
      const src = (img.getAttribute('src') || '').split('/').pop().split('?')[0];
      out.push({
        issueType: 'imageWithoutDimension', severity: 'low',
        selector: sel(img), bbox: bb(img),
        description: `<img src="${src.slice(0, 40)}"> has no width/height attributes and no CSS aspect-ratio. Causes Cumulative Layout Shift while loading.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~10 findings per cell
- Self-skips: page with no images / avatars returns []
- The `avatarShapeMixed` catches circle + square avatars used together
- The `logoSizeInconsistent` catches same logo rendered different sizes across page locations
- The `imageWithoutDimension` is the main Cumulative Layout Shift cause for image-heavy pages
