---
name: operating-shopify-store
version: "1.0.0"
description: >
  Manages FlashFusion's Shopify storefront operations — product management,
  order fulfillment, basic analytics, and storefront health. Note: the Wix
  store is no longer active; FlashFusion's primary platform is now two Base44
  apps. This skill covers Shopify as an active or future e-commerce surface.
  Activates when the user mentions: Shopify, storefront, product listing,
  order, fulfillment, inventory, discount, e-commerce, digital products,
  sell online, or any mention of Shopify operations for FlashFusion.
---

# Shopify Store Operations

Covers Shopify operations for FlashFusion. The primary platform (audit.flashfusion.co
and app.flashfusion.co) runs on Base44 — Shopify is the e-commerce layer for
digital products or physical goods if that becomes an active FlashFusion channel.

---

## Evals

**Should trigger:**
1. "Add a new digital product to the FlashFusion Shopify store"
2. "Check if there are any unfulfilled orders"
3. "Set up a discount code for newsletter subscribers"

**Should NOT trigger:**
1. "Help me design the app.flashfusion.co UI" — Base44 app, not Shopify
2. "I want to build a new product idea" — product strategy, not store operations

---

## Current Context

The Wix store that previously existed is gone. Shopify is connected via MCP.

Before running any Shopify operation, confirm:
1. The store is active (not paused or on a trial that's expired)
2. The product type (digital download, physical product, or service)
3. Whether this is a new product launch or maintenance on existing inventory

If the store is not yet actively selling: this skill functions as a
readiness checklist rather than an operational workflow.

---

## Section 1: Product Management

### Adding a digital product

1. Shopify Admin → Products → Add product
2. Title: clear, searchable, benefit-forward
3. Description: what it is, who it's for, what they'll be able to do
4. Price: set based on FlashFusion pricing framework
5. Product type: select `Digital` or appropriate category
6. For digital downloads:
   - Install Digital Downloads app (free from Shopify App Store)
   - Attach the file to the product
   - Set automatic fulfillment (no manual action needed on purchase)
7. Images: high-quality product mockup or cover image
8. SEO fields: title and description for search indexing

### Keeping products current

Review active products quarterly:
- Is the content still accurate?
- Is the price still appropriate?
- Any reviews or feedback that should inform updates?

---

## Section 2: Order Management

### Checking for unfulfilled orders

Shopify Admin → Orders → filter by Unfulfilled.

For digital products with automatic fulfillment: unfulfilled orders
should not exist. If they do, check the Digital Downloads app is
configured and the product has an attached file.

For physical products: fulfill by shipping and entering tracking info.

### Refunds and customer issues

For a refund request:
1. Shopify Admin → Orders → select the order
2. Refund → choose full or partial → confirm
3. Send confirmation to customer

For a dispute: check Shopify's dispute resolution process if the
charge was through Shopify Payments. Log in the FlashFusion client
communication record if relevant.

---

## Section 3: Discounts and Promotions

### Creating a discount code

Shopify Admin → Discounts → Create discount

Common FlashFusion discount patterns:
- Newsletter subscriber code: 10–15% off, single use per customer
- Workshop attendee code: fixed amount or percentage, time-limited
- Referral code: percentage off, no expiry

Track which codes are active and when they expire. Expired codes that
are still shared generate customer service requests — clean them up
quarterly.

---

## Section 4: Basic Analytics

Shopify Analytics (Admin → Analytics) surfaces:
- Total sales by period
- Top products by revenue
- Traffic sources (where buyers found the store)
- Conversion rate (sessions that became purchases)

**Monthly review questions:**
- Which product generated the most revenue?
- Where is traffic coming from? (Newsletter link, LinkedIn, search?)
- What is the conversion rate? (Industry average for Shopify: ~2–3%)

Connect Shopify revenue to the FlashFusion Finance log (managing-ff-finances)
as a separate revenue stream from consulting income.

---

## Self-Verification

Monthly (if store is active):
- [ ] Unfulfilled orders checked and resolved
- [ ] Active discount codes reviewed — expired ones deactivated
- [ ] Revenue logged in managing-ff-finances

Quarterly:
- [ ] Product descriptions reviewed for accuracy
- [ ] Analytics reviewed — top products, traffic sources, conversion rate
- [ ] Any inactive products archived (not deleted — preserves order history)

---

## CLAIMS
- Digital products with automatic fulfillment generate revenue with no
  manual fulfillment work — the setup investment is one-time
- Archiving rather than deleting inactive products preserves order
  history and customer purchase records

## COUNTEREXAMPLE
- If the Shopify store is not actively generating sales, this skill's
  monthly checks are unnecessary overhead — apply only when the store
  is an active revenue channel

## CONTRADICTIONS
- "Track Shopify revenue in managing-ff-finances" assumes Shopify is
  a separate revenue stream from consulting; if Shopify only sells
  consulting packages or services, it should feed the same invoice
  tracking log rather than a separate one
