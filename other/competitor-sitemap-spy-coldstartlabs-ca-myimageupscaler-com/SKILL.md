---
name: competitor-sitemap-spy
description: Inspect a competitor's sitemap to reverse-engineer their SEO strategy and find traffic you can steal. Use when asked to "analyze competitor sitemap", "spy on competitor pages", "reverse engineer competitor SEO", "steal competitor traffic", or "find content gaps from competitor".
user_invocable: true
argument_description: "<competitor-domain> e.g. upscale.media or imgupscaler.com"
---

You are an elite competitive SEO analyst. Your job is to crawl a competitor's sitemap, categorize every URL they have, identify their content strategy, and produce a battle plan to steal a chunk of their organic traffic.

## Workflow

### Step 1: Identify the Competitor

Get the competitor domain from the user's argument. If none provided, ask.

### Step 2: Fetch & Parse the Sitemap

Fetch the competitor's sitemap systematically. Try these in order:

```
1. https://{domain}/sitemap.xml
2. https://{domain}/sitemap_index.xml
3. https://{domain}/robots.txt (look for Sitemap: directive)
4. https://www.{domain}/sitemap.xml
```

If the sitemap is a **sitemap index** (contains `<sitemap>` entries), fetch each child sitemap too.

Use `WebFetch` to retrieve each sitemap URL with the prompt: "Extract ALL URLs from this XML sitemap. Return them as a plain list, one URL per line. If this is a sitemap index, list the child sitemap URLs."

Collect **every URL** into a master list. For large sitemaps (1000+ URLs), work in batches and keep a running count.

### Step 3: Categorize URLs

Group every URL into categories by analyzing the URL path patterns. Common categories:

| Category | Pattern Examples |
|----------|----------------|
| Homepage | `/`, `/home` |
| Tool/App Pages | `/upscale`, `/enhance`, `/process` |
| Image-Type pSEO | `/upscale-{type}`, `/{type}-upscaler` |
| Format-Specific pSEO | `/upscale-{format}`, `/{format}-enhancer` |
| Blog/Content | `/blog/*`, `/articles/*`, `/guides/*` |
| Comparison Pages | `/vs/*`, `/*-vs-*`, `/alternative*` |
| Landing Pages | `/features/*`, `/solutions/*`, `/use-cases/*` |
| Legal/Info | `/privacy`, `/terms`, `/about`, `/contact` |
| Help/Support | `/help/*`, `/faq/*`, `/support/*` |
| API/Docs | `/api/*`, `/docs/*`, `/developers/*` |

For each category, count the number of URLs and list 5-10 representative examples.

### Step 4: Analyze Their pSEO Strategy

If they have programmatic SEO pages (image-type-specific, format-specific, etc.):

1. **Count total pSEO pages** - How many templated pages?
2. **Identify the template patterns** - What variables do they use? (image type, format, use case, etc.)
3. **Estimate keyword coverage** - What keyword clusters do these pages target?
4. **Spot gaps** - What combinations are they MISSING?

For each pSEO pattern found, fetch 2-3 sample pages with `WebFetch` and analyze:
- Title tag pattern
- H1 pattern
- Content structure (headings, sections)
- Internal linking strategy
- Schema markup used
- Word count estimate
- Unique vs. templated content ratio

### Step 5: Cross-Reference with Our Pages

Check what WE already have vs. what they have:

1. Read our sitemap data from `lib/seo/` directory
2. Look at our pSEO pages in `app/seo/data/` JSON files
3. Check our sitemap generation in `app/sitemap-*.xml/` routes
4. Identify:
   - **Pages they have that we DON'T** (content gaps)
   - **Pages we have that they DON'T** (our advantages)
   - **Pages both have** (head-to-head competition)

### Step 6: Traffic Estimation

For their top page categories, estimate traffic potential:

| Signal | How to Assess |
|--------|--------------|
| Search volume | Use keyword patterns + known data from `docs/SEO/keywords/` |
| Their likely traffic share | Pages with high intent keywords in URL = higher traffic |
| Our ability to compete | Based on our DR, existing content, and pSEO capability |

Rate each opportunity:
- **Impressions potential**: Low / Medium / High / Very High
- **Competition difficulty**: Easy / Medium / Hard
- **Implementation effort**: Quick Win / Medium / Major Project
- **Priority score**: 1-10 (weighted: potential 40%, difficulty 30%, effort 30%)

### Step 7: Produce the Battle Plan

## Output Format

```markdown
# Competitor Sitemap Intelligence: {domain}

**Analyzed**: {date}
**Total URLs found**: {count}
**Sitemap structure**: {index with N child sitemaps / single sitemap}

---

## Sitemap Breakdown

| Category | Count | % of Site | Examples |
|----------|-------|-----------|----------|
| ... | ... | ... | ... |

## Their pSEO Strategy

### Pattern 1: {description}
- **URL pattern**: `/{pattern}`
- **Total pages**: {N}
- **Title template**: "{template}"
- **Target keywords**: {keyword cluster}
- **Sample pages analyzed**: {list}

### Pattern 2: ...

## Content Strategy Summary

**What they're doing well:**
1. ...

**Their weaknesses:**
1. ...

## Content Gap Analysis

### Pages They Have That We Don't (OPPORTUNITIES)

| Their URL Pattern | Est. Pages | Keyword Cluster | Traffic Potential | Priority |
|-------------------|-----------|-----------------|-------------------|----------|
| ... | ... | ... | ... | ... |

### Pages We Have That They Don't (OUR EDGE)

| Our URL Pattern | Count | Advantage |
|-----------------|-------|-----------|
| ... | ... | ... |

## Traffic Steal Battle Plan

### Phase 1: Quick Wins (1-2 weeks)
Pages we can create immediately using existing pSEO infrastructure.

| Action | Target Keywords | Est. Monthly Searches | Effort |
|--------|----------------|----------------------|--------|
| ... | ... | ... | ... |

### Phase 2: Content Expansion (2-4 weeks)
New content types or page categories to build.

| Action | Target Keywords | Est. Monthly Searches | Effort |
|--------|----------------|----------------------|--------|
| ... | ... | ... | ... |

### Phase 3: Strategic Moves (1-3 months)
Bigger initiatives to capture significant traffic share.

| Action | Target Keywords | Est. Monthly Searches | Effort |
|--------|----------------|----------------------|--------|
| ... | ... | ... | ... |

## Estimated Traffic Capture

| Phase | New Pages | Est. Monthly Traffic | Timeline |
|-------|-----------|---------------------|----------|
| Quick Wins | ... | ... | 1-2 weeks |
| Expansion | ... | ... | 2-4 weeks |
| Strategic | ... | ... | 1-3 months |
| **Total** | **...** | **...** | |

## Recommendations

1. **Highest priority**: ...
2. ...
3. ...
```

## Important Guidelines

- **Be specific** - Don't say "create blog posts". Say "create 15 image-type-specific upscaling guide pages targeting `upscale {type} image` keywords".
- **Show your math** - When estimating traffic, explain the reasoning.
- **Prioritize ruthlessly** - Not everything is worth doing. Rate and rank.
- **Reference our existing infrastructure** - We have a pSEO system. Recommend actions that leverage it.
- **Cross-reference GSC data** - If available in `docs/SEO/gsc-exports/`, use real impression data to validate opportunity size.
- **Cross-reference keyword research** - Check `docs/SEO/keywords/` for volume data.
- **Save the report** - Write the final report to `docs/SEO/competitors-report/{domain}-sitemap-analysis-{date}.md`

## Tools Used

- `WebFetch` - Fetch sitemaps and sample pages
- `WebSearch` - Supplemental research on competitor
- `Read` / `Glob` / `Grep` - Cross-reference with our own sitemap and pages
- `Write` - Save the final report
