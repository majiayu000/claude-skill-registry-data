---
name: senternet-site-gdpr
description: Add an EU/GB-only cookie consent toaster that gates Google Analytics until the visitor accepts.
---

# GDPR Cookie Consent (EU/GB geo + GA gate)

Add a simple cookie consent banner for EEA and UK visitors that:

1. **Auto-detects** whether the visitor is in the EEA or GB (not shown elsewhere)
2. Offers **Allow all** / **Reject unnecessary**
3. **Does not load Google Analytics** until the visitor accepts (or is outside a consent region)
4. Appears as a **footer toaster** that matches the site chrome (not a modal wall)

Reference implementation: Highwire (`www.highwire.news`) in the monorepo that first shipped this pattern.

## When to run

- After `/senternet-site-google-analytics` (or when GA is already wired)
- When the site starts getting EEA/UK traffic and needs a consent gate before analytics cookies
- Not needed if the only analytics is cookieless (e.g. Ahrefs Web Analytics alone)

## Design principles

- **Geo-scoped chooser.** Only EEA + GB see the bar. US-primary traffic is not nagged.
- **Analytics is the only third-party cookie gated.** Auth sessions (Firebase IndexedDB / local storage), reCAPTCHA, and other strictly necessary storage stay on. Do not gate anonymous Firebase tokens behind this banner.
- **Consent is prior.** Until accept (or a resolved non-consent region), do not load gtag / PostHog capture that sets cookies.
- **Choice in localStorage**, not a cookie of its own: keys like `{prefix}.cookieConsent` and `{prefix}.consentRegion`.
- **Inject GA with the DOM when consent flips.** Do not rely on `next/script` `afterInteractive` for a component that mounts only after Allow all. That strategy often never inserts tags after first paint; imperative `document.createElement('script')` works for both auto-load and accept-click paths.
- **Never use em dashes** in copy, comments, or docs.

## Legal notes (keep short, do not overclaim)

- EEA/UK analytics cookies need a prior opt-in under GDPR / UK GDPR and ePrivacy-style rules.
- **Anonymous Firebase auth is essential/functional**, not marketing. Leave it always on. Disclose it in Privacy. Do not feed the anonymous UID into GA as a user id.
- reCAPTCHA / bot defense for sign-in is the same "necessary" bucket.
- This skill is engineering for a common Senternet pattern, not formal legal advice. Point Privacy Policy edits at counsel if the product is regulated.

## Country set (consent required)

ISO 3166-1 alpha-2:

- **EU 27:** AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE
- **EEA non-EU:** IS LI NO
- **UK:** GB (accept CDN alias `UK` as well)
- Treat `XX` / empty / private IPs as **not required** for the chooser (no banner flash on localhost)

## Storage contract

| Key | Values | Meaning |
|-----|--------|---------|
| `{prefix}.cookieConsent` | `accepted` \| `rejected` | Explicit choice |
| `{prefix}.consentRegion` | `required` \| `not_required` | Cached geo class |

Prefix: product slug, e.g. `highwire`, `premail`. One prefix per site.

**Allow rules for analytics:**

- `accepted` → load
- `rejected` → never load
- `not_required` + no choice → load
- unknown region + no choice → do **not** load (and do not show the bar until region resolves)

**Show banner when:** `region === 'required'` and choice is null.

Fire a window event after write, e.g. `{prefix}:cookie-consent`, so the analytics mount can react without a full navigation.

## Geo resolution

Same-origin `GET /api/geo` (Next.js) or equivalent Cloud Function / Hosting rewrite (Vite):

1. Read CDN country headers if present: `cf-ipcountry`, `x-vercel-ip-country`, `cloudfront-viewer-country`, `x-appengine-country`, `x-country-code`, `x-geo-country`, `x-client-geo-location` (first segment before comma).
2. Else take client IP from leftmost `X-Forwarded-For` (one hop, match load balancer trust) or `X-Real-IP`.
3. Skip private/loopback IPs (dev).
4. Best-effort free IP lookup server-side (e.g. `https://get.geojs.io/v1/ip/country/{ip}.json`) with a short timeout (~1.5s). **No third-party origin in the browser CSP.**
5. Response: `{ country: string | null, consentRequired: boolean }`, `Cache-Control: no-store`.

**Failure policy:** if `/api/geo` itself fails (network), do not cache a region; keep analytics off and the bar hidden; retry next visit. If geo succeeds with `country: null` (private IP), return `consentRequired: false`.

Share one in-flight client lookup between the banner and the analytics gate so first paint does not double-fetch.

## UI (footer toaster)

- `position: fixed` near the bottom edge, max-width ~34rem, centered or inset
- Paper/surface background, site border tokens, primary + secondary buttons
- Copy pattern (adapt brand voice):

  > **Cookies**  
  > We use analytics cookies to understand how {Product} is used. Sign-in and security storage always work. See the [Privacy Policy](/privacy).  
  > [Reject unnecessary]  [Allow all]

- `role="dialog"` with labelled title/description
- SSR / first client paint: render **nothing** until region is known and required (no flash for US visitors)
- z-index under account/signup modals, above sticky header

Match existing button and label styles; do not invent a second design system.

## Gate Google Analytics

### Next.js track (reference)

1. Env: `NEXT_PUBLIC_GA_ID` in production / `apphosting.yaml` with **BUILD** availability. Leave empty in local `.env` unless deliberately testing.
2. Root layout mounts both `<Analytics />` and `<CookieConsentBanner />`.
3. `Analytics` returns null when the ID is unset.
4. When allowed, install gtag **imperatively**:

```ts
window.dataLayer = window.dataLayer || [];
if (typeof window.gtag !== 'function') {
  // Push the Arguments object (official snippet), not a rest array.
  window.gtag = function gtag() {
    window.dataLayer!.push(arguments);
  } as (...args: unknown[]) => void;
  window.gtag('js', new Date());
  window.gtag('config', gaId);
}
if (!document.getElementById('ga4-src')) {
  const script = document.createElement('script');
  script.id = 'ga4-src';
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(gaId)}`;
  document.head.appendChild(script);
}
```

5. App Router still needs a `page_view` on `usePathname()` changes after the first config.
6. `trackEvent` already no-ops when `window.gtag` is missing; keep that contract.

### Vite track

1. Do **not** leave the unconditional GA block from `/senternet-site-google-analytics` in `index.html` if this skill is applied. Either:
   - Strip the `GA_START`/`GA_END` block from HTML and load only from a client consent module, or
   - Keep the build-time ID substitution but make the injected snippet a no-op stub that waits for consent before appending the googletagmanager script.
2. Mount the banner + consent gate near the app root (e.g. `Layout.tsx` / `App.tsx`).
3. Geo: add a Hosting rewrite to a small Cloud Function or use Firebase App Check-free callable that returns the same JSON. Pure client calls to third-party geo APIs force CSP `connect-src` changes and leak the lookup to the browser; prefer same-origin.
4. Prerender: ensure prerendered HTML never includes a live gtag script tag (already true if consent-gated client-only).

## Privacy Policy

Update the Cookies / Analytics sections to state:

- Analytics loads only when allowed (EEA/UK after Allow all; outside those regions without a prompt when geo says so)
- Reject unnecessary keeps sign-in and security storage and never loads the analytics script
- Choice is remembered in local storage on this browser
- Clearing site data forgets the choice

Bump the policy updated date.

## Files to add or touch (Next.js checklist)

| Path | Role |
|------|------|
| `lib/cookie-consent.ts` | Country set, storage, allow/show rules, shared region resolve |
| `lib/geo-country.ts` | Header + IP country helpers |
| `app/api/geo/route.ts` | Same-origin geo JSON |
| `app/cookie-consent-banner.tsx` | Toaster UI |
| `app/analytics.tsx` (or equivalent) | Consent-gated GA install |
| `app/layout.tsx` | Mount banner + analytics |
| Global CSS / design tokens | `.cookie-consent*` toaster styles |
| Privacy page | Document the chooser |
| Tests | Pure helpers + SSR banner empty |

## Verification

1. **Non-EU (or forced `not_required`):** no banner; with GA ID set, network shows `googletagmanager.com/gtag/js` after load.
2. **EU force for local test:**

```js
localStorage.removeItem('{prefix}.cookieConsent');
localStorage.setItem('{prefix}.consentRegion', 'required');
location.reload();
```

3. Click **Allow all** → Network filter `googletagmanager` / `google-analytics` shows the library and a collect hit.
4. Click **Reject unnecessary** → no gtag script; reload stays dark.
5. Confirm CSP already allows GA origins only when the measurement ID is configured (see `/senternet-site-csp` and `/senternet-site-google-analytics`).
6. Confirm Firebase anonymous sign-in still runs for a rejecter.

## What not to do

- Do not put the measurement ID in committed local `.env` permanently; production owns it (`apphosting.yaml` or CI secrets).
- Do not gate Firebase anonymous auth or reCAPTCHA behind the reject path.
- Do not use `next/script` `afterInteractive` as the only path for post-consent inject.
- Do not call a third-party geo API from the browser when a same-origin route can do it.
- Do not add `ClaimReview` or other product-specific schema as part of this skill.
- Do not show the bar worldwide "to be safe" unless the product is EEA-only; the product requirement here is geo-scoped.

## Framework: Next.js track

Primary target of this skill (App Router + App Hosting). Use `NEXT_PUBLIC_GA_ID`, route handlers under `app/api/`, and client components for the banner and gate. List any new public env in `apphosting.yaml` with BUILD availability.

## Framework: Vite track

Same behavior, different wiring: no `app/api` by default; use a Hosting rewrite or Functions endpoint for geo. Strip or consent-gate the `index.html` GA block from `/senternet-site-google-analytics`. Use `VITE_GA_ID` and the existing htmlPlugin only if the injected snippet defers the real library until consent.

See `/senternet-site-framework` for the convention map and `/senternet-site-google-analytics` for Measurement ID provisioning.
