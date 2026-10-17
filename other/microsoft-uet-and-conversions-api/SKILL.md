---
name: microsoft-uet-and-conversions-api
description: Instrument Microsoft Advertising conversion tracking with the UET tag (browser) and the Conversions API (server-side CAPI). Use when the user asks about UET, the UET tag, Microsoft Advertising conversion tracking, Bing Ads tracking, the Conversions API, capi.uet.microsoft.com, adStorageConsent, EEA/UK/Switzerland consent mode, hashing email and phone for enhanced conversions, msclkid capture, ID sync, or deduplicating browser and server events.
---

# Microsoft UET and Conversions API

Set up Microsoft Advertising conversion measurement so events actually match, attribute, and survive cookie loss: the UET tag for the browser path, the Conversions API (CAPI) for the server path, both keyed to the same UET tag ID. UET is the framework that records site actions for conversion goals, remarketing, automated bidding, and Merchant Center; CAPI sends those same events server-to-server so you keep signal when the browser blocks the tag.

This skill assumes you know what a conversion, a click ID, and SHA-256 hashing are. For KPI math and shared definitions, see the `programmatic-foundations` skill. This is the Microsoft-specific counterpart to `meta-conversions-api-and-datasets`, `tiktok-events-api-server-side`, and `gtm-server-conversion-enhancement`; the mechanics differ per platform, so do not copy field names across them.

## When to use this skill

- "Set up UET" / "add the UET tag" / "Microsoft Advertising conversion tracking" / "Bing Ads conversion tracking."
- "Send server-side conversions to Microsoft" / "Conversions API" / "CAPI" / "capi.uet.microsoft.com."
- "How do I deduplicate the UET tag and the CAPI events?"
- "adStorageConsent" / "ad_storage granted or denied" / "consent mode for EEA, UK, Switzerland."
- "Hash email and phone for enhanced conversions" / "em and ph fields."
- "Capture msclkid" / "why are my Microsoft conversions not attributing to clicks."
- "ID sync" / "c.bing.com/c.gif" / "remarketing is not building an audience from CAPI."

Boundaries with sibling skills:
- Meta CAPI dataset, Event Match Quality, event_id dedup: `meta-conversions-api-and-datasets`.
- TikTok Events API 2.0, consolidated endpoint, TikTok dedup window: `tiktok-events-api-server-side`.
- Google Ads and Floodlight server-side routing through a server container: `gtm-server-conversion-enhancement`.
- Decoding TCF and GPP consent strings to prove suppression: `consent-signal-verification-and-decode`.
- DSAR, deletion, and sub-processor governance across platforms: `data-subject-rights-and-subprocessor-governance`.

## Quick reference

| Decision | Choose | Why |
| --- | --- | --- |
| Standard site, can run JavaScript | UET tag only | Auto-tags, handles the complexity, powers UET Insights and Clarity |
| Browser blocks the tag, ad blockers, ITP, or you need durable signal | UET tag plus CAPI (same tag ID) | CAPI recovers server-side events the browser drops |
| Backend-only integration, no Microsoft JS allowed | CAPI plus a client-side ID sync pixel | ID sync is the only way to capture Microsoft third-party cookie IDs |
| Traffic from EEA, UK, or Switzerland | Consent mode is mandatory (pass `ad_storage`) | Required since May 5 2025; missing signals lose attribution and remarketing |
| Remarketing or audience targeting off CAPI | Client-side ID sync pixel is required | Server events alone cannot resolve off-site identity |
| Conversion attribution off CAPI | Always include `msclkid` | vid alone is not sufficient to attribute a click |

CAPI endpoint at a glance:

- URL: `https://capi.uet.microsoft.com/v1/{tagId}/events`, HTTP POST, JSON body.
- Auth: `Authorization: Bearer <ApiToken>` (token from the UET Tag section in the Microsoft Advertising UI, pilot).
- Success: HTTP 200. Failure: HTTP 400 (validation) or 401 (bad or missing token).
- Batch max: 1,000 events per request. `eventTime` must be a UNIX epoch seconds value within the last 7 days.

## Core process

1. Provision or reuse a UET tag in the Microsoft Advertising account, because both the browser tag and CAPI are keyed to the same `tagId`. One tag can serve all conversion goals and remarketing lists. Create a second, dedicated CAPI tag only when you deliberately want to avoid commingling browser and server events.
2. Install the browser UET tag sitewide, in the head or the site-wide layout, so it fires once per page. This is the default path and captures `msclkid` from auto-tagged landing pages automatically.
3. Define conversion goals against the tag (destination URL, event, duration, pages-per-visit, or app install), because UET records actions but goals decide which ones count as conversions. Mark the goal's event action so custom events can target it.
4. Stand up the server path only when you need it: format events and POST them to the CAPI endpoint with the Bearer token. Send one `pageLoad` event per page or SPA navigation and zero or more `custom` events, linking each custom event to its page with `pageLoadId`.
5. Attach identity to every server event: `msclkid` for click attribution (never omit it on conversions), a stable `anonymousId` (the vid), hashed `em` and `ph` for enhanced conversions, plus `clientUserAgent` and `clientIpAddress`. See the ID-sync reference for why vid alone does not resolve off-site identity.
6. Set consent on every event. Pass `adStorageConsent` as "G" (granted) or "D" (denied). For EEA, UK, and Switzerland traffic this is mandatory, and a "D" event is excluded from all advertising use, including attribution and retargeting. Read the consent reference before shipping to those regions.
7. Deduplicate the browser and server paths when both fire for the same action: put a matching `eventId` on the UET JS push and on the CAPI event, using the same UET tag ID for both. Without a shared `eventId` the same conversion counts twice.
8. Fire the client-side ID sync pixel (`c.bing.com/c.gif`) from the browser, not the server, because only a client-side beacon lets Microsoft read its third-party cookie IDs and map them to your vid. This is required for remarketing and audience building, recommended for measurement.
9. Verify before trusting the numbers. Check the UET Tags view that events are received, confirm conversions appear, and read back a sample CAPI payload for a valid SHA-256 `em`/`ph`, an `eventTime` inside the 7-day window, and the correct `adStorageConsent`. Gate any change to live goals or spend behind a human review.

## Decision rules and thresholds

### UET tag vs CAPI vs both

- Run the UET tag alone when JavaScript is fine and you have no material browser-side loss. It is the lowest-effort path and unlocks UET Insights, Clarity, and the future Privacy Sandbox path.
- Add CAPI alongside the tag when ad blockers, ITP, or tracking-prevention are eroding browser events. CAPI is a recovery and durability layer, not a replacement, so keep the tag running and dedup the overlap.
- Use CAPI without the tag only when you cannot run Microsoft JS. The integration effort is significantly higher, and you must add a client-side ID sync pixel or you forfeit remarketing and off-site identity.

### Required vs recommended CAPI fields

- Always required on every event: `eventType` ("pageLoad" or "custom") and `eventTime` (UNIX seconds, within 7 days).
- Required for `pageLoad`: `eventSourceUrl`.
- Strongly recommended on all events: `msclkid` (mandatory in practice for conversion attribution), `anonymousId` (must equal the vid from ID sync), `clientUserAgent`, `clientIpAddress`, and hashed `em` and `ph` when available.
- Recommended for singular events like a purchase: `transactionId` (also the key that enables restate and retract corrections).
- Field-by-field types, examples, and the vertical-specific retail and hotel blocks are in `references/uet-roles-and-capi-endpoint.md`.

### Hashing rules (enhanced conversions)

- `em` and `ph` must be valid lowercase-hex SHA-256 strings, or the API rejects the event with a validation error.
- Email: trim whitespace, remove all dots from the user portion, strip any `+alias`, lowercase the whole address, then SHA-256.
- Phone: normalize to E.164 with country code (for example `+14255551234`), then SHA-256.
- Never send raw user IDs. Use a UUID or a hash for `anonymousId` and `externalId`.

### Deduplication

- Dedup applies when the same conversion can arrive from both the UET JS and CAPI under the same UET tag ID.
- Put the same `eventId` on both sides: on the UET JS push (`event_id`) and on the CAPI event (`eventId`). Microsoft collapses the pair. No shared `eventId` means double counting.
- If browser and server use different tag IDs on purpose, they are separate streams and dedup does not apply.

### Consent (EEA, UK, Switzerland)

- Consent mode is mandatory for site visits from the EEA, UK, and Switzerland as of May 5 2025. Pass `ad_storage` on the tag and `adStorageConsent` on CAPI for every such event.
- Values: "G" granted, "D" denied. Events default to granted when the parameter is absent, so you must send "D" explicitly for denied users or you overcount and risk a compliance gap.
- A denied event is not used for any advertising purpose, including conversion attribution and retargeting. Do not expect denied traffic to appear in conversions or feed remarketing.
- TCF is an accepted alternative transport: pass consent via a TCF 2.0 string or your CMP. See `consent-signal-verification-and-decode` for decoding and proving suppression.

### ID sync and remarketing

- Fire the ID sync pixel client-side on as many pages as practical, at minimum once per session (first page view). Throttle if needed but never move it server-side.
- Required parameters: `Red3` as `BACID_<CID>` (the customer ID, not the tag ID) and `vid` (a v1 UUID guest ID). `uid` is optional and anonymized.
- The CAPI `anonymousId` must equal the pixel's `vid`, or Microsoft cannot stitch the server event to the off-site identity for view-through attribution and audiences.

## Reference material

- `references/uet-roles-and-capi-endpoint.md`: the browser tag vs server CAPI roles, the full CAPI endpoint contract (auth, batching, 7-day window, 200/400/401), the complete field map (data schema, userData, customData, items, retail, hotel), restate and retract, and worked purchase and cart payloads. Read this when building or debugging a CAPI integration or wiring specific fields.
- `references/consent-and-advanced-consent-mode.md`: the EEA/UK/Switzerland mandate and May 5 2025 deadline, the `ad_storage` signal, basic vs advanced consent mode, the browser `window.uetq` consent default/update pattern, the CAPI `adStorageConsent` G/D mapping, TCF as an alternative, and what denied events lose. Read this before shipping to regulated regions.
- `references/idsync-and-msclkid-for-remarketing.md`: the ID sync pixel (`c.bing.com/c.gif`), `Red3`/`vid`/`uid` parameters, the vid-to-anonymousId contract, `msclkid` capture and 90-day storage, and the dos and don'ts that decide whether remarketing and attribution work. Read this when remarketing will not build or conversions will not attribute to clicks.

## Templates and examples

CAPI custom purchase event, consent granted, enhanced conversions on:

```json
{
  "data": [
    {
      "eventType": "custom",
      "eventId": "order-90a7f2-2026-0212",
      "eventName": "purchase",
      "eventTime": 1770000000,
      "adStorageConsent": "G",
      "userData": {
        "clientUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
        "anonymousId": "b171a9b06ce011ecafcd1b209be8601b",
        "msclkid": "dd4afcccb1c9a4cad9544dd7e5006",
        "em": "ec81f3ac7b2b19675bab9d54cf416f9f18cff87c97da5cca82c0f0891bc40602",
        "ph": "c59475d96e9f01d7d18d06cfad84dd02333207f02c0c2c5663ef2782cda0390e",
        "clientIpAddress": "203.0.113.42"
      },
      "customData": {
        "eventCategory": "ecommerce",
        "transactionId": "order-90a7f2",
        "value": 129.50,
        "currency": "USD",
        "pageType": "purchase",
        "ecommTotalValue": 129.50,
        "items": [
          { "id": "sku-4412", "quantity": 1, "price": 129.50, "name": "Standing Desk Mat" }
        ]
      }
    }
  ],
  "continueOnValidationError": false,
  "dataProvider": "checkout_service"
}
```

Matching UET JS push so the browser and server events dedup on `event_id`:

```html
<script>
  window.uetq = window.uetq || [];
  window.uetq.push('event', 'purchase', {
    event_category: 'ecommerce',
    event_label: 'order-90a7f2',
    revenue_value: 129.50,
    currency: 'USD',
    event_id: 'order-90a7f2-2026-0212'
  });
</script>
```

Client-side ID sync pixel (rendered into the HTML response, fired first page view of the session):

```html
<img src="https://c.bing.com/c.gif?vid=b171a9b06ce011ecafcd1b209be8601b&Red3=BACID_123456" width="1" height="1" alt="">
```

Denied-consent event from an EEA visitor (still sent, but excluded from advertising use):

```json
{
  "eventType": "custom",
  "eventName": "purchase",
  "eventTime": 1770000000,
  "adStorageConsent": "D",
  "userData": { "anonymousId": "9f2c1e40-0b6a-11ef-9d21-0242ac120002" }
}
```

## Common pitfalls

- Omitting `msclkid` on conversion events. vid alone does not attribute a click, so conversions silently fail to tie back to the ad. Capture `msclkid` from the auto-tagged landing page, store it per user (first-party cookie or local storage, 90-day retention), and overwrite on each new click.
- vid and anonymousId do not match. If the ID sync pixel's `vid` differs from the CAPI `anonymousId`, Microsoft cannot stitch identity, so view-through attribution and remarketing break even though events arrive.
- Firing ID sync from the server. A server-side beacon cannot read Microsoft's third-party cookie IDs, so remarketing never builds. It must fire client-side.
- Sending unhashed or wrongly normalized `em`/`ph`. The API rejects any `em`/`ph` that is not a valid lowercase-hex SHA-256, and skipping the dot and `+alias` normalization on email produces a hash that never matches. Normalize first, then hash.
- Stale `eventTime`. Events older than 7 days are rejected, and a millisecond timestamp (not seconds) fails validation. Send UNIX epoch seconds within the window.
- Double counting. Running the UET tag and CAPI on the same tag ID without a shared `eventId` counts each conversion twice. Put a matching `eventId` / `event_id` on both paths.
- Treating absent consent as denied. The CAPI defaults to granted when `adStorageConsent` is missing, so a denied user with no signal gets processed. For EEA, UK, and Switzerland you must send "D" explicitly.
- Batch failure surprises. By default one invalid event fails the entire batch. Set `continueOnValidationError: true` only when you intend to skip bad events and keep the rest.

## Sources

- [Conversions API (CAPI) Guide, Microsoft Advertising](https://learn.microsoft.com/en-us/advertising/guides/uet-conversion-api-integration?view=bingads-13) (as of July 2026)
- [Universal Event Tracking, Microsoft Advertising](https://learn.microsoft.com/en-us/advertising/guides/universal-event-tracking?view=bingads-13) (as of July 2026)
- [Providing user consent signals on your Microsoft campaigns by May 5, 2025](https://about.ads.microsoft.com/en/blog/post/march-2025/providing-user-consent-signals-on-your-microsoft-campaigns-by-may-5-2025) (as of July 2026)
