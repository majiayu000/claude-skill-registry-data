---
name: meta-conversions-api-and-datasets
description: Implement and QA server-side Meta Conversions API (CAPI) events into a dataset with correct SHA-256 hashing, deduplication against the browser Pixel via a shared event_id, and Event Match Quality monitoring. Use when the user asks about Meta CAPI, Facebook Conversions API, dataset events, the Pixel plus server setup, hashing user_data, em/ph/fn normalization, event_id deduplication, duplicate conversions, Event Match Quality, EMQ, the Dataset Quality API, test_event_code, or why server events are not matching or are double-counting.
---

# Meta Conversions API and datasets

Stand up server-side Meta conversions that a campaign can actually optimize on: send well-formed events to a dataset, hash the customer information the way Meta requires, deduplicate them against the browser Pixel with a shared `event_id`, and watch Event Match Quality (EMQ) so match rates do not silently rot. The Conversions API (CAPI) posts events from your server straight to the dataset (formerly the Pixel), which is what keeps measurement alive as browser signal drops.

This skill assumes you know what a conversion, a match key, and a Pixel are. For the shared measurement math and the 2026 signal-loss picture, see the `programmatic-foundations` and `privacy-sandbox-and-signal-loss-2026` skills.

## When to use this skill

- "Set up the Meta Conversions API / Facebook CAPI for server-side events."
- "How do I hash email and phone for `user_data`?" / "Why is my `em` / `ph` not matching?"
- "I am double-counting conversions." / "How do I dedupe the Pixel and server events?"
- "What is Event Match Quality and why is mine 4 out of 10?"
- "Pull the Dataset Quality API." / "Which match keys am I missing?"
- "My server events are rejected." / "Events older than 7 days error out."
- "What `action_source` do I send for a phone order / in-store sale?"

Boundaries with sibling skills:
- TikTok server events (Events API 2.0, consolidated endpoint): `tiktok-events-api-server-side`.
- Microsoft UET plus its CAPI: `microsoft-uet-and-conversions-api`.
- Google Ads and Floodlight server-side via server GTM: `gtm-server-conversion-enhancement`.
- Consent-string decode and proving denied users were suppressed: `consent-signal-verification-and-decode`.
- Reconciling Meta-reported conversions against other platforms and the warehouse: `cross-platform-conversion-reconciliation`.
- Deep field maps, normalization tables, and the Dataset Quality API query pattern live in this skill's `references/` (linked below), not in the body.

## Quick reference

| Situation | Do this | Why |
| --- | --- | --- |
| Web conversion also fired by the Pixel | Send server event with the SAME `event_id` and `event_name` | Meta dedupes the pair and keeps one |
| Server-only event (phone order, CRM, offline) | Set `action_source` to `phone_call`, `physical_store`, `system_generated` | No browser event exists to dedupe against |
| Any PII match key (email, phone, name, DOB, zip) | Normalize, then SHA-256, then send the hex digest | Meta never accepts raw PII in these fields |
| IP, user agent, `fbp`, `fbc`, `fb_login_id`, `lead_id` | Send raw, do NOT hash | Hashing them breaks matching |
| Event happened more than 7 days ago | Do not send it | `event_time` older than 7 days rejects the whole request |
| Match rate looks low | Pull EMQ from the Dataset Quality API and read `match_key_feedback` | Tells you which keys to add or fix |
| Testing before go-live | Add `test_event_code`, verify in Events Manager, then REMOVE it | A live payload with a test code will not count |

Two things must be true for a healthy CAPI setup: (1) the same real conversion carries one stable `event_id` on both the Pixel and the server so it is counted once, and (2) `user_data` carries enough correctly hashed match keys that EMQ stays high. Miss the first and you double-count. Miss the second and the event lands but cannot be attributed.

## Core process

1. Create or identify the dataset. In Events Manager, the dataset is the object that receives both Pixel and server events, and its numeric ID is what you POST to. Confirm you are pointing at the right dataset before sending anything, because events sent to the wrong ID are unrecoverable.
2. Mint a system user access token. Generate a system user token in Business Settings with the dataset assigned and the `ads_management` permission, so the token survives a person leaving and is not tied to a personal login. Store it in an environment variable or a secrets manager, never in code.
3. Map your events to Meta event names. Use standard events (`Purchase`, `Lead`, `AddToCart`, `CompleteRegistration`, `InitiateCheckout`, `ViewContent`) where one fits, because standard events unlock optimization and reporting that custom events do not. Reserve custom event names for genuinely bespoke actions.
4. Assemble `user_data`. Collect every match key you legitimately have (email, phone, name, city, state, zip, country, DOB, external ID, plus `fbp` and `fbc` from the browser when available). More correct keys means higher EMQ, so pass all you have.
5. Normalize and hash the PII keys. Lowercase and trim, apply the per-field normalization (phone to digits with country code, DOB to `YYYYMMDD`, and so on), then SHA-256 each and send the lowercase hex digest. Do not hash IP, user agent, `fbp`, `fbc`, `fb_login_id`, or `lead_id`. The full table is in `references/hashing-and-dedup-rules.md`.
6. Set `event_id` for deduplication. Generate one stable ID per real conversion and put the identical value on the browser Pixel event and the server event, so Meta collapses the pair. See the dedup section below.
7. Set `event_time` and `action_source`. `event_time` is a Unix timestamp in seconds and must be within the last 7 days. `action_source` names where the conversion happened (`website`, `app`, `phone_call`, `physical_store`, `email`, `chat`, `business_messaging`, `system_generated`, `other`).
8. POST to the events edge. Send `POST https://graph.facebook.com/v25.0/{dataset_id}/events` with the events in a `data` array (up to 1,000 per request) and the access token. Read the response for `events_received` and any `messages` warnings.
9. Validate with a test event code first. Add `test_event_code`, confirm the event appears in the Events Manager Test Events tab within about 20 minutes, then remove the code before going live. A payload that still carries a test code will not be counted for optimization.
10. Monitor EMQ and coverage. Pull the Dataset Quality API on a schedule, read the composite EMQ score and `match_key_feedback`, and alert when EMQ drops or a key's coverage falls. See `references/emq-and-dataset-quality-api.md`.

Safe by default: this skill reads and recommends. Any change that alters what a live campaign optimizes on (swapping the optimization event, turning off the Pixel, changing dedup keys in production) is a human-gated decision, not something to push silently.

## Decision rules and thresholds

### Deduplication (the double-counting killer)

- Meta deduplicates a browser Pixel event and a server event when they share the same `event_id` AND the same `event_name`. Both must match. Same ID with a different event name will not dedupe.
- Generate the `event_id` once per real conversion (a UUID or your order ID works) and stamp it on both the client-side Pixel event and the server-side CAPI event for the same action.
- When both arrive, Meta keeps one and drops the duplicate, so send both without fear. Redundancy is the point: the server event backstops the Pixel when the browser drops it.
- If you only have a server event (offline, phone, CRM), there is no Pixel counterpart, so `event_id` is still good practice for idempotency but dedup does not apply.
- The failure mode is a missing or mismatched `event_id`: you then count the Pixel and the server hit as two conversions. Audit for inflated counts after any CAPI launch.

### Hashing rules (matching lives or dies here)

- Hash every PII match key with SHA-256 after normalizing: `em`, `ph`, `fn`, `ln`, `ct`, `st`, `zp`, `country`, `db`, `ge`. Send the lowercase hexadecimal digest.
- Never hash: `client_ip_address`, `client_user_agent`, `fbp`, `fbc`, `fb_login_id`, `lead_id`, `subscription_id`, `external_id` (hashing external ID is allowed but optional, and consistency matters more than hashing it).
- Normalize before hashing or the hash will not match Meta's: lowercase and trim email; strip everything but digits from phone and prepend the country code (US is `1`); DOB to `YYYYMMDD`; state to lowercase two-letter code; zip to the first 5 digits lowercased; country to ISO 3166-1 alpha-2 lowercase.
- One wrong normalization step silently zeroes a key's match value. The event still posts, so the only way you catch it is EMQ and `match_key_feedback`.

### Event Match Quality thresholds

- EMQ is a 0 to 10 composite score of how well your `user_data` can match to Meta accounts. It is web-only today.
- Treat below 6.0 as a problem worth fixing and aim for 7.0 or higher. Low EMQ means events land but attribute poorly, so optimization degrades even though your dashboards show events flowing.
- Do not chase 10.0 by inventing data. Add the keys you legitimately have (email and phone move the score most), fix normalization, and make sure `fbp` and `fbc` are captured client-side and forwarded.

### `event_time` freshness

- `event_time` can be at most 7 days in the past. An event older than 7 days rejects the entire request, not just that event, so batch carefully and drop stale rows before sending.
- For offline or delayed pipelines, send within the window or the conversions are lost.

### Consent gating

- Do not send `user_data` for a user who did not consent to advertising data use. Server-side sending does not exempt you from consent; it moves where the call happens, not whether it is lawful.
- In consent-required regions, gate the CAPI call on the same consent signal that gates the Pixel. For decoding and verifying the consent string, and proving denied users were suppressed, hand off to `consent-signal-verification-and-decode`.

## Reference material

- `references/dataset-and-required-fields.md`: the dataset object, the events edge and request envelope, required versus optional server-event fields, the `action_source` enum, `custom_data` for value and currency, standard event names, and the response fields. Read this when building or debugging the request payload.
- `references/hashing-and-dedup-rules.md`: the full per-field normalization and SHA-256 table (which keys hash, which never do), worked normalization examples, and the `event_id` deduplication contract between the Pixel and the server. Read this when a match key is not matching or you are double-counting.
- `references/emq-and-dataset-quality-api.md`: the Dataset Quality API endpoint and method, the EMQ composite score, `match_key_feedback` and `diagnostics`, additional-conversions and coverage metrics, and a query and alerting pattern. Read this when match rates look low or you are setting up quality monitoring.

## Templates and examples

Standard web `Purchase`, deduped against the Pixel (values illustrative):

```json
POST https://graph.facebook.com/v25.0/1234567890/events
{
  "data": [
    {
      "event_name": "Purchase",
      "event_time": 1751414400,
      "event_id": "order_10482",
      "action_source": "website",
      "event_source_url": "https://shop.example.com/checkout/success",
      "user_data": {
        "em": ["8f9dc3...<sha256 of jane@example.com>"],
        "ph": ["a1b2c3...<sha256 of 13105551234>"],
        "fn": ["e5f6...<sha256 of jane>"],
        "ln": ["c7d8...<sha256 of doe>"],
        "ct": ["...<sha256 of losangeles>"],
        "st": ["...<sha256 of ca>"],
        "zp": ["...<sha256 of 90025>"],
        "country": ["...<sha256 of us>"],
        "fbp": "fb.1.1751414000000.0987654321",
        "fbc": "fb.1.1751414000000.IwAR1abc",
        "client_ip_address": "203.0.113.7",
        "client_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
      },
      "custom_data": { "currency": "USD", "value": "148.00" }
    }
  ],
  "access_token": "<SYSTEM_USER_TOKEN_FROM_ENV>"
}
```

The browser Pixel fires the same `Purchase` with `eventID: "order_10482"`. Because `event_id` and `event_name` match, Meta keeps one.

Server-only phone order (no Pixel counterpart, so no dedup partner):

```json
{
  "event_name": "Purchase",
  "event_time": 1751410800,
  "event_id": "call_55231",
  "action_source": "phone_call",
  "user_data": {
    "ph": ["...<sha256 of 13105559876>"],
    "em": ["...<sha256 of buyer@example.com>"]
  },
  "custom_data": { "currency": "USD", "value": "320.00" }
}
```

Normalization before hashing (feed these strings, not the raw ones, into SHA-256):

- `Jane@Example.com ` becomes `jane@example.com`
- `(310) 555-1234` (US) becomes `13105551234`
- `2/16/1997` becomes `19970216`
- `Los Angeles` becomes `losangeles`
- `90025-1234` becomes `90025`

## Common pitfalls

- Missing or mismatched `event_id`. The Pixel and server events are counted twice. Stamp the identical `event_id` and `event_name` on both. Audit conversion counts right after launch.
- Hashing what must stay raw. Hashing `fbp`, `fbc`, IP, user agent, or `fb_login_id` destroys matching. Only PII keys get hashed.
- Skipping normalization. An unnormalized email or phone hashes to a digest Meta cannot match, so the key is dead weight. The event still posts, which hides the bug until EMQ shows it.
- Leaving `test_event_code` in the live payload. Test events do not count for optimization. Remove the code before go-live.
- Sending stale events. Anything with `event_time` older than 7 days rejects the whole batch. Filter stale rows first.
- Ignoring EMQ. Events flowing is not the same as events matching. A dashboard full of events with EMQ of 3 is optimizing on almost nothing. Monitor EMQ and coverage, not just receipt.
- Ignoring consent. Server-side does not launder a missing consent signal. Gate the call in consent-required regions.
- Wrong `action_source`. A phone or in-store sale tagged `website` misrepresents where the conversion happened and can distort attribution. Match the source to reality.

## Sources

- [Conversions API overview](https://developers.facebook.com/docs/marketing-api/conversions-api/) (as of July 2026)
- [Server event parameters](https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/server-event/) (as of July 2026)
- [Using the Conversions API](https://developers.facebook.com/docs/marketing-api/conversions-api/using-the-api/) (as of July 2026)
- [Dataset Quality API](https://developers.facebook.com/docs/marketing-api/conversions-api/dataset-quality-api/) (as of July 2026)
