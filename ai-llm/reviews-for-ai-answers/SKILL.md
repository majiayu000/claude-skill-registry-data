---
name: reviews-for-ai-answers
description: Build an honest review presence on the platforms AI engines check before recommending a business, such as G2, Capterra, Trustpilot, Yelp, Google, app stores and Amazon. Use for "get more reviews", "AI says customers complain about us" or the review side of an AEO, GEO or LLM SEO plan. Finds cited platforms, fixes profiles, sets up honest asks.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/reviews-for-ai-answers
---

# Reviews for AI answers

Find which review platforms AI engines actually cite when buyers ask about the brand's category, get the brand's profiles on those platforms complete and accurate, and set up a steady, honest flow of reviews from real customers that follows each platform's rules and the law. You hand back a per-engine map of cited review platforms, a profile fix list, a review-request programme with timing, links and wording, reply templates for negative reviews, buyer wording mined from reviews for prompts and pages, and a measurement plan.

> **Romeo's rule:** Ask every customer the same way at the same moment; once you choose who gets asked, your rating stops meaning anything.

## Use this when

- AI answers to "best [category]", "is [brand] legit" or "[brand] reviews" cite G2, Capterra, Trustpilot, app stores, Amazon or an industry review site, and the brand's profile there is missing, thin or old.
- An engine says "users complain about…" and the complaint was fixed long ago, or comes from a handful of old reviews.
- Competitors have hundreds of recent reviews on the cited platforms and the brand has a few dozen from two years ago.
- A profile shows the wrong category, old pricing, old screenshots or a dead product name.
- You want the words customers really use, to feed the prompt set and the pages that should be cited.

## Don't use this for

- Reddit, Quora and forum answers → `reddit-quora-answers`.
- Google Business Profile, map-pack reviews and local citations → `local-seo-audit`; "near me" answers in AI engines → `local-ai-visibility`.
- Third-party "best X" and comparison articles → `best-of-list-inclusion`.
- The prompt set, baseline and full citation-source map → `ai-search-visibility`.

## What you need

### Required

- Brand, category, country and language, and business model (B2B software, app, online shop, service).
- The user's own prompt runs with cited URLs: at least 10 buying prompts on the 2 or 3 engines the audience uses, 2 to 3 runs each. The platform list comes from these, never from a generic list. If they don't exist, run them first (`ai-search-visibility`).
- Admin access to existing profiles, or the name of whoever has it: G2 or Capterra vendor portals, Trustpilot Business, App Store Connect, Google Play Console, Amazon Seller or Vendor Central, Yelp for Business, industry sites.
- The customer journey: when customers first get real value (first successful job, delivery, project completion, renewal), and which channels can lawfully reach them.

### Helpful

- Review exports or a copy of recent reviews from each platform, for the brand and 2 or 3 competitors, including 1 to 3 star reviews.
- Support themes, churn reasons and sales-call notes, to compare with what reviewers say.
- Any current review incentives, review-collection vendors or "rate us" flows, so they can be checked against the rules.
- A legal or compliance contact for regulated sectors, and an AI visibility tracker export (optional; spot-check it by hand).

### No tools?

Run the prompts by hand in a private or logged-out window and open every cited link from a review site. Read each profile in the browser; copy the latest 50 reviews per platform (yours and two competitors') into a spreadsheet with date, rating and text. Most review platforms let a business claim its profile and reply to reviews free of charge (app stores and Amazon through the developer or seller account you already have); that is enough to run the whole skill.

## Ground rules

- Build the platform list from the user's own prompts, per engine. Citation shares by domain swing by tracker and month: Reddit's share of ChatGPT citations collapsed in September 2025 and again in August 2026. Last quarter's platform mix may already be wrong.
- Real reviews from real customers only. Never write, buy, swap or script reviews, or let staff and family post as customers. In the US the FTC's Consumer Reviews and Testimonials Rule (16 CFR Part 465, in force since 21 October 2024) bans fake reviews, buying reviews conditioned on their sentiment, undisclosed insider reviews and suppressing reviews through threats, with civil penalties. In the UK the DMCC Act 2024 made fake reviews and concealed incentivised reviews banned practices from 6 April 2025. Elsewhere, check local law.
- No review gating. Don't send happy customers to the review site and unhappy ones to support, or ask "love us? leave a review". FTC staff say gating can still breach the FTC Act, and Google, Trustpilot, G2 and Capterra prohibit it.
- Incentives depend on the platform. Google, Trustpilot and Yelp ban them; G2 and Capterra allow modest incentives offered to everyone, disclosed and never tied to the rating; app stores ban incentivised ratings. Where incentives are allowed, disclose them: in the US an undisclosed incentive can still breach the FTC Act. Check current rules before every campaign.
- Yelp is the exception: don't ask for Yelp reviews at all. Yelp filters solicited reviews out of the rating and says it can demote pages that show organised solicitation.
- Accuracy beats volume. Engines often lift profile text and review summaries (check the cited passages in your own runs), so a complete, current profile prevents wrong answers that no number of new reviews will fix.
- A steady flow beats a blast. Buyers read recency, platforms' fraud systems flag sudden spikes, and engines probably weigh fresh reviews more (`inferred`).
- Reply to negative reviews in public, factually and politely. Never threaten legal action over an honest review; that's review suppression under the FTC rule. Report only reviews that genuinely break the platform's rules.
- Don't copy third-party reviews into your own `Review` or `AggregateRating` markup. Google says not to aggregate ratings from other sites, and pages where the business controls its own reviews are ineligible for review stars (`LocalBusiness` and `Organization`).
- Measure per engine, as rates across repeated runs. One answer quoting one review proves nothing.

## Steps

1. **Map the review platforms each engine cites.** From the prompt runs, pull every cited URL from a review or rating site.
   - Include review-type prompts if the set lacks them: "[brand] reviews", "is [brand] worth it", "is [brand] legit", "what do people complain about with [brand]", "[brand] vs [competitor]", "most reliable [category]".
   - Per platform and engine: runs citing it ÷ runs, which prompts, and whether the cited page is the brand's profile, a competitor's, or a category page (G2's category grids, for example, are built largely from review data, so reviews move those too).
   - Typical candidates to look for, not to assume: B2B software → G2, Capterra, GetApp, Software Advice, TrustRadius, Gartner Peer Insights; consumer brands and shops → Trustpilot, Amazon, Sitejabber; apps → App Store, Google Play; agencies → Clutch; local and hospitality → Google, Yelp, Tripadvisor (route to `local-seo-audit`); plus the trade's own sites (Houzz, Healthgrades, Avvo and similar).
   - Mark platforms cited on 2+ engines or for 3+ money prompts as priority. A platform no engine cites for these prompts is `Leave it` for AI purposes, whatever its reputation.
2. **Audit each priority profile.** Claimed, and by whom? Then check:
   - Exact brand and product name as on the site; correct category (a wrong category puts you in the wrong comparisons); description matching the site's one-line description; pricing and plan names with the date they were true; current screenshots and video; website link; integrations and platforms; contact details.
   - App stores: subtitle and description, screenshots, "What's New" notes, developer website. Amazon: title, bullets, images, brand store details.
   - Rating, total reviews, reviews in the last 90 days, newest review date, reply rate, and the 3 most repeated complaints.
   - Any profile fact that AI answers repeat wrongly is `Fix now`. Request a category change through the platform's vendor support if needed.
   - No profile on a priority platform: claim or create the free listing before asking anyone for a review (`Fix next`).
3. **Benchmark against competitors.** For each priority platform: competitors' rating, total reviews, last-90-day reviews and reply rate. Chase recency and coverage of your real segments, not their lifetime total.
4. **Design the review-request programme.**
   - Who: every customer who reached the value moment, by a rule that ignores satisfaction. Exclusions only on neutral grounds (staff, partners, accounts younger than a set number of days), written down.
   - When: one trigger for everyone, just after value. Software: after the first successful outcome or at a fixed day after activation; shops: a set number of days after delivery; apps: after a completed task, never at launch; services: at project completion.
   - Where: one platform per ask, the one most cited for your prompts; rotate cohorts if two matter. Send the direct review link: the platform's review-collection link (G2, Capterra, Trustpilot invitations), the Google review link from the profile, the StoreKit review prompt on iOS, Google Play's In-App Review API, Amazon's "Request a Review" button.
   - Wording: neutral and short. "How has [product] worked for you? An honest review on [platform] helps other [buyers], good or bad." Never mention stars, suggest content or offer anything the platform bans.
   - Platform rules to apply, as checked in late 2026 (re-check each one before launch):
     - Google: no incentives, no gating, no staff review quotas, no asking for specific content, no pressure on premises.
     - Trustpilot: no incentives; invite every customer the same way at the same point in the journey, with non-leading wording.
     - Yelp: don't ask at all.
     - G2: incentives allowed within G2's cap, disclosed to G2 and never tied to sentiment; G2 labels incentivised reviews and bans segmenting out likely negative reviewers.
     - Capterra, GetApp and Software Advice: incentives offered equally regardless of rating, a broad cross-section of users, no coaching, collection on their own site.
     - Amazon: the "Request a Review" button (once per order) or neutral messages; never ask for positive reviews or for negative ones to be removed; no incentives outside Amazon Vine.
     - App Store: Apple's review API only; custom review prompts are disallowed and the system shows the prompt at most three times a year per user. Google Play: the In-App Review API, with no "Do you like the app?" question before it; no incentivised ratings.
   - Consent: email only customers you may lawfully contact, under the sender's local rules.
5. **Reply to reviews, negative ones first.** Aim for every review within a few working days.
   - Thank them, name the specific issue, state the fix or the current fact without arguing ("two-way sync shipped in March 2026"), and offer a named contact. No personal or account details in public.
   - Never offer anything for changing or removing a review. If the issue is fixed, say so in the reply; the reviewer may update it on their own.
   - Fake, competitor or off-topic reviews: use the platform's report process with evidence. Don't accuse reviewers publicly.
   - Replies are public text engines may read (`inferred`), so state dated, current facts, not slogans.
6. **Mine reviews for buyer wording.** Export 100 to 300 recent reviews for the brand and 2 or 3 competitors, including 1 to 3 star ones.
   - Tag: the job they hired the product for, their segment, the trigger that made them look, alternatives they tried, outcome phrases, complaints and reasons for switching.
   - Turn it into: new prompts in buyers' own words (→ `ai-prompt-research`), answers and "who it's for" lines for pages (→ `ai-citable-pages`), honest comparison criteria (→ `comparison-page-writer`), and product feedback for the user.
   - Quote reviews on your own site only with attribution and within each platform's content-use terms (Capterra's guidelines, for example, ask for attribution and reviews under 12 months old). Paraphrase in analysis; never name private reviewers in deliverables.
7. **Check what engines say about the reviews.** Run the review-type prompts and compare every claim ("users say support is slow") with the last 12 months of reviews.
   - Outdated complaint: reply on the old reviews with the fix and date, update the profile, publish a dated changelog entry, and trace the source → `ai-brand-facts`.
   - Accurate complaint: that's product or service work. Say so plainly; reviews will follow the fix, not the other way round.
8. **Measure per engine.** Monthly: per platform, total reviews, last-90-day reviews, rating, reply rate. Per engine, with 2 to 3 runs per prompt: which review platforms are cited, whether the brand's profile is among them, mention rate on review-type prompts, and how the brand is described (quote it). Re-derive the platform map at least quarterly, because citation shares move. Call a change real only when it holds across two monthly runs.

## Run it with DataForSEO (optional)

Replaces manual review copying in steps 2, 3 and 6, and adds a web-wide view of brand mentions. Connect through the official MCP server (`dataforseo-mcp-server`, calling endpoints through its `api_request` tool) or plain HTTPS with Basic auth.

- **Google reviews:** `/v3/business_data/google/reviews/task_post` (Standard queue only), then `tasks_ready` and `task_get/$id`.
  - Send `keyword` (the business name) or `cid` / `place_id`, plus `location_code`, `language_code`, `depth` (multiples of 10, max 4,490) and `sort_by` (`newest`, `lowest_rating`, `highest_rating` or `relevant`).
  - Read `rating.value`, `rating.votes_count`, `reviews_count`, and per item `review_text`, `rating.value`, `timestamp` and `owner_answer` (shows your reply rate).
- **Trustpilot reviews:** `/v3/business_data/trustpilot/reviews/task_post` with `domain`, `depth` (billed per 20 reviews) and `sort_by` (`recency` or `relevance`).
- **App reviews:** `/v3/app_data/apple/app_reviews/task_post` (`app_id`, `depth` in multiples of 25, max 500, `sort_by: "most_recent"`) and `/v3/app_data/google/app_reviews/task_post`.
- **Brand mentions and sentiment across the web:** `/v3/content_analysis/search/live`.
  - Send `keyword` set to the brand in escaped double quotes for an exact match, optional `page_type` (for example `["blogs", "message-boards"]`), and `limit: 100`.
  - Read `url`, `domain`, `content_info.snippet`, `content_info.connotation_types` and `content_info.date_published`.
  - `/v3/content_analysis/sentiment_analysis/live` and `/v3/content_analysis/summary/live` give the positive, negative and neutral split and the totals.
- **Example cost:** 300 Google reviews each for the brand and 2 competitors = 90 blocks of 10 at about $0.00075 per 10 on the Standard queue (published price) ≈ $0.07 plus task fees; 3 Content Analysis calls ≈ $0.06 to $0.10. Well under $1; confirm current prices with `user_data`.
- **Guardrails:**
  - Estimate the cost and get the user's OK before any paid call; default cap $2 per run.
  - Check `money.balance` with the free `GET /v3/appendix/user_data` first.
  - Always set `depth` or `limit`; use the Standard queue for batches; cache results for 30 days.
  - Test new code on `https://sandbox.dataforseo.com/v3/` first. Never print or save the API password.
  - Reviewer names and profile links are personal data: keep exports internal and report themes, not people.

## What to hand back

Fill in this template. Every action gets a priority label and an evidence label with confidence.

```markdown
# Reviews for AI answers: [brand], [date]

**What I found:** [one line, e.g. "ChatGPT and Perplexity cite G2 and Capterra for 9 of 12 money prompts; we have 14 G2 reviews, newest from 2024."]
**What matters most:** [one line]
**What to do first:** [one line]

## Method
- Prompts: [N] ([groups]); engines: [list]; runs per prompt: [n]; dates: [x]; country/language: [x]

## Review platforms cited, per engine
| Platform | Engines citing it (rate) | Prompts | Our profile cited? | Our rating / reviews / last 90 days | Leading competitor |
|---|---|---|---|---|---|

## Profile fixes
1. [Fix now | Fix next | Worth doing] [platform]: [what's wrong] → [fix] - evidence: [seen | tool | inferred], [high | medium | low]

## Review-request programme
- Who: [rule]; when: [trigger]; where: [platform + link type]; wording: "[text]"
- Platform rules checked on [date]: [list]; legal notes: [FTC / DMCC / local]

## Replies
- Negative reviews needing a reply: [count, links]; template: [text]
- Reviews to report (rule broken, evidence): [links]

## Buyer wording from reviews
- New prompts: [list]; page changes: [list]; recurring complaints: [list]

## What AI says about our reviews
- "[quoted claim]" on [engine]; reality in last 12 months: [summary]; action: [action]

## Leave it
- [platform or task, and why it isn't worth the time]

## Re-measure plan
- Next run [date]; success = [metric change]

## What I could not check
- [platform, engine or data not checked, and what would verify it]
```

## Stop and flag if

- The user wants to write or buy reviews, use staff, friends or agencies to post them, gate requests by satisfaction, offer incentives where the platform bans them, or pressure people to remove negative reviews.
- A platform shows a warning, consumer alert or suspension on the brand's profile. Stop all review requests until the cause is understood.
- The business is in healthcare, finance, legal or another regulated field. Replies must never confirm that someone is a patient or client; get compliance sign-off on templates.
- A review alleges something serious (safety, fraud, discrimination). Escalate to the user; don't reply from a template.
- Fewer than 10 prompts or one run each: present the platform map as provisional.
- Unacceptable output: invented ratings, review counts or quotes, request wording that mentions stars or rewards, or customer emails sent without the user's approval.

## Next step

- Run `ai-citable-pages` with the buyer wording and recurring questions mined from reviews.
- Run `ai-brand-facts` with every outdated claim engines repeat about the brand's reviews.
- Re-run `ai-search-visibility` monthly with the same prompt set to measure the change.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
