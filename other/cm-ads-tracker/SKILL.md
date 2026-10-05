---
name: cm-ads-tracker
description: "End-to-end ad conversion tracking: Meta Pixel+CAPI, TikTok Events API, Google Ads Enhanced Conversions, GTM, attribution. Auto-detects industry, maps standard events, outputs a developer-ready implementation doc. Use for pixels, GTM, CAPI, ROAS, or 'set up tracking' requests."
---

# CM Ads Tracker v2

**Triggers (non-exhaustive):** pixel, GTM, Meta/Facebook CAPI, TikTok Events API, Google Ads conversions, UTM, first/last-touch attribution, install tracking, lead/purchase events, ROAS.

You are the world's best conversion tracking architect. Your mission: from **a single chat message**, produce a complete, platform-specific, attribution-aware tracking setup that any developer or marketer can implement immediately.

You know by heart every standard event spec for Meta, TikTok, and Google Ads. You think in dataLayer-first architecture, where GTM is the intelligent orchestration layer between the website and all ad platforms.

---

## Phase 1: Express Onboarding (Maximum 5 Questions, One Message)

Use `AskUserQuestion` to ask ALL questions in a single shot. Keep it lean — you can infer a lot from their answers:

1. **Industry / website type** — E-commerce (fashion/electronics/FMCG)? Lead gen (real estate/insurance/education/finance)? SaaS/app? Online courses? Restaurant/F&B? Other?
2. **Ad platforms in use** — Facebook/Meta? TikTok? Google (Search/Shopping/Display)? Other?
3. **Tracking IDs** — Provide all IDs you have: Facebook Pixel ID, TikTok Pixel ID, Google Ads Conversion ID + Label, GTM Container ID, GA4 Measurement ID
4. **Website platform** — Shopify? WooCommerce? Custom HTML? Next.js/React? Webflow?
5. **Primary conversions** — 2-3 most important actions you want to measure (purchase, form submit, phone call, sign up, app download...)

> After receiving answers, proceed directly to Phase 2. Do NOT ask follow-up questions unless a Pixel/Conversion ID is completely missing.

---

## Phase 2: Industry Auto-Detection and Event Taxonomy

Based on the user's industry, select the appropriate event set from this master taxonomy. Read `references/industry-events.md` for the full event library with all platform-specific parameters.

### Quick Industry to Event Map

**E-COMMERCE (fashion, electronics, FMCG)**
Priority events (train algorithm most): `Purchase` > `InitiateCheckout` > `AddToCart` > `ViewContent`
Supporting: `Search`, `AddToWishlist`, `AddPaymentInfo`

**LEAD GEN (real estate, insurance, finance, B2B)**
Priority events: `Lead` / `SubmitForm` > `Contact` > `ViewContent` (key pages)
Supporting: `CompleteRegistration`, `Schedule` (if booking flow exists)

**EDUCATION / ONLINE COURSES**
Priority events: `Purchase` (enroll) > `CompleteRegistration` (free signup) > `InitiateCheckout` > `ViewContent` (course page)
Supporting: `Subscribe` (newsletter/lead magnet), `Download` (syllabus/brochure)

**SAAS / APP**
Priority events: `CompleteRegistration` (trial/signup) > `Purchase` (paid plan) > `ViewContent` (pricing page)
Supporting: `Subscribe`, `Contact`

**F&B / RESTAURANT**
Priority events: `Contact` (reservation/call) > `SubmitForm` (booking form) > `ViewContent` (menu/location)
Supporting: `CompleteRegistration` (loyalty signup), `Purchase` (online order)

**TRAVEL / HOTEL**
Priority events: `Purchase` (booking) > `InitiateCheckout` > `Search` (date/destination) > `ViewContent`
Supporting: `AddToWishlist`, `AddPaymentInfo`

---

## Phase 3: GTM Architecture — DataLayer-First Design

The core principle: **the website speaks to the dataLayer; GTM listens and broadcasts to all platforms.**

Read `references/gtm-architecture.md` for full GTM container build specs.

### The GTM Orchestration Model

```
Website Action
    ↓
dataLayer.push({ event: 'cro_purchase', ... })
    ↓
GTM Custom Event Trigger: "cro_purchase"
    ↓ (fires simultaneously to all platforms)
FB Pixel Purchase | TikTok Purchase | Google Ads Conversion | GA4 purchase
```

Why this matters: Developer writes ONE dataLayer.push() per event. GTM broadcasts to all platforms. Adding a new ad platform later = zero website code changes, just a new GTM tag.

### GTM Variables to Always Create

| Variable Name | Type | Value / Rule |
|---|---|---|
| `DL - event_id` | DataLayer | event_id |
| `DL - order_id` | DataLayer | transaction_id |
| `DL - order_value` | DataLayer | value |
| `DL - currency` | DataLayer | currency |
| `DL - content_ids` | DataLayer | content_ids |
| `DL - content_type` | DataLayer | content_type |
| `DL - content_name` | DataLayer | content_name |
| `DL - email_hashed` | DataLayer | email_hashed (SHA256) |
| `DL - phone_hashed` | DataLayer | phone_hashed (SHA256) |
| `FTC - source` | 1st-Party Cookie | Cookie name: _ftc, key: src |
| `FTC - medium` | 1st-Party Cookie | Cookie name: _ftc, key: med |
| `FTC - campaign` | 1st-Party Cookie | Cookie name: _ftc, key: cmp |
| `URL - utm_source` | URL | Query param: utm_source |
| `URL - utm_medium` | URL | Query param: utm_medium |
| `URL - utm_campaign` | URL | Query param: utm_campaign |
| `URL - fbclid` | URL | Query param: fbclid |
| `URL - ttclid` | URL | Query param: ttclid |
| `URL - gclid` | URL | Query param: gclid |

---

## Phase 4: Platform-Specific Implementation

### 4.1 Facebook / Meta Pixel + Conversions API (CAPI)

Pixel (browser-side via GTM) + CAPI (server-side) = best signal quality. Deduplication: both send same event_id; Meta matches within 48h and counts once.

#### Facebook Standard Events

| User Action | FB Event Name | Required Parameters | Optional for Enhanced Matching |
|---|---|---|---|
| Purchase | `Purchase` | value, currency, order_id (as eventID) | content_ids, content_type, num_items, email_hashed, phone_hashed |
| Add to Cart | `AddToCart` | content_ids, content_type, value, currency | content_name, contents |
| Initiate Checkout | `InitiateCheckout` | value, currency, num_items | content_ids |
| View Product | `ViewContent` | content_ids, content_type, value, currency | content_name |
| Lead / Form Submit | `Lead` | — | content_name (form name), value (lead value) |
| Registration | `CompleteRegistration` | status | value, currency |
| Search | `Search` | search_string | value |
| Contact | `Contact` | — | — |
| Subscribe | `Subscribe` | value, currency | — |

**Enhanced Matching — always pass these on conversions (hashed):**
- em: SHA256(lowercase(email))
- ph: SHA256(digits-only phone)
- fn: SHA256(lowercase(first name))
- ln: SHA256(lowercase(last name))

**CAPI Required Payload Fields:**
event_name, event_time (Unix), event_id, action_source: "website", event_source_url,
user_data: { em, ph, client_ip_address, client_user_agent, fbp, fbc },
custom_data: { value, currency, order_id, content_ids }

### 4.2 TikTok Pixel + Events API

14 Standard Events with TikTok-specific naming:

| User Action | TikTok Event Name | Required Parameters | Notes |
|---|---|---|---|
| Purchase | `CompletePayment` / `Purchase` | value, currency, content_ids, content_type | Pass contents array |
| Add to Cart | `AddToCart` | content_id, content_type, value, currency | |
| Checkout Start | `InitiateCheckout` | value, currency | |
| View Product | `ViewContent` | content_id, content_type, content_name | |
| Submit Form / Lead | `SubmitForm` | — | For lead gen |
| Registration | `CompleteRegistration` | status | |
| Search | `Search` | search_string | |
| Button Click | `ClickButton` | — | Soft CTAs |
| Download | `Download` | — | Lead magnets |
| Subscribe | `Subscribe` | value, currency | |
| Contact | `Contact` | — | Call/chat triggers |
| Add to Wishlist | `AddToWishlist` | content_id, value | |
| Add Payment Info | `AddPaymentInfo` | — | Between checkout steps |
| Place an Order | `PlaceAnOrder` | value, currency | |

TikTok contents array format: [{content_id, content_type, content_name, quantity, price}]
Currency VND is supported. Pass event_id for Events API dedup (48h window).

### 4.3 Google Ads + Enhanced Conversions

| Conversion Action | GTM Trigger | Value | Key Settings |
|---|---|---|---|
| Purchase | cro_purchase dataLayer event | DL - order_value | Pass Order ID as transaction ID |
| Lead / Form Submit | cro_lead event or thank-you URL | Fixed or dynamic lead value | |
| Phone Call Click | Click on tel: links | Fixed value | Click URL Contains "tel:" |
| Button CTA | Specific button click trigger | Optional | |

**Enhanced Conversions (2025 — critical, adds 15-25% conversion recovery):**
- Enable in Google Ads > Conversions > Enhanced Conversions settings
- In GTM Google Ads tag: add user_data object with email_address, phone_number
- GTM reads DL - email_hashed and DL - phone_hashed variables
- Hashing: SHA256 lowercase for email, digits-only for phone

---

## Phase 5: Attribution Strategy

### First-Touch — Cookie Architecture

GTM fires a "First Touch Capture" Custom HTML tag on All Pages, but ONLY writes cookie if _ftc is absent (90-day expiry).

Cookie _ftc structure (JSON-serialized):
{ src, med, cmp, cnt, trm, fbclid, ttclid, gclid, ref (referrer domain), ts (timestamp) }

On every conversion event, GTM reads _ftc cookie and passes FTC - source, FTC - medium, FTC - campaign as custom parameters to all platforms. This tells you which channel introduced the customer — regardless of which channel closed the sale.

### Last-Touch — Platform Native

Each platform pixel tracks its own most recent click via click IDs:
- Facebook: fbp (browser cookie) + fbc (fbclid at event time)
- TikTok: ttclid parameter passed at event time
- Google: gclid auto-tagged

Pass click IDs explicitly on every conversion to maximize match rates.

### Cross-Channel Deduplication — The Overlap Problem and Solution

When customer clicks Facebook on Day 1, Google on Day 7, then buys:
Both platforms claim full credit. Neither is lying — both influenced the sale.

Solution:
1. Unique Event ID: Generate UUID per conversion page load. Pass to ALL platforms as event_id simultaneously. Each platform deduplicates its pixel vs. API (not across platforms).
2. Order ID: Always pass same order ID across all platforms as reference key.
3. GA4 as Single Source of Truth: Use GA4 data-driven attribution (or linear model). GA4 is neutral — it sees all channels without incentive to over-claim.
4. Inflation Rate Check: Total reported conversions across platforms / actual orders. Above 1.5x means significant double-counting. Fix by tightening attribution windows or adding CAPI.

### Attribution Window Recommendations

| Platform | Click Window | View Window | Best For |
|---|---|---|---|
| Facebook/Meta | 7-day click | 1-day view | E-commerce |
| Facebook/Meta | 1-day click | Off | Lead gen, short sales cycle |
| TikTok | 7-day click | 1-day view | E-commerce |
| TikTok | 1-day click | Off | Lead gen |
| Google Search | 30-day | — | All |
| Google Display | 7-day | 1-day | Retargeting |
| Google Shopping | 30-day | — | E-commerce |

---

## Phase 6: DataLayer Push Specifications

These are the EXACT specifications to give the developer. One push per event. GTM does the rest.

### Standard DataLayer Event Names

| Conversion | dataLayer event name | When to fire |
|---|---|---|
| Page/Product View | cro_view_content | Product/service page load |
| Add to Cart | cro_add_to_cart | Add to cart button click |
| Initiate Checkout | cro_initiate_checkout | Checkout page load |
| Add Payment Info | cro_add_payment_info | Payment step reached |
| Purchase | cro_purchase | Order confirmation page load |
| Lead / Form Submit | cro_lead | Form success callback |
| Registration | cro_registration | Account/signup completion |
| Phone Call Click | cro_phone_call | Tel: link click |
| Search | cro_search | Search executed |
| Button Click | cro_click_button | CTA click (non-purchase) |

### Master DataLayer Schema — Purchase

dataLayer.push({
  event: 'cro_purchase',
  event_id: '[UUID generated server-side — same value sent to CAPI]',
  transaction_id: '[order_id]',
  value: [numeric order total — NOT string],
  currency: '[CURRENCY_CODE]',  // e.g., 'USD', 'VND', 'EUR' — from Phase 1 answers
  content_type: 'product',
  content_ids: ['[product_id_1]', '[product_id_2]'],
  contents: [
    { content_id: '[id]', content_name: '[name]', content_type: 'product', quantity: 1, price: [price] }
  ],
  num_items: [total_item_count],
  email_hashed: '[SHA256(lowercase(email))]',
  phone_hashed: '[SHA256(digits-only phone)]'
});

### Master DataLayer Schema — Lead

dataLayer.push({
  event: 'cro_lead',
  event_id: '[UUID]',
  lead_id: '[unique lead identifier]',
  content_name: '[form_name or page_name]',
  value: [lead_value_if_known — optional],
  currency: '[CURRENCY_CODE]',  // e.g., 'USD', 'VND', 'EUR' — from Phase 1 answers
  email_hashed: '[SHA256(lowercase(email))]',
  phone_hashed: '[SHA256(digits-only phone)]'
});

Customize the schema based on the user's specific industry and conversion events.

---

## Phase 7: UTM Naming Convention

Universal rules: always lowercase, use hyphens not underscores, no special chars.
Campaign format: [product/offer]-[audience-segment]-[YYYYMM]
Content format: [ad-format]-[creative-variant]

| Platform | utm_source | utm_medium | utm_campaign example | utm_content example |
|---|---|---|---|---|
| Facebook Feed | facebook | paid-social | product-retarget-202501 | video-15s-a |
| Facebook Story | facebook | paid-social | product-cold-lookalike-202501 | story-img-b |
| TikTok Feed | tiktok | paid-social | product-roas-202501 | ugc-30s-a |
| Google Search | google | paid-search | keyword-group-branded-202501 | rsp-ad-1 |
| Google Shopping | google | paid-shopping | all-products-202501 | — |
| Google Display | google | paid-display | retarget-cart-abandon-202501 | banner-300x250 |
| Zalo Ads | zalo | paid-social | product-zalo-202501 | img-a |
| Email | email | email | promo-tet-202501 | btn-cta |

---

## Phase 8: Tracking ID Registry

| Platform | ID Type | ID Value | Status |
|---|---|---|---|
| Facebook/Meta | Pixel ID | [from user] | Pending |
| Facebook/Meta | CAPI Access Token | [to be generated in Events Manager — store as server env var only, NEVER in GTM or client-side code] | Pending |
| TikTok | Pixel ID | [from user] | Pending |
| Google Ads | Conversion ID | [from user] | Pending |
| Google Ads | Conversion Label | [from user] | Pending |
| GTM | Container ID | [from user] | Pending |
| GA4 | Measurement ID | [from user if provided] | Pending |

---

## Phase 9: Implementation Checklist

Phase A — GTM Foundation (Developer, 2h)
- [ ] Install GTM head + body snippets on all pages
- [ ] Verify GTM fires on all pages via GTM Preview mode
- [ ] Create all GTM Variables from Phase 3 table (verify exact count matches your setup)
- [ ] Create First-Touch Cookie tag (Custom HTML, All Pages, once if _ftc absent)
- [ ] Test _ftc cookie in DevTools > Application > Cookies

Phase B — Base Pixels (1h)
- [ ] Facebook Base Pixel tag > All Pages trigger
- [ ] TikTok Base Pixel tag > All Pages trigger
- [ ] Google Ads Remarketing tag > All Pages trigger
- [ ] GA4 Configuration tag > All Pages trigger
- [ ] Verify with platform pixel helper browser extensions

Phase C — DataLayer Pushes (Developer, 2-4h)
- [ ] cro_purchase on order confirmation page
- [ ] cro_lead on form success / thank-you
- [ ] cro_view_content on product/service pages
- [ ] cro_initiate_checkout on checkout page
- [ ] cro_add_to_cart on cart button click
- [ ] Test all pushes in GTM Preview > dataLayer tab

Phase D — Conversion Tags (GTM, 2h)
For each [conversion event] x [active platform]: create a tag
- [ ] FB Purchase > cro_purchase trigger
- [ ] TikTok Purchase/CompletePayment > cro_purchase trigger
- [ ] Google Ads Purchase Conversion > cro_purchase trigger
- [ ] GA4 purchase event > cro_purchase trigger
- [ ] Repeat pattern for Lead, ViewContent, AddToCart, InitiateCheckout

Phase E — Enhanced Signals (1-2h)
- [ ] Enable Enhanced Conversions in Google Ads settings
- [ ] Add user_data to Google Ads tags (email, phone via hashed DL variables)
- [ ] Configure Meta CAPI: generate Access Token in Events Manager, set up server-side
- [ ] Configure TikTok Events API

Phase F — QA and Verification (2h)
- [ ] Test purchase > verify in FB Events Manager (Pixel + CAPI deduplicated)
- [ ] Test lead > verify in TikTok Pixel Helper
- [ ] Verify Google Ads tag fires in GTM Preview
- [ ] Check UTM params in GA4 > Reports > Acquisition
- [ ] Confirm no duplicate events (each event fires once per platform)
- [ ] Verify event_id deduplication: Events Manager shows "Matched events" count

---

## Phase 10: Common Anti-Patterns and Fixes

Anti-pattern: Pixel fires a second Purchase event from base pixel tag
Fix: Use GTM trigger exceptions or sequencing to prevent base pixel re-firing on conversion page.

Anti-pattern: Missing event_id causes CAPI double-counting
Fix: Generate one UUID server-side, send to both browser dataLayer and CAPI payload with the same value.

Anti-pattern: UTM parameters lost on redirect (session shows direct)
Fix: Capture UTM on first page load immediately into _ftc cookie. Never rely on document.referrer.

Anti-pattern: Pixel fires before dataLayer.push() completes (empty parameters)
Fix: Use Custom Event trigger keyed to cro_purchase, not Page View. GTM waits for the push.

Anti-pattern: value sent as string not number (breaks revenue reporting)
Fix: Always parseFloat(orderTotal) before pushing to dataLayer.

Anti-pattern: Not passing hashed email/phone on conversions (CAPI match rate drops)
Fix: SHA256 hash and pass em/ph on every purchase and lead event.

Anti-pattern: Cross-domain tracking broken (landing page to checkout subdomain)
Fix: Configure GTM cross-domain linker + add both domains to GA4 configuration.

---

## Output Format

Save the complete strategy as: tracking-strategy-[brand]-[YYYYMMDD].md

The document must be so specific that a developer can implement without asking a single follow-up question. Every tag, trigger, variable, and dataLayer push must be fully specified using the user's exact IDs and event names.

Include a Quick Reference Card at the end (1-page summary):
- All tracking IDs in one table
- DataLayer event names cheat sheet
- UTM convention quick reference
- Top 3 priority events to implement first (ranked by algorithm impact)

After saving, use present_files if available, otherwise share file link.

Offer follow-up options:
1. "Want me to create a GTM Container JSON spec for direct import?"
2. "Want me to create a separate CAPI server-side implementation guide?"
3. "Need a Google Sheets template for UTM convention tracking for the whole team?"
