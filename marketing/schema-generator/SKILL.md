---
name: schema-generator
description: Generate validated JSON-LD structured data markup for any page type
tags: [seo, schema, structured-data, json-ld, rich-snippets]
---

# Schema Generator

Generates ready-to-paste JSON-LD structured data markup for any page type. Supports Product, Article, FAQ, LocalBusiness, Organization, HowTo, Review, Service, BreadcrumbList, WebSite, Event, and more. Gathers required and recommended fields per schema type, generates valid JSON-LD, validates against schema.org specifications, and outputs script tags ready for insertion into page HTML.

## Prerequisites

- Target page type or URL to generate schema for
- Content details (product info, FAQ pairs, business details, etc.)
- Optional: `agency.config.json` for organization defaults
- Optional: browser automation tool for extracting content from a live URL

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `agency.name`, `agency.url`, `agency.logo` for Organization schema defaults.
3. Extract `agency.social_profiles` for sameAs links.
4. Check `tools.browser` availability for live page content extraction.
5. Accept parameters:
   - `page_type` -- (required) one of: `product`, `article`, `faq`, `local_business`, `organization`, `how_to`, `review`, `service`, `breadcrumb`, `website`, `event`, `person`, `recipe`, `video`, `course`, `job_posting`, `software_application`
   - `url` -- (optional) live page URL to extract content from automatically
   - `data` -- (optional) object with field values to populate the schema
   - `multiple` -- (optional) boolean, generate multiple schema types for the same page. Default: false
   - `include_breadcrumb` -- (optional) boolean, auto-add BreadcrumbList alongside primary schema. Default: true

## Phase 1: Schema Type Resolution

### Determine Required Schema Types
Based on `page_type`, identify the primary schema and any supplementary schemas:

| Page Type | Primary Schema | Supplementary Schemas |
|-----------|---------------|----------------------|
| product | Product | BreadcrumbList, Review, Offer, AggregateRating |
| article | Article / BlogPosting / NewsArticle | BreadcrumbList, Organization (publisher) |
| faq | FAQPage | BreadcrumbList |
| local_business | LocalBusiness | BreadcrumbList, PostalAddress, GeoCoordinates |
| organization | Organization | WebSite, SearchAction |
| how_to | HowTo | BreadcrumbList |
| review | Review | BreadcrumbList, itemReviewed |
| service | Service | Organization (provider), BreadcrumbList, Offer |
| breadcrumb | BreadcrumbList | (standalone) |
| website | WebSite | Organization, SearchAction |
| event | Event | BreadcrumbList, Place, Offer |
| person | Person | (standalone) |
| video | VideoObject | BreadcrumbList |
| course | Course | BreadcrumbList, Organization (provider) |
| job_posting | JobPosting | Organization (hiringOrganization) |
| software_application | SoftwareApplication | BreadcrumbList, Review, Offer |

## Phase 2: Field Gathering

### If URL Provided
- Visit the page via browser automation
- Auto-extract relevant fields:
  - Page title, description, headings
  - Product details: name, price, currency, availability, images, SKU, brand
  - Article details: headline, author, datePublished, dateModified, image
  - FAQ: extract Q&A pairs from heading + paragraph patterns
  - Business: name, address, phone, hours from footer/contact page
  - Breadcrumb: derive from URL path structure
- Present extracted data for user confirmation before generating

### If Data Object Provided
- Validate that all required fields for the schema type are present
- Prompt for any missing required fields
- Apply defaults from config where appropriate

### Required vs Recommended Fields
For each schema type, clearly separate:
- **Required fields**: schema will fail validation without these
- **Recommended fields**: improve rich snippet eligibility
- **Optional fields**: enhance completeness but not required

## Phase 3: Schema Generation

### Product Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{product_name}}",
  "image": ["{{image_url_1}}", "{{image_url_2}}"],
  "description": "{{description}}",
  "sku": "{{sku}}",
  "brand": {
    "@type": "Brand",
    "name": "{{brand_name}}"
  },
  "offers": {
    "@type": "Offer",
    "url": "{{page_url}}",
    "priceCurrency": "{{currency}}",
    "price": "{{price}}",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "{{seller_name}}"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{rating}}",
    "reviewCount": "{{review_count}}"
  }
}
```

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{headline}}",
  "image": ["{{image_url}}"],
  "datePublished": "{{date_published}}",
  "dateModified": "{{date_modified}}",
  "author": {
    "@type": "Person",
    "name": "{{author_name}}",
    "url": "{{author_url}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{publisher_name}}",
    "logo": {
      "@type": "ImageObject",
      "url": "{{publisher_logo_url}}"
    }
  },
  "description": "{{description}}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{page_url}}"
  }
}
```

### FAQ Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{question_1}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{answer_1}}"
      }
    }
  ]
}
```

### LocalBusiness Schema
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{{business_name}}",
  "image": "{{image_url}}",
  "url": "{{website_url}}",
  "telephone": "{{phone}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{street}}",
    "addressLocality": "{{city}}",
    "addressRegion": "{{state}}",
    "postalCode": "{{zip}}",
    "addressCountry": "{{country}}"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "{{lat}}",
    "longitude": "{{lng}}"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ]
}
```

### Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{org_name}}",
  "url": "{{org_url}}",
  "logo": "{{logo_url}}",
  "sameAs": [
    "{{linkedin_url}}",
    "{{twitter_url}}",
    "{{facebook_url}}"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "{{phone}}",
    "contactType": "customer service"
  }
}
```

### HowTo Schema
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{{title}}",
  "description": "{{description}}",
  "totalTime": "{{duration_iso8601}}",
  "step": [
    {
      "@type": "HowToStep",
      "name": "{{step_name}}",
      "text": "{{step_text}}",
      "image": "{{step_image_url}}"
    }
  ]
}
```

### BreadcrumbList Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{{base_url}}"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{{category_name}}",
      "item": "{{category_url}}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{page_name}}",
      "item": "{{page_url}}"
    }
  ]
}
```

### Service Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{{service_name}}",
  "description": "{{description}}",
  "provider": {
    "@type": "Organization",
    "name": "{{provider_name}}",
    "url": "{{provider_url}}"
  },
  "serviceType": "{{service_type}}",
  "areaServed": {
    "@type": "Country",
    "name": "{{country}}"
  },
  "offers": {
    "@type": "Offer",
    "price": "{{starting_price}}",
    "priceCurrency": "{{currency}}"
  }
}
```

## Phase 4: Validation

### Schema.org Compliance Check
- Verify all required properties are present for the schema type
- Verify data types match expectations (string, number, URL, date in ISO 8601)
- Verify URLs are absolute, not relative
- Verify image URLs are accessible
- Check for deprecated properties and suggest current alternatives
- Ensure `@context` is `https://schema.org` (not http)

### Common Error Prevention
- No trailing commas in JSON
- No single quotes (must be double quotes)
- Dates in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Prices as strings with decimals: `"29.99"` not `29.99`
- Availability values must be full schema.org URLs: `https://schema.org/InStock`

### Rich Results Eligibility
- Check which Google rich result types the schema qualifies for
- Flag any missing fields that would prevent rich result display
- Note: FAQ rich results, Product rich results, Review stars, Recipe cards, How-to steps

## Phase 5: Output

Return structured JSON:

```json
{
  "page_url": "https://example.com/products/widget",
  "generated_at": "2024-01-15T14:30:00Z",
  "page_type": "product",
  "schemas_generated": ["Product", "BreadcrumbList"],
  "validation_status": "PASS",
  "rich_result_eligible": ["Product snippet", "Review stars", "Price display"],
  "script_tags": [
    {
      "schema_type": "Product",
      "json_ld": "<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"Product\",\n  ...\n}\n</script>"
    },
    {
      "schema_type": "BreadcrumbList",
      "json_ld": "<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"BreadcrumbList\",\n  ...\n}\n</script>"
    }
  ],
  "validation_notes": [
    "All required Product fields present",
    "AggregateRating included -- eligible for review stars in SERPs",
    "BreadcrumbList derived from URL path structure"
  ],
  "missing_recommended_fields": [
    { "field": "gtin", "impact": "Adds product identification for Google Shopping" },
    { "field": "review", "impact": "Individual reviews strengthen review star display" }
  ],
  "implementation_instructions": "Add both script tags to the <head> section of the page. Test with Google Rich Results Test: https://search.google.com/test/rich-results"
}
```

## Example Usage

Trigger phrases:
- "Generate schema for [page type]"
- "Create JSON-LD for [url]"
- "Add structured data to [page type]"
- "Schema markup for my [product/article/FAQ]"
- "Generate FAQ schema for these questions"

```
User: Generate product schema for plasho.com/services/shopify-setup
Assistant: [visits page, extracts service details, generates Service + Organization + BreadcrumbList JSON-LD, validates, returns ready-to-paste script tags]
```

```
User: Create FAQ schema for these Q&As: "How long does setup take?" "2-3 weeks", "What's included?" "Full store setup with theme customization"
Assistant: [generates FAQPage JSON-LD with both Q&A pairs, validates, returns script tag]
```

```
User: What schema should I add to my homepage?
Assistant: [recommends Organization + WebSite + SearchAction, gathers details, generates all three, returns validated script tags]
```
