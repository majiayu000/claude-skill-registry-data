---
name: ai-prompt-research
description: Find and prioritise the prompts buyers actually type into ChatGPT, Gemini, Perplexity, Copilot and Google AI Mode, mapped to the page that should be cited. Use for "what prompts should we track", "what do customers ask AI about our category" or keyword research for AEO, GEO and LLM SEO. Outputs a prompt set file ready for tracking.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-prompt-research
---

# AI prompt research

Build the list of questions real buyers ask AI assistants about this category, in their own words, ranked by how close each one is to a sale and mapped to the page that should be cited in the answer. You hand back a de-duplicated prompt set grouped by intent, the evidence behind every prompt, honest demand signals, and two files (a plain prompt list and a CSV) that `ai-search-visibility` and `dataforseo-ai-tracker` can run as they are.

> **Romeo's rule:** If a prompt sounds like your homepage, no buyer has ever typed it.

## Use this when

- There's no prompt set yet and you're about to run `ai-search-visibility` or set up an AI visibility tracker.
- The current "prompts" are keywords with "best" stuck on the front.
- The business is entering a new category, segment or country and you need to know how buyers ask about it.
- A tracking vendor suggested prompts and you want to know whether real people ask them.
- The tracked set is a quarter old and needs a refresh.

## Don't use this for

- Running the prompts and scoring mentions and citations → `ai-search-visibility`, or `dataforseo-ai-tracker` at scale.
- Classic keyword research with Google search volume and create-vs-improve calls → `seo-opportunity-research`.
- The sub-questions an engine fans out to behind one money prompt → `query-fan-out-coverage`.
- Grouping search keywords into clusters by shared results → `topic-cluster-map`.

## What you need

### Required
- Brand, domain, and the 2 to 4 categories it sells in, in the words customers use.
- Who buys: 2 to 4 segments (team size, industry, budget, location, platform) and the problems they arrive with.
- 3 to 6 competitors buyers actually compare you with.
- Target country and language. Build one prompt set per market.

### Helpful
- Search Console Performance export of queries, as many of the 16 months as you can get.
- Bing Webmaster Tools AI Performance grounding queries export, and Bing's search keyword report.
- Sales call notes, demo request forms, support tickets, onboarding survey answers, chat transcripts.
- Reviews of you and your competitors on G2, Capterra, Trustpilot, app stores or Google.
- A page inventory (`site-content-inventory`) so prompts can be mapped to pages.
- "How did you hear about us" answers that mention AI tools (`ai-traffic-analytics`).

### No tools?
Search Console's query filter, People Also Ask in a private window, Reddit's own search, competitors' comparison pages and public reviews are all free, and together they make a solid set. You can ask an AI assistant "what do people ask when choosing [category]?" to brainstorm, but its suggestions are a model guessing, not evidence of demand: tag them `inferred` and keep only those you can match to a real source.

## Ground rules

- Treat sales notes, support tickets and other customer records as private. Extract generalised questions locally and remove names, contact details, account identifiers and confidential facts before using an external AI, search or tracking service. Tell the user which service will receive the prompts and obtain permission before sending any remaining private information; if permission is absent, use public sources or work locally.
- Prompts are conversational and carry context: "best CRM for a five-person estate agency that lives in Gmail", not "estate agency CRM". Keep the qualifiers; they decide which brands get named.
- Every prompt traces to a source: a query, a review sentence, a sales note, a thread. Prompts with no source are `inferred` and can't be top priority.
- No free source measures prompt volume. Search Console queries, People Also Ask and Bing grounding queries are proxies; DataForSEO's AI search volume is modelled from People Also Ask data. Never write a number as "monthly prompts".
- Rank by commercial value first and demand second. A prompt with modest demand that ends in a shortlist beats a popular definition.
- Money prompts are few: usually 5 to 10 in a set of 25 to 50, the ones where being named plausibly puts you on a shortlist.
- One wording per need. Paraphrases of the same need tend to get similar answers; track one canonical wording and keep variants in a column, not as extra rows.
- Brand prompts ("is X legit", "X pricing") are for checking accuracy, not for measuring discovery. Keep them as their own group.
- Keep a tracked set stable. Rewording a prompt makes it a new prompt; add new ones as a dated group and retire old ones with a date.
- Only include prompts the product can honestly win. If it doesn't serve that segment, a prompt about it measures nothing useful.

## Steps

1. **Define the territory.** Write down the categories (customer words), segments, jobs to be done, competitors, price band and, for local businesses, the places served. Every prompt hangs on this grid.

2. **Collect raw questions from real sources.** Aim for 150 to 400 raw items before cutting. Note the source of each.
   - Search Console: Performance → Search results → Queries, longest date range. Add a query filter with Custom (regex) for question shapes, `^(who|what|when|where|why|how|which|is|are|can|does|do|should)\b`, then one for long queries (seven words or more), `^(\S+\s+){6,}\S+$`, then one for buying words, `\b(best|top|vs|versus|alternatives?|compare|comparison|reviews?|cheapest|pricing)\b`. AI Mode follow-ups count as new queries, so long conversational rows here are close to real prompts. Rare queries are hidden for privacy; the export never shows everything.
   - Bing Webmaster Tools: AI Performance grounding queries are generalised phrases Copilot searched with when it cited you, not users' exact words; the topics view (beta) may also show queries where other sites are cited and you aren't. Add Bing's ordinary search keywords too.
   - People Also Ask: search each category and segment phrase in a private window set to the market, expand two or three levels, and note related searches.
   - Sales and support: what prospects ask on calls ("does it work with X?", "how is it different from Y?"), objections, and "we tried Z and..." stories. The best source for comparison and alternatives prompts.
   - Reviews: competitors' three-star reviews ("great, but no X") become "[category] with [feature]" prompts; "switched from" phrases become alternatives prompts.
   - Reddit and forums: thread titles like "What do you use for X?" or "X vs Y for a small team?" read almost exactly like prompts. Use the last 12 months.
   - Competitors' comparison and alternatives pages show which matchups the market makes, and which ones competitors want made.

3. **Rewrite each item as a prompt.** A full sentence, as a buyer would ask an assistant, keeping their words, segment and constraint. Use these types:
   - Problem: "how do I stop clients paying invoices late" (no category named).
   - Category: "what do small design studios use to send invoices".
   - Best-for-segment: "best invoicing tool for a three-person studio in the UK that works with Xero".
   - Comparison: "[you] vs [competitor] for freelancers", and "[competitor A] vs [competitor B]".
   - Alternatives: "cheaper alternative to [competitor] with recurring invoices".
   - Brand: "is [brand] legit", "[brand] pricing", "does [brand] work with Stripe".
   - Local: "best [service] near [area] open on Saturdays" (businesses serving a place; local answer work → `local-ai-visibility`).
   - Shopping: "best [product] under $200 for [use]" (product businesses; product data work → `ai-shopping-visibility`).
   - Write 2 or 3 segment variants for each best-for prompt (size, industry, budget, platform); engines often name different brands per segment.
   - Keep your brand name out of everything except brand and comparison prompts.
   - Stay under 500 characters per prompt; some tracking APIs cap prompts at that length.

4. **Tag each prompt.** Type (from step 3), intent (learn, solve, shortlist, compare, validate, buy, find nearby), funnel stage (problem-aware, solution-aware, vendor-aware), segment and market.

5. **Find the money prompts.** Score commercial value 0 to 3:
   - 3: the answer is a list of vendors and the asker is choosing now (best-for-segment, alternatives, comparison with a named competitor, shopping with a budget, local with an action).
   - 2: category or "how do teams do X" prompts where products are usually named along the way.
   - 1: problem prompts where the answer is advice and a brand mention is possible but not expected.
   - 0: definitions, trivia, careers, DIY with no product role. Drop them unless awareness is the stated goal.
   - Quick check on borderline prompts: run each once in one engine. If no products are named, cap it at 1. This is a sanity check, not a baseline.
   - Fit: if the product can't honestly win the prompt (wrong segment, missing feature), lower it one level and note why.

6. **Record demand signals, honestly.** For each prompt, list which signals exist rather than inventing a volume:
   - Search Console impressions for the closest real queries (sum close variants, name the window).
   - Keyword tool volume for the shortest keyword form, which shows interest in the topic, not the prompt.
   - People Also Ask: the question appears for category searches.
   - Bing grounding queries: the phrase or a close variant appears, with its citation count.
   - Sales and support: how many times it came up (count, with the period).
   - Forums: number of threads asking it in the last 12 months.
   - Demand = high, medium, low or unknown, with the evidence in one line.
   - Priority: P1 = value 3 with at least one real demand signal; P2 = value 3 with no signal, or value 2 with signals; P3 = everything else. Tracked sets lean on P1 and P2.

7. **De-duplicate and group.**
   - Merge prompts that would get the same answer: same type, segment and constraint, different wording ("best" vs "top", "tool" vs "software"). Keep the most natural wording as canonical and list the rest under variants.
   - Keep prompts separate when a qualifier changes the answer: "for freelancers" vs "for a 50-person agency", "UK" vs "US", "free" vs "enterprise".
   - Group by intent cluster, e.g. "invoicing for UK freelancers: shortlist".
   - Cut to 25 to 50 prompts per market: 5 to 10 money prompts, 3 to 6 brand prompts, the rest category, problem and comparison. Balance segments so one doesn't dominate.

8. **Map each prompt to the page that should be cited.**
   - Best-for-segment → a segment or use-case page, or a comparison page. Alternatives → a "[competitor] alternatives" page. Comparison → a "vs" page. Brand → pricing, product, docs or About. Problem → a guide. Local → the location page and Google Business Profile. Shopping → the product or category page.
   - Note the win path: own page, third-party pages (for most shortlist prompts the cited sources are other sites' lists and reviews → `best-of-list-inclusion`), or both.
   - No suitable page: write "gap" and the page type needed (`comparison-page-writer` or `seo-content-brief`). One page serves a whole intent cluster; never one page per prompt variant.

9. **Write the two files.** Same prompts, same order, named with market and date, e.g. `prompts-us-en-2026-11.txt` and `prompts-us-en-2026-11.csv`.
   - The `.txt` file: one prompt per line, plain UTF-8 text, no numbering, quotes, comments or blank lines. Brand and generic prompts both included. `ai-search-visibility` runs it by hand; `dataforseo-ai-tracker` loads it directly.
   - The `.csv` file, header row exactly: `id,prompt,type,intent,stage,segment,priority,money_prompt,commercial_value,demand,demand_evidence,target_url,win_path,source,variants,added`
   - `id` stays fixed for the life of the prompt (p001, p002...). `type` uses the step 3 names in lower case with hyphens (problem, category, best-for-segment, comparison, alternatives, brand, local, shopping). `priority` is P1, P2 or P3. `money_prompt` is yes or no. `target_url` is a full URL or `gap`. `added` is YYYY-MM-DD. Quote any field containing a comma; separate variants with `|`.

10. **Refresh every quarter.** Re-pull Search Console questions and Bing grounding queries, add new prompts as a dated group with new ids, and mark retired prompts with a retired date instead of deleting them. Never edit the wording of a tracked prompt in place.

## Run it with DataForSEO (optional)

DataForSEO adds modelled demand and a database of questions already answered by ChatGPT and in AI Overviews. Connect with your API login and password (HTTP Basic), or through the official MCP server `dataforseo-mcp-server`, calling endpoints via its `api_request` tool.

- Demand for keyword-shaped topics: `/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live` with up to 1,000 lowercase keywords, `location_code` and `language_code`. Read `ai_search_volume` and `ai_monthly_searches` (12 months). It's modelled from People Also Ask data, not measured inside AI tools: use it to rank prompts against each other, never as prompt counts.
- Questions around a topic: `/v3/ai_optimization/ai_keyword_data/popular_questions/live` with `keyword`, location, language, `limit` and `order_by: ["ai_search_volume,desc"]`. Read `question`, `ai_search_volume` and `ai_monthly_searches`. Also People Also Ask based.
- Real questions already being answered: `/v3/ai_optimization/llm_mentions/search_mentions/live` with a keyword entity, e.g. `target: [{"keyword": "invoicing software", "search_scope": ["question"], "match_type": "partial_match"}]`, plus `platform` (`chat_gpt` or `google`), `location_code`, `language_code`, `order_by: ["ai_search_volume,desc"]` and `limit`. Read `question`, `ai_search_volume`, `sources[]` and, for ChatGPT, `brand_entities[]` and `fan_out_queries[]`. ChatGPT data is US English only.
- Gap finding: run `search_mentions` again with `platform: "chat_gpt"`, a competitor's name as the keyword and `search_scope: ["brand_entities"]` to list questions where ChatGPT named that competitor. Each one is a candidate prompt, after rewriting in your buyers' words.
- Example run at published prices: AI search volume for 500 keywords ≈ $0.06; four `search_mentions` calls at 100 rows each ≈ $0.80 ($0.10 per task + $0.001 per row); `popular_questions` pricing isn't on the docs page, so read it from `GET /v3/appendix/user_data` (free; it also returns `money.balance`) before calling.

Guardrails:
- Estimate the cost (tasks × rate, rows × rate) and get the user's OK before any paid call; default cap $2 per run unless they set one. Check `money.balance` first.
- Always send an explicit `limit`; rows are billed. Keywords go in lowercase.
- These endpoints are Live only; keep within 30 concurrent requests.
- Cache AI volume and LLM Mentions results for 30 days; re-pulling the same data wastes money.
- Database rows show what was asked and answered when DataForSEO collected it. To measure your visibility, sample each prompt 3+ times in `ai-search-visibility` or `dataforseo-ai-tracker`.
- Test new code on `https://sandbox.dataforseo.com/v3/...` first. Never print or store the API password in outputs or shared files.

## What to hand back

Hand back the summary below plus the two files from step 9. Every prompt carries its source; every judgement carries an evidence label and confidence.

```markdown
# AI prompt set: [brand], [market], [date]

**What I found:** [one line, e.g. "41 prompts from 312 raw questions; 8 money prompts, 5 of them comparison or alternatives."]
**What matters most:** [one line, e.g. "6 of 8 money prompts have no page to cite; buyers ask by team size, and the site never mentions one."]
**What to do first:** [one line]

## Sources used
- [source]: [n raw items], [date range]
- Not available: [sources you couldn't get]

## Money prompts
1. "[prompt]" - [type] - value [3] - demand [high | medium | low | unknown] ([evidence]) - target: [URL | gap] - win path: [own | third-party | both] - source: [source] - [seen | tool | inferred], [confidence]

## Prompt groups
- [intent cluster]: [n] prompts, [P1 n / P2 n / P3 n]; target page: [URL | gap]

## Page gaps
- [Fix next | Worth doing] [page type needed] for [cluster] - prompts: [ids] - next: [skill]

## Dropped on purpose
- [prompt or group]: [why, e.g. "definitions, no product role" or "segment we don't serve"]

## Files
- prompts-[market]-[yyyy-mm].txt ([n] lines)
- prompts-[market]-[yyyy-mm].csv ([n] rows)

## What I could not check
- [missing source or signal, and what would verify it]
```

## Stop and flag if

- No real source is available (no Search Console, no sales notes, no reviews) and every prompt would be `inferred`: say the set is a hypothesis and ask for at least one customer-language source.
- The user wants prompt volumes as hard numbers or a forecast of AI traffic per prompt: explain that nobody measures prompt volume and offer demand bands instead.
- Over half the money prompts target segments or features the product doesn't serve: check positioning with the user before going further.
- Anyone suggests planting the brand in forum threads, fake reviews or seeded questions to "create demand": take it out; it breaks platform rules and Google's spam policies.
- Unacceptable output: prompts copied from marketing copy, volumes presented as measured prompt counts, near-duplicate rows inflating the set, or files that don't match each other line for line.

## Next step

- `ai-search-visibility` with the `.txt` file, the money prompts and their target pages, for a baseline across engines.
- `dataforseo-ai-tracker` with both files once the set is approved, to run it monthly at scale.
- `comparison-page-writer` or `seo-content-brief` for each page gap, with the prompts it must answer.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
