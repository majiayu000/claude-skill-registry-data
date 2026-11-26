---
name: query-fan-out-coverage
description: Map the sub-questions AI search engines look up behind a money prompt (query fan-out) to your pages and sections, find the gaps, and fill them without thin pages. Use for "query fan-out", "which sub-questions are we missing", or AEO / LLM SEO / GEO content coverage for Google AI Overviews, AI Mode and ChatGPT.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/query-fan-out-coverage
---

# Query fan-out coverage

Behind one buyer prompt, AI search engines run several narrower searches (definitions, prices, comparisons, segments, constraints) and build the answer from what those searches return. This skill lists the sub-questions likely behind each money prompt, maps each one to the URL and section that answers it or marks it missing, checks how that page ranks for it, and decides whether to add a section, add a page or leave it. You hand back a coverage map per prompt, a short build list that guards against thin pages, and a re-test plan.

> **Romeo's rule:** An engine that asks ten follow-up questions doesn't need ten new pages from you; it needs ten good answers it can find.

## Use this when

- AI answers to a money prompt cite competitors for pricing, integrations, segments or setup questions you have nothing on.
- Your main page is strong, but engines cite other sites for the comparisons, limits or how-to steps around it.
- `ai-search-visibility` found gap prompts and you need to know what content is missing, not just that you're missing.
- Bing grounding queries or long Search Console queries show questions your pages don't answer.
- You're planning content around a product or category and want to cover what engines actually look up, not just the head keyword.

## Don't use this for

- Finding and prioritising the money prompts themselves → `ai-prompt-research`; measuring visibility across engines and the sources they cite → `ai-search-visibility`.
- Rewriting one page passage by passage once you know what it must cover → `ai-citable-pages`.
- Grouping a keyword list into pages and hub-and-spoke clusters by shared results → `topic-cluster-map` (pair it with this skill for every "add a page" decision).
- Planning hundreds of template pages from a dataset → `programmatic-seo-plan`.

## What you need

### Required

- 3 to 10 money prompts: buyer questions where being cited or named leads to sales (from `ai-prompt-research` or an `ai-search-visibility` baseline).
- The site URL and a list of its pages (sitemap, CMS export or `site-content-inventory`).
- Target country and language, and what the business sells to whom.

### Helpful

- Search Console Performance export with query and page (last 3 to 16 months).
- Bing Webmaster Tools AI Performance: grounding queries and cited pages.
- People Also Ask questions for each money prompt and its main variants.
- Current AI answers and citations for the money prompts, with any search steps the engine displayed.
- Keyword volumes from a named tool (estimates; label them `tool`), and conversions by landing page.

### No tools?

Search each money prompt and 2 or 3 variants in Google in a private window set to the right country, expand People Also Ask (each click loads more questions), and note "People also search for". Run the prompt in ChatGPT with search on, Perplexity, Gemini and Google AI Mode, twice each, and note what the answers cover and cite; when an engine shows the searches it ran, copy them and label them `seen`. In Search Console's Performance report, filter Query by custom regex (RE2 syntax) to pull long and question-style searches. Find existing coverage with `site:yourdomain.com` plus the sub-question's key words. A workable minimum: 3 money prompts with 10 to 20 sub-questions each.

## Ground rules

- Fan-out is confirmed but not published. Google says AI Overviews and AI Mode may run "multiple related searches across subtopics and data sources", and OpenAI says ChatGPT search rewrites a prompt into one or more targeted queries and may follow up with more. Neither publishes the searches or how many they run for a given prompt, so your list is a model: label it `inferred` unless you saw the queries.
- Never state "this prompt fans out into N queries" as fact. Observed fan-out queries change from run to run; count how often a sub-question recurs instead.
- Sub-questions are retrieval targets, not page targets. Most belong as a section on a page you already have.
- One URL per intent. Sub-questions served by the same search results and the same reader job share a URL, however differently they're worded.
- Rank first. AI Overview and AI Mode citations come from Google's index, and many cited pages also rank for the searches behind the answer, though a growing share comes from outside the top 10 (Ahrefs, February/March 2026, directional). Check how your mapped page ranks for each sub-question's search.
- No thin or scaled pages. Google's scaled content abuse policy covers many pages made mainly to manipulate rankings with little value to users, however they're produced. Google's guide to optimizing for generative AI features (May 2026) says creating separate content for every search variation, primarily to manipulate rankings or AI responses, violates that policy. A page per sub-question is the quickest way to build exactly that.
- Coverage isn't length. A sub-question is covered by a clear 40 to 80 word answer with the facts, not by 800 more words.
- Some sub-questions are third-party-shaped ("[brand] reviews", "is [brand] legit", "best X"). Engines answer them from other sites, so a page of yours rarely wins; route them to off-site work.
- Judge the work by re-tested citations and mentions over repeated runs, never by how many sub-questions now have a heading.

## Steps

1. **Pick the money prompts.** One row per prompt: wording, the page you want cited, segment, and current state (cited, named, both or neither, from a baseline if one exists). Keep it to 3 to 10 prompts per cycle.

2. **List the likely sub-questions for each prompt.** Aim for 10 to 25 per prompt, written as short searches an engine might run ("acme payroll price per employee"), not as chat prompts.
   - Cover the types: definitions (what is X, what does Y mean); comparisons (X vs Y, X or Y for Z); pricing (cost, plans, free option, fees); alternatives (alternatives to X, cheaper than X); segments (for small teams, agencies, an industry, a country); constraints (works with a platform, compliance, limits, languages, budget); how-to (set up, migrate, do the job); reviews and trust (is X good, X reviews, X complaints).
   - People Also Ask: the questions are `seen`; treating them as fan-out searches is `inferred`.
   - Search Console: long queries are real searches your pages appeared for (`tool`). Example filters: `^\S+(\s+\S+){6,}$` for 7 or more words, `^(how|what|which|why|is|can|does|do|should)\b` for questions. Long, conversational queries often look like the prompts behind AI answers.
   - Bing AI Performance grounding queries: Microsoft describes them as the key phrases the AI used to retrieve content it cited (`tool`, a sample). They show sub-questions you already win, not the ones you're missing, so read them as a pattern of how Copilot phrases its searches.
   - AI answers: the topics, headings and comparison criteria that recur across runs and engines (`inferred`), plus any displayed search steps (`seen`).
   - Watch the modifiers engines add (a year, a segment, "pricing", "reviews", "vs"); they show which facts get checked.
   - Merge near-duplicates, drop what doesn't fit the business, and note how many sources and runs each sub-question appeared in.

3. **Map each sub-question to a URL and section.** Give each one a status.
   - Answered: a section on the right page answers it in a passage that stands alone. Record the URL and the H2 or H3.
   - Partial: mentioned, but no direct answer, or the answer lacks the key fact (price, limit, platform).
   - Buried: the answer exists only in a tab, image, PDF, JavaScript-only widget or a page section with an unrelated heading.
   - Wrong page: answered on a page with a different intent (a pricing answer in a blog post from 2023).
   - Duplicated: two or more of your URLs answer it. Send the pair to `keyword-cannibalization-check`.
   - Missing: nothing on the site answers it.
   - Feed or profile data: for shops and local businesses, price, stock, hours and location sub-questions may be answered from Merchant Center or Business Profile data, which Google's AI features guidance asks you to keep current. Check those before writing page copy.

4. **Check how the mapped page ranks for it.** For each sub-question with a mapped or candidate page, search it in Google (private window, right country) or read Search Console's query and page data.
   - Record: mapped URL in the top 10, 11 to 30, or not found; another of your URLs ranking instead; and which page types fill the top 10 (vendor pages, listicles, forums, docs, video).
   - Note whether an AI Overview appears for that search and which domains it cites (directional; it varies by run and day).
   - If review sites, forums and "best X" lists own the top 10, mark it third-party-shaped and route it to `best-of-list-inclusion` or `reviews-for-ai-answers`.
   - If you have answer data from a tool or the DataForSEO route below, note pages that were retrieved but not cited: the engine found them and passed. That's a passage problem for `ai-citable-pages`, not a coverage gap.

5. **Decide: add a section, add a page, or leave it.** Default to a section.
   - Add a section when the sub-question serves the same reader job as an existing page, or when its top results overlap that page's main query results (use `topic-cluster-map`'s rule: 4 or more shared top-10 URLs means one page; 2 or 3 shared means decide by intent, and default to a section). Partial and buried answers are fixed in place.
   - Add a page only when all of these hold: the sub-question's results differ from every existing page's (0 or 1 shared URLs), it needs a different format or intent (a comparison, an integration setup guide, a calculator, a segment page with a genuinely different offer), it has demand or sales value, and you can say something specific the current results don't (product facts, data, first-hand experience).
   - Leave it when it's a commodity definition you can't improve on (answer in a sentence on the hub and link a good source), when it's third-party-shaped, or when it isn't your business.
   - Thin-page guards: no page per synonym, city or segment unless each has distinct facts, offer or proof; no near-identical templates with nouns swapped; every new page passes "would we publish this if AI engines didn't exist?"; house rule of no more than 3 new pages per money prompt per cycle. More than that is a scale project for `programmatic-seo-plan`.
   - Priorities: `Fix now` for missing or wrong answers to pricing, availability and "does it do Z" sub-questions on money prompts; `Fix next` for comparisons, segments and constraints; `Worth doing` for definitions and how-to that support the journey; `Leave it` with a reason.

6. **Spec each addition.** For every section or page to add, write: the heading in buyer wording, the answer the opening 40 to 80 words must give (naming the business), the facts needed and who confirms them, the evidence to cite, and the internal links in and out. Hand sections to `ai-citable-pages` and new pages to `seo-content-brief`; "vs" and "alternatives" pages go to `comparison-page-writer`.

7. **Use descriptive headings, internal links and one URL per intent.**
   - Headings say what the section answers ("Does Acme work with Xero?"), never "Overview" or "More info". One sub-question per H2 or H3.
   - The money page links to each supporting page with anchor text that names the sub-question's topic, and each supporting page links back. Fragment links (`/pricing#teams`) help readers land on the section; Google treats them as the same URL, so they never count as new pages.
   - New pages are linked from the hub and listed in the sitemap, never orphaned. Linking gaps go to `internal-linking-plan`.
   - Any sub-question answered on two URLs after the changes gets one owner; merge or differentiate the other.

8. **Re-test citations.** Wait until changed pages are recrawled (last crawl date in Search Console URL Inspection; Bing URL Inspection; submit via IndexNow), then repeat the baseline.
   - Run each money prompt 2 to 3 times per engine in clean sessions, same country. Record cited URLs and sections, whether the business is named, and whether the new sections are the ones quoted.
   - Search the top sub-questions in Google again and note AI Overview citations and rankings for the mapped pages.
   - Watch Bing AI Performance for new grounding queries and cited pages, Search Console generative AI impressions by page, and impressions for long queries on the mapped pages.
   - Repeat monthly; call a change real only when it holds across two monthly runs.

## Run it with DataForSEO (optional)

Replaces much of the guesswork in step 2 with fan-out queries observed in real answers, and speeds up step 8. Connect through the official MCP server (`dataforseo-mcp-server`, endpoints called via its `api_request` tool) or plain HTTPS with Basic auth. The manual route above still works without it.

- Observed ChatGPT fan-out: `POST /v3/ai_optimization/chat_gpt/llm_scraper/task_post`.
  - Send `keyword` (the money prompt), location and language, and `force_web_search: true`. Collect with `tasks_ready` and `task_get/advanced`. Run each prompt 3 times.
  - Read `fan_out_queries` (the searches ChatGPT ran), `sources[]` (what the answer cited) and `search_results[]` (everything retrieved). Your URL in `search_results` but not in `sources` is retrieved-but-not-cited (step 4).
  - Count how often each fan-out query recurs across runs and label them `tool`; a query seen once is weak evidence. Check the current docs for whether Gemini scraper results include `fan_out_queries`.
- Pre-collected answers: `POST /v3/ai_optimization/llm_mentions/search_mentions/live`.
  - `platform: "chat_gpt"` (US, English only: `location_code: 2840`, `language_code: "en"`), `target: [{"keyword": "payroll software", "search_scope": ["question"], "match_type": "partial_match"}]`, `limit: 50`, `order_by: ["ai_search_volume,desc"]`.
  - Read `question`, `fan_out_queries[]`, `sources[]` and `ai_search_volume`, then tally the fan-out queries across rows.
  - `"search_scope": ["fan_out_queries"]` instead finds answers whose fan-out searches contain a phrase you care about.
- Question demand: `POST /v3/ai_optimization/ai_keyword_data/popular_questions/live` with `keyword`, `limit` and `order_by` returns questions with `ai_search_volume`. That volume is modelled from search data, not measured inside AI tools; say so in the report.
- Other engines: LLM Responses (`/v3/ai_optimization/chat_gpt/llm_responses/live` and the Claude and Gemini equivalents, with `web_search: true`) also return `fan_out_queries`, but through the model's API, which can answer differently from the consumer app.
- Example cost: 10 prompts × 3 runs via LLM Scraper Standard ≈ $0.04; 5 `search_mentions` calls at `limit` 50 ≈ $0.75. The `popular_questions` price isn't confirmed here, so read it from `user_data` before running.
- Guardrails:
  - Estimate the cost and get the user's OK before any paid call (default cap $2 per run). Check `money.balance` with the free `GET /v3/appendix/user_data` first.
  - Always set `limit`. Use the Standard queue for batches and Live only when the user is waiting.
  - Cache results (30 days for LLM Mentions and AI volume) and sample each prompt at least 3 times.
  - Test new code on `sandbox.dataforseo.com` first. Never print or store the API password.

## What to hand back

Fill in this template. Every decision carries a priority label and an evidence label with confidence.

```markdown
# Query fan-out coverage: [site], [date]

**What I found:** [one line, e.g. "Of 61 likely sub-questions behind 4 money prompts, 19 are answered, 17 partly, 25 missing."]
**What matters most:** [one line, e.g. "Pricing and Xero integration sub-questions are missing, and engines cite competitors for both."]
**What to do first:** [one line]

## Method
- Money prompts: [n]; sources: [People Also Ask | Search Console long queries | Bing grounding queries | AI answers | DataForSEO fan_out_queries]; country/language: [x]; dates: [dates]
- Sub-questions are `inferred` unless marked `seen` or `tool`. Google and OpenAI confirm fan-out happens; neither publishes the searches for a prompt.

## Coverage map: [money prompt]
- [sub-question] - type: [definition | comparison | pricing | alternatives | segment | constraint | how-to | reviews] - seen in: [sources, runs] ([label]) - mapped to: [URL#section | partial | buried | wrong page | duplicated | missing] - ranks: [top 10 | 11-30 | not found | other URL] - decision: [add section | add page | leave it | off-site] - [Fix now | Fix next | Worth doing | Leave it] ([seen | tool | inferred], [high | medium | low])

## Build list
1. [label] Add section "[heading]" to [URL] - covers: [sub-questions] - facts needed: [list] - links: [in/out]
2. [label] New page "[working title]" - own URL because: [distinct results / format] - what it adds that current results lack: [x] - hub: [URL]

## Off-site sub-questions
- [sub-question] - who owns the results: [sites] - route: [best-of-list-inclusion | reviews-for-ai-answers | other]

## Leave it
- [sub-question] - why: [commodity | not our business | already well answered]

## Re-test plan
- Prompts: [list]; engines: [list]; runs: [n]; after recrawl ([dates]), then monthly on [date]
- Success looks like: [e.g. pricing section cited in 3+ of 9 runs; brand named for "for agencies" variant]

## What I could not check
- [item, and what would verify it]
```

## Stop and flag if

- The build list grows past what the business can write and maintain well, or the user wants a page for every keyword, city or segment variant. Stop and route to `programmatic-seo-plan` with the scaled-content warning.
- A sub-question needs claims the business can't support or won't publish (prices, compliance, outcomes). Ask before planning content around it.
- The money page itself isn't indexed or ranks nowhere for its main query. Fix that first (`technical-seo-audit`, `on-page-seo-review`).
- Publishing or editing live pages: draft the sections and briefs, and change the site only with explicit permission.
- Unacceptable output: fan-out queries presented as Google's actual searches without evidence, a stated number of fan-out queries per prompt, invented search volumes, or a build list of near-duplicate pages.

## Next step

- Run `topic-cluster-map` with the sub-questions marked "add a page" and their top-10 URLs, to confirm page boundaries and hub-and-spoke links before anything is written.
- Run `ai-citable-pages` on each existing page that gets new or rebuilt sections.
- Run `seo-content-brief` for each approved new page.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
