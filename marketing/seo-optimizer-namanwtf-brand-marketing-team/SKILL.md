---
name: seo-optimizer
description: Automated SEO optimization with keyword research and content optimization
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting
category: seo
---

# 🔍 SEO Optimizer Agent

**Purpose:** Dominate search rankings with automated keyword research, on-page optimization, and technical SEO fixes.

---

## When to Use

```bash
# Research keywords for new content
@seo-optimizer research "best gaming phones 2025"

# Optimize existing page
@seo-optimizer optimize /blog/post-url

# Technical SEO audit
@seo-optimizer audit website

# Track rankings
@seo-optimizer track "product x"

# Generate meta tags
@seo-optimizer meta product-page
```

---

## Capabilities

### 1. Keyword Research
- Find high-volume, low-competition keywords
- Analyze search intent (informational, transactional, navigational)
- Discover long-tail opportunities
- Competitor keyword gap analysis

### 2. On-Page Optimization
- Title tag optimization (50-60 chars)
- Meta description generation (150-160 chars)
- Header structure (H1, H2, H3 optimization)
- Internal linking suggestions
- Image alt text generation

### 3. Technical SEO
- Site speed analysis
- Mobile-friendliness check
- Schema markup generation
- XML sitemap creation
- Robots.txt optimization
- Broken link detection

### 4. Content Optimization
- Keyword density analysis
- Readability scoring
- LSI (Latent Semantic Indexing) keywords
- Content gap analysis vs competitors
- Featured snippet optimization

---

## Usage Examples

### Keyword Research
```
User: @seo-optimizer research "budget gaming phones"

Agent: 📊 KEYWORD RESEARCH RESULTS

Primary Keyword: "budget gaming phones under 20000"
• Volume: 14,000/month
• Difficulty: Medium (35/100)
• CPC: $0.45
• Intent: Transactional

Related Keywords:
1. "best gaming phone under 20000" - 8,100/mo
2. "gaming smartphone budget" - 5,400/mo
3. "cheap gaming phones 2025" - 3,600/mo

Content Recommendation:
Create comparison article targeting primary keyword
Include secondary keywords in H2s
Add video review for featured snippet
```

### Page Optimization
```
User: @seo-optimizer optimize /products/product-x

Agent: 🔧 ON-PAGE OPTIMIZATION

Current Issues:
❌ Title too long (72 chars)
❌ Missing H1 tag
❌ No meta description
❌ Images missing alt text

Optimized Version:
✅ Title: "Product X Gaming Device | Long Battery | Under $200" (58 chars)
✅ H1: "Product X: The Ultimate Gaming Device for Budget Buyers"
✅ Meta: "Experience 2-day battery life with Product X. Premium display, long battery, under $200. Free shipping. Shop now!" (155 chars)
✅ Alt text added to 12 images

Expected Impact:
• Click-through rate: +25%
• Ranking improvement: 5-10 positions
• Organic traffic: +40%
```

### Technical Audit
```
User: @seo-optimizer audit

Agent: 🔍 TECHNICAL SEO AUDIT

Critical Issues (Fix Immediately):
🔴 3 pages with 404 errors
🔴 Missing schema markup on product pages
🔴 Mobile speed: 4.2s (should be <3s)

Warnings (Fix This Week):
⚠️ 12 images without alt text
⚠️ Duplicate meta descriptions
⚠️ Missing canonical tags

Opportunities:
💡 Add FAQ schema for rich snippets
💡 Create XML sitemap
💡 Implement breadcrumbs

Priority Fix List Generated ✓
```

---

## Configuration

Add to `brand-context.md`:

```yaml
seo-optimizer:
  target-keywords: []
  competitors: []
  priority-pages: []
  target-locations: ["US", "UK", "India"]
  
  optimization:
    title-length: [50, 60]
    meta-length: [150, 160]
    readability-level: "8th-grade"
    keyword-density: [1, 3]  # percentage
```

---

## Related Skills

- **copywriting**: Creates SEO-optimized content
- **analytics-dashboard**: Tracks ranking improvements
- **content-calendar**: Schedules SEO content

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
