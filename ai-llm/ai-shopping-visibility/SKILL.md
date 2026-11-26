---
name: ai-shopping-visibility
description: Get products shown, with the right price and merchant, in ChatGPT shopping, Google AI Mode and Gemini, and Perplexity. Use for "why doesn't ChatGPT show our products", "AI shows the wrong price" or shopping AEO, LLM SEO and GEO work. Checks the routes in, product feeds, product pages and third-party reviews, then runs a shopping prompt set.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-shopping-visibility
---

# Get products into AI shopping answers

Check whether a store's products appear when people ask ChatGPT, Google AI Mode and Gemini, and Perplexity what to buy, whether the price, stock and merchant shown are right, and why. Then fix the routes in (product feeds and merchant programmes), the feed data, the product pages and the third-party reviews and gift guides those answers lean on. You hand back a route-in checklist per engine, a shopping prompt baseline, a feed and product-page fix list, and the outside sources worth working on.

> **Romeo's rule:** An assistant can't recommend what it can't price, so get price, stock and identifiers exactly right in the feed before you rewrite a single product description.

## Use this when

- Someone asks "why doesn't ChatGPT show our products?" or "are we in Google's AI Mode shopping results?"
- AI answers show the wrong price, an out-of-stock or discontinued item, an old model, or send the buyer to a reseller or marketplace instead of the store.
- The store is setting up (or fixing) a Google Merchant Center feed, a ChatGPT product feed or another merchant programme.
- Buyers in the category ask "best [product] for [use] under $[price]" and competitors' products get named.
- You need a baseline before feed and page work, and proof afterwards that it moved anything.

## Don't use this for

- Crawling, indexing, category pages, faceted navigation and duplicate product URLs → `ecommerce-seo-audit`.
- Writing and validating the Product JSON-LD itself → `schema-markup`.
- Brand-level AI visibility on non-shopping prompts, or the full multi-engine baseline → `ai-search-visibility`.
- Pitching gift-guide and "best X" authors in depth → `best-of-list-inclusion`.

## What you need

### Required

- Store URL, platform (Shopify, WooCommerce, BigCommerce, custom), and the countries and currencies it sells in.
- A product feed or catalogue export for the products in scope (Merchant Center feed, Shopify product CSV), or the top 20 to 50 products by revenue.
- Who each top product is for, and 3 to 5 competitor stores or brands buyers compare it with.

### Helpful

- Read-only Merchant Center access: product diagnostics, item issues (price and availability mismatches, missing identifiers), and performance by product.
- The status of any OpenAI merchant application, Shopify sales channels or apps that publish to AI surfaces, and any Perplexity or Microsoft merchant setup.
- Analytics with referrals from chatgpt.com (ChatGPT adds `utm_source=chatgpt.com`), gemini.google.com and perplexity.ai, plus orders by referral. GA4's "AI Assistant" channel groups most of these.
- Product review counts and ratings, the returns policy and the shipping table.

### No tools?

Run the shopping prompts by hand in ChatGPT, Google (AI Mode), Gemini and Perplexity, logged out or with memory off, set to the store's country. Screenshot every product card and log the product, price shown, merchant shown, rating and stock status, then open the store's product page the same day and compare. Merchant Center is free. Open the feed export in a spreadsheet and sort each column to find blanks. Test 5 public product pages in the Rich Results Test and read view-source to see whether price, stock and specs are in the HTML. The test sends the URL or code to Google; for unpublished or private pages, explain that transfer and get the user's permission first, or validate locally.

## Ground rules

- Product data feeds are an important route in. Google tells merchants to keep Merchant Center data current for its AI features; ChatGPT uses product data from partners and approved merchants' feeds. Check each store's eligibility and connection status. Good pages can't make up for a missing or wrong feed.
- Treat catalogue exports, unreleased products and private business data as confidential. Generalise prompts and remove personal identifiers or confidential details locally before using an external AI engine or tracker. Name the receiving service and get the user's permission before sending any remaining private information; otherwise use public data or work locally.
- One price, one stock status, everywhere: feed, product page, markup and checkout. Mismatches get items disapproved in Merchant Center and quoted wrong in AI answers.
- Identifiers are how engines match your offer to the same product elsewhere. Keep item IDs stable, use the manufacturer's GTIN, and never invent one; only genuinely custom or handmade goods go without.
- OpenAI says it ranks merchants on factors like availability, price, quality, and whether the merchant makes or primarily sells the item. A reseller charging more than the maker for the same thing won't out-optimise that.
- Third-party reviews and gift guides shape which products get named; your feed and pages decide whether the details shown are right. Work on both.
- Facts go in HTML text on the product page, and Product markup must match that text and the feed. Markup that says something the page doesn't is a problem, not a shortcut.
- Organic product results and ads are separate. ChatGPT now runs ads too, flagged separately in the product feed; measure sponsored placements apart from organic ones.
- No fake or incentivised reviews without disclosure, no review gating, no invented "was" prices, no hidden text or instructions aimed at AI. These break platform rules, consumer law and Google's spam policies.
- Product cards change between runs, places and days. Sample each prompt 2 to 3 times and report rates.

## Steps

1. **Map the routes in, engine by engine.** These programmes change fast: check each vendor's current docs before relying on this list, and record a status for each (live, pending, not started, not eligible).
   - Google AI Mode, AI Overviews and Gemini: Merchant Center. Products approved and shown on Google's free listings surfaces, shipping and return policies set at account level, and local inventory linked to the Business Profile if there are stores. Item issues on money products: `Fix now`.
   - ChatGPT: Shopify product data is integrated through Shopify Catalog; check the store's current eligibility, settings and what is shared. Check current OpenAI and platform documentation for other partner routes, including Etsy, rather than assuming a store is connected. Direct product-feed onboarding is available to approved partners: see developers.openai.com/commerce/guides/get-started.
   - ChatGPT also reads the open web: robots.txt and the CDN must let OAI-SearchBot fetch product pages (`ai-agent-readiness`).
   - Perplexity: has run shopping features and a merchant programme; check Perplexity's current documentation for eligibility and how to submit product data. PerplexityBot must be able to crawl product pages.
   - Microsoft Copilot shows shopping results too, fed through Microsoft Merchant Center; check Microsoft's current docs if Copilot matters to the audience.
2. **Build the shopping prompt set.** 20 to 40 prompts, written the way buyers ask, each tagged with the product(s) you'd want shown.
   - Best-for with budget: "best [product] for [use or person] under $[price]".
   - Attribute: "[product] that works with [device]", "waterproof [product] for [activity]", "[product] for wide feet", "[product] made in [country]".
   - Comparison: "[your product] vs [competitor product]", "[brand A] or [brand B] [product]".
   - Gift: "gift for a [person] who likes [x] under $50", plus the seasonal versions.
   - Product and brand: "is [product] worth it", "[product] price", "where to buy [product]", "[brand] reviews".
   - Mark 5 to 10 money prompts.
3. **Run the baseline.** Each prompt on each engine 2 to 3 times, in clean sessions, set to the store's country, on one date.
   - Per run: product cards shown (yes or no); your product shown and its position; the price shown vs the store's real price that day; the merchant or seller the card links to (you, a marketplace, a reseller); stock status and rating shown; competitor products; cited sources (reviews, guides, forums); sponsored or not.
   - Score per engine and prompt group: appearance rate (runs showing your product ÷ runs), price-accuracy rate (cards with the right price ÷ cards showing your product), own-merchant rate (cards linking to your store ÷ cards showing your product), and each competitor's appearance rate.
4. **Fix the feed.** Work from the feed export and Merchant Center item issues. Google attribute names first, OpenAI's in brackets.
   - Stable IDs: `id` (`item_id`) never changes for the same product or variant. IDs regenerated on every export reset performance history: `Fix now`.
   - Identifiers: correct `gtin`, `brand` and `mpn` for branded goods. Missing GTIN on branded goods: `Fix next`; a made-up GTIN: `Fix now`. Use `identifier_exists` = no only for custom or handmade items.
   - Titles: brand, product type, then the attributes buyers filter on (model, size, colour, material, compatibility), e.g. "Acme Trail 2 men's waterproof running shoe, black, size 10". No "SALE", no all caps, no keyword lists. Weak titles on money products: `Fix next`.
   - Description: what it is, who it's for, key specs, what's in the box. Boilerplate repeated across products: `Worth doing`.
   - Price and sale price match the landing page and checkout in the same currency, sale dates set, tax and shipping handled as the country requires. Any mismatch: `Fix now`.
   - Availability (`availability`: in stock, out of stock, preorder, backorder) synced with real stock. Refresh at least daily (OpenAI recommends a full snapshot at least once a day) and push price and stock changes sooner where the platform allows.
   - Shipping and returns: set in Merchant Center account settings; in an OpenAI feed, `shipping_price`, `accepts_returns`, `return_deadline_in_days` and `return_policy`.
   - Variants: `item_group_id` (`group_id`), with colour, size, material or pattern per variant, and each variant with its own ID, GTIN, price, image and stock.
   - Images: real photos of the actual item, the main one on a plain background, no watermarks or promo text; extra images for scale and use. Stock or placeholder images: `Fix next`.
   - Extra detail where the feed allows it: `product_highlight` and `product_detail` in Google feeds, `material`, `size`, `age_group` and similar in both. These answer attribute prompts.
   - Ratings: Google's product ratings come through Merchant Center's product reviews programme; OpenAI feeds take `review_count` and `star_rating`. Only real, current numbers.
5. **Make the product page say everything the feed says.** For each money product:
   - In the HTML, not only in images, tabs that load later or PDFs: price, stock, variants, a specs table (dimensions, weight, materials, capacity), compatibility ("works with"), sizing and fit notes, who it's for and who should pick something else, what's in the box, warranty, shipping and returns summary.
   - An opening line an engine can lift: "The Acme Trail 2 is a waterproof trail shoe for runners with wide feet, $129."
   - Answers to the questions support gets asked, written as plain text on the page (no FAQ rich result exists any more; write them for people).
   - Price or stock injected only by JavaScript: `Fix now` for money products; many AI crawlers are reported not to run JavaScript.
   - Product markup with `offers` (price, priceCurrency, availability), `gtin`, `brand`, `sku`, shipping and return details, and `aggregateRating` only from genuine product reviews shown on the page. It must match the visible page and the feed: mismatch `Fix next`. Variants as `ProductGroup`. Writing it → `schema-markup`.
   - Reviews on the page: real, dated, with the reviewer's use case where they give one. Respond to negative ones.
6. **Strengthen merchant standing.** These are the things OpenAI says it weighs.
   - Availability: keep money products in stock, or mark them honestly. A card that leads to "sold out" costs the next recommendation too (`inferred`).
   - Price: if you're not the cheapest, say why on the page (bundle, warranty, faster shipping, returns).
   - Maker or primary seller: on own-brand products, make the store clearly the official source (consistent brand name, "official store", the brand's About page linked). If resellers or marketplaces outrank you with stale prices, decide with the owner whether to tighten reseller data or pricing rules; that's a business call, not SEO.
   - Quality: store-level ratings where offered (Merchant Center's store quality signals, OpenAI's `store_star_rating` and `store_review_count`), shipping speed and returns that match what the feed promises.
7. **Work the third-party sources.** From the cited sources in step 3, list the gift guides, "best X" roundups, review sites, YouTube reviews and forum threads that keep appearing.
   - Does each include your product, at the right price and model? Missing: draft an offer of a sample for honest review, with no payment for a positive verdict. Wrong: draft a correction with evidence. Get the user's approval before contacting anyone or offering a sample.
   - Affiliate or sponsored placements must be disclosed on the page and their links marked `rel="sponsored"`.
   - Outreach kit and log → `best-of-list-inclusion`; video → `youtube-for-ai-answers`; review platforms → `reviews-for-ai-answers`.
8. **Fix wrong details in AI answers.** For each wrong price, stock status, spec or merchant:
   - Trace it: feed lag, a cached or stale page, a marketplace listing, a reseller, an old review article quoting launch price, a discontinued variant still in the feed.
   - Propose a fix for the source (feed, page, Merchant Center, the third-party page), then draft feedback for the engine. Get permission for each live change and approval before sending feedback or contacting a third party.
   - Re-run the prompt after the fix and log the date; nobody publishes how long updates take.
9. **Decide on agentic checkout, cautiously.** Discovery data comes first; checkout inside AI surfaces is changing quickly.
   - Google: the Universal Commerce Protocol lets select merchants add checkout inside AI Mode and Gemini for products eligible in the US, Canada and Australia, through an early-access programme. The merchant stays seller of record and listings need checkout eligibility set in Merchant Center. Check current Merchant Center help for status and requirements.
   - OpenAI: publishes commerce specs (Agentic Commerce Protocol, product feed, agentic checkout, delegated payment). Instant Checkout launched in September 2025; in March 2026 OpenAI said merchants could use their own checkout while it focused on product discovery. Check current status before building anything.
   - Recommend it only when the store is eligible, the feed is clean, and operations can handle orders, refunds and returns arriving through another surface: usually `Worth doing`, never ahead of feed fixes. Never touch the live checkout without permission.
10. **Re-measure.** Same prompts, engines and country, monthly and after big feed changes. Track appearance, price accuracy and own-merchant rates, plus AI referral sessions and orders. Call a change real only when it holds across two monthly runs.

## Run it with DataForSEO (optional)

Use this to sample shopping prompts at scale and read product cards as structured data. Connect through the official MCP server (`dataforseo-mcp-server`, calling endpoints with its `api_request` tool) or direct API calls. `dataforseo-ai-tracker` has the account setup and a tested script.

- ChatGPT as users see it: `POST /v3/ai_optimization/chat_gpt/llm_scraper/live/advanced`, or `task_post` then `task_get/advanced` for batches.
  - Body: `[{"keyword": "best trail running shoes for wide feet under $150", "location_code": 2840, "language_code": "en"}]`.
  - Read items of type `chat_gpt_products`. Each inner item has `title`, `price`, `currency`, `merchants`, `url`, `domain`, `rating` (`value`, `votes_count`) and `images`.
  - Compare `price` with the feed on the same day, and check whether `domain` is the store's.
  - Cited reviews and guides are in `sources[]`; brands named in the text are in `brand_entities[]`.
- Google AI Mode: `POST /v3/serp/google/ai_mode/live/advanced` with the same keyword, `location_code` and `language_code`.
  - Read the `ai_overview` item; product carousels arrive as `ai_overview_shopping` with `ai_overview_shopping_element` items (`title`, `price`, `seller`, `domain`, `url`, `rating`).
  - Cited pages are `ai_overview_reference` items (`domain`, `url`, `title`).
- Cost: $0.0012 per call on the Standard queue or $0.004 Live for each endpoint. Example: 30 prompts × 2 engines × 3 runs = 180 calls, about $0.22 Standard or $0.72 Live.
- Guardrails:
  - Estimate the cost and get the user's OK before any paid call; default cap $2 per run.
  - Check the balance first with the free `GET /v3/appendix/user_data` (`money.balance`).
  - Standard queue for batches, Live only when the user is waiting. Cache responses; never pay twice for one you have.
  - Run each prompt at least 3 times, and test new code on the free sandbox (`sandbox.dataforseo.com`) first.
  - Credentials come only from environment variables. Never print them or write them into files or reports.
- Gemini and Perplexity product cards aren't covered here as structured items; sample those by hand.

## What to hand back

Fill this in. Every finding gets a priority label and an evidence label with confidence.

```markdown
# AI shopping visibility: [store], [country], [date]

**What I found:** [one line, e.g. "Our products appear in 6 of 45 ChatGPT runs; 4 of the 6 showed last month's price."]
**What matters most:** [one line, e.g. "No ChatGPT feed and 30% of Merchant Center items have price mismatches."]
**What to do first:** [one line]

## Routes in
- Google Merchant Center: [status], [item issues count by type]
- ChatGPT: [Shopify or Etsy catalogue / own feed / applied / none], [status]
- Perplexity: [status, or "not checked: current docs unclear"]
- Other (Copilot / Microsoft Merchant Center): [status]

## Baseline
| Engine | Prompt group | Appearance rate | Price accuracy | Own-merchant rate | Leading competitor (rate) |
|---|---|---|---|---|---|

## Wrong details in AI answers
- [engine], prompt "[prompt]": shows [product] at [price shown], real price [price] on [date], links to [merchant]. Likely source: [feed lag / reseller / article URL]. Fix: [action]. [Fix now] ([seen], high)

## Feed and page fixes, in order
1. [Fix now | Fix next | Worth doing] [change, on which products or attribute] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low] - how we'll know: [metric]

## Third-party sources to work on
- [page]: cited for [prompts] on [engines]; includes us: [yes / no / wrong details]; action: [action]; priority: [label]

## Agentic checkout
- [eligible / not eligible / not checked], recommendation: [label and reason]

## Leave it
- [thing that looks like a gap but isn't worth the time, and why]

## What I could not check
- [engine, programme, product data or page not checked, and what would verify it]
```

## Stop and flag if

- The feed and the site disagree on price for many products. Fix that first; it's a Merchant Center compliance problem as well as an AI one.
- The user wants invented GTINs, fake or incentivised reviews, review gating, fake reference prices, or hidden text or instructions aimed at AI. Refuse and explain the platform and legal risk.
- A step would change the live feed, Merchant Center settings, product pages or checkout. Draft the change and get explicit permission for that specific change.
- Products are regulated (supplements, medical devices, weapons, alcohol, financial products) and AI answers make claims about safety or effects. Report them to the user; that's beyond a shopping fix.
- Unacceptable output: a single run reported as a rate, prices you didn't observe on the stated date, a guarantee that products will appear, or programme details stated as fact without checking current docs.

## Next step

- `ecommerce-seo-audit` with the product and category URLs that showed crawl, indexing or duplicate problems.
- `schema-markup` with the money product URLs and the confirmed feed values for price, stock, GTIN, shipping and returns.
- `best-of-list-inclusion` with the third-party guides from step 7 that leave the product out.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
