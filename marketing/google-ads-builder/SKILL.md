---
name: google-ads-builder
description: Build complete Google Search ad campaigns with keywords, ad copy, and extensions
tags: [google-ads, ppc, search-ads, sem, paid-search]
---

# Google Ads Builder

Builds Google Search ad campaigns end-to-end: defines campaign and ad group structure, generates keyword lists by match type, writes Responsive Search Ad (RSA) copy within character limits, sets up ad extensions (sitelinks, callouts, structured snippets), and recommends bidding strategies. Outputs a complete campaign structure formatted for Google Ads Editor import or manual setup.

## Prerequisites

- WebSearch tool available for SERP analysis, keyword research, and competitor ad analysis
- Business services, target audience, and budget range
- Optional: `agency.config.json` for service details, ICP, and case studies
- Optional: existing Google Ads account data for optimization

## Capabilities Used

1. `keyword-miner` -- for keyword discovery and expansion
2. `content-seo-optimizer` -- for landing page alignment with ad messaging
3. `landing-page-auditor` -- for ad-to-landing-page message match validation

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` for campaign and ad group structure.
3. Extract `icp.segments[]` for audience targeting context and keyword intent.
4. Extract `case_studies[]` for proof points in ad copy.
5. Extract `agency.url` for landing page URLs.
6. Check `tools.websearch` availability.
7. Accept parameters:
   - `business_name` -- (required) business name for ad copy
   - `services` -- (optional) array of services to advertise. Default: derive from config
   - `landing_pages` -- (optional) map of service to landing page URL
   - `budget_monthly` -- (optional) monthly budget in local currency
   - `target_market` -- (optional) geographic targeting: country, region, or city list
   - `competitors` -- (optional) array of competitor names for conquest campaigns
   - `goal` -- (optional) `leads` | `sales` | `traffic` | `awareness`. Default: `leads`

## Phase 1: Campaign Structure Design

### Campaign Architecture
Design campaign hierarchy based on the business:

**Campaign Level** (budget and targeting)
- One campaign per major service category or business objective
- Separate brand campaigns from non-brand
- Separate competitor/conquest campaigns
- Geographic campaign splits if budget warrants it

**Ad Group Level** (keyword themes)
- Each ad group targets a tight cluster of related keywords
- 5-20 keywords per ad group (tightly themed)
- Each ad group has its own ad copy tailored to that keyword theme
- Each ad group points to the most relevant landing page

### Recommended Structure
```
Campaign: [Service 1] - Search
  Ad Group: [Service 1] - Core Terms
  Ad Group: [Service 1] - Long Tail
  Ad Group: [Service 1] - How To / Informational
  Ad Group: [Service 1] - Location Terms

Campaign: [Service 2] - Search
  Ad Group: [Service 2] - Core Terms
  ...

Campaign: Brand - Search
  Ad Group: Brand - Exact
  Ad Group: Brand - Modified

Campaign: Competitor - Search
  Ad Group: [Competitor 1] - Conquest
  Ad Group: [Competitor 2] - Conquest
```

## Phase 2: Keyword List Generation

### Keyword Research per Ad Group
For each ad group:

**Core Keywords**
- WebSearch seed keywords related to the ad group theme
- Extract related search suggestions
- Mine "People Also Ask" for question keywords
- Identify commercial intent keywords (buy, hire, agency, service, cost, pricing)

**Match Type Distribution**
For each keyword, generate three versions:
- **Exact Match**: `[shopify development agency]` -- highest intent, lowest volume
- **Phrase Match**: `"shopify development agency"` -- medium intent and volume
- **Broad Match**: `shopify development agency` -- widest reach, needs careful monitoring

### Negative Keywords
Generate negative keyword lists to prevent wasted spend:
- **Universal negatives**: free, cheap, DIY, tutorial, how to (unless targeting informational)
- **Industry negatives**: job, career, salary, course, certification (unless relevant)
- **Competitor negatives** (for non-conquest campaigns): competitor brand names
- **Irrelevant service negatives**: services you don't offer that share keywords

### Keyword Organization
Per ad group, target:
- 3-5 exact match keywords (high intent, highest bid)
- 5-10 phrase match keywords (medium intent)
- 3-5 broad match keywords (discovery, lowest bid)
- 10-20 negative keywords

## Phase 3: Ad Copy Writing

### Responsive Search Ads (RSAs)
For each ad group, write one RSA with:

**Headlines (up to 15, max 30 characters each)**
Write 15 headlines in these categories:
- 3 headlines with primary keyword inserted
- 2 headlines with a unique value proposition
- 2 headlines with a CTA (Get Started, Book a Demo, Get a Quote)
- 2 headlines with social proof (Trusted by X+ Brands, 5-Star Rated)
- 2 headlines with an offer or differentiator (Free Audit, 2-Week Setup)
- 2 headlines with urgency or scarcity (Limited Spots, This Month Only)
- 2 headlines with location or market relevance

Pin headline 1 (keyword headline) and headline 2 (value prop) for consistency.

**Descriptions (up to 4, max 90 characters each)**
Write 4 descriptions:
- Description 1: Core value proposition with keyword and CTA
- Description 2: Social proof and credibility (case study numbers, client count)
- Description 3: Service details and differentiators
- Description 4: Urgency or offer-focused

### Ad Copy Rules
- Every headline must make sense on its own (they appear in random combinations)
- No headline should repeat the same message as another
- Include target keyword in at least 3 headlines and 2 descriptions
- Include a CTA in at least 2 headlines and all descriptions
- Use title case for headlines
- Character counts are strict: 30 for headlines, 90 for descriptions

### Display URL Paths
- Set display URL paths to reinforce keyword theme
- Path 1: service category (e.g., "Shopify")
- Path 2: specific offering (e.g., "Development")

## Phase 4: Ad Extensions Setup

### Sitelink Extensions (4-8 per campaign)
For each sitelink:
- Link text (max 25 characters)
- Description line 1 (max 35 characters)
- Description line 2 (max 35 characters)
- Final URL

Common sitelinks:
- Portfolio / Case Studies
- Pricing / Packages
- About Us / Why Us
- Contact / Get a Quote
- Blog / Resources
- Specific service pages

### Callout Extensions (4-10 per campaign)
Short phrases highlighting differentiators (max 25 characters each):
- "Free Initial Consultation"
- "24/7 Support Available"
- "100+ Clients Served"
- "Certified Shopify Partner"
- "2-Week Delivery"
- "Money-Back Guarantee"

### Structured Snippet Extensions
Select categories and values:
- **Services**: list 3-8 specific services
- **Types**: list service/product types
- **Brands**: list brands worked with (if applicable)

### Call Extension
- Phone number for call tracking
- Schedule: business hours only

### Location Extension (if applicable)
- Link Google Business Profile

## Phase 5: Bidding Strategy Recommendation

### Based on Campaign Goal
- **Leads (form fills)**: Target CPA or Maximize Conversions
- **Sales (ecommerce)**: Target ROAS or Maximize Conversion Value
- **Traffic**: Maximize Clicks with a bid cap
- **Awareness**: Target Impression Share

### Budget Allocation Across Campaigns
- Allocate 60-70% to core service campaigns (highest intent)
- Allocate 15-20% to brand campaigns (protect brand, cheapest clicks)
- Allocate 10-15% to competitor campaigns (expensive but high intent)
- Reserve 5-10% for testing new ad groups and keywords

### Bid Modifiers
Recommend adjustments for:
- Device: mobile vs desktop (based on conversion data)
- Location: boost bids in target geography
- Time of day: boost during business hours
- Audience: boost for remarketing lists

## Phase 6: Conversion Tracking Setup

### Recommended Conversions
- Primary: form submission, phone call, demo booking
- Secondary: page view (pricing page), time on site (> 2 min), scroll depth
- Set up Google Tag for conversion tracking
- Link Google Analytics 4 for full funnel visibility

## Phase 7: Output

Return structured JSON:

```json
{
  "business_name": "Example Agency",
  "built_at": "2024-01-15T14:30:00Z",
  "goal": "leads",
  "target_market": "India",
  "monthly_budget": "50000 INR",
  "campaigns": [
    {
      "campaign_name": "Shopify Development - Search",
      "campaign_type": "Search",
      "budget_allocation": "60%",
      "bidding_strategy": "Maximize Conversions (Target CPA: 500 INR)",
      "geographic_targeting": "India",
      "ad_groups": [
        {
          "ad_group_name": "Shopify Dev - Core Terms",
          "landing_page": "https://example.com/services/shopify-development",
          "keywords": {
            "exact": ["[shopify development agency]", "[hire shopify developer]"],
            "phrase": ["\"shopify store development\"", "\"shopify agency india\""],
            "broad": ["shopify development services"]
          },
          "negative_keywords": ["free", "tutorial", "course", "job", "salary"],
          "rsa": {
            "headlines": [
              "Shopify Development Agency",
              "Expert Shopify Developers",
              "Book a Free Consultation",
              "Trusted by 100+ D2C Brands",
              "Launch Your Store in 2 Weeks"
            ],
            "descriptions": [
              "Expert Shopify development for D2C brands. Custom themes, CRO, and ongoing support. Get a free audit.",
              "Trusted by 100+ brands. 2-week delivery. Shopify Partner certified. Book your free strategy call today."
            ],
            "pinned": { "headline_1": "Shopify Development Agency", "headline_2": "Expert Shopify Developers" },
            "display_paths": ["Shopify", "Development"]
          }
        }
      ]
    }
  ],
  "extensions": {
    "sitelinks": [
      { "text": "View Case Studies", "description_1": "See Real Client Results", "description_2": "100+ Stores Launched", "url": "/case-studies" }
    ],
    "callouts": ["Free Consultation", "Certified Partner", "2-Week Delivery", "24/7 Support"],
    "structured_snippets": { "category": "Services", "values": ["Store Development", "CRO Audits", "Theme Customization", "Migration"] }
  },
  "negative_keyword_lists": {
    "universal": ["free", "cheap", "DIY", "tutorial", "course", "job", "salary", "intern"],
    "campaign_specific": {}
  },
  "budget_plan": {
    "core_service_campaigns": "60%",
    "brand_campaign": "20%",
    "competitor_campaigns": "15%",
    "testing_budget": "5%"
  },
  "projected_metrics": {
    "estimated_monthly_clicks": "800-1200",
    "estimated_cpc_range": "20-60 INR",
    "estimated_monthly_leads": "40-80",
    "estimated_cpa": "500-1000 INR"
  }
}
```

## Example Usage

Trigger phrases:
- "Build Google Ads campaigns for [business]"
- "Create search ads for [service]"
- "Google Ads keyword list for [niche]"
- "Write RSA ad copy for [service]"
- "Set up Google Ads campaign structure for [business]"

```
User: Build Google Ads campaigns for plasho.com targeting Shopify development leads in India
Assistant: [reads config, structures campaigns by service, generates keyword lists with match types, writes RSAs within char limits, sets up extensions, returns complete campaign ready for import]
```

```
User: Write Google search ad copy for a CRO audit service
Assistant: [generates 15 headlines and 4 descriptions within character limits, sets up extensions, returns formatted RSA]
```

```
User: Google Ads keyword list for a Shopify agency -- include negative keywords
Assistant: [mines keywords by intent, organizes by match type, generates comprehensive negative keyword list, returns organized keyword plan]
```
