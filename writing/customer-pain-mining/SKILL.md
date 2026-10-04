---
name: customer-pain-mining
description: Extract verbatim customer complaints about competitors — the exact wording the founder's product copy should steal, in customers' own words. Use when a founder asks "what do users hate about X?", "what's broken about [category]?", "what's the white space?", or needs raw customer language for landing-page copy, custdev prep, ad copy, or product strategy. Combines Anysite MCP (Reddit broad sweeps, LinkedIn issue-level pain search, YouTube comments under review videos, Twitter for viral pain quotes) with Exa MCP (semantic search for review blog posts, comparison articles, "why I left X" Medium posts). Returns 3–5 pain clusters with 2–3 verbatim quotes each plus a white-space section listing features customers ask for that no competitor ships. Run competitor-discovery first if there's no validated competitor list.
---

# Customer Pain Mining

Competitors at the early stage aren't a threat — they're a **proxy for the customer**. Their unhappy users have already done your custdev calls. This skill harvests them.

The goal is **verbatim wording**, not paraphrase. Founders summarize and lose the gold. Pull exact phrases — they become product copy.

## When this skill applies

- A founder asks what users dislike about competitors or the category
- Preparing custdev calls — you want talking points in the customer's own language
- Writing landing-page copy or positioning — you need real pain wording
- Hunting white-space features competitors aren't shipping
- After `competitor-discovery` — going deeper on the named players

## What you need

1. **Competitor list** — 1 to 5 named competitors (run `competitor-discovery` first if there isn't one)
2. **Niche / category** — one line for context (e.g. "AI writing for students")
3. **Use case for the output** — affects source weighting:
   - Custdev prep → Reddit (long-form verbatim wins)
   - Ad copy → Exa for short blog-post pull-quotes
   - Product strategy → Exa for structured "Pros / Cons" review pages

## Tools

**Anysite MCP**:
- `mcp__claude_ai_Anysite__execute(source="reddit", category="search", endpoint="search_posts", params={...})` — Reddit posts by query (anonymous, viral, long-form).
- `mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_posts", params={"keywords": "<pain-phrase>", "sort": "relevance", "count": 15})` — LinkedIn posts BY professionals describing the pain. Critical: search by the PAIN, not the competitor name (see Step 5).
- `mcp__claude_ai_Anysite__query_cache(cache_key, conditions, ...)` — filter cached results (e.g. `vote_count > 50`).
- `mcp__claude_ai_Anysite__get_page(cache_key, offset)` — paginate.
- `mcp__claude_ai_Anysite__execute(source="youtube", category="video", endpoint="video_comments", params={"video": "<id>", "count": 50})` — comments under a competitor-review YouTube video; people who watched a 15-min review have committed to evaluating the product. Filter `like_count >= 5`. Watch for affiliate astroturf (5+ short identical-tone praises from different accounts).
- `mcp__claude_ai_Anysite__execute(source="twitter", category="search", endpoint="search_posts", params={"query": "<niche+pain>", "min_likes": 5, "count": 20, "language": "English"})` — viral short-form pain quotes. Set `min_likes` ≥ 50 for breakthrough quotes; otherwise filter aggressively for relevance because the query catches handle namesakes (e.g. "Bright" matches users named "Bright").

**Exa MCP** (covers review aggregators and blog content):
- `mcp__claude_ai_Exa__web_search_exa(query, numResults)` — find blog reviews, comparison articles, "why I left X" Medium posts.
- `mcp__claude_ai_Exa__web_fetch_exa(urls)` — pull full review content. Note: Exa fetch on Reddit URLs sometimes returns SOURCE_NOT_AVAILABLE; use the Anysite Reddit endpoint as primary for Reddit content.

Budget: ~8 Anysite executes (3-4 Reddit + 1-2 LinkedIn + 1 YouTube + optional Twitter) + ~5 Exa calls. Reddit, LinkedIn, Exa, and YouTube comments each carry distinct slices of signal — Reddit is anonymous-viral, LinkedIn is identified-professional, Exa is curated review-blog, YouTube comments are evaluation-stage.

## Source mix — pick by segment BEFORE you start

The order of sources depends on where the user lives professionally. Don't run blindly — pick the right primary first:

| Segment | Primary | Secondary | Skip / late |
|---|---|---|---|
| Consumer + EdTech + B2C SaaS | Reddit broad sweep (Step 1) | Exa review blogs (Step 6) | LinkedIn helpful but not primary |
| B2B SaaS sold to professionals (sales tools, marketing, HR) | LinkedIn issue-pain search (Step 5) | Exa fetch of structured review pages | Reddit thinner for these niches |
| Developer tools / DevTool / AI infrastructure | Exa review blogs + LinkedIn issue-pain (parallel) + r/programming / r/LocalLLaMA / r/webscraping / r/AI_Agents | YouTube comments under review videos; Twitter for viral pain | — |
| Mixed (pro-sumer, freelance tools) | Reddit + LinkedIn in parallel | Exa review blogs | — |

Test (3 second check): "Would the typical user of this competitor post their complaint on Reddit (anonymous), LinkedIn (professional reputation), or a developer blog post (technical depth)?" Start with whichever wins.

## How to run

### Step 1 — Reddit category-level pain sweep (start broad) — **consumer / viral-pain niches only**

Counterintuitively, **for niches where pain is broadly viral, a broad query often returns more pain than a negative query.** Reddit's algorithm surfaces high-virality posts; in pain-dominated niches (consumer detector/integrity scandals, broken health products, expensive subscriptions), pain dominates.

`mcp__claude_ai_Anysite__execute(source="reddit", category="search", endpoint="search_posts", params={"query": "<niche> <one descriptor>", "sort": "top", "time_filter": "year", "count": 20})`

For pain-dominant consumer niches (e.g. AI-writing-students), broad queries like `"best AI writing tool college essay"` (sort=top) surface viral pain posts at 20K–48K upvotes describing exactly the product friction you'd otherwise need to dig for. The query is framed as discovery but the algorithm bubbles up frustration.

Pre-check before running this step: Skim the top 5 results' titles. If most are about regulation/ethics/controversy and NOT about product friction, the niche isn't pain-dominant and broad-Reddit-first will mislead. Drop to Step 2 + Step 5 instead. For developer / B2B niches, broad-Reddit-first usually misleads — skip to Step 2 + Step 5 + Step 6.

### Step 2 — Reddit per-competitor sweep

For each named competitor, run ONE single-phrase query. Avoid OR-chains — Reddit's relevance ranking gets confused:

`mcp__claude_ai_Anysite__execute(source="reddit", category="search", endpoint="search_posts", params={"query": "<competitor> <one descriptor>", "sort": "relevance", "time_filter": "year", "count": 15})`

Working query patterns:
- `"<competitor> review"` — review threads
- `"<competitor> <quality complaint>"` — e.g. `"QuillBot paraphrase robotic"` or `"Bright Data expensive failed requests"`
- `"<competitor> <accuracy complaint>"` — e.g. `"Jenni citations hallucination"` or `"Firecrawl credit multiplier"`
- `"<competitor> alternative"` — implicit critique (also surfaces substitute names)

Anti-patterns to avoid:
- OR-chains like `"<competitor> sucks OR broken OR hate OR alternative"` confuse relevance and return off-topic threads.
- Single-phrase queries combining a smaller-brand name with multiple descriptors can return zero results because the smaller brand has a thin Reddit footprint. Start with the most-talked-about competitor first.

For each post, capture: title, subreddit, vote_count, any quotable phrase from the title. Titles are usually the most distilled version of the complaint.

Filter cached results to keep only posts with real engagement (10+ votes for small subs, 50+ for major ones):

```
mcp__claude_ai_Anysite__query_cache(cache_key="<from step 2>", conditions=[{"field": "vote_count", "op": ">=", "value": 10}], sort_by="vote_count", sort_order="desc")
```

### Step 3 — Find the dedicated subreddit

Niche pain often clusters in a single subreddit dedicated to the problem. For AI-writing-detection pain, validation has surfaced `r/BypassAiDetect`, `r/humanizing`, `r/PromptEngineering`. For web-scraping API pain, the recurring subs are `r/webscraping`, `r/WebScrapingInsider`, `r/WebDataDiggers`, `r/Agent_AI`, and `r/LocalLLaMA` (self-host workaround).

If you spot a recurring sub in Step 1–2 results, run one targeted query inside it via title-keyword filtering — though the Reddit endpoint doesn't filter by sub directly, results from that sub float to the top of relevance queries.

### Step 4 — YouTube comments under a top review video

For consumer or DevTool products with strong YouTube review presence, comments under a 10–30K-view "honest review" video are dense pain. People watching a 15-minute review have committed to evaluating the product.

1. `mcp__claude_ai_Anysite__execute(source="youtube", category="search", endpoint="search_videos", params={"query": "<competitor> honest review problems", "count": 10})` — pick 1–2 videos with `view_count >= 5000` and `duration_seconds >= 300`.
2. `mcp__claude_ai_Anysite__execute(source="youtube", category="video", endpoint="video_comments", params={"video": "<id>", "count": 50})`
3. Filter `like_count >= 5`. Watch for affiliate astroturf — 5+ short identical-tone praise comments from different accounts is paid promotion, not signal. Skip the cluster.

Validated on the web-scraping niche: Greg Isenberg's Firecrawl explainer (169K views) returns comments like `"dont use the firecrawl agent, it sucks"` plus free-tier and pricing questions that are themselves a signal.

### Step 5 — LinkedIn issue-pain search (the most underused primitive)

The key insight: Searching LinkedIn by *competitor name* (e.g. `"QuillBot review"`) returns affiliate-marketer spam. Searching by *the pain itself* (e.g. `"Turnitin flagged my essay"`, `"scrapers break every time website changes"`) returns verifiable professionals describing the problem with their names attached.

This is the most underused pain source. LinkedIn pain has a property Reddit doesn't: identity + social proof. A Wharton professor writing "False positives are unavoidable with AI detectors" carries weight anonymous Reddit can't. A founder can @-mention the person to do custdev.

#### Query patterns that work

```
mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_posts",
  params={"keywords": "<pain phrase in domain-professional vocabulary>", "sort": "relevance", "count": 15})
```

Examples that have surfaced high-engagement pain quotes:

- AI-writing niche: `"AI detector false positive student essay"`, `"Turnitin flagged my essay"` — surface Wharton professors, PhDs, undergrads with 65–222 likes describing false-positive pain in their own words.
- Web-scraping API niche: `"scrapers break every time website changes"` — Eric Vyacheslav's Scrapling launch post at **2,045 likes**, the single highest-engagement pain quote in the niche.
- B2B SaaS niche: `"<pain in professional vocabulary>"` — search by the verb of the pain ("manually copying from website to spreadsheet"), not the product name.

#### Query patterns that don't work

- `"Grammarly frustrating problem"` → mostly generic frustration posts, not Grammarly-specific (10/10 noise).
- `"QuillBot review"` → affiliate marketing posts ("I made $4200 with QuillBot"), not pain.
- `"<competitor> alternative"` → promotional content from competing vendors.

Why: LinkedIn rewards branded posts that drive engagement — affiliates and brand content rank above complaints under product-name queries. Reddit is the opposite. On LinkedIn, search by the *problem*, not the *product*.

#### How to filter

Use `query_cache` to keep only posts with engagement (reactions[0].count >= 5) and pull from the result. The first reaction in the array is usually "like" with the highest count.

#### Bonus filter: by `author_industries` or `author_title`

If your niche has a clear professional audience, add `author_industries` (e.g. "Education", "Higher Education", "Marketing and Advertising", "Information Technology and Services") or `author_title` (e.g. "Professor", "Marketing Director") to narrow to in-domain voices.

### Step 6 — Exa: review blog posts (verbatim quote goldmine)

This is where the highest-density verbatim quotes live. Describe the ideal review post:

`mcp__claude_ai_Exa__web_search_exa(query="<competitor> honest review complaints — what's frustrating about it — <audience> blog post", numResults=6)`

A well-targeted query typically surfaces 6 review posts in one call, each with 5–10 pull-quote complaints. The Exa snippets often contain the quote directly — you may not even need to fetch. If you need more context, fetch:

`mcp__claude_ai_Exa__web_fetch_exa(urls=["<top 2 review URLs>"])`

Validated on the web-scraping niche: `"honest review of Firecrawl Bright Data Apify web scraping API — what's frustrating about pricing and reliability — developer blog post"` returned 8 review blogs with structured Pros/Cons including the verbatim ScrapeGraphAI breakdown: *"Firecrawl's credit multipliers make the real cost 5-7x higher than the headline numbers suggest for AI extraction workloads."*

### Step 7 — Exa: "why I left" / churned-user posts

Long-form pain from people who actively quit:

`mcp__claude_ai_Exa__web_search_exa(query="why I stopped using <competitor> — switched to alternative — frustrated user blog post", numResults=5)`

Churned-user posts are gold for product strategy because the user has already articulated their next-best alternative and the specific reason they left.

### Step 8 — Cluster the pain

Read everything. Group into **3–5 themes**. Themes should be distinct (don't merge "buggy" with "expensive"). For each theme:

- 3–6 word name (e.g. "AI-detector false flags ruin grades")
- **2–3 verbatim quotes**, with quotation marks. Cite source: subreddit + post title + vote_count, OR LinkedIn name + headline + reactions, OR blog URL.
- 1-line **trigger** — what causes the complaint (specific feature, pricing change, competitor release)
- 1-line **workaround** users describe — often the seed of a feature idea
- (optional) **Cross-platform signal**: if pain appears on Reddit AND LinkedIn AND Exa-blogs, that's a strong validated pattern — call it out.

### Step 9 — Identify white space

The single most valuable output: what users **ask for** that no competitor ships. Re-scan everything for phrases:

- "I wish X did Y"
- "If only..."
- "Why doesn't anyone..."
- "I would pay for..."
- "I built my own script to..."

Pull these separately. Each is a candidate feature with proven demand. Even 1–2 quotes here is gold.

## Output

Markdown report, ~600–900 words:

```
# Pain Mining — <Niche / Product>

## Executive summary
3 sentences: the dominant pain theme, the most-asked-for-but-missing feature, the one quote the founder should pin to the wall.

## Pain clusters

### 1. <Theme name> (most common)
- "<verbatim quote>" — r/<subreddit>, "<post title>" (<N> votes)
- "<verbatim quote>" — blog: <URL>
- "<verbatim quote>" — r/<subreddit>, "<post title>"

**Trigger:** <1 line>
**Workaround:** <1 line>

### 2. <Theme name>
[same pattern]

### 3. <Theme name>
[same pattern]

## White space (asked for, not shipped)
- "<verbatim quote>" — <source>
- "<verbatim quote>" — <source>

## Recommendations
- Landing-page copy line the founder could literally use
- Custdev question to validate the dominant pain
- One product gap worth exploring
```

## Quality bar

- **Verbatim only.** If you can't find a real quote, mark the cluster "weak evidence" and move on.
- **At least 2 quotes per cluster.** One quote is anecdote; two is pattern.
- **Cite every quote.** The founder must be able to validate it themselves.
- **Don't editorialize.** "Users find onboarding frustrating" is paraphrase. "I spent 3 hours trying to import my data" is the real thing.
- **Filter astroturf.** If a "complaint" is suspiciously polished and links to a competitor's homepage in the same paragraph, skip it.

## Don't

- Don't fabricate quotes. Ever. If signal is thin, return fewer clusters.
- Don't exceed ~8 Anysite calls + ~6 Exa calls.
- Don't rank-order pain by your judgment — order by engagement (vote count, reactions).
- Don't bury white space at the bottom — it's often the single most valuable section.
- Don't write paragraphs. Quotes + 1-line annotations only.
- Don't use Reddit OR-chains (`A OR B OR C OR D`) — confuses ranking. Single-phrase queries only.
- Don't search LinkedIn by competitor name (`"QuillBot review"`, `"Grammarly frustrating"`) — that returns affiliate spam. Search by the pain itself (`"Turnitin flagged my essay"`, `"scrapers break every time website changes"`).
- Don't run Twitter without aggressive engagement filters. `min_likes` ≥ 5 catches namesake-handle noise (e.g. `"Bright Data"` matches users whose handle starts with `bright_`); for breakthrough quotes set ≥ 50 and skim manually.
- Don't try to use the Anysite `g2` source for verbatim reviews — only `g2/search/search` is exposed and it returns category listings without Pros/Cons content. For G2-style review depth, use Exa to fetch the actual G2 page URL or use the Exa-for-review-blogs pattern in Step 6.
- Don't blindly run Step 1 (broad-Reddit-first) for B2B / DevTool niches — professionals don't vent on r/mildlyinfuriating. Start with Step 5 (LinkedIn) + Step 6 (Exa) for B2B / DevTool.
- Don't expect GitHub issue mining via Anysite right now — the GitHub source is registered but its categories are not currently exposed via this MCP. For dev-tool pain mining on GitHub issues, use Exa to fetch the specific GitHub issues page.

## Example session — Anysite

Input: "Pain mining for Anysite (web scraping / data extraction API for developers + AI agents). Competitors: Apify, Bright Data, Firecrawl, ScrapingBee. Use case: landing page copy."

Segment check: DevTool + B2B-leaning niche → start with Step 5 (LinkedIn issue-pain) + Step 6 (Exa review blogs) in parallel, add Reddit per-competitor for cross-validation.

```
1. mcp__claude_ai_Anysite__execute(reddit/search/search_posts, query="Bright Data alternative expensive", sort="relevance", time_filter="year", count=20)
   → "Bright Data is getting too expensive for failed requests" thread in r/WebScrapingInsider. Direct pricing-pain evidence.

2. mcp__claude_ai_Anysite__execute(reddit/search/search_posts, query="Apify pricing expensive credits", count=15)
   → r/B2BLeadGenPro Apify-cost-math thread; r/automation competitor-prices-without-code thread.

3. mcp__claude_ai_Anysite__execute(reddit/search/search_posts, query="scraper breaks website changed maintenance", count=15)
   → "Why CSS selectors are becoming obsolete" (r/WebDataDiggers); "The self-healing scraper: A practical guide" (r/WebDataDiggers).

4. mcp__claude_ai_Anysite__execute(linkedin/search/search_posts, keywords="scrapers break every time website changes", count=15)
   → Eric Vyacheslav's Scrapling launch post (2,045 likes) — the single highest-engagement pain quote: "Most scrapers break the moment a website changes a class name or rolls out anti-bot protection." Plus Rohit Patil (8 likes): "We've spent two decades building scrapers that break every time a website changes." Plus Mark M. (Firecrawl, 40 likes): "Your web scraper is dead."

5. mcp__claude_ai_Anysite__execute(linkedin/search/search_posts, keywords="web scraping rate limit blocked frustrated", count=15)
   → Matthew Scott Goldstein (20 likes) structured 7-bullet pain post: "Sites fight back. CAPTCHAs everywhere. Websites change constantly." Plus DataDome's own admission: "Only 7% of websites successfully block advanced anti-fingerprinting bots."

6. mcp__claude_ai_Anysite__execute(youtube/video/video_comments, video="eH8JdttKIdA", count=30)
   → Greg Isenberg Firecrawl explainer (169K views). Genuine: "dont use the firecrawl agent, it sucks." Plus pricing/free-tier questions confirming the cost concerns surfaced in Step 1.

7. mcp__claude_ai_Exa__web_search_exa(query="honest review of Firecrawl Bright Data Apify web scraping API — what's frustrating about pricing and reliability — developer blog post", numResults=8)
   → 8 review blogs. Verbatim pull-quotes: ScrapeGraphAI's Firecrawl pricing breakdown: "Firecrawl's credit multipliers make the real cost 5-7x higher than the headline numbers suggest." "If Firecrawl attempts a request and it fails mid-way, you may still lose credits."

8. mcp__claude_ai_Exa__web_fetch_exa(urls=["scrapegraphai.com/blog/firecrawl-pricing", "architjn.com/blog/apify-vs-bright-data-vs-firecrawl-honest-comparison-2026"]) — full verbatim for cluster 2.

9. mcp__claude_ai_Anysite__query_cache(cache_key="<step 4>", conditions=[{"field": "reactions[0].count", "op": ">=", "value": 100}], sort_by="reactions[0].count", sort_order="desc") → keep top viral pain posts.

10. Synthesize.
```

Output clusters:

### 1. "Scrapers break every time the website changes — endless maintenance" (dominant — 2,000+ aggregated LinkedIn likes; cross-platform)
- "Most scrapers break the moment a website changes a class name or rolls out anti-bot protection." — Eric Vyacheslav, LinkedIn, 2,045 likes
- "I've watched good engineers spend 3 days building scrapers that break in a week." — Sarisha Jaitly, AERIX, LinkedIn, 26 likes
- "We've spent two decades building scrapers that break every time a website changes: brittle selectors, endless maintenance, constant retries." — Rohit Patil, LinkedIn, 8 likes
- "Hot take: web scraping isn't dead. Your web scraper is. The old way: write a Python script, hardcode CSS selectors, pray the site doesn't update, it updates, spend your weekend fixing it, repeat forever." — Mark M., Firecrawl, LinkedIn, 40 likes

**Trigger:** Target site ships a CSS/markup change. Brittle selectors collapse. Pipeline silently breaks; team discovers it via downstream data quality alerts.
**Workaround:** Patch selectors weekly, or pay a managed API to absorb the cost, or hire someone to maintain 14 scripts who then quits.

### 2. "Pricing surprises: credit multipliers, failed-request charges, rate-limit throttling at scale"
- "Firecrawl's credit multipliers make the real cost 5-7x higher than the headline numbers suggest for AI extraction workloads." — Marco Vinciguerra, ScrapeGraphAI blog (Mar 2026)
- "If Firecrawl attempts a request and it fails mid-way (timeout, server error, JS rendering failure), you may still lose credits. On flaky target sites, you can burn 20-30% more credits than expected." — same blog
- "Bright Data is getting too expensive for failed requests." — r/WebScrapingInsider thread title
- "the extra cost is 17x more expensive than getting a google SERP from bright data" — @andersonbcdefg, X (Twitter), 17 likes

**Trigger:** Team scopes a 50K-page extraction at the headline rate, launches it, discovers credits burning 5x faster than expected.
**Workaround:** Pair tools (Firecrawl crawl + ScrapeGraphAI extract) — explicitly recommended in 2 separate cost blogs.

### 3. "AI agents need the web, but the web wasn't built for them"
- "AI agents are only as good as the data they can access. That's the bottleneck most teams hit — not the model, not the prompt. The data pipeline." — Li Chen (Octoparse PM), LinkedIn
- "Bright Data are centralized, expensive, and designed for enterprise buyers managing web dashboards. AI agents can't use web dashboards." — @spacecoin, Twitter, 21 likes, 13K views
- "The next wave of internet users will be AI agents, but our current web infrastructure is designed purely for human clicks." — Abdulrahman Ibn-Sa'eed, LinkedIn

**Trigger:** Founder builds an AI agent. Discovers existing scraping vendors assume a human operator on a dashboard.
**Workaround:** Use the only major vendor positioned "for AI" from day one (Firecrawl) and absorb the credit-multiplier tax — or stitch together Tavily + Crawl4AI + custom infra.

## White space (asked for, not shipped)

- "I wish [the vendor] didn't charge me for failed requests." — explicit Reddit thread title + multiple blog complaints
- "I want one credit per call, no multipliers, no surprises." — Marco Vinciguerra, ScrapeGraphAI blog
- "I want to describe what I need in plain English and have the platform pick the endpoints + estimate cost *before* running." — implied by Sarisha Jaitly's AERIX pitch and Anysite's own demo flow

## Recommendations

- **Landing-page copy:** "The web scraping API that doesn't charge you for failed requests, doesn't ship credit multipliers, and self-heals when sites change layout."
- **Custdev question:** "Tell me about the last time your scraper broke at 3 AM. What did it cost you to fix? What would a tool need to do to keep that from happening again?"
- **Product gap:** A "no surprises" pricing dashboard that shows credit estimate + failure-budget *before* running a crawl.
