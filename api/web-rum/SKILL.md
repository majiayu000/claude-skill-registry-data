---
name: web-rum
category: observability
description: Use when an "enable observability" card asks for rum on a frontend, or web.* signals are unbound - how the developer collects Core Web Vitals and page views (web-vitals to the app's own endpoint as log lines, or Sentry / PostHog), what each event must carry, and what stays out of it
source: GoogleChrome/web-vitals (Apache-2.0), getsentry/sentry-javascript and PostHog docs (MIT), adapted
---

# Real-user monitoring for a web frontend

What the frontend's golden signals need: Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout Shift (judged at the 75th percentile), page views, and front-end errors. Choose one path per app; never ship two RUM SDKs.

## Path 1 — the app's own backend (no vendor)

1. Add `web-vitals` and report every metric once per page view:
   `onLCP(send); onINP(send); onCLS(send); onFCP(send); onTTFB(send);` where `send` posts `{name, value, rating, id, navigationType, page, release}` with `navigator.sendBeacon('/api/rum', body)` (falling back to `fetch(..., {keepalive: true})`).
2. Page views: one event per route change from the router (not per render).
3. The backend's `/api/rum` endpoint validates the body (known `name`, a number `value`, a bounded size), rate-limits by client, and writes **one structured log line per event** — `event=web_vital name=LCP value=2310 rating=needs-improvement page=/checkout release=1.42.0` — and answers 204. Those lines are what a logs data source (Loki, Elasticsearch, the cloud's logging) reads; the `web.*` signals bind to them.
4. Front-end errors: `window.addEventListener('error' | 'unhandledrejection')` posting the message, stack, page and release to the same endpoint as `event=frontend_error`.

`page` is the route pattern (`/orders/:id`), never the raw URL: ids and query strings are personal data and explode the label count.

## Path 2 — Sentry

`@sentry/browser` (or `@sentry/react`, `@sentry/nextjs`) with `browserTracingIntegration()`; `release` and `environment` set from the build, `tracesSampleRate` 0.1 in production. Web Vitals and errors come with it; a `sentry` data source reads its issues and release health.

## Path 3 — PostHog

`posthog-js` with `capture_pageview: 'history_change'` for single-page apps and `capture_performance` for web vitals; the project key is public, the host is the team's PostHog instance.

## Either way

- No personal data in any event: no email, name, token, form value or full URL.
- Sample when traffic is high (10% of sessions still gives a stable p75).
- The release version rides on every event, so a deploy-impact read can compare before and after.

Acceptance criteria: "Given a visitor loads /checkout in production, then an LCP event for page /checkout with this release's version is readable from <data source> within a minute"; "Given a page throws, then a frontend_error event with its stack is recorded."
