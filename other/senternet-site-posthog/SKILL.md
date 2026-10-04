---
name: senternet-site-posthog
description: Add PostHog Cloud product analytics with browser-only lazy loading, production gating, and non-PII event tracking.
---

# PostHog Setup

Add PostHog to a Vite + React site for product analytics — events, funnels, retention, and optional session replay — with lazy loading, environment gating, and no render-blocking. Use this when the user has chosen PostHog over GA4 (see `/senternet-site-analytics` if the provider is still undecided).

## Design principles

- PostHog initializes after the app mounts, in the browser only — it never blocks FCP or LCP
- The project API key is read from a build-time env var so dev builds are PostHog-free
- The client is gated on `import.meta.env.PROD` and a configured key — it never loads in dev, staging, SSR, or prerender
- All capture calls go through one small helper so events stay consistent and payloads stay non-PII

## Steps

### 1. Create or confirm a PostHog Cloud project

In PostHog Cloud, create (or confirm) a project and copy:
- The **project API key** (starts with `phc_`)
- The **API host** (`https://us.i.posthog.com` or `https://eu.i.posthog.com`)

### 2. Add env vars

Put the key and host in the site's env files. Set real values only in `.env.production` so dev stays free of PostHog traffic:

```
VITE_POSTHOG_KEY=phc_xxxxxxxx
VITE_POSTHOG_HOST=https://us.i.posthog.com
```

Leave them empty/absent in `.env` / `.env.development`.

### 3. Install the client

```bash
npm install posthog-js
```

### 4. Create a gated analytics helper — `src/lib/analytics.ts`

Centralize init and capture so the rest of the app never imports `posthog-js` directly:

```ts
import type { PostHog } from 'posthog-js';

let client: PostHog | null = null;

const enabled =
  import.meta.env.PROD && !!import.meta.env.VITE_POSTHOG_KEY;

export async function initAnalytics(): Promise<void> {
  if (!enabled || client || typeof window === 'undefined') return;
  const { default: posthog } = await import('posthog-js'); // dynamic — kept out of the main bundle
  posthog.init(import.meta.env.VITE_POSTHOG_KEY, {
    api_host: import.meta.env.VITE_POSTHOG_HOST,
    capture_pageview: true,
    autocapture: false, // capture intentional events only — keeps payloads clean and non-PII
  });
  client = posthog;
  capture('app_opened');
}

export function capture(event: string, props?: Record<string, unknown>): void {
  client?.capture(event, props);
}
```

### 5. Initialize after the app mounts

Call `initAnalytics()` from a top-level effect so it runs after first paint, never during prerender:

```tsx
import { useEffect } from 'react';
import { initAnalytics } from './lib/analytics';

useEffect(() => {
  initAnalytics();
}, []);
```

### 6. Capture events through the helper

Use small, named events instead of raw `posthog.capture` calls scattered through the app:

```ts
import { capture } from './lib/analytics';

capture('cta_clicked', { location: 'hero' });
```

## Implementation rules

- Gate everything on `import.meta.env.PROD` **and** a configured key — no key means no load.
- Import `posthog-js` dynamically from the browser only — never at module top level, during SSR, or in the prerender pass.
- Keep payloads non-PII: provider type, counts, flags, tab/section names, and other app metadata only.
- Never send email addresses, names, subjects, bodies, prompts, API keys, tokens, or unsubscribe URLs.
- Leave `autocapture` off unless the user explicitly wants it — it can sweep up form values and text content.

## Prerender / CSP notes

- Because init is gated behind `PROD` + a runtime effect, the prerender pass produces no PostHog markup — no strip-list entry is needed. Confirm the prerendered HTML contains no `posthog` references.
- If the site has a Content Security Policy (`/senternet-site-csp`), add the configured `VITE_POSTHOG_HOST` to `connect-src` (and `script-src` if you load session replay).

## Validation

- Dev (`npm run dev`) shows **no** requests to the PostHog host in the network tab.
- A production build with a key initializes once and emits the `app_opened` event.
- The PostHog host appears in the network tab only in production.
- Spot-check captured event payloads in PostHog — confirm no PII.

## Framework: Next.js track

Same product setup; different wiring.

- `NEXT_PUBLIC_POSTHOG_KEY` and `NEXT_PUBLIC_POSTHOG_HOST` replace the `VITE_*` names, read via `process.env`. Both must also appear in `apphosting.yaml` with `BUILD` availability or they will be `undefined` in the deployed bundle.
- Initialization goes in a `'use client'` provider component mounted from `app/layout.tsx`, not in `main.tsx`. Guard on `typeof window !== 'undefined'` — the layout renders on the server, and calling `posthog.init` there throws.
- Capture pageviews on `usePathname()` / `useSearchParams()` changes rather than relying on PostHog's automatic capture, which only sees the initial document load under client-side routing. Wrap the `useSearchParams()` reader in `<Suspense>` or it opts the whole route into dynamic rendering.
- Session replay and autocapture still must stay off for any route that renders PII.

See `/senternet-site-framework` for the full convention map.
