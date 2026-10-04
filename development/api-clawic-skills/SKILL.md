---
name: API / Application Programming Interface
slug: api
version: 1.3.7
description: 'Integrates and debugs third-party REST and GraphQL APIs: auth, rate limits, pagination, webhooks, with reference for 147 services. Use when calling Stripe, OpenAI, GitHub, Slack, Twilio, or any external service, when a request that should work returns 401, 403, or 429, times out, hits a CORS error, or silently returns wrong data, when choosing an OAuth flow, signing requests, adding retries with backoff and idempotency keys, verifying webhook signatures, consuming SSE streams, uploading files, polling async jobs, caching with ETags, or syncing API data into a local database — with per-service gotchas and curl examples. Not for designing or building your own API.'
homepage: https://clawic.com/skills/api
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
metadata:
  clawdbot:
    emoji: 🔌
    requires:
      anyBins:
      - curl
      - jq
    os:
    - linux
    - darwin
    - win32
    displayName: API / Application Programming Interface
    configPaths:
    - ~/Clawic/data/api/
    - ~/api/
    - ~/clawic/api/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/api/
      - ~/api/
      - ~/clawic/api/
---

REST and GraphQL API reference for 147 services: authentication, endpoints, rate limits, and per-service gotchas, plus pattern playbooks for everything that goes wrong between you and an API. User preferences live in `~/Clawic/data/api/` — the only location this skill writes (see `setup.md` on first use). If you have data at an old location (`~/api/` or `~/clawic/api/`), move it to `~/Clawic/data/api/`, and say in one line that you moved it and from where.

## When To Use

- User names a service to integrate ("call the Stripe API", "post to a Slack channel") → its section via API Categories below
- A request that "should work" returns 401/403/429, times out, or silently returns wrong data → `debug.md` and the pattern files
- Designing the client side of any integration: retries, pagination, webhooks, streaming, file transfer, async job polling
- Choosing between similar providers in a category (email, auth, media) → compare sections in the same category file
- Not for building your OWN API (routing, schema design, versioning your endpoints) — this skill documents consuming others' APIs

## Quick Reference

| Situation | Read |
|-----------|------|
| Endpoints/auth for a named service | Its category file — API Categories table below |
| 401/403 that "should work", OAuth flow choice, JWT rejected | `auth.md` |
| Works in curl but not in code, works locally but not in prod, TLS errors, mysterious 400s | `debug.md` |
| Duplicated/missing items across pages, loop never ends | `pagination.md` |
| Timeouts, retries, flaky upstream, circuit breakers, provider outage | `resilience.md` |
| 429s, rate-limit headers, quota budgeting, spending less of the limit | `rate-limits.md` |
| Polling for changes, ETag/304 conditional requests, what to cache client-side | `caching.md` |
| Mirroring API data locally, incremental sync, detecting deletions, sync token expired | `sync.md` |
| Blocked by CORS, calling an API from frontend code, key would ship to the browser | `browser.md` |
| SSE stream buffers, hangs, or cuts off; events half-parsed; WebSocket drops | `streaming.md` |
| Receiving events, signature verification, duplicate deliveries | `webhooks.md` |
| Upload rejected with 400/411/413, download corrupted or truncated, presigned URLs | `files.md` |
| 202 Accepted, job polling, batch partial failures, async exports | `async-jobs.md` |
| The service speaks GraphQL (GitHub v4, Shopify, Linear) | `graphql.md` |
| Version pinning, `Sunset`/`Deprecation` headers, provider changed the API | `versioning.md` |
| Sandbox vs live, mocking providers, recorded fixtures, contract drift | `testing.md` |
| Money amounts, timestamps, big numeric IDs, unicode limits in payloads | `data-formats.md` |
| Multiple accounts/keys for one service | `credentials.md` |
| Anything else | Core Rules below, then the Official Docs link at the end of each API section |

## API Categories

| Category | File | Services |
|----------|------|----------|
| AI/ML | `apis/ai-ml.md` | anthropic, openai, cohere, groq, mistral, perplexity, huggingface, replicate, stability, elevenlabs, deepgram, assemblyai, together, anyscale |
| Payments | `apis/payments.md` | stripe, paypal, square, plaid, chargebee, paddle, lemonsqueezy, recurly, wise, coinbase, binance, alpaca, polygon |
| Communication | `apis/communication.md` | twilio, sendgrid, mailgun, postmark, resend, mailchimp, slack, discord, telegram, zoom |
| Realtime | `apis/realtime.md` | sendbird, stream-chat, pusher, ably, onesignal, courier, knock, novu |
| CRM | `apis/crm.md` | salesforce, hubspot, pipedrive, attio, close, apollo, outreach, gong |
| Marketing | `apis/marketing.md` | drift, crisp, front, customer-io, braze, iterable, klaviyo |
| Developer | `apis/developer.md` | github, gitlab, bitbucket, vercel, netlify, railway, render, fly, digitalocean, heroku, cloudflare, circleci, pagerduty, launchdarkly, split, statsig |
| Database | `apis/database.md` | supabase, firebase, planetscale, neon, upstash, mongodb, fauna, xata, convex, appwrite |
| Auth | `apis/auth-providers.md` | clerk, auth0, workos, stytch |
| Media | `apis/media.md` | cloudinary, mux, bunny, imgix, uploadthing, uploadcare, transloadit, vimeo, youtube, spotify, unsplash, pexels, giphy, tenor |
| Social | `apis/social.md` | twitter, linkedin, instagram, tiktok, pinterest, reddit, twitch |
| Productivity | `apis/productivity.md` | notion, airtable, google-sheets, google-drive, google-calendar, dropbox, linear, jira, asana, trello, monday, clickup, figma, calendly, cal, loom, typeform |
| Business | `apis/business.md` | shopify, docusign, hellosign, bitly, dub |
| Geo | `apis/geo.md` | openweather, mapbox, google-maps |
| Support | `apis/support.md` | intercom, zendesk, freshdesk, helpscout |
| Analytics | `apis/analytics.md` | mixpanel, amplitude, posthog, segment, sentry, datadog, algolia |

## How to Navigate API Files

Each category file starts with an index table (API name → line number). Read the index, then only the section you need (50-100 lines each):

```bash
head -20 apis/ai-ml.md          # index
sed -n '139,251p' apis/ai-ml.md # one API's section (OpenAI, per the index)
```

## Core Rules

1. **Raw request before client code.** Reproduce with curl first; if curl succeeds and the SDK fails, the bug is in SDK config (base URL, version pin, auth header name), not the API. Chains: `debug.md`.

2. **Backoff with full jitter, and `Retry-After` overrides it.** `sleep = random(0, min(cap, base × 2^attempt))`, base 1s, cap 30-60s, max `retry_max` attempts (default 4; AWS "full jitter"). Attempt 3 → sleep is a random value in [0, 8s], not exactly 8s — the randomness is what prevents synchronized retry storms. If the 429/503 carries `Retry-After`, obey it instead.

3. **Retry only what cannot double-execute.** GET/PUT/DELETE are idempotent; retry freely. POST only with an idempotency key — a 500 or timeout on POST may have committed server-side (the charge went through, the response didn't). Details and key lifetime: `resilience.md`.

4. **Status triage in this order: 401 → credential, 403 → permission, 404 → maybe permission too.** 401 = the API doesn't know who you are (missing/expired/malformed token). 403 = it knows you and says no (scope, plan tier, IP allowlist). Some APIs (GitHub among them) return 404 for resources you lack access to, to avoid confirming existence — a "not found" on a resource you know exists is an auth bug, not a URL bug.

5. **HTTP 200 is not success.** Check the body for `error`/`errors` fields (GraphQL always returns 200 — `graphql.md`), batch endpoints for per-item failures (207 Multi-Status or a 200 with a mixed `results` array — `async-jobs.md`), and streams for completion (`streaming.md`).

6. **Both timeouts, always.** Set connect and read timeouts explicitly; a request without them hangs forever on a dead upstream. Values and rationale: `resilience.md`; for streams, read timeout means inter-chunk idle (`streaming.md`).

7. **Credentials in headers, never in URLs.** Query-param keys land in access logs, proxy caches, and browser history. Env vars only; naming scheme for multi-account setups: `credentials.md`.

8. **Paginate to completion or say you didn't.** Terminate on the API's own signal (`has_more`, next cursor absent) — never on item count alone. If you stop early, state that results are partial.

## Status Triage

Beyond Core Rule 4's 401/403/404 chain:

| Code | Meaning | First move |
|------|---------|-----------|
| 400 | Request malformed or rejected | Read the body's error field, then `debug.md` Mysterious 400s |
| 405 | Method not allowed | Wrong verb — or a redirect: clients follow 301/302 on POST by re-issuing GET (trailing-slash URLs are the classic trigger) |
| 409 | State conflict | Re-fetch current state; concurrent edit or duplicate create |
| 410 | Gone permanently | Retired resource or API version (`versioning.md`); expired sync token (`sync.md` Sync Tokens) |
| 412 | Precondition failed | Your `If-Match` ETag is stale — re-read, re-apply, retry |
| 415 | Unsupported media type | `Content-Type` missing or wrong (top trap below) |
| 422 | Validation failed | Well-formed but semantically rejected — field-level errors are in the body |
| 429 | Rate limited | `rate-limits.md`; obey `Retry-After` |
| 500 | Server bug | Retry only idempotent requests (`resilience.md` Retry Logic) |
| 502/503/504 | Edge/LB failure or overload, often with an HTML body | Backoff and retry; check the status page (`resilience.md` Provider Outages) |

## Output Gates

Before emitting integration code or a diagnosis, check:

- Every POST/PUT/PATCH example includes `Content-Type: application/json` (or the API's required type)
- No secret appears in a URL, code literal, or logged output — env var references only
- Every pagination loop terminates on the API's `has_more`/cursor signal, not on `len(items)`
- Retry logic distinguishes 4xx (don't retry, fix the request) from 429/5xx (backoff and retry)
- Webhook handler verifies signature on the raw body before parsing (→ `webhooks.md`)
- Money handled in the currency's own convention (minor units, exponent), IDs as strings (→ `data-formats.md`)
- Examples reference the `default_environment` credential (sandbox unless the user asked for live)

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/api/config.yaml` (loading and recording procedure: `setup.md`).

| Variable | Type | Default | Effect |
|---|---|---|---|
| example_language | curl \| python \| javascript \| go | curl | Language every request example is rendered in, across all category and pattern files |
| client_style | raw \| sdk | raw | Whether examples use raw HTTP or the provider's official SDK (tradeoff: Where Experts Disagree) |
| default_environment | sandbox \| live | sandbox | Which credential examples reference (`credentials.md` naming); live only on explicit request — enforced by the last Output Gate |
| retry_max | number (0-10) | 4 | Retry ceiling used in Core Rule 2's formula and all generated retry code |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Tooling**: HTTP client library (requests/httpx, axios/fetch, net/http) and testing tool (curl, HTTPie, Postman) — shapes every snippet
- **Integrations**: the user's chosen provider per category (payments → Stripe, email → Postmark) — which service section answers a generic ask
- **Conventions**: credential env-var naming (default scheme: `credentials.md`), error-handling style (exceptions vs result values) — shapes generated code
- **Thresholds**: org-mandated timeouts and retry budgets — override the `resilience.md` defaults when stated
- **Safety posture**: whether examples may include write/mutating calls, confirm-before-live behavior — tightens or relaxes the environment gate
- **Output format**: snippet-only vs annotated walkthrough — answer verbosity

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Missing `Content-Type` on POST | Many APIs parse the body as form-encoded or reject with an unhelpful 400/415 | Always send `Content-Type: application/json` with JSON bodies |
| Trusting the default page size | Defaults are small; you silently process a fraction of the data | Loop until the API's completion signal (→ `pagination.md`) |
| Retrying 400 Bad Request | The request itself is invalid; identical retries burn quota and can trigger abuse detection | Fix the payload; retry only 429/5xx |
| Copy-pasted token fails with 401 | Trailing newline or wrapping quotes from the clipboard corrupt the header | `echo -n`, or trim before use |
| Testing against production keys | Live-mode side effects (real charges, real emails) during development | Sandbox key first; gate and prefixes in `testing.md` and `credentials.md` |
| One giant try/catch around the whole call | 401, 429, and 500 need different responses; a generic catch retries the unretryable | Branch on status class before any retry |
| Parsing each network chunk as one SSE event | TCP splits and merges events arbitrarily; JSON parse fails mid-token | Buffer to the blank-line delimiter (→ `streaming.md`) |
| Numeric IDs parsed as numbers | 64-bit IDs overflow JS's 2^53−1 and round silently | Treat every ID as an opaque string (→ `data-formats.md`) |
| Buffering a whole download in memory | Multi-GB export = OOM that dev-sized data never showed | Stream to disk; verify against `Content-Length` (→ `files.md`) |
| Calling a third-party API straight from the browser | Most APIs send no CORS headers, and any key in the bundle is public | Proxy through your backend; only provider-designated browser-safe keys ship client-side (→ `browser.md`) |

## Where Experts Disagree

- **Official SDK vs raw HTTP.** SDKs win where auth is hard (request signing, OAuth refresh) and lose freshness — new endpoints land in the API before the SDK. Default: raw HTTP for simple bearer-token APIs; SDK when the provider signs requests or its docs treat the SDK as the primary interface. `client_style` records the user's side.
- **Webhooks vs polling.** Webhooks for volume and latency; polling is legitimately simpler when events are rare, no public endpoint can be hosted, or the poll interval is acceptable staleness. The wrong answer is webhooks without the full handler order (`webhooks.md`).
- **Idempotency keys on every POST vs only where double-execution hurts.** Every-POST buys uniform retry safety; minimalists note the bookkeeping cost. Boundary: any POST whose duplicate the user would notice (charge, email, order) gets a key — no exceptions there, optional elsewhere.

## Security & Privacy

This skill is documentation: endpoint reference, auth patterns, and example requests for the external services listed above. Example endpoints belong to the respective providers (Stripe, OpenAI, etc.).

It does NOT:
- Store or manage API keys or secrets — it references env-var names; values are never read, printed, or persisted
- Make API calls on its own — the user runs the requests
- Send data to any external service

Guardrails:
- Credential discovery lists variable NAMES, never values (`credentials.md` Selection Rules)
- Sandbox/test credentials by default; live keys only on explicit user request
- Generated webhook handlers always verify signatures before parsing the payload

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/api (install if the user confirms):

- `http` — HTTP request patterns
- `webhook` — Webhook handling
- `json` — JSON processing

## Feedback

- If useful, star it: https://clawic.com/skills/api
- Latest version: https://clawic.com/skills/api

---

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/api.
