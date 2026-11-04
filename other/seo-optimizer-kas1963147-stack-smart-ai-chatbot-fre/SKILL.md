---
name: seo-optimizer
description: Complete SEO optimization for WordPress - meta tags, structured data, sitemaps, redirects, keyword tracking, and content analysis. Yoast/RankMath compatible.
tools_required: [seo_meta, seo_schema, seo_sitemap, seo_redirects, seo_social, seo_analyze, seo_robots, seo_keywords, seo_links, seo_webmaster]
always_on: false
group: seo
order: 1
suggests: [content-creator]
---

# SEO Optimizer

Complete SEO management for WordPress sites with meta optimization, structured data, and technical SEO.

## When to Use This Skill

- Optimizing page meta tags (title, description)
- Adding structured data (JSON-LD schema)
- Managing XML sitemaps
- Setting up 301/302 redirects
- Analyzing content for SEO scores
- Tracking keyword rankings
- Managing robots.txt
- Verifying with search engines

## Core Capabilities

### On-Page SEO
- Meta title optimization (50-60 characters)
- Meta description optimization (150-160 characters)
- Open Graph tags for social sharing
- Twitter Card configuration
- Canonical URLs

### Technical SEO
- XML sitemap generation and management
- Robots.txt configuration
- 301/302 redirect management
- Webmaster tools verification
- Core Web Vitals monitoring

### Content SEO
- Keyword density analysis
- Content readability scoring
- Internal link analysis
- Heading structure validation
- Image alt text checking

### Structured Data
- Article schema
- Product schema (WooCommerce)
- Organization schema
- Breadcrumb schema
- FAQ schema
- Review/Rating schema

## Workflow

### Optimizing a Page

1. **Analysis**
   - Run `seo_analyze` on the page
   - Check current SEO score
   - Identify improvement areas

2. **Meta Optimization**
   - Update title and description with `seo_meta`
   - Set focus keyword
   - Configure canonical URL

3. **Schema Markup**
   - Add appropriate schema with `seo_schema`
   - Validate structured data
   - Test rich snippets

4. **Social Optimization**
   - Set Open Graph image with `seo_social`
   - Configure Twitter Card type
   - Preview social appearance

### Technical SEO Audit

1. **Sitemap Check**
   - Review sitemap with `seo_sitemap`
   - Ensure all important pages included
   - Check for errors

2. **Redirect Audit**
   - Review redirects with `seo_redirects`
   - Fix redirect chains
   - Remove broken redirects

3. **Robots Configuration**
   - Check robots.txt with `seo_robots`
   - Ensure proper crawl directives
   - Block unwanted pages

## SEO Checklist

### Every Page
- [ ] Unique meta title (50-60 chars)
- [ ] Compelling meta description (150-160 chars)
- [ ] Focus keyword in title
- [ ] Focus keyword in first paragraph
- [ ] Proper heading hierarchy (H1 → H6)
- [ ] Alt text on all images
- [ ] Internal links to related content
- [ ] External links to authoritative sources

### Technical
- [ ] Page in XML sitemap
- [ ] Canonical URL set
- [ ] No broken links
- [ ] Mobile-responsive
- [ ] Fast loading (<3s)
- [ ] HTTPS enabled

### Schema
- [ ] Organization schema on homepage
- [ ] Article schema on blog posts
- [ ] Product schema on products
- [ ] Breadcrumb schema enabled

## Best Practices

1. **One focus keyword per page**
2. **Write for humans, optimize for search engines**
3. **Natural keyword placement (1-3% density)**
4. **Unique content on every page**
5. **Update old content regularly**
6. **Build quality internal links**
7. **Fix technical issues promptly**

## Key Metrics

- Organic traffic
- Keyword rankings
- Click-through rate (CTR)
- Bounce rate
- Page load time
- Core Web Vitals scores
