---
name: ai-search-visibility
description: The AEO, LLM SEO and GEO hub. Get a brand cited and recommended in Google AI Overviews and AI Mode, ChatGPT, Perplexity, Copilot, Claude and Gemini. Use for "why doesn't ChatGPT recommend us", "are we in AI Overviews" or "track our AI visibility". Runs a buyer prompt set, measures citation share and routes fixes for pages and sources.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-search-visibility
---

# Get cited in AI search answers

Find out where AI answer engines mention, cite or ignore a brand for the questions its buyers actually ask, work out why, and fix it. You hand back a baseline scorecard per prompt and engine, the third-party sources each engine leans on, every wrong fact the engines repeat about the brand, and a prioritised fix list covering access, quotable pages, entity clarity and outside mentions.

> **Romeo's rule:** Answer engines mostly repeat what the rest of the web already says about you, so change what the web says before you fiddle with your own markup.

## Use this when

- Someone asks "why does ChatGPT recommend our competitors and not us?" or "are we showing up in AI Overviews?"
- You need a baseline before spending on AI search work, or proof afterwards that the work moved anything.
- Clicks fell on informational queries where Google now shows an AI Overview, and you want to know whether you're cited in it.
- AI answers describe the brand wrongly: old pricing, missing features, confused with a company of the same name.
- A launch, rebrand or new product category needs to start appearing in AI answers.

## Don't use this for

- Robots.txt rules for AI bots, llms.txt, Markdown page versions and whether agents can use the site → `ai-agent-readiness`; pages that aren't indexed or render blank for Googlebot → `technical-seo-audit`.
- One part of this job in depth: finding and ranking the prompts buyers ask → `ai-prompt-research`; wrong facts AI repeats about the brand → `ai-brand-facts`; rewriting a page so AI can quote it → `ai-citable-pages`; the sub-questions behind a money prompt → `query-fan-out-coverage`; Search Console's AI Overview and AI Mode data and the opt-out decision → `google-ai-overviews-audit`; AI referrals, signups and revenue → `ai-traffic-analytics`; tracking hundreds of prompts on a schedule → `dataforseo-ai-tracker`.
- Doing the work the fix list points to: writing the "best X", "X vs Y" or "alternatives" pages this skill tells you to create → `comparison-page-writer`; third-party "best X" lists → `best-of-list-inclusion`; review platforms → `reviews-for-ai-answers`; YouTube → `youtube-for-ai-answers`; Reddit and Quora threads → `reddit-quora-answers`; LinkedIn → `linkedin-for-ai-search`; author pages, About page and reputation signals → `eeat-trust-review`.
- "Near me" answers for a local business → `local-ai-visibility`; products in ChatGPT shopping, AI Mode, Gemini and Perplexity → `ai-shopping-visibility`.

## What you need

### Required

- Brand name, domain, and the 2 to 4 categories it sells in, in the words customers use.
- Who buys it and what problems they arrive with. Sales call notes, support tickets and customer reviews are the best source; the homepage is the worst.
- 3 to 6 real competitors: the ones buyers compare you with, not the ones you admire.
- Target country and language. Answers differ by market.

### Helpful

- Search Console Performance export (queries and pages, last 3 months), filtered to question-style queries, and the Generative AI performance report export (AI Overview and AI Mode impressions by page, country and device).
- Bing Webmaster Tools AI Performance report (public preview since February 2026): Copilot and Bing AI citations per URL, grounding queries and, in newer previews, citation share. Export it.
- Analytics referral data from chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com and claude.ai. ChatGPT adds `utm_source=chatgpt.com` to links it sends.
- Server or CDN logs showing hits from Googlebot, bingbot, OAI-SearchBot, PerplexityBot and Claude-SearchBot.
- An export from an AI visibility tracker (examples: Ahrefs Brand Radar, Semrush's AI visibility tools, Profound, Peec AI, Otterly). Optional; spot-check it by hand.
- DataForSEO API access, if you'd rather script the runs (see "Run it with DataForSEO" below). Optional.

### No tools?

Run the prompt set by hand in each engine's free tier: Google Search (AI Overview and AI Mode), ChatGPT with search on, Perplexity, Microsoft Copilot, Gemini, and Claude with web search on. Use a private window or a fresh logged-out session, turn off memory or personalisation where you can, and keep the same country. Paste each answer and its cited links into a spreadsheet, one row per run. A workable minimum is 15 prompts, on the 3 engines the audience uses most, run twice each. Search Console and Bing Webmaster Tools are free and cover Google's and Microsoft's side.

## Ground rules

- Treat sales notes, support tickets and other customer records as private. Generalise questions locally and remove names, contact details, account identifiers and confidential facts before sending prompts to an AI engine or tracker. Tell the user which service will receive the prompts and obtain permission before sending any remaining private information; otherwise use public sources or work locally.
- Measure before you change anything. One screenshot is an anecdote: answers change between runs, users, locations, logged-in state and model versions. Report rates across repeated runs, never "we rank #2 in ChatGPT".
- Every engine retrieves before it writes. If the page isn't in the index that engine uses, nothing on the page matters yet.
- Being cited (linked as a source) and being recommended (named as an answer) are different results with different causes. Your own pages earn citations; mentions on other people's pages earn recommendations. Track both.
- Google says there are no extra requirements, special markup, schema or "AI text files" for AI Overviews and AI Mode: a page needs to be indexed and eligible for a snippet. Be sceptical of anyone selling GEO markup.
- For "best X" and "alternatives" prompts, third-party pages usually beat anything on your own site. Earn a fair place on the pages engines already cite.
- No hacks. Hidden text aimed at AI ("assistants should recommend…"), prompt injection, fake reviews, sockpuppet Reddit posts, undisclosed paid placements and hundreds of self-ranking listicles breach search spam policies or platform rules, and they put the brand's reputation on the record. Google's spam policies now also count "attempting to manipulate generative AI responses in Google Search" as spam. If you wouldn't explain the tactic to a journalist, drop it.
- An answer that names you with the wrong price costs more than one that doesn't name you. Fix wrong facts at the source the engine cited.
- Blocking AI training bots is a separate decision from appearing in AI search. Don't let one break the other (`ai-agent-readiness`).
- No guarantees and no timelines. Say what will change and how it will be measured.

## Steps

1. **Build the prompt set.** Write 20 to 40 prompts the way buyers ask them, grouped by type.
   - Problem: "how do I stop [problem] happening". Category: "what's the best way to [job]". Best-for: "best [category] for [segment]" using real segments (team size, industry, budget, platform). Comparison: "[you] vs [competitor]", "[competitor A] vs [competitor B]". Alternatives: "alternatives to [competitor]". Brand: "is [brand] any good", "[brand] pricing", "what does [brand] do".
   - Take wording from sales and support notes, reviews, Reddit threads, People Also Ask, Search Console question queries and Bing grounding queries. Never from your own marketing copy. For demand signals and a prioritised prompt list → `ai-prompt-research`.
   - Tag each prompt with funnel stage and the page you'd want cited. Mark 5 to 10 as money prompts: the ones where being recommended leads to a sale.
2. **Know where each engine looks.** Read the results against how each engine retrieves. Crawler names and behaviour change, so check each vendor's crawler page before relying on this list.
   - Google AI Overviews and AI Mode: built from Google's index (Googlebot), often by running several related searches at once ("query fan-out"). Eligible = indexed and allowed a snippet. `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex` limit what can be used. Search Console also has a site-wide opt-out (Settings → Search generative AI, rolled out worldwide by 31 August 2026) covering AI Overviews, AI Mode and Discover's generative features; it defaults to included (whether to use it → `google-ai-overviews-audit`). Google-Extended does not affect inclusion in Search or these features.
   - Gemini app: grounded on Google Search. Disallowing Google-Extended opts content out of Gemini training and out of grounding in Gemini Apps and Vertex AI, so it can cost Gemini app citations.
   - ChatGPT search: OpenAI's OAI-SearchBot index plus third-party search providers (check OpenAI's current publisher FAQ for which). Sites that block OAI-SearchBot are left out of search answers except as navigational links; OpenAI says robots.txt changes take about 24 hours. ChatGPT-User fetches pages a user asks about; GPTBot is for training only.
   - Perplexity: its own index built by PerplexityBot. Perplexity-User fetches pages for a user's question and, per Perplexity, generally ignores robots.txt.
   - Microsoft Copilot: Bing's index. Today `NOARCHIVE` keeps a page out of Copilot answers and `NOCACHE` limits use to URL, title and snippet; Microsoft starts honouring new, separate AI training and AI grounding preferences on 1 February 2027 and stops reading `NOARCHIVE` and `NOCACHE` for AI use on 1 March 2027 (Bing blog, October 2026).
   - Claude: Claude-SearchBot indexes for search (check Anthropic's current help pages for any third-party search providers); Claude-User fetches on a user's request; ClaudeBot is training.
3. **Run the baseline.** For every prompt on every engine in scope, run at least twice (three times for money prompts) in clean sessions, same country, and note date, engine, mode and model if shown. Record:
   - Whether an AI answer appeared at all. Google shows AI Overviews only for some queries; "no AI answer" is not the same result as "not mentioned".
   - Brand named (yes/no) and position: named first, in the first three, later, or not at all.
   - Every cited URL, yours and others', and which competitors were named.
   - Tone towards the brand: positive, neutral, negative, or factually wrong. Quote wrong statements word for word.
   - If a tracker supplied the data, re-run 5 prompts by hand. Trackers often query through APIs that answer differently from the consumer app.
4. **Score it and find the gaps.** Per prompt and engine: mention rate = runs naming you ÷ runs; citation rate = runs linking your domain ÷ runs; do the same for each competitor. Roll up by prompt group. Then list:
   - Gap prompts: competitors named, you not. These are the work.
   - Cited but not recommended: your page is a source but another brand gets the recommendation. Usually your page answers the question without saying who the product is for.
   - Wrong facts and where each came from. Follow the cited link; it's often your own old pricing page, an outdated review, or a directory listing. Tracing and fixing them → `ai-brand-facts`.
   - The source map: the 10 to 20 third-party domains cited most often across money prompts, and whether each mentions you.
   - For Google prompts, compare cited URLs with the classic top 10 for the same query and its obvious sub-questions. Cited pages usually rank there too (`inferred`), so a competitor cited because it ranks and you don't is a classic SEO gap → `on-page-seo-review` or `seo-opportunity-research`. Sub-questions no page of yours answers → `query-fan-out-coverage`.
5. **Check access and indexing for the engines that matter.** For every page you want cited:
   - Indexed in Google (URL Inspection) and in Bing (Bing Webmaster Tools URL Inspection). Not in Bing means invisible to Copilot, and possibly weaker in engines that buy third-party search results. `Fix now` for money pages.
   - robots.txt and the CDN or firewall let Googlebot, bingbot, OAI-SearchBot, PerplexityBot and Claude-SearchBot through. Look for 403, 429 or challenge pages in logs. Policy design and testing → `ai-agent-readiness`.
   - The answer, price and product name are in the initial HTML. Many AI crawlers are reported not to run JavaScript (Googlebot does), and no vendor promises they do.
   - No `nosnippet`, `max-snippet:0` or `data-nosnippet` wrapped around the part you want quoted, and Search Console's Search generative AI setting still includes the site (a child property can override its parent).
   - New or changed pages submitted to Bing through IndexNow or Bing Webmaster Tools.
   - Shops and local businesses: Merchant Center product data and the Google Business Profile are current; Google names both as inputs to its AI features. ChatGPT and Perplexity run their own merchant programmes for product data; check their current documentation before relying on them. In depth → `ai-shopping-visibility` and `local-ai-visibility`.
6. **Make the pages easy to quote.** For each page mapped to a money prompt, check that the first 40 to 80 words under the relevant heading answer the question on their own and name the entity ("Acme is payroll software for UK agencies under 50 staff", not "Our tool helps you…"), that prices, limits and dates sit in HTML text rather than images, PDFs or JavaScript tabs, and that claims are sourced and dated; list each failure as a fix and hand the passage-by-passage rewrite to `ai-citable-pages`.
7. **Make the entity unambiguous.** Check that one brand name, one-line description and category are used the same way on the site, social profiles, LinkedIn, Crunchbase, app stores and review sites (mismatches are `Fix next`), and that Organization markup with `sameAs` to official profiles exists (validation → `schema-markup`); the fact sheet, name collisions and source-by-source fixes belong to `ai-brand-facts`.
8. **Keep facts fresh.** Update prices, statistics, screenshots and comparison pages when facts change, and change the visible "updated" date and `dateModified` only for real edits. Redirect or update old pages that contradict current facts; stale pricing and feature pages are a common source of wrong AI answers.
9. **Earn mentions where the engines already look.** Work through the source map from step 4, highest-cited first.
   - "Best X" articles and listicles: send the author a factual update, a correction or a free account to test. Paid inclusion must be disclosed on the page and its links marked `rel="sponsored"`; undisclosed paid placement breaks advertising rules and Google's link spam policy. Pitch kit and outreach log → `best-of-list-inclusion`; vet any paid placement first with `sponsored-placement-vetting`.
   - Review platforms (G2, Capterra, Trustpilot, app stores, Google Business Profile): ask real customers, all of them, not just happy ones. Reply to negative reviews. Never write, buy or gate reviews. Which platforms and how → `reviews-for-ai-answers`.
   - Reddit, forums and Q&A sites: answer as yourself with your affiliation stated, only where you genuinely help. No sockpuppets. Finding the threads that rank or get cited → `reddit-quora-answers`; LinkedIn articles from a named person → `linkedin-for-ai-search`.
   - Integration directories, partner pages, docs, YouTube reviews, podcasts and newsletters the engines cite. Your own answer videos → `youtube-for-ai-answers`. Link-side opportunities → `backlink-profile-review`.
   - Wrong facts on third-party pages: ask the owner for a correction with evidence. This often fixes AI answers faster than anything on your own site (→ `ai-brand-facts`).
10. **Measure over time.** Re-run the same prompt set, same method, monthly and after major changes.
   - Track mention rate, citation rate and competitor share per prompt group; Bing AI Performance citations; AI referral sessions and conversions; Search Console clicks for the mapped pages, plus AI Overview and AI Mode impressions by page from Search Console's Generative AI performance report (rolled out to all sites by 31 August 2026; that data is also part of the "Web" search type, and the report may not appear for sites with few AI impressions).
   - Call a change real only when it holds across two or more monthly runs. Keep the prompt set fixed; add new prompts as a separate group so trends stay comparable.
   - In depth: AI referrals, signups and revenue → `ai-traffic-analytics`; Search Console's AI Overview and AI Mode report → `google-ai-overviews-audit`; more prompts than you can run by hand → `dataforseo-ai-tracker`.

## Run it with DataForSEO (optional)

Replaces the manual runs in steps 3, 4 and 10 if you have a DataForSEO account. Connect through the official MCP server (`dataforseo-mcp-server`, calling each path below with its `api_request` tool) or over HTTPS with Basic auth at `https://api.dataforseo.com`.

- ChatGPT and Gemini as users see them (LLM Scraper): `/v3/ai_optimization/chat_gpt/llm_scraper/task_post`, then `task_get/advanced` (same pattern under `gemini`). Send `keyword` (the prompt), `location_code`, `language_code` and, for ChatGPT, `force_web_search: true`. Read `markdown` (the answer), `sources[]` (what it cited), `brand_entities[]` (brands named) and `fan_out_queries`.
- Claude and Perplexity (LLM Responses): `/v3/ai_optimization/claude/llm_responses/task_post` (or `live`) and `/v3/ai_optimization/perplexity/llm_responses/live` (Live only). Send `user_prompt`, `model_name` (list them with the free `models` endpoint), `web_search: true`, `web_search_country_iso_code` and `max_output_tokens` of 2,048 or less. Read `items[].sections[].text`, `annotations[]` (cited URLs; can be empty even with search on) and `money_spent`. These run through the model's API, so answers can differ from the consumer apps; re-run 5 prompts by hand.
- Google AI Overviews, AI Mode and Copilot (SERP API): `/v3/serp/google/organic/task_post` plus `task_get/advanced` with `load_async_ai_overview: true` (without it you only get cached AI Overviews), reading the `ai_overview` item's `references[]`; AI Mode at `/v3/serp/google/ai_mode/task_post` plus `task_get/advanced`; Copilot as the `ai_overview` item in `/v3/serp/bing/organic/live/advanced`.
- Database share of voice (LLM Mentions): `/v3/ai_optimization/llm_mentions/multi_target_metrics/live` with you and each competitor as target groups (2 to 10), `top_mentioned_domains/live` for the source map, `historical/live` for the trend. These are DataForSEO's pre-collected prompts, not yours, for `google` (AI Overviews) and `chat_gpt` (US English only). Groups can overlap, so don't add them up as shares.
- Example costs at published prices: 30 prompts × 4 engines × 3 runs ≈ $1.20 to $5.70 (mostly Claude and Perplexity model charges); AI Overview citations for 200 keywords ≈ $0.25 to $0.55; a share-of-voice pull ≈ $0.90.
- Guardrails:
  - Estimate the cost (calls × rate, model charges as a range) and get the user's OK before any paid call; cap a run at $2 unless they set another limit. Check `money.balance` with the free `GET /v3/appendix/user_data` first, and read the AI Overview price there (it's documented inconsistently).
  - Always send `limit`. No search operators, `depth` over 10 or `calculate_rectangles` unless asked; they multiply the price.
  - Standard queue (`task_post`, up to 100 tasks per POST) for batches; Live only when someone is waiting. Cache results: SERPs 7 days, LLM Mentions 30 days.
  - Run each prompt 3 or more times and report rates, as in step 3. Test new code on the free sandbox (`https://sandbox.dataforseo.com/v3/...`) first. Check each task's `status_code` (20000 = OK). Never print or save the API password.
- Scheduled tracking, hundreds of prompts or a reusable script → `dataforseo-ai-tracker`.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# AI search visibility: [brand], [date]

**What I found:** [one line, e.g. "Named in 4 of 30 money-prompt runs; competitors A and B in 19 and 14."]
**What matters most:** [one line, e.g. "Not indexed in Bing, and the three listicles every engine cites don't mention you."]
**What to do first:** [one line]

## Method
- Prompts: [N] ([groups]); engines: [list]; runs per prompt: [n]; dates: [dates]; country/language: [x]; session: [logged out / memory off]
- Data sources: [manual runs / tracker name / Bing AI Performance / Search Console / analytics]

## Baseline by prompt group
| Prompt group | Engine | Mention rate | Citation rate | Leading competitor (rate) |
|---|---|---|---|---|

## Wrong or outdated facts in AI answers
- "[quoted claim]" on [engine], prompt "[prompt]"; cited source: [URL]. Fix: [action]. [Fix now] ([seen], high)

## Fixes, in order
1. [Fix now | Fix next | Worth doing] [what to change, on which page or site] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low] - how we'll know: [metric]

## Third-party sources to work on
- [domain/page]: cited for [prompts] on [engines]; mentions us: [yes / no / wrongly]; action: [action]; priority: [label]

## Leave it
- [thing that looks like a gap but isn't worth the time, and why]

## Re-measure plan
- Same [N] prompts, [engines], [runs] each, next run on [date]; success looks like [metric change].

## What I could not check
- [engine, data or page not checked, and what would verify it]
```

## Stop and flag if

- The site deliberately blocks OAI-SearchBot, PerplexityBot, bingbot or Claude-SearchBot, or has opted out in Search Console's Search generative AI setting. Confirm it's intended before recommending a change; it may be a legal or licensing decision.
- AI answers make claims about the product's safety, legality, health effects or financial risk. Report them to the user straight away; that's beyond an SEO fix.
- You have one run per prompt, or fewer than 10 prompts. Present results as anecdotal, not a baseline.
- Any proposed tactic involves hidden text, prompt injection, fake or incentivised reviews, sockpuppets or undisclosed paid placement. Remove it from the plan.
- The user wants a guaranteed position or a date by which ChatGPT will recommend them. Say plainly that nobody can promise that.
- Unacceptable output: invented mention or citation numbers, citations you didn't see, a single run reported as a rate, or "ranking #1 in ChatGPT" language.

## Next step

- Run `ai-agent-readiness` with the list of bots that were blocked, challenged or slow, and the pages whose content isn't in the raw HTML.
- Fix what the baseline found on your own pages: `ai-brand-facts` with every wrong claim quoted and its cited source; `ai-citable-pages` on the pages that are cited but not recommended, then `eeat-trust-review` on them to strengthen authorship, proof and reputation; `comparison-page-writer` for the gap prompts that need a "best X", "vs" or "alternatives" page, with the source map as competitor evidence.
- Work the source map, then measure: `best-of-list-inclusion`, `reviews-for-ai-answers`, `reddit-quora-answers`, `youtube-for-ai-answers` or `linkedin-for-ai-search`, depending on which source types dominate your money prompts, then `ai-traffic-analytics` to tie AI referrals to signups and revenue.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
