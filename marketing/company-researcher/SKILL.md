---
name: company-researcher
description: Deep research on a prospect company using WebSearch for outreach personalization
tags: [research, company-intel, personalization, prospecting]
---

# Company Researcher

Performs deep research on a prospect company using WebSearch. Returns structured data across multiple dimensions, including business overview, tech stack, social presence, team signals, news, pain points, and company LinkedIn URL for downstream enrichment. The output feeds directly into `message-generator` for Tier 3 personalization.

## Prerequisites

- WebSearch tool available
- Target company name and/or website URL
- Optional: `agency.config.json` for ICP context (what to look for based on agency services)

## Phase 0: Intake

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[].name` and `services[].keywords` to know what pain points to look for.
3. Accept parameters:
   - `company_name` -- (required) the company to research
   - `website` -- (optional but recommended) the company's website URL
   - `industry` -- (optional) to focus research
   - `depth` -- `quick` (3-5 searches) | `standard` (8-12 searches) | `deep` (15-20 searches). Default: `standard`

## Phase 1: Business Overview

Run WebSearch queries:
- `"{{company_name}}" about`
- `"{{company_name}}" "founded" OR "launched" OR "started"`
- `site:{{website}}` (homepage, about page)

Extract:
- What they sell (products/services)
- Target market / customer base
- Brand positioning and story
- Founding year, founding team
- Headquarters / location
- Revenue indicators (if public)
- Business model (D2C, B2B, marketplace, subscription)

## Phase 2: Tech Stack Analysis

If the company has a website, analyze their ecommerce/tech setup:

WebSearch queries:
- `site:{{website}}` -- visit the actual site
- `"{{website}}" "powered by" OR "built with" OR "shopify" OR "woocommerce"`
- `builtwith.com/{{domain}}` or `wappalyzer` results

Extract:
- **Platform**: Shopify, WooCommerce, Magento, custom, etc.
- **Theme**: Identify the Shopify theme (check page source for theme name)
- **Apps visible**: Review apps, upsell apps, chat widgets, email popups, loyalty programs
- **Payment providers**: Stripe, PayPal, Razorpay, etc.
- **Analytics**: Google Analytics, Hotjar, Mixpanel, etc.
- **Email marketing**: Klaviyo, Mailchimp, Omnisend, etc.

If the site is on Shopify, note the theme version and any customization indicators.

## Phase 3: Social Presence

WebSearch queries:
- `"{{company_name}}" site:instagram.com`
- `"{{company_name}}" site:linkedin.com/company`
- `"{{company_name}}" site:twitter.com OR site:x.com`
- `"{{company_name}}" site:facebook.com`
- `"{{company_name}}" site:youtube.com`

**IMPORTANT**: Always capture the full company LinkedIn URL (e.g., `https://linkedin.com/company/brandx`). This URL is required for downstream skills (decision-maker-finder, outreach).

For each found profile, extract:
- Handle / URL
- Follower count (if visible in search results)
- Posting frequency (active daily, weekly, sporadic, dormant)
- Content type (product shots, lifestyle, UGC, educational, promotional)
- Engagement level (comments, likes relative to followers)

Focus on Instagram and LinkedIn as primary channels for D2C outreach context.

## Phase 4: Team and Growth Signals

WebSearch queries:
- `"{{company_name}}" site:linkedin.com/in` -- find team members
- `"{{company_name}}" "hiring" OR "open roles" OR "careers"`
- `"{{company_name}}" "team" OR "about us"`

Extract:
- Approximate team size (from LinkedIn company page or about page)
- Key people (founder, CEO, head of ecommerce, marketing lead)
- Open roles (indicates growth areas and pain points)
- Recent hires (LinkedIn announcements)
- Growth trajectory (hiring = growing, layoffs = contracting)

## Phase 5: Recent News and Events

WebSearch queries:
- `"{{company_name}}" news {{current_year}}`
- `"{{company_name}}" "raises" OR "funding" OR "acquisition" OR "partnership" OR "launch"`
- `"{{company_name}}" "Series A" OR "seed" OR "pre-seed" OR "revenue"`

Extract:
- Funding events (amount, round, investors)
- Product launches
- Partnerships or collaborations
- Awards or recognition
- Press coverage
- Conference appearances

## Phase 6: Pain Points and Opportunities

Based on all gathered data, identify pain points relevant to the agency's services:

- **Website issues**: Slow load times, poor mobile experience, outdated design, missing trust signals, weak product pages
- **Ecommerce gaps**: No reviews app, no upsell/cross-sell, poor navigation, missing size guides, weak checkout flow
- **Marketing gaps**: Low social engagement, inconsistent posting, no email capture, weak SEO
- **Growth constraints**: Small team trying to do everything, no dedicated ecommerce person, outdated tech stack

Cross-reference findings against `services[].keywords` to identify where the agency can help.

## Phase 7: Personalization Hooks

From all research, distill 3-5 personalization hooks that can be used in outreach:

- Things to compliment (genuine strengths)
- Specific issues to reference (without being critical)
- Shared connections or interests
- Timely references (recent funding, launch, hire)
- Industry-specific angles

Each hook should be a concrete sentence or phrase, ready to drop into a message.

## Phase 8: Output

Return structured JSON:

```json
{
  "company_name": "BrandX",
  "website": "https://brandx.com",
  "linkedin_url": "https://linkedin.com/company/brandx",
  "business_summary": "D2C skincare brand founded in 2021, selling premium organic face serums. Based in Mumbai, targeting 25-35 urban women.",
  "business_model": "D2C",
  "industry": "Skincare / Beauty",
  "founded": "2021",
  "location": "Mumbai, India",
  "tech_stack": {
    "platform": "Shopify",
    "theme": "Dawn 12.0",
    "apps_visible": ["Judge.me Reviews", "Klaviyo", "ReConvert"],
    "payment": ["Razorpay", "UPI"],
    "analytics": ["Google Analytics"],
    "email_marketing": "Klaviyo"
  },
  "social": {
    "instagram": {
      "handle": "@brandx",
      "followers": "12.5K",
      "posting_frequency": "3-4 times/week",
      "content_type": "Product photography + UGC reels",
      "engagement": "Medium (2-3% engagement rate)"
    },
    "linkedin": {
      "url": "https://linkedin.com/company/brandx",
      "followers": "450",
      "activity": "Monthly posts"
    },
    "twitter": null,
    "youtube": null
  },
  "team_size": "15-25",
  "key_people": [
    {"name": "Jane Doe", "title": "Founder & CEO", "linkedin": "..."},
    {"name": "John Smith", "title": "Head of Marketing", "linkedin": "..."}
  ],
  "open_roles": ["Performance Marketing Manager", "Graphic Designer"],
  "recent_news": [
    "Raised $500K seed round from XYZ Ventures (Jan 2024)",
    "Launched new vitamin C serum line (Dec 2023)"
  ],
  "pain_points": [
    "Product pages lack detailed ingredient breakdowns",
    "No before/after imagery for skincare results",
    "Mobile checkout flow has 4 steps (high friction)",
    "No loyalty or referral program visible"
  ],
  "strengths": [
    "Strong Instagram aesthetic and consistent branding",
    "Good product photography",
    "Active founder with LinkedIn presence"
  ],
  "personalization_hooks": [
    "Reference their recent seed round -- perfect time to invest in the storefront",
    "Their product pages are missing ingredient breakdowns, which skincare shoppers expect",
    "Compliment their Instagram aesthetic and suggest extending it to the Shopify experience",
    "Their new vitamin C line launch is a great moment to optimize product pages for conversion",
    "They're hiring a marketing manager, which means they're scaling -- the store needs to scale too"
  ],
  "researched_at": "2024-01-15T14:30:00Z",
  "depth": "standard",
  "search_count": 10
}
```

## Example Usage

Trigger phrases:
- "Research this company"
- "Tell me about [company] before I reach out"
- "Deep dive on [company]"
- "Company intel for [company]"
- "Prep research for outreach to [company]"

```
User: Research BrandX before I email their founder
Assistant: [runs 10-12 WebSearches, analyzes site, social, news, returns structured JSON with personalization hooks]
```

```
User: Quick research on this company: example.com
Assistant: [runs 3-5 quick searches, returns condensed version]
```
