---
name: senternet-site-google-analytics
description: Add GA4 with build-time env gating and lazy loading.
---

# Google Analytics (GA4) Setup

Add GA4 to a Vite + React site with lazy loading, environment gating, and no render-blocking. Use the Firebase Console to link the Firebase project to Google Analytics, then retrieve or confirm the Measurement ID.

## Prerequisites

Run `/senternet-site-gcloud-auth` first if you haven't authenticated this machine yet (requires the `analytics.edit` scope). The auth skill should try the browser-based Google login flow on behalf of the user before asking them to do anything manually; only fall back to an explicit command if that browser flow cannot complete in this environment. Never try to complete ADC or quota-project setup automatically inside this flow.

If the site already has a Firebase project, link it to Google Analytics in the Firebase Console before wiring the Measurement ID. There is no CLI link path in this skill.

## Design principles

- GA loads after `window.load` so it never blocks FCP or LCP
- The Measurement ID is injected at build time via a Vite plugin so dev builds are GA-free
- The GA block is stripped entirely in dev/staging — it never loads on non-prod environments
- All pageviews (including bounces) are tracked because the script loads on every visit, not on interaction

## Steps

### 1. Link the Firebase project to Google Analytics manually

If the Firebase project is not yet linked, open the Firebase Console and complete the link there. There is no CLI path in this skill for creating the Firebase ↔ Google Analytics connection.

Use this flow:
1. Open the Firebase Console for the exact project ID from `.firebaserc`.
2. Go to Project settings, then the Google Analytics / Integrations section.
3. Click the link option and connect the project to the correct GA account or property.
4. Finish the browser flow until the Firebase Console shows the project is linked.
5. Return here only after the link is visible in the console.

Do not try to link the project with `addGoogleAnalytics`, `analyticsDetails`, or any other CLI/API step in this skill. If the project is already linked, skip straight to the Measurement ID step below.

### 2. Get a GA4 Measurement ID via the Analytics Admin API

Run the following to retrieve or create a GA4 property and get the Measurement ID:

**Step 2a — Get an access token:**
```bash
TOKEN=$(gcloud auth print-access-token)
```

**Step 2b — List GA accounts to find your account ID:**
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://analyticsadmin.googleapis.com/v1beta/accounts" | python3 -m json.tool
```

The response lists your GA accounts. Note the `name` field (e.g. `accounts/123456`). If there's only one account, use it automatically. If there are multiple, show the list and ask the user which account to use.

**Step 2c — Check if a property already exists for this domain:**
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://analyticsadmin.googleapis.com/v1beta/properties?filter=parent:accounts/ACCOUNT_ID" | python3 -m json.tool
```

If a property matching the site's domain exists, use it (skip to step 2e). If not, create one.

**Step 2d — Create a new GA4 property:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "APP_NAME",
    "timeZone": "America/New_York",
    "currencyCode": "USD",
    "parent": "accounts/ACCOUNT_ID",
    "industryCategory": "TECHNOLOGY"
  }' \
  "https://analyticsadmin.googleapis.com/v1beta/properties" | python3 -m json.tool
```

Note the `name` field from the response (e.g. `properties/789012`).

**Step 2e — Create a web data stream to get the Measurement ID:**
```bash
MEASUREMENT_ID=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "DOMAIN web stream",
    "type": "WEB_DATA_STREAM",
    "webStreamData": {
      "defaultUri": "https://DOMAIN"
    }
  }' \
  "https://analyticsadmin.googleapis.com/v1beta/PROPERTY_NAME/dataStreams" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['webStreamData']['measurementId'])")

echo "Measurement ID: $MEASUREMENT_ID"
```

If any step fails with a 403, the token is missing the analytics scope. Run `/senternet-site-gcloud-auth` again and retry with the browser-based auth commands above.

If the user already has a Measurement ID they want to use, accept it and skip the API steps above.

### 3. Add the GA block to `index.html`

Insert between comment markers so the Vite plugin can substitute or strip it:

```html
<!-- GA_START -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
  window.addEventListener('load', function() {
    if (document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) return;
    var s = document.createElement('script');
    s.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
    s.async = true;
    document.head.appendChild(s);
  });
</script>
<!-- GA_END -->
```

The literal string `GA_MEASUREMENT_ID` is replaced at build time by the Vite plugin below.

### 4. Add the `htmlPlugin` to `vite.config.ts`

```typescript
const htmlPlugin = (gaId: string): Plugin => ({
  name: 'html-transform',
  transformIndexHtml(html) {
    if (gaId) {
      return html
        .replace(/GA_MEASUREMENT_ID/g, gaId)
        .replace(/\s*<!-- GA_START -->\n/, '\n      <!-- Google Analytics -->\n')
        .replace(/\n\s*<!-- GA_END -->/, '');
    }
    return html.replace(/[ \t]*<!-- GA_START -->[\s\S]*?<!-- GA_END -->\n?/g, '');
  },
});
```

### 5. Set `VITE_GA_ID` in env files

```bash
# .env.development — GA disabled in dev
VITE_GA_ID=

# .env.production — use the Measurement ID retrieved above
VITE_GA_ID=G-XXXXXXXXXX
```

### 6. Strip GA script from prerendered HTML

In `scripts/prerender.mjs`, strip the GA `<script>` tag so it isn't double-loaded when the hydrated app adds it:

```js
html = html.replace(
  /<script[^>]*src="https:\/\/www\.googletagmanager\.com\/gtag\/js[^"]*"[^>]*><\/script>/g,
  ''
);
```

### 7. Add GA event tracking helper

```typescript
// src/lib/analytics.ts
export function trackEvent(eventName: string, params?: Record<string, unknown>) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, params);
  }
}
```

### 8. Add gtag type declaration

In `src/vite-env.d.ts`:
```typescript
declare function gtag(...args: unknown[]): void;
```

## Verification

After deploying to production:
- Open Chrome DevTools → Network tab
- Filter by `googletagmanager.com`
- Confirm the script loads after the page `load` event fires, not during initial HTML parse
- Check GA4 Realtime report to confirm hits are arriving

## Framework: Next.js track

The Firebase Console linking and Measurement ID retrieval steps above are unchanged. The wiring is different: there is no `index.html`, no `htmlPlugin`, no `GA_START`/`GA_END` markers, and no prerender strip step.

**1. Env var** — `NEXT_PUBLIC_GA_ID` instead of `VITE_GA_ID`, read via `process.env`. It must also be listed in `apphosting.yaml` with `BUILD` availability, or it is `undefined` in the deployed client bundle even though `.env.production` has it:

```yaml
env:
  - variable: NEXT_PUBLIC_GA_ID
    value: G-XXXXXXXXXX
    availability: [BUILD, RUNTIME]
```

Leave it empty in `.env.development` so dev never reports.

**2. Load it with `next/script`** in `app/layout.tsx`. The gating is a plain conditional — an empty ID renders nothing at all, which is the equivalent of the Vite plugin stripping the block:

```tsx
import Script from 'next/script';

const gaId = process.env.NEXT_PUBLIC_GA_ID;

// inside the layout's returned JSX, before </body>
{gaId && (
  <>
    <Script src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`} strategy="lazyOnload" />
    <Script id="ga-init" strategy="lazyOnload">
      {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
        gtag('js',new Date());gtag('config','${gaId}');`}
    </Script>
  </>
)}
```

`strategy="lazyOnload"` is the equivalent of the Vite track's `window.addEventListener('load', ...)` deferral — it keeps GA off the critical path so it never costs FCP or LCP. Do not use `beforeInteractive`.

**3. Pageviews on client-side navigation.** The Vite track gets one `config` call per full page load. Here the App Router navigates without a reload, so add a small `'use client'` component that fires `gtag('event', 'page_view', ...)` on `usePathname()` changes, or GA will record only the entry page of each session.

**4. No prerender strip.** Step 6 above (removing the gtag `<script>` from prerendered HTML) does not apply — `next/script` loads it once.

The `trackEvent` helper is unchanged; put it in `lib/analytics.ts` and mark any component that calls it `'use client'`.

See `/senternet-site-framework` for the full convention map.
