---
type: Skill
name: design-content-research
description: Produces WordPress draft posts from research findings — converts Paper Store research records or raw research data into publishable blog posts, buying guides, brand spotlights, and how-to articles. Use when the task asks to "turn research into a post", "create a blog post from findings", "publish my research", "research to content", or "write up the findings". Covers the full research-to-post pipeline with Paper Store integration.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Content Research → Post Pipeline

Use this skill when research findings need to become WordPress content — blog posts, buying guides, brand profiles, or landing pages.

## Available Tool

| Tool | Purpose |
|---|---|
| `create_post_from_research` | Convert a Paper Store research record or raw JSON data into a WordPress draft post |
| `create_post` | Direct WordPress post creation with images, charts, categories, tags, and meta |
| `save_post` | Create or update a post by ID |

For simple post creation (non-research content), use `create_post` directly:

```
create_post {
  title: "Post Title"
  content: "HTML content here"
  post_type: "post"
  status: "draft"
  categories: ["category-slug"]
  tags: ["tag1", "tag2"]
  content_images: [{ source: 123, position: "start" }]
}
```

Use `save_post` to update an existing post by passing `post_id`.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for research-to-post workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai content` | Search existing posts to avoid duplicate topics |
| `wp mcp-ai paper-store list` | List available research records in Paper Store collections |
| `wp mcp-ai paper-store read` | Read a specific Paper Store research record before conversion |
| `wp mcp-ai bulk` | Batch-create multiple posts from research records |

## When to use this skill

Trigger when ANY of the following is true:

- Research is complete and needs to become a WordPress post or page.
- The task asks to "turn this research into a post" or "create a blog post from findings".
- Converting a Paper Store research record into published content.
- Building a buying guide, brand spotlight, or educational article from research data.
- The task mentions "post from research", "research to content", or "publish the findings".

## `create_post_from_research` — Research → WordPress Post

Takes structured research and creates a WordPress draft. Can pull from Paper Store records or accept raw JSON data directly.

### Parameters

```
paper_store_record_id  — Paper Store record ID to convert (required if no `data`)
paper_store_collection — Collection containing the record (required with record_id)
data                   — Raw research data object (alternative to Paper Store)
                         Must include "title". Can include "report" (content),
                         "description" (excerpt), and "sources".
post_type              — WordPress post type (default: "post")
post_status            — "draft" or "pending" (default: "draft")
category_id            — Category term ID to assign
tags                   — Array of tag strings
author_id              — User ID for post author (default: current user)
update_paper_status    — Auto-update Paper Store record to "published" after creation
```

### Workflow A: From Paper Store

```
1. Research is stored in Paper Store (e.g., from deep_research or research_product)

2. create_post_from_research {
     paper_store_record_id: "conatural-brand-profile"
     paper_store_collection: "research-reports"
     post_type: "post"
     post_status: "draft"
     category_id: 2046  // CoNatural category
     tags: ["conatural", "skincare", "brand-spotlight", "sri-lanka"]
     update_paper_status: true
   }

3. Review the draft in WordPress admin
4. Edit, add images, optimize SEO
5. Publish when ready
```

### Workflow B: From Raw Data

```
1. Research is complete but not in Paper Store

2. create_post_from_research {
     data: {
       title: "The Ultimate Guide to Layering Fragrances for Sri Lanka's Climate"
       report: "In Sri Lanka's tropical humidity, fragrance layering is both
                an art and a science. Here's how to make your scent last..."
       description: "Master fragrance layering for long-lasting scent in
                     tropical weather. Expert tips for Sri Lankan perfume lovers."
       sources: ["https://source1.com", "https://source2.com"]
     }
     post_type: "post"
     post_status: "draft"
     category_id: 123  // Blog category
     tags: ["fragrance-tips", "layering", "tropical-climate", "sri-lanka"]
   }

3. Review and publish
```

### Post Types

| Post Type | Use For |
|---|---|
| `post` (default) | Blog articles, buying guides, brand spotlights |
| `page` | Landing pages, evergreen guides, about pages |
| `product` | WooCommerce product pages (if WooCommerce is active) |

### Status Selection

| Status | When |
|---|---|
| `draft` | Standard — review and edit before publishing |
| `pending` | Editorial workflow — needs editor approval |

## Content Types This Pipeline Supports

### 1. Brand Spotlights

```
Research → Post about a brand The Parfumerie carries

Example: "Inside Conatural: The Women-Led Skincare Brand Taking
         Sri Lanka by Storm"
```

### 2. Buying Guides

```
Research → Educational guide helping customers choose

Example: "EDP vs EDT vs Parfum: Which Fragrance Concentration
         Is Right for You?"
```

### 3. Trend Reports

```
Research → Article about industry trends

Example: "5 Fragrance Trends Dominating Sri Lanka in 2026"
```

### 4. How-To Guides

```
Research → Instructional content

Example: "How to Make Your Perfume Last All Day in Sri Lanka's Humidity"
```

### 5. Gift Guides

```
Research → Curated product recommendations

Example: "The Parfumerie's Ultimate Gift Guide: Fragrance, Jewelry & Skincare"
```

## Post Creation Checklist

Before creating the post, verify:

```
□ Research is complete and accurate
□ Title is SEO-optimized (brand + topic + key differentiator)
□ Content has a clear structure (H2/H3 headings, short paragraphs)
□ Sources are cited where relevant
□ Category and tags are assigned
□ Post status is appropriate (draft for review, pending for editorial)
□ update_paper_status is set if the research record should be marked as published
```

After creation:

```
□ Review the draft in WordPress admin
□ Add featured image (use generate_gemini_image_validated if needed)
□ Optimize meta description (see design-seo-content)
□ Add internal links to products and related posts
□ Preview before publishing
```

## Paper Store Integration (on request)

The pipeline naturally integrates with Paper Store:

```
Store → Research → Create Post → Mark Complete
  ↑                                    ↓
  └────────── Future reference ────────┘

1. paper_store_write: Save research
2. create_post_from_research: Convert to WordPress draft
3. update_paper_status: true — mark the research as "published"
4. paper_store_read: Retrieve later for updates or repurposing
```

When explicitly asked, use `connection_id` to target the correct site:

```
paper_store_write {
  connection_id: "conn_8srcad8zylhe"
  collection: "research-reports"
  ...
}
```

## Critical Rules

- **Research before posting** — never create a post from incomplete or unverified research.
- **Draft first, publish later** — always create as `draft` or `pending`. Review before publishing.
- **One post per research record** — don't try to cram multiple topics into one post.
- **Assign categories and tags** — posts without taxonomy are hard to find and organize.
- **Update Paper Store status** — if the research is done, mark it as published.
- **SEO follows creation** — after the draft exists, run through `design-seo-content` for optimization.

## Common Mistakes

```
WRONG:
  ● Publishing directly (skip review) — always draft first
  ● No category or tags assigned — post becomes orphaned
  ● Creating a post from thin research — verify findings first
  ● Forgetting to set update_paper_status — Paper Store record stays "draft" forever
  ● Cramming 5 research topics into one post — one topic, one post

RIGHT:
  ✅ Draft → review → optimize → publish workflow
  ✅ Category + 3–5 relevant tags per post
  ✅ Research verified and cited before posting
  ✅ update_paper_status: true when research is complete
  ✅ One clear topic per post
```

## What This Skill Does NOT Cover

- **Conducting the actual research (web search, deep research)** — use **`design-deep-research`** or **`design-web-research`**.
- **SEO optimization of the resulting post** — use **`design-seo-content`** after draft creation.
- **Publishing or scheduling the post** — use `save_post` (status: "publish") or `schedule_social_post`.
- **Creating featured images for the post** — use **`design-image-generation`**.
- **Managing Paper Store collections and records directly** — use `paper_store_write` / `paper_store_read` / `paper_store_search` tools.
- **Product-specific research for WooCommerce** — use **`design-product-research`**.
- **Writing social media posts promoting the content** — use **`design-social-content`**.

## Cross-references

- Run **`design-deep-research`** for the research that feeds this pipeline — use `deep_research`.
- Run **`design-web-research`** for quick fact checks and source URLs — use `web_search` and `run_crawl4ai_job`.
- Run **`design-product-research`** for product-specific research — use `research_product`.
- Run **`design-seo-content`** to optimize the draft post for search engines.
- Run **`design-image-generation`** to create a featured image — use `generate_gemini_image_validated`.
- Run **`design-campaign-orchestration`** to integrate the post into a monthly content calendar.
- Use **`paper_store_*`** with `connection_id` to persist research before converting to posts.
