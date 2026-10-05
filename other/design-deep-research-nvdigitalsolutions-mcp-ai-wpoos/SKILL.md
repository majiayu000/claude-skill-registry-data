---
type: Skill
name: design-deep-research
description: Perform comprehensive, multi-source research on any topic using AI-powered web search and analysis. Covers deep_research for broad discovery and semantic_content_search for site-specific knowledge retrieval. Use when you need to research brands, markets, competitors, or trends with citations — before creating content, planning campaigns, or making strategic decisions.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Deep Research

Use this skill when the task requires thorough, multi-source research with citations — more depth than a quick web search.

## Available Tools

| Tool | Purpose | Depth |
|---|---|---|
| `deep_research` | Multi-step web search + AI analysis with citations | Comprehensive — generates full reports |
| `semantic_content_search` | Search site content via vector embeddings | Finds related content already on your WordPress site |
| `search_content` | Hybrid keyword + semantic search of site content | Use `search_type: "hybrid"` for best results across your content |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for research workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai harness` | Semantic search across stored content |
| `wp mcp-ai health` | Check search/tool connectivity |
| `wp mcp-ai memory` | Review stored research context |

## When to use this skill

Trigger when ANY of the following is true:

- The task asks to "research", "investigate", or "do a deep dive" on a topic.
- Building a brand or company profile for marketing purposes.
- Researching a market, industry trend, or competitive landscape.
- The task requires citations, sources, and substantiated findings.
- "Find out everything about X" — breadth + depth matters.
- Preparing a research report that will inform a campaign, content piece, or strategy.
- The task mentions "deep research", "comprehensive research", or "multi-source".

## `deep_research` — Comprehensive Topic Research

Use for broad, multi-source investigation. Performs multi-step web searches, AI analysis, and generates a structured report with citations.

### Parameters

```
topic          — The research topic or question (required)
depth          — "basic" | "standard" | "comprehensive" (default: "standard")
focus_areas    — Optional specific aspects: ["technical", "historical", "pricing", "competitors"]
include_sources — Include source citations (default: true)
run_mode       — "immediate" (synchronous) | "background" (WordPress cron)
include_site_content — Search WordPress + Vector Store alongside web (default: true)
memory_agent_id — Recall prior research from agent memory before starting
store_to_memory — Auto-store report in agent memory (requires memory_agent_id)
```

### Depth Selection

| Depth | When | Example |
|---|---|---|
| **basic** | Quick overview, fact-checking, simple questions | "What are the top fragrance brands in Sri Lanka?" |
| **standard** | Marketing research, brand profiles, campaign prep | "Research Conatural — history, products, target market, competitors" |
| **comprehensive** | Competitive analysis, market reports, strategic planning | "Full analysis of Sri Lanka's luxury fragrance e-commerce market" |

### Focus Areas

Guide the research by specifying aspects:

```
For a brand:    ["history", "product range", "pricing", "target audience", "competitors"]
For a market:   ["market size", "trends", "key players", "consumer behavior", "growth forecast"]
For a trend:    ["origins", "current state", "adoption", "future outlook", "Sri Lanka context"]
For a competitor: ["products", "pricing", "marketing channels", "USPs", "weaknesses"]
```

### Run Modes

| Mode | When | Time |
|---|---|---|
| **immediate** | Interactive tasks where you need results now | 30s–2min |
| **background** | Long research, non-urgent, large scope | Minutes to hours |

Use `immediate` for most Sophie tasks. Use `background` for comprehensive market reports or when researching 10+ entities.

### Output

Returns:
- **Report** — structured findings with sections
- **Sources** — URLs with type labels (manufacturer, retailer, news, etc.)
- **Product data** (if applicable) — specs, pricing, images, attributes
- **SEO keywords** — extracted from research for content optimization

### Example

```
deep_research {
  topic: "Conatural skincare brand — history, product range, target market,
          certifications, competitors in Sri Lanka"
  depth: "standard"
  focus_areas: ["brand history", "product categories", "certifications",
                "pricing strategy", "Sri Lanka market position"]
  include_sources: true
  run_mode: "immediate"
}
```

## `semantic_content_search` — Site Knowledge Retrieval

Search your own WordPress content (posts, pages, products) by meaning, not just keywords. Uses vector embeddings for semantic matching.

### Parameters

```
query          — Natural language search query
post_types     — Post types to search (default: ["post", "page"])
limit          — Max results (default: 10, max: 100)
threshold      — Minimum similarity score 0–1 (default: 0.7)
vector_store_id — Optional OpenAI vector store ID
include_meta   — Include post metadata (default: false)
```

### When to use

- "Have we written about this before?" — check for existing content
- "What products are related to X?" — find semantically similar products
- "Find all content about Sri Lankan luxury market" — thematic search
- Before creating new content — avoid duplication

### Example

```
semantic_content_search {
  query: "luxury fragrance gifting ideas for Sri Lankan customers"
  post_types: ["post", "product"]
  threshold: 0.75
  limit: 10
}
```

## Research Workflow

For a typical research task, follow this sequence:

```
1. SITE CHECK (optional)
   semantic_content_search → "Do we already have content on this?"

2. DEEP RESEARCH
   deep_research {
     topic: "..."
     depth: "standard"
     include_sources: true
   }

3. EXTRACT INSIGHTS
   From the report, pull:
   ● Key facts (for content)
   ● Competitor intel (for positioning)
   ● Market gaps (for campaign angles)
   ● Sources (for citations and further reading)

4. ACT ON IT
   → Feed findings into campaign orchestration
   → Create a WordPress post via create_post_from_research
   → Save to Paper Store for future reference
```

## Paper Store Integration (on request)

When explicitly asked to persist research:

```
paper_store_write {
  collection: "research-reports"
  id: "topic-slug"
  title: "Research: [Topic]"
  connection_id: "conn_8srcad8zylhe"
  tags: ["deep-research", "topic-tag", "brand-tag"]
  body: {
    topic: "..."
    report: "..."
    key_findings: [...]
    sources: [...]
    researched_at: "YYYY-MM-DD"
  }
}
```

## Critical Rules

- **Match depth to need** — a brand overview doesn't need `comprehensive`. Save that for competitive analysis.
- **Always include sources** — citations make research actionable and credible.
- **Use focus areas** — they dramatically improve report quality by guiding the AI.
- **Check site content first** — `semantic_content_search` prevents duplicating work already done.
- **Feed research into action** — research without application is wasted. Every report should inform a decision, campaign, or piece of content.
- **Store when asked** — persist to Paper Store only when the user requests it.

## Common Mistakes

```
WRONG:
  ● Using deep_research for "What's 2+2?" (use web_search for quick facts)
  ● Running comprehensive depth for a 2-minute task
  ● Not specifying focus_areas (generic report, misses what you need)
  ● Researching without a purpose — no link to campaign, content, or decision
  ● Saving every research to Paper Store automatically

RIGHT:
  ✅ deep_research for multi-source, cited, structured reports
  ✅ web_search for quick fact checks
  ✅ standard depth for most marketing research tasks
  ✅ Specific focus_areas tied to what you'll do with the results
  ✅ Research → insight → action chain
  ✅ Paper Store only when explicitly requested
```

## What This Skill Does NOT Cover

- **Quick fact-checking** — use `design-web-research` for fast lookups via `web_search` or `brave_web_search`.
- **Product-specific research** — use `design-product-research` for structured SKU/catalog investigations via `research_product`.
- **Content writing** — use `design-content-research` to convert research into WordPress draft posts via `create_post_from_research`.
- **Campaign planning** — use `design-campaign-orchestration` to apply research insights to campaign themes and calendars.
- **SEO implementation** — use `design-seo-content` to apply research keywords to product/category pages.
- **Image or visual research** — use `analyze_image` or `design-image-generation` for visual reference gathering.

## Cross-references

- Run **`design-web-research`** for quick web searches — use `web_search` or `brave_web_search` instead of `deep_research`.
- Run **`design-product-research`** for structured product-specific research — use `research_product`.
- Run **`design-content-research`** to convert research into WordPress drafts — use `create_post_from_research`.
- Run **`design-campaign-orchestration`** to apply research insights to campaign planning.
- Run **`design-seo-content`** to use research keywords in product and category pages.
- Use **`paper_store_*`** with `connection_id` to persist research reports to specific sites.
