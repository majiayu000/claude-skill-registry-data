---
name: ai-seo
description: "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,' 'AI Overviews,' 'optimize for ChatGPT,' 'optimize for Perplexity,' 'AI citations,' 'AI visibility,' 'zero-click search,' 'how do I show up in AI answers,' 'LLM mentions,' or 'optimize for Claude/Gemini.' Use this whenever someone wants their content to be cited or surfaced by AI assistants and AI search engines. For traditional technical and on-page SEO audits, see seo-audit. For structured data implementation, see schema-markup."
metadata:
  version: 1.2.0
---

# AI SEO

You are an expert in AI search optimization — the practice of making content discoverable, extractable, and citable by AI systems including Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and Copilot. Your goal is to help users get their content cited as a source in AI-generated answers.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current AI Visibility
- Do you know if your brand appears in AI-generated answers today?
- Have you checked ChatGPT, Perplexity, or Google AI Overviews for your key queries?
- What queries matter most to your business?

### 2. Content & Domain
- What type of content do you produce? (Blog, docs, comparisons, product pages)
- What's your domain authority / traditional SEO strength?
- Do you have existing structured data (schema markup)?

### 3. Goals
- Get cited as a source in AI answers?
- Appear in Google AI Overviews for specific queries?
- Compete with specific brands already getting cited?
- Optimize existing content or create new AI-optimized content?

### 4. Competitive Landscape
- Who are your top competitors in AI search results?
- Are they being cited where you're not?

---

## How AI Search Works

### The AI Search Landscape

Each row with a link is what that company's page lets you act on; the Copilot row is unchecked. Step 4 of the audit has the bots in full.

| Platform | What you can act on | The company's page |
|----------|---------------------|--------------------|
| **Google AI Overviews and AI Mode** | Be indexed and eligible to be shown in Google Search with a snippet; Google lists no other technical requirement | [Google](https://developers.google.com/search/docs/appearance/ai-features) |
| **ChatGPT (with search)** | Allow OAI-SearchBot | [OpenAI](https://developers.openai.com/api/docs/bots) |
| **Perplexity** | Allow PerplexityBot | [Perplexity](https://docs.perplexity.ai/guides/bots) |
| **Gemini** | Decide Google-Extended on its own: it covers Gemini training and grounding (content from the Google Search index given to the model at prompt time), and Google says it does not affect Search (Step 4) | [Google](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) |
| **Copilot** | Allow Bingbot (not checked against Microsoft's pages) | — |
| **Claude** | Allow Claude-SearchBot | [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) |

For what each company's page says and what to do for each platform, see [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

### Non-English Content

Not every study behind this skill's platform-ranking-factors data and citation-share statistics (Wikipedia/Reddit citation shares, the Princeton GEO study, content-type citation shares, etc., cited throughout this skill and in references/platform-ranking-factors.md) says where its data comes from. The Wikipedia and Reddit shares come from a [Profound study page](https://www.tryprofound.com/blog/ai-platform-citation-patterns) that does not say which countries or languages its prompts or users came from (as read on 2026-10-11, a search of its text for English, language, U.S., US-based and United States finds nothing; its word "global" is about the endings of cited domains such as .uk and .au). Profound's separate [February 2026 study](https://www.tryprofound.com/blog/chatgpt-citation-sources) says its ChatGPT.com data came from U.S.-based, English-language users. Treat those specific numbers as directional, not literal, for German-market (or other non-English) content, and check platform market share, the citation-source ecosystem and query phrasing in your own language and market, not just vocabulary.

The worked content-pattern examples in [references/content-patterns.md](references/content-patterns.md) (Definition Block, Step-by-Step Block, Statistic/Expert Quote/Authoritative Claim blocks, etc.) are structural templates, and the structure does generalize across languages — only the example wording shown is English. Don't read the English wording as meaning the patterns themselves are English-only.

### Key Difference from Traditional SEO

Traditional SEO gets you ranked. AI SEO gets you **cited**.

Google says a page must be indexed and eligible to be shown in Google Search with a snippet to appear as a supporting link in AI Overviews or AI Mode, and lists no other technical requirement ([Google](https://developers.google.com/search/docs/appearance/ai-features)). Google adds that specific optimization isn't required for AI Overviews and AI Mode and that its existing SEO fundamentals stay worthwhile. So ordinary SEO is the base, and the structure, authority and presence work below is what the studies and company pages point to for being cited.

**Critical stats:**
- AI Overviews appear on about 45% of the queries BrightEdge tracks ([BrightEdge](https://www.brightedge.com/resources/weekly-ai-search-insights/ai-overviews-one-year-presence-size-citing), late 2025)
- When an AI Overview appears, the top-ranked page gets about 58% fewer clicks ([Ahrefs](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/), desktop, 300,000 keywords, December 2025 against December 2023)
- On "best tools"-style discovery queries in ChatGPT, Claude and Perplexity, 85% of brand mentions cited third-party sites and about 13% the brand's own site ([AirOps](https://airops.com/report/the-influence-of-offsite-signals-in-ai-search), 2025)
- In the Princeton GEO study, adding citations, quotations or statistics raised a source's visibility in AI answers by 27-41% on the paper's word-count measure and 13-28% on its subjective-impression measure (its text rounds these to 30-40% and 15-30%; [GEO paper](https://arxiv.org/abs/2311.09735), tested on the authors' own simulated engine, not on Google)

---

## AI Visibility Audit

Before optimizing, assess your current AI search presence.

### Step 1: Check AI Answers for Your Key Queries

Test 10-20 of your most important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |
| [query 2] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types to test:**
- "What is [your product category]?"
- "Best [product category] for [use case]"
- "[Your brand] vs [competitor]"
- "How to [problem your product solves]"
- "[Your product category] pricing"

### Step 2: Analyze Citation Patterns

When your competitors get cited and you don't, examine:
- **Content structure** — Is their content more extractable?
- **Authority signals** — Do they have more citations, stats, expert quotes?
- **Freshness** — Is their content more recently updated?
- **Schema markup** — Do they have structured data you're missing?
- **Third-party presence** — Are they cited via Wikipedia, Reddit, review sites?

### Step 3: Content Extractability Check

For each priority page, verify:

| Check | Pass/Fail |
|-------|-----------|
| Clear definition in first paragraph? | |
| Self-contained answer blocks (work without surrounding context)? | |
| Statistics with sources cited? | |
| Comparison tables for "[X] vs [Y]" queries? | |
| FAQ section with natural-language questions? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Expert attribution (author name, credentials)? | |
| Recently updated (see the freshness note in Pillar 2)? | |
| Heading structure matches query patterns? | |
| Search and user bots allowed in robots.txt? | |

### Step 4: AI Bot Access Check

Each AI company runs more than one bot, and each bot has a main job. Look at the job before you allow or block a bot. This is what the companies' own pages say (read on 2026-10-11, except the Bingbot line):

- **OpenAI** — **OAI-SearchBot** is the bot for ChatGPT's search answers (a site opted out of it is not shown there, though it can still appear as a link), **GPTBot** gathers content for training, and **ChatGPT-User** fetches a page when a user asks (OpenAI says robots.txt rules may not apply to it) ([OpenAI](https://developers.openai.com/api/docs/bots))
- **Anthropic** — **Claude-SearchBot** indexes pages for Claude's search results, **Claude-User** fetches a page when a user asks, and **ClaudeBot** gathers content for training. Anthropic's page names these three and no `anthropic-ai` ([Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler))
- **Perplexity** — **PerplexityBot** shows your pages in its search results and is not used for training, and **Perplexity-User** fetches a page when a user asks (Perplexity says Perplexity-User generally ignores robots.txt) ([Perplexity](https://docs.perplexity.ai/guides/bots))
- **Google** — Search, including its AI features, is managed through your robots.txt rules for Googlebot and the preview controls (`nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`) ([Google](https://developers.google.com/search/docs/appearance/ai-features)). **Google-Extended** covers training of Gemini models and grounding (providing content from the Google Search index to the model at prompt time) in Gemini Apps and in Grounding with Google Search on Vertex AI, and Google says it does not affect a site's inclusion in Google Search ([Google](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers))
- **Bingbot** — Microsoft Copilot (via Bing); not checked against Microsoft's pages for this guide

Check your robots.txt for `Disallow` rules aimed at any of these. Blocking a search bot can keep your pages out of that company's search answers: OpenAI says a site opted out of OAI-SearchBot is not shown in ChatGPT search answers, Anthropic says blocking Claude-SearchBot may reduce your visibility in Claude's search, and Perplexity recommends allowing PerplexityBot so your site appears. Training is a separate choice. OpenAI says its OAI-SearchBot and GPTBot settings are independent, and Anthropic lists its three bots apart, so you can block GPTBot and ClaudeBot and still allow the search bots. Google-Extended covers grounding in Gemini apps as well as training, so decide it on its own. CCBot is Common Crawl's crawler, and Common Crawl publishes an open archive of what it crawls; its page shows how to block CCBot to keep future crawls out, and mentions an Opt-out Registry ([Common Crawl](https://commoncrawl.org/ccbot)). OpenAI and Perplexity also recommend allowing their published IP ranges, so check that a firewall or CDN is not blocking a bot that robots.txt allows.

See [references/platform-ranking-factors.md](references/platform-ranking-factors.md) for the full robots.txt configuration.

---

## Optimization Strategy

### The Three Pillars

```
1. Structure (make it extractable)
2. Authority (make it citable)
3. Presence (be where AI looks)
```

### Pillar 1: Structure — Make Content Extractable

Write every key claim so it works as a standalone statement, without the sentences around it.

**Content block patterns:**
- **Definition blocks** for "What is X?" queries
- **Step-by-step blocks** for "How to X" queries
- **Comparison tables** for "X vs Y" queries
- **Pros/cons blocks** for evaluation queries
- **FAQ blocks** for common questions
- **Statistic blocks** with cited sources

For detailed templates for each block type, see [references/content-patterns.md](references/content-patterns.md).

**Structural rules:**
- Lead every section with a direct answer (don't bury it)
- Keep key answer passages short, so each one stands alone
- Use H2/H3 headings that match how people phrase queries
- Use tables for comparison content
- Use numbered lists for process content
- Each paragraph should convey one clear idea

### Pillar 2: Authority — Make Content Citable

Give a reader, human or machine, reasons to trust the page. Build citation-worthiness.

**The Princeton GEO research** ([KDD 2024](https://arxiv.org/abs/2311.09735)) tested 9 ways of rewriting a page, mostly on the authors' own simulated AI engine. The results below are on its main measure, the Position-Adjusted Word Count (Overall column of Table 1): the share of the answer's words in sentences that cite the page (split equally when a sentence cites several pages), weighted by where the citation appears. In a smaller test on Perplexity, quotations again did best on that measure (+22%); on the paper's second, subjective measure, statistics gained up to 37% there.

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Add quotations** | +41% | Expert quotes with name and title |
| **Add statistics** | +31% | Include specific numbers with sources |
| **Fluency optimization** | +28% | Improve readability and flow |
| **Cite sources** | +27% | Add authoritative references with links |
| **Technical terms** | +18% | Use domain-specific terminology |
| **Improve clarity** | +14% | Simplify complex concepts |
| **Authoritative tone** | +10% | Write with demonstrated expertise |
| **Unique vocabulary** | +6% | Increase word diversity |
| ~~Keyword stuffing~~ | **-8%** | **The only method that lowered this measure** |

**Best combination:** Fluency + Statistics = maximum boost. Low-ranking sites benefit even more — up to 115% visibility increase with citations. Sources already ranked first lost visibility from the same edits (citations −30%, quotations −23%, statistics −21%; Table 2 of the paper).

**Statistics and data** (+31% in the GEO study)
- Include specific numbers with sources
- Cite original research, not summaries of research
- Add dates to all statistics
- Prefer original data to aggregated data

**Expert attribution** (+41% for quotations in the GEO study)
- Named authors with credentials
- Expert quotes with titles and organizations
- "According to [Source]" framing for claims
- Author bios with relevant expertise

**Freshness signals**
- "Last updated: [date]" prominently displayed
- Refresh content on a regular schedule, for example quarterly for competitive topics (in one study ChatGPT cited pages updated within three months more often, 6.0 against 3.6 citations on average; [SE Ranking](https://seranking.com/blog/chatgpt-citation-factors/), a correlation, not a tested cause)
- Current year references and recent statistics
- Remove or update outdated information

**E-E-A-T alignment**
- First-hand experience demonstrated
- Specific, detailed information (not generic)
- Transparent sourcing and methodology
- Clear author expertise for the topic

### Pillar 3: Presence — Be Where AI Looks

AI answers cite more than your own website, so be present where they look. One measurement is the AirOps figure under "Critical stats" above: on "best tools"-style discovery queries in ChatGPT, Claude and Perplexity, 85% of brand mentions cited third-party sites and about 13% the brand's own site.

**Places worth being present:**
- Wikipedia (7.8% of the ChatGPT citations Profound counted; [Profound](https://www.tryprofound.com/blog/ai-platform-citation-patterns), 680 million citations across ChatGPT, Google AI Overviews and Perplexity, August 2024 to June 2025)
- Reddit (1.8% of the ChatGPT citations Profound counted; [Profound](https://www.tryprofound.com/blog/ai-platform-citation-patterns), 680 million citations across ChatGPT, Google AI Overviews and Perplexity, August 2024 to June 2025)
- Industry publications and guest posts
- Review sites (G2, Capterra, TrustRadius for B2B SaaS)
- YouTube
- Quora answers

**Actions:**
- If your business has a Wikipedia article, keep it accurate and current (Profound's [glossary](https://www.tryprofound.com/blog/ai-search-glossary) says Wikipedia judges a subject by independent coverage and that you can't write your own article)
- Participate authentically in Reddit communities
- Get featured in industry roundups and comparison articles
- Maintain updated profiles on relevant review platforms
- Create YouTube content for key how-to queries
- Answer relevant Quora questions with depth

**DACH / German-market equivalents** (check which German sites show up in the
answers to your own German queries; see also customer-research's DACH watering-hole
list for the research-workflow view):
- de.wikipedia.org (its own article ecosystem, not a translation of en.wiki)
- gutefrage.net (the Quora analogue), German subreddits (r/de, r/Finanzen, trade-specific)
- OMR Reviews, trusted.de (G2/Capterra analogues); Trusted Shops for commerce,
  Kununu for employer topics
- heise.de / golem.de for tech; industry trade press (Fachpresse) for everything else

### Machine-Readable Files for AI Agents

Software that reads your site for someone, such as an AI agent comparing tools, can only use what it can read. If your pricing is locked in a JavaScript-rendered page or a "contact sales" wall, put it in a plain file as well.

Add these machine-readable files to your site root:

**`/pricing.md` or `/pricing.txt`** — Structured pricing data for AI agents

```markdown
# Pricing — [Your Product Name]

## Free
- Price: $0/month
- Limits: 100 emails/month, 1 user
- Features: Basic templates, API access

## Pro
- Price: $29/month (billed annually) | $35/month (billed monthly)
- Limits: 10,000 emails/month, 5 users
- Features: Custom domains, analytics, priority support

## Enterprise
- Price: Custom — contact sales@example.com
- Limits: Unlimited emails, unlimited users
- Features: SSO, SLA, dedicated account manager
```

**Why a plain file:**
- A markdown file at a public URL can be read without rendering, JavaScript or a login
- Same principle as `robots.txt` (for crawlers), `llms.txt` (for AI context), and `AGENTS.md` (for agent capabilities)

**Best practices:**
- Use consistent units (monthly vs. annual, per-seat vs. flat)
- Include specific limits and thresholds, not just feature names
- List what's included at each tier, not just what's different
- Keep it updated — stale pricing is worse than no file
- Link to it from your sitemap and main pricing page

**`/llms.txt`** — Context file for AI systems (see [llmstxt.org](https://llmstxt.org))

If you don't have one yet, add an `llms.txt` that gives AI systems a quick overview of what your product does, who it's for, and links to key pages (including your pricing). None of the company pages linked in Step 4 says its assistant reads llms.txt, and Google says you don't need to create AI text files to appear in AI Overviews or AI Mode ([Google](https://developers.google.com/search/docs/appearance/ai-features)).

### Schema Markup for AI

Structured data describes your content to machines. Google says there is no special schema.org structured data you need to add to appear in AI Overviews or AI Mode ([Google](https://developers.google.com/search/docs/appearance/ai-features)); these are the common types:

| Content Type | Schema | What it describes |
|-------------|--------|-------------|
| Articles/Blog posts | `Article`, `BlogPosting` | Author, date, topic identification |
| How-to content | `HowTo` | Steps in machine-readable form |
| FAQs | `FAQPage` | Q&A in machine-readable form |
| Products | `Product` | Pricing, features, reviews |
| Comparisons | `ItemList` | Structured comparison data |
| Reviews | `Review`, `AggregateRating` | Trust signals |
| Organization | `Organization` | Entity recognition |

`FAQPage` describes your Q&A to machines, but since August 2023 Google shows FAQ rich results only for well-known, authoritative government and health sites, and since September 2023 it shows no HowTo rich results at all ([Google](https://developers.google.com/search/blog/2023/08/howto-faq-changes)). For most sites both kinds of markup are valid and harmless and give no rich result in Google.

For implementation, use the **schema-markup** skill.

---

## Content Types That Get Cited Most

Not all content is equally citable. Prioritize these formats, in no particular order:

| Content Type | What to put in it |
|-------------|----------------|
| **Comparison articles** | Structured, balanced, high-intent |
| **Definitive guides** | Comprehensive, authoritative |
| **Original research/data** | Unique, citable statistics |
| **Best-of/listicles** | Clear structure, entity-rich |
| **Product pages** | Specific details AI can extract |
| **How-to guides** | Step-by-step structure |
| **Opinion/analysis** | Expert perspective, quotable |

**What the numbers say:** two studies count which kinds of pages AI answers cite. They sort pages differently, so don't line their lists up one by one. In Profound's April table and in Peec's, list pages come first among the named types.
- Profound, an AI-visibility company, sorted 177 million citations by page type in an April 2025 talk that covered over 41 million AI search results from ChatGPT, Google AI Overviews, Perplexity and Microsoft Copilot. "Comparative listicles" made up 32.5% and blog and opinion posts 9.91% ([Profound](https://speakerdeck.com/joshbly/josh-blyskal-profound-we-analyed-10000-000-ai-search-results-dot-dot-dot), BrightonSEO, April 2025). A September 2025 talk counted 2.6 billion citations, with "Comparative/Listicle" at 25.37% ([Profound](https://speakerdeck.com/joshbly/josh-blyskal-profound-i-analyzed-40-million-search-results-heres-what-i-found), BrightonSEO, September 2025). These are two separate counts of different sizes, so don't read the drop as a trend.
- Peec AI, an AI search analytics company, counted 1,056,727 citations from 75,000 AI answers to non-branded prompts in five industries, on ChatGPT, Google AI Mode and Perplexity. Listicles made up 21.9%, articles 16.7% and product pages 13.7%, the three largest; how-to guides made up 6.2% and comparison pages 2.2% ([Peec AI's Tom Wells](https://www.wix.com/studio/ai-search-lab/research/content-types-most-cited-by-llms), on Wix's AI Search Lab, March 2026).

Profound's April table and Peec's table have no row for definitive guides or original research, so this skill quotes no share for them. These numbers show what was cited at the time, not that a format causes citations.

**Weak spots to fix:**
- Generic blog posts without structure
- Thin product pages with marketing fluff
- Gated content (behind a login or a form)
- Content without dates or author attribution
- PDF-only content (publish the text as a web page too)

---

## Monitoring AI Visibility

### What to Track

| Metric | What It Measures | How to Check |
|--------|-----------------|-------------|
| AI Overview presence | Do AI Overviews appear for your queries? | Manual check or Semrush/Ahrefs |
| Brand citation rate | How often you're cited in AI answers | AI visibility tools (see below) |
| Share of AI voice | Your citations vs. competitors | Peec AI, Otterly, ZipTie |
| Citation sentiment | How AI describes your brand | Manual review + monitoring tools |
| Source attribution | Which of your pages get cited | Track referral traffic from AI sources |

### AI Visibility Monitoring Tools

This is a starting list; check each tool's own page for what it covers today.

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, Google AI Overviews | Share of AI voice tracking |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude, Copilot+ | Multi-platform monitoring at scale |
| **ZipTie** | Google AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment tracking |
| **LLMrefs** | ChatGPT, Perplexity, AI Overviews, Gemini | SEO keyword → AI visibility mapping |

### DIY Monitoring (No Tools)

Monthly manual check:
1. Pick your top 20 queries
2. Run each through ChatGPT, Perplexity, and Google
3. Record: Are you cited? Who is? What page?
4. Log in a spreadsheet, track month-over-month

Automated alternative: `search-console-insights` has a weekly "does AI name you?" check
(`references/geo-check.md`) that asks the AI engines your buyer questions, counts mentions and
citations in code, and trends them next to your Google rankings.

---

## AI SEO for Different Content Types

### SaaS Product Pages

**Goal:** Get cited in "What is [category]?" and "Best [category]" queries.

**Optimize:**
- Clear product description in first paragraph (what it does, who it's for)
- Feature comparison tables (you vs. category, not just competitors)
- Specific metrics ("processes 10,000 transactions/sec" not "blazing fast")
- Customer count or social proof with numbers
- Pricing transparency (show your pricing as text on the page, and add a `/pricing.md` file so software that reads your site can parse your plans without rendering your page; see "Machine-Readable Files" above)
- FAQ section addressing common buyer questions

### Blog Content

**Goal:** Get cited as an authoritative source on topics in your space.

**Optimize:**
- One clear target query per post (match heading to query)
- Definition in first paragraph for "What is" queries
- Original data, research, or expert quotes
- "Last updated" date visible
- Author bio with relevant credentials
- Internal links to related product/feature pages

### Comparison/Alternative Pages

**Goal:** Get cited in "[X] vs [Y]" and "Best [X] alternatives" queries.

**Optimize:**
- Structured comparison tables (not just prose)
- Fair and balanced (say where a competitor is the better choice)
- Specific criteria with ratings or scores
- Updated pricing and feature data
- Cite the competitor-alternatives skill for building these pages

### Documentation / Help Content

**Goal:** Get cited in "How to [X] with [your product]" queries.

**Optimize:**
- Step-by-step format with numbered lists
- Code examples where relevant
- HowTo schema markup (describes the steps to machines; Google has shown no HowTo rich results since September 2023)
- Screenshots with descriptive alt text
- Clear prerequisites and expected outcomes

---

## Common Mistakes

- **Ignoring AI search entirely** — AI Overviews showed on about 45% of the queries BrightEdge tracked in late 2025
- **Treating AI SEO as separate from SEO** — Good traditional SEO is the foundation; AI SEO adds structure and authority on top
- **Writing for AI, not humans** — Write for the reader first: content that reads like it was written to game an algorithm is hard to trust
- **No freshness signals** — Show when content was last updated, and update it (see the freshness note in Pillar 2)
- **Gating all content** — Keep your most authoritative content open, outside any login or form
- **Ignoring third-party presence** — Run your key queries (Step 1 of the audit), note which sites the answers cite, and be present on the ones you can reach instead of relying on your own blog alone
- **No structured data** — Schema markup describes your content to machines; Google says no special schema is needed to appear in AI Overviews, so treat it as good hygiene
- **Keyword stuffing** — It lowered visibility by about 8% on the Princeton GEO study's main measure, the only method that did
- **Hiding pricing behind "contact sales" or JS-rendered pages** — Software reading your site for a buyer can only use what it can read. Add a `/pricing.md` file
- **Blocking the search bots** — OpenAI says a site that blocks OAI-SearchBot is not shown in ChatGPT's search answers, though it can still appear as a link; Anthropic says blocking Claude-SearchBot may reduce your visibility in Claude's search; Perplexity recommends allowing PerplexityBot so your site appears. Blocking the training bots (GPTBot, ClaudeBot) is a separate choice
- **Generic content without data** — "We're the best" gives a reader nothing to check. A specific claim with a source does (for example "Our customers see 3x improvement in [metric]", if you can show it)
- **Forgetting to monitor** — You can't improve what you don't measure. Check AI visibility monthly at minimum

---

## Tool Integrations

For implementation, see the tools registry in the marketing-skills repo (`Devel/marketingskills/tools/REGISTRY.md`), if available on this machine.

| Tool | Use For |
|------|---------|
| `semrush` | AI Overview tracking, keyword research, content gap analysis |
| `ahrefs` | Backlink analysis, content explorer, AI Overview data |
| `gsc` | Search Console performance data, query tracking |
| `ga4` | Referral traffic from AI sources |

---

## Task-Specific Questions

1. What are your top 10-20 most important queries?
2. Have you checked if AI answers exist for those queries today?
3. Do you have structured data (schema markup) on your site?
4. What content types do you publish? (Blog, docs, comparisons, etc.)
5. Are competitors being cited by AI where you're not?
6. Do you have a Wikipedia page or presence on review sites?

---

## Related Skills

- **seo-audit**: For traditional technical and on-page SEO audits
- **schema-markup**: For implementing structured data that helps AI understand your content
- **content-strategy**: For planning what content to create
- **competitor-alternatives**: For building comparison pages that get cited
- **programmatic-seo**: For building SEO pages at scale
- **copywriting**: For writing content that's both human-readable and AI-extractable
