---
name: ga4-property-and-data-stream-setup
description: Stand up a Google Analytics 4 property, create web and app data streams, install the Google tag or GTM, and configure enhanced measurement, data retention, reporting identity, and data controls. Use when the user asks how to set up GA4, create a property, add a web or app data stream, get the Measurement ID or G- tag, install gtag.js or GTM, turn enhanced measurement on or off, set data retention, pick a reporting identity, enable Google signals, or prepare a property before events and key events are defined.
---

# GA4 property and data stream setup

Create the GA4 property, wire each web and app data stream to the site or app, and set the property-level controls (enhanced measurement, retention, reporting identity, data controls) so collection is clean before anyone builds events or reports on top of it. Setup mistakes here (wrong data stream, retention left at 2 months, timezone wrong, tag not firing) are expensive to unwind because they corrupt historical data you cannot backfill.

This skill assumes you know what a session, an event, and a conversion pixel are. For KPI math and shared definitions, see the `programmatic-foundations` skill.

## When to use this skill

- "Set up a GA4 property from scratch." / "Create a new property for this brand."
- "Add a web data stream / app data stream." / "Where do I get the Measurement ID (G-XXXX) or the tag?"
- "Install the Google tag / gtag.js / connect GA4 to GTM."
- "Turn enhanced measurement on or off." / "Why is GA4 double-counting scrolls or site search?"
- "Set data retention." / "Reporting identity: Blended, Observed, or Device-based?"
- "Enable Google signals." / "Set the reporting timezone and currency."
- "Create a property through the Admin API." / "Send events server-side with the Measurement Protocol."

Boundaries with sibling skills:
- Designing the event model and marking key events (the 2024+ term for conversions): `ga4-events-and-key-events`.
- Building audiences and exporting conversions to Google Ads, DV360, SA360, Ad Manager, and the June 2026 consent change: `ga4-conversions-and-audiences`.
- Explore workspace analyses and standard reports: `ga4-explorations-and-reporting`.
- BigQuery export config and querying the nested schema: `ga4-bigquery-export-and-sql`.
- GTM container design, the dataLayer contract, and Consent Mode v2 wiring: `gtm-web-container-and-datalayer`, `gtm-tags-triggers-variables`, `gtm-consent-mode-v2`.
- Linking GA4 to CM360 Floodlight and the GMP spine: `gmp-integration-floodlight-ga4-linking`.

## Quick reference

| Decision | Default choice | Why |
| --- | --- | --- |
| Property structure | One property per brand or business unit, not per domain | Cross-domain traffic belongs in one property; splitting by domain fragments the user journey |
| Data stream per property | One web stream per property in most cases; add app streams for iOS and Android | A property unifies streams; multiple web streams for one site inflates users and splits sessions |
| Tag install path | GTM when a tag manager exists or is planned, else the Google tag (gtag.js) direct | GTM decouples tag changes from code deploys and carries Consent Mode cleanly |
| Data retention | Set to 14 months on day one (Standard max) | Default is 2 months; Explore and user-level analysis silently lose history you cannot recover |
| Reporting identity | Blended | Uses User-ID, then Google signals, then device, then modeling for the most complete view |
| Enhanced measurement | On, but disable events you also send manually | Prevents double-counting when your GTM tags already fire scroll, search, or form events |
| Google signals | On only with consent coverage and a business need (audiences, demographics) | It enables cross-device and personalization, which needs the consent and privacy review |

## Core process

1. Create the property under the right account, because the account is the top-level container and moving a property between accounts later is disruptive. Set the reporting timezone and currency at creation, since a wrong timezone shifts every daily boundary and a wrong currency corrupts revenue and ROAS forever forward.
2. Add the data stream that matches the platform. Web stream for a website, iOS and Android app streams for mobile apps (app streams route through Firebase). One property can hold multiple streams and unifies them; do not create a second web stream for the same site just to separate sections, because that inflates user and session counts.
3. Copy the Measurement ID (`G-XXXXXXXXXX`) from the web stream. This is the ID every gtag and GTM GA4 tag references. App streams use a Firebase App ID and the platform SDK instead.
4. Install the tag. Prefer GTM: publish a Google tag or GA4 Configuration tag keyed to the Measurement ID and hand tag design to `gtm-web-container-and-datalayer`. If installing directly, place the gtag.js snippet high in the `<head>` on every page. Verify collection in Realtime and DebugView before calling it done, because a tag that fires on some pages only looks fine in aggregate but breaks attribution.
5. Review enhanced measurement on the web stream. It is on by default and auto-collects page_view, scroll, click (outbound), view_search_results, video engagement, file_download, and form interactions. Disable any event you also send manually through GTM or gtag, so you do not double-count. Set the site-search query parameters if they are not the defaults.
6. Set data retention to 14 months (Standard) immediately. The default of 2 months only affects Explore and user-level and event-level data, not the aggregate standard reports, so the loss is invisible until an analyst needs 13-month-ago cohort data that no longer exists.
7. Choose the reporting identity (Blended is the default and usually correct) and decide on Google signals. Enable Google signals only when you need cross-device reporting, demographics, or Google-based audiences and you have consent coverage for it, because it turns on personalization data flows that a privacy review must sign off.
8. Set data controls before traffic scales: internal-traffic and developer-traffic filters, cross-domain measurement if the journey spans domains, unwanted-referral exclusions (payment gateways), and consent settings. For Consent Mode v2 wiring, hand off to `gtm-consent-mode-v2`.
9. Gate anything that changes billing, personal-data flow, or live config behind a human review: turning on Google signals, linking Google Ads, enabling BigQuery export, and publishing the tag to production. Read and recommend first, then let a human approve the change.

## Decision rules and thresholds

### Property and stream structure

- One property per brand or reporting unit. Consolidate domains that share a user journey into one property with cross-domain measurement, rather than one property per domain.
- One web stream per site. A single property unifies data across its streams, so adding a second web stream for the same site double-counts users. Use separate streams only for genuinely separate platforms (web vs iOS vs Android).
- App analytics run through Firebase. Creating an iOS or Android stream links a Firebase project; the SDK, not gtag.js, sends the data.

### Enhanced measurement (web stream)

Enhanced measurement is on by default. Auto-collected events and their triggers:

| Event | Fires on | Watch for |
| --- | --- | --- |
| `page_view` | Every page load (and history changes for SPAs if enabled) | SPA route changes need the browser-history option on |
| `scroll` | First time a user reaches 90% page depth | Only one scroll event per page, at 90%, so it is not a granular depth metric |
| `click` | Click on a link leaving the current domain (outbound) | Cross-domain links you added to the linker are not outbound |
| `view_search_results` | URL contains a site-search query parameter | Defaults are `q`, `s`, `search`, `query`, `keyword`; set custom ones if your site differs |
| `video_start` / `video_progress` / `video_complete` | Embedded YouTube players with JS API enabled | Only embedded YouTube; other players need manual events |
| `file_download` | Click on a link to a common file type (pdf, docx, xlsx, zip, and more) | Extension list is fixed; unusual extensions need a manual event |
| `form_start` / `form_submit` | First interaction with and submission of a form | Overlaps with manual form events; disable one side to avoid double-counting |

Rule: if a GTM tag or gtag call already sends an equivalent event (your own scroll, search, or form event), disable that enhanced-measurement toggle so the property does not record both. Disabling an enhanced-measurement event does not delete already-collected data; it only stops future collection.

### Data retention

| Tier | Options (months) | Default | Set to |
| --- | --- | --- | --- |
| Standard | up to 14 | 2 | 14 |
| 360 | 2, 14, 26, 38, 50 (XL properties capped at 2) | 2 | as long as the analysis window requires |

Retention governs user-level and event-level data used by Explore and audiences, not aggregate standard reports. Leaving it at 2 means an exploration cannot look back beyond 2 months even though the standard reports still show 14. Turn on "Reset user data on new activity" so an active user's window keeps rolling rather than expiring mid-relationship.

### Reporting identity

| Identity | Uses, in order | Pick when |
| --- | --- | --- |
| Blended | User-ID, then Google signals, then device ID, then modeling | Default; most complete cross-device view when signals and modeling are available |
| Observed | User-ID, then Google signals, then device ID (no modeling) | You want only observed data, no modeled gap-filling |
| Device-based | Device ID only, ignores User-ID and signals | Strict single-device counting, or User-ID and signals are not trusted |

Reporting identity changes how reports resolve users but does not change collected data, so you can switch and compare without data loss. Blended is the default because it deduplicates the same person across devices most aggressively.

### Google signals and consent

- Google signals enables cross-device reporting, demographics and interests, and Google-based remarketing audiences, using data from signed-in Google users who opted into Ads Personalization.
- A June 15, 2026 change decouples the Google signals control from Google Ads cookie collection. After that date, Consent Mode `ad_storage` becomes the single control for whether the Analytics tag collects Google Ads cookies and IDs; Google signals then only controls whether Analytics data is associated with signed-in user information. Later in 2026, `ad_personalization` becomes the exclusive control for using linked Analytics data for personalization in Ads. Details and the activation impact live in `ga4-conversions-and-audiences`.
- Do not enable Google signals as a default reflex. It turns on personalization data flows; confirm consent coverage and a real reporting or audience need first.

### Admin API vs UI, and Measurement Protocol

- Configure one property in the UI; configure many (agency onboarding, templated rollouts) through the GA4 Admin API v1. Key edit methods: `properties.create`, `properties.dataStreams.create` (web, Android, iOS types), `properties.updateDataRetentionSettings`, `properties.googleAdsLinks.create`, and `properties.keyEvents` (the current resource; `conversionEvents` is the deprecated predecessor). Edit calls need the `analytics.edit` scope; read-only calls use `analytics.readonly`.
- The Measurement Protocol (`/mp/collect`) is for server-side and offline events that augment gtag and GTM collection, not a replacement for the browser tag. It requires `measurement_id` (or `firebase_app_id`) plus an `api_secret`, and a JSON body with `client_id` (or `app_instance_id`) and an `events` array. Validate against `/debug/mp/collect` before sending live. Detail and payload shape are in `references/reporting-identity-and-retention.md`.

## Reference material

- `references/ga4-limits-standard-vs-360.md`: every configuration cap that shapes a build (custom dimensions and metrics by scope, key events, audiences, Ads links, Explore sampling and export row limits, retention options) for Standard vs 360. Read this when a build is approaching a limit or when you must justify a 360 upgrade.
- `references/enhanced-measurement-events.md`: the full enhanced-measurement event map with every parameter each event carries, the exact triggers, the site-search parameter defaults, the toggle-off behavior, and the double-counting decision table against manual events. Read this when configuring the web stream or diagnosing inflated scroll, search, video, or form counts.
- `references/reporting-identity-and-retention.md`: reporting identity option details and the order each resolves, the retention field map, the Admin API method table for setup, and the Measurement Protocol request shape with a filled-in payload. Read this when scripting property creation, switching reporting identity, or sending server-side events.

## Templates and examples

New DTC brand, single site `shopexample.com`, US audience:
- One property "ShopExample Web", account "ShopExample Inc", timezone `America/New_York`, currency `USD`.
- One web stream `https://shopexample.com`, Measurement ID `G-A1B2C3D4E5`.
- Install via GTM: one Google tag keyed to `G-A1B2C3D4E5`, published behind a Consent Mode default of denied.
- Enhanced measurement on, but `form_start`/`form_submit` disabled because the checkout sends manual `begin_checkout` and `purchase` through the dataLayer.
- Retention 14 months, reset on new activity on. Reporting identity Blended. Google signals off pending the privacy review.
- Internal-traffic filter for the office IP `203.0.113.0/24`, set to Testing first, then Active after DebugView confirms it tags internal hits.

Agency onboarding 40 client properties from a template:
- Script `properties.create` and `properties.dataStreams.create` through the Admin API v1 with `analytics.edit`, then `updateDataRetentionSettings` to 14 months on each, so no property ships at the 2-month default.
- Read-only nightly audit with `analytics.readonly` flags any property whose retention drifted or whose data stream lost its tag.

## Common pitfalls

- Retention left at 2 months. The default silently caps Explore and user-level lookback while standard reports still show 14, so nobody notices until an analyst needs old cohort data that is gone. Set 14 on day one.
- Wrong timezone or currency at creation. Both apply forward-only and cannot rewrite history. A wrong timezone shifts every day boundary; a wrong currency corrupts all revenue and ROAS. Fix before traffic starts.
- Two web streams for one site. A property already unifies streams, so a second web stream double-counts users and splits sessions. Use one web stream per site.
- Enhanced measurement double-counting. If GTM already sends scroll, site search, video, or form events, enhanced measurement records a second copy. Disable the overlapping toggles.
- Tag on some pages only. A snippet missing from a subset of templates looks fine in aggregate but breaks landing-page and attribution reporting. Verify in DebugView across page types, not just the homepage.
- Google signals switched on by reflex. It starts personalization data flows and needs consent coverage and a privacy sign-off. Enable it only with a real need.
- Treating the Measurement Protocol as the tag. It augments server-side and offline events; it does not replace the browser tag and will not backfill browser context you did not send.

## Sources

- [Set up Analytics for a website and/or app (enhanced measurement)](https://support.google.com/analytics/answer/9304153?hl=en) (as of July 2026)
- [Google Analytics 360 (retention options by tier)](https://support.google.com/analytics/answer/11202874?hl=en) (as of July 2026)
- [Configuration limits](https://support.google.com/analytics/answer/12229528?hl=en) (as of July 2026)
- [Upcoming changes to data controls between Analytics and Ads](https://support.google.com/analytics/answer/17016975?hl=en) (as of July 2026)
- [BigQuery export (streaming and daily)](https://support.google.com/analytics/answer/9358801?hl=en) (as of July 2026)
- [Google signals and cross-device](https://support.google.com/analytics/answer/12800258?hl=en) (as of July 2026)
- [Attribution and attribution models](https://support.google.com/analytics/answer/10596866?hl=en) (as of July 2026)
- [Key events and marking events](https://support.google.com/analytics/answer/13965727?hl=en) (as of July 2026)
- [Google Analytics Admin API v1](https://developers.google.com/analytics/devguides/config/admin/v1) (as of July 2026)
- [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1) (as of July 2026)
- [Measurement Protocol for GA4](https://developers.google.com/analytics/devguides/collection/protocol/ga4) (as of July 2026)
