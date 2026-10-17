---
name: tiktok-events-api-server-side
description: Send server-side TikTok conversions through the Events API 2.0 consolidated endpoint (v1.3) with correct access-token auth, SHA-256 hashing, event_id deduplication against the Pixel, and Test Event validation. Use when the user asks how to set up TikTok Events API, send server-side or offline TikTok conversions, integrate CAPI for TikTok, hash email or phone for TikTok, dedupe browser Pixel and server events, why TikTok events are double-counting or under-matching, what the dedup window is, how to pass ttclid and ttp, or how to validate events with a test event code.
---

# TikTok Events API server-side

Send TikTok conversions from your server through the Events API 2.0 consolidated endpoint instead of relying on the browser Pixel alone. Server-side events survive cookie deletion, ad blockers, and consent-driven Pixel suppression, so they recover conversions the Pixel loses and raise match quality. The job here is the payload and the plumbing: authenticate with an access token, hash the identifiers TikTok expects, share one `event_id` with the Pixel so the two fire streams dedupe instead of double-count, and validate with a test event code before you flip production traffic on.

This skill assumes you know CPA, ROAS, and match rate. For those definitions see the `programmatic-foundations` skill. For the equivalent Meta build (dataset, Event Match Quality, shared `event_id` dedup) see `meta-conversions-api-and-datasets`, and for Microsoft see `microsoft-uet-and-conversions-api`. The mechanics rhyme across all three but the endpoints, field names, and dedup windows differ, so do not copy a payload between them.

## When to use this skill

- "Set up the TikTok Events API" or "send TikTok conversions server-side / offline / from my CRM."
- "Integrate TikTok CAPI" or "move TikTok Pixel events to the server."
- "How do I hash email and phone for TikTok?" or "what fields must be SHA-256 hashed?"
- "My TikTok Pixel and server events are double-counting" or "how does TikTok dedup work?"
- "What is the TikTok dedup window?" (5 minutes to 48 hours, see Decision rules).
- "How do I pass ttclid and ttp?" or "match quality is low, how do I raise it?"
- "How do I validate events before going live?" (Test Events with a `test_event_code`).
- "Which endpoint do I hit now?" (the single consolidated v1.3 endpoint, not the old Web/App/Offline split).

Boundaries with sibling skills:
- Meta server-side events (dataset, EMQ, `fbc`/`fbp`): `meta-conversions-api-and-datasets`.
- Microsoft UET server-side (CAPI endpoint, `msclkid`, EEA consent mode): `microsoft-uet-and-conversions-api`.
- Consent-gating what you are allowed to forward, and decoding TCF/GPP strings to prove suppression: `consent-signal-verification-and-decode` and `privacy-and-consent`.
- Governing pixels and server tags as inventory (ownership, change control): `tag-and-pixel-governance`.
- Reconciling TikTok-reported conversions against GA4 and the DSP: `cross-platform-conversion-reconciliation`.
- TikTok campaign structure, Smart+ automation, and bidding are out of scope here. This skill stops at "the event arrived, matched, and deduped."

## Quick reference

| Decision | Choose | Why |
| --- | --- | --- |
| Which endpoint | The single consolidated v1.3 endpoint (`/open_api/v1.3/event/track/`) | TikTok merged the old Web, App, and Offline endpoints into one; integrate once, tag the source per batch |
| How to authenticate | Long-lived access token in the `Access-Token` header | Events API 2.0 auth is token-based, not per-request signing |
| Which event source | `web`, `app`, or `offline` in `event_source`, plus `event_source_id` | One integration, but each batch declares where the data came from |
| What to hash | Email, phone, and external_id: SHA-256 of normalized value | TikTok matches on hashed PII; unhashed PII is rejected or ignored |
| What not to hash | `ttclid`, `ttp`, IP, user agent | Click ID and cookie are already opaque; IP/UA are matched raw |
| Stop double-counting | Send the same `event_id` from Pixel and server | Dedup keys on event name plus `event_id`; without it both count |
| Dedup window | 5 min to 48 h (Pixel-to-server), 48 h (same-source) | TikTok keeps the first event received and enriches it |
| Before go-live | Fire through a `test_event_code` and watch Test Events | Validates schema, hashing, and match before real traffic counts |

## Core process

1. Provision access. In TikTok Events Manager create or select the web/app/offline event you will feed, then generate a long-lived access token for the Events API. Store the token, the event source ID (the pixel or event set identifier), and the advertiser ID in a secrets manager or environment variables, never in code. The token authorizes writes to that specific event source, so treat it like a password.
2. Decide Pixel-plus-server or server-only. Most web advertisers run both: the browser Pixel for on-page signals and rich context, the server for durability. Offline and CRM conversions are server-only by nature. If you run both, you must dedupe (step 5), or you double-count every web conversion.
3. Build the payload. One request carries a `data` array of events. Each event names the standard action (`CompletePayment`, `PlaceAnOrder`, `AddToCart`, `Lead`, and so on), a UNIX `event_time`, an `event_id`, a `user` object of match keys, and `properties` (value, currency, contents). Match keys drive attribution, so send every one you legitimately have.
4. Hash the PII, pass the rest raw. Normalize then SHA-256 email (lowercase, trim), phone (E.164 digits, drop the plus and spaces), and external_id. Send `ttclid` (the click ID from the landing-page URL parameter), `ttp` (the first-party `_ttp` cookie), IP, and user agent unhashed. The full normalize-and-hash table is in `references/dedup-window-and-match-keys.md`.
5. Share one event_id with the Pixel. For any web conversion that fires both browser-side and server-side, generate a single `event_id` per user action and send the identical value on both paths. TikTok dedupes on event name plus `event_id`; matching values collapse to one counted event, mismatched values count twice.
6. Validate with a test event code. Attach `test_event_code` to the batch and confirm each event lands in the Test Events tab with the fields matched and no errors, before removing the code for production. The step-by-step is in `references/test-event-validation.md`. Never ship a new payload straight to production; a bad `event_time` unit or an unhashed email silently tanks match quality.
7. Ship, then monitor match. After go-live, watch the event's diagnostics and match rate in Events Manager for the first 48 hours. Falling match rate means a field regressed (hashing, missing `ttclid`, wrong currency). This is a read-and-alert step; do not change bidding or budgets off a one-day match dip.

Human-gate anything that changes what leaves your server. Adding a new match key that carries PII, or forwarding events for users who denied consent, is a compliance decision, not an engineering one. Read and recommend; let a human approve the config change.

## Decision rules and thresholds

### Deduplication window and precedence

- Send the same `event_id` on the Pixel and the Events API for every web event that fires on both. This is the one required field for dedup.
- Pixel-to-server dedup applies when the duplicate arrives after 5 minutes and within 48 hours of the first event. A server duplicate inside the first 5 minutes may not dedupe, so do not fire the same event twice within that window on purpose.
- Same-source dedup (Pixel-to-Pixel or server-to-server) applies within 48 hours of the first event.
- TikTok keeps the first event received and enriches it with data from the later duplicate. It does not prefer the server event over the browser event or vice versa, so you cannot rely on "the server one wins." Design your `event_id` so the two paths describe the same action, not so one overrides the other.

### What to hash and what to send raw

- Hash with SHA-256 after normalizing: email, phone number, external_id (your own user ID). Lowercase and trim email; reduce phone to E.164 digits; trim external_id. A hash of a non-normalized value will not match.
- Do not hash: `ttclid`, `ttp`, IP address, user agent. These are matched as sent.
- Send every match key you legitimately hold. Match quality rises with the number of valid identifiers per event; a lone hashed email matches worse than email plus phone plus `ttclid` plus IP and user agent.
- `ttclid` is the strongest web signal because it ties the event to a specific ad click. Capture it from the click-through URL parameter on the landing page and persist it (server session or first-party cookie) so later server events can attach it.

### Event source and the consolidated endpoint

- Hit the single consolidated v1.3 endpoint. TikTok replaced the separate Web (Pixel), App, and Offline endpoints with one, so you integrate once and declare the origin per batch with `event_source` (`web`, `app`, or `offline`) and `event_source_id`.
- Do not build against the retired split endpoints. New integrations should target the consolidated endpoint only; the field map is in `references/consolidated-endpoint-and-auth.md`.

### Timestamp and value discipline

- `event_time` is a UNIX timestamp in seconds. Milliseconds will be read as a date far in the future and the event will be dropped or misattributed. Assert the unit in code.
- Events older than the platform's accepted lookback are ignored for optimization; do not backfill ancient offline conversions and expect them to train bidding.
- For value events send both `value` (a number, not a string) and a 3-letter ISO `currency` (`USD`, `GBP`, `EUR`). A value with no currency, or a currency mismatch against the account, corrupts ROAS reporting.

### Consent before you send

- Only forward events for users whose consent state permits it. Server-side sending does not bypass consent; it moves where the event originates, not whether you are allowed to send it. Decode the consent signal and suppress denied users upstream of the API call. See `consent-signal-verification-and-decode`.

## Reference material

- `references/consolidated-endpoint-and-auth.md`: the consolidated v1.3 endpoint path and method, required headers (`Access-Token`, `Content-Type`), the full request-body field map (`event_source`, `event_source_id`, `data`, `test_event_code`) and per-event fields, how to generate and scope the access token, and rate/batch limits. Read this when building or debugging the request itself.
- `references/dedup-window-and-match-keys.md`: the dedup precedence table (Pixel-to-server, same-source, the 5-minute and 48-hour windows), the full match-key table with normalize-and-hash rules per field, and how `ttclid`/`ttp` are captured and passed. Read this when match quality is low or events double-count.
- `references/test-event-validation.md`: the Test Events workflow, the `test_event_code` mechanics, a validation checklist (schema, hashing, dedup, value/currency), and a decode of the common diagnostic warnings. Read this before every go-live and when the Test Events tab shows a warning.

## Templates and examples

A minimal web `CompletePayment` event, hashed and dedup-ready (values illustrative):

```json
{
  "event_source": "web",
  "event_source_id": "C1A2B3D4E5F6G7H8I9J0",
  "data": [
    {
      "event": "CompletePayment",
      "event_time": 1751472000,
      "event_id": "order_88213_1751472000",
      "user": {
        "email": "b6...9f",
        "phone": "3a...c1",
        "external_id": "7d...e2",
        "ttclid": "E.C.P.abc123def456",
        "ttp": "2f8c1a...",
        "ip": "203.0.113.44",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X)"
      },
      "properties": {
        "value": 129.00,
        "currency": "USD",
        "contents": [
          { "content_id": "SKU-4471", "content_type": "product", "quantity": 1, "price": 129.00 }
        ]
      }
    }
  ]
}
```

- The `email`, `phone`, and `external_id` values above are SHA-256 hashes of normalized inputs, truncated here for readability.
- The same `event_id` (`order_88213_1751472000`) must be sent by the browser Pixel for this purchase, or the two fire streams double-count.
- Offline example: same shape with `event_source: "offline"`, no `ttclid`/`ttp`, matched on hashed email and phone from your CRM.
- Test example: add `"test_event_code": "TEST12345"` at the top level, confirm it appears in Test Events, then remove it for production.

## Common pitfalls

- No shared event_id, so every web conversion double-counts. The single most common failure. Generate one `event_id` per action and send it on both the Pixel and the server.
- Firing the server duplicate inside 5 minutes. Pixel-to-server dedup starts after 5 minutes; a same-action server event sent seconds after the Pixel may not dedupe. Send server events on a slight delay or from the backend that owns the confirmed order.
- Sending PII unhashed, or hashing a non-normalized value. Both destroy match. Lowercase and trim email, E.164 the phone, then SHA-256. A hash of `Jane@Example.com ` will never match `jane@example.com`.
- `event_time` in milliseconds. Seconds only. Milliseconds place the event years in the future and it is dropped.
- Missing `ttclid`. Without the click ID, web events fall back to weaker probabilistic matching and attribution suffers. Capture the URL parameter on the landing page and persist it.
- Value as a string or currency omitted. `"value": "129.00"` or a missing `currency` corrupts ROAS. Send a number and an ISO currency.
- Shipping to production without a test event. A schema or hashing error is invisible until match rate craters days later. Always validate through `test_event_code` first.
- Assuming the server event beats the Pixel. TikTok keeps the first event received and enriches it; there is no server-wins rule. Do not rely on precedence to fix a duplicate design.
- Ignoring consent because it is server-side. Server origin does not grant permission. Suppress denied users before the API call.

## Sources

- [Getting started with the Events API](https://ads.tiktok.com/help/article/getting-started-events-api?lang=en) (as of July 2026)
- [Event deduplication](https://ads.tiktok.com/help/article/event-deduplication?lang=en) (as of July 2026)
- [Events API consolidated endpoint](https://ads.tiktok.com/business/en/blog/events-api-consolidated-endpoint) (as of July 2026)
