---
name: geo
description: "GEO-first SEO analysis tool. Optimizes websites for AI-powered search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining traditional SEO foundations. Performs full GEO audits, citability scoring, AI crawler analysis, llms.txt generation, brand mention scanning, platform-specific optimization, schema markup, technical SEO, content quality (E-E-A-T), and client-ready GEO report generation. Use when user says \"geo\", \"seo\", \"audit\", \"AI search\", \"AI visibility\", \"optimize\", \"citability\", \"llms.txt\", \"schema\", \"brand mentions\", \"GEO report\", or any URL for analysis."
---

# GEO-SEO Analysis Tool — Codex Skill

> **Philosophy:** GEO-first, SEO-supported. AI search is eating traditional search.
> This tool optimizes for where traffic is going, not where it was.

---

## Quick Reference

| Invocation | What It Does |
|---------|-------------|
| `$geo-setup` | Initialize plugin/classic runtime dependencies |
| `$geo-audit <url>` | Full GEO + SEO audit with parallel agents first; skills fallback |
| `$geo page <url>` | Deep single-page GEO analysis (listed for orchestrator routing; no dedicated sub-skill yet) |
| `$geo-citability <url>` | Score content for AI citation readiness |
| `$geo-crawlers <url>` | Check AI crawler access (robots.txt analysis) |
| `$geo-llmstxt <url>` | Analyze or generate llms.txt file |
| `$geo-brand-mentions <url>` | Scan brand mentions across AI-cited platforms |
| `$geo-platform-optimizer <url>` | Platform-specific optimization (ChatGPT, Perplexity, Google AIO) |
| `$geo-schema <url>` | Detect, validate, and generate structured data |
| `$geo-technical <url>` | Traditional technical SEO audit |
| `$geo-content <url>` | Content quality and E-E-A-T assessment |
| `$geo-report <url>` | Generate client-ready GEO deliverable |
| `$geo-report-pdf <url>` | Generate professional PDF report with charts and scores |
| `$geo quick <url>` | 60-second GEO visibility snapshot |
| `$geo-prospect <cmd>` | CRM-lite: manage prospects through the sales pipeline |
| `$geo-proposal <domain>` | Auto-generate client proposal from audit data |
| `$geo-compare <domain>` | Monthly delta report: show score improvements to client |
| `$geo-update` | Pull latest GEO skill updates from upstream |

---

## Market Context (Why GEO Matters)

| Metric | Value | Source |
|--------|-------|--------|
| GEO services market (2025) | $850M-$886M | Yahoo Finance / Superlines |
| Projected GEO market (2031) | $7.3B (34% CAGR) | Industry analysts |
| AI-referred sessions growth | +527% (Jan-May 2025) | SparkToro |
| AI traffic conversion vs organic | 4.4x higher | Industry data |
| Google AI Overviews reach | 1.5B users/month, 200+ countries | Google |
| ChatGPT weekly active users | 900M+ | OpenAI |
| Perplexity monthly queries | 500M+ | Perplexity |
| Gartner: search traffic drop by 2028 | -50% | Gartner |
| Marketers investing in GEO | Only 23% | Industry surveys |
| Brand mentions vs backlinks for AI | 3x stronger correlation | Ahrefs (Dec 2025) |

---

## Orchestration Logic

### Full Audit (`$geo-audit <url>`)

**Phase 1: Discovery (Sequential)**
1. Fetch homepage HTML (curl or WebFetch)
2. Detect business type (SaaS, Local, E-commerce, Publisher, Agency, Other)
3. Extract key pages from sitemap.xml or internal links (up to 50 pages)

**Phase 2: Parallel Agents First, Skills Fallback**
Run these 5 analysis tracks. Prefer launching the matching TOML agents in parallel when they are available under `~/.codex/agents/` or the active Codex environment. If an agent is missing or unavailable, execute only that track directly through the listed skills and rubrics. The scoring formula, findings structure, and output contract are identical in both modes.

| Track | Preferred Agent | Fallback Skills / Responsibility |
|-------|-----------------|----------------------------------|
| AI Visibility | `agents/geo-ai-visibility.toml` | `geo-citability`, `geo-crawlers`, `geo-llmstxt`, `geo-brand-mentions` |
| Platform Analysis | `agents/geo-platform-analysis.toml` | `geo-platform-optimizer` for ChatGPT, Perplexity, Google AIO, Gemini, Bing Copilot |
| Technical GEO | `agents/geo-technical.toml` | `geo-technical` for Core Web Vitals, crawlability, indexability, rendering |
| Content Quality | `agents/geo-content.toml` | `geo-content` for E-E-A-T, readability, source quality, freshness |
| Structured Data | `agents/geo-schema.toml` | `geo-schema` for schema detection, validation, and generation |

**Phase 3: Synthesis (Sequential)**
1. Collect all analysis-track reports
2. Calculate composite GEO Score (0-100)
3. Generate prioritized action plan
4. Output client-ready report

### Scoring Methodology

| Category | Weight | Measured By |
|----------|--------|-------------|
| AI Citability & Visibility | 25% | Passage scoring, answer block quality, AI crawler access |
| Brand Authority Signals | 20% | Mentions on Reddit, YouTube, Wikipedia, LinkedIn; entity presence |
| Content Quality & E-E-A-T | 20% | Expertise signals, original data, author credentials |
| Technical Foundations | 15% | SSR, Core Web Vitals, crawlability, mobile, security |
| Structured Data | 10% | Schema completeness, JSON-LD validation, rich result eligibility |
| Platform Optimization | 10% | Platform-specific readiness (Google AIO, ChatGPT, Perplexity) |

---

## Business Type Detection

Analyze homepage for patterns:

| Type | Signals |
|------|---------|
| **SaaS** | Pricing page, "Sign up", "Free trial", "/app", "/dashboard", API docs |
| **Local Service** | Phone number, address, "Near me", Google Maps embed, service area |
| **E-commerce** | Product pages, cart, "Add to cart", price elements, product schema |
| **Publisher** | Blog, articles, bylines, publication dates, article schema |
| **Agency** | Portfolio, case studies, "Our services", client logos, testimonials |
| **Other** | Default — apply general GEO best practices |

Adjust recommendations based on detected type. Local businesses need LocalBusiness schema and Google Business Profile optimization. SaaS needs SoftwareApplication schema and comparison page strategy. E-commerce needs Product schema and review aggregation.

---

## Runtime Resolution

When a workflow needs bundled scripts, schema templates, or report templates, resolve `GEO_ROOT` in this order:

1. `CODEX_GEO_ROOT` if set.
2. The plugin/repository root that contains this skill's `skills/geo/SKILL.md` plus sibling `scripts/`, `schema/`, and `templates/`.
3. The classic installer path `${CODEX_HOME:-$HOME/.codex}/skills/geo`.

Use `$geo-setup` when dependencies are missing. In plugin mode, the virtual environment can live under `${CODEX_HOME:-$HOME/.codex}/geo-seo-codex/.venv`; in classic installer mode it remains under `~/.codex/skills/geo/.venv`.

---

## Sub-Skills (16 Specialized Components)

| # | Skill | Directory | Purpose |
|---|-------|-----------|---------|
| 1 | geo-audit | `skills/geo-audit/` | Full audit orchestration and scoring |
| 2 | geo-citability | `skills/geo-citability/` | Passage-level AI citation readiness |
| 3 | geo-crawlers | `skills/geo-crawlers/` | AI crawler access and robots.txt |
| 4 | geo-llmstxt | `skills/geo-llmstxt/` | llms.txt standard analysis and generation |
| 5 | geo-brand-mentions | `skills/geo-brand-mentions/` | Brand presence on AI-cited platforms |
| 6 | geo-platform-optimizer | `skills/geo-platform-optimizer/` | Platform-specific AI search optimization |
| 7 | geo-schema | `skills/geo-schema/` | Structured data for AI discoverability |
| 8 | geo-technical | `skills/geo-technical/` | Technical SEO foundations |
| 9 | geo-content | `skills/geo-content/` | Content quality and E-E-A-T |
| 10 | geo-report | `skills/geo-report/` | Client-ready deliverable generation |
| 11 | geo-prospect | `skills/geo-prospect/` | CRM-lite prospect and client pipeline management |
| 12 | geo-proposal | `skills/geo-proposal/` | Auto-generate client proposals from audit data |
| 13 | geo-compare | `skills/geo-compare/` | Monthly delta tracking and progress reports |
| 14 | geo-update | `skills/geo-update/` | Pull latest updates from upstream repository |
| 15 | geo-setup | `skills/geo-setup/` | Initialize or repair plugin/classic runtime dependencies |

---

## Optional Subagents (5 Parallel Workers)

These agents are the preferred fast path for full audits. Do not require them for plugin-only use; fall back to the matching skills when agents are unavailable.

| Agent | File | Skills Used |
|-------|------|-------------|
| geo-ai-visibility | `agents/geo-ai-visibility.toml` | geo-citability, geo-crawlers, geo-llmstxt, geo-brand-mentions |
| geo-platform-analysis | `agents/geo-platform-analysis.toml` | geo-platform-optimizer |
| geo-technical | `agents/geo-technical.toml` | geo-technical |
| geo-content | `agents/geo-content.toml` | geo-content |
| geo-schema | `agents/geo-schema.toml` | geo-schema |

---

## Output Files

All invocations generate structured output:

| Invocation | Output File |
|---------|------------|
| `$geo-audit` | `GEO-AUDIT-REPORT.md` |
| `$geo page` | `GEO-PAGE-ANALYSIS.md` |
| `$geo-citability` | `GEO-CITABILITY-SCORE.md` |
| `$geo-crawlers` | `GEO-CRAWLER-ACCESS.md` |
| `$geo-llmstxt` | `llms.txt` (ready to deploy) |
| `$geo-brand-mentions` | `GEO-BRAND-MENTIONS.md` |
| `$geo-platform-optimizer` | `GEO-PLATFORM-OPTIMIZATION.md` |
| `$geo-schema` | `GEO-SCHEMA-REPORT.md` + generated JSON-LD |
| `$geo-technical` | `GEO-TECHNICAL-AUDIT.md` |
| `$geo-content` | `GEO-CONTENT-ANALYSIS.md` |
| `$geo-report` | `GEO-CLIENT-REPORT.md` (presentation-ready) |
| `$geo-report-pdf` | `GEO-REPORT.pdf` (professional PDF with charts) |
| `$geo quick` | Inline summary (no file) |
| `$geo-prospect` | Updates `~/.geo-prospects/prospects.json` |
| `$geo-proposal` | `~/.geo-prospects/proposals/<domain>-proposal-<date>.md` |
| `$geo-compare` | `~/.geo-prospects/reports/<domain>-monthly-<YYYY-MM>.md` |

---

## PDF Report Generation

The `$geo-report-pdf <url>` invocation converts `GEO-AUDIT-REPORT.md` into a styled, client-ready PDF.

### Requirements
- **pandoc** — install with Homebrew, Chocolatey, Scoop, apt, or your platform package manager
- **Chrome/Chromium-compatible browser** — Google Chrome, Microsoft Edge, Chromium, or Brave

No Python dependencies required for PDF generation.

### What the PDF Includes
- **Cover page** — dark navy gradient, GEO score badge, brand/domain/date/location metadata
- **Color-coded score tables** — cells with `XX/100` values are automatically colored green/blue/amber/orange/red
- **Severity-tagged findings** — Critical/High/Medium/Low sections get colored left-border callout blocks
- **Section page breaks** — major sections break to new pages automatically
- **Styled code blocks** — JSON schema templates render with dark monospace theme

### Templates
Bundled under `${GEO_ROOT}/templates/`:
- `geo-report-style.css` — stylesheet (edit colors, fonts, layout here)
- `geo-report-template.html` — pandoc HTML template (edit cover fields here)

### Workflow
1. Run `$geo-audit <url>` to produce `GEO-AUDIT-REPORT.md`
2. Run `$geo-report-pdf` — extracts metadata from the report and runs:
   ```bash
   pandoc GEO-AUDIT-REPORT.md \
     --to html5 --standalone --embed-resources \
     --template "$GEO_ROOT/templates/geo-report-template.html" \
     --css "$GEO_ROOT/templates/geo-report-style.css" \
     --metadata brand_name="..." --metadata geo_score="..." \
     -o GEO-REPORT.html

   "$GEO_CHROME" \
     --headless=new --disable-gpu --no-sandbox \
     --print-to-pdf="$(pwd)/GEO-REPORT.pdf" \
     --print-to-pdf-no-header --no-pdf-header-footer \
     --virtual-time-budget=5000 \
     "file://$(pwd)/GEO-REPORT.html"
   ```
3. Output: `GEO-REPORT.pdf` in the current directory

---

## Quality Gates

- **Crawl limit:** Max 50 pages per audit (focus on quality over quantity)
- **Timeout:** 30 seconds per page fetch
- **Rate limiting:** 1-second delay between requests, max 5 concurrent
- **Robots.txt:** Always respect, always check
- **Duplicate detection:** Skip pages with >80% content similarity

---

## Quick Start Examples

```
# Full GEO audit of a website
$geo-audit https://example.com

# Check if AI bots can see your site
$geo-crawlers https://example.com

# Score a specific page for AI citability
$geo-citability https://example.com/blog/best-article

# Generate an llms.txt file for your site
$geo-llmstxt https://example.com

# Get a 60-second visibility snapshot
$geo quick https://example.com

# Generate a client-ready report
$geo-report https://example.com
```
