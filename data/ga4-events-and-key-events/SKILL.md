---
name: ga4-events-and-key-events
description: Design the GA4 event data model and mark and manage key events plus their Google Ads conversion counterparts using current terminology. Use when the user asks about GA4 events, key events, "conversions vs key events", event taxonomy, reserved event names, recommended events, ecommerce events (purchase, add_to_cart, begin_checkout), create-event or modify-event, event parameters and limits, or importing a GA4 key event as a Google Ads conversion.
---

# GA4 events and key events

Design the GA4 event schema, mark the handful of events that matter as key events, and hand
the right ones to Google Ads as conversions. In GA4 everything is an event. A key event is an
event you flagged as business-critical, and a conversion is the ad-side action Google Ads
optimizes and bills against. Getting the names, parameters, and the key-event flag right at
collection time is what makes every downstream report, audience, and bid strategy work.

This skill assumes you know what a session, an event, and a conversion are, and the KPI math
behind CPA and ROAS. For those, see the `programmatic-foundations` skill. For standing up the
property, data streams, and enhanced measurement, see `ga4-property-and-data-stream-setup`. For
building audiences and exporting them and conversions to Google Ads, DV360, SA360, and Ad
Manager, see `ga4-conversions-and-audiences`.

## When to use this skill

- "What events should I send to GA4?" / "How do I name events?" / "Design my event taxonomy."
- "What is a key event?" / "Key events vs conversions, what changed?" / "How do I mark a key event?"
- "Which events are reserved?" / "Can I name a custom event `page_view`?" / "Why is my custom event rejected?"
- "Set up ecommerce tracking." / "What parameters does `purchase` need?" / "What goes in the `items` array?"
- "Create an event from `page_view` without code." / "Modify an existing event's parameters."
- "How many event parameters can I send?" / "What are the GA4 event limits?"
- "Turn my `generate_lead` key event into a Google Ads conversion."

Boundaries with sibling skills:
- Property, data stream, Google tag or GTM install, enhanced measurement toggles: `ga4-property-and-data-stream-setup`.
- Where the events physically get pushed (dataLayer contract, GTM tags and triggers): `gtm-web-container-and-datalayer` and `gtm-tags-triggers-variables`.
- Building audiences from key events and exporting conversions to the ad platforms, plus the June 2026 consent gating: `ga4-conversions-and-audiences`.
- Consent Mode v2 signals and default-vs-update ordering: `gtm-consent-mode-v2`.
- Querying event-level data unsampled in SQL: `ga4-bigquery-export-and-sql`.
- Reconciling GA4 conversion counts against CM360 and the DSPs: `cross-platform-conversion-reconciliation`.

## Quick reference

Terminology, current as of 2026. GA4 renamed "conversions" to "key events" for the analytics
side; "conversion" now refers only to the ad-side action. The chain is one direction:

`Event -> Key event -> Conversion (Google Ads)`

| You want | Do this | Why |
| --- | --- | --- |
| Measure any interaction | Send an event (auto, enhanced, recommended, or custom) | Everything in GA4 is an event |
| Flag an event as business-critical for reporting | Mark it a key event in Admin > Key events | Key events surface in reports and feed audiences |
| Optimize and bill an ad campaign on that action | Import the key event as a Google Ads conversion | Only Google Ads counts conversions and bids on them |
| Track a purchase, cart, or checkout | Use the reserved ecommerce event names and the `items` array | Reserved names unlock ecommerce reports and item-scoped dimensions |
| Fire an event on a specific page with no code | Create event from an existing event (URL condition) | No developer needed for simple triggers |
| Fix or enrich an event already collected | Modify event (overwrites the original) | Repair naming or add parameters retroactively going forward |

Four event categories, in order of preference when a name exists:

1. Automatically collected (`first_visit`, `session_start`, `page_view`, `user_engagement`).
2. Enhanced measurement (`scroll`, `click`, `file_download`, `form_start`, `form_submit`, `video_start`).
3. Recommended (Google-defined names like `purchase`, `add_to_cart`, `generate_lead`).
4. Custom (your own name, only when nothing above fits).

Always prefer a recommended name over a custom one. Recommended names unlock prebuilt reports,
predictive audiences, and correct semantics that a custom name will never get.

## Core process

1. Inventory the business actions worth measuring, then map each to an event, because a clean
   taxonomy is cheaper to build once than to untangle later. Start from the standard reports
   you owe the client (funnel, ecommerce, lead) and work backward to the events they need.
2. Match each action to a name in priority order (auto, enhanced, recommended, custom), so you
   inherit Google's semantics wherever one exists. Only invent a custom name when no recommended
   event fits. Never reuse a reserved name for a different meaning.
3. Define the parameter contract per event before anyone codes it, because parameters are what
   turn a raw count into a usable dimension or metric. Decide required vs optional, types, and
   allowed values, and register the ones you will report on as custom dimensions or metrics.
4. Implement collection through the tag layer, not ad hoc. Push events via the dataLayer and GTM
   (see `gtm-tags-triggers-variables`) so naming stays consistent and consent gating is central.
5. Mark the two to five events that actually matter as key events in Admin > Key events, because
   more than a handful dilutes reporting and optimization. Set a default value and currency on
   monetizable key events so value-based reporting and bidding have something to optimize.
6. For actions you cannot code right now, create the event from an existing event using a URL or
   parameter condition, then plan to replace it with a real coded event when possible.
7. Link the property to Google Ads and import the key event as a conversion (hand off to
   `ga4-conversions-and-audiences`), because only the ad side can optimize and bill on it.
8. Validate in DebugView and the Realtime report before trusting the data. Confirm the event
   name, every parameter, and that the key-event flag registers. Do not gate a launch on data
   you have not seen fire.

## Decision rules and thresholds

### Recommended vs custom event names

- If Google defines a recommended event for the action, use it exactly. `purchase`, not
  `Purchase`, `buy`, or `order_complete`. Names are case-sensitive and a mismatch fragments data.
- Use a custom event only when no recommended name fits. Custom events do not get prebuilt
  ecommerce or predictive features.
- Never name a custom event with a reserved name or reserved prefix (`ga_`, `google_`,
  `firebase_`). GA4 silently drops or mishandles it. The full reserved list is in
  `references/event-taxonomy-and-reserved-names.md`.

### Key event count and quality

- Mark only the two to five events that represent real business value per property. A property
  with fifteen key events has none. Report clarity and bidding both degrade when everything is
  "key".
- Put a value and currency on any key event tied to money (`purchase`, `generate_lead` with a
  lead value) so value-based bidding and ROAS reporting have signal.
- Key events count on the default counting method for their type. Confirm counting matches how
  the client thinks about the action before you report on it.

### When to create vs modify vs code an event

- Code the event (dataLayer plus GTM) whenever you can. It is the durable, parameter-rich path.
- Create event (no code, from an existing event) when you need a distinct event for a page or
  condition fast and cannot ship code, for example a `thank_you` event when the URL contains
  `/order-confirmation`.
- Modify event to repair a bad name or inject a parameter on events already flowing. Modify
  overwrites the original event, so test on a copy of the condition and watch DebugView, because
  a wrong modify rule quietly corrupts data going forward.

### Collection limits that break data silently

These are hard platform limits. Exceed them and data is truncated or dropped without an error.

- 25 event parameters per event. Design the contract to stay under it.
- Event name under 40 characters, alphanumeric and underscores, must start with a letter.
- Up to 500 distinct event names per property (web) before new names are grouped as "(other)".
- Up to 500 distinct events per app user per day on mobile.
- Register only the parameters you will report on as custom dimensions or metrics; those slots
  are also capped. The full limit table is in
  `references/event-taxonomy-and-reserved-names.md`.

### Key event to Google Ads conversion

- A GA4 key event does not become a Google Ads conversion by itself. Link the property to Google
  Ads, then import the key event as a conversion action on the ad side.
- Imported key-event conversions appear in the Advertising section in GA4 and in Google Ads, but
  imported ones do not show in standard GA4 reports as Google Ads conversions.
- The June 2026 consent change gates whether ads-data (including imported conversions and
  audiences) flows at all. Get the export mechanics and the consent gate from
  `ga4-conversions-and-audiences` before promising a client that conversions will import.

## Reference material

- `references/event-taxonomy-and-reserved-names.md`: the four event categories in full, the
  reserved event names and reserved prefixes you cannot reuse, the automatically collected and
  enhanced measurement event lists, the naming convention (snake_case, case sensitivity), and the
  hard collection limits table. Read this when designing a taxonomy or debugging why a custom
  event is being dropped or grouped as "(other)".
- `references/key-events-vs-conversions-flow.md`: the exact `Event -> Key event -> Conversion`
  model, what changed when GA4 renamed conversions to key events, how to mark and unmark a key
  event, counting methods, default values, where imported conversions do and do not appear, and
  the create-event and modify-event operations with conditions. Read this when a stakeholder is
  confused about terminology or you are wiring the GA4-to-Google-Ads handoff.
- `references/recommended-ecommerce-events.md`: the full ecommerce event sequence with every
  required and recommended parameter, the `items` array field map, filled-in `purchase` and
  `add_to_cart` payloads, the lead-generation and gaming recommended events, and which parameters
  drive which reports. Read this when implementing ecommerce or lead tracking or writing the
  dataLayer contract for a retail client.

## Templates and examples

Retail property, minimal viable key-event set:

- Send the recommended ecommerce sequence: `view_item`, `add_to_cart`, `begin_checkout`,
  `add_shipping_info`, `add_payment_info`, `purchase`, `refund`.
- Mark exactly one key event: `purchase`, with `value` and `currency` populated per transaction.
- Import `purchase` as the Google Ads conversion for bidding. Everything upstream stays reporting
  and audience signal, not a conversion.

Lead-gen property:

- Send `generate_lead` on form submit with a `value` reflecting expected lead worth, plus a
  `lead_source` custom parameter registered as a custom dimension.
- Optionally send `qualify_lead` and `close_convert_lead` further down the funnel.
- Mark `generate_lead` (and `close_convert_lead` if the sales team acts on it) as key events.
- Import `generate_lead` to Google Ads; feed `close_convert_lead` value back through offline
  conversion import for value-based bidding (see `google-ads-conversion-tracking-and-attribution`).

No-code confirmation event:

- Create event `thank_you` from `page_view` where `page_location` contains `/order-confirmation`.
- Mark `thank_you` a key event as a stopgap. Replace it with a coded `purchase` carrying
  transaction parameters as soon as engineering can ship it, because `thank_you` carries no
  revenue.

Filled `purchase` payload (dataLayer): see `references/recommended-ecommerce-events.md` for the
complete object with the `items` array and every parameter typed.

## Common pitfalls

- Custom name where a recommended one exists. `order_complete` instead of `purchase` loses every
  prebuilt ecommerce report and predictive audience. Rename to the recommended event.
- Case and spelling drift. `Purchase`, `add_To_Cart`, or a trailing space create separate events
  that never reconcile. Enforce snake_case in the dataLayer contract, not per developer.
- Reserved name or prefix collision. A custom `page_view` or a `google_` prefixed name is dropped
  or mishandled. Check the reserved list before naming anything.
- Everything marked a key event. Fifteen key events give bidding and reporting no signal about
  what matters. Cut to the two to five that carry real value.
- Over 25 parameters or names over 40 characters. Data truncates silently with no error. Design
  the contract against the limit table up front.
- Assuming a key event auto-imports to Google Ads. It does not. You must link and import, and the
  June 2026 consent gate can block the data entirely. Confirm both before committing to a client.
- Trusting the tag without watching it fire. Reserved-name typos, missing parameters, and broken
  modify rules only show up in DebugView. Verify every event and parameter before launch.
- Modify event corrupting data. A too-broad modify rule overwrites more events than intended and
  the damage is only forward-looking and silent. Scope the condition tightly and watch DebugView.

## Sources

- [Key events vs. conversions](https://support.google.com/analytics/answer/13965727?hl=en) (as of July 2026)
- [About events](https://support.google.com/analytics/answer/9322688?hl=en) (as of July 2026)
- [Event naming rules (reserved names and prefixes)](https://support.google.com/analytics/answer/13316687?hl=en) (as of July 2026)
- [Recommended events](https://support.google.com/analytics/answer/9267735?hl=en) (as of July 2026)
- [Ecommerce events reference](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) (as of July 2026)
- [Create and modify events](https://support.google.com/analytics/answer/12844695?hl=en) (as of July 2026)
- [Analytics audiences in advertising products](https://support.google.com/analytics/answer/12800258?hl=en) (as of July 2026)
