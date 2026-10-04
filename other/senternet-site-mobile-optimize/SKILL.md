---
name: senternet-site-mobile-optimize
description: Optimize hero images, loading, and motion for mobile.
---

# Mobile View Optimization

Optimize mobile page load by eliminating images that get visually hidden by content on small screens, and applying mobile-specific performance patterns.

## The problem this solves

Many marketing pages have a layout like:
- Desktop: hero text left, app screenshot right — both visible
- Mobile: hero text stacks on top, screenshot scrolls below the fold or gets hidden behind a CTA

If the screenshot image is downloaded even when hidden on mobile, it wastes bandwidth and hurts mobile LCP. The fix is to serve a smaller image (or no image) on mobile.

## Patterns

### Pattern 1: Responsive image with mobile-specific src

When the image exists on mobile but at a smaller size:

```html
<!-- In index.html -->
<link rel="preload" as="image" href="/hero-sm.webp" type="image/webp" fetchpriority="high"
  media="(max-width: 768px)" />
<link rel="preload" as="image" href="/hero.webp" type="image/webp" fetchpriority="high"
  media="(min-width: 769px)" />
```

```tsx
<picture>
  <source srcSet="/hero-sm.webp" type="image/webp" media="(max-width: 768px)" />
  <source srcSet="/hero.webp" type="image/webp" media="(min-width: 769px)" />
  <img src="/hero.webp" alt="App screenshot" width="560" height="1000" />
</picture>
```

The fallback `<img src>` must be `.webp` — no PNG fallback needed since WebP is universally supported.

Create the smaller version:
```js
// In convert-images.mjs or a separate script
await sharp('public/hero.png').resize(240).webp({ quality: 82 }).toFile('public/hero-sm.webp');
```

### Pattern 2: Hide below-fold images on mobile entirely

When the image is completely below the fold or hidden on mobile (e.g., a Mac desktop screenshot in a "desktop app" section):

```tsx
// CSS: hide on mobile
<div className="hidden md:block">
  <img src="/screenshot-mac.webp" alt="Desktop view" loading="lazy" />
</div>
```

With Tailwind's `hidden md:block`, the image renders in the DOM but is hidden. But the browser still downloads it. To prevent the download entirely:

```tsx
import { useState, useEffect } from 'react';

function DesktopOnlyImage() {
  const [isDesktop, setIsDesktop] = useState(false);
  useEffect(() => {
    setIsDesktop(window.matchMedia('(min-width: 768px)').matches);
  }, []);

  if (!isDesktop) return null;

  return <img src="/screenshot-mac.webp" alt="Desktop view" loading="lazy" />;
}
```

Note: this causes a hydration mismatch with prerendering. Use the CSS-only approach (`hidden md:block`) for images that are merely decorative on mobile, and the JS approach only for images large enough to meaningfully impact load time.

### Pattern 3: Lazy load below-the-fold images

All images that are not in the initial viewport should use `loading="lazy"`:

```tsx
<img src="/feature-image.webp" alt="Feature" loading="lazy" width="400" height="300" />
```

**Never** use `loading="lazy"` on the LCP image (the hero/above-fold image) — it defeats the point.

### Pattern 4: Disable animations on mobile

CSS animations (opacity transitions, glow pulses, floating effects) cause the GPU to repaint on every frame. On mobile CPUs this tanks Speed Index and LCP.

```css
/* Disable decorative animations on mobile */
@media (max-width: 768px) {
  .orb, .neon-glow, .float-animation {
    animation: none;
    opacity: 0.3; /* or display: none if purely decorative */
  }
}
```

In Tailwind:
```tsx
<div className="animate-pulse md:animate-none">...</div>
```

### Pattern 5: Reduce image dimensions for mobile via the conversion script

In `scripts/convert-images.mjs`, add a mobile variant step:

```js
// Generate a mobile-sized version of the hero screenshot
await sharp('public/screenshot-app.png')
  .resize(440)  // ~240px display + 2x retina
  .webp({ quality: 82 })
  .toFile('public/screenshot-app-sm.webp');
```

## Checklist

- [ ] Hero image has separate mobile and desktop variants (`-sm.webp` suffix)
- [ ] Both variants have `<link rel="preload">` in `index.html` with `media` attributes
- [ ] Desktop-only decorative images are not downloaded on mobile (conditional render or CSS `hidden`)
- [ ] All below-fold images use `loading="lazy"`
- [ ] All images have explicit `width` and `height` to prevent CLS
- [ ] Decorative CSS animations are disabled on mobile via media query
- [ ] Particle systems, orbs, and canvas animations check `window.innerWidth` before initializing

## Testing

Check mobile performance in Chrome DevTools:
1. Open DevTools → Network tab
2. Set throttling to "Slow 3G" and device to "Moto G Power" (or similar low-end mobile)
3. Reload and check what images downloaded
4. Any image that's `display: none` should not appear in the waterfall — if it does, prevent the download with conditional rendering

## Framework: Next.js track

The mobile hero, lazy loading, and reduced-motion rules all still apply; the implementation shifts to framework features.

- Responsive hero variants and `loading="lazy"` come from `next/image` with a correct `sizes` prop, rather than hand-generated `-sm.webp` files and manual `<picture>` sources. Keep `priority` on the hero only.
- There is no `index.html` to add a `<link rel="preload" media="...">` to. `priority` on the LCP image emits the preload for you.
- Animation disabling on mobile stays a CSS concern (`@media (prefers-reduced-motion)` and width-based rules) — no change.
- Any component gating on `window.matchMedia` or viewport width must be `'use client'` and read the value in an effect. Reading it during render breaks the server render.

See `/senternet-site-framework` for the full convention map.
