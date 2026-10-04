---
name: senternet-site-ccpa
description: Add a California-only CCPA opt-out toaster for analytics cookies (GA may load until the visitor rejects).
---

# CCPA Cookie Notice (California geo + analytics opt-out)

Add a simple analytics privacy toaster for **California** visitors that:

1. **Auto-detects** California (US country **and** state/region CA)
2. Offers **Allow all** / **Reject unnecessary**
3. **May load Google Analytics before** the visitor chooses (opt-out, not opt-in)
4. **Stops tracking** if they reject (disable flag, drop `gtag`, clear `_ga` cookies)
5. Appears as a **footer toaster** matching the site chrome

Reference implementation: Highwire (`www.highwire.news`), which runs **both** GDPR opt-in and CCPA opt-out from one consent module (`regime`: `gdpr` | `ccpa` | `none`).

## When to run

- After `/senternet-site-google-analytics` (or when GA is already wired)
- When the product serves California residents and needs a clear opt-out for analytics
- Prefer pairing with `/senternet-site-gdpr` if EEA/UK traffic also matters; implement **one shared regime system**, not two unrelated banners
- Not needed if the only analytics is cookieless (e.g. Ahrefs Web Analytics alone)

## Design principles

- **Geo-scoped chooser.** Only California sees the CCPA bar. Other US states and the rest of the world do not.
- **State required.** Country `US` alone is **not** CCPA. Region/state must be `CA` or `California`.
- **Opt-out, not opt-in.** Analytics may run until Reject. Contrast with `/senternet-site-gdpr`, which must not load GA until Allow all.
- **Reject must actually stop tracking.** Unmounting a React component is not enough if gtag and `_ga` cookies already exist. Set `window['ga-disable-' + gaId] = true`, attempt `gtag('consent', 'update', …)`, remove `window.gtag`, clear `_ga` / `_gid` / `_ga_*` cookies.
- **Analytics is the only third-party cookie gated.** Auth sessions and reCAPTCHA stay on. Do not gate anonymous Firebase behind this banner.
- **Choice in localStorage**, not a consent cookie: `{prefix}.cookieConsent`, `{prefix}.consentRegion` (or `consentRegime`).
- **Never use em dashes** in copy, comments, or docs.

## Legal notes (keep short, do not overclaim)

- CCPA/CPRA gives California residents rights around sale/share of personal information and opt-outs for certain tracking. This skill implements a practical **analytics opt-out bar** for a marketing or product site, not a full "Do Not Sell or Share" preference center for every vendor.
- If the product sells data or runs ad pixels, expand beyond GA; this skill alone is not a complete CCPA program.
- This is engineering for a Senternet pattern, not formal legal advice.

## Location set (CCPA regime)

- **Country:** `US`
- **Region:** `CA` or `California` (case-insensitive)
- GDPR countries (EEA/GB) use the **gdpr** regime instead when both skills are applied; GDPR wins if somehow both matched (they should not).

## Shared regime model (preferred)

When both GDPR and CCPA are in scope, store:

| Key | Values | Meaning |
|-----|--------|---------|
| `{prefix}.cookieConsent` | `accepted` \| `rejected` | Explicit choice |
| `{prefix}.consentRegion` | `gdpr` \| `ccpa` \| `none` | Cached geo regime |

**Allow rules for analytics:**

| Regime | No choice | Accepted | Rejected |
|--------|-----------|----------|----------|
| `gdpr` | **off** (opt-in) | on | off |
| `ccpa` | **on** (opt-out) | on | off |
| `none` | on | on | off |
| unknown | off until geo resolves | on | off |

**Show banner when:** regime is `gdpr` or `ccpa` and choice is null.

Legacy caches from GDPR-only ship: map `required` → `gdpr`, `not_required` → `none`.

Fire `{prefix}:cookie-consent` on write so the analytics mount can load **or shut down** without a navigation.

## Geo resolution

Same-origin `GET /api/geo` (Next.js) or Hosting rewrite / Function (Vite):

1. Country headers: `cf-ipcountry`, `x-vercel-ip-country`, `cloudfront-viewer-country`, `x-appengine-country`, `x-country-code`, `x-geo-country`, `x-client-geo-location` (may be `US,CA`).
2. Region headers: `x-vercel-ip-country-region`, `cloudfront-viewer-country-region`, `cf-region-code`, `x-appengine-region`.
3. Client IP from leftmost `X-Forwarded-For` (one hop) or `X-Real-IP`. Skip private/loopback.
4. If country is missing, **or** country is `US` without a region, call a server-side IP geo that returns **state** (e.g. `https://get.geojs.io/v1/ip/geo/{ip}.json` with `region` / `region_code`). Country-only endpoints are not enough for CCPA.
5. Response shape:

```json
{
  "country": "US",
  "region": "CA",
  "regime": "ccpa",
  "consentRequired": false
}
```

`consentRequired` may remain as a legacy GDPR boolean (`true` only for `gdpr`). Prefer `regime` for new clients.

**Failure policy:** network failure → do not cache; keep analytics conservative (off if regime unknown); hide bar; retry next visit. Resolved null location → `regime: "none"`.

Share one in-flight client lookup between banner and analytics.

## UI (footer toaster)

Same chrome as GDPR: fixed bottom toaster, site tokens, Allow all + Reject unnecessary.

**CCPA copy pattern** (adapt brand voice):

> **Your privacy choices**  
> We use analytics cookies to understand how {Product} is used. They are on unless you opt out. Sign-in and security storage always work. See the [Privacy Policy](/privacy).  
> [Reject unnecessary]  [Allow all]

SSR / first paint: render **nothing** until regime is known and is `ccpa` or `gdpr` (no flash for unregulated visitors).

## Gate Google Analytics

### Load rules

- `ccpa` + no choice → **install GA immediately** while the bar is open.
- `ccpa` + reject → **disable** (below); do not reinstall until accept or storage clear.
- `gdpr` → only after accept (see `/senternet-site-gdpr`).
- `none` → install after geo resolves, no bar.

### Install (imperative, not `next/script` afterInteractive for late mounts)

```ts
window.dataLayer = window.dataLayer || [];
if (typeof window.gtag !== 'function') {
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

Clear `window['ga-disable-' + gaId]` before reinstalling after a later accept.

### Disable on reject (required for CCPA)

```ts
window[`ga-disable-${gaId}`] = true;
if (typeof window.gtag === 'function') {
  try {
    window.gtag('consent', 'update', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
    });
  } catch { /* ignore */ }
}
delete window.gtag;
// Expire _ga, _gid, _ga_*, _gat* cookies on Path=/ and common Domain= forms.
```

App Router still needs `page_view` on `usePathname()` after the first config. `trackEvent` no-ops when `gtag` is missing.

### Vite track

Strip or consent-gate the unconditional `index.html` GA block from `/senternet-site-google-analytics`. Mount banner + gate at the app root. Prefer same-origin geo over browser calls to third-party geo APIs.

## Privacy Policy

Document:

- California residents may see analytics load first and can opt out from the notice; Reject stops the script and clears its cookies
- EEA/UK remain opt-in if GDPR is also implemented
- Choice lives in local storage; clearing site data forgets it
- Sign-in / security storage is not gated by Reject

Bump the policy updated date.

## Files to touch (Next.js checklist)

| Path | Role |
|------|------|
| `lib/cookie-consent.ts` | Regimes, storage, allow/show rules, shared resolve |
| `lib/geo-country.ts` | Country + **region**, California class |
| `app/api/geo/route.ts` | `{ country, region, regime }` |
| `app/cookie-consent-banner.tsx` | Toaster (regime-specific copy) |
| `app/analytics.tsx` | Load when allowed; **disable on reject** |
| Privacy page | CCPA opt-out language |
| Tests | `isCalifornia`, allow rules for `ccpa`, geo headers with region |

If `/senternet-site-gdpr` already landed a GDPR-only module, **extend** it to the three-regime model rather than stacking a second banner.

## Verification

1. **Force CCPA locally:**

```js
localStorage.removeItem('{prefix}.cookieConsent');
localStorage.setItem('{prefix}.consentRegion', 'ccpa');
location.reload();
```

2. Banner visible; Network already shows `googletagmanager.com/gtag/js` (opt-out).
3. **Reject unnecessary** → further collect stops; `_ga` cookies cleared; reload stays dark.
4. **Allow all** → bar dismisses; GA continues.
5. Force `none` → no bar; GA loads.
6. Force `gdpr` (if dual regime) → bar without GA until Allow all.
7. Confirm Firebase anonymous still works after reject.

## What not to do

- Do not treat all US traffic as CCPA.
- Do not use country-only IP lookup and claim California detection.
- Do not leave GA running after reject (scripts + cookies still live).
- Do not use `next/script` `afterInteractive` as the only path for consent-time inject.
- Do not gate Firebase anonymous auth or reCAPTCHA.
- Do not invent a second storage key namespace when GDPR is already present; share one.

## Relationship to GDPR skill

| | GDPR skill | CCPA skill |
|---|------------|------------|
| Geography | EEA + GB | California |
| Default | analytics **off** | analytics **on** |
| Choice | opt-in | opt-out |
| On reject | never load | stop + clear |

Implement once with `regime`; run both skills as extend/verify steps when both jurisdictions matter.

## Framework: Next.js track

Primary reference (App Router + App Hosting). `NEXT_PUBLIC_GA_ID` in `apphosting.yaml` with BUILD availability.

## Framework: Vite track

Same behavior; geo via Hosting rewrite or Function; consent-gate the HTML GA block.

See `/senternet-site-framework`, `/senternet-site-google-analytics`, and `/senternet-site-gdpr`.
