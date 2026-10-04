---
name: senternet-site-ads-reddit-pixel
description: Install the Reddit conversion pixel with build-time gating.
---

# Reddit Pixel Setup

Add the Reddit Ads conversion pixel for tracking installs and page visits from Reddit ad campaigns.

## Steps

### 1. Add the bootstrap stub to `index.html`

Add this to `<head>` before the closing tag. It initializes the `window.rdt` queue so the pixel can be called before `pixel.js` loads:

```html
<!-- REDDIT_PIXEL_START -->
<script>
  window.rdt = window.rdt || function() {
    (window.rdt.callQueue = window.rdt.callQueue || []).push(arguments);
  };
  window.rdt.callQueue = window.rdt.callQueue || [];
</script>
<!-- REDDIT_PIXEL_END -->
```

The comment markers allow the prerender script to strip this script from the static HTML snapshot (it would double-load otherwise).

### 2. Get the Pixel ID from Reddit Ads

In Reddit Ads → Advertise → Pixels → create or copy your pixel ID. It looks like `t2_XXXXXXXX`.

### 3. Add `VITE_REDDIT_PIXEL_ID` to env files

`.env.production`:
```
VITE_REDDIT_PIXEL_ID=t2_XXXXXXXX
```

`.env.development`:
```
VITE_REDDIT_PIXEL_ID=
```

### 4. Create `src/components/RedditPixel.tsx`

```tsx
import { useEffect } from 'react';

interface RdtFn {
  (...args: unknown[]): void;
  callQueue: unknown[][];
}

declare global {
  interface Window { rdt?: RdtFn; }
}

const PIXEL_ID = import.meta.env.VITE_REDDIT_PIXEL_ID as string | undefined;

export function trackRedditEvent(eventName: string) {
  if (typeof window !== 'undefined' && window.rdt && PIXEL_ID) {
    window.rdt('track', eventName);
  }
}

export function RedditPixel() {
  useEffect(() => {
    if (!PIXEL_ID || !window.rdt) return;

    const alreadyInited = window.rdt.callQueue.some(
      (args) => Array.isArray(args) && args[0] === 'init' && args[1] === PIXEL_ID
    );
    if (alreadyInited) return;

    const existing = document.querySelector<HTMLScriptElement>('script[data-reddit-pixel]');
    if (!existing) {
      const s = document.createElement('script');
      s.src = 'https://www.redditstatic.com/ads/pixel.js';
      s.async = true;
      s.dataset.redditPixel = 'true';
      document.head.appendChild(s);
    }

    window.rdt('init', PIXEL_ID);
    window.rdt('track', 'PageVisit');
  }, []);

  return null;
}
```

### 5. Add `<RedditPixel>` to the app root

In `src/App.tsx`:
```tsx
import { RedditPixel } from './components/RedditPixel';

function App() {
  return (
    <>
      <RedditPixel />
      {/* ... rest of app */}
    </>
  );
}
```

### 6. Track conversion events

Call `trackRedditEvent` when a meaningful conversion happens (e.g. App Store link clicked):

```tsx
import { trackRedditEvent } from './components/RedditPixel';

function HeroSection() {
  return (
    <a
      href="https://apps.apple.com/app/..."
      onClick={() => trackRedditEvent('Lead')}
    >
      Download on App Store
    </a>
  );
}
```

Common Reddit Ads event names: `PageVisit`, `ViewContent`, `Lead`, `AddToCart`, `Purchase`, `SignUp`.

### 7. Strip Reddit pixel from prerendered HTML

In `scripts/prerender.mjs`, the strip block should include Reddit:
```js
html = html
  .replace(/<script[^>]*src="https:\/\/www\.redditstatic\.com\/ads\/pixel\.js[^"]*"[^>]*><\/script>/g, '')
  // ...other strips
```

### 8. Verify in Reddit Ads

In Reddit Ads → Pixels, click "Test Pixel". Visit your site and confirm events appear in the tester. PageVisit should fire on every page load.

## Notes

- The pixel only loads when `VITE_REDDIT_PIXEL_ID` is set — empty on dev, so no accidental test events
- The bootstrap stub in `index.html` ensures `window.rdt` exists before React hydrates, so tracking calls in `onClick` handlers never throw
- Reddit pixel does NOT fire from prerendered HTML (the script is stripped) — it fires when the live user's browser loads and React hydrates

## Framework: Next.js track

- `NEXT_PUBLIC_REDDIT_PIXEL_ID` replaces `VITE_REDDIT_PIXEL_ID`, and must also be listed in `apphosting.yaml` with `BUILD` availability.
- The bootstrap stub and the pixel script both load through `next/script` in `app/layout.tsx` with `strategy="lazyOnload"`, gated on the env var being non-empty. There is no `index.html` stub and no prerender strip step.
- The `RedditPixel` component that fires conversion events must be a `'use client'` component, and page-view tracking must key off `usePathname()` — client-side navigation does not reload the pixel.
- Campaign landing pages are usually `noindex`; that is set in the page's `metadata`, not by the pixel wiring.

See `/senternet-site-framework` for the full convention map.
