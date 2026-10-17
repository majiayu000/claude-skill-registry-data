---
name: gtm-tags-triggers-variables
description: Build and wire the tag, trigger, and variable configuration in a Google Tag Manager web container for GA4, Google Ads, and Floodlight. Use when the user asks how to set up a GA4 configuration or event tag, a Google Ads conversion or remarketing tag, a Conversion Linker, a Floodlight sales or counter tag, which trigger to use (all pages, custom event, click, form, scroll, element visibility), how the April 2025 Google tag autoload works, tag firing priority or sequencing, tag consent checks, or why a tag is not firing.
---

# GTM tags, triggers, and variables

Wire the three objects a Google Tag Manager web container fires with: tags (what runs), triggers (when it runs), and variables (the values it reads). This skill covers building GA4, Google Ads, and Floodlight tags, choosing the trigger that fires each one, and mapping dataLayer values into variables so every downstream platform gets clean, deduplicated events. Correct wiring here is what makes a key event count once, a conversion attribute to the right click, and a consent check gate the right tag.

This skill assumes you know CPM, CPA, ROAS, and what a conversion is. For the dataLayer contract that feeds these tags (init pattern, ecommerce object schema, push model), see the `gtm-web-container-and-datalayer` skill. For consent state signals and Basic vs Advanced Consent Mode, see `gtm-consent-mode-v2`. For running the same tags through a tagging server, see `gtm-server-side-tagging`.

## When to use this skill

- "Set up a GA4 configuration tag / GA4 event tag in GTM."
- "Add a Google Ads conversion tracking tag / remarketing tag / Conversion Linker."
- "Create a Floodlight sales tag / counter tag in GTM" and "what cart parameters does Floodlight take now?"
- "Which trigger should fire this tag: all pages, custom event, click, form submit, scroll, element visibility, timer?"
- "What is the April 2025 Google tag autoload and do I still need a separate Google tag?"
- "How do tag firing priority, tag sequencing, and once-per-event work?"
- "Add a consent check to a tag so it only fires with ad_storage granted."
- "Why is my tag not firing / firing twice / firing on the wrong pages?"

Boundaries with sibling skills:
- The dataLayer object model, ecommerce schema, and push timing: `gtm-web-container-and-datalayer`.
- Consent Mode v2 signals, default vs update ordering, Basic vs Advanced: `gtm-consent-mode-v2`.
- The server container, clients, and web-to-server transport: `gtm-server-side-tagging`.
- Which GA4 events to send and which to mark as key events: `ga4-events-and-key-events`.
- Floodlight activity/group setup, counting methods, and offline uploads on the CM360 side: `cm360-floodlight-and-conversions`.

## Quick reference

| You need to track | Tag | Trigger | Key variables it reads |
| --- | --- | --- | --- |
| Base GA4 measurement on every page | GA4 configuration (Google tag) | Initialization or All Pages | measurement ID, consent state |
| A GA4 event (purchase, generate_lead, sign_up) | GA4 event | Custom Event on the dataLayer event name | items, value, currency, transaction_id |
| A Google Ads conversion | Google Ads Conversion Tracking | Custom Event on the conversion event | conversion ID/label, value, currency, transaction_id |
| First-party cookies for Google Ads/Floodlight attribution | Conversion Linker | All Pages | (none; reads URL linker params) |
| Google Ads remarketing membership | Google Ads Remarketing | All Pages or page-group trigger | user_id or hashed email if provided |
| A Floodlight counter (page visit, e.g. lead thank-you) | Floodlight Counter | Custom Event or page-view trigger | u-variables, match ID |
| A Floodlight sale (transaction with revenue) | Floodlight Sales | Custom Event on purchase | order ID, revenue, quantity, cart params |

Firing rule of thumb: base/config and Conversion Linker fire on every page; event and conversion tags fire on a Custom Event that matches a named dataLayer push. Never fire a conversion on All Pages.

## Core process

1. Confirm the dataLayer contract first, because a tag can only read values the page has already pushed. Check that the event name and parameters you will trigger and map on exist in the dataLayer (see `gtm-web-container-and-datalayer`). If they do not, fix the dataLayer before building tags; a tag wired to a missing variable silently sends empty values.
2. Lay the base layer. Add one GA4 configuration tag (the Google tag) on the Initialization or All Pages trigger, and one Conversion Linker on All Pages, so Google Ads and Floodlight have first-party cookies to attribute against. As of April 10, 2025 a container that holds Google Ads or Floodlight tags autoloads a Google tag first before sending events, so you no longer hand-place a separate Google tag purely to satisfy those tags, but you still want an explicit GA4 configuration tag to control GA4 settings and consent.
3. Build event tags one per conversion. For each key event, create a GA4 event tag and (if that event is a Google Ads or Floodlight conversion) a matching Google Ads Conversion Tracking or Floodlight tag. Map each parameter from a dataLayer variable, not a hardcoded value, so revenue and IDs come from the page.
4. Choose the narrowest trigger that fires exactly once per real event. Prefer a Custom Event trigger keyed to a named dataLayer push (for example `purchase`, `generate_lead`) over DOM-guessing triggers (Click, Form Submit) because DOM triggers break when markup changes. Reserve auto-event triggers (Click, Element Visibility, Scroll, Timer) for interactions the site does not push to the dataLayer.
5. Set the transaction identifier on every conversion, because deduplication downstream depends on it. Pass `transaction_id` to GA4, the order ID to Google Ads and Floodlight, so GA4, Google Ads, Floodlight, and any DSP can dedupe the same purchase. Reconciliation of those counts lives in `cross-platform-conversion-reconciliation`.
6. Add a consent check to any tag that sets advertising or analytics state. Set the tag's built-in and additional consent checks so it waits for the required signal (for example `ad_storage` for a Google Ads conversion). This is a read-and-recommend step; the signal definitions and Basic vs Advanced behavior are in `gtm-consent-mode-v2`.
7. Preview, do not publish blind. Use the container's preview and debug mode to confirm each tag fires on the right event, once, with the right variable values, before you publish. A live-config change (publishing a container version) is a human gate; recommend the version and its notes, and let a person publish.

## Decision rules and thresholds

### Which trigger fires the tag

| Signal available | Use this trigger | Why |
| --- | --- | --- |
| The site pushes a named event to the dataLayer | Custom Event on that name | Deterministic, survives markup changes, fires once |
| Must run before any tag, to set config/consent | Initialization / Consent Initialization | Guarantees ordering ahead of measurement |
| Needed on literally every page | All Pages | Base tags: GA4 config, Conversion Linker |
| A click with no dataLayer push | Click (All Elements / Just Links) with a filter | Last resort; filter tightly on click classes/URL |
| A form submit with no dataLayer push | Form Submission with a filter | Fragile; a dataLayer push on submit is better |
| Content scrolled into view | Scroll Depth or Element Visibility | Engagement signals, not conversions |
| Time on page threshold | Timer | Rarely a conversion; use for engagement |

Rule: a conversion tag fires on a Custom Event, never on All Pages or a bare pageview, or it will overcount on every page load.

### Firing options that prevent double counting

- Tag firing priority: higher number fires first within the same event. Use it to force the Conversion Linker or a consent tag ahead of conversions.
- Tag sequencing (setup/cleanup tag): fire tag B only after tag A succeeds. Use for a strict dependency, not for ordering you can solve with priority.
- Firing frequency "Once per event" vs "Once per page": set conversion tags to once per event so a single purchase push fires one conversion, even if the page re-triggers.
- Trigger exceptions (blocking triggers): add a blocking trigger to stop a tag on pages where it must not run (for example, block a lead conversion on the confirmation page reload).

### When to route through the server container instead

Fire tags client-side for standard web measurement. Move Google Ads and Floodlight to the server container when you need first-party cookie longevity, want to reduce data sent to third parties from the browser, or need to enrich with server data. Note that as of July 28, 2025 Floodlight tags in server-side Tag Manager transmit unconsented requests server-to-server, which changes what leaves the browser; account for that in your consent posture. Server setup is in `gtm-server-side-tagging`.

### Consent gating

Every Google Ads and Floodlight tag should carry a consent check so it holds until the required signal is granted. The four signals are `ad_storage`, `analytics_storage`, `ad_user_data`, and `ad_personalization`. A June 2026 change gates the flow of ads data on consent, so a tag that ignores consent can drop data or fall out of compliance. Do not hand-roll consent with a Custom HTML tag; use the container's consent settings. Full signal and mode logic is in `gtm-consent-mode-v2`.

## Reference material

- `references/tag-and-trigger-types.md`: every web-container tag type (GA4 configuration and event, Google Ads Conversion Tracking, Conversion Linker, Google Ads Remarketing, Floodlight Counter and Sales, Custom HTML/Image) mapped to its purpose, its usual trigger, its required fields, and the matching GTM API v2 Tag/Trigger resource fields. Read this when building a specific tag or automating container edits through the API.
- `references/apr-2025-google-tag-autoload.md`: what changed on April 10, 2025 (containers with Google Ads or Floodlight tags autoload a Google tag first before sending events), what you still configure by hand, and how it interacts with the GA4 configuration tag and consent. Read this when a user asks whether they still need a separate Google tag or why a Google tag is loading they did not place.
- `references/floodlight-sales-cart-params.md`: the Floodlight sales vs counter decision, counting-method implications for GTM, the standard u-variables, and the July 2025 cart data parameters (Merchant ID, Merchant Feed Label, Merchant Feed Language) with how to map them from the dataLayer. Read this when trafficking a Floodlight sales tag or wiring cart/product parameters.

## Templates and examples

Ecommerce purchase, fully wired (real values):

- dataLayer push on the confirmation page:
  `dataLayer.push({ event: 'purchase', ecommerce: { transaction_id: 'T-48213', value: 129.90, currency: 'USD', items: [{ item_id: 'SKU-7', quantity: 2, price: 64.95 }] } });`
- GA4 event tag: event name `purchase`, trigger Custom Event `purchase`, parameters `value` = {{DLV - ecommerce.value}}, `currency` = {{DLV - ecommerce.currency}}, `transaction_id` = {{DLV - ecommerce.transaction_id}}, items from the ecommerce object.
- Google Ads Conversion Tracking tag: conversion ID `AW-1234567890`, label `AbC-D_efG`, trigger Custom Event `purchase`, value {{DLV - ecommerce.value}}, currency {{DLV - ecommerce.currency}}, order ID {{DLV - ecommerce.transaction_id}}, once per event, consent check requires `ad_storage`.
- Floodlight Sales tag: advertiser and activity from CM360, trigger Custom Event `purchase`, revenue {{DLV - ecommerce.value}}, order ID {{DLV - ecommerce.transaction_id}}, quantity from items, consent check requires `ad_storage`.
- Conversion Linker: trigger All Pages, no parameters. GA4 configuration tag: trigger Initialization.

Lead form (no ecommerce), example:

- dataLayer push on submit success: `dataLayer.push({ event: 'generate_lead', lead_type: 'demo_request', form_id: 'contact-hero' });`
- GA4 event tag `generate_lead` on Custom Event `generate_lead`, parameter `lead_type` = {{DLV - lead_type}}.
- Google Ads Conversion Tracking tag for the lead conversion action on the same Custom Event, no value or a static lead value, once per event, consent requires `ad_storage`.
- Floodlight Counter tag on the same Custom Event with a unique match ID, consent requires `ad_storage`.

Variable naming convention that scales: prefix Data Layer Variables `DLV - `, Constants `C - `, Lookup Tables `LT - `, so anyone reading the container knows a variable's source at a glance.

## Common pitfalls

- Conversion tag on All Pages. Fires on every page view and overcounts wildly. Move it to a Custom Event trigger keyed to the purchase or lead push.
- Missing Conversion Linker. Without it, Google Ads and Floodlight cannot set first-party cookies, so click-through conversions under-report. Add it on All Pages and give it firing priority so it runs before conversions.
- Hardcoded value or currency. A tag with a fixed value sends the same revenue for every order. Map value, currency, and IDs from Data Layer Variables.
- No `transaction_id` / order ID. Without a shared identifier, GA4, Google Ads, and Floodlight cannot dedupe the same sale, and reconciliation breaks. Always pass it.
- Firing twice from two triggers. A tag on both a page-path pageview and a Custom Event fires twice. Pick one trigger and set once-per-event.
- Consent check omitted on ad tags. The tag fires before consent is granted and can drop data or breach policy after the June 2026 gating change. Add the built-in consent check; do not fake it with Custom HTML.
- DOM-guessing triggers that break. A Click or Form Submission trigger matched on a CSS class breaks the next time the site's markup changes. Ask for a dataLayer push instead and trigger on it.
- Publishing without preview. Publishing a container version is a live change. Confirm every tag in preview/debug first, then let a person publish the version.

## Sources

- [Google Tag Manager release notes](https://support.google.com/tagmanager/answer/4620708?hl=en) (as of July 2026)
- [Set up consent management (Consent Mode)](https://developers.google.com/tag-platform/security/guides/consent) (as of July 2026)
- [The data layer](https://developers.google.com/tag-platform/tag-manager/datalayer) (as of July 2026)
- [Set up Google Ads conversion tracking (server-side)](https://developers.google.com/tag-platform/tag-manager/server-side/ads-setup) (as of July 2026)
- [Tag Manager API v2](https://developers.google.com/tag-platform/tag-manager/api/v2) (as of July 2026)
