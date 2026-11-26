---
name: google-ai-overviews-audit
description: Find out what Google AI Overviews and AI Mode are doing to your clicks and conversions, page by page. Use for "are AI Overviews killing our traffic", "are we cited in AI Overviews" or "should we opt out of AI Mode". The Google side of AEO and GEO, built on Search Console's generative AI report.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/google-ai-overviews-audit
---

# Google AI Overviews and AI Mode audit

Work out what Google's AI Overviews and AI Mode are doing to a site's search traffic, page by page, and what to do about each page. You hand back a page list built from 16 months of Search Console Performance data joined to the generative AI report, spot-checked citations for the top queries on both surfaces, an eligibility check, a class and a priority for every page that matters (cited and fine, shown but not cited, commodity content losing clicks, unaffected), realistic expectations from dated studies, and a reasoned call on whether to opt out of anything.

> **Romeo's rule:** A page that lost half its clicks and none of its signups has a reporting problem, not a business problem.

## Use this when

- Clicks fell on informational pages while impressions held or rose, and someone blames AI Overviews.
- Search Console's generative AI report shows AI Overview or AI Mode impressions and you want to know what they're worth.
- The team is debating whether to opt out of, block or "optimise for" Google's AI features.
- A key page ranks on page one, but competitors are the ones cited in the AI Overview.
- You need a Google-specific before/after baseline for AEO work.

## Don't use this for

- Visibility across ChatGPT, Perplexity, Copilot, Claude and Gemini, or a cross-engine prompt baseline → `ai-search-visibility`.
- Rewriting the pages this audit flags: passages that can be quoted → `ai-citable-pages`; sub-questions the AI fans out to → `query-fan-out-coverage`.
- A traffic drop where the affected queries show no AI feature at all → `seo-performance-audit`.
- Ongoing measurement of AI referrals and conversions from every engine → `ai-traffic-analytics`.

## What you need

### Required
- Search Console access, or these exports: Performance (Search results, search type Web) by page and by month for the full 16 months, plus queries for each key page; and the Generative AI performance report by page and date, Search view and (if the site gets Discover traffic) Discover view.
- The 10 to 50 pages that matter commercially, and what counts as a conversion on each (signup, lead, sale, booking).
- Target country and language.

### Helpful
- Search Console API access or a Looker Studio connection, because UI exports stop at 1,000 rows per table.
- GA4 or another analytics tool with key events, filtered to Organic Search by landing page, for the same 16 months.
- URL Inspection results and a crawl showing meta robots, `X-Robots-Tag`, `data-nosnippet` and structured data per template.
- A rank tracker or SERP export that records AI Overview presence and cited URLs (spot-check it by hand).
- Dates of migrations, redesigns, content pruning and Google core updates inside the window.

### No tools?
Use the Search Console UI. Performance → Search results → date range "last 16 months", then compare the last 3 months with the same 3 months a year earlier and export the Pages tab; filter by each key page and export its Queries tab. Open the Generative AI performance report under Performance and export the Pages tab for the same months. Put both in one spreadsheet keyed on URL. Spot-check queries in a private, logged-out window set to the target country, recording AI Overviews and AI Mode separately. That covers 20 to 30 pages properly.

## Ground rules

- The generative AI report counts impressions only: no clicks, CTR, position or queries. Clicks from AI Overviews and AI Mode sit inside normal Web data in Search Console and inside Organic Search in GA4, and can't be separated out. Any "AI Overviews cost us X clicks" figure is `inferred`; label it.
- AI feature impressions are part of Web impressions too. A page that starts appearing in AI Overviews gains impressions without gaining clicks, so its CTR falls even when clicks don't. Read clicks first, CTR second.
- An AI Overview occupies one position and every link in it gets that position (Search Console help). A page "jumping to position 2" may just have started being cited.
- AI Overviews and AI Mode are separate surfaces. Ahrefs (Dec 2025, vendor data) found ~86% similar answers but only ~13.7% of citations shared. Check and report each separately.
- Google's stated requirements are short: indexed, eligible for a snippet, and the site included in Search generative AI features. No schema, file or markup makes a page eligible; treat anyone selling one with suspicion.
- Answers change by run, day, location and account. A screenshot proves the feature exists for a query, not that you're always or never cited.
- Seasonality, core updates and ranking losses move clicks too. Compare year over year and against pages with no AI impressions before blaming AI features.
- Never block Googlebot or `noindex` a page to escape AI Overviews; that removes it from Search. The tools are snippet controls and the Search Console setting.
- Judge pages on conversions, with clicks as context. Google says clicks from results pages with AI Overviews are "higher quality"; check that claim against this site's key event rates.
- Don't create pages to match fan-out query variations. Google's generative AI guide treats that as spam; cover sub-questions on the pages where they belong.

## Steps

1. **Pull 16 months of Performance data.** Search results, search type Web (text-based unless image search matters), country filter if the business serves one market.
   - Per page per month: clicks, impressions, CTR, average position. Per key page: its top 20 to 50 queries for the last 3 months and the same 3 months a year earlier.
   - The UI caps each export at 1,000 rows. For larger sites use the Search Console API (25,000 rows per request, paged with `startRow`; Google documents a ceiling of about 50,000 rows per day per search type) or Looker Studio. The BigQuery bulk export only holds data from the day it was switched on.
   - Normalise URLs before any join: drop `#` fragments and tracking parameters, settle protocol and trailing slash. Count the rows that fail to match and say how many.
   - AI Mode follow-up questions count as new queries in Search Console, so long conversational queries in the export may come from AI Mode (`inferred`). Keep them; they show how people phrase the topic.

2. **Pull the generative AI report.** Search view (AI Overviews and AI Mode combined) and Discover view, by page and by month; add country and device for the Search view if the business is multi-market or mobile-heavy.
   - Google announced it on 3 June 2026 and it reached all sites by 31 August 2026, so history is short. Note the first date with data; there is no year-over-year comparison yet.
   - Exported "~" and "-" values come out as zeros. Treat them as "too small to show", not as zero.
   - Search Labs experiments aren't included. Chart totals count several links from your site in one answer as one impression, so page rows won't add up to the chart total.
   - No report at all means either too few AI feature impressions or the property is excluded under Settings → Search generative AI. Find out which before concluding anything.

3. **Join and compute, one row per page.**
   - AI impressions for the last 3 months, and AI share = AI impressions ÷ Web impressions for the same months (`inferred`, rough, because the two reports count slightly differently).
   - Clicks, impressions, CTR and average position: last 3 months vs the same months a year earlier. Year over year removes most seasonality.
   - Key events and revenue per landing page from analytics, same windows.
   - A control group: 10 or more pages of similar intent with negligible AI impressions. If their clicks fell just as much, AI features aren't the main cause.
   - Pattern flags: clicks down 20%+ year over year, impressions flat or up, position steady within about one place, AI share high = the typical AI Overview pattern (`inferred`). Position down as well = a ranking loss first → `seo-performance-audit`.

4. **Spot-check the top queries.** For each key page take its 3 to 5 highest-impression queries, plus the business's money queries: usually 30 to 60 queries.
   - Private window, logged out, target country and language, mobile and desktop if traffic is split. Check each query on two different days; three for money queries.
   - AI Overview: shown, not shown, or only after "show more"? Site cited? Which of its URLs (often not the page you expected)? Which other domains are cited? Does the site rank in the classic top 10 for the same query?
   - AI Mode, recorded separately: same questions. Note when AI Mode cites you and the AI Overview doesn't, or the reverse.
   - Note "cited, wrong URL" (a blog post cited where the product page should be) and any wrong statement about the brand, quoted word for word (→ `ai-brand-facts`).
   - Record date, device and session state for every check. A single check is reported as a single check.

5. **Classify each page.** One class per page, with the evidence behind it.
   - **Cited and fine.** AI impressions present, cited in most checks, key events steady or up year over year even if clicks fell. `Leave it`, or `Worth doing` for factual freshness edits. Don't rewrite the passages being quoted.
   - **Shown but not cited.** An AI Overview or AI Mode answer appears on the page's main queries and the page ranks on page one, but other sites are cited. Usually the page never answers the exact question in a self-contained passage, or misses sub-questions the AI answers from other pages. `Fix next`: passages → `ai-citable-pages`; missing sub-questions → `query-fan-out-coverage`. Not on page one? Classic SEO comes first → `on-page-seo-review`.
   - **Commodity information losing clicks.** The page answers common knowledge (definitions, "what is", unit conversions, simple how-tos, generic tips) that the AI answer covers completely; clicks down year over year with impressions steady, cited or not. If the topic feeds conversions: `Fix next`, reposition it into something a summary can't replace, such as a calculator or tool, original data, templates, first-hand testing, current prices, or a clear expert opinion; or merge it into a stronger page. If it never converted: `Leave it` and stop judging it on clicks.
   - **Unaffected.** No AI feature on its main queries, or negligible AI impressions. Whatever moved its traffic, it wasn't this → `seo-performance-audit` if it moved.
   - A page that fits two classes gets the one that drives the action; note the other.

6. **Check eligibility for every page you want cited.**
   - Indexed: URL Inspection shows "URL is on Google" and the Google-selected canonical is this URL. A money page that isn't indexed is `Fix now`.
   - Snippet-eligible: no `nosnippet` or `max-snippet:0` in meta robots or `X-Robots-Tag`; no small sitewide `max-snippet` value set by a plugin; no `data-nosnippet` wrapped around the main answer. Accidental ones are `Fix now`.
   - Settings → Search generative AI says Include for the property. Child properties (subdomains, URL-prefix properties for a folder) can stop inheriting and exclude themselves; check each property that covers key pages.
   - Structured data matches the visible text: prices, ratings, availability, dates, authors. Markup claiming what the page doesn't show is `Fix next` → `schema-markup`.
   - The answer is in the HTML Googlebot renders (URL Inspection → View crawled page), not behind a click, login or consent wall.
   - `Google-Extended` in robots.txt doesn't affect AI Overviews or AI Mode. `Leave it` for this purpose.

7. **Set expectations with dated studies.** Use them as context, never as a forecast for this site.
   - Pew Research Center (Jul 2025; browsing data from ~900 US adults, March 2025): people clicked a traditional result on 8% of visits with an AI summary vs 15% without, and a link inside the summary on 1%.
   - Ahrefs (Feb 2026, vendor data): AI Overviews went with ~58% lower CTR for the top-ranking page.
   - Seer Interactive (2025-26, vendor data): ~3.3% organic CTR on queries without an AI Overview, ~2.1% when the brand was cited in it, ~0.9% when it wasn't.
   - Google's AI features documentation says these clicks are higher quality (people spend longer on the site). It gives no numbers; test it with this site's key event rates.
   - How often AI Overviews appear varies hugely by study and query mix. Never quote one prevalence figure; use the site's own spot checks.

8. **Measure conversions, not just clicks.** GA4 counts AI Overview and AI Mode clicks as Organic Search (Google's channel definitions say so); they can't be split out.
   - Landing page report, Organic Search, year over year: sessions, key events, key event rate and revenue for every classified page.
   - Sessions down but key events steady means the lost clicks were low-intent; sessions and key events both down is the real loss. Put those pages first.
   - Branded search impressions rising while non-brand clicks fall can mean people meet you in AI answers and search your name later (`inferred`; tracking → `ai-traffic-analytics`).

9. **Decide whether to opt out.** The default is to stay included. Write the decision up with numbers:
   - What's at stake: clicks and key events on pages with AI impressions. Excluding the site means no traffic or impressions from these features at all.
   - Does inclusion cost more than it brings? Only when the content is the product (data, reference, recipes, paid research) and the evidence shows the summary replacing the visit: AI impressions up, clicks down, no conversion lift.
   - Will the answer just use someone else? Yes. Google says other sites' content still appears; opting out removes you, not the AI Overview.
   - Use the narrowest tool: `data-nosnippet` on specific passages (proprietary figures) → `max-snippet` on a template (also shortens normal snippets) → `nosnippet` on a page (normal snippet goes too; expect lower CTR) → Exclude under Settings → Search generative AI for a property (a URL-prefix property can isolate one folder). The setting covers AI Overviews, AI Mode and Discover's generative features, takes a few days, and doesn't control AI training.
   - Never: block Googlebot, `noindex`, or serve Google's AI different content from what users see.
   - To test, exclude one folder for an agreed period (6 to 8 weeks is a practical minimum given weekly noise) against a matched control folder, and compare clicks and key events. It's the owner's decision: draft the change, don't make it.

10. **Re-measure monthly.** Re-export both reports, re-run the same spot-check queries the same way, and update classes. Call a change real when it holds for two months running.

## Run it with DataForSEO (optional)

DataForSEO replaces the manual spot checks in step 4 and finds AI Overview citations across far more keywords. Connect with your API login and password (HTTP Basic), or through the official MCP server `dataforseo-mcp-server`, calling endpoints via its `api_request` tool.

- AI Overviews: `/v3/serp/google/organic/task_post`, then `/v3/serp/google/organic/task_get/advanced/$id` (or `/v3/serp/google/organic/live/advanced` when someone is waiting), with `keyword`, `location_code`, `language_code`, `device`, `depth: 10` and `load_async_ai_overview: true`. Without that flag you only get cached AI Overviews.
- Read the `ai_overview` item: `items[]` for the answer text and `references[]` (type `ai_overview_reference`: `source`, `domain`, `url`, `title`, `text`) for citations. Read the organic items in the same response to see whether the site ranks top 10.
- AI Mode, as its own run: `/v3/serp/google/ai_mode/task_post` + `task_get/advanced` (or `live/advanced`). The result is an `ai_overview` container with `markdown`, `items` and `references`. Only works in markets where Google offers AI Mode.
- Keywords where the domain is already cited in AI Overviews: `/v3/dataforseo_labs/google/ranked_keywords/live` with `target` (the domain), `location_code`, `language_code`, `item_types: ["ai_overview_reference"]` and an explicit `limit`. This is DataForSEO's database, not a live check: use it to find candidate queries, then confirm with SERP calls.
- Example run at published prices: 200 keywords × 2 days of Standard SERP calls with async AI Overviews ≈ $0.50-1.10; the same 200 in AI Mode Standard × 2 ≈ $0.48; one ranked_keywords call returning 1,000 rows ≈ $0.13. The AI Overview surcharge is documented inconsistently, so read current prices from `GET /v3/appendix/user_data` (free; it also returns `money.balance`).

Guardrails:
- Estimate the cost (calls × rate, rows × rate) and get the user's OK before any paid call; default cap $2 per run unless they set one. Check `money.balance` first.
- Always set `limit`. Keep `depth` at 10; no search operators (5× price), `calculate_rectangles` or clickstream data unless asked.
- Standard queue (`task_post`, up to 100 tasks per POST) for batches; Live only when someone is waiting.
- Cache SERP results for 7 days. Check money queries on at least 3 different days and report how often you were cited, not one result.
- Test new code on `https://sandbox.dataforseo.com/v3/...` first. Never print or store the API password in outputs or shared files.

## What to hand back

Fill in this template. Every recommendation carries a priority label, an evidence label and a confidence.

```markdown
# Google AI Overviews and AI Mode audit: [site], [date]

**What I found:** [one line, e.g. "22 of 40 key pages get AI feature impressions; 7 are cited and converting, 8 shown but not cited, 5 commodity pages lost 40-60% of clicks year over year."]
**What matters most:** [one line, e.g. "The pricing guide is shown but not cited on 9 of 12 money-query checks, and its key events fell 30%."]
**What to do first:** [one line]

## Data and method
- Performance: [date range], Web, [country]; [n] pages via [UI / API / Looker Studio]; unmatched URLs: [n]
- Generative AI report: Search from [first date with data] to [date]; Discover: [yes / no data]
- Analytics: [tool]; key events used: [list]
- Spot checks: [n] queries × [runs] on [dates], [country], [device], logged out; AI Overviews and AI Mode recorded separately
- Control group: [n] pages with negligible AI impressions; their clicks year over year: [x%]

## Pages by class
- [URL] - [cited and fine | shown but not cited | commodity losing clicks | unaffected] - AI impressions (3 mo): [n] - clicks YoY: [x%] - CTR YoY: [x → y] - position: [x → y] - key events YoY: [x%] - AIO cited: [k of n checks] - AI Mode cited: [k of n checks] - action: [label]

## Fixes, in order
1. [Fix now | Fix next | Worth doing] [what to change, on which page] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low] - how we'll know: [metric]

## Eligibility problems
- [page or property]: [not indexed / snippet control / generative AI setting / markup mismatch / not in rendered HTML] - fix: [change] - [priority label]

## Citations found
- "[query]": AIO [shown / not shown] - cited: [our URL / no] - AI Mode cited: [our URL / no] - cited instead: [domains]

## Opt-out recommendation
- [stay included / data-nosnippet on X / test exclusion of folder Y]; at stake: [clicks, key events]; reasoning: [two lines]; decision owner: [name]

## Leave it
- [thing that looks like a problem but isn't worth the time, and why]

## What I could not check
- [data, query or page not checked, and what would verify it]
```

## Stop and flag if

- The property is set to Exclude under Search generative AI, or key templates carry `nosnippet`: ask whether it's deliberate before calling it a defect. It may be a licensing decision.
- The generative AI report is missing while the setting is Include: say the site may have too few AI impressions. Don't fill the gap with third-party "AI traffic" estimates; Google's own guide warns against tools that claim access to its internal metrics.
- The click drop lines up with a migration, a core update or a position drop: run `seo-performance-audit` first.
- Anyone proposes blocking Googlebot, `noindex`, cloaking, hidden instructions to AI or mass pages for fan-out variations. Google's spam policies cover attempts to manipulate generative AI responses in Search. Take it out of the plan.
- You're asked to change the Search Console setting, robots directives or templates: draft the change and ask permission for that specific change.
- Unacceptable output: AI-caused click losses labelled `seen`, studies presented as this site's forecast, one-run citation claims, a single AI Overview prevalence figure, or AI Overviews and AI Mode merged into one result.

## Next step

- `ai-citable-pages` for each "shown but not cited" page, with the spot-check notes: who was cited instead and which passage they used.
- `query-fan-out-coverage` for money queries where the answer cites other sites for sub-questions this site never covers.
- `ai-traffic-analytics` to report AI referrals, branded search and conversions every month from here.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
