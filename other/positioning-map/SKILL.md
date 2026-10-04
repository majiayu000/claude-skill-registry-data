---
name: positioning-map
description: Build a positioning map for 3–5 competitors and identify the empty quadrant the founder could own. Use when a founder asks "where's the positioning gap?", "how do I position against X?", "what's the competitive landscape look like on hero / pricing / hiring / customers?", or needs a structured comparison before a launch, repositioning, or fundraise. Combines Anysite MCP (LinkedIn company entity + post search + jobs search; SEC for late-stage) with Exa MCP (fetch JS-heavy SaaS marketing pages, find case studies and changelogs). Returns a comparison table across 5 axes (hero / pricing / specialities / recent shipping / hiring), 3 candidate positioning moves with explicit choice criteria, and a one-sentence positioning statement. Requires customer pain themes as input — positioning without pain context is just rearranging marketing copy. Run competitor-discovery and customer-pain-mining first if you don't have a curated competitor list + pain themes.
---

# Positioning Map

Positioning isn't marketing copy — it's a **product decision about who you say no to**. This skill makes that choice visible by mapping competitors on 5 signal axes, locating the empty space, and forcing you to pick between 3 candidate moves rather than defaulting to the first one that sounds good.

Founders consistently underweight four things on competitor positioning: hero copy is the most-curated surface (so trust it least), pricing reveals who they actually sell to, what they ship reveals what they think matters, and **who they hire reveals where they're going next quarter** (the leakiest signal of all). Customer logos reveal who they actually catch, which often contradicts who they pitch.

## Frameworks this skill draws from

This skill is the operational version of three positioning frameworks, executed against real public data:

1. **April Dunford — *Obviously Awesome* (5 components):** competitive alternatives, unique attributes, value (and proof), target market characteristics, market category. Dunford's #1 insight: **start with competitive alternatives, not with what you do.** This skill operationalizes that by always grounding "the empty quadrant" against the actual competitor set, not against an abstract market.
2. **Geoffrey Moore — *Crossing the Chasm* (positioning statement template):** "For [target customer] who [need], the [product] is a [category] that [benefit]. Unlike [primary alternative], our product [primary differentiation]." This is the format of the deliverable — the one-sentence positioning move.
3. **Ries & Trout — *Positioning: The Battle for Your Mind* (mental real-estate):** you can only own ONE word/concept in the customer's mind. The "empty quadrant" framing inherits from this: the position you can own is the one nobody else is claiming AND that customers care about.

Adjacent frameworks worth knowing but not directly encoded here: **Treacy & Wiersema's three value disciplines** (product leadership / operational excellence / customer intimacy — pick one, do the others adequately) and **Ulwick's outcome-driven JTBD** (positioning aligned to unmet desired outcomes). If the founder uses these in their own thinking, fold them into the axis choices.

## When this skill applies

- Founder asks where the positioning gap is
- Pre-launch — choosing what to say no to
- Pre-fundraise — proving positioning is defensible
- Post-`customer-pain-mining` — synthesizing what you found with what competitors actually claim

## What you need (inputs)

1. **3–5 competitors with URLs** — fewer than 3 isn't a map; more than 5 is noise.
2. **The job-to-be-done** — one line. Without it, "axis" has no meaning.
3. **Customer pain themes — REQUIRED, not optional.** Output from `customer-pain-mining`. Positioning without pain context is just rearranging marketing copy. The gap lives where pain ≠ competitor claims. If the founder hasn't run pain-mining, refuse to produce a positioning sentence — produce only a descriptive map and flag this in the executive summary.
4. **(Optional) Founder's current positioning** — if doing a repositioning exercise.

If you don't have item 1, run `competitor-discovery`. If you don't have item 3, run `customer-pain-mining` first.

## Tools

**Exa MCP** (primary for axes 1, 2, 4 — modern SaaS marketing sites are JS-rendered SPAs):
- `mcp__claude_ai_Exa__web_fetch_exa(urls)` — pull homepage / pricing / customers / changelog pages. Batch multiple URLs per call.
- `mcp__claude_ai_Exa__web_search_exa(query, numResults)` — find case studies, changelog blogs, "X review" comparison posts.

**Anysite MCP**:
- `mcp__claude_ai_Anysite__execute(source="linkedin", category="company", endpoint="company", params={"company": "<alias>"})` — company entity + URN + employee count + specialities[] + short_description.
- `mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_posts", params={"keywords": "<competitor> <category>", "date_posted": "past-month", "count": 10})` — what they're posting and what's being said about them in the last month. Use this for the "recent shipping" axis; it covers the same ground as `linkedin/company/company_posts` but with richer engagement filtering via `query_cache`.
- `mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_jobs", params={"keywords": "<competitor>", "count": 20})` — open roles. Filter response by `company.alias` matching the actual target (keyword search can catch namesakes — e.g. a keyword search for one competitor may return a different competitor's roles that mention it in the JD).
- `mcp__claude_ai_Anysite__execute(source="sec", category="search", endpoint="search_companies", params={"entity_name": "<competitor>", "forms": ["10-K","S-1","D"], "count": 5})` — only for late-stage / public competitors. For early-stage consumer SaaS, returns nothing useful.
- `mcp__claude_ai_Anysite__execute(source="webparser", category="parse", endpoint="parse", params={...})` — only for static-HTML competitor sites. Modern SaaS marketing pages (Next.js / Vercel) return empty; use Exa instead.

Budget: ~3 Anysite calls per competitor (LinkedIn company + post search + jobs search) + ~2 Exa fetches per competitor. For 5 competitors: ~15 Anysite + ~10 Exa.

## How to run

For each competitor, run the same 5 axes. Capture as a row in a growing table.

### Axis 1 — Hero copy (who they pitch)

`mcp__claude_ai_Exa__web_fetch_exa(urls=["https://<competitor>.com"])`

Extract: H1 headline, sub-headline, the verb (build / write / cite / extract / scrape / etc.), explicit audience callout if any ("for academic researchers," "for indie devs," "for teams 10–500", "for AI agents").

Validated on the web-scraping niche: a single batched Exa fetch on `["brightdata.com", "apify.com", "firecrawl.dev", "scrapingbee.com", "anysite.io"]` returns hero + subhead + pricing summary + customer-logo trust bar for all 5 competitors in one call. The hero is the most curated surface — trust it least for "what the product actually does" and most for "who the company is currently pitching."

Webparser tends to fail on JS-rendered SPAs (Next.js / Vercel marketing sites) — Exa fetch is the reliable primary.

### Axis 2 — Pricing (who they actually sell to)

`mcp__claude_ai_Exa__web_fetch_exa(urls=["https://<competitor>.com/pricing"])`

If `/pricing` returns `CRAWL_NOT_FOUND` (it sometimes does for Next.js sites), the pricing is usually on the homepage from Axis 1 — search for "$" in the body text.

Extract: tier names, lowest paid tier (in $), highest published tier, gating (seats / usage / features / credits). Convert everything to monthly USD for comparability. The lowest tier reveals their floor; the highest reveals ambition.

Web-scraping API niche pricing spread (validated): Firecrawl $0 → $16 Hobby → $83 Standard → $333 Growth (credit-based, 5x multiplier on extract). Apify $5 free → $49 Starter (compute-unit). Bright Data product-by-product: Crawl $1/1K req; Unlocker $1/1K; Browser API $5/GB; Web Scraper $0.001/record; effective $499/mo for 510K records. ScrapingBee $49/mo Freelance → $99 Startup → $599 Business+. The whole category is in pricing turmoil — the dominant pain in `customer-pain-mining` is the credit-multiplier surprise, so the pricing axis has positioning leverage right now.

### Axis 3 — LinkedIn company entity (the org's verbatim self-positioning)

`mcp__claude_ai_Anysite__execute(source="linkedin", category="company", endpoint="company", params={"company": "<alias or website-derived alias>"})`

Returns: `short_description`, `description`, `employee_count`, `founded_on`, `specialities[]`, `headquarter_location`.

What to extract:
- `short_description` — often a single positioning sentence the company curates for LinkedIn (different from their homepage hero — useful contrast).
- `specialities[]` — explicit, comma-separated list of what they claim to do. Rare verbatim self-positioning. In Dunford's terms, this is their stated "unique attributes" list.
- `employee_count` — sets the stage size (e.g. Bright Data=355, Apify=231, Firecrawl=48, ScrapingBee=17).
- `founded_on` — for stage context.

Validated on the web-scraping niche: Bright Data's `specialities[]` is 13 terms long, dominated by use-cases (price intelligence, brand monitoring, market research, AI Agents). Apify's is 8 terms, platform-shaped ("Web scraping, Browser automation, AI agents, API integration, Data pipelines, No-code tools, Actor marketplace, Developer platform"). Firecrawl + ScrapingBee both ship empty `specialities[]` (small pages, content-marketing-led) — that absence is itself a signal.

Skip `company_employee_stats` for competitors under ~200 employees — the endpoint returns empty arrays for small organizations.

For the "what did they ship lately" axis, prefer `linkedin/search/search_posts` from Axis 4 over `linkedin/company/company_posts` because Axis 4's keyword + `mentioned[]` filter gives richer engagement-based filtering via `query_cache`.

### Axis 4 — Recent shipping / signal (what they think matters now)

What did they ship or signal in the last 30 days?

`mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_posts", params={"keywords": "<competitor name> <category keyword>", "sort": "recent", "date_posted": "past-month", "count": 10})`

Filter for signal — many results will be SEO listicles. Keep posts where (a) the author is the company itself (mentioned[] contains the company), or (b) `comment_count + sum(reactions[].count) >= 10`. Use `query_cache`.

Alternative: Exa for changelogs / feature blog posts:

`mcp__claude_ai_Exa__web_search_exa(query="<competitor> new feature release 2025 — changelog blog post — what's new", numResults=5)`

Then fetch the top URL if promising. Some products have explicit `/changelog`, `/whats-new`, `/blog` pages.

What to extract: count feature-release posts vs customer-story posts vs marketing posts in the last 30 days. The ratio tells you the company's stage and what they think the buyer cares about.

Validated on the web-scraping niche: Firecrawl ships fastest on AI-agent affordances (Onboarding-Skill flow, CLI launch, MCP server, "Highlights and Question formats are now live"). Bright Data ships compliance/enterprise content (DataDome partnership, Web MCP "now free"). Apify ships marketplace breadth (native MCP highlight, Creator Growth program, LangChain/n8n integrations). The recent-shipping axis reveals which company believes the buyer cares about which thing this quarter.

### Axis 5 — Hiring signal (where they're going next quarter)

`mcp__claude_ai_Anysite__execute(source="linkedin", category="search", endpoint="search_jobs", params={"keywords": "<competitor name>", "count": 20})`

Hiring is the leakiest competitive signal. Companies can curate hero copy, hide pricing, lawyer up customer logos. They cannot hide that they just opened 5 enterprise sales reqs.

What to extract: count of open roles filtered by `company.alias` matching the actual target (keyword search can catch namesakes — a keyword search for one competitor can return roles at another company that mentions it in the JD). Then group by function:

- Eng / AI / R&D → product surface expansion incoming
- Growth / Performance Marketing / SEO → optimizing the paid funnel; scaling existing model
- Enterprise Sales / AE / Customer Success → moving upmarket
- Partnerships / Channel / Solutions → going institutional / channel-led
- Product Marketing / Product Enablement → revenue-stage execution, not net-new product
- Developer Relations / Creator Growth → developer-ecosystem / platform play

The function MIX, not the count, is the signal. Validated on the web-scraping niche: Bright Data has 20+ open roles skewed Enterprise Sales (Overlay Sales Director, AI Account Executive UK, BDR NYC) + CS + global Solutions Architects → scaling enterprise GTM + global presence. Apify has 20+ skewed developer-platform (Senior Backend for proxy/unblocking, Fraud Prevention Eng, Product Marketing, Creator Growth Lead) → scaling developer + creator/Actor-publisher side. Firecrawl shows 0 results on LinkedIn jobs → small (~48 employees) and content-marketing-led, not hiring publicly. ScrapingBee shows 1 (Sr PM Vilnius) → stable, lean.

Mark "no signal" for very-small competitors (< ~30 employees) or content-marketing-led teams — absence of LinkedIn jobs isn't absence of hiring, it's absence of public hiring. Don't fabricate; mark explicitly and move on.

### Axis 6 (skip unless asked) — Customer logos / case studies

Often a separate page (`/customers`, `/case-studies`), often on the homepage scroll. The Exa fetch from Axis 1 usually catches it.

Note the mismatch between hero pitch and customer logos. If the hero pitches one audience but the customer logos show a different audience, that mismatch is often where the positioning gap is.

If logos aren't on the homepage:
`mcp__claude_ai_Exa__web_search_exa(query="<competitor> customer case study OR testimonial 2024 2025 — <industry or audience>", numResults=5)`

### Axis 7 (skip unless competitor is public / late-stage) — SEC filings

`mcp__claude_ai_Anysite__execute(source="sec", category="search", endpoint="search_companies", params={"entity_name": "<competitor>", "forms": ["10-K","S-1","D"], "count": 5})`

Only meaningful when the competitor has filed (e.g. Grammarly has Form D filings under CIK 0002033975). Returns canonical positioning language they've committed to in legal filings — rigid, lawyered, but unedited.

For early-stage / private consumer SaaS this returns nothing useful. Skip.

### Synthesize — the positioning table

Build a markdown table with axes × N competitors + the founder's own product as the last column. The point of including yourself is to make the gap visible relative to where you stand now.

### Cross-reference with pain themes (the load-bearing step)

This is what makes positioning real rather than wishful: only positions that map onto a top-3 customer pain theme are worth considering. Take the pain themes from `customer-pain-mining` and rank them by signal density (upvotes, reactions, mention count). For each empty quadrant you spot in the table, check: is there a pain theme that backs this position? If no, drop it.

Validated on the web-scraping niche: the top pain theme was "scrapers break every time the website changes" (2,045-like LinkedIn launch post for Scrapling + cross-platform Reddit + Exa-blog confirmation). The empty quadrant "agent-native + predictable pricing" maps directly onto this pain combined with the credit-multiplier complaints from cluster 2. That alignment is what makes the move defensible.

### Generate three candidate positioning moves (not one)

April Dunford's empirical observation: founders who write ONE candidate positioning statement default to the first one that sounds good. The fix is to write 3 and force a choice. For each candidate, use Moore's template:

> "For [target customer] who [need], [product] is a [category] that [benefit]. Unlike [primary alternative], our product [primary differentiation]."

Pick 3 candidates that genuinely differ on **competitive alternative** (per Dunford). Concretely:
- **Candidate A** — position against the obvious primary competitor.
- **Candidate B** — position against the "do nothing / DIY" alternative.
- **Candidate C** — position against a category-adjacent tool (something not in the named competitor set but that customers actually use).

For each candidate, evaluate on 3 criteria:
1. **Pain coverage** — does it map to a top-3 pain theme from `customer-pain-mining`?
2. **Defensibility** — does the founder have a structural advantage to hold this position (data, team, integrations, customer base)? Or is it just marketing copy?
3. **Empty-quadrant evidence** — how many of the 5 axes show this position as unclaimed?

Score each 1–3, pick the highest total. State why the other two lose. **Show the work.**

## Output

Markdown report, ~900–1100 words:

```
# Positioning Map — <Niche>

## Executive summary
3 sentences: dominant positioning pattern, the empty quadrant the founder could own, the single positioning move that creates the most contrast (the WINNER of the candidate-3).

## Comparison table

|  | <Competitor A> | <Competitor B> | <Competitor C> | <Your product> |
|---|---|---|---|---|
| **Hero copy** | "..." (verbatim H1) | "..." | "..." | "..." |
| **Pricing floor / ceiling** | $X / $Y per mo | ... | ... | ... |
| **LinkedIn specialities (top 3)** | A, B, C | ... | ... | ... |
| **Last 30 days shipped** | 3 features + 2 case studies | 1 feature + 5 SEO posts | ... | ... |
| **Hiring (function mix)** | 4 Eng / 2 Sales / 1 CS — moving upmarket | "no signal" (early-stage) | ... | ... |

## The empty quadrant
1–2 paragraphs naming the position no one currently occupies. Quote evidence from at least 2 of the 5 axes AND tie it to a named pain theme from `customer-pain-mining`.

## The three candidates (and why this one wins)

**Candidate A — vs primary competitor:**
> "<Moore template>"
Pain coverage: X/3. Defensibility: Y/3. Empty-quadrant evidence: Z/5 axes. Total: X+Y+Z.

**Candidate B — vs do-nothing / DIY:**
> "<Moore template>"
Pain coverage: ... Defensibility: ... Empty-quadrant evidence: ... Total: ...

**Candidate C — vs category-adjacent:**
> "<Moore template>"
Pain coverage: ... Defensibility: ... Empty-quadrant evidence: ... Total: ...

**Winner: <A | B | C>** because <one sentence per losing candidate explaining why it's weaker>.

## So what
- Hero-copy change to try
- One feature to ship that signals the new position
- One customer segment to pursue first
```

## Quality bar

- **Cite evidence** for each cell. "Hero: 'fastest browser automation' — homepage H1" beats "Hero: speed-focused."
- **Convert pricing to monthly USD.** Don't let one competitor's "annual / per seat" obscure the comparison.
- **Distinguish what they say from what they do.** Hero vs. customers vs. recent shipping vs. hiring — these often contradict each other; the contradiction is the gap.
- **The empty quadrant must be defendable AND pain-backed.** "Nobody is cheapest" is not a strategy unless you have a structural cost advantage. "Nobody serves writing centers" is a strategy only if you have evidence writing centers are buyers (pain theme + founder relationship/data).
- **Show three candidate positionings, not one.** A single sentence picked first means you skipped the comparative step that makes the choice defensible.
- **The hiring axis confirms or denies the other four.** If hiring says "everyone is going enterprise" but hero copy says "we love students" — the hiring is right and the hero is lagging. Use this as a sanity check.

## Don't

- Don't include more than 5 competitors. The table becomes noise.
- Don't paraphrase hero copy — quote it. Exact wording is the unit of analysis.
- Don't rate competitors qualitatively (good/bad). The map is descriptive.
- Don't pick the "cheapest" gap unless cost is structural.
- Don't pick a position that doesn't map to a real pain theme. That's marketing fiction.
- Don't write a single positioning sentence without showing the 2 alternatives you considered and rejected.
- Don't run `webparser/parse` on modern SaaS marketing sites — they're JS SPAs. Use `mcp__claude_ai_Exa__web_fetch_exa`.
- Don't run `linkedin/company/company_employee_stats` for competitors under ~200 employees — returns empty arrays.
- Don't pass `company` URN as filter for `linkedin/search/jobs` — URN filtering is often too literal for subsidiary brands (e.g. a product brand often sits under a parent-company URN). Use `keywords` and filter the response by `company.alias`.
- Don't trust `linkedin/search/jobs` for very-early-stage or content-marketing-led competitors (< ~30 employees or zero jobs returned). Absence of public roles isn't absence of hiring. Mark "no signal" — don't fabricate.
- Don't trust `similar_organizations[]` on the LinkedIn company endpoint — noisy for small companies. Use `linkedin/search/search_companies` results instead.
- Don't run `sec/search/search_companies` for early-stage private competitors — returns nothing meaningful. Reserve for late-stage / public.
- Don't bury the positioning sentence. It's the deliverable — put it in the executive summary too.
- Don't use the Anysite `g2` or `crunchbase` sources for positioning data — `g2/search/search` returns category listings only (no per-product Pros/Cons), and `crunchbase` categories aren't currently exposed via this MCP. For G2 / Crunchbase content, fetch the specific page via Exa.

## Example session — Anysite

Input: "Positioning map for Anysite — API-first web data platform with 40+ sources + MCP server for AI agents. Competitors: Bright Data, Apify, Firecrawl, ScrapingBee. Pain themes from `customer-pain-mining`: (1) scrapers break every time the website changes — 2,045-like Scrapling launch post; (2) credit-multiplier pricing surprises + failed-request charges; (3) AI agents need the web but vendors assume a human dashboard operator."

For each competitor: 1 Exa fetch (homepage) + 1 Anysite linkedin/company + 1 Anysite linkedin/search/posts + 1 Anysite linkedin/search/jobs. ~4 calls × 4 competitors = 16 calls (in practice batched to ~10 because Exa batches multiple URLs in one call).

```
1. mcp__claude_ai_Exa__web_fetch_exa(urls=["https://brightdata.com/", "https://apify.com/", "https://firecrawl.dev/", "https://scrapingbee.com/", "https://anysite.io/"])  ← single batched call
2. mcp__claude_ai_Anysite__execute(linkedin/company/company, company="bright-data")   → 355 employees; 13-term specialities
3. mcp__claude_ai_Anysite__execute(linkedin/company/company, company="apify")          → 231 employees, founded 2016; 8-term specialities
4. mcp__claude_ai_Anysite__execute(linkedin/company/company, company="firecrawl")      → 48 employees; empty specialities (content-marketing-led)
5. mcp__claude_ai_Anysite__execute(linkedin/company/company, company="scrapingbee")    → 17 employees, Paris; empty specialities
6. mcp__claude_ai_Anysite__execute(linkedin/search/search_posts, keywords="Firecrawl Bright Data web scraping", count=25) → 50-like AI-consensus post + recent shipping signal
7. mcp__claude_ai_Anysite__execute(linkedin/search/jobs, keywords="Bright Data", count=20)   → 20+ roles, heavy Enterprise Sales
8. mcp__claude_ai_Anysite__execute(linkedin/search/jobs, keywords="Apify", count=20)         → 20+ roles, developer-platform-heavy
9. mcp__claude_ai_Anysite__execute(linkedin/search/jobs, keywords="Firecrawl", count=15)     → 0 (small + content-marketing-led)
10. mcp__claude_ai_Anysite__execute(linkedin/search/jobs, keywords="ScrapingBee", count=15)  → 1 (Sr PM Vilnius)
11. mcp__claude_ai_Exa__web_search_exa(query="Apify Bright Data Firecrawl honest comparison 2026 — what each one wins", numResults=8) → review blogs surfacing pricing-trap + credit-multiplier evidence
12. mcp__claude_ai_Exa__web_fetch_exa(urls=["architjn.com/blog/apify-vs-bright-data-vs-firecrawl-honest-comparison-2026", "scrapegraphai.com/blog/firecrawl-pricing"]) → full verbatim for pain-mapping
13. (skip linkedin/search/jobs for Anysite — small; mark "no signal")
14. (skip company_employee_stats; skip Anysite g2/github/crunchbase — categories not currently exposed via the MCP; skip SEC — no public incumbent yet in pure web-data category)
```

Findings:

| | Bright Data | Apify | Firecrawl | ScrapingBee | Anysite (own) |
|---|---|---|---|---|---|
| Hero copy | "The web's data, unlocked" | "Get real-time web data for your AI" | "Power AI agents with clean web data" | "The Best Web Scraping API to Avoid Getting Blocked" | "Turn Any Website Into an API — The entire web is your database" |
| Pricing floor / ceiling | $1/1K req → $499/mo for 510K records | $5 free → $49 Starter (compute-unit) | $0 → $16 Hobby → $83 → $333 (5x extract multiplier) | $49 → $99 → $599 | $30 MCP Unlimited → $49 Starter → $1,199 Enterprise |
| LinkedIn specialities | 13 terms (price intelligence, brand monitoring, AI Agents, ...) | 8 terms (Web scraping, Browser automation, AI agents, Actor marketplace, ...) | empty (content-marketing-led; short_description: "Web data API for AI") | empty (short_description: "Web Scraping API") | 40+ named endpoints + MCP server (homepage copy) |
| Last 30d signal | Web MCP free; enterprise compliance content | Native MCP highlight; Creator Growth program | Onboarding-Skill flow; CLI launch; "scrapers are dead" content | CLI launch | YAML pipeline-as-code; MCP server; pre-built skills |
| Hiring (function mix) | 20+ enterprise GTM (Sales Directors, AEs, BDR; global expansion) | 20+ developer platform (Senior Backend, Fraud Prevention, Creator Growth, Product Marketing) | 0 (small + content-led) | 1 (Sr PM Vilnius) | 0 (small) |

### Empty quadrant

Cross-referencing 5 axes + pain themes:

1. Hero axis: Bright Data + Apify both pitch "platform"; Firecrawl pitches "for AI"; ScrapingBee pitches "avoid blocks." Nobody pitches *predictable, agent-discoverable pricing*. That phrase fits Anysite's own demo flow and is unclaimed elsewhere.
2. Pricing axis: every major competitor uses some form of credit/compute/page metering. Pain mining surfaced "credit multipliers" + "failed-request charges" as a top-3 cluster. Anysite's $30/mo flat MCP-Unlimited plan + cost-estimate-before-run is the only positioning that directly answers that cluster.
3. LinkedIn specialities axis: Bright Data's `specialities[]` is 13 use-case terms; Apify's is 8 platform terms. Anysite's source-coverage shape (LinkedIn + Twitter + Reddit + YouTube + SEC + Crunchbase + GitHub + Amazon + Any URL) is a different *unit* of self-positioning.
4. Recent shipping axis: Firecrawl + Anysite are the only two shipping for the agent itself; Bright Data + Apify still position humans-on-dashboards.
5. Hiring axis: nobody is staffing "agent-native DX" specifically — Apify has a Creator Growth Lead (Actor-publisher side), but no one is hiring for "DX for AI agents." Unstaffed function across the field.

### Three candidates (and why C wins)

**Candidate A — vs Firecrawl (the closest direct AI-agent threat):**
> "For developers building AI agents that need structured data from any platform, Anysite is the agent-native data API that ships 40+ pre-built source endpoints — so your agent can discover and call exactly the data shape it needs. Unlike Firecrawl, Anysite doesn't charge a 5x multiplier on AI extraction, and you don't have to write a JSON schema for every page."
Pain coverage: 2/3 (pricing + agent-native). Defensibility: 2/3 (Firecrawl can match the multiplier story by changing pricing; the 40-source library is harder to copy). Empty-quadrant evidence: 3/5 axes. **Total: 7/11.**

**Candidate B — vs Bright Data (the price ceiling + dashboard incumbent):**
> "For teams whose AI agents need web data but can't drive a vendor dashboard, Anysite is the agent-native web data platform that's discoverable and callable end-to-end from Claude Code or Cursor. Unlike Bright Data, you don't pay enterprise pricing to access enterprise-grade structured data."
Pain coverage: 2/3 (agent-native; partial pricing). Defensibility: 2/3 (Bright Data already ships an MCP server). Empty-quadrant evidence: 3/5 axes. **Total: 7/11.**

**Candidate C — vs "Build it yourself: Crawl4AI + LLM key + proxies + maintenance" (the do-nothing alternative — the #1 alternative per Reddit + blog signal):**
> "For developer teams scoping a web-data pipeline who are choosing between a managed API and stitching together Crawl4AI + a proxy provider + their own LLM key, Anysite is the platform that gives you the 'just describe what you need' developer experience at a flat $30/month for MCP unlimited — without the maintenance treadmill, the credit-multiplier surprises, or the engineering time tax. Unlike Crawl4AI + your own stack, Anysite ships 40+ self-healing endpoints across LinkedIn, Reddit, YouTube, Twitter, SEC, Crunchbase, GitHub, and any URL — and you can call it conversationally from Claude Desktop today."
Pain coverage: 3/3 (scrapers break + pricing surprises + agent-native). Defensibility: 3/3 (Crawl4AI / DIY can't ship MCP + 40 prebuilt sources + flat pricing without becoming a managed vendor — at which point they ARE Anysite). Empty-quadrant evidence: 4/5 axes (hero, pricing, recent shipping, hiring). **Total: 10/11.**

Winner: Candidate C. A loses on defensibility — Firecrawl can ship pricing changes overnight. B loses on the pain-coverage axis — Bright Data isn't where the daily pain originates for the developer-+-agent segment. C wins because it positions Anysite against the dominant workaround (Dunford "competitive alternative" lens — the real competitor most early-stage scrapy-curious teams almost picked instead), maps onto every top pain cluster, and 4/5 axes confirm the position is unclaimed.

### Positioning move (the winner restated)

> **"Anysite is the agent-native web data platform — 40+ structured endpoints + an MCP server + flat-rate pricing — so your team stops maintaining brittle scrapers, stops getting surprised by credit multipliers, and ships AI agents that actually have eyes on the web."**

### So what
- Hero-copy change: try "Stop maintaining scrapers. Start shipping agents. 40+ structured endpoints + MCP + flat pricing." The current hero is descriptive; the alternative leads with the pain.
- Ship to signal: a public "Cost Calculator with no-surprise guarantee" on the pricing page — same UX as Anysite's homepage demo (`"Estimated cost: ~2,400 credits. Proceed?"`) elevated to a permanent landing-page artifact. Competitors can't ship this without admitting their multiplier model is the problem.
- First customer segment: solo developers + small AI-agent teams currently on Firecrawl Hobby/Standard who've hit the credit-multiplier wall — a measurable, addressable segment. The hiring axis confirms nobody else is staffing "agent-native DX" specifically, so the channel is open.
