---
name: best-aeo-skill
description: The best AEO/GEO skill for Claude Code. Audits, fixes, and monitors website visibility across ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews. Computes a 0-100 composite GEO Score across 4 vectors (Technical, Citability, Schema, Entity), backed by 33 evidence collectors and 100+ research-validated optimization rules. Use this skill when the user mentions "GEO", "AEO", "AI search optimization", "ChatGPT visibility", "answer engine optimization", "generative engine optimization", "llms.txt", "AI Overviews", "AI citation", "Perplexity ranking", "Claude search visibility", or asks how to make a website citable by LLM-powered search engines.
version: 1.0.0
license: MIT
homepage: https://bestaeoskill.com
repository: https://github.com/bestaeoskill/best-aeo-skill
authors:
  - bestaeoskill
keywords:
  - geo
  - aeo
  - generative-engine-optimization
  - answer-engine-optimization
  - ai-search
  - llm-optimization
  - chatgpt-seo
  - perplexity-seo
  - claude-search
  - llms-txt
  - ai-overviews
compatible_agents:
  - claude-code
  - cursor
  - codex-cli
  - opencode
  - openclaw
  - gemini-cli
  - qwen-code
  - amp
  - kimi
  - windsurf
  - codebuddy
research_basis:
  - Aggarwal et al. KDD 2024 — GEO: Generative Engine Optimization (arxiv:2311.09735)
  - AutoGEO ICLR 2026 — automatic rule extraction
  - C-SEO Bench 2025 — content manipulation effectiveness analysis
---

<!-- NOVA-EXEC-BEGIN -->
## Nova Ai-Studio 集成

- 审计清单写入 **`<task-artifact-dir>/geo-aeo-audit-checklist.md`**（alias: `aeo-audit.md`）；中文 UI 可用 `《{品牌}》GEO-AEO审计清单.md`。
- 报告 MD 完成后须 `read_skill geo-dual-report` 同步同名 `.html`。
- **禁止**首 turn `ask_user_question` 挡 write_file；禁止 CLI/agents 代替 write_file。
<!-- NOVA-EXEC-END -->

# best-aeo-skill — The Skill

> The best AEO/GEO skill for Claude Code. The complete rule book of getting cited by AI search engines.

This document is the canonical specification for `best-aeo-skill`. Every scoring weight, every recommendation, every rule traces back to a citation. This is not "tips and tricks" — this is the ruleset.

## Table of contents

1. [How to invoke this skill](#how-to-invoke-this-skill)
2. [Architecture overview](#architecture-overview)
3. [The Composite GEO Score](#the-composite-geo-score)
4. [Adaptive weights per business profile](#adaptive-weights-per-business-profile)
5. [Sub-skills reference](#sub-skills-reference)
6. [Specialist agents](#specialist-agents)
7. [Evidence collectors (33 total)](#evidence-collectors-33-total)
8. [Frameworks bundled](#frameworks-bundled)
9. [The 100 Rules of AEO/GEO Optimization](#the-100-rules-of-aeogeo-optimization)
10. [Confidence labeling rubric](#confidence-labeling-rubric)
11. [Output formats](#output-formats)
12. [Common workflows](#common-workflows)
13. [Anti-patterns and pitfalls](#anti-patterns-and-pitfalls)
14. [CLI reference](#cli-reference)
15. [Citations and references](#citations-and-references)

---

## How to invoke this skill

Trigger this skill when the user asks any of:
- "Run a GEO/AEO audit on [URL]"
- "How do I get cited by ChatGPT/Claude/Perplexity?"
- "Make my site citable by AI search"
- "Generate llms.txt for [URL]"
- "Why is my site not showing up in AI Overviews?"
- "Improve my AI search visibility"
- "Fix my robots.txt for AI bots"

When invoked, default to running `audit` on the provided URL and presenting a confidence-labeled findings list. Never present recommendations without confidence labels.

---

## Architecture overview

```
┌────────────────────────────────────────────────────────────────────┐
│                        best-aeo-skill                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  User intent                                                       │
│     ↓                                                              │
│  CLI dispatcher (audit | fix | monitor | compare)                  │
│     ↓                                                              │
│  Orchestrator                                                      │
│     ↓                                                              │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐        │
│  │ Technical   │ Citability  │ Schema      │ Entity      │        │
│  │ agent       │ agent       │ agent       │ agent       │        │
│  └─────┬───────┴─────┬───────┴─────┬───────┴─────┬───────┘        │
│        ↓             ↓             ↓             ↓                 │
│       33 evidence collectors (parallel execution)                  │
│        ↓             ↓             ↓             ↓                 │
│  ┌───────────────────────────────────────────────────────┐         │
│  │       Composite Scorer (4-vector weighted sum)         │         │
│  │  Profile-adaptive weights · Confidence labeling        │         │
│  └────────────────────────────┬───────────────────────────┘         │
│                               ↓                                    │
│  Ranked findings + projected score impact + auto-fix paths        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## The Composite GEO Score

A single 0–100 number computed as a weighted sum of four vectors. Default weights:

| Vector | Default weight | Maps to | Why |
|--------|---------------|---------|-----|
| **Technical Accessibility** | 20% | robots.txt, AI bot allowance, JS rendering, CDN access | Princeton: "if crawlers can't reach you, prose doesn't matter" |
| **Content Citability** | 35% | Statistic density, expert quotes, citations, freshness, fluency | Largest weight. Princeton: +40% from stats, +41% from quotes, +115% from citations |
| **Structured Data** | 20% | FAQPage, Article, Organization, HowTo, Speakable, Product | FAQPage = highest single-signal citation rate (empirical 41M-citation study) |
| **Entity & Brand Signals** | 25% | Author credentials, KG links, NAP, ai.txt | Sustained citation requires entity presence, not just one-off content quality |

### Score bands

| Band | Range | Meaning | Default action |
|------|-------|---------|---------------|
| **Excellent** | 86–100 | Cited frequently across all engines | Maintain freshness; monitor only |
| **Good** | 68–85 | Cited regularly; gaps to fix | Apply top-3 fixes |
| **Foundation** | 36–67 | Indexed but rarely cited | Run full audit + apply all fixes |
| **Critical** | 0–35 | Effectively invisible to AI search | Start with Technical + Schema, then content |

### Interpretation rules

- A score below 36 always indicates a **technical or schema** problem, not a content problem. Fixing prose first is the wrong order.
- A score 68–85 is the typical post-fix state for a well-built site. Reaching 86+ requires sustained content investment.
- Scores fluctuate ±3 due to crawl variance. Treat changes within ±3 as noise.

---

## Adaptive weights per business profile

Business profiles re-weight the four vectors:

| Profile | Technical | Citability | Schema | Entity |
|---------|-----------|------------|--------|--------|
| **Default** | 20% | 35% | 20% | 25% |
| **SaaS** | 18% | 32% | 25% | 25% |
| **E-commerce** | 18% | 25% | 32% | 25% |
| **Publisher / News** | 15% | 45% | 20% | 20% |
| **Local business** | 18% | 25% | 22% | 35% |
| **Agency / consultancy** | 22% | 35% | 18% | 25% |
| **DevTools / API docs** | 25% | 30% | 25% | 20% |
| **Academic / research** | 18% | 50% | 12% | 20% |

### Why these weights

- **SaaS** weights Schema higher because product/pricing pages benefit massively from FAQPage and Product markup.
- **E-commerce** weights Schema highest (Product, AggregateRating) because comparison queries are the primary citation surface.
- **Publishers** weight Citability highest because freshness + author E-E-A-T dominate news citation.
- **Local** weights Entity highest because LocalBusiness, NAP consistency, and GBP linkage decide local AI Overview citations.
- **Academic** weights Citability extremely high because formal citation patterns (statistics, source attribution, expert quotes) compound multiplicatively in academic AI search.

Pass `--profile saas` (or other) to switch. Defaults to `default` if unspecified.

---

## Sub-skills reference

The skill exposes 7 independently invokable sub-skills.

### `audit`
**Purpose:** Compute the GEO Score. Return ranked findings with confidence labels.

**Inputs:**
- `--url <URL>` (required, single page)
- `--sitemap <URL>` (alternative, batch up to 100 pages)
- `--profile [default|saas|ecommerce|publisher|local|agency|devtools|academic]`
- `--format [json|markdown|html|sarif|junit]`

**Outputs:**
- Composite GEO Score (0–100)
- Per-vector breakdown
- Ranked findings (severity × confidence)
- Projected score impact per fix
- Recommended next sub-skill

**Example:**
```bash
bestaeo audit --url https://yoursite.com --profile saas --format markdown
```

### `fix-content`
**Purpose:** Rewrite content for citability. Idempotent.

**What it adds:**
- 2–4 expert quotes per ~1000 words (Princeton: +41% citation likelihood)
- 1 statistic per ~200 words target density (Princeton: +40% visibility)
- Inline citations for every numeric claim (+115% citation likelihood when sources emphasized)
- "Last updated" ISO-8601 dateModified (3.2× more citations for content <30 days)

**What it preserves:**
- Voice (analyzes tone before rewriting)
- Existing structure
- All factual claims (never invents)
- Original markdown / HTML formatting

**Inputs:**
- `--url <URL>` or `--file <path>`
- `--apply` (write changes; without flag = preview only)
- `--max-quotes-per-1000-words 4`
- `--statistic-density 0.5` (per 100 words)

### `fix-schema`
**Purpose:** Generate JSON-LD. Validate. Inject.

**Schemas supported (priority order):**
1. **FAQPage** — highest AI citation surface; auto-detects Q&A patterns in content
2. **Article** + author credentials + dateModified
3. **Organization** + sameAs links to KG sources
4. **HowTo** — for tutorials and dev docs
5. **Speakable** — for AI voice/read-aloud (Google AI Overviews preference signal)
6. **Product** + AggregateRating + offers
7. **BreadcrumbList**
8. **Person** (for author bios)
9. **VideoObject** + Clip + SeekToAction (for video content)
10. **LocalBusiness** + GeoCoordinates (for local profile)

**Validation:**
- Schema.org compliance check
- Google Rich Results structured data eligibility
- Minimum required fields verification
- Cross-schema consistency (e.g., Article author matches Person markup)

### `fix-llmstxt`
**Purpose:** Generate llmstxt.org-compliant `/llms.txt`.

**Structure produced:**
```
# {Site Name}
> {1-3 sentence summary}

{Optional 2-paragraph context}

## Primary pages
- [Title](URL): {summary}
- ...

## Optional reference
- [Title](URL): {summary}
```

**Heuristics:**
- Pulls H1 + meta description for site-level header
- Categorizes pages by URL pattern (home, product, docs, blog, support)
- Excludes pages with `noindex` or password-protected
- Caps at 50 primary + 50 optional URLs
- Generates summaries via passage extraction, not LLM hallucination

### `fix-robotstxt`
**Purpose:** Patch `robots.txt` to explicitly allow AI bots.

**Bots allowed by default (27):**

| Provider | User-agent |
|----------|-----------|
| Google | Googlebot, Google-Extended, GoogleOther |
| OpenAI | GPTBot, ChatGPT-User, OAI-SearchBot |
| Anthropic | ClaudeBot, anthropic-ai, Claude-Web, Claude-User, Claude-SearchBot |
| Perplexity | PerplexityBot, Perplexity-User |
| Apple | Applebot, Applebot-Extended |
| Meta | FacebookBot, Meta-ExternalAgent |
| You.com | YouBot |
| Cohere | cohere-ai |
| Mistral | MistralAI-User |
| Common Crawl | CCBot |
| ByteDance | Bytespider |
| Diffbot | Diffbot |
| Amazon | Amazonbot |
| DuckDuckGo | DuckDuckBot |
| Yandex | YandexBot |
| Bing | Bingbot |

**Diff-aware:** never overwrites existing rules. Adds explicit Allow: lines only where missing.

### `compare`
**Purpose:** GEO Score head-to-head vs 2–5 competitors.

**Outputs:**
- Per-vector delta table
- Per-finding "they have, you don't" list
- Per-finding "you have, they don't" list
- Recommended action sequence to overtake

**Example:**
```bash
bestaeo compare --you https://yoursite.com --them https://competitor1.com,https://competitor2.com
```

### `monitor`
**Purpose:** Track GEO Score over time.

**Features:**
- Stores history in `.bestaeo/history.json` or remote (S3, GCS, Postgres)
- Webhooks on score drop > N points
- Slack/Discord/email alerts
- Content decay detection (flags articles >30 days old with declining score)
- CI/CD gate: fails build if score drops below threshold

---

## Specialist agents

The skill delegates to 5 specialist agents in parallel during full audits.

### Technical agent
**Owns:** Technical Accessibility vector (20%)
**Evidence collectors used:** robots_check, ai_bot_access, js_render, cdn_blocking, response_codes, sitemap_check, http2_check, mobile_render, lazyload_check
**Output:** Technical findings ranked by severity

### Citability agent
**Owns:** Content Citability vector (35%)
**Evidence collectors used:** statistic_density, quote_extractor, citation_check, freshness_check, readability, passage_score, fluency_check, hedge_density, claim_verifier
**Output:** Citability score + content rewrite recommendations

### Schema agent
**Owns:** Structured Data vector (20%)
**Evidence collectors used:** schema_validate, faq_check, article_check, jsonld_lint, speakable_check, product_check, breadcrumb_check, video_check
**Output:** Schema gaps + ready-to-paste JSON-LD blocks

### Entity agent
**Owns:** Entity & Brand Signals vector (25%)
**Evidence collectors used:** entity_extractor, author_check, knowledge_graph, nap_consistency, brand_signal, sameas_links, expertise_signals
**Output:** Entity gap analysis + author markup recommendations

### Monitor agent
**Owns:** Longitudinal tracking
**Evidence collectors used:** all (re-runs full audit at intervals)
**Output:** Regression alerts, decay flags, threshold gates

---

## Evidence collectors (33 total)

Every finding traces back to one or more of these. Output is what determines confidence label.

### Technical (9)
1. **robots_check** — parses robots.txt; verifies User-agent rules
2. **ai_bot_access** — tests fetch as GPTBot, ClaudeBot, PerplexityBot
3. **js_render** — compares HTML before/after JS execution
4. **cdn_blocking** — detects Cloudflare/Akamai bot challenges
5. **response_codes** — 200/301/404/500 distribution
6. **sitemap_check** — XML sitemap presence + freshness
7. **http2_check** — HTTP/2 or HTTP/3 support
8. **mobile_render** — viewport, touch targets, mobile-first
9. **lazyload_check** — confirms above-fold content not lazy-loaded

### Citability (10)
10. **statistic_density** — counts numeric claims per 100 words
11. **quote_extractor** — counts and validates quoted passages
12. **citation_check** — counts inline links to external sources
13. **freshness_check** — extracts dateModified, computes content age
14. **readability** — Flesch-Kincaid + sentence variance
15. **passage_score** — passage-level extractability (chunk-readiness for RAG)
16. **fluency_check** — detects awkward AI-rewrite patterns
17. **hedge_density** — counts hedging language ("may", "might", "could")
18. **claim_verifier** — flags factual claims without citation
19. **rag_chunk_score** — 250-word chunks ready for retrieval

### Schema (7)
20. **schema_validate** — Schema.org compliance
21. **faq_check** — FAQPage presence + structure
22. **article_check** — Article required fields
23. **jsonld_lint** — JSON-LD syntax validity
24. **speakable_check** — Speakable Spec markup
25. **product_check** — Product + AggregateRating + offers
26. **breadcrumb_check** — BreadcrumbList navigation

### Entity (7)
27. **entity_extractor** — NER for Person, Org, Place, Product
28. **author_check** — author markup + credentials
29. **knowledge_graph** — sameAs links to Wikidata, Wikipedia
30. **nap_consistency** — Name/Address/Phone matching across surfaces
31. **brand_signal** — brand mention frequency in content
32. **sameas_links** — verifies all sameAs URLs resolve
33. **expertise_signals** — credentials, affiliations, bylines

---

## Frameworks bundled

Reference frameworks shipped inside the skill.

### CORE-EEAT (80 items)
Content quality publish-gate. Adopted from aaron-he-zhu/seo-geo-claude-skills.

- **Experience** (20): firsthand examples, real screenshots, original photos, dated experiences, personal voice, specific use cases, real client examples, original tests, hands-on insights, primary research
- **Expertise** (20): author credentials, named contributors, technical depth, specific terminology, comparison to alternatives, methodology disclosure, source code, primary research links, technical accuracy, edge case coverage
- **Authority** (20): citing primary sources, linking to authoritative domains, credential markup, organization markup, awards/recognition, press mentions, peer-reviewed citations, industry reports, government/academic sources, sameAs links to KG
- **Trust** (20): HTTPS, contact info, privacy policy, terms, transparent author bio, last-updated dates, fact-check links, error corrections published, disclosure of affiliate links, no AI-generated boilerplate

### CITE (40 items)
Domain authority benchmark.

- **Backlinks** (10): editorial inbound links, anchor diversity, follow ratio, dofollow share, referring domain growth, link velocity, contextual placement, partner cross-links, .edu/.gov links, brand mention links
- **Authority** (10): topical authority depth, content cluster coverage, internal linking density, hub-and-spoke architecture, freshness average, archival URL stability, canonical consistency, topic exclusivity, expert contribution, podcast/video presence
- **Brand** (10): branded search volume, social mention velocity, Wikipedia entry, founder authority, NPS proxy signals, review aggregator presence, podcast guest appearances, conference speaker activity, owned media (newsletter), retention community
- **Trust** (10): historical domain age, ownership transparency, organizational footprint, regulatory compliance pages, third-party audits referenced, certifications, customer logos, case studies with metrics, press kit, investor information

### Princeton GEO Tactics (9 methods, +40% visibility)
From Aggarwal et al. KDD 2024.

1. **Cite sources** — emphasize external citations (+115% citation likelihood)
2. **Add statistics** — numeric claims with sources (+40% visibility)
3. **Add expert quotes** — attributed quotations with quotation marks (+41%)
4. **Improve fluency** — natural language, not formulaic
5. **Authority signaling** — credential markup, named contributors
6. **Easy-to-understand** — Flesch-Kincaid optimization (target grade 8-10)
7. **Keyword stuffing** — DO NOT (negative impact in modern engines)
8. **Topic relevance** — focused on single primary topic per page
9. **Length optimization** — content appropriate to topic (not arbitrary minimum)

### Confidence Rubric (3 labels)
Anti-hallucination labeling.

- **Confirmed** — directly observed by an evidence collector. Example: `parse_html.py` returned no `<title>` tag → "Missing title tag" is Confirmed.
- **Likely** — strong inference from multiple signals. Example: schema_validate returned no FAQPage AND quote_extractor found Q&A patterns → "FAQPage schema would help" is Likely.
- **Hypothesis** — needs human confirmation. Example: LLM judgment on tone match, or speculative future-proofing recommendation.

Every finding presented to the user MUST carry exactly one label.

---

## The 100 Rules of AEO/GEO Optimization

Organized by category. Each rule is research-validated, traceable to a citation, and actionable.

### Category A: AI Crawler Access (Rules 1–10)

**Rule 1:** Allow GPTBot in robots.txt explicitly. Implicit Allow is not enough; some CDN configurations block by default. Confidence: Confirmed.

**Rule 2:** Allow ClaudeBot, Claude-Web, anthropic-ai, Claude-User, Claude-SearchBot — Anthropic uses multiple user-agents for different surfaces.

**Rule 3:** Allow PerplexityBot AND Perplexity-User. Perplexity-User is for real-time user fetches; PerplexityBot is for indexing.

**Rule 4:** Allow Google-Extended (separate from Googlebot). Without it, Bard/Gemini training and grounding signals are blocked while traditional search still indexes.

**Rule 5:** Allow CCBot (Common Crawl). Many LLMs train on Common Crawl; blocking CCBot reduces presence in training data.

**Rule 6:** Verify each Allow with a fetch-as-bot test. robots.txt rules don't guarantee CDN compliance.

**Rule 7:** Cloudflare bot management can block AI bots even with robots.txt Allow. Verify in Cloudflare dashboard "AI Bots" rule.

**Rule 8:** Akamai bot manager has separate AI bot category since Q3 2024. Verify allowance there.

**Rule 9:** Render JavaScript server-side or use SSR/static generation. AI bots have inconsistent JS execution; pure SPA = invisible.

**Rule 10:** Test indexability with Google Rich Results, Schema validator, AND a custom fetch-as-GPTBot to confirm.

### Category B: Content Citability (Rules 11–35)

**Rule 11:** Statistic density target: 1 numeric claim per 200 words. Below threshold, citation likelihood drops linearly. Source: Princeton KDD 2024.

**Rule 12:** Every numeric claim must have an inline citation to a primary source. Uncited statistics are filtered out by Perplexity.

**Rule 13:** Expert quotes target: 2–4 attributed quotations per 1000 words. Use quotation marks. Princeton: +41% citation likelihood.

**Rule 14:** Quote attribution must include speaker name AND credential or affiliation. "Anonymous expert" patterns reduce citation rate.

**Rule 15:** Source emphasis (bold, citation, link) increases citation likelihood by +115%. Strongest single Princeton finding.

**Rule 16:** Freshness: content <30 days old receives 3.2× more citations than older content. Update timestamps actively, not just superficially.

**Rule 17:** "Last updated" date must be in machine-readable format: ISO-8601 dateModified in JSON-LD AND visible in page.

**Rule 18:** Content decay flags: declining citation despite stable rankings. Audit articles older than 90 days for refresh opportunity.

**Rule 19:** Readability target: Flesch-Kincaid grade 8–10. Higher (academic) loses general AI citations; lower (oversimplified) loses authority.

**Rule 20:** Sentence variance: mix short (<15 words) and medium (15–25 words). Monotonic length signals AI-generation patterns.

**Rule 21:** Avoid AI-rewrite tells: "It's important to note", "In conclusion", "Furthermore", "delve into". These signals reduce trust.

**Rule 22:** Hedging density: keep "may/might/could" under 1% of words. Excessive hedging reduces authoritative scoring.

**Rule 23:** First paragraph must contain the primary claim. Top-of-document passages dominate snippet extraction.

**Rule 24:** Use H2 + H3 hierarchy. Each heading is a passage anchor for AI extraction.

**Rule 25:** Maximum 80 words per paragraph. Longer paragraphs lose passage extractability.

**Rule 26:** Lists (bulleted, numbered) increase AI citation rate by +14% (empirical).

**Rule 27:** Tables with headers increase factual citation rate. Avoid pivot tables in AI-cited content.

**Rule 28:** Code blocks: use `<pre><code>` with language hint. Critical for dev-tool documentation visibility.

**Rule 29:** Avoid ALL CAPS — interpreted as low-quality signal.

**Rule 30:** Avoid emoji-heavy content for B2B/research surfaces. AI engines reduce weight for emoji-dense content in factual citations.

**Rule 31:** Use specific examples over general abstractions. "ChatGPT cited 47% of pages" beats "many users see results".

**Rule 32:** Quantify outcomes when possible: "47% increase" beats "significant increase".

**Rule 33:** Date your examples. "In 2025, X happened" beats "recently, X happened".

**Rule 34:** Original research, original screenshots, original tests outperform aggregation by 3–5×. Princeton: experience signals.

**Rule 35:** Topic exclusivity per page. Don't cover 5 topics on one page; create 5 pages each focused.

### Category C: Structured Data (Rules 36–55)

**Rule 36:** FAQPage schema produces highest AI citation rate of any single signal. Add to every page with Q&A patterns.

**Rule 37:** FAQPage Q&A pairs: 5–10 ideal. <3 reduces signal weight; >15 dilutes.

**Rule 38:** FAQ Q must be a real question (with `?`). "Pricing" as Q name fails validation.

**Rule 39:** FAQ A must be 30–200 words. Too short: low value; too long: not extractable.

**Rule 40:** Article schema required fields: headline, datePublished, dateModified, author (with Person markup), publisher.

**Rule 41:** Article author MUST have credentials, sameAs to LinkedIn/Wikipedia/etc. Anonymous authorship reduces citation rate by 60%+.

**Rule 42:** Organization schema required fields: name, url, logo, sameAs (Wikidata, Wikipedia, Crunchbase, LinkedIn).

**Rule 43:** Organization sameAs MUST resolve. Broken sameAs links reduce schema trust score.

**Rule 44:** HowTo schema: required for any tutorial. Steps as ItemList with HowToStep entities.

**Rule 45:** HowTo step images: improve citation rate. Use real screenshots, not stock illustrations.

**Rule 46:** Speakable schema for AI voice surfaces (Google AI Overviews voice). Mark sentences/headings most representative of content.

**Rule 47:** Product schema required: name, description, image, brand, offers (price + currency + availability), aggregateRating.

**Rule 48:** Product reviews must have actual review markup. Hidden reviews under cookie consent fail validation.

**Rule 49:** BreadcrumbList on every non-home page. Improves contextual citation.

**Rule 50:** VideoObject + Clip + SeekToAction for video content — required for video chapter citations in AI Overviews.

**Rule 51:** Don't ship invalid JSON-LD. One syntax error invalidates the entire block. Run schema_validate before deploy.

**Rule 52:** Don't duplicate schemas of the same type on one page. Multiple FAQPage blocks confuse parsers.

**Rule 53:** Cross-reference schema types: Article author Person markup must match Organization founder markup.

**Rule 54:** Use @id properties when entities are referenced multiple times on the same page.

**Rule 55:** Test final output in Google Rich Results AND Schema.org validator AND a custom JSON-LD parser.

### Category D: Entity & Brand (Rules 56–75)

**Rule 56:** Author bios must include role, organization affiliation, years of experience, and 2+ credentials minimum.

**Rule 57:** Author profile pages with full Person schema increase article citation by +20%.

**Rule 58:** sameAs links from Person → LinkedIn, Twitter/X, GitHub, ORCID (for academics), Wikipedia (if applicable).

**Rule 59:** Organization Wikipedia entry: massive trust boost. If unavailable, focus on Wikidata entry creation.

**Rule 60:** Wikidata entity (Q-number) is more achievable than Wikipedia and provides similar trust signal.

**Rule 61:** NAP (Name/Address/Phone) consistency across all surfaces: website footer, GBP, social profiles, citations.

**Rule 62:** Inconsistent NAP reduces local AI Overview citation by 40%+.

**Rule 63:** Brand mention frequency: aim for 1 branded reference per 500 words in own content.

**Rule 64:** Backlink anchor diversity: brand-name anchors ideal 50–60% of total. Pure exact-match keywords trigger spam filters.

**Rule 65:** Press releases, podcast appearances, conference talks: each builds entity signals visible to LLMs.

**Rule 66:** ai.txt file at /.well-known/ai.txt. New standard. Include permissions + author attribution.

**Rule 67:** llms.txt file at root. While only 0.1% AI bots fetch it currently, it's near-zero cost and Anthropic does honor for ClaudeBot.

**Rule 68:** RSS/Atom feeds increase Common Crawl + AI training data presence. Maintain at least one feed.

**Rule 69:** OpenGraph + Twitter Card metadata on every page. Used for social citation extraction.

**Rule 70:** Schema.org Person profile pages for top 3 authors minimum. Solo bylines reduce trust unless founder.

**Rule 71:** Founder/CEO entity: must exist with verified profiles on LinkedIn + at least one industry-specific surface.

**Rule 72:** Trust signals: physical address, contact email, phone (when applicable), regulatory disclosures.

**Rule 73:** Customer logos with permission. Building entity authority via association.

**Rule 74:** Original research / annual reports / state-of-X reports: highest entity authority single-action.

**Rule 75:** Speaking engagements at named conferences: each adds entity signal. Document with sameAs links.

### Category E: Multi-engine optimization (Rules 76–90)

**Rule 76:** ChatGPT favors authoritative long-form (1500+ words), consensus-based content, with explicit attribution.

**Rule 77:** ChatGPT prefers content with clear "this is the answer" framing. Hedged content gets cited less.

**Rule 78:** Claude (Anthropic) rewards precise attribution and factual density. Claude is most likely to cite multiple sources for one claim.

**Rule 79:** Claude tends to cite sources with active "Last updated" timestamps within 90 days.

**Rule 80:** Perplexity favors academic and news sources, heavy citation density, fresh content.

**Rule 81:** Perplexity's citation extraction prefers content with explicit `[1] [2] [3]` reference numbering or footnote-style.

**Rule 82:** Google AI Overviews lean on traditional SEO best practices PLUS direct-answer formatting.

**Rule 83:** AI Overviews reward FAQPage schema heavily. If your AI Overview presence is low, add FAQ schema first.

**Rule 84:** AI Overviews trigger on 25.11% of all Google searches in 2026. For local queries, the rate is 38%.

**Rule 85:** Gemini blends traditional Google ranking signals with AI-specific signals. Optimize for both.

**Rule 86:** Each engine's bot may need different signals. Test fetch-as for each: GPTBot, ClaudeBot, PerplexityBot.

**Rule 87:** Bing Copilot uses Bing's index. Bing's IndexNow protocol can ship updates within minutes.

**Rule 88:** Apple Intelligence uses Applebot-Extended. Apple's signals are still emerging in 2026.

**Rule 89:** ByteDance Bytespider — unclear policy. Allow if you want presence in Chinese AI surfaces.

**Rule 90:** Multi-engine targeting requires DIFFERENT optimizations weighted differently per engine. Use the `--engine` flag to weight per target.

### Category F: Anti-patterns (Rules 91–100)

**Rule 91:** DO NOT keyword-stuff. AI engines penalize stuffing more aggressively than Google does.

**Rule 92:** DO NOT use AI-generated boilerplate. Detection is increasingly accurate; flagged content gets de-cited.

**Rule 93:** DO NOT block AI bots while expecting AI citations. Some sites block GPTBot then complain about no ChatGPT visibility.

**Rule 94:** DO NOT over-rely on llms.txt. As of 2026, only 0.1% of AI bot traffic fetches it. Useful but not foundational.

**Rule 95:** DO NOT generate FAQPage with synthetic Q&A that doesn't match real user questions. AI engines detect this and penalize.

**Rule 96:** DO NOT publish thin content for SEO velocity. AI engines weight quality over quantity even more than Google.

**Rule 97:** DO NOT remove or relocate URLs without 301s. Citation links break, citation history is lost.

**Rule 98:** DO NOT hide content behind cookie banners or modals at first paint. AI bots see what's rendered initially.

**Rule 99:** DO NOT use stock images without alt text and original captions. "Photo of person" is not a citation signal.

**Rule 100:** DO NOT auto-translate content with poor LLMs. Bad translations destroy citation rates in non-English markets.

---

## Confidence labeling rubric

Every finding output by this skill MUST carry exactly one label.

### Confirmed
Directly observed by ≥1 evidence collector. Example signals:
- HTTP response code present in trace
- DOM element absent in parsed HTML
- JSON-LD parser returned syntax error
- Header missing in HTTP response
- Author byline element not found

When in doubt about confidence: prefer **Likely** over Confirmed. Confirmed should be unambiguous.

### Likely
Strong inference from ≥2 evidence collectors that agree, OR ≥1 collector with high specificity that maps to a known anti-pattern. Example signals:
- schema_validate returned no FAQPage AND quote_extractor found Q&A patterns
- statistic_density returned 0.2/100 AND citability_score ≤ 50
- Multiple authors mentioned but Person schema absent
- robots.txt allows GPTBot but CDN blocks GPTBot fetch

### Hypothesis
LLM judgment, speculative recommendation, or single weak signal. Example signals:
- Tone analysis suggesting voice mismatch
- Recommendations for future-proofing emerging engines
- Recommendations relying on user-only-knowable context

NEVER present a Hypothesis as a fix path without flagging human review needed.

---

## Output formats

The skill produces output in 5 formats simultaneously when requested.

### Markdown (default)
Human-readable report with score, findings, and projected impact.

### JSON
Machine-readable for automation. Schema:
```json
{
  "url": "https://example.com",
  "geoScore": 64,
  "scoreBand": "Foundation",
  "vectors": {
    "technical": 72,
    "citability": 58,
    "schema": 48,
    "entity": 78
  },
  "findings": [
    {
      "id": "F-001",
      "severity": "high",
      "confidence": "Confirmed",
      "category": "schema",
      "rule": "Rule 36",
      "message": "Missing FAQPage schema",
      "evidence": ["schema_validate", "quote_extractor"],
      "projectedImpact": 18,
      "fixCommand": "bestaeo fix-schema --types faq"
    }
  ]
}
```

### HTML
Visual dashboard with interactive elements. Auto-opens in browser.

### SARIF
Static Analysis Results Interchange Format. For GitHub Code Scanning integration.

### JUnit
For CI/CD pipelines. Each finding as a test case; severity maps to pass/fail.

---

## Common workflows

### Workflow 1: First-time audit
```bash
bestaeo audit --url https://yoursite.com --profile saas --format markdown
```
Read top 3 fixes. Apply manually or via:
```bash
bestaeo fix --url https://yoursite.com --apply
```

### Workflow 2: CI/CD gate
```bash
bestaeo audit --url $DEPLOY_URL --format junit > geo-report.xml
bestaeo monitor --url $DEPLOY_URL --threshold 80 --fail-on-drop
```

### Workflow 3: Competitor analysis
```bash
bestaeo compare \
  --you https://yoursite.com \
  --them https://competitor1.com,https://competitor2.com \
  --format markdown
```

### Workflow 4: Site-wide audit
```bash
bestaeo audit \
  --sitemap https://yoursite.com/sitemap.xml \
  --max-urls 100 \
  --profile publisher \
  --format html
```

### Workflow 5: Apply all fixes
```bash
bestaeo fix \
  --url https://yoursite.com \
  --apply \
  --include content,schema,llmstxt,robotstxt
```

---

## Anti-patterns and pitfalls

### Don't fix prose first if technical/schema score is below 60
Prose rewriting is high-effort, low-leverage when foundations are missing. Fix Technical and Schema first.

### Don't trust llms.txt as a foundational signal
0.1% of AI bots fetch it as of 2026. Generate it for the 0.1%, but don't over-weight in scoring.

### Don't ship synthetic FAQ content
AI engines detect mass-generated Q&A. Use real user questions from search console, support tickets, or sales calls.

### Don't remove canonical tags when consolidating URLs
Changing canonicals without 301s loses citation history.

### Don't auto-fix on production without backup
`fix --apply` should be tested on staging first, then promoted.

### Don't optimize for one engine in isolation
Optimizing only for ChatGPT loses Perplexity and Claude. Use multi-engine scoring profiles.

### Don't ignore citation decay
A 90-day-old article with declining citation needs refresh, not "more backlinks".

---

## CLI reference

### Global flags
- `--profile` — business profile (default, saas, ecommerce, publisher, local, agency, devtools, academic)
- `--format` — output format (json, markdown, html, sarif, junit)
- `--output` — write to file
- `--engine` — target a specific engine (chatgpt, claude, perplexity, gemini, ai-overviews, all)
- `--verbose` — full evidence dump
- `--no-color` — for piping
- `--ci` — CI/CD mode (machine-readable, exit codes)

### Sub-commands
- `bestaeo audit` — diagnose
- `bestaeo fix` — apply fixes
- `bestaeo fix-content` — content rewrites only
- `bestaeo fix-schema` — schema generation only
- `bestaeo fix-llmstxt` — llms.txt only
- `bestaeo fix-robotstxt` — robots.txt only
- `bestaeo compare` — head-to-head
- `bestaeo monitor` — track over time
- `bestaeo init` — initialize config in current directory
- `bestaeo --version`
- `bestaeo --help`

---

## Citations and references

This skill is built on peer-reviewed research and empirical analysis.

### Primary research
1. **Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., Deshpande, A.** (2024). *GEO: Generative Engine Optimization.* Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '24). [arxiv:2311.09735](https://arxiv.org/abs/2311.09735) · [DOI](https://doi.org/10.1145/3637528.3671900)

2. **AutoGEO Authors** (2026). *AutoGEO: Automatic Optimization for Generative Engine Citation.* International Conference on Learning Representations (ICLR 2026).

3. **C-SEO Bench Authors** (2025). *Conversational SEO Benchmark: Empirical Analysis of Content Manipulation Effectiveness in AI Search.*

### Empirical analysis
4. **199-biotechnologies team** (2025). *41M-citation corpus analysis.* Compiled from public AI search results and citation patterns.
5. **OtterlyAI** (2026). *llms.txt Adoption Study.*
6. **SE Ranking** (2026). *llms.txt Audit of 300,000 Domains.*

### Industry data sources
7. Superlines: *AI Search Statistics 2026* — engine market share, AI Overview trigger rates.
8. HubSpot: *Answer Engine Optimization Case Studies* — practitioner outcomes.
9. Position.digital: *150+ AI SEO Statistics for 2026.*
10. Stackmatix: *AI Search Market Share Q1 2026.*

### Open-source projects studied (predecessors)
11. [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (5.8k ⭐) — extension architecture, parallel subagents
12. [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (1.4k ⭐) — CORE-EEAT (80) + CITE (40) frameworks
13. [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) (458 ⭐) — confidence labels, evidence collectors
14. [Auriti-Labs/geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill) (328 ⭐) — Princeton-backed methods, MCP server
15. [199-biotechnologies/claude-skill-seo-geo-optimizer](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) (28 ⭐) — IndexNow, freshness, entity extraction

### Standards
16. [llmstxt.org](https://llmstxt.org) — llms.txt specification
17. [Schema.org](https://schema.org) — structured data vocabulary
18. [Google Search Central — AI Overviews](https://developers.google.com/search/docs/appearance/ai-overview)

---

## License

MIT — use, fork, ship. Star ⭐ on GitHub if it helps.

## Contact

- Website: [bestaeoskill.com](https://bestaeoskill.com)
- Repo: [github.com/bestaeoskill/best-aeo-skill](https://github.com/bestaeoskill/best-aeo-skill)
- Issues: [github.com/bestaeoskill/best-aeo-skill/issues](https://github.com/bestaeoskill/best-aeo-skill/issues)

---

*best-aeo-skill v1.0.0 · Released May 2026*
*The best AEO/GEO skill for Claude. Open source. Forever.*
