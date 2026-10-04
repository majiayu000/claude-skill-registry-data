---
name: qa-detect-images
section: visual
description: "Detects missing alt text, broken images, oversized images, aspect-ratio distortion (stretched), and hero/banner images without object-fit:cover"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasImages]
---

## What it checks
- Missing alt attribute (absent, not empty)
- Failed loads (broken image)
- Images rendered at <1/3 natural size (oversized download for tiny render)
- Images stretched: rendered aspect ratio differs from natural aspect ratio by >20%
- Hero/banner images without `object-fit: cover` — renders as distorted fill or letterboxed contain

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // Returns true only if the element is actually rendered and visible to the user.
  // Skips images inside collapsed sidebars, hidden navs, display:none containers,
  // and elements parked entirely off-screen (negative coords / beyond the viewport).
  const vw = innerWidth, vh = innerHeight;
  const isRendered = el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    // Entirely outside the viewport box → user never sees it (e.g. collapsed sidebar
    // logo at x:-228, or off-canvas drawer image past the right edge).
    if (r.right <= 0 || r.left >= vw || r.bottom <= 0 || r.top >= vh) return false;
    let node = el;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
      node = node.parentElement;
    }
    return true;
  };

  // Returns true for small UI icons that are purely decorative alongside visible text.
  // These should have alt="" but are not content-carrying images — flagging them as
  // missingAlt creates false-positive noise (user sees no "image", just an icon).
  const isDecorativeIcon = (img) => {
    const r = img.getBoundingClientRect();
    // Only applies to small icons (≤ 40×40px render size)
    if (r.width > 40 || r.height > 40) return false;
    // Explicitly marked decorative by the developer → fully skip, no issue at all
    if (img.getAttribute('aria-hidden') === 'true' || img.getAttribute('role') === 'presentation') return true;
    // Icon-like src filename hint (icon, glyph, sprite, badge, etc.)
    const src = (img.src || '').toLowerCase();
    if (/\b(icon|glyph|sprite|badge|avatar|favicon|logo)\b/.test(src)) return true;
    // Small image inside a card-header, stat-widget, nav, topbar, or sidebar
    // where sibling/parent visible text already carries the semantic meaning
    const decorativeContainer = img.closest(
      'nav, [class*="sidebar"], [class*="navbar"], [class*="topbar"], [class*="appbar"],' +
      '[class*="card-header"], [class*="card-icon"], [class*="stat"], [class*="widget-header"],' +
      '[class*="menu-item"], [class*="nav-item"], [class*="breadcrumb"]'
    );
    if (decorativeContainer) {
      // Icon is alongside text — it's decorative in this context
      const parent = img.parentElement;
      if (parent) {
        const hasNearbyText = parent.innerText && parent.innerText.trim().length > 0;
        if (hasNearbyText) return true;
      }
    }
    return false;
  };

  for (const img of document.querySelectorAll('img')) {
    if (out.length >= 20) break;
    const src = (img.src || '').slice(0,100);
    const selector = `img[src="${src.slice(0,60)}"]`;

    // 1. Missing alt — only on rendered, non-decorative images.
    // Icons alongside text labels are decorative — they need alt="" not descriptive alt,
    // and are filed at low severity with a targeted fix message to avoid false-positive noise.
    if (!img.hasAttribute('alt') && isRendered(img)) {
      // Completely skip if aria-hidden or role=presentation (developer already handled it)
      if (img.getAttribute('aria-hidden') === 'true' || img.getAttribute('role') === 'presentation') {
        // no issue
      } else if (isDecorativeIcon(img)) {
        // Small icon next to visible text — needs alt="" (empty) not descriptive alt
        out.push({ issueType:'decorativeIconMissingEmptyAlt', severity:'low', selector,
          description:`Small icon <img> (${Math.round(img.getBoundingClientRect().width)}×${Math.round(img.getBoundingClientRect().height)}px) is missing alt="". Since it appears alongside a visible text label it is decorative — add alt="" or aria-hidden="true" to silence screen readers.`, bbox: bb(img) });
      } else {
        // Real content image — needs a meaningful description
        out.push({ issueType:'missingAlt', severity:'medium', selector,
          description:`<img> element is missing the alt attribute entirely. Add descriptive alt text so screen-reader users know what the image conveys.`, bbox: bb(img) });
      }
    }

    // 2. Broken image — only flag if the image is actually rendered/visible.
    // Hidden images (inside collapsed sidebar, display:none nav, etc.) are NOT flagged here —
    // they may be intentional placeholders or off-screen variants never shown to the user.
    if (img.complete && img.naturalWidth === 0) {
      if (!isRendered(img)) continue; // collapsed sidebar, hidden panel, off-screen — skip
      out.push({ issueType:'brokenImage', severity:'critical', selector,
        description:`Image failed to load: ${src}`, bbox: bb(img) });
      continue; // can't compute ratios without natural dimensions
    }

    const r = img.getBoundingClientRect();
    if (img.naturalWidth === 0 || img.naturalHeight === 0) continue;
    if (r.width === 0 || r.height === 0) continue;
    if (!isRendered(img)) continue; // off-screen / hidden — oversized/stretched are irrelevant if unseen

    // 3. Oversized (downloaded much larger than rendered)
    if (img.naturalWidth/r.width > 3) {
      const ratio = (img.naturalWidth/r.width).toFixed(1);
      out.push({ issueType:'oversizedImage', severity:'low', selector,
        description:`Natural size ${img.naturalWidth}×${img.naturalHeight}px rendered at ${Math.round(r.width)}×${Math.round(r.height)}px (${ratio}x oversized)`, bbox: bb(img) });
    }

    // 4. Stretched (aspect ratio distortion)
    const naturalRatio  = img.naturalWidth / img.naturalHeight;
    const renderedRatio = r.width / r.height;
    const ratioDiff = Math.abs(naturalRatio - renderedRatio) / naturalRatio;
    if (ratioDiff > 0.20) {
      const pctOff = Math.round(ratioDiff * 100);
      out.push({ issueType:'imageStretched', severity:'medium', selector,
        description:`Aspect ratio distorted: natural ${img.naturalWidth}×${img.naturalHeight} (${naturalRatio.toFixed(2)}:1) rendered at ${Math.round(r.width)}×${Math.round(r.height)} (${renderedRatio.toFixed(2)}:1) — ${pctOff}% off`, bbox: bb(img) });
    }
  }

    // 6. CSS background-image hero sections — background-size not cover
    const heroContainerSelectors = [
      '[class*="hero"]','[class*="banner"]','[class*="jumbotron"]','[class*="masthead"]',
      '[class*="splash"]','header[class*="bg"]','section[class*="cover"]'
    ];
    const seenBgEls = new Set();
    for (const hSel of heroContainerSelectors) {
      for (const el of document.querySelectorAll(hSel)) {
        if (out.length >= 20 || seenBgEls.has(el)) break;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height < 150) continue;
        const s = getComputedStyle(el);
        const bgImage = s.backgroundImage;
        if (!bgImage || bgImage === 'none' || !bgImage.startsWith('url')) continue;
        seenBgEls.add(el);
        const bgSize = s.backgroundSize;
        if (bgSize === 'cover') continue; // correct
        const selector = `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : '')}`.slice(0, 120);
        out.push({ issueType: 'heroBackgroundNoCover', severity: 'medium', selector,
          description: `Hero/banner section (${Math.round(r.width)}×${Math.round(r.height)}px) has background-image with background-size:${bgSize || 'auto'} — use background-size:cover to prevent letterboxing or distortion on different screen sizes`,
          bbox: bb(el) });
      }
    }

    // 5. Hero image object-fit — large/banner images without object-fit:cover
    //
    // CRITICAL: a "hero" image must actually be hero-sized AND not a logo. The
    // previous selector `header img` matched ANY <img> inside ANY <header>,
    // including site logos in sidebar/topbar headers. We now require BOTH a
    // hero-like ancestor class AND minimum size, OR size-only for unclassed cases,
    // AND skip anything that smells like a logo/brand glyph.
    const isLogoOrBrand = (img) => {
      const alt = (img.getAttribute('alt') || '').toLowerCase();
      if (/^(logo|brand|favicon|icon|avatar|profile)\b/.test(alt)) return true;
      const cls = ((img.className && typeof img.className === 'string') ? img.className : '').toLowerCase();
      if (/\b(logo|brand|favicon|avatar)\b/.test(cls)) return true;
      // Image inside a logo/brand/avatar/nav-icon container
      const container = img.closest(
        '[class*="logo"], [class*="Logo"], [class*="brand"], [class*="Brand"], ' +
        '[class*="avatar"], [class*="Avatar"], [class*="profile-pic"], [class*="favicon"], ' +
        'nav, aside, [class*="sidebar"], [class*="Sidebar"], [class*="topbar"], [class*="Topbar"], ' +
        '[class*="navbar"], [class*="NavBar"], [class*="appbar"], [class*="AppBar"]'
      );
      if (container) return true;
      // src filename hints
      const src = (img.src || '').toLowerCase();
      if (/(logo|brand|favicon|avatar|profile)[-_]?\w*\.(png|jpe?g|svg|webp)/.test(src)) return true;
      return false;
    };

    const heroImgs = new Set();
    // Class-based heroes — but still must be a real-sized image (not a 40px logo
    // inside a `<header class="page-header">`).
    const heroSelectors = [
      '[class*="hero"] img', '[class*="banner"] img', '[class*="jumbotron"] img',
      '[class*="masthead"] img', '[class*="splash"] img'
    ];
    for (const hSel of heroSelectors) {
      for (const hImg of document.querySelectorAll(hSel)) {
        const r = hImg.getBoundingClientRect();
        // Must be at least 40% viewport width AND 120px tall to qualify as hero
        if (r.width >= innerWidth * 0.4 && r.height >= 120) heroImgs.add(hImg);
      }
    }
    // Size-only fallback for unclassed pages: ≥60% viewport width AND ≥200px tall
    for (const img of document.querySelectorAll('img')) {
      const r = img.getBoundingClientRect();
      if (r.width >= innerWidth * 0.6 && r.height >= 200) heroImgs.add(img);
    }
    for (const img of heroImgs) {
      if (out.length >= 20) break;
      if (isLogoOrBrand(img)) continue;                              // skip logos / avatars / nav icons
      if (img.complete && img.naturalWidth === 0) continue;          // already caught as broken
      const r = img.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const s = getComputedStyle(img);
      const objectFit = s.objectFit || 'fill';
      const src = (img.src || '').slice(0, 100);
      const heroSel = `img[src="${src.slice(0, 60)}"]`;
      if (objectFit === 'fill' || objectFit === 'none') {
        out.push({ issueType: 'heroImageNoCover', severity: 'medium', selector: heroSel,
          description: `Hero/banner image (${Math.round(r.width)}×${Math.round(r.height)}px) uses object-fit:${objectFit} — will distort on different aspect-ratio screens. Use object-fit:cover.`, bbox: bb(img) });
      } else if (objectFit === 'contain') {
        out.push({ issueType: 'heroImageLetterboxed', severity: 'low', selector: heroSel,
          description: `Hero/banner image (${Math.round(r.width)}×${Math.round(r.height)}px) uses object-fit:contain — may show empty letterbox bars on different screens. Consider object-fit:cover with object-position.`, bbox: bb(img) });
      }
    }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| missingAlt | medium | "img element is missing the alt attribute entirely" |
| brokenImage | critical | "Image failed to load: {src}" |
| oversizedImage | low | "Natural size {nw}×{nh}px rendered at {rw}×{rh}px ({ratio}x oversized)" |
| imageStretched | medium | "Aspect ratio distorted: natural {nw}×{nh} ({nr}:1) rendered at {rw}×{rh} ({rr}:1) — {pct}% off" |
| heroImageNoCover | medium | "Hero/banner image uses object-fit:{fill|none} — will distort on different aspect-ratio screens" |
| heroImageLetterboxed | low | "Hero/banner image uses object-fit:contain — may show empty letterbox bars on different screens" |
| heroBackgroundNoCover | medium | "Hero/banner section has background-image with background-size:{size} — use background-size:cover" |

## Threshold note
The 20% threshold balances catching genuine distortion (logos squashed, photos stretched) against allowing minor variations from `object-fit: cover` cropping. Increase to 30% if false positives appear on photos with intentional cropping; decrease to 10% for strict design QA.
