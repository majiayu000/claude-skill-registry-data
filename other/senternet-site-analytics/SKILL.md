---
name: senternet-site-analytics
description: Help the user choose among Google Analytics, PostHog, and Ahrefs Web Analytics (any combination), then hand off to each matching setup skill.
---

# Analytics Router

Use this skill when the user wants analytics on the site but has **not** yet picked a provider. It routes across Google Analytics 4, PostHog, and Ahrefs Web Analytics, then hands off — it does not implement anything itself.

## Choosing a provider

Whenever the user wants analytics, prompt them for which provider(s) they prefer. Any combination is valid — one, two, or all three. They don't conflict: all load lazily and gate on production. Present the options, then route:

- **Google Analytics 4** → run `/senternet-site-google-analytics`. Best for marketing-site traffic measurement, acquisition channels, and Search/Ads integration. Pairs naturally with the Firebase project this suite already sets up.
- **PostHog** → run `/senternet-site-posthog`. Best for product analytics: events, funnels, retention, and session replay on an app-like site.
- **Ahrefs Web Analytics** → run `/senternet-site-ahrefs-web-analytics`. Best for free, privacy-friendly, cookieless traffic and acquisition analytics; a lightweight GA4 alternative that needs no Firebase/Google linking.

Quick guidance when the user is unsure:

- Marketing/brochure site, cares about traffic sources and SEO → **GA4** or **Ahrefs Web Analytics**.
- Wants traffic analytics without cookies, consent banners, or a Google/Firebase dependency → **Ahrefs Web Analytics**.
- App, dashboard, or interactive product where per-user behavior and funnels matter → **PostHog**.
- Wanting more than one is valid — they don't conflict. Set them up in turn; all load lazily and gate on production.

## Handoff rules

- Once the provider(s) are known, hand off immediately to the target skill(s) and stop.
- When multiple providers are chosen, hand off to each setup skill in turn.
- Do not repeat or preview the target skill's setup steps here.
- Do not explain the options at length unless the user explicitly asks for a comparison.

## Framework note

Provider selection is framework-independent — the same three options apply on both tracks. Only the wiring differs, and each provider skill has a **Framework: Next.js track** section covering it. The one rule worth knowing before you choose: on the Next.js track every client-read variable is `NEXT_PUBLIC_*` and must also be listed in `apphosting.yaml` with `BUILD` availability, or the provider silently never initializes in production.

See `/senternet-site-framework` for the full convention map.
