---
name: marty-needs-an-idea
description: find mundane products with oddly specific review comments on live amazon, walmart, target, chewy, home depot, lowe's, etsy, and other retail product pages. use when the user wants funny reviews, bizarre reviews, oddly specific customer comments, direct product urls, or fresh retail review examples. prioritize live product detail pages with visible review text or review snippets. reject listicles, roundup articles, screenshot galleries, and retailer search urls in final output. ask for review tone when missing. write findings to a timestamped markdown file.
---

# Marty Needs an Idea

Find and document oddly specific reviews for mundane products, prioritizing live retail product detail pages with visible review text, review snippets, or retailer-provided review summaries.

## Core Rule

This is a live product-page retrieval task, not a roundup-content task.

Final answers must contain only live direct product detail page URLs. Search pages, listicles, roundup articles, affiliate pages, social reposts, archived pages, and fallback links are not allowed in final output unless the user explicitly asks for fallback sources.

## When to Use

Use this skill when the user wants:
- funny product reviews
- oddly specific customer comments
- bizarre Amazon or Walmart reviews
- unhinged reviews for mundane products
- direct product URLs with weird review text
- fresh retail review examples for content creation, entertainment, or research

## Workflow

```text
Step 1: Clarify tone and scope if missing
Step 2: Build a broad candidate pool from retail domains first
Step 3: Exclude repeats and same-category clustering
Step 4: Verify each candidate on a live product detail page
Step 5: Rank for novelty, specificity, category spread, and freshness
Step 6: Write a timestamped markdown file
Step 7: Format with prettier if available
```

## Step 1: Clarify Tone First

Before searching, ask the user only for missing high-value inputs. Keep it short.

Preferred clarifications:
1. **Review Tone**: Extremely Positive, Neutral, Negative, or Unhinged?
2. **Purpose**: Entertainment/Fun, Research/Analysis, Content Creation, or Other?
3. **Categories**: Household Basics, Personal Care, Office/School Supplies, Any Mundane Products, or Specific Category?
4. **Specific Product Name**: A product name to target, or leave it open-ended.
5. **Output Format**: List with Links, Detailed Report, Just Examples, or Search Strategy?

If the user does not specify:
- default tone to **unhinged**
- default purpose to **content creation**
- default category to **any mundane products**
- default output to **list with links**

## Step 2: Search Strategy

### Source Rules

#### Hard requirements
- Return only direct product detail page URLs in the final answer.
- Every final result must point to a single specific product.
- Prefer canonical PDPs from Amazon, Walmart, Target, Chewy, Home Depot, Lowe's, Etsy, and brand storefronts.
- Verify each result on the live product page before keeping it.

#### Hard rejects for final output
Never include these in the final answer:
- listicles
- roundup articles
- screenshot galleries
- “funniest reviews” blogs
- retailer search result pages
- Google or Bing search result pages
- category pages
- affiliate redirect pages
- social reposts
- forum threads
- archived pages

#### Allowed only for discovery
You may use listicles, articles, forums, or search results only to discover candidate products. If you do:
1. extract the candidate product
2. open the live direct product page
3. verify the review text or review summary there
4. discard the candidate if you cannot verify it on the product page

If a live direct product page is unavailable, discard the result and find another product. Do not substitute search pages, archives, or blog posts unless the user explicitly asks for fallback sources.

### Retail-First Search Preference

Prefer retail-domain discovery before broad web searches.

Start with query shapes like:
- `site:amazon.com [category] review`
- `site:walmart.com [category] review`
- `site:target.com [category] review`
- `site:chewy.com [category] review`
- `site:homedepot.com [category] review`
- `site:lowes.com [category] review`

Only broaden beyond retail domains if needed to generate leads.

### Primary Search Queries

Run multiple searches in parallel with category, tone, and freshness variations. Always include at least one explicit unhinged branch in the candidate pool, even when the requested tone is not unhinged.

```text
Query variations:
- site:amazon.com [category] review
- site:walmart.com [category] review
- site:target.com [category] review
- site:chewy.com [category] review
- [category] oddly specific review amazon newest
- [category] oddly specific review walmart recent
- [category] funny review specific complaint current year
- [category] best ever review amazon recent
- [category] worst purchase review amazon verified purchase
- [category] neutral review oddly specific newer
- [category] unhinged review mundane product recent
- [category] absolutely not review amazon
- [category] what is happening review walmart
- [category] this product has seen things review
```

### Pattern-Based Searches

Also search for phrases that often signal weirdly specific reviews:
- `tastes like`
- `looks like`
- `waste of money`
- `save yourself`
- `I have tasted better`
- `cardboard`
- `sawdust`
- `broke immediately`
- `changed my life`
- `works fine`
- `nothing special`

Use these only to surface candidate products. Final results still must be verified on direct product pages.

### URL Heuristics

Prefer URLs that look like product detail pages.

Good signs:
- Amazon `/dp/`
- Walmart product detail paths
- retailer-specific product slug pages
- a title, price, rating, and review count all on one page

Reject URLs that look like:
- `search?q=`
- `/search`
- `/s?`
- `/browse`
- `/category`
- `/collections`
- `utm_`
- redirect wrappers
- deal aggregator links

### Freshness Rules

Treat freshness as a hard filter.
- Prefer active product pages with visible recent review dates, newer ratings, or a sort-by-newest view.
- Prefer results with current-year review activity when visible.
- Reject old recycled internet-famous examples when fresher options exist.
- If the best evidence is only an old roundup or stale viral example, keep searching.

### Anti-Repeat Rules

Before accepting any result, prefer items that are different from recent picks in at least two ways:
- product category
- platform
- price band or use case
- review angle or complaint type
- recency or active review stream

If the user did not provide exclusions, still avoid clustering around the same evergreen examples. Keep a candidate bank of at least 8 to 12 products, then choose the most varied final set.

### Category Rotation

Spread searches across rotating mundane categories:
- pantry and snacks
- cleaning supplies
- bathroom basics
- office and school supplies
- small kitchen tools
- laundry and storage
- personal care and grooming
- pet supplies
- automotive accessories
- gardening and household hardware

### Review Tone Targets

Adjust search terms based on the chosen tone:
- **Extremely Positive**: `love this`, `best ever`, `changed my life`, `would buy again`
- **Neutral**: `does the job`, `as expected`, `nothing special`, `works fine`
- **Negative**: `waste of money`, `cardboard`, `broke immediately`, `save yourself`
- **Unhinged**: `I did not expect`, `absolutely not`, `what is happening`, `this product has seen things`

When ranking results, keep at least one unhinged candidate in the final set if a strong one exists, even if the requested tone is different.

## Step 3: Exclude Previously Covered Items

If the user provides already-covered products or links:
- parse exclusions
- skip results matching those ASINs or product IDs
- note exclusions in the final report

## Step 4: Verify and Compile Findings

For each candidate, perform this verification workflow:

1. Find a candidate product.
2. Open the direct product page.
3. Confirm the URL is a product detail page, not a search or category page.
4. Confirm the page visibly shows:
   - product title
   - rating and/or review count
   - at least one visible review snippet, review text, or retailer-provided review summary
5. Keep the result only if all checks pass.

Discard the candidate if:
- the URL is a search, category, or roundup page
- the page is not clearly a single product
- review text or a review summary cannot be verified on the live product page
- the listing appears dead, redirecting, or no longer useful

For each valid finding, capture:

| Field | Description |
| --- | --- |
| Product Name | Full product name |
| Platform | Amazon/Walmart/Target/Chewy/etc. |
| Direct Product URL | Canonical live product detail page |
| Review Snippet or Summary | Visible review text or visible retailer review summary |
| Specifics | What makes it oddly specific |
| Review Date | Date of the cited review, if visible |
| Freshness | Why this source counts as current |
| Rating | Product rating and review count |
| Helpfulness | Helpful-vote count if visible |

Do not keep separate “source URL” fields unless they are also direct product pages.

### Categories to Find

1. Food products with vivid taste comparisons or praise
2. Kitchen gadgets that fail spectacularly
3. Cleaning tools with specific complaints
4. Small appliances with bizarre failures
5. Store-brand products that disappoint
6. Personal care items with unusually exact reactions
7. Office and school supplies with weirdly detailed failures
8. Pet products with surprisingly specific praise or complaints

### Common Themes to Look For

- vivid sensory comparisons
- hyperbolic specificity
- exact measurements, times, or percentages
- social impact on coworkers or family
- inefficiency comedy
- design flaws with exact consequences
- product-page review snippets that surface the complaint without needing a locked review URL
- rare, specific use cases

### Selection Rules

When multiple valid candidates are available, prefer the set that:
- covers more categories
- mixes platforms instead of using only one retailer
- includes at least one non-obvious product
- includes at least one unhinged result if supported by the pool
- has active listings with recent review activity
- avoids the same flagship examples unless explicitly requested

Before returning results, run this final check:
- Is every URL a live direct product page?
- Would the user land directly on the product without needing another search?
- Did any listicle, article, search result, archive, or category URL slip into the final set?

If yes, fix before responding.

## Step 5: Write Markdown File

### File Naming Convention

```bash
date +"%Y-%m-%d_%H-%M-%S"
```

Use:
```text
YYYY-MM-DD_HH-MM-SS_source_material.md
```

### Directory

Write to:
```text
/home/tully/Sync/marty/
```

### Template

```markdown
# Detailed Report: Reviews for Mundane Products

**Date Compiled:** [Timestamp]  
**Purpose:** [User's stated purpose]  
**Review Tone:** [Extremely Positive / Neutral / Negative / Unhinged]  
**Requested Product Name:** [Exact product name, if provided]

---

## Executive Summary

[Brief description of findings]

---

## Product Links & Findings

### 1. [Category Name]

#### [Product Name]

- Platform: [Amazon / Walmart / Target / Chewy / Other]
- Direct Product URL: [Live product detail page URL]
- Review: "_[Visible review snippet or retailer review summary]_"
- Specifics: [What makes it oddly specific]
- Review Date: [Date if visible]
- Freshness: [Why this source is current / active]
- Rating: [X.X/5 stars] ([Y] reviews)
- Helpfulness: [Helpful-vote count if visible]

[... additional products ...]

---

## Analysis of Patterns

### Common Themes in Oddly Specific Reviews

1. [Theme 1]
2. [Theme 2]

### Product Categories Most Prone to These Reviews

1. [Category 1]
2. [Category 2]

---

## Recommendations for Content Use

- **Social media series:** "Most Oddly Specific Retail Review of the Week"
- **Video compilation:** Dramatic readings with product demonstrations
- **Article:** "When Mundane Products Inspire Extreme Opinions"
- **Podcast segment:** Analyze why certain products inspire such vivid reactions

---

## Sources

- Search terms used: [list]
- Platforms: [list]
- Date range: [range]
- Direct product URLs used: [list]

Hard requirement: every final report entry must include a live clickable direct product detail page URL. Do not include search URLs, roundup articles, archives, or fallback links unless explicitly requested by the user.

---

_Report compiled using live retail product pages - [Date]_
```

## Step 6: Format with Prettier

If prettier is installed, format the markdown:

```bash
prettier --write /home/tully/Sync/marty/[filename].md
```

If prettier is not available, skip formatting.

## Example Output Structure

After completing the task, output:

```text
Done. File saved to: `/home/tully/Sync/marty/[timestamp]_source_material.md`
```

Include a brief summary of:
- number of products found
- most notable finding
- categories covered
