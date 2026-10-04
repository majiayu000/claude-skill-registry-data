---
name: ahrefs
description: Query Ahrefs SEO data — backlinks, domain rating, organic keywords, competitors, and SERP analysis. Use for competitive analysis, link building, and keyword research.
allowed-tools: Bash, Read, Write, WebSearch
env:
  - AHREFS_API_KEY
  - AHREFS_MCP_TOKEN
---

# Ahrefs SEO Analysis Skill

Query Ahrefs API for backlink data, domain metrics, keyword research, and competitive analysis.

## Quick Start (After OAuth)

First authenticate: Run `/mcp` in Claude Code and authorize with Ahrefs.

Then use MCP tools:

```bash
# Domain Rating & Overview
mcp__ahrefs__site-explorer-domain-rating(target="your-domain.com", date="2026-01-26")
mcp__ahrefs__site-explorer-metrics(target="your-domain.com", date="2026-01-26")
mcp__ahrefs__site-explorer-backlinks-stats(target="your-domain.com", date="2026-01-26")

# Top Organic Keywords
mcp__ahrefs__site-explorer-organic-keywords(
  target="your-domain.com",
  date="2026-01-26",
  country="us",
  select="keyword,position,volume,traffic,keyword_difficulty"
)

# Organic Competitors
mcp__ahrefs__site-explorer-organic-competitors(
  target="your-domain.com",
  date="2026-01-26",
  country="us",
  select="domain,common_keywords,org_traffic,domain_rating"
)

# Top Pages by Traffic
mcp__ahrefs__site-explorer-top-pages(
  target="your-domain.com",
  date="2026-01-26",
  select="url,traffic,keywords,top_keyword"
)

# Referring Domains (Backlinks)
mcp__ahrefs__site-explorer-refdomains(
  target="your-domain.com",
  select="domain,domain_rating,backlinks,first_seen"
)

# Keyword Research
mcp__ahrefs__keywords-explorer-overview(
  keywords="your target keyword",
  country="us",
  select="keyword,volume,keyword_difficulty,cpc,traffic_potential"
)

# SERP Analysis
mcp__ahrefs__serp-overview-serp-overview(
  keyword="your target keyword",
  country="us",
  select="position,url,domain_rating,traffic,backlinks"
)
```

## Available MCP Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `site-explorer-domain-rating` | DR score | `target`, `date` |
| `site-explorer-metrics` | Traffic, keywords count | `target`, `date`, `country` |
| `site-explorer-backlinks-stats` | Backlink counts | `target`, `date` |
| `site-explorer-organic-keywords` | What you rank for | `target`, `date`, `country`, `select` |
| `site-explorer-organic-competitors` | Who you compete with | `target`, `date`, `country`, `select` |
| `site-explorer-top-pages` | Best performing pages | `target`, `date`, `select` |
| `site-explorer-refdomains` | Who links to you | `target`, `select` |
| `site-explorer-all-backlinks` | Individual backlinks | `target`, `select` |
| `site-explorer-broken-backlinks` | Broken links to fix | `target`, `select` |
| `keywords-explorer-overview` | Keyword research | `keywords`, `country`, `select` |
| `keywords-explorer-matching-terms` | Keyword ideas | `keywords`, `country`, `select` |
| `serp-overview-serp-overview` | SERP analysis | `keyword`, `country`, `select` |

## When to Use

- **Competitive Analysis**: Compare your domain to competitors
- **Link Building**: Find backlink opportunities, broken links to reclaim
- **Keyword Research**: Discover keywords and their difficulty
- **Content Strategy**: See what pages drive organic traffic
- **SERP Analysis**: Understand ranking difficulty for target keywords

## Configuration

Two authentication methods available:

### Method 1: Remote MCP with OAuth (Recommended)

Uses your Ahrefs subscription with full access to all endpoints.

```bash
# Authenticate via MCP:
/mcp
# Browser opens -> Login to Ahrefs -> Authorize
```

### Method 2: Direct Scripts (Using OAuth Token)

Claude Code stores OAuth tokens in macOS Keychain. After `/mcp` auth, you can extract the token:

```bash
bun .claude/skills/ahrefs/scripts/get-ahrefs-token.ts
bun .claude/skills/ahrefs/scripts/get-ahrefs-token.ts --json
```

## Common Use Cases

### 1. Competitor Analysis
```bash
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts overview competitor.com
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts keywords competitor.com 50
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts competitors your-domain.com
```

### 2. Link Building
```bash
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts refdomains your-domain.com 50
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts broken-backlinks your-domain.com
```

### 3. Keyword Research
```bash
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts keyword-overview "your keyword"
bun .claude/skills/ahrefs/scripts/ahrefs-api.ts serp "your keyword"
```

## API Limits

Ahrefs API uses units. Each call consumes units based on complexity:
- Simple metrics (DR): ~1 unit
- Backlinks list: ~5-10 units
- Keyword research: ~10 units

Monitor your usage at: https://app.ahrefs.com/api-profile
