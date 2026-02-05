---
name: seo
description: SEO audit and optimization skill for Meryll Dindin's personal portfolio website. Activates when discussing meta tags, Schema.org, structured data, personal branding SEO, search optimization, or content improvements.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# SEO Skill - Helix Portfolio

## Skill Structure

```
seo/
├── SKILL.md              # This file
├── pyproject.toml        # Python dependencies
├── references/           # Context documents
│   └── seo-guidelines.md
└── scripts/              # Python implementation
    ├── seo_audit.py      # Main entry point
    ├── output/           # Audit reports
    ├── validators/       # SEO validation modules
    └── models/           # Pydantic models
```

## Activation Triggers

This skill activates automatically when discussing:

- SEO, meta tags, Schema.org, structured data for the portfolio
- Search engine optimization for personal branding
- Professional profile SEO (LinkedIn, GitHub, social profiles)
- Page performance, Core Web Vitals, technical SEO
- Content optimization, keywords, heading hierarchy
- Review and optimize pages for search traffic

## Commands

Run from the skill root directory:

| Command                                           | Description                           |
| ------------------------------------------------- | ------------------------------------- |
| `uv run python scripts/seo_audit.py --all`        | Full SEO audit (source files)         |
| `uv run python scripts/seo_audit.py --live`       | Live site audit (deployed website)    |
| `uv run python scripts/seo_audit.py --all --live` | Both source and live audits           |
| `uv run python scripts/seo_audit.py --meta`       | Meta tags validation only             |
| `uv run python scripts/seo_audit.py --schema`     | Schema.org validation only            |
| `uv run python scripts/seo_audit.py --content`    | Content analysis (headings, keywords) |
| `uv run python scripts/seo_audit.py --technical`  | Technical SEO checks                  |

### Live Site Validator

The `--live` flag fetches and analyzes the deployed website at `https://merylldindin.com`:

- Verifies robots.txt and sitemap.xml accessibility
- Checks meta tags (title, description, canonical, OG tags)
- Validates heading hierarchy (H1 presence)
- Confirms SSR is rendering content server-side
- Detects JSON-LD structured data presence

## Dependencies

- `pydantic` - Data validation
- `httpx` - HTTP client for live site validation

## Key Website Files

### Meta Management

- `src/content/pages/*.json` - Page-level content with head.\* meta

### Schema.org

- `src/content/schemas/default.json` - Person schema
- `src/content/schemas/website.json` - WebSite schema
- `src/utils/schemas/` - Dynamic schema generators

### Configuration

- `nuxt.config.ts` - Sitemap, runtime config, SEO settings

## SEO Improvement Workflow

1. **Audit**: Run `uv run python scripts/seo_audit.py --all` to identify issues
2. **Review**: Check reports in `scripts/output/`
3. **Fix**: Apply changes to relevant src/ files
4. **Verify**: Re-run specific validators to confirm fixes

## Quick Reference

### Meta Tag Guidelines

- Title: 50-60 characters, keyword-first
- Description: 120-160 characters, compelling summary
- Canonical: Absolute URL with trailing slash
- OG Image: 1200x630px recommended

### Schema.org Types Used

- Person (primary identity)
- WebSite / WebPage
- Article / BlogPosting (thoughts section)
- BreadcrumbList
- ItemList (collections)

### Priority Keywords

**Primary**: Meryll Dindin, AI entrepreneur, data scientist, healthcare AI
**Professional**: machine learning, artificial intelligence, startup founder
**Ventures**: Polygon, Parallel Learning, Dillygence

## Site Architecture

```
/                          → Landing page
/ventures/                 → Companies & projects
/thoughts/                 → Blog/articles
/suggestions/              → Recommendations
/mentions/                 → Press & media
/missions/                 → Mission statement
```
