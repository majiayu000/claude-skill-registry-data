---
name: cm360-floodlight-and-conversions
description: Configure Campaign Manager 360 Floodlight activities and upload offline conversions. Use when the user asks about Floodlight activity types, Counter vs Sales, counting methods (standard, unique, per session, transactions, items sold), the ord parameter, custom Floodlight variables, conversion windows and lookback, view-through vs click-through attribution, the Conversions API (batchinsert / batchupdate), gclid/dclid/matchId/encryptedUserId identifiers, EncryptionInfo, adUserDataConsent, enhanced conversions, or offline conversion imports.
---

# CM360 Floodlight and conversions

Set up Floodlight so it counts the right thing once, and get offline and online conversions into Campaign Manager 360 with the right identifier, attribution window, and consent flags. Floodlight is the measurement spine of the Google Marketing Platform: the same activity feeds CM360 reporting, DV360, and SA360, so a wrong counting method or window here is wrong everywhere downstream.

This skill assumes you know CPA, ROAS, click-through vs view-through, and lookback windows. For that KPI math see the `programmatic-foundations` skill. For building the tags that fire Floodlight on the page (placements, ad tags, click macros), see `cm360-trafficking-and-ad-tags`. For deduplicating a Floodlight number against GA4 and each DSP, see `cross-platform-conversion-reconciliation`.

## When to use this skill

- "Should this be a Counter or a Sales activity?" / "Which counting method?"
- "Set standard vs unique vs per-session counting." / "transactions vs items sold."
- "How does the `ord` value dedupe conversions?" / "What is `num` for?"
- "Add a custom Floodlight variable (u1, u2 ...)." / "How many U variables can I have?"
- "Set the conversion window / lookback." / "click-through vs view-through window."
- "Upload offline conversions via the Conversions API." / "batchinsert / batchupdate."
- "Which identifier: gclid, dclid, matchId, encryptedUserId, mobile device id?"
- "Restate a conversion value / adjust a conversion after the fact."
- "Set `adUserDataConsent` / consent flags on the upload." / "enhanced conversions for CM360."

Boundaries with sibling skills:
- Placements, ad tags, click commands, and Floodlight tag macros on the page: `cm360-trafficking-and-ad-tags`.
- Reconciling the Floodlight count against GA4, DV360, and platforms: `cross-platform-conversion-reconciliation`.
- Linking Floodlight into GA4 and sharing it to DV360/SA360: `gmp-integration-floodlight-ga4-linking`.
- GA4 key events and their Google Ads counterparts (a different measurement system): `ga4-events-and-key-events`.
- Consent Mode signals on the web page that gate tag firing: `gtm-consent-mode-v2`.

## Quick reference

| Decision | Choose | Why |
| --- | --- | --- |
| Track a page visit, lead, signup, app open (no revenue) | Counter activity | Counter measures how often an action happens |
| Track a purchase with revenue and/or items | Sales activity | Sales captures transaction count, revenue, and item quantity |
| Count every fire (page views, repeat leads) | Counter: Standard | No dedup, every event counts |
| Count one per user per day (unique leads) | Counter: Unique | Dedupes to first per user per 24-hour day |
| Count one per session (engagement) | Counter: Per session | One per user per session window you set |
| One row per order, plus revenue | Sales: Transactions | Counts transactions and total revenue |
| Revenue plus how many items in the basket | Sales: Items sold | Counts items and total revenue |
| Import CRM / call-center / in-store conversions | Conversions API batchinsert | Offline events with a stored identifier |
| Restate a value or adjust an existing conversion | Conversions API batchupdate | Updates an existing conversion in place |

Identifier decision (one per conversion, most specific wins):

| You have | Use | Notes |
| --- | --- | --- |
| Google Ads click id | `gclid` | Preferred when the click came through Google Ads / DV360 |
| CM360 click id | `dclid` | From a CM360-served click (`%eaid`/click macro path) |
| iOS / Android app click id | `gbraid` / `wbraid` | App-to-web and app conversions, privacy-safe click ids |
| First-party match key you set | `matchId` | You control it; must match the value sent at click time |
| Hashed user id from `%m` macro or Data Transfer | `encryptedUserId` (+ `EncryptionInfo`) | Requires the encryption entity that hashed it |
| Advertising device id (IDFA/AAID) | `mobileDeviceId` | Raw device id, subject to platform limits |

## Core process

1. Pick the activity type first. Counter for events without a monetary value (leads, signups, page views, app opens), Sales for purchases where you report revenue or item count. This is a one-way-ish choice: reporting metrics differ, so getting it right up front avoids re-tagging.
2. Pick the counting method to match the KPI, not the traffic. Standard counts every fire; Unique dedupes to the first per user per 24-hour day; Per session counts once per user per session. For Sales, Transactions counts orders and revenue, Items sold adds basket quantity. See `references/counter-vs-sales-and-counting.md`.
3. Put the activity in a Floodlight group and confirm the group tag type (global site tag or image/iframe legacy). The group carries shared settings and the configuration id every downstream product references. Tag mechanics live in `cm360-trafficking-and-ad-tags`.
4. Declare any custom Floodlight variables you need (u1 ... u100) in the Floodlight configuration before you reference them in tags or uploads. Up to 100 per configuration, typed String or Number. Undeclared U variables are dropped.
5. Set the conversion window (lookback). Choose a click-through window and a view-through window that fit the buying cycle and the media mix, knowing view-through is capped shorter than click-through. See `references/conversion-windows-and-attribution.md`.
6. For online conversions, verify the tag fires with the right `ord` value for the counting method (unique random `ord` for Standard/Transactions/Items sold, `ord=1` plus a session id for Unique/Per session). The `ord` value is what dedup is built on.
7. For offline conversions, choose the identifier (table above), build the Conversion objects, and call `conversions.batchinsert`. Include `adUserDataConsent` and the child/underage flags. Read and dry-run before you send. See `references/conversions-api-identifiers.md`.
8. To restate values or fix mistakes, use `conversions.batchupdate` keyed on the same activity, identifier, `ordinal`, and `timestampMicros`. You update value/quantity in place, you do not insert a second row.
9. Reconcile the resulting Floodlight count against the source system and against GA4/DSP before anyone trusts it for billing or optimization. Hand off to `cross-platform-conversion-reconciliation`.

Safe-by-default: read the current Floodlight config and pull a report first. Any change to a counting method, window, or a live conversion upload changes billed and optimization numbers, so treat those as human-gated. Always dry-run a batch upload against a test activity before the production activity.

## Decision rules and thresholds

### Counter vs Sales

- No revenue and no item count in the report you need -> Counter. Adding revenue later means a new Sales activity, so if revenue is even plausibly needed, use Sales now.
- You report revenue or ROAS, or you need basket item counts -> Sales. Transactions for order-level revenue, Items sold when quantity per order matters (retail, travel seats, tickets).

### Counting method

- Standard: every fire counts. Use for raw page views or when you truly want repeat counts. Risk: double counts refreshes and back-button hits.
- Unique: one per user per 24-hour day. Use for lead-gen and signups where a person should count once a day.
- Per session: one per user per session (you set the session length). Use for engagement events where per-session is the honest unit.
- Transactions (Sales): counts each order plus total revenue. The default for ecommerce purchase.
- Items sold (Sales): counts items plus revenue. Use when average basket size is the metric.

The `ord` (ordinal) parameter is how the method dedupes: Standard and both Sales methods use a unique per-event random `ord` (a cache buster) so every event is distinct; Unique and Per session send `ord=1` plus a session identifier so repeats collapse. Wrong `ord` wiring silently breaks dedup and either inflates or suppresses the count. Details and macro values in `references/counter-vs-sales-and-counting.md`.

### Conversion windows (lookback)

- Click-through (post-click) windows run longer than view-through (post-impression) windows. Set the click window to cover the realistic consideration cycle; set view-through shorter and more conservatively, since a view is weaker evidence than a click.
- Longer windows credit more conversions to earlier touches and inflate view-through volume. Shorter windows undercount long cycles. Pick per the sales cycle, then keep it stable so trend lines stay comparable.
- Changing a window retroactively changes reported history for the affected model, which breaks period-over-period comparisons. Change deliberately and annotate the date.

Exact maximums and the interaction with attribution models are in `references/conversion-windows-and-attribution.md`.

### Offline conversion upload

- Timestamp must fall inside the activity's conversion window relative to the matched click/impression, or the conversion will not attribute. Do not backfill events older than the window and expect credit.
- One identifier per conversion. Send the most specific id you have (`gclid`/`dclid`/`gbraid`/`wbraid` before `matchId`, `matchId` before `encryptedUserId`, and `encryptedUserId` only with its `EncryptionInfo`).
- `EncryptionInfo` (`encryptionEntityId`, `encryptionEntityType`, `encryptionSource`) is required whenever `encryptedUserId` or `encryptedUserIdCandidates[]` is used, and only then. It names the entity that produced the hash so CM360 can decrypt-match.
- Set `adUserDataConsent` to reflect the user's ad-user-data consent. Absent or DENIED consent restricts how the conversion can be used, consistent with the wider 2026 move to gate ads-data flow on consent (see `gtm-consent-mode-v2`). Also set `childDirectedTreatment` / `treatmentForUnderage` where the audience requires it.
- Batch sizing: send conversions in batches (not one call per event) and handle per-row status in the response. Rows can succeed and fail independently, so never assume a 200 means every row landed.

### Update vs insert

- `batchupdate` updates an existing conversion (for example restating `value` after a refund or a corrected order total). It matches on the activity, identifier, `ordinal`, and `timestampMicros`, so those must equal the original insert.
- Do not use `batchinsert` to "fix" a value; a second insert with a fresh `ord` creates a second conversion and double counts.

## Reference material

- `references/counter-vs-sales-and-counting.md`: Counter vs Sales side by side, all five counting methods with what each counts and dedupes, the full `ord`/`num`/`cost`/`qty`/`u` tag parameter map, custom Floodlight variable rules (up to 100, String/Number, forbidden characters), and worked counting examples. Read this when choosing or auditing a counting method.
- `references/conversion-windows-and-attribution.md`: click-through vs view-through lookback windows, maximums and defaults, how windows interact with attribution models across GMP, and a decision table by sales-cycle length. Read this when setting or debating a conversion window.
- `references/conversions-api-identifiers.md`: the full Conversion object field map for CM360 API v5 (`batchinsert` / `batchupdate`), required vs optional fields, the identifier decision tree, `EncryptionInfo` fields, consent and child-treatment flags, the endpoint and OAuth scope, and per-row error handling. Read this before building an offline upload.
- `references/aug-2026-sdf-count-value-split.md`: what changed recently in CM360 measurement plumbing (API v5 status, GPP/TCF consent macros in tag generation, the count-vs-value reporting split practitioners should plan for), and how to keep a pipeline forward-compatible. Read this when a pipeline broke after an update or you are hardening it against the next one.

## Templates and examples

Lead-gen Counter, one lead per person per day:
- Activity type Counter, method Unique. Custom variable `u1` = form name (String), `u2` = lead score (Number). Tag sends `ord=1` and a session id so a refresh does not double count. Click-through window sized to the sales cycle, view-through short.

Ecommerce purchase Sales, order-level revenue:
- Activity type Sales, method Transactions. Revenue passed as `cost`/value, `ord` is a unique random cache buster per order so each order is distinct. `u1` = coupon code, `u2` = new-vs-returning. Reconcile the daily order count and revenue against the order database before trusting ROAS.

Offline CRM upload, closed-won deals from Salesforce, keyed on gclid:
- One Conversion object per deal: `floodlightConfigurationId`, `floodlightActivityId`, `gclid`, `ordinal` (unique per event), `timestampMicros` (deal close time, inside the window), `value` = deal amount, `quantity` = 1, `adUserDataConsent` = GRANTED for consented records. Call `conversions.batchinsert` in batches of a few hundred, log each row's status, retry only the failed rows.

Restate a deal value after an upsell:
- Same activity, `gclid`, `ordinal`, and `timestampMicros` as the original insert, new `value`. Call `conversions.batchupdate`. Confirm the report reflects the new value and that the row count did not increase.

Encrypted user id upload from Data Transfer files:
- `encryptedUserId` from the `%m` match table plus `EncryptionInfo` with the `encryptionEntityId`/`encryptionEntityType`/`encryptionSource` that produced the hash. Without matching `EncryptionInfo` the row fails.

## Common pitfalls

- Counter chosen when revenue is needed later. Counter has no revenue, so you re-tag and lose history. If revenue is plausibly in scope, start with Sales.
- Wrong `ord` for the method. Unique/Per session need `ord=1` plus a session id; Standard/Sales need a unique random `ord`. Mismatched `ord` silently double counts or suppresses. Verify in the fired tag.
- Custom variable referenced but not declared. U variables not defined in the Floodlight configuration are dropped, so the report column is empty and no error is thrown. Declare u1 ... u100 first.
- Backfilling conversions older than the window. Events outside the lookback do not attribute; the upload "succeeds" per row but the conversion never shows against media. Check the timestamp against the window.
- Multiple identifiers or the wrong one. Send exactly one identifier, the most specific you have. A `matchId` that does not equal the value sent at click time will not match.
- `encryptedUserId` without `EncryptionInfo`. The row fails. Encryption fields are mandatory for encrypted ids and forbidden context otherwise.
- Insert used to fix a value. A second `batchinsert` double counts. Use `batchupdate` keyed on the original ordinal and timestamp.
- Assuming a 200 means success. Batch rows fail independently. Parse the per-row status and retry only failures; do not resend the whole batch (that double counts the ones that landed).
- Window changed mid-flight without annotation. Retroactively rewrites reported history and breaks trend comparisons. Change deliberately, record the date, tell the reconciliation owner.

## Sources

- [About Floodlight activities and counting](https://support.google.com/campaignmanager/answer/2823400?hl=en) (as of July 2026)
- [Floodlight conversion windows](https://support.google.com/campaignmanager/answer/2823351?hl=en) (as of July 2026)
- [Custom Floodlight variables](https://support.google.com/campaignmanager/answer/2823222?hl=en) (as of July 2026)
- [Set up conversion tracking in Campaign Manager 360](https://support.google.com/campaignmanager/answer/17108857?hl=en) (as of July 2026)
- [Uploading conversions overview](https://developers.google.com/doubleclick-advertisers/guides/conversions_overview) (as of July 2026)
- [conversions.batchinsert, CM360 API v5 reference](https://developers.google.com/doubleclick-advertisers/rest/v5/conversions/batchinsert) (as of July 2026)
- [conversions.batchupdate, CM360 API v5 reference](https://developers.google.com/doubleclick-advertisers/rest/v5/conversions/batchupdate) (as of July 2026)
- [CM360 API deprecation schedule](https://developers.google.com/doubleclick-advertisers/deprecation) (as of July 2026)
- [CM360 API changelog](https://developers.google.com/doubleclick-advertisers/changelog) (as of July 2026)
