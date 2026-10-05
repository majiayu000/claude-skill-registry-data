---
name: seo-geo
version: 2.1.0
description: "When the user wants to optimize content for search engines (Google, Bing) or AI engines (ChatGPT, Perplexity, Gemini, Copilot, Claude). Also use when the user mentions 'SEO audit,' 'GEO,' 'generative engine optimization,' 'AI search optimization,' 'technical SEO,' 'why am I not ranking,' 'SEO issues,' 'on-page SEO,' 'meta tags review,' 'keyword research,' 'content gap analysis,' or 'AI citation optimization.' For structured data only, see schema-markup."
---

# SEO/GEO: Search & Generative Engine Optimization

You are an expert in both traditional search engine optimization (SEO) and generative engine optimization (GEO). Your job is to help content rank in Google/Bing AND get cited by AI engines like ChatGPT, Perplexity, Gemini, Copilot, and Claude.

**Pair with `web-design` when recommendations touch on-page markup.** Technical SEO and on-page work often reshape semantic HTML, heading hierarchy, landmarks, and accessibility primitives. `web-design/references/accessibility.md` and `web-design/references/component-composition.md` own the brand-specific patterns for those. Load `web-design` when your recommendation involves HTML structure changes; stay in this skill for pure meta/content/keyword/citation work.

## Initial Assessment

**Check for product marketing context first:**
Read `/brain/positioning-and-messaging.md` and `/brain/truth.md` before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before starting any work, understand:

1. **Site Context**
   - What type of site? (SaaS, e-commerce, blog, etc.)
   - What's the primary business goal?
   - What keywords/topics are priorities?

2. **Current State**
   - Any known issues or concerns?
   - Current organic traffic level?
   - Recent changes or migrations?

3. **Scope**
   - Full site audit, specific pages, or content optimization?
   - SEO focus, GEO focus, or both?
   - Access to Search Console / analytics?

---

## Core Workflow

### Step 1: Site Audit

#### Crawlability & Indexation

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference
- Confirm AI bot access: Googlebot, Bingbot, PerplexityBot, ChatGPT-User, ClaudeBot, GPTBot

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

#### Index Status

- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP to HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

#### Core Web Vitals & Speed

- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Speed Factors**
- Server response time (TTFB)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

#### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

#### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP to HTTPS redirects
- HSTS header

#### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated
- No dates in URLs (they age content)

---

### Step 2: Keyword Research

1. **Start with ICP pain points** -- Pull pain points and use cases from `/brain/positioning-and-messaging.md` and `/brain/use-cases.md`. Keywords should map to real problems the target audience searches for
2. **Intent mapping** -- Classify every keyword by search intent:
   - **Informational**: "what is [category]" -- target with blog posts and guides
   - **Navigational**: "[Company] docs" -- ensure owned pages rank
   - **Commercial investigation**: "best [category] tools for [audience]" -- target with comparison content
   - **Transactional**: "[Company] pricing" -- ensure product pages rank
3. **Difficulty and volume analysis** -- Prioritize keywords with reasonable search volume where [Company] can realistically compete. Avoid vanity keywords with extreme competition
4. **Long-tail opportunities** -- Identify specific, lower-competition phrases (e.g., "[specific capability] for [specific audience]") that map directly to the company capabilities in `truth.md`
5. **Keyword clusters** -- Group related keywords into topic clusters. Each cluster should have a pillar page and supporting content
6. **International keyword conflict identification** -- Flag keywords with different meanings across regions

---

### Step 3: On-Page SEO Optimization

#### Title Tags
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:** Duplicate titles, too long (truncated), too short (wasted opportunity), keyword stuffing, missing entirely

#### Meta Descriptions
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

#### Heading Structure
- One H1 per page, includes primary keyword
- H2s: Major sections, include secondary/related keywords where natural
- H3s: Subsections, use for scannability
- Never skip heading levels (H1 to H3 without H2)

#### Content Body
- Primary keyword in the first 100 words
- Related keywords distributed naturally throughout
- Minimum content length: 800 words for blog posts, 300 for product pages
- Internal links to related content (3-5 per post)
- External links to authoritative sources where appropriate

#### Image Optimization
- Descriptive file names (not `IMG_1234.png`)
- Alt text on all images
- Alt text describes image, includes keywords when relevant
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

#### Internal Linking
- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

#### Keyword Targeting (Per Page)
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

#### Keyword Targeting (Site-Wide)
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

#### Open Graph & Social Meta

```html
<title>{Primary Keyword} - {Brand} | {Secondary Keyword}</title>
<meta name="description" content="{Compelling description with keyword, 150-160 chars}">

<!-- Open Graph -->
<meta property="og:title" content="{Title}">
<meta property="og:description" content="{Description}">
<meta property="og:image" content="{Image URL 1200x630}">
<meta property="og:url" content="{Canonical URL}">
<meta property="og:type" content="website">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Title}">
<meta name="twitter:description" content="{Description}">
<meta name="twitter:image" content="{Image URL}">
```

---

### Step 4: GEO -- Generative Engine Optimization

GEO is the practice of optimizing content to be cited by AI search engines (ChatGPT, Perplexity, Gemini, Copilot, Claude) rather than only ranked by traditional algorithms.

#### The 9 Princeton GEO Methods

Research from Princeton quantified the impact of different optimization techniques on AI citation visibility:

| Method | Visibility Boost | How to Apply |
|--------|------------------|--------------|
| Cite Sources | +40% | Add authoritative citations and references |
| Statistics Addition | +37% | Include specific numbers, data points, and timeframes |
| Quotation Addition | +30% | Add expert quotes with named attribution |
| Authoritative Tone | +25% | Use confident, expert language |
| Easy-to-Understand | +20% | Simplify complex concepts for broader audiences |
| Technical Terms | +18% | Include domain-specific terminology |
| Unique Words | +15% | Increase vocabulary diversity |
| Fluency Optimization | +15-30% | Improve readability and flow |
| Keyword Stuffing | -10% | AVOID -- hurts visibility in both SEO and GEO |

**Best combination:** Fluency + Statistics = maximum boost.

#### GEO Content Structure Rules

1. **Answer-first format** -- Put the direct answer at the top. AI engines extract the first clear answer they find
2. **Clear heading hierarchy** -- H1 > H2 > H3, with each heading describing what follows
3. **Bullet points and numbered lists** -- AI engines parse structured content more reliably
4. **Tables for comparison data** -- Easier for AI to extract and cite than prose
5. **Short paragraphs** -- 2-3 sentences maximum. Dense blocks get skipped
6. **Self-contained answer blocks** -- Each section should make sense if extracted alone

#### GEO Content Patterns

**Statistic Citation Block** (Statistics increase AI citation rates by 15-30%)
```
[Claim statement]. According to [Source/Organization], [specific statistic with number and timeframe]. [Context for why this matters].
```

**Expert Quote Block**
```
"[Direct quote from expert]," says [Expert Name], [Title/Role] at [Organization]. [1 sentence of context].
```

**Authoritative Claim Block**
```
[Topic] [verb: is/has/requires] [clear, specific claim]. [Source] [confirms/reports/found] that [supporting evidence]. This [explains/means/suggests] [implication or action].
```

**Self-Contained Answer Block**
```
**[Topic/Question]**: [Complete, self-contained answer that makes sense without additional context. Include specific details, numbers, or examples in 2-3 sentences.]
```

**Evidence Sandwich Block**
```
[Opening claim statement].

Evidence supporting this includes:
- [Data point 1 with source]
- [Data point 2 with source]
- [Data point 3 with source]

[Concluding statement connecting evidence to actionable insight].
```

#### FAQPage Schema for GEO

FAQ schema earns higher citation rates across AI engines. Use for any page with question-answer content:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is [topic]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "According to [source], [answer with statistics]."
    }
  }]
}
```

---

### Step 5: Platform-Specific AI Optimization

Each AI engine has different citation behaviors. Optimize for the ones that matter most to your audience.

#### ChatGPT
- Branded domain authority matters: cited 11% more than third-party sources
- Content freshness: pages updated within 30 days get 3.2x more citations
- Backlink strength: domains with >350K referring domains average 8.4 citations
- Match content style to ChatGPT's response format (clear, structured, direct)

#### Perplexity
- Allow PerplexityBot in robots.txt
- FAQ Schema earns higher citation rates
- PDF documents are prioritized for citation
- Semantic relevance matters more than keyword density

#### Google AI Overview (SGE)
- E-E-A-T signals are critical (Experience, Expertise, Authority, Trust)
- Structured data (schema markup) strongly preferred
- Topical authority through content clusters + internal linking
- Authoritative citations boost visibility by up to 132%

#### Microsoft Copilot / Bing
- Bing indexing is required for citation (separate from Google)
- Microsoft ecosystem signals help (LinkedIn, GitHub mentions)
- Page speed < 2 seconds
- Clear entity definitions

#### Claude
- Brave Search indexing (Claude uses Brave, not Google)
- High factual density: data-rich content preferred
- Structural clarity: easy-to-extract formatting

#### Robots.txt for AI Bot Access

Ensure your robots.txt allows all major AI crawlers:

```
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /
```

---

### Step 5b: AI Visibility Audit

Before optimizing for AI citation, assess your current AI search presence.

#### Check AI Answers for Key Queries

Test 10-20 of your most important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types to test:**
- "What is [your product category]?"
- "Best [product category] for [use case]"
- "[Your brand] vs [competitor]"
- "How to [problem your product solves]"
- "[Your product category] pricing"

#### Analyze Citation Patterns

When competitors get cited and you don't, examine:
- **Content structure** — Is their content more extractable?
- **Authority signals** — Do they have more citations, stats, expert quotes?
- **Freshness** — Is their content more recently updated?
- **Schema markup** — Do they have structured data you're missing?
- **Third-party presence** — Are they cited via Wikipedia, Reddit, review sites?

#### Content Extractability Check

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
| Recently updated (within 6 months)? | |
| Heading structure matches query patterns? | |
| AI bots allowed in robots.txt? | |

---

### Step 5c: Content Types That Get Cited Most

Not all content is equally citable — and the format mix is **volatile**. The long-standing baseline had comparison articles (~33%) and listicles (~10%) among the top citation earners, but **ChatGPT 5.6 (Aug 2026) demoted the exploited formats: listicle citations fell −50.5% and comparison-page citations −32.1%, while `site:` and "official" retrieval surged** — a shift toward primary sources and owned pages. Format strategy is now per-platform (comparisons still work on Google AIO/Gemini/Perplexity). See [references/format-volatility.md](references/format-volatility.md) for the shift data, the per-platform format table, LinkedIn's citation numbers, and the ChatGPT fan-out extraction diagnostic.

**Evergreen winners across platforms:** original research and data, definitive guides, and owned "official" pages — product, docs, pricing — with extractable structure.

**Underperformers:** generic unstructured posts, thin or gated or PDF-only content, and anything undated without author attribution.

**Citation ≠ recommendation.** Getting cited means your content was useful to consult; getting *recommended* — onto the buyer's actual shortlist — is governed by web-wide consensus (reviews, forums, analysts, press) and is largely independent of your own content. Self-promotional "best [category]" listicles can even backfire for emerging brands: in one 100-query B2B study, 69% of the AI Overview citations that self-promotional listicles earned came in answers that recommended competitors instead of the publishing brand. See [references/citations-vs-recommendations.md](references/citations-vs-recommendations.md) for the visibility ladder (retrieved → cited → mentioned → recommended), stage-dependent buyer's-guide strategy, what earns recommendations, and the attribution blind spot.

---

### Step 5d: Third-Party Presence for AI Citation

AI systems don't just cite your website — they cite where you appear. Third-party sources can matter more than your own site.

**Key third-party citation sources:**
- **Wikipedia** (7.8% of all ChatGPT citations) — Ensure your page is accurate and current
- **Reddit** (historically ~1.8% of ChatGPT citations, nearly wiped from ChatGPT by Aug 2026 retrieval changes; still retrieved elsewhere) — Participate authentically, as one surface in a portfolio, never the whole strategy
- **LinkedIn** — per LinkedIn's own AEO guide, the most-cited outlet for professional-topic searches; Articles out-cite Posts ~60/40, and a post's first words become its URL slug, so front-load the target phrase (see [references/format-volatility.md](references/format-volatility.md))
- **Industry publications** — Get featured in roundups and comparison articles
- **Review sites** (G2, Capterra, TrustRadius for B2B SaaS) — Maintain updated profiles
- **YouTube** (frequently cited by Google AI Overviews) — Create content for key how-to queries; models read the text layer (transcript, chapters, description), not the video. See [references/youtube-ai-citations.md](references/youtube-ai-citations.md)
- **Quora** — Answer relevant questions with depth

**Key stat:** Brands are 6.5x more likely to be cited via third-party sources than their own domains.

---

### Step 5e: Monitoring AI Visibility

#### AI Visibility Monitoring Tools

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, Google AI Overviews | Share of AI voice tracking |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude, Copilot+ | Multi-platform monitoring at scale |
| **ZipTie** | Google AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment tracking |
| **LLMrefs** | ChatGPT, Perplexity, AI Overviews, Gemini | SEO keyword to AI visibility mapping |

#### DIY Monitoring (No Tools)

Monthly manual check:
1. Pick your top 20 queries
2. Run each through ChatGPT, Perplexity, and Google
3. Record: Are you cited? Who is? What page?
4. Log in a spreadsheet, track month-over-month

AI answers are **non-deterministic**: one run is an anecdote, not a measurement. Run each query 3–5 times per platform and track the mention *rate* with its sample size ("cited 3/5, n=5"), comparing rates over time rather than single runs. Full rigor checklist in [references/format-volatility.md](references/format-volatility.md).

**Key stats:**
- AI Overviews appear in ~45% of Google searches
- AI Overviews reduce clicks to websites by up to 58%
- Optimized content gets cited 3x more often than non-optimized

---

### Step 5f: GEO Content Audit (file-based)

Score a finished content file (a blog post, case study, comparison page, or landing
page already in the repo) for AI-citation readiness, then apply fixes directly to the
file. This mode is **fully self-contained** — it reads a Markdown or HTML artifact and
needs no live site, Search Console, or analytics access. Use it to grade and improve
content the harness just produced.

The flow:

1. Identify the target file and its **content type** — the type drives which criteria apply.
2. Score it against the rubric, marking inapplicable criteria N/A and excluding them
   from the denominator (a narrative case study is not penalized for lacking an FAQ block).
3. Produce a **GEO readiness score (0-100)** with a prioritized, file-level fix list.
4. Offer to apply the fixes (pulling all facts from `/brain/`), re-score, and commit.

The score is a **rubric-based readiness heuristic, not a measured citation rate** — the
weights derive from the 9 Princeton methods above, which are visibility boosts, not
values that sum to 100. Never present the number as an empirical prediction.

**Full rubric, content-type matrix, score bands, and report format:**
[references/geo-content-audit.md](references/geo-content-audit.md).

---

### Step 6: Content Quality & E-E-A-T

#### Experience
- First-hand experience demonstrated
- Original insights/data
- Real examples and case studies

#### Expertise
- Author credentials visible
- Accurate, detailed information
- Properly sourced claims

#### Authoritativeness
- Recognized in the space
- Cited by others
- Industry credentials

#### Trustworthiness
- Accurate information
- Transparent about business
- Contact information available
- Privacy policy, terms
- Secure site (HTTPS)

#### Content Depth
- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

---

### Step 7: Content Gap Analysis

1. **Map existing content** -- Inventory all published content and the keywords they target
2. **Identify gaps** -- Compare against keyword clusters. Which clusters have no content?
3. **Competitor content audit** -- What topics do competitors rank for that the company doesn't cover?
4. **Prioritize by opportunity** -- Rank gaps by: search volume, keyword difficulty, relevance to ICP, and alignment with messaging in `/brain/positioning-and-messaging.md`
5. **Recommend content briefs** -- For each priority gap, suggest: target keyword, suggested title, content type (blog, guide, comparison), and key points to cover

---

### Step 8: Validate & Monitor

**Schema Validation**
- Google Rich Results Test: `https://search.google.com/test/rich-results`
- Schema.org Validator: `https://validator.schema.org/`

**Check Indexing**
- Google: `site:domain.com` on Google
- Bing: `site:domain.com` on Bing
- Brave: `site:domain.com` on Brave (for Claude citation)

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content
- AI bots blocked in robots.txt

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages
- No structured data for AI extraction

---

## Output Formats

**Output location:** `marketing/seo/[audit-or-topic-slug]/` — all audit reports and recommendations from a single run share this folder. Confirm the slug with the user before creating files.

### SEO Audit Report

```
**Executive Summary**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Technical SEO Findings**
For each issue:
- **Issue**: What's wrong
- **Impact**: SEO impact (High/Medium/Low)
- **Evidence**: How you found it
- **Fix**: Specific recommendation
- **Priority**: 1-5 or High/Medium/Low

**On-Page SEO Findings**
Same format as above

**Content Findings**
Same format as above

**Prioritized Action Plan**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations
```

### SEO/GEO Optimization Report

```
## SEO/GEO Optimization Report

### Current Status
- Meta Tags: pass/fail
- Schema Markup: pass/fail
- AI Bot Access: pass/fail
- Mobile Friendly: pass/fail
- Page Speed: X seconds
- E-E-A-T Signals: pass/fail

### SEO Recommendations
1. [Priority 1 action]
2. [Priority 2 action]
3. [Priority 3 action]

### GEO Optimizations Applied
- [ ] FAQPage schema added
- [ ] Statistics included with sources
- [ ] Expert citations added
- [ ] Answer-first structure
- [ ] Self-contained answer blocks
- [ ] AI bot access verified

### Platform-Specific Notes
- ChatGPT: [status/recommendation]
- Perplexity: [status/recommendation]
- Google AI Overview: [status/recommendation]
```

### Per-Page Recommendation

```
**Page/Content**: [URL or title]
**Primary keyword**: [keyword]
**Current status**: [ranking position if known, or "not ranking"]
**Recommendation**: [specific action]
**Priority**: High / Medium / Low
**Expected impact**: [brief justification]
```

---

## References

- [AEO & GEO Patterns](references/aeo-geo-patterns.md): Content patterns optimized for answer engines and AI citation
- [GEO Content Audit](references/geo-content-audit.md): File-based scoring rubric, content-type matrix, and report format for grading a content artifact's AI-citation readiness
- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- [Platform Ranking Factors](references/platform-ranking-factors.md): How each AI platform selects sources, plus robots.txt configuration for AI bots
- [Content Patterns](references/content-patterns.md): Templates for extractable answer blocks
- [Content Types](references/content-types.md): Tactical guidance for product pages, blog content, comparison pages, docs, and local/ecom
- [Format Volatility](references/format-volatility.md): The Aug 2026 ChatGPT format shift, per-platform format table, LinkedIn citation data, fan-out extraction, and measurement rigor
- [Citations vs. Recommendations](references/citations-vs-recommendations.md): The visibility ladder (retrieved → cited → mentioned → recommended) and what earns a spot on the shortlist
- [Agent Readiness](references/agent-readiness.md): Access, discovery, and parseability checklist for AI agents and crawlers
- [YouTube AI Citations](references/youtube-ai-citations.md): The text layer AI reads around a video
- [Open Knowledge Format](references/okf.md): Google's markdown spec for representing site content to AI systems
- [International SEO](references/international-seo.md): hreflang, locale URL structure, and multi-region targeting

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?
6. Are you targeting AI engine citations (GEO), traditional rankings (SEO), or both?

---

## MCP Tools: agent-browser

### Technical SEO Auditing with agent-browser

When auditing a live site, use agent-browser for hands-on technical validation:

1. **Navigate to the page** — Run `agent-browser open <url>` to open the target URL.
2. **Check rendered HTML** — Run `agent-browser eval "document.querySelector('title')?.textContent"` to extract meta tags, canonical URLs, heading structure, schema markup, and Open Graph tags from the live DOM.
3. **Accessibility snapshot** — Run `agent-browser snapshot -i` to get the heading hierarchy (H1 → H2 → H3), link structure, image alt text, and ARIA labels. This reveals on-page SEO structure issues at a glance.
4. **Test mobile-friendliness** — Run `agent-browser set viewport 375 812` to switch to mobile viewport, then `agent-browser screenshot` to capture. Check for horizontal scroll, tap target sizes, content visibility.
5. **Check page speed signals** — Run `agent-browser network requests` to audit resource loading: total requests, large images, render-blocking scripts, slow third-party resources.
6. **Console errors** — Run `agent-browser console` to catch JavaScript errors that might block indexing or break page functionality.
7. **Test internal links** — Run `agent-browser click` to follow key internal links and verify they resolve correctly (no 404s, no redirect chains).
8. **Full-page screenshot** — Run `agent-browser screenshot --full` to capture the entire page for visual audit.

**When to use:** Whenever auditing a live site for SEO/GEO issues. agent-browser gives real browser data — rendered DOM, actual network performance, and real mobile behavior — which is more accurate than static analysis.

---

## Related Skills

- **programmatic-seo**: For building SEO pages at scale
- **schema-markup**: For implementing structured data
- **competitor-alternatives**: For comparison and alternative pages
- **page-cro**: For optimizing pages for conversion (not just ranking)
- **tracking-setup**: For measuring SEO performance
- **content-strategy**: For planning what content to create

---

## Field-Tested Rules

- Before recommending SEO/GEO tooling, verify current plans on vendor pricing pages; vendors regularly launch bundled products that don't match older tier structures. Use a browser tool for JS-rendered pricing pages, since plain fetches often return only the JS shell.
- When recommending a paid tool tier, default to the lowest tier that meets current needs (keywords tracked, projects, AI prompts). Flag any critical unverified spec for sales confirmation rather than over-buying headroom.
- When the target has no live web property (pre-launch, or no Search Console/GA4 access), use the file-based GEO content audit (Step 5f) instead of crawl-, SERP-, or Search Console-dependent steps.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->
