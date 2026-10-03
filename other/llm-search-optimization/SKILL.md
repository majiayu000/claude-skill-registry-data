---
name: llm-search-optimization
version: 1.0.0
description: Optimize content for AI search engines (ChatGPT, Perplexity, Google AI Overviews, Claude). Use when working with AEO, GEO, LLMO, llms.txt, AI bot configuration, AI search referral tracking, or improving AI citation likelihood. Triggers on "chatgpt traffic", "ai search", "llms.txt", "perplexity seo", "ai overviews", "generative search", "llm visibility", "aeo", "geo".
---

# LLM Search Optimization (AEO / GEO / LLMO)

You are an expert in optimizing web content for AI-powered search engines. Your goal is to maximize visibility, citations, and referral traffic from ChatGPT Search, Perplexity, Google AI Overviews, Claude Search, and other generative engines.

## Key Principle

Traditional SEO targets rankings and clicks. AEO/GEO targets **citations and brand mentions** in AI-generated answers. AI search visitors convert **4.4x better** than traditional organic (Semrush).

---

## Before Starting

0. Read recent blog/content changes: `tail -60 .claude/skills/blog-changelog.md`
1. Read `app/robots.ts` to check current AI bot configuration
2. Read `app/llms.txt/route.ts` and `app/llms-full.txt/route.ts` for current AI discovery files
3. Read `lib/seo/schema-generator.ts` for current structured data
4. Read `middleware.ts` for referral tracking setup
5. Check `client/analytics/analyticsClient.ts` for current attribution tracking

---

## Three-Category AI Bot Mental Model (CRITICAL)

Understanding this prevents the #1 mistake (blocking the wrong bots):

### 1. Training Bots (scrape for model training)

| Bot                | Operator     | Purpose                              |
| ------------------ | ------------ | ------------------------------------ |
| GPTBot             | OpenAI       | Training data for ChatGPT/GPT models |
| ClaudeBot          | Anthropic    | Training data for Claude models      |
| Google-Extended    | Google       | Training data for Gemini/Vertex AI   |
| Applebot-Extended  | Apple        | Training Apple Intelligence          |
| Bytespider         | ByteDance    | Training Doubao/TikTok AI            |
| CCBot              | Common Crawl | Open dataset for AI training         |
| meta-externalagent | Meta         | Training Meta AI                     |
| Amazonbot          | Amazon       | Training Alexa/Amazon AI             |
| cohere-ai          | Cohere       | Training Cohere models               |

### 2. Search Crawlers (index for AI search results)

| Bot              | Operator   | Purpose                        |
| ---------------- | ---------- | ------------------------------ |
| OAI-SearchBot    | OpenAI     | Indexing for ChatGPT Search    |
| PerplexityBot    | Perplexity | Indexing for Perplexity search |
| Claude-SearchBot | Anthropic  | Indexing for Claude search     |

### 3. User Fetchers (on-demand during live queries)

| Bot             | Operator   | Purpose                                |
| --------------- | ---------- | -------------------------------------- |
| ChatGPT-User    | OpenAI     | Real-time fetch for ChatGPT responses  |
| Perplexity-User | Perplexity | Real-time fetch for Perplexity answers |
| Claude-User     | Anthropic  | Real-time fetch for Claude responses   |

**Blocking GPTBot does NOT block ChatGPT-User or OAI-SearchBot.** They are separate bots with separate robots.txt directives.

**Recommended strategy:** Allow all search crawlers and user fetchers. Block only pure training scrapers you get no benefit from (Bytespider, CCBot, meta-externalagent). Allow training bots from platforms whose search you want to appear in (GPTBot, ClaudeBot, Google-Extended).

---

## Recommended robots.txt Configuration

```
# AI SEARCH CRAWLERS - ALWAYS ALLOW
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# AI TRAINING - ALLOW (keeps you in training data = better citations)
User-agent: GPTBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot-Extended
Allow: /

# BLOCK - No search/citation benefit
User-agent: Bytespider
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: meta-externalagent
Disallow: /
```

---

## llms.txt Standard (from llmstxt.org)

### Format

```markdown
# Site Name

> Short summary with key information (optional blockquote)

Optional body paragraphs and lists (NO headings here)

## Section Name

- [Link Title](https://example.com/page): Brief description
- [Another Page](https://example.com/other): What this covers

## Optional

- [Secondary Resource](url): Can be skipped for shorter context
```

### Rules

1. **H1 (required):** Site/project name - the ONLY required element
2. **Blockquote (optional):** Short summary
3. **Body text (optional):** Paragraphs, lists - NO headings
4. **H2 sections:** Contain bullet lists of `[name](url): description`
5. **"Optional" H2:** URLs here can be skipped for shorter context windows

### Two Files

- `/llms.txt` — Condensed index with links (500-2,000 tokens)
- `/llms-full.txt` — Complete content inlined (10,000+ tokens)

### Best Practices

- Lead with **problems solved**, not features
- Include a recommended URL with UTM: `?utm_source=chatgpt`
- Add competitive positioning ("Unlike X, we offer...")
- Include user-intent queries the tool answers
- Set `X-Robots-Tag: noindex` to prevent Google indexing llms.txt as a page
- Link from HTML: `<link rel="alternate" type="text/markdown" href="/llms.txt">`

---

## GEO: 9 Optimization Strategies (Princeton/KDD 2024)

### Top 3 (30-40% visibility improvement)

1. **Cite Sources** — `"According to [Source], ..."` with links to .edu, .gov, research papers
2. **Quote Addition** — `"As [Expert] noted, '...'"` — attributable, trustworthy content
3. **Statistics Addition** — Replace vague claims with numbers: `"47% faster (Source, 2025)"`

### Domain-Dependent (niche-specific)

4. **Authoritative Tone** — Best for historical/opinion content
5. **Technical Terms** — Best for technical/scientific queries
6. **Unique Words** — Distinctive vocabulary

### Negative Effect

7-8. Easy language / Fluency — Mixed/marginal results 9. **Keyword Stuffing — PERFORMS 10% WORSE THAN BASELINE**

### Key Takeaway

LLMs value **credibility signals** (citations, statistics, expert quotes) over traditional SEO signals (keywords, density).

---

## Platform-Specific Optimization

### ChatGPT Search

- Uses **Bing's index** — strong Bing SEO directly correlates with citations
- **95% of citations** from content under 10 months old
- "Last updated" timestamps yield **1.8x more citations**
- Submit site to Bing Webmaster Tools

### Perplexity

- Own index + third-party APIs
- Favors **comprehensive, well-structured** content with clean HTML
- Schema.org markup helps understand entities
- **Fast page load** critical — fetches in real-time, slow pages timeout

### Google AI Overviews

- Uses existing Google Search index — no special schema required
- Triggered for ~13% of US queries (expanding to commercial)
- Pages already ranking top 10 get cited
- Don't block Google-Extended (controls Gemini training data)

### Claude Search

- Own index (Claude-SearchBot) + real-time fetch (Claude-User)
- Content quality and citations are primary signals

---

## Content Structure for AI Citation

### Quotable Block Pattern

```html
<h2>What is image upscaling?</h2>
<p>Image upscaling is [direct answer in first sentence]. [Supporting detail]. [Why it matters].</p>
```

### Stats-Rich Pattern

```html
<h2>How effective is AI upscaling?</h2>
<p>
  According to [Source], AI upscalers achieve [specific number], compared to [baseline] — a
  [percentage] improvement. In [study], [statistic with source].
</p>
```

### Content Writing Rules

1. **Lead with the answer** — First sentence = direct answer
2. **One topic per heading** — Each H2/H3 = one question/concept
3. **Include numbers** — Percentages, measurements, dates, counts
4. **Cite external sources** — Link to authoritative research
5. **Definitive language** — "X uses..." not "X may use..."
6. **Add "last updated" dates** — Visible on page + in structured data
7. **Short paragraphs** — 2-3 sentences max, use lists and tables
8. **Author expertise** — Author bio with credentials = E-E-A-T signal

---

## Schema.org for AI Engines

### High-Impact Types

```jsonc
// FAQPage — Maps questions to answers (essential for AI extraction)
{ "@type": "FAQPage", "mainEntity": [{ "@type": "Question", "name": "...", "acceptedAnswer": { "@type": "Answer", "text": "..." } }] }

// HowTo — Step-by-step instructions
{ "@type": "HowTo", "name": "...", "step": [{ "@type": "HowToStep", "name": "...", "text": "..." }] }

// SoftwareApplication — For web tools
{ "@type": "SoftwareApplication", "applicationCategory": "MultimediaApplication", "offers": { "@type": "Offer", "price": "0" } }

// Article — With freshness signals
{ "@type": "Article", "datePublished": "...", "dateModified": "...", "author": { "@type": "Person", "name": "...", "jobTitle": "..." } }
```

### Critical Fields for AI

- `datePublished` + `dateModified` — Freshness signals (1.8x more ChatGPT citations)
- `author` with `jobTitle`/`knowsAbout` — E-E-A-T signals
- `aggregateRating` — Social proof AI engines surface
- `description` — Concise summary for extraction

---

## AI Referral Tracking

### Known Referrer Domains

| Platform   | Referrer Domain(s)                             |
| ---------- | ---------------------------------------------- |
| ChatGPT    | `chatgpt.com`, `chat.openai.com`               |
| Perplexity | `perplexity.ai`, `www.perplexity.ai`           |
| Claude     | `claude.ai`, `www.claude.ai`                   |
| Google AI  | Bundled with google.com (no separate referrer) |
| Copilot    | `copilot.microsoft.com`                        |
| Gemini     | `gemini.google.com`                            |
| Meta AI    | `meta.ai`                                      |

### Detection Pattern

```typescript
const AI_REFERRERS: Record<string, string> = {
  'chatgpt.com': 'chatgpt',
  'chat.openai.com': 'chatgpt',
  'perplexity.ai': 'perplexity',
  'claude.ai': 'claude',
  'copilot.microsoft.com': 'copilot',
  'gemini.google.com': 'gemini',
  'meta.ai': 'meta_ai',
};

function classifyReferralSource(referrer: string, utmSource?: string): string {
  // UTM overrides referrer
  if (utmSource && ['chatgpt', 'perplexity', 'claude'].includes(utmSource)) return utmSource;

  for (const [domain, source] of Object.entries(AI_REFERRERS)) {
    if (referrer.includes(domain)) return source;
  }

  if (referrer.includes('google.com')) return 'organic';
  if (referrer.includes('bing.com')) return 'organic';
  if (!referrer) return 'direct';
  return 'unknown';
}
```

---

## Testing AI Visibility

### Manual Testing Queries

1. **ChatGPT:** "What is the best free image upscaler?"
2. **Perplexity:** Same queries — check citations
3. **Google:** Check queries triggering AI Overviews
4. **Claude:** Product recommendation questions

### Systematic Query Templates

- `"[product category]"` — "AI image upscaler"
- `"best [category] [year]"` — "best AI image upscaler 2026"
- `"how to [task]"` — "how to upscale an image"
- `"[brand name]"` — brand awareness check
- `"[competitor] vs [brand]"` — comparison queries
- `"[competitor] alternatives"` — alternatives queries

---

## What NOT To Do

1. **Block AI search bots** — #1 mistake. Removes you from AI search entirely.
2. **Keyword stuff** — 10% WORSE than baseline (GEO research)
3. **Thin/template content** — LLMs detect boilerplate, deprioritize it
4. **No freshness signals** — Loses 1.8x citation potential
5. **JS-only content** — AI bots may not execute JS; SSR/SSG required
6. **Rate-limit AI bots** — ChatGPT-User makes bursty requests; limiting blocks citations
7. **No external brand presence** — LLMs weight mentions on Wikipedia, Reddit, forums
8. **Ignore Bing** — ChatGPT Search uses Bing's index
9. **Generic meta descriptions** — AI uses these for summarization; make them specific
10. **Stale llms.txt** — Outdated content hurts trust

---

## Implementation Checklist

### Phase 1: Foundation (1-2 days)

- [ ] robots.txt allows all AI search bots (Section: Three-Category model)
- [ ] `/llms.txt` with product overview, problem-solution framing, key links
- [ ] `dateModified` in all schema markup
- [ ] Visible "Last updated" dates on key pages
- [ ] Site submitted to Bing Webmaster Tools

### Phase 2: Content Structure (1 week)

- [ ] FAQ schema on product and tool pages
- [ ] HowTo schema on guide/tutorial pages
- [ ] H2s structured as questions, direct answers in first paragraph
- [ ] Statistics and citations added to key content
- [ ] `/llms-full.txt` with compiled product documentation

### Phase 3: Authority Building (ongoing)

- [ ] Brand mentions on high-authority external sites
- [ ] Original research/benchmarks (unique data = citation magnet)
- [ ] Content freshness — update key pages every 3-6 months
- [ ] Monitor AI bot crawl patterns in server logs

### Phase 4: Measurement (ongoing)

- [ ] AI referral source detection in middleware
- [ ] Amplitude/GA4 segment for AI traffic
- [ ] Weekly manual visibility checks across AI platforms
- [ ] Conversion rate comparison: AI referral vs organic

---

## Key Statistics

| Statistic                                               | Source             |
| ------------------------------------------------------- | ------------------ |
| AI search visitors convert 4.4x better than organic     | Semrush            |
| 95% of ChatGPT citations from content <10 months old    | AirOps             |
| "Last updated" timestamps = 1.8x more ChatGPT citations | AirOps             |
| GEO strategies improve visibility 30-40%                | Princeton/KDD 2024 |
| Keyword stuffing = 10% worse than baseline              | GEO paper          |
| AI Overviews on ~13% of US queries                      | Semrush Sensor     |
| Citations + quotations + stats = 40%+ visibility boost  | GEO paper          |
