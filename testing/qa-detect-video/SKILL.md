---
name: qa-detect-video
section: visual
description: "Detects unresponsive <video> elements and non-responsive YouTube/Vimeo iframe embeds: missing max-width, container overflow, no controls, no aspect-ratio wrapper on embeds"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasVideo, hasAudio]
---

## What it checks
- `videoNotResponsive` — `<video>` element has no `max-width:100%` or `width:100%` and is wider than 300px rendered
- `videoOverflowsContainer` — `<video>` `scrollWidth` exceeds its parent container width
- `videoNoControls` — `<video>` is missing the `controls` attribute (mobile users cannot play/pause)
- `videoIframeNotResponsive` — YouTube/Vimeo `<iframe>` embed has no responsive wrapper (no `aspect-ratio` CSS, no `padding-bottom` ratio trick, no `max-width:100%`)
- `videoIframeFixedSize` — YouTube/Vimeo `<iframe>` has hard-coded `width`/`height` HTML attributes without responsive override

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : el.className ? `.${String(el.className).trim().split(/\s+/)[0]}` : '')).slice(0, 120);
  const vw = innerWidth;

  // 1 & 2 & 3. <video> responsiveness and controls
  for (const video of document.querySelectorAll('video')) {
    if (out.length >= 20) break;
    const r = video.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue; // not rendered
    const s = getComputedStyle(video);
    const parent = video.parentElement;
    const pr = parent ? parent.getBoundingClientRect() : null;

    // 1. videoNotResponsive — no max-width:100% / width:100% on a substantial video
    if (r.width > 300) {
      const hasFluidWidth = s.width === '100%' || s.maxWidth === '100%' ||
        parseFloat(s.maxWidth) / vw >= 0.99 ||
        (s.width.endsWith('%') && parseFloat(s.width) >= 90);
      if (!hasFluidWidth) {
        out.push({ issueType: 'videoNotResponsive', severity: 'medium', selector: sel(video),
          description: `<video> element (${Math.round(r.width)}px wide) has no max-width:100% or width:100% — will overflow on smaller screens`,
          bbox: bb(video) });
      }
    }

    // 2. videoOverflowsContainer
    if (pr && r.width > pr.width + 5) {
      out.push({ issueType: 'videoOverflowsContainer', severity: 'high', selector: sel(video),
        description: `<video> (${Math.round(r.width)}px) overflows its container (${Math.round(pr.width)}px) — horizontal scroll or clipping on mobile`,
        bbox: bb(video) });
    }

    // 3. videoNoControls — no native controls, no custom overlay with play button
    if (!video.hasAttribute('controls') && !video.hasAttribute('autoplay')) {
      // Check for custom play button overlay in parent
      const customPlay = parent && parent.querySelector('[class*="play"], [aria-label*="play" i], button[data-testid*="play"]');
      if (!customPlay) {
        out.push({ issueType: 'videoNoControls', severity: 'medium', selector: sel(video),
          description: `<video> has no controls attribute and no detected custom play button — mobile users cannot play this video`,
          bbox: bb(video) });
      }
    }
  }

  // 4 & 5. YouTube / Vimeo <iframe> embed responsiveness
  const videoIframeHosts = /youtube\.com|youtu\.be|vimeo\.com|dailymotion\.com|wistia\.com|loom\.com/i;
  for (const iframe of document.querySelectorAll('iframe')) {
    if (out.length >= 20) break;
    const src = iframe.src || iframe.getAttribute('data-src') || '';
    if (!videoIframeHosts.test(src)) continue;

    const r = iframe.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const s = getComputedStyle(iframe);
    const parent = iframe.parentElement;
    const ps = parent ? getComputedStyle(parent) : null;

    // 4. videoIframeNotResponsive — no responsive wrapper
    const iframeHasFluid = s.width === '100%' || s.maxWidth === '100%' || (s.width.endsWith('%') && parseFloat(s.width) >= 90);
    const parentHasAspectRatio = ps && (ps.aspectRatio !== 'auto' || ps.paddingBottom.endsWith('%'));
    if (!iframeHasFluid && !parentHasAspectRatio) {
      out.push({ issueType: 'videoIframeNotResponsive', severity: 'high', selector: sel(iframe),
        description: `Video embed iframe (${src.slice(0, 60)}) has no responsive wrapper — fixed size will overflow on mobile. Wrap in a container with aspect-ratio:16/9 and width:100%.`,
        bbox: bb(iframe) });
    }

    // 5. videoIframeFixedSize — hard-coded width/height HTML attributes
    const attrW = iframe.getAttribute('width');
    const attrH = iframe.getAttribute('height');
    if (attrW && !attrW.endsWith('%') && parseInt(attrW) > 300) {
      out.push({ issueType: 'videoIframeFixedSize', severity: 'medium', selector: sel(iframe),
        description: `Video embed iframe has fixed HTML width="${attrW}" attribute — override with CSS width:100% and remove the attribute for responsive sizing`,
        bbox: bb(iframe) });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| videoNotResponsive | medium | "`<video>` element ({w}px wide) has no max-width:100% or width:100% — will overflow on smaller screens" |
| videoOverflowsContainer | high | "`<video>` ({w}px) overflows its container ({cw}px) — horizontal scroll or clipping on mobile" |
| videoNoControls | medium | "`<video>` has no controls attribute and no detected custom play button — mobile users cannot play" |
| videoIframeNotResponsive | high | "Video embed iframe has no responsive wrapper — fixed size will overflow on mobile" |
| videoIframeFixedSize | medium | "Video embed iframe has fixed HTML width attribute — override with CSS width:100%" |
