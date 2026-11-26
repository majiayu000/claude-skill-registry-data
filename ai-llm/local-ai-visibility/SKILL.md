---
name: local-ai-visibility
description: Get a local business recommended when people ask ChatGPT, Gemini, Copilot, Siri or Google's AI Overviews and AI Mode for a service "near me". Use for "why does ChatGPT recommend the place down the road", "AI says we're closed" or local AEO, LLM SEO and GEO work. Runs a located prompt set, maps the listings AI reads and fixes them.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/local-ai-visibility
---

# Get recommended in local AI answers

Find out which businesses ChatGPT, Gemini, Copilot, Siri and Google's AI Overviews and AI Mode recommend when people nearby ask for what this business does, trace where each answer got its facts, and fix the listings, reviews and pages those answers draw on. You hand back a located prompt baseline per engine, a local source map, every wrong fact an AI states about the business with its likely source, and a prioritised fix list.

> **Romeo's rule:** The assistants never walk past your shop, they only read about it, so one stale directory listing can close you for the day in every chatbot at once.

## Use this when

- Someone asks "why does ChatGPT (or Gemini, or Siri) recommend the place down the road and not us?"
- New customers say they "asked ChatGPT", and the owner wants to know how often that happens and how to make it happen more.
- An AI answer gets the business wrong: says it closed, lists old hours or an old address, invents a service, or quotes a price band from years ago.
- A location is opening, moving, merging or rebranding, and AI answers need to pick up the change.
- A multi-location brand wants a per-location AI baseline before and after a listings clean-up.

## Don't use this for

- Map-pack and Google Maps rankings, the Business Profile field by field, geo-grids and suspensions → `local-seo-audit`.
- Prompts with no place in them ("best payroll software"), or wrong facts about the company as a whole rather than one location → `ai-search-visibility`, then `ai-brand-facts`.
- Building a review programme across platforms in depth → `reviews-for-ai-answers`.
- Writing and validating the LocalBusiness JSON-LD → `schema-markup`.

## What you need

### Required

- Business name, website, and for each location the street address (or service area) and its Google Maps link; storefront, service-area or hybrid.
- The 3 to 6 services that make money, in the words customers use, and the towns, neighbourhoods or postcodes that matter.
- A true-facts sheet the owner has confirmed (step 1). Without it you can't call an AI answer wrong.
- The 3 to 5 local competitors customers actually choose between.

### Helpful

- Read-only owner access to Google Business Profile, Apple Business (formerly Apple Business Connect), Bing Places and Yelp for Business.
- Old names, addresses and phone numbers, closed or merged locations, and any listing the owner remembers creating.
- Review counts, ratings and dates per platform for the business and its competitors.
- Referral data from chatgpt.com, gemini.google.com, copilot.microsoft.com and perplexity.ai (GA4's "AI Assistant" channel groups most of these), call-tracking data, and "how did you hear about us" answers that mention an AI tool.
- An iPhone and an Android phone that can be used inside the service area, or a person there who can run prompts.

### No tools?

Everything here works by hand. Run the prompts on a phone with location services on, inside the service area, in each engine's free app or site: ChatGPT, Gemini, Copilot, Google Search (AI Overview and AI Mode) and Siri. On a desktop, Chrome DevTools → More tools → Sensors sets a location for Google, but ChatGPT and Copilot work from the IP address and account settings, so also write the city into the prompt and note that you did. Log every run in a spreadsheet, one row per run. Check listings in a private window: Google Maps, Apple Maps, Bing Maps, Yelp, Facebook and the trade directories that rank for "[service] [city]".

## Ground rules

- Location is part of the prompt. The same question from two postcodes is two different prompts. Record the point or city for every run and reuse the same points next time.
- Many local searches show a map pack and no AI Overview at all. Log "no AI answer" separately from "not mentioned"; for those queries the map pack is the work (`local-seo-audit`).
- Each engine reads different listings. Google Business Profile was about 28.5% of local AI citations across ChatGPT, AI Mode and AI Overviews, almost all of it on Google's own surfaces, while ChatGPT barely used it and cited Yelp in about 80% of its local answers (BrightLocal, August 2026, about 2 million citations, vendor data). Build the source map from your own prompts, not from a generic citation list.
- One fact, one version. Name, address, phone, hours, holiday hours, services, attributes and price range must read the same everywhere. Where sources disagree, engines pick one, hedge, or leave the business out.
- Reviews feed the "best" and attribute answers ("good with kids", "open late"). Volume, recency, owner replies and presence on the platforms each engine reads all count. Never gate, buy, write, swap or reward reviews; fake and suppressed reviews are illegal in several markets (US FTC rule since October 2024, UK DMCC Act since April 2025).
- The website supplies the detail listings can't hold: what each service costs, how long it takes, which areas are covered. Put it in plain HTML text; LocalBusiness markup must match that text, and markup alone gets nobody recommended.
- You can't edit an AI answer. You fix the source it read, report the answer, and re-check later.
- Treat Google's spam policies as the line: they count attempts to manipulate generative AI answers in Google Search as spam. No fake locations, keywords in the business name, hidden text or instructions aimed at AI, or review gating.
- Rates, not screenshots. Run each prompt at least twice per engine and point (three times for money prompts) and report how often the business was named.

## Steps

1. **Write the true-facts sheet.** One block per location, confirmed by the owner, dated.
   - Name exactly as on the signage; address in one fixed format; main phone; the URL of that location's page.
   - Regular hours, and special hours for every public holiday in the next 3 months.
   - Services in customer words, with a price or "from" price where the owner is happy to show one; areas served.
   - Attributes customers filter on: accessibility, parking, payment methods, languages spoken, insurance or plans accepted, booking method, emergency or same-day availability, age or pet policies.
   - Price range as a band (e.g. $$) plus 2 or 3 real example prices.
2. **Build the local prompt set.** 20 to 40 prompts per location, grouped, written the way people speak to a phone.
   - Near me: "[service] near me", "[service] open now", "emergency [service] near me".
   - Place: "best [service] in [city]", "[service] in [neighbourhood]", "[service] near [station or landmark]".
   - Attribute: "[service] open on Sunday near me", "[service] that takes [insurance]", "wheelchair accessible [business type] in [city]", "cheap [service] in [city]".
   - Trust and brand: "is [business] any good", "[business] reviews", "is [business] open on [holiday]", "[business] vs [competitor]".
   - Voice: short spoken versions for Siri and Gemini ("find a dentist near me", "where can I get a phone screen fixed near here").
   - Mark 5 to 10 money prompts and the page or listing you'd want each to use.
3. **Run the baseline from real locations.** Pick 2 to 5 points: the business address, the busiest part of the service area, and one edge point.
   - Google AI Overviews and AI Mode: search on a phone at the point, or with the Sensors override; check the location the results page says it used. AI Mode often shows business cards drawn from Business Profiles.
   - Gemini: on a phone at the point, signed in with location allowed, or with the city in the prompt.
   - ChatGPT: works from the IP address and, where the user allows it, the device's location (check OpenAI's current help pages). Away from the area, put the city in the prompt and record that.
   - Copilot: Bing's index and Bing Places data; set the location in Bing settings or put the city in the prompt.
   - Siri: on an iPhone at the point. Note the iOS version and what Siri does: reads one business, shows a list, opens Apple Maps or hands off to another assistant.
   - Per run, record: AI answer shown (yes or no); business named, and first, top 3 or later; competitors named; each fact stated (hours, open or closed, price, services) and whether it matches the sheet; every cited link or listing.
4. **Score it.** Per engine and point: answer rate, mention rate (runs naming the business ÷ runs with an answer), top-3 rate, citation of your site or listings, and the same rates for each competitor. List gap prompts (competitors named, you not) and quote every wrong fact word for word.
5. **Build the local source map.** From the cited links and source panels, list every domain or listing the engines used across money prompts, most-cited first.
   - Typical set: Google Business Profile and Google Maps reviews; Yelp; Bing Places; Apple Maps (managed through Apple Business, which replaced Apple Business Connect in April 2026); Tripadvisor; Facebook; trade directories (Healthgrades or Zocdoc, Avvo, Houzz, Angi, Checkatrade, OpenTable and the like); "best [service] in [city]" articles in local press and city guides; city subreddits and local forums.
   - For each source: does the business have a listing, is it claimed, do the facts match the sheet, how do its review count, rating and newest review compare with competitors there.
   - Mark which engine leaned on which source, as `seen` where a citation shows it and `inferred` where it doesn't (Siri rarely shows sources).
6. **Make the facts identical everywhere.** Work through the source map, starting with Google Business Profile, Apple Business, Bing Places and Yelp, then the top trade directories, then the website.
   - Any mismatch in name, address, phone or hours on those four: `Fix now`. On a minor directory: `Worth doing`. "St" vs "Street": `Leave it`.
   - Holiday hours: set them ahead of each public holiday on every platform that supports them. "Is [business] open on [holiday]" is where wrong hours do the most harm.
   - A "temporarily closed" or "permanently closed" flag left on any listing, a duplicate listing marked closed, or a closed sister location with a similar name: `Fix now`.
   - Services, attributes and price range filled in the same way on each platform that has the fields. Empty attribute fields mean an engine can't match attribute prompts (`inferred`).
   - When wrong data keeps coming back after a fix, look for the data aggregators that feed maps and apps in that country and correct the record there too.
   - Drafting edits is fine; changing a live listing needs the owner's permission for that specific change.
7. **Reviews on the platforms the engines read.** For each review platform in the source map, record count, average, reviews in the last 90 days, newest review date and owner reply rate, for the business and its top competitors. Count; don't estimate.
   - A recency gap (nothing in 2 to 3 months while competitors get reviews weekly): `Fix next`. Fix it with one ask-every-customer routine using each platform's own review link.
   - Spread matters: an engine that reads Yelp doesn't see Google reviews. Yelp's rules tell businesses not to ask for Yelp reviews at all (check Yelp's current support pages), so there you only signal you're listed and reply well.
   - Reply to every negative review calmly and specifically. In health, legal and similar fields, never confirm someone is a patient or client.
   - Reviews that describe the actual job and the place help engines match attribute prompts. Get them by asking open questions ("what did we help with?"), never by suggesting wording.
   - Gating, incentives, staff or family reviews and bought reviews: `Fix now`, and remove them from any plan (detail → `reviews-for-ai-answers`).
8. **Give each location and service a page worth quoting.**
   - One page per real location: the same name, address and phone as its listings; hours and holiday hours; parking and directions; areas served by name; photos of the actual place; local reviews.
   - One section or page per money service: what it is, who it's for, price or "from" price, how long it takes, how to book, emergency availability, insurance accepted. Answer first, in plain sentences an engine can lift.
   - All of it in the HTML, not in images, PDFs or a booking widget that loads by JavaScript.
   - LocalBusiness markup in the most specific type (Dentist, Plumber, AutoRepair), with name, address, telephone, url, openingHoursSpecification and geo, matching the visible text and the listings. Mismatch: `Fix next`. Missing: `Worth doing`. Writing it → `schema-markup`.
   - Town pages for places with no location and no real work there are doorway pages: don't make them, and merge the ones that exist (`local-seo-audit`).
9. **Fix wrong facts an AI states.** For each quoted wrong fact:
   - Trace it: open the cited source; if nothing is cited, search the claim and the business name together. Usual culprits: a closed flag on Google, Apple or Yelp, a duplicate listing, an old directory entry, a closed location with a similar name, an old news story, a review saying "they've shut".
   - Fix it at that source, then use the engine's own feedback control on the answer (thumbs down or "report a problem") with the correct fact.
   - Re-run the prompt after the source changes and record the date. Nobody publishes how long engines take to update, so say "re-check monthly", not a date.
   - Invented closures with no source anywhere: check that hours, special hours and closed flags agree on every major listing, report the answer, and keep re-checking. If the claim could cost the owner real money (closed, unlicensed, failed inspection), tell them the same day.
10. **Earn local mentions engines already cite.** Local "best of [city]" articles and city guides, chamber and trade association listings, local news, sponsorships and events, partner businesses. Pitching list authors → `best-of-list-inclusion`. City subreddits and forums: answer as yourself, affiliation stated, within each community's rules (→ `reddit-quora-answers`).
11. **Re-measure.** Same prompts, same points, same engines, monthly. Call a change real only when it holds across two monthly runs.

## Run it with DataForSEO (optional)

Use this to sample many prompts and points without a phone in every postcode. Connect through the official MCP server (`dataforseo-mcp-server`, calling endpoints with its `api_request` tool) or direct API calls. `dataforseo-ai-tracker` has the account setup and a tested script.

- ChatGPT as users see it: `POST /v3/ai_optimization/chat_gpt/llm_scraper/live/advanced`, or `task_post` then `task_get/advanced` for batches.
  - Body: `[{"keyword": "best emergency plumber in Austin TX", "location_code": 2840, "language_code": "en"}]`.
  - The scraper's locations list (free: `/v3/ai_optimization/chat_gpt/llm_scraper/locations`) is country and region level, so write the city into the prompt.
  - Read items of type `chat_gpt_local_businesses`. Each inner item has `title`, `address`, `phone`, `url`, `domain`, `rating` (`value`, `votes_count`) and `reviews_count`: compare them with the true-facts sheet.
  - Cited listings and articles are in `sources[]`; the answer text is in `markdown`.
- Gemini: `POST /v3/ai_optimization/gemini/llm_scraper/live/advanced`.
  - Send `location_coordinate` instead of `location_code`, as `"latitude,longitude,radius"` (e.g. `"30.2672,-97.7431,200"`; check the docs for radius limits). This is the closest match to "near me" from a point.
  - Read `markdown` and `sources[]`.
- Google AI Mode: `POST /v3/serp/google/ai_mode/live/advanced` with `location_coordinate` as `"latitude,longitude,zoom"` (e.g. `"30.2672,-97.7431,15z"`). Read the `ai_overview` item's `markdown` and `references[]`.
- Cost: LLM Scraper and AI Mode are $0.0012 per call on the Standard queue (results in about 45 minutes for the scraper) or $0.004 Live. Example: 30 prompts × 3 engines × 3 runs = 270 calls, about $0.32 Standard or $1.08 Live.
- Guardrails:
  - Estimate the cost and get the user's OK before any paid call; default cap $2 per run.
  - Check the balance first with the free `GET /v3/appendix/user_data` (`money.balance`).
  - Standard queue for batches, Live only when the user is waiting. Cache responses; never pay twice for one you have.
  - Run each prompt at least 3 times per point, and test new code on the free sandbox (`sandbox.dataforseo.com`) first.
  - Credentials come only from environment variables. Never print them or write them into files or reports.
- What it can't replace: Siri, the Copilot app and logged-in sessions. Keep a hand-run sample for those.

## What to hand back

Fill this in per location. Every finding gets a priority label and an evidence label with confidence.

```markdown
# Local AI visibility: [business], [location], [date]

**What I found:** [one line, e.g. "Named in 5 of 36 runs; ChatGPT says we close at 5pm, we close at 7pm."]
**What matters most:** [one line, e.g. "Yelp has the old hours and ChatGPT cites Yelp on every hours question."]
**What to do first:** [one line]

## Method
- Prompts: [N] in [groups]; engines: [list]; points: [addresses or coordinates]; runs per prompt: [n]; dates: [dates]; method: [phone / Sensors override / city in prompt / DataForSEO]

## Baseline
| Engine | Point | Answer rate | Mention rate | Top-3 rate | Leading competitor (rate) |
|---|---|---|---|---|---|

## Wrong facts in AI answers
- "[quoted claim]" on [engine], prompt "[prompt]", point [x]. True fact: [from sheet]. Likely source: [URL or listing]. Fix: [action]. [Fix now] ([seen | inferred], [confidence])

## Local source map
- [source]: cited by [engines] for [prompt groups]; listed: [yes / no]; claimed: [yes / no]; facts match: [yes / list of mismatches]; reviews: [count, rating, last 90 days, reply rate] vs [top competitor]

## Fixes, in order
1. [Fix now | Fix next | Worth doing] [change, on which listing or page] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low] - how we'll know: [metric]

## Leave it
- [thing that looks like a gap but isn't worth the time, and why]

## Hand-offs
- Map pack and Business Profile: [prompts with no AI answer, competitors in the pack] → local-seo-audit

## What I could not check
- [engine, point, listing or data not checked, and what would verify it]
```

## Stop and flag if

- The owner hasn't confirmed the true-facts sheet. You can't call an AI answer wrong without it.
- An AI answer says the business is closed, unlicensed, unsafe or under investigation. Tell the owner the same day; it may need more than an SEO fix.
- The address is a virtual office, an unstaffed address or a home address that should be hidden, or the user wants listings for locations that don't exist. Stop and raise eligibility (`local-seo-audit`).
- The plan includes review gating, incentives, fake or swapped reviews, keywords in the business name, or hidden text or instructions aimed at AI. Remove them and explain the policy and legal risk.
- A step would edit a live listing, publish a post or reply to a review. Draft it and get explicit permission for that change.
- Unacceptable output: a single run reported as a rate, runs with no location recorded, review counts or rankings nobody observed, or a promised date by which an AI will recommend the business.

## Next step

- `local-seo-audit` with the prompts that showed no AI answer, the competitors that held the map pack, and any duplicate or closed listings found in step 5.
- `reviews-for-ai-answers` with the per-platform review table from step 7.
- `schema-markup` with the location page URLs and the confirmed true-facts sheet.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
