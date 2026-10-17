---
name: gtm-server-conversion-enhancement
description: Route Google Ads and Floodlight conversions through a server-side GTM container with first-party data, Enhanced Conversions (hashed user_data), and consent-aware forwarding. Use when the user asks how to move Google Ads or Floodlight conversions server-side, set up server-side Enhanced Conversions, send hashed user-provided data, add the Conversion Linker plus Google Ads Conversion Tracking tags on a tagging server, forward conversions server to server, recover conversions lost to cookie and browser signal loss in 2026, choose between the Google tag gateway and a full sGTM server, or why server-side conversions are under-reporting or double-counting.
---

# GTM server-side conversion enhancement

Send Google Ads and Floodlight conversions from a server-side GTM container (a tagging server you control) instead of from the browser, attach hashed first-party user data for Enhanced Conversions, and gate every forward on consent. The payoff is recovery: server-side firing plus Enhanced Conversions restores conversions that browser cookie deletion, ITP, and consent denial would otherwise lose, and consent gating keeps the forward legal. This skill is about the conversion tags and their payload, not the box they run on.

This skill assumes you already have a tagging server. For provisioning the server, its clients, and the browser-to-server transport, see the `gtm-server-side-tagging` skill. For the four consent signals and their default/update ordering, see `gtm-consent-mode-v2`. For where you know CPA, ROAS, and match rate, see `programmatic-foundations`.

## When to use this skill

- "Move my Google Ads / Floodlight conversions server-side."
- "Set up server-side Enhanced Conversions" or "send hashed user_data to Google Ads."
- "Add the Conversion Linker and Google Ads Conversion Tracking tags on the server."
- "Forward Floodlight conversions server to server" or "server-side CM360 conversions."
- "Recover conversions lost to Safari / Firefox / iOS / cookie deletion in 2026."
- "My server-side conversions are under-counting / double-counting versus GA4 or the browser tag."
- "Google tag gateway or a full server container, which do I need?"
- "What data can I legally forward from the server, and how do I gate it on consent?"
- "Enhanced Conversions match rate is low, how do I raise it?"

Boundaries with sibling skills:
- Standing up the Cloud Run server, its clients, transport, and first-party domain: `gtm-server-side-tagging`. This skill assumes the server exists.
- The four consent signals, default/update commands, and region defaults: `gtm-consent-mode-v2`. This skill reads those signals and decides what to forward.
- Browser container, dataLayer contract, and web tags/triggers/variables: `gtm-web-container-and-datalayer` and `gtm-tags-triggers-variables`.
- Floodlight activity configuration in CM360 and the CM360 Conversions API: `cm360-floodlight-and-conversions`.
- The Google Ads conversion action itself, attribution model, and Enhanced Conversions on the Google Ads side: `google-ads-conversion-tracking-and-attribution`.
- Marking key events and the GA4 event model: `ga4-events-and-key-events`. GA4 uses key events, not "conversions"; do not carry the old term into GA4 config.
- Reconciling counts across GA4, Google Ads, CM360, and the DSP: `cross-platform-conversion-reconciliation`.

## Quick reference

| Decision | Choose | Why |
| --- | --- | --- |
| Just want durable first-party Google-tag delivery, no event server | Google tag gateway | Serves Google tags from your domain, no container to process events |
| Full control of the conversion payload, hashing, and forwarding | Full sGTM server container | Only the server can attach hashed user_data and decide what leaves |
| Google Ads conversions server-side | Conversion Linker + Google Ads Conversion Tracking tags on the server | Linker reads the click ID cookie; tracking tag fires the conversion |
| Floodlight conversions server-side | Floodlight tags on the server behind the Conversion Linker | Same linker, CM360 counter/sales activities |
| Raise Google Ads match rate | Enhanced Conversions with hashed `user_data` | Matches server-side conversions to signed-in Google users |
| Ad consent denied | Do not forward user_data; set `ads_data_redaction` true | Forwarding under denial breaks consent and the June 2026 gating |
| Reconcile a discrepancy | Compare event_id, dedup, and consent state, not raw totals | Under/over-count is almost always dedup or consent, not the tag |

Mental model: the browser (or Measurement Protocol) sends one event to your first-party domain. A client on the server parses it into an event with `user_data`. The Conversion Linker resolves the click identifier. The Google Ads and Floodlight tags fire server to server, forwarding the hashed data only when consent allows. The server is where you control the payload; the browser is just the courier.

## Core process

1. Confirm the server and transport are live first, because this skill only adds tags on top. The tagging server must be on a first-party domain with a client claiming the incoming requests, verified in Preview. If it is not, start in `gtm-server-side-tagging`.
2. Add the Conversion Linker tag on the server, triggered on all events, because it reads and writes the Google click identifier (gclid/wbraid/gbraid) cookie that every downstream conversion tag needs to attribute. Without it, server-side Google Ads and Floodlight conversions cannot join back to the click.
3. Add the Google Ads Conversion Tracking tag on the server. Set the conversion ID and label from the Google Ads conversion action, and trigger it on the specific conversion event (purchase, lead) rather than all pages, so it fires once per real conversion.
4. Provide user-provided data as a `user_data` object for Enhanced Conversions, because that is what raises match rate and recovers unmatched conversions. Collect email and phone at minimum, plus name and address where available. Set the variable's event parameter name to exactly `user_data`. Hash on the server with SHA256, or send raw and let Google hash; never forward plaintext to a third party.
5. Add Floodlight tags for CM360 conversions the same way, behind the same Conversion Linker, mapping each Floodlight counter or sales activity. Keep the u-variables and sales/quantity fields consistent with the CM360 activity so counts reconcile.
6. Gate every forward on consent. Read the ad-consent signals (`ad_user_data`, `ad_personalization`) the browser set. When ad consent is denied, do not send `user_data` and set `ads_data_redaction` to true so click identifiers are redacted. This is not optional after the June 2026 ads-data gating.
7. Deduplicate against the browser. If a browser tag and the server tag can both fire for the same conversion, carry a shared transaction or event identifier so the platform counts one, not two. Decide up front which side is authoritative.
8. Preview, then human-gate the publish. Open Preview on the server container, confirm the Conversion Linker resolves the click ID, the conversion tag fires once with a populated `user_data`, consent is respected, and outgoing requests return 2xx. Server-side conversion tags send real conversions and hashed personal data to vendors, so get sign-off before publishing the version.

## Decision rules and thresholds

### Gateway vs full server container

- Use the Google tag gateway when the only goal is durable first-party delivery of the Google tag itself. It serves Google tags from your own domain (via your CDN, load balancer, or web server) with automatic configuration and no event-processing container to run. It does not let you rewrite the conversion payload or attach server-controlled hashed data.
- Use a full sGTM server container when you need to control what leaves: attach hashed `user_data`, strip fields, enforce consent server-side, or forward to non-Google endpoints. Only the server container gives you the payload control that Enhanced Conversions and consent-aware forwarding require.
- They are complementary, not either/or. Google recommends mapping a custom domain and then loading first-party scripts via the gateway for the most durable setup, with the server container processing and forwarding events behind it. See `references/gateway-vs-sgtm.md`.

### Enhanced Conversions and user_data

- Send the strongest identifiers you have, in priority order: email, then phone, then name plus mailing address. Email is the single highest-yield field. More fields raise match rate but email alone already recovers a large share.
- The event parameter name must be exactly `user_data`. A misnamed variable silently drops Enhanced Conversions with no error.
- Hashing: normalize (trim, lowercase email, E.164 phone) then SHA256. If you pre-hash, prefix the keys as `sha256_` so Google knows the value is already hashed. If you send raw, Google hashes it; either way plaintext must never reach a non-Google vendor.
- Enhanced Conversions only helps where a match exists (a signed-in Google user). It does not conjure conversions from anonymous denied traffic. That gap is closed by modeling (see `gtm-consent-mode-v2`), not by user_data.
- Match rate below roughly 70 percent usually means missing or malformed fields, not a platform problem. Check normalization and field coverage first. See `references/enhanced-conversions-user-data.md`.

### Consent-aware forwarding (the non-negotiable gate)

- The four consent signals are `ad_storage`, `analytics_storage`, `ad_user_data`, and `ad_personalization`. Enhanced Conversions user_data flow to Google Ads depends on `ad_user_data` being granted; personalized/remarketing use depends on `ad_personalization`.
- When ad consent is denied: do not attach `user_data`, and set `ads_data_redaction` to true so ad click identifiers in Google Ads and Floodlight requests are redacted. A conversion may still be pinged cookielessly, but no personal data forwards.
- The June 2026 gating tightened this: ads-related data flow is gated on the ad-consent pair being granted, so `ad_storage` alone no longer suffices to forward ads data. If forwarding stopped after mid-2026, confirm `ad_user_data` and `ad_personalization`, not just the storage signals.
- Moving tags to the server does not remove the consent requirement. The browser still sets the signals; the server must honor them. See `references/enhanced-conversions-user-data.md` for the forward matrix.

### Deduplication

- Any conversion that can fire both in the browser and on the server needs a shared identifier so the platform counts it once. Use the order or transaction ID as the dedup key, carried on both the browser tag and the server tag.
- Decide which side is authoritative. Common pattern: fire server-side as the source of truth and either suppress the browser tag for that conversion or rely on the shared ID for dedup. Never leave both firing unkeyed, or you double-count.
- Dedup windows and keys differ by platform. Google Ads dedups on the conversion action plus order ID; Floodlight dedups per activity. Reconcile with `cross-platform-conversion-reconciliation` when totals disagree.

### 2026 server-to-server recovery

- The real signal loss in 2026 is not Privacy Sandbox. Chrome kept third-party cookies, and on 17 October 2025 Google announced it is retiring the Privacy Sandbox advertising APIs (Topics, Protected Audience, Attribution Reporting) for low adoption. The durable loss is Safari ITP, Firefox ETP, iOS, and consent denial. Server-side firing plus Enhanced Conversions plus consent modeling is the recovery stack, not any Sandbox API.
- Server-side firing recovers conversions that browser-side tags lose to ad blockers, ITP cookie capping, and third-party request failures, because the hit originates first-party from your server.
- Enhanced Conversions recovers matchable conversions that lost their cookie, by rejoining on hashed user data.
- Consent modeling (advanced consent mode) recovers a modeled share of denied traffic. It needs the click-volume threshold and lives in `gtm-consent-mode-v2`.
- Do not oversell the recovery. It restores a share of lost conversions, not all of them, and only where consent and a match exist. See `references/2026-server-to-server-recovery.md`.

### Safe-by-default

- Read and preview before you publish. Publishing a server container version changes what fires on live traffic and what personal data is forwarded to Google and CM360. Treat every publish as a live-config and data-forwarding change requiring human sign-off.
- Never forward plaintext personal data to any non-Google endpoint, and never forward `user_data` under denied ad consent. Confirm hashing and the consent gate in Preview before publishing.

## Reference material

- `references/server-ads-stack.md`: the server-side conversion tag stack in order (Conversion Linker, Google Ads Conversion Tracking, Floodlight), the exact fields each tag needs, the event-data variables that feed them, and the client/event-data plumbing that carries the payload. Read this when building or debugging the actual tags on the server.
- `references/enhanced-conversions-user-data.md`: the full `user_data` field map, normalization and SHA256 hashing rules, the `sha256_` pre-hash prefix, the match-rate diagnostic ladder, and the consent forward matrix (which signal gates which forward). Read this when wiring Enhanced Conversions or troubleshooting a low match rate.
- `references/2026-server-to-server-recovery.md`: the 2026 signal-loss ground truth (Sandbox retired, Chrome cookies stay, real loss is Safari/Firefox/iOS/consent), what each recovery lever actually recovers, and a realistic recovery-stack decision table. Read this when scoping or setting expectations for a recovery project.
- `references/gateway-vs-sgtm.md`: the Google tag gateway versus a full server container, what each does and does not let you control, the decision table, and how they combine for the most durable setup. Read this when choosing the architecture or explaining why one is not a substitute for the other.

## Templates and examples

Ecommerce purchase, Google Ads Enhanced Conversions server-side. The browser sends the purchase event to `sgtm.shopname.com`; the GA4 client parses it; the server fires the conversion:

```
Conversion Linker tag        -> trigger: All events (reads gclid/wbraid/gbraid cookie)
Google Ads Conversion Tracking -> Conversion ID: AW-123456789, Label: AbC-D_efGh
                                 trigger: event equals "purchase"
                                 user_data: {{ED - user_data}}  (parameter name exactly user_data)
                                 dedup key: {{ED - transaction_id}}
Consent gate                   -> require ad_user_data = granted before sending user_data
                                 else set ads_data_redaction = true, drop user_data
```

The `user_data` event-data variable, normalized and hashed on the server, sent to Google Ads:

```json
{
  "sha256_email_address": "a1b2c3...   (lowercased, trimmed, then SHA256)",
  "sha256_phone_number": "d4e5f6...    (E.164 +14155551234, then SHA256)",
  "address": {
    "sha256_first_name": "...",
    "sha256_last_name": "...",
    "postal_code": "94103",
    "country": "US"
  }
}
```

Floodlight sales activity server-side, same server, behind the same Conversion Linker:

```
Floodlight (Sales) tag -> Advertiser ID + Activity Group + Activity (from CM360)
                          u-variables mapped to the CM360 activity's custom fields
                          revenue: {{ED - value}}, quantity: {{ED - quantity}}
                          order ID: {{ED - transaction_id}}  (Floodlight dedup key)
                          trigger: event equals "purchase"
```

Analytics-only consent (visitor accepted analytics, declined ads): the GA4 event still flows, but the Google Ads and Floodlight tags send no `user_data`, and `ads_data_redaction` is true so the gclid is redacted. The conversion may still be counted cookielessly, but nothing personal forwards.

## Common pitfalls

- No Conversion Linker on the server. The Google Ads and Floodlight tags fire but cannot join to the click, so conversions come in unattributed. Add the Conversion Linker triggered on all events, before the conversion tags.
- `user_data` misnamed. If the event parameter is not exactly `user_data`, Enhanced Conversions silently does nothing and match rate stays low with no error. Name it exactly, verify in Preview that the object is populated.
- Forwarding under denied consent. Sending `user_data` when `ad_user_data` is denied breaks consent and, after June 2026, is gated anyway. Gate the forward, and set `ads_data_redaction` true on denial.
- Double-counting browser plus server. Leaving both the browser and server conversion tags firing without a shared dedup key double-counts every conversion. Carry the transaction/order ID on both, pick one authoritative side.
- Plaintext leaving the server. Forwarding unhashed email or phone to any non-Google endpoint is a data leak. Normalize and SHA256 on the server (or send raw only to Google, which hashes it); prefix pre-hashed keys `sha256_`.
- Expecting the gateway to do payload work. The Google tag gateway serves scripts first-party but does not attach hashed data or enforce server-side consent. If you need Enhanced Conversions or payload control, you need the full server container.
- Publishing without Preview. Server-side conversion tags forward real conversions and hashed personal data. An unverified publish can double-count, mis-map a Floodlight activity, or leak data. Preview the linker, the single fire, the consent gate, and outgoing 2xx, then get sign-off.
- Blaming the tag for a discrepancy. Under- or over-count versus GA4 or the browser is almost always dedup or consent state, not the tag. Compare event_id, dedup key, and consent before touching the configuration. Hand off to `cross-platform-conversion-reconciliation`.

## Sources

- [Set up Google Ads conversion tracking server-side](https://developers.google.com/tag-platform/tag-manager/server-side/ads-setup) (as of July 2026)
- [Server-side tagging intro](https://developers.google.com/tag-platform/tag-manager/server-side/intro) (as of July 2026)
- [Send data to a server container](https://developers.google.com/tag-platform/tag-manager/server-side/send-data) (as of July 2026)
- [Consent for tags and server-side tagging](https://developers.google.com/tag-platform/security/guides/consent) (as of July 2026)
- [Google tag gateway for advertisers](https://developers.google.com/tag-platform/tag-manager/gateway) (as of July 2026)
- [dataLayer reference](https://developers.google.com/tag-platform/tag-manager/datalayer) (as of July 2026)
- [Debug a server container](https://developers.google.com/tag-platform/tag-manager/server-side/debug) (as of July 2026)
- [Server-side tagging setup (Tag Manager Help)](https://support.google.com/tagmanager/answer/4620708?hl=en) (as of July 2026)
- [Update on plans for Privacy Sandbox technologies](https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies) (as of July 2026)
