---
name: programmatic-seo
description: Plan and blueprint programmatic SEO page strategies at scale
tags: [seo, programmatic-seo, content-strategy, templates, scale]
---

# Programmatic SEO

Plans programmatic SEO strategies by identifying repeatable page patterns (service + location, service + industry, tool + use case), defining template structures, identifying data sources for dynamic content, planning internal linking strategies, and estimating page count and traffic potential. Outputs a complete programmatic SEO blueprint ready for implementation.

## Prerequisites

- WebSearch tool available for SERP analysis and pattern validation
- Browser automation tool for analyzing competitor programmatic pages
- Business services, target locations, or target verticals to combine
- Optional: `agency.config.json` for service and ICP context

## Capabilities Used

1. `keyword-miner` -- for validating search volume of programmatic keyword patterns
2. `content-seo-optimizer` -- for optimizing page templates
3. `schema-generator` -- for generating template-level structured data

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` for service-based page patterns.
3. Extract `icp.segments[].industries` for industry-based page patterns.
4. Extract `icp.segments[].geos` for location-based page patterns.
5. Accept parameters:
   - `domain` -- (required) target website domain
   - `pattern_type` -- (optional) `service_location` | `service_industry` | `tool_usecase` | `comparison` | `integration` | `template_gallery` | `auto`. Default: `auto` (analyze and recommend)
   - `services` -- (optional) array of services to create pages for
   - `locations` -- (optional) array of locations for location pages
   - `industries` -- (optional) array of industries for vertical pages
   - `max_pages` -- (optional) maximum page count to plan. Default: 500

## Phase 1: Pattern Identification

### Analyze Existing Site Structure
- Visit the domain via browser automation
- Map current page types and URL patterns
- Identify existing programmatic pages (if any)
- Note the site's CMS and templating capabilities
- Count current indexed pages: WebSearch `site:{{domain}}`

### Identify Repeatable Patterns
Based on the business type, evaluate these programmatic patterns:

**Service + Location** (most common for agencies and service businesses)
- Pattern: `/{{service}}/{{city}}` or `/{{service}}-in-{{city}}`
- Example: `/shopify-development/mumbai`, `/shopify-development/delhi`
- Works when: business serves multiple geographic markets

**Service + Industry**
- Pattern: `/{{service}}/{{industry}}` or `/{{service}}-for-{{industry}}`
- Example: `/shopify-development/fashion-brands`, `/cro-audit/electronics`
- Works when: service delivery varies by vertical

**Tool/Feature + Use Case**
- Pattern: `/tools/{{tool}}/{{use-case}}` or `/features/{{feature}}-for-{{goal}}`
- Example: `/tools/ab-testing/product-pages`, `/features/checkout-optimization-for-aov`
- Works when: product has multiple features or use cases

**Comparison Pages**
- Pattern: `/compare/{{your-product}}-vs-{{competitor}}`
- Example: `/compare/plasho-vs-competitor-agency`
- Works when: prospects are comparing solutions

**Integration Pages**
- Pattern: `/integrations/{{platform}}` or `/works-with/{{tool}}`
- Example: `/integrations/klaviyo`, `/works-with/google-analytics`
- Works when: product/service integrates with other tools

**Template/Example Gallery**
- Pattern: `/templates/{{category}}/{{subcategory}}`
- Example: `/templates/fashion/minimalist`, `/examples/food-beverage/premium`
- Works when: showcasing portfolio or template variety

### Competitor Programmatic Page Analysis
- WebSearch: `site:{{competitor}} inurl:{{pattern_slug}}` -- find competitor programmatic pages
- Analyze competitor page templates, content patterns, internal linking
- Note what ranks well and what doesn't
- Identify patterns competitors use that the target does not

## Phase 2: Keyword Validation

### Generate Keyword Matrix
For the chosen pattern, generate the full keyword matrix:
- List all dimension A values (services, tools, features)
- List all dimension B values (locations, industries, use cases)
- Create the cross-product: A x B = total page list

### Validate Search Demand
For a sample of 20-30 keyword combinations:
- WebSearch each combination to check for:
  - Search results count (more results = more demand)
  - Autocomplete suggestions (confirms search volume)
  - "People Also Ask" presence (confirms informational demand)
  - Competitor pages ranking (confirms commercial viability)
- Categorize demand levels: High, Medium, Low, No demand

### Filter and Prioritize
- Remove combinations with no search demand
- Rank remaining by estimated volume and commercial intent
- Identify "head" terms (high volume, competitive) vs "long tail" (low volume, easy)
- Calculate total addressable search volume for the page set

## Phase 3: Template Structure Design

### Page Template Components
Define the standard template structure for the programmatic pages:

**Above the Fold**
- Dynamic H1: `{{Service}} in {{Location}}` or `{{Service}} for {{Industry}}`
- Dynamic meta title: `{{Service}} {{Modifier}} in {{Location}} | {{Brand}}`
- Dynamic meta description template
- Hero section with dynamic city/industry imagery or relevant visual
- Primary CTA (contact, demo, quote)

**Body Content Sections**
- Introduction paragraph (template with dynamic variables)
- Service/product details specific to the dimension (location-specific info, industry-specific pain points)
- Benefits section (can be partially templated, partially dynamic)
- Social proof: case studies, testimonials, reviews filtered by dimension
- FAQ section: dimension-specific FAQ pairs
- Related services/pages: internal links to sibling pages

**Below the Fold**
- Trust signals (logos, certifications, awards)
- Secondary CTA
- Related content links

### Content Differentiation Strategy
The biggest risk in programmatic SEO is thin/duplicate content. Plan for:
- **Unique intro paragraph** per page (at least 2-3 sentences unique to each dimension)
- **Dimension-specific data** (location stats, industry benchmarks, relevant case studies)
- **Dynamic FAQ pairs** (different questions per dimension)
- **Unique internal links** (each page links to different related pages)
- Minimum unique content per page: 300+ words beyond shared template content

## Phase 4: Data Source Planning

### Identify Data Sources for Dynamic Content
For each dynamic element, specify where the data comes from:

| Dynamic Element | Data Source | Update Frequency |
|----------------|-------------|------------------|
| Location stats | Census data, Wikipedia, public APIs | Yearly |
| Industry benchmarks | Industry reports, public studies | Quarterly |
| Case studies | Internal CMS / portfolio database | As created |
| Testimonials | Review platforms, CRM | Monthly |
| FAQ pairs | Customer support data, PAA mining | Quarterly |
| Local imagery | Stock photo APIs, local photography | Once |
| Pricing variations | Internal pricing database | As changed |

### Data Collection Plan
- List all data points needed per dimension
- Identify free vs paid data sources
- Estimate data collection effort per dimension
- Plan for data freshness: how often does each data point need updating?

## Phase 5: Internal Linking Architecture

### Hub and Spoke Model
- **Hub page**: main service/category page that links to all programmatic child pages
- **Spoke pages**: individual programmatic pages that link back to hub + to 3-5 sibling pages
- **Cross-links**: programmatic pages in one dimension link to related pages in another dimension

### Link Structure
```
/services/shopify-development (hub)
  -> /shopify-development/mumbai (spoke)
  -> /shopify-development/delhi (spoke)
  -> /shopify-development/bangalore (spoke)

Each spoke links to:
  - Hub page (parent)
  - 3-5 sibling spokes (nearest cities or most relevant)
  - Related service pages (cross-dimension)
  - Blog posts about the dimension topic
```

### Sitemap Strategy
- Generate XML sitemap for all programmatic pages
- Group by dimension in sitemap index
- Set appropriate change frequency and priority
- Plan for sitemap updates as new pages are added

## Phase 6: Implementation Roadmap

### Phase-Based Rollout
Recommend staged deployment:

1. **Pilot (Week 1-2)**: Build 10-20 pages for highest-demand combinations. Monitor indexing, rankings, and traffic.
2. **Validation (Week 3-4)**: Analyze pilot performance. Refine template based on what ranks. Fix any indexing issues.
3. **Scale (Week 5-8)**: Expand to next 50-100 pages. Add unique content and data enrichment.
4. **Full deployment (Month 3+)**: Launch remaining pages. Ongoing content quality improvements.

### Technical Requirements
- CMS template capability or static site generation
- Dynamic content rendering (server-side preferred for SEO)
- URL management and canonical tag strategy
- Internal linking automation
- Sitemap generation and submission

## Phase 7: Output

Return structured JSON:

```json
{
  "domain": "example.com",
  "planned_at": "2024-01-15T14:30:00Z",
  "pattern_type": "service_location",
  "total_pages_planned": 150,
  "dimensions": {
    "dimension_a": {
      "name": "Services",
      "values": ["shopify-development", "cro-audit", "store-migration"],
      "count": 3
    },
    "dimension_b": {
      "name": "Locations",
      "values": ["mumbai", "delhi", "bangalore", "hyderabad", "pune"],
      "count": 50
    }
  },
  "keyword_validation": {
    "total_combinations": 150,
    "validated_sample_size": 25,
    "demand_distribution": {
      "high": 8,
      "medium": 10,
      "low": 5,
      "no_demand": 2
    },
    "estimated_total_monthly_volume": "5K-15K",
    "top_keywords": [
      { "keyword": "shopify development mumbai", "estimated_volume": "Medium", "difficulty": "Easy" }
    ]
  },
  "template_structure": {
    "url_pattern": "/{{service}}/{{location}}",
    "title_template": "{{Service}} in {{Location}} | Expert Shopify Agency | {{Brand}}",
    "meta_description_template": "Looking for {{service}} in {{location}}? We help {{location}} brands...",
    "sections": [
      "Dynamic H1 + hero",
      "Location-specific intro (unique 150+ words)",
      "Service details",
      "Local case studies / testimonials",
      "Location stats and market data",
      "FAQ (5 location-specific questions)",
      "CTA + contact info",
      "Related service pages"
    ],
    "min_unique_content_per_page": "300 words"
  },
  "data_sources": [
    { "element": "Location population and market data", "source": "Census / Wikipedia", "collection_effort": "Low (automated)" },
    { "element": "Industry-specific pain points", "source": "Customer interviews + ICP research", "collection_effort": "Medium (manual)" }
  ],
  "internal_linking_plan": {
    "hub_pages": ["/services/shopify-development"],
    "sibling_links_per_page": 5,
    "cross_dimension_links": 2,
    "blog_content_links": 1
  },
  "rollout_plan": {
    "pilot": { "pages": 15, "timeline": "Week 1-2", "focus": "Top 5 cities x 3 services" },
    "validation": { "timeline": "Week 3-4", "metrics": ["Indexing rate", "Ranking positions", "Organic clicks"] },
    "scale": { "pages": 50, "timeline": "Week 5-8" },
    "full_deployment": { "pages": 150, "timeline": "Month 3+" }
  },
  "traffic_projection": {
    "month_3": "500-1000 organic visits/month",
    "month_6": "2000-5000 organic visits/month",
    "month_12": "5000-15000 organic visits/month"
  },
  "risks_and_mitigations": [
    { "risk": "Thin content penalty", "mitigation": "Minimum 300 unique words per page, noindex low-quality pages until content is added" },
    { "risk": "Crawl budget waste", "mitigation": "Prioritize high-demand pages in sitemap, use internal linking to signal importance" },
    { "risk": "Cannibalization with existing pages", "mitigation": "Clear canonical strategy, distinct keyword targeting per page" }
  ]
}
```

## Example Usage

Trigger phrases:
- "Plan programmatic SEO for [domain]"
- "Create location pages strategy for [business]"
- "Programmatic SEO blueprint for [service] + [dimension]"
- "How many pages should I create for [niche]?"
- "Scale content with programmatic SEO"

```
User: Plan programmatic SEO for plasho.com -- service + city pages for India
Assistant: [identifies services from config, generates city list, validates keyword demand, designs template, plans rollout, returns complete blueprint]
```

```
User: Programmatic SEO strategy: shopify development + industry verticals
Assistant: [maps services to industries, validates search demand per combo, designs template with industry-specific content, returns implementation plan]
```

```
User: Should I create comparison pages for plasho.com?
Assistant: [researches "plasho vs" queries, analyzes competitor comparison pages, evaluates demand, recommends if viable, returns blueprint if yes]
```
