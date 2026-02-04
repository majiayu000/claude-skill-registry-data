---
name: schema-patterns
description: Schema.org structured data patterns for lead gen sites. LocalBusiness, FAQ, HowTo, Service, Review, BreadcrumbList. Rich snippets for better SERP visibility.
---

# Schema Patterns Skill

## Purpose

Provides comprehensive Schema.org markup patterns for lead generation sites to maximize rich snippet visibility in search results. Implement structured data to enable knowledge panels, FAQ accordions, star ratings, and other rich SERP features that increase click-through rates.

## Core Rules

1. **One primary schema per page** - LocalBusiness OR Organization at root
2. **Nest related schemas** - Reviews inside LocalBusiness, not separate
3. **Validate always** - Test with Google Rich Results Test before deployment
4. **Match visible content** - Schema must reflect what users see on page
5. **Keep updated** - Hours, prices, reviews must be current
6. **Use absolute URLs** - All image and link URLs must be absolute, not relative
7. **Follow Google requirements** - Check required fields for each schema type
8. **No fake content** - Only use real, verifiable reviews and ratings
9. **Test in production** - Validate with Search Console after deployment
10. **Prioritize P0 schemas** - LocalBusiness and FAQPage first for lead gen

## Schema Priority for Lead Gen

| Priority | Schema Type | Rich Result | Page Type |
|----------|-------------|-------------|-----------|
| P0 | LocalBusiness | Knowledge panel, maps | All pages |
| P0 | FAQPage | FAQ accordion in SERP | FAQ sections |
| P1 | Service | Service listings | Service pages |
| P1 | BreadcrumbList | Breadcrumb trail | Inner pages |
| P1 | AggregateRating | Star ratings | Business pages |
| P2 | HowTo | Step-by-step cards | Guide content |
| P2 | Article | Article cards | Blog posts |
| P3 | VideoObject | Video thumbnails | Video content |
| P3 | Product | Product cards | Product pages |

## References

### Schema Implementation Files

- [LocalBusiness & Service Schemas](./references/local-business.md) - Business and service markup
- [FAQ & HowTo Schemas](./references/faq-howto.md) - FAQ pages and step-by-step guides
- [Article & VideoObject Schemas](./references/article-video.md) - Blog posts and video content
- [Supporting Schemas](./references/supporting-schemas.md) - BreadcrumbList, Review, WebSite, combined examples
- [Validation & Testing](./references/validation-testing.md) - Validation code, testing tools, common mistakes

### External Resources

- [Google Rich Results Test](https://search.google.com/test/rich-results) - Primary validation tool
- [Schema.org Validator](https://validator.schema.org/) - Official schema validator
- [Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) - Schema guidelines
- [Schema.org Documentation](https://schema.org/) - Complete schema reference

## Quick Start

1. Add LocalBusiness schema to your base layout (all pages)
2. Add FAQPage schema to pages with FAQ sections
3. Add Service schema to service-specific pages
4. Add BreadcrumbList schema to all inner pages
5. Validate all schemas with Google Rich Results Test
6. Monitor Search Console for schema errors
7. Update business info (hours, prices) regularly

## Usage Example

```astro
---
// src/layouts/BaseLayout.astro
import LocalBusinessSchema from '@/components/schema/LocalBusinessSchema.astro';
import BreadcrumbSchema from '@/components/schema/BreadcrumbSchema.astro';

const breadcrumbs = getBreadcrumbs(Astro.url.pathname);
---

<html>
  <head>
    <LocalBusinessSchema {...siteConfig.business} />
    {breadcrumbs.length > 1 && <BreadcrumbSchema items={breadcrumbs} />}
  </head>
  <body>
    <slot />
  </body>
</html>
```

See [references/supporting-schemas.md](./references/supporting-schemas.md) for complete multi-schema examples.

## Forbidden

- Schema for content not visible on the page
- Fake reviews or ratings
- Outdated business information (hours, prices, phone)
- Multiple conflicting primary schemas
- Spammy keyword stuffing in schema values
- Hidden schema-only content not shown to users
- Relative URLs in schema markup

## Definition of Done

- [ ] LocalBusiness schema implemented on all pages
- [ ] FAQPage schema added to FAQ sections
- [ ] Service schema on all service pages
- [ ] BreadcrumbList on all inner pages
- [ ] Article schema on blog posts
- [ ] All schemas validated with Google Rich Results Test (zero errors)
- [ ] No schema errors in Google Search Console
- [ ] Schema content matches visible page content
- [ ] Business info (hours, prices, contact) is current and accurate
- [ ] All image and link URLs are absolute
