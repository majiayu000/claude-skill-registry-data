---
name: google-ads-shopping-and-feed
description: Set up Google Merchant Center and the product feed, optimize product data for query coverage, diagnose disapprovals, and decide how Shopping campaigns sit next to Performance Max. Use when the user asks about Google Shopping, Merchant Center or Merchant Center Next, product feed, feed optimization, feed quality, product attributes, GTIN or product identifiers, product titles and images, supplemental feeds or feed rules, product disapprovals or the diagnostics view, product-level CPA or ROAS, Shopping vs Performance Max, or Shopping campaign priority.
---

# Google Ads Shopping and feed

Set up Merchant Center, get the product feed clean and approved, optimize product data so it matches the queries you want to win, and decide how Shopping campaigns coexist with Performance Max. For retail, the feed is the campaign: there are no keywords and there is no ad copy to write, so the product data (title, image, identifiers, attributes) is what enters the auction. Most retail performance problems trace back to the feed, not the bid.

Google Ads is Google's self-service auction platform across Search, Shopping, YouTube, the Display Network, Discover, Gmail, and Maps. Merchant Center is the separate product-data hub that feeds it. This is a different platform from DV360; do not carry DV360 line-item or insertion-order concepts into Google Ads. For KPI definitions and goal math (CPA, ROAS, CPM), see the `programmatic-foundations` skill. For choosing Shopping against other campaign types, see `google-ads-campaign-types`. For Performance Max setup and tuning, see `google-ads-performance-max`. For bid-strategy mechanics, see `google-ads-bidding`, and for reporting and feeding conversion values, see `value-based-bidding`.

## When to use this skill

- "How do I set up Merchant Center / Merchant Center Next?" / "How do I upload my product feed?"
- "What product attributes are required vs recommended?" / "Do I need a GTIN?"
- "How do I optimize my product titles / descriptions / images?" / "Why is my product not showing for X searches?"
- "What is a supplemental feed / feed rule / attribute rule?"
- "My products are disapproved." / "What is the diagnostics / Needs attention view telling me?"
- "Which products are driving my CPA / ROAS?" / "How do I analyze performance at the product level?"
- "Shopping vs Performance Max?" / "How do listing groups relate to product groups?"
- "I run Standard Shopping and Performance Max on the same products. Which one serves?"

Boundaries with sibling skills:
- Which campaign type to run at all (Search, Shopping, Demand Gen, Video, App): `google-ads-campaign-types`.
- Performance Max setup, asset groups, audience signals, and listing-group tuning: `google-ads-performance-max`. This skill covers the feed that PMax consumes and how the two interact, not PMax internals.
- Bid strategy choice and mechanics (Target ROAS, Maximize conversion value, learning period): `google-ads-bidding`.
- Reporting conversion values back so bidding can optimize on margin or value: `value-based-bidding`.
- Conversion tracking and attribution that Smart Bidding depends on: `google-ads-conversion-tracking-and-attribution`.
- Reading results against the goal the campaign serves: `reporting-by-campaign-goal`.

## Quick reference

Where the levers are in retail:

| Lever | Lives in | Controls |
| --- | --- | --- |
| Product data (title, image, attributes, identifiers) | Merchant Center feed | Whether the product is eligible and which queries it matches |
| Feed structure (data sources, supplemental sources, rules) | Merchant Center | How the feed is assembled, fixed, and enriched |
| Approval status | Merchant Center diagnostics | Whether a product can serve at all |
| Campaign type and priority | Google Ads | Which campaign bids for a product and on what surface |
| Bid strategy and conversion values | Google Ads | How aggressively each product bids toward the goal |

Shopping surface decision in one table:

| Situation | Run | Why |
| --- | --- | --- |
| Want explicit control of product groups, bids, and a contained surface | Standard Shopping | Product groups expose product-level bidding on Search and the Shopping tab |
| Want maximum reach and AI optimization across all Google channels for the catalog | Performance Max with the feed | Listing groups extend the same catalog across every channel |
| Want both: a controlled baseline plus broad automated reach | Both, with priority understood | Performance Max generally takes precedence for the same products (see priority below) |
| No working conversion tracking yet | Neither | Smart Bidding has nothing to optimize toward; set up tracking first |

Required versus recommended attributes change over time, so confirm the current list in the product data specification rather than trusting a hardcoded set. The stable concept: a small set of attributes is required for every product (identifier, title, description, link, image, price, availability, condition), identifier attributes (GTIN, brand, MPN) are required or conditionally required by product type, and a wider set is recommended because it improves matching and eligibility for richer formats.

## Core process

1. Create and verify the Merchant Center account. Tell Merchant Center about the business and where you sell (online, in store, or both), then claim and verify the website so product links resolve to a site you own. Without a verified, claimed site the feed cannot serve.
2. Choose how product data enters Merchant Center. Options include automatic extraction from the store, an ecommerce-platform connection, a scheduled file or Google Sheet, manual entry, or the API. Pick the most automated path the platform supports so the feed stays fresh; stale prices and availability cause disapprovals and wasted spend.
3. Build the primary data source with correct required attributes. The primary data source is the main source Merchant Center uses for product data. Get the required attributes right first (identifier, title, description, link, image_link, price, availability, condition) before optimizing anything, because a product missing a required attribute will not serve.
4. Get product identifiers right. Submit a valid GTIN where one exists; for products that genuinely have no GTIN (custom, vintage, one-of-a-kind), set the identifier-exists attribute to false rather than inventing one. Correct identifiers improve matching and unlock eligibility; wrong or missing ones are a common disapproval.
5. Optimize titles, descriptions, and images for query coverage. The title is the single strongest relevance signal because there are no keywords. Front-load the terms a shopper would search (brand, product type, key attributes) within the character limit, keep descriptions accurate and specific, and use a clear principal product image on a plain background. See Feed optimization below.
6. Enrich and fix with supplemental sources and attribute rules. Use a supplemental data source to enhance or override the primary data (better titles, extra images, custom labels) without re-exporting the whole feed, and use attribute rules to transform data to meet the specification (fix formatting, map values, set defaults). These are how you improve a feed you do not fully control at the source.
7. Resolve disapprovals in the diagnostics view before scaling spend. Work the Needs attention and item-issue views: fix account-level issues first (they can suppress everything), then product-level disapprovals and warnings. A campaign cannot perform on products that are not approved.
8. Structure the campaign and add conversion values. For Standard Shopping, organize products into product groups for product-level bidding; for Performance Max, organize listing groups by Merchant Center attributes. Report conversion values so Smart Bidding can optimize toward revenue or margin (see `value-based-bidding` and `google-ads-bidding`).
9. Analyze at the product level and act on the feed first. Pull performance by product or product group, find the products carrying or dragging CPA and ROAS, and ask whether the fix is a feed change (title, image, identifier, exclusion) before it is a bid change. In Shopping, the feed is usually the faster lever.

## Decision rules and thresholds

- Fix the feed before you touch bids. In retail the product data decides eligibility and matching, so a disapproval, a weak title, or a missing identifier costs more than a suboptimal bid. Clear disapprovals first, then optimize titles and images, then tune bids.
- Treat the title as the primary keyword surrogate. With no keywords, the title carries most of the matching weight. Lead with the terms shoppers actually type; do not bury the product type behind marketing phrasing.
- Submit a GTIN whenever the product has one. Valid identifiers improve matching and eligibility. Only set identifier-exists to false for products that truly lack a GTIN, and never fabricate one.
- Use a supplemental source, not a feed rebuild, for enrichment. When the source system cannot produce the data you need (better titles, custom labels, extra fields), layer a supplemental source over the primary rather than re-engineering the export.
- Account issues outrank item issues. An account-level problem can suppress the whole catalog, so resolve those before chasing individual product disapprovals.
- Decide Shopping versus Performance Max on control versus reach, and know who wins for shared products. Standard Shopping gives product-group control on a contained surface; Performance Max gives automated reach across all channels. When the same products run in both, Performance Max generally serves over Standard Shopping (see priority below), so run both only deliberately.
- Use campaign priority only within Standard Shopping. Priority (High, Medium, Low; default Low) decides which Standard Shopping campaign bids when a product is in more than one, with the higher-priority campaign bidding even at a lower bid. It does not arbitrate between Shopping and Performance Max.
- Do not over-subdivide product groups or listing groups. More subdivisions means thinner data and slower learning per group. Split by a real dimension (category, brand, custom label, margin tier) and stop.

## Feed optimization for query coverage

Because there are no keywords, query coverage comes from the product data. Optimize in this order:

- Title. The highest-leverage attribute. Include the terms a shopper searches, ordered by importance, within the character limit in the specification. A practical pattern is brand plus product type plus key distinguishing attributes (size, color, material, model, gender, quantity) in the order your buyers search them. Match the title to the product on the landing page; do not keyword-stuff or add promotional text, which can trigger disapprovals.
- Description. Accurate, specific, and complete. It is a weaker matching signal than the title but still contributes and supports richer listings. Describe the product, not the brand story, and keep it consistent with the landing page.
- Image. Use a clear principal image of the product on a plain background, meeting the image requirements in the specification. Generic, placeholder, or logo images are disapproved, and a poor image suppresses click-through even when the product is eligible.
- Identifiers and attributes that widen eligibility. GTIN, brand, MPN, product category, product type, and structured attributes (color, size, gender, age group, material) help Google understand and match the product and qualify it for more formats and filters. Fill the recommended attributes that apply to the category; each one is a coverage opportunity.

Validate every change against the current product data specification, because exact limits and required-versus-recommended status change. State the concept to the user and point them to the specification page for the live values rather than asserting a stale character count.

## Disapprovals and the diagnostics view

- Work issues by scope. Account-level issues can suppress the entire catalog, so clear those first; then handle product-level disapprovals (the product cannot serve) and warnings (it serves but is at risk). The Needs attention and product views in Merchant Center group these for you.
- Read the issue, then fix the data. Most disapprovals map to a specific attribute or policy: missing or wrong GTIN, image too generic, price or availability mismatch with the landing page, or a policy violation. Fix the underlying product data or the site, not just the symptom.
- Separate policy disapprovals from data errors. Data errors (a malformed attribute, a broken link) are fixed in the feed; policy disapprovals (prohibited or restricted content, site requirements) require bringing the product or site into policy. Check the Shopping ads policies when the issue is policy, not formatting.
- Re-fetch and re-review after fixing. Changes take time to reprocess; confirm the product moves back to approved before judging campaign performance, since a campaign cannot perform on disapproved inventory.

## Product-level CPA and ROAS analysis

- Analyze where the data lives. Standard Shopping exposes product groups for product-level bids and reporting; Performance Max rolls reporting up but still lets you see listing-group and product performance and surfaces feed and listing-group problems when delivery stalls.
- Find the products that move the goal. Pull performance by product or product group and separate the winners (efficient CPA, high ROAS, real volume) from the drains (spend with weak conversion or value). Concentrate budget and bids on the winners.
- Reach for the feed lever first. For an underperformer, ask whether a feed change fixes it before a bid change: a stronger title to match better-converting queries, a better image to lift click-through, a corrected identifier to improve matching, a custom label to isolate it for bidding, or an exclusion to stop spend on a product that should not run.
- Bid on value, not just conversions. Report conversion values (revenue, and margin if you can) so Smart Bidding optimizes toward profit rather than raw orders. The value plumbing and Target ROAS mechanics live in `value-based-bidding` and `google-ads-bidding`.

## Shopping and Performance Max: how they interact

- Same feed, two ways to organize it. Standard Shopping organizes the catalog into product groups (subsets of inventory that share a bid, subdivided by attributes such as brand, category, condition, or custom label). Performance Max organizes the same Merchant Center products into listing groups by their attributes inside an asset group. Both read the same product data, so a feed improvement helps either.
- Know who serves for shared products. When the same products are eligible in both a Standard Shopping campaign and a Performance Max campaign, Performance Max generally takes precedence. Run both only when you have a deliberate reason (for example, a controlled Standard Shopping baseline alongside broad PMax reach) and you understand which one is actually serving each product.
- Campaign priority arbitrates within Standard Shopping only. Priority decides which Standard Shopping campaign bids for a product that appears in several of them; the higher-priority campaign bids even at a lower bid, and if it runs out of budget the lower-priority campaign bids. It is not a setting that controls Shopping versus Performance Max.
- Feed quality is the shared dependency. Both surfaces inherit the same disapprovals, titles, images, and identifiers, so feed work compounds. Fix the feed once and both Shopping and Performance Max benefit.

## Templates and examples

- New retailer, first feed: create and verify Merchant Center, claim the site, connect the ecommerce platform for automatic product data, confirm required attributes and valid GTINs, clear all account and product disapprovals in the diagnostics view, then launch Standard Shopping with product groups split by top categories and Target ROAS once value history exists (see `google-ads-bidding`).
- Feed you do not fully control: keep the platform export as the primary data source, add a supplemental data source that overrides weak titles (brand plus product type plus key attributes) and adds custom labels for margin tier, and use attribute rules to fix recurring formatting errors. Then bid by the custom-label product groups so high-margin products get more budget.
- Retailer running both surfaces: Performance Max with the feed as the primary reach engine (listing groups by category), plus a Standard Shopping campaign only if you want a controlled baseline, knowing PMax generally serves the shared products. Use Standard Shopping campaign priority solely to arbitrate among multiple Standard Shopping campaigns, never as a lever against PMax.
- Product-level cleanup: pull performance by product group, exclude or down-bid the spenders with no conversions, rewrite titles on the near-miss products to match better-converting queries, fix any image-too-generic disapprovals, and re-check approval before reading results.

## Common pitfalls

- Treating Shopping like Search and tuning bids while the feed is broken. In retail the feed is the campaign; a disapproval or a weak title outweighs any bid. Fix the data first.
- Burying the product type in the title behind marketing language. The title is the main matching signal; lead with what shoppers search, within the spec limit, and keep it consistent with the landing page.
- Fabricating or omitting GTINs. Invented identifiers and missing ones both cause disapprovals and worse matching. Submit a valid GTIN where one exists; set identifier-exists to false only for products that truly lack one.
- Rebuilding the entire feed for a small enrichment. Use a supplemental data source and attribute rules to enhance or fix data without re-engineering the source export.
- Chasing item issues while an account issue suppresses the catalog. Resolve account-level issues first, then product-level disapprovals.
- Generic or placeholder images. They are disapproved and they kill click-through. Use a clear principal product image that meets the specification.
- Running Standard Shopping and Performance Max on the same products without knowing PMax generally wins. You end up paying for and reporting on the surface you did not intend. Decide deliberately and verify which one serves.
- Misusing campaign priority. Priority only arbitrates among Standard Shopping campaigns; it does nothing for Shopping versus Performance Max.
- Hardcoding attribute requirements from memory. Required-versus-recommended status and exact limits change. Confirm against the current product data specification and cite it.

## Sources

- [Get started with Merchant Center](https://support.google.com/merchants/answer/188924) (as of June 2026)
- [How to upload your products to Merchant Center](https://support.google.com/merchants/answer/11586438) (as of June 2026)
- [Create a product data source](https://support.google.com/merchants/answer/14990942) (as of June 2026)
- [Product data specification](https://support.google.com/merchants/answer/7052112) (as of June 2026)
- [Title [title] and structured title [structured_title]](https://support.google.com/merchants/answer/6324415) (as of June 2026)
- [Image link [image_link]](https://support.google.com/merchants/answer/6324350) (as of June 2026)
- [GTIN [gtin]](https://support.google.com/merchants/answer/6324461) (as of June 2026)
- [How to fix: Missing or incorrect GTIN](https://support.google.com/merchants/answer/6098295) (as of June 2026)
- [Supplemental data source](https://support.google.com/merchants/answer/15624457) (as of June 2026)
- [Set up your attribute rules](https://support.google.com/merchants/answer/14994083) (as of June 2026)
- [Issues in Merchant Center](https://support.google.com/merchants/answer/2948694) (as of June 2026)
- [Shopping ads policies](https://support.google.com/merchants/answer/6149970) (as of June 2026)
- [About Shopping ads](https://support.google.com/google-ads/answer/2454022) (as of June 2026)
- [Manage a Shopping campaign with product groups](https://support.google.com/google-ads/answer/6275317) (as of June 2026)
- [Use campaign priority for Standard Shopping campaigns](https://support.google.com/google-ads/answer/6275296) (as of June 2026)
- [Manage a Performance Max campaign with listing groups](https://support.google.com/google-ads/answer/11596074) (as of June 2026)
