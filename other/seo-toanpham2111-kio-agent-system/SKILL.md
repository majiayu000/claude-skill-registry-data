---
name: kio-seo
description: Agency-Grade Master SEO & AEO Powerhouse (26 sub-skills, 19 sub-agents & Multi-format Evidence Report Engine). Covers Technical SEO (crawlability, indexability, CWV, status codes), Schema.org JSON-LD, E-E-A-T Content Quality, GEO (AI Overviews, ChatGPT Search, Perplexity), Local SEO/GBP, Programmatic SEO, and Client Reports (HTML/PDF/Markdown).
version: 3.0.0
license: MIT
metadata:
  author: Kio System / Toan Pham
---

# 🔍 Kio SEO & AEO Master Powerhouse

This skill is the **Agency-Grade SEO & AEO Hub**, unifying 26 sub-skills, 19 specialised sub-agents, a Python CLI toolchain and a multi-format report engine (HTML, PDF, Markdown).

---

## 🧭 Command & Feature Matrix (/seo)

The full command list lives in [`subskills/seo/SKILL.md`](subskills/seo/SKILL.md). The most common commands:

| Service Domain | Command | Sub-skill | Core Mission |
|---|---|---|---|
| **Full Site Audit** | `/seo audit <url>` | `subskills/seo-audit/` | Site-wide crawl, structure analysis, technical defects and opportunities |
| **Technical SEO** | `/seo technical <url>` | `subskills/seo-technical/` | 9 technical categories: crawlability, robots, canonicals, status codes, CWV |
| **Single Page Deep** | `/seo page <url>` | `subskills/seo-page/` | One-URL deep dive: title, H1–H6, keyword use, internal links |
| **AI Search / GEO** | `/seo geo <url>` | `subskills/seo-geo/` | AI Overviews, Perplexity, ChatGPT Search, passage citability |
| **Agentic Readiness** | `/seo agentic <url>` | `subskills/seo-agentic/` | AI agent readability (Lighthouse Agentic, WebMCP, llms.txt) |
| **Schema Markup** | `/seo schema <url>` | `subskills/seo-schema/` | Detect, validate and generate Schema JSON-LD for Google Rich Results |
| **E-Commerce SEO** | `/seo ecommerce <url>` | `subskills/seo-ecommerce/` | WooCommerce/Shopify: merchant schema, filter UX, variant SEO |
| **Content & E-E-A-T** | `/seo content <url>` | `subskills/seo-content/` | Content depth, author E-E-A-T, AI-fluff removal |
| **Content Brief** | `/seo content-brief <topic>` | `subskills/seo-content-brief/` | SEO brief: target keywords, search intent, internal links |
| **Topic Cluster** | `/seo cluster <keyword>` | `subskills/seo-cluster/` | Topic clusters and pillar pages |
| **XML Sitemaps** | `/seo sitemap <url>` | `subskills/seo-sitemap/` | Audit, debug and generate XML sitemaps |
| **Image SEO** | `/seo images <url>` | `subskills/seo-images/` | Compression, contextual ALT, IPTC AI metadata, responsive srcset |
| **Local SEO & Maps** | `/seo local <url>`, `/seo maps` | `subskills/seo-local/`, `subskills/seo-maps/` | Google Business Profile, local pack, NAP citations, geo-grid rankings |
| **Programmatic SEO** | `/seo programmatic [url\|plan]` | `subskills/seo-programmatic/` | Template-driven pages at scale, thin-content and index-bloat safeguards |
| **Client Reports** | Node script | `scripts/render-report.mjs` | Generates `seo-audit-report.md`, `.html` and `.pdf` together |

---

## 🛠️ Bundled Python Toolchain

### Running scripts (read first)

Every sub-skill calls scripts as `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run <script.py>` and references docs as `${CLAUDE_PLUGIN_ROOT}/subskills/<name>/...`. In Kio, `CLAUDE_PLUGIN_ROOT` **is this `references/seo/` directory**:

```bash
export CLAUDE_PLUGIN_ROOT="<kio-growth-marketing install dir>/references/seo"   # e.g. ~/.claude/skills/kio-growth-marketing/references/seo
"$CLAUDE_PLUGIN_ROOT/scripts/claude-seo" setup        # only when the user asks (/seo setup): private venv, requirements.txt, Chromium
"$CLAUDE_PLUGIN_ROOT/scripts/claude-seo" doctor --json # readiness check
"$CLAUDE_PLUGIN_ROOT/scripts/claude-seo" run parse_html.py page.html
```

Requires Python 3.11–3.14. Until setup is done you can still run tool-free analysis (reading HTML, judging content) and must say which findings were not verified with tools. Without Chromium, rendered-page features (screenshots, visual analysis) are skipped.

All tools live in [`scripts/`](scripts/):
- **Core Web Vitals**: `pagespeed_check.py`, `crux_history.py`, `lcp_subparts.py`
- **Google Search Console**: `gsc_inspect.py`, `gsc_query.py`, `google_report.py`
- **Schema & Validation**: `schema_generate.py`, `schema_ecommerce_validate.py`
- **AI Agentic & GEO**: `agentic_check.py`, `lighthouse_agentic.py`, `content_quality.py`
- **Sitemap & URL Crawl**: `sitemap_discovery.py`, `render_page.py`, `parse_html.py`
- **HTML & PDF Report Generator**: `render-report.mjs`

---

## 📋 Mandatory Evidence-Based Deliverables

Every professional SEO audit is stored at:
📁 `${PROJECT_ROOT}/seo-reports/YYYY-MM-DD/`

With all **3 standard report files**:
1. 📄 `seo-audit-report.md`: detailed Markdown inventory with severity (Critical/High/Medium/Low).
2. 🌐 `seo-audit-report.html`: polished HTML for the browser.
3. 📕 `seo-audit-report.pdf`: PDF rendered from the HTML via headless Chromium / WeasyPrint.

Render command:
```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/render-report.mjs" \
  --input "${PROJECT_ROOT}/seo-reports/YYYY-MM-DD/audit-data.json" \
  --out "${PROJECT_ROOT}/seo-reports/YYYY-MM-DD"
```

---

## 🛑 Hard Rules

1. **Never promise rankings or a guaranteed #1**: SEO is evidence-based technical and content optimisation.
2. **No fabricated data**: every finding cites a specific URL, a real HTTP status code, or the failing DOM snippet.
3. **Protect production**: never change URL structure, canonicals, robots.txt or 301 redirects without user approval.
4. **Never index sensitive pages**: always `noindex` cart (`/cart`), checkout (`/checkout`), admin (`/wp-admin`) and internal URLs.
