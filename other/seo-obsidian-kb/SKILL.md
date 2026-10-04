---
name: seo-obsidian-kb
description: Build an Obsidian knowledge base from a sitemap — bulk-fetch pages via Python, generate Obsidian-optimized MD notes with parallel agents
trigger: /seo obsidian-kb
---

# /seo obsidian-kb

Build an Obsidian knowledge base from any product website's sitemap. Uses Python for fast bulk-fetching and parallel Claude agents for quality content analysis and MD generation.

## Usage

```
/seo obsidian-kb --sitemap <URL> --product "<Name>" [--vault <path>] [--base-path <path>]
```

**Parameters:**
- `--sitemap` (required): Sitemap URL (e.g., `https://www.zoho.com/campaigns/sitemap.xml`)
- `--product` (required): Product name for folder and tagging (e.g., `"Zoho Campaigns"`)
- `--vault` (optional): Obsidian vault path. Default: `~/Documents/Obsidian Vault`
- `--base-path` (optional): URL base path prefix (e.g., `/campaigns/`). Auto-detected if omitted.

## What You Must Do When Invoked

Follow these steps in order. Do not skip steps.

### Step 1 — Ensure dependencies are installed

```bash
python3 -c "import aiohttp, bs4, lxml" 2>/dev/null || python3 -m pip install aiohttp beautifulsoup4 lxml -q --break-system-packages
```

### Step 2 — Run the Python fetcher

```bash
python3 ~/.claude/skills/seo-obsidian-kb/fetch_pages.py \
  --sitemap "SITEMAP_URL" \
  --output /tmp/seo-obsidian-kb-pages.json \
  --base-path "BASE_PATH" \
  --concurrency 15
```

Replace SITEMAP_URL and BASE_PATH with the user's values (or omit `--base-path` for auto-detection).

Read the output JSON silently. Present a clean summary:

```
Fetched: X / Y pages
Categories: {category: count, ...}
Domain: example.com
```

If `total_pages` is 0: stop with "No pages found. Check the sitemap URL."
If `total_pages` > 300: warn the user and ask if they want to proceed or limit scope.

### Step 3 — Create vault structure

Derive the product folder name from `--product` by lowercasing and hyphenating (e.g., "Zoho Campaigns" → "zoho-campaigns").

Create directories:
```
{vault}/
  _HQ/                    # Only if it doesn't exist
    _SEO Command Center.md
    _Templates/
  {product-folder}/
    {category}/            # One folder per category from the JSON
```

If `_HQ/_SEO Command Center.md` already exists, update it to add the new product row — do NOT overwrite.

### Step 4 — Generate MD notes with parallel agents

This is the critical quality step. Split pages into batches and dispatch parallel agents.

**Batch size:** ~20 pages per agent.
**Model:** Use `sonnet` for the worker agents (fast + quality balance).

**For each agent, provide this exact prompt structure:**

```
You are generating Obsidian knowledge base notes for the product "{product_name}".
Product folder: {product-folder}
Vault path: {vault_path}

For EACH page in the batch below, create a markdown file at:
  {vault_path}/{product-folder}/{category}/{slug}.md

Use this EXACT frontmatter + body template:

---TEMPLATE START---
---
product: {product-folder}
category: {category}
slug: {slug}
alias: "{human-readable title derived from h1 or title}"
url: "{url}"

page_type: {classify as: feature|pricing|comparison|alternative|case-study|landing|blog|integration|docs|homepage}
primary_intent: {classify as: informational|commercial|navigational|transactional}
funnel_stage: {classify as: tofu|mofu|bofu}
target_audience: "{infer from page content and type}"

title: "{title}"
h1: "{h1}"
word_count: {word_count}
has_schema: {true|false}
schema_types: [{list}]

tags:
  - {product-folder}/{category}
  - page-type/{page_type}
  - intent/{primary_intent}
  - status/live
---

# {title or h1}

**URL:** [{url}]({url})
**Product:** [[{product-folder}/_{product_name}|{product_name}]]

## About This Page
{Write 2-3 sentences describing what this page is about, its role in the site, and who it serves. Use the heading outline and meta description to inform this.}

## Page Sections
{Format the headings array as a structured outline:}
### {H2 heading}
- {H3 sub-heading}
- {H3 sub-heading}

## Key Takeaways for LLM Context
{Write 5-8 bullet points summarizing the most important facts Claude should know about this page. Focus on: what the page offers, key features mentioned, CTAs, unique value propositions.}

## Internal Links (Outbound)
{For each resolved_outbound_link, write:}
- [[{target_slug}|{target_title}]] - anchor: "{anchor_text}"

## Internal Links (Inbound)
{For each inbound_link, write:}
- [[{from_slug}|From: {from_category}/{from_slug}]] - anchor: "{anchor_text}"
---TEMPLATE END---

IMPORTANT RULES:
1. page_type classification: pricing pages = "pricing", feature descriptions = "feature", X-vs-Y = "comparison", customer stories = "case-study", product landing = "landing", help/docs = "docs", blog articles = "blog", integration pages = "integration", homepage/index = "homepage"
2. primary_intent: pricing/plans = "commercial", features/how-it-works = "informational", login/signup = "transactional", brand/homepage = "navigational"
3. funnel_stage: awareness/educational = "tofu", evaluation/comparison = "mofu", purchase/signup/pricing = "bofu"
4. Wikilinks use the slug only (Obsidian resolves by filename). For cross-category links, use category/slug format.
5. Write the actual file to disk using the Write tool.
6. If a page has 0 headings, write "No structured headings detected on this page." in Page Sections.
7. Deduplicate inbound/outbound links (same slug appearing multiple times with different anchors — keep the first occurrence).

PAGE BATCH:
{paste the JSON array of page objects for this batch}
```

**Dispatch all agents in a single message for maximum parallelism.**

Wait for all agents to complete. Count total files written.

### Step 5 — Generate category indexes

For EACH category folder, create `_{category}.md`:

```markdown
---
product: {product-folder}
category: {category}
type: category-index
alias: "{Category Name}"
tags:
  - {product-folder}/{category}
  - type/index
---

# {Category Name}

> {page_count} pages in the {category} category for {product_name}

## Pages

| Page | Type | Intent | Words |
|------|------|--------|-------|
{for each page in this category: | [[{slug}\|{alias}]] | {page_type} | {primary_intent} | {word_count} |}

```

### Step 6 — Generate product MOC

Create `{product-folder}/_{product_name}.md`:

```markdown
---
product: {product-folder}
type: product-moc
alias: "{product_name}"
domain: "{domain}"
tags:
  - {product-folder}/moc
  - type/moc
---

# {product_name} Knowledge Base

> {total_pages} pages across {category_count} categories

## Categories

| Category | Pages | Index |
|----------|-------|-------|
{for each category: | {category} | {count} | [[_{category}\|View]] |}

## All Pages by Type

```dataview
TABLE page_type AS "Type", length(rows) AS "Count"
FROM "{product-folder}"
WHERE !contains(tags, "type/index") AND !contains(tags, "type/moc")
GROUP BY page_type
SORT length(rows) DESC
```
```

### Step 7 — Update master MOC

If `_HQ/_SEO Command Center.md` exists, add the new product to the Products table.
If it doesn't exist, create it:

```markdown
---
type: master-moc
alias: "SEO Command Center"
tags:
  - type/moc
---

# SEO Command Center

## Products

| Product | Folder | Pages | Status |
|---------|--------|-------|--------|
| [[{product-folder}/_{product_name}\|{product_name}]] | `{product-folder}/` | {total_pages} | Active |

## How to Use

1. **Navigate by product** — click a product above to see its MOC
2. **Graph view** — each product is color-coded as a distinct cluster
3. **Search** — use Obsidian search or Dataview queries on frontmatter
4. **Claude integration** — Claude reads this vault for context, uses Ahrefs/GSC MCPs for live metrics
```

### Step 8 — Quality verification

After all files are written, verify:

1. **Count files**: `find {vault}/{product-folder} -name "*.md" | wc -l` — should match total_pages + category_indexes + 1 (product MOC)
2. **Spot-check 3 random pages**: Read them and verify frontmatter is complete (all fields populated, no empty strings where data existed)
3. **Check for broken wikilinks**: Grep for `[[` patterns and verify target files exist
4. **Report summary**:

```
=== SEO Obsidian KB Complete ===
Product:    {product_name}
Vault:      {vault_path}
Pages:      {count} notes created
Categories: {count} ({list})
MOC:        {product-folder}/_{product_name}.md
Graph tip:  Open Obsidian > Graph View > filter by tag:#{product-folder}
```

## Frontmatter Schema Reference

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| product | string | CLI arg | Product folder name |
| category | string | Python (URL path) | Category derived from URL |
| slug | string | Python (URL path) | Page slug from URL |
| alias | string | Agent (from h1/title) | Human display name |
| url | string | Python (sitemap) | Full page URL |
| page_type | string | Agent (classified) | feature/pricing/comparison/etc |
| primary_intent | string | Agent (classified) | informational/commercial/etc |
| funnel_stage | string | Agent (classified) | tofu/mofu/bofu |
| target_audience | string | Agent (inferred) | Who this page serves |
| title | string | Python (HTML) | Title tag content |
| h1 | string | Python (HTML) | H1 tag content |
| word_count | int | Python (HTML) | Body text word count |
| has_schema | bool | Python (JSON-LD) | Schema.org markup detected |
| schema_types | list | Python (JSON-LD) | Schema types found |
| tags | list | Agent (generated) | Obsidian tags for graph/filter |

## Notes

- **No SEO metrics stored** — Claude fetches live data from Ahrefs/GSC MCPs when needed
- **Vault is additive** — running for a new product adds to existing vault, never overwrites other products
- **Run `/graphify` after** for community detection and surprise connections across pages
- **Templates** at `_HQ/_Templates/` can be used for manual note creation in Obsidian
