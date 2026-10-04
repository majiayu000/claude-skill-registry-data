---
name: ad-spy
description: Monitor competitor ads across Meta, Google, and LinkedIn with strategic analysis
tags: [competitive-intel, ads, meta-ads, google-ads, ad-monitoring]
---

# Ad Spy

Monitors competitor advertising across platforms by searching Meta Ad Library, Google Ads Transparency Center, and LinkedIn Ad Library. Analyzes ad copy themes, offers, CTAs, landing pages, creative formats, and estimated spend patterns. Outputs a competitive ad intelligence report with actionable insights for your own campaigns.

## Prerequisites

- WebSearch tool available for searching ad libraries and transparency centers
- Browser automation tool for navigating ad library interfaces
- Competitor names and/or domains to monitor
- Optional: `agency.config.json` for industry context and competitor list

## Capabilities Used

1. `ad-creative-intel` -- for deeper analysis of winning creative patterns
2. `landing-page-auditor` -- for evaluating competitor landing pages

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `competitors[]` for default competitor list.
3. Extract `services[]` for understanding which ad categories are relevant.
4. Extract `icp.segments[]` for audience overlap analysis.
5. Check `tools.websearch` and `tools.browser` availability.
6. Accept parameters:
   - `competitors` -- (required) array of competitor names or domains
   - `platforms` -- (optional) `meta` | `google` | `linkedin` | `all`. Default: `all`
   - `timeframe` -- (optional) `last_7_days` | `last_30_days` | `last_90_days` | `all_time`. Default: `last_30_days`
   - `focus` -- (optional) `copy` | `creative` | `offers` | `landing_pages` | `all`. Default: `all`
   - `industry` -- (optional) industry vertical for broader competitive scan

## Phase 1: Meta Ad Library Search

### Search Meta Ad Library
For each competitor:
- WebSearch: `site:facebook.com/ads/library "{{competitor_name}}"` -- find their ad library page
- WebSearch: `"{{competitor_name}}" meta ad library OR facebook ad library`
- Navigate to Meta Ad Library (facebook.com/ads/library) via browser automation
- Search for the competitor page name
- Filter by: country, active ads, media type

### Extract Ad Data
For each active ad found:
- Ad creative type (image, video, carousel)
- Primary text (full ad copy)
- Headline and description
- CTA button type
- Landing page URL
- Start date (how long has the ad been running -- longer = likely performing well)
- Multiple versions (A/B testing indicators)
- Platform placement (Facebook, Instagram, Messenger, Audience Network)

### Pattern Analysis
- **Copy themes**: What messaging angles do they use most? (pain point, benefit, social proof, urgency)
- **Offer patterns**: What offers appear? (free trial, discount, lead magnet, demo)
- **CTA patterns**: Which CTAs dominate? (Learn More, Sign Up, Shop Now, Get Quote)
- **Creative patterns**: Image vs video ratio, UGC vs polished, text-heavy vs visual
- **Longevity signals**: Ads running > 30 days are likely profitable

## Phase 2: Google Ads Transparency Center

### Search Google Ads Transparency
For each competitor:
- WebSearch: `site:adstransparency.google.com "{{competitor_name}}"` OR `"{{competitor_domain}}"`
- WebSearch: `"{{competitor_name}}" google ads transparency`
- Navigate to adstransparency.google.com via browser automation
- Search by advertiser name or domain

### Extract Ad Data
For each ad found:
- Ad format (text ad, display ad, video ad, shopping ad)
- Ad copy (headlines, descriptions)
- Display URL and destination URL
- Geographic targeting (where ads are shown)
- Date range of activity
- Ad variations

### Search Ads Analysis
- **Keyword themes**: What search terms are they bidding on? (inferred from ad copy)
- **Value propositions**: What do they lead with?
- **Competitive positioning**: How do they differentiate?
- **Landing page alignment**: Does the ad match the landing page?
- **Extension usage**: Sitelinks, callouts, structured snippets visible

## Phase 3: LinkedIn Ad Intelligence

### Search LinkedIn Ads
For each competitor:
- WebSearch: `"{{competitor_name}}" linkedin ads` -- find references to their LinkedIn advertising
- Visit the competitor's LinkedIn company page
- Check the "Ads" tab on their company page (if available)
- WebSearch: `site:linkedin.com "{{competitor_name}}" sponsored`

### Extract Ad Data
For each ad found:
- Ad format (single image, carousel, video, document, conversation ad, text ad)
- Ad copy (intro text, headline, description)
- CTA type
- Content topic and angle
- Targeting signals (inferred from content -- who is this ad speaking to?)

### LinkedIn-Specific Analysis
- **Content marketing vs direct response**: Are they promoting thought leadership or driving leads?
- **ABM signals**: Are they running account-specific campaigns?
- **Retargeting indicators**: Are they showing ads to page followers and website visitors?
- **Sponsored content vs message ads**: Which formats are they using?

## Phase 4: Landing Page Analysis

### For Each Unique Landing Page Found
- Visit the landing page via browser automation
- Analyze:
  - Page type (homepage, service page, dedicated landing page, lead gen form)
  - Above-fold content (headline, subheadline, CTA, hero image/video)
  - Message match with the ad (does the landing page deliver on the ad's promise?)
  - Social proof elements (testimonials, logos, case studies, reviews)
  - Form length and friction (number of fields, multi-step?)
  - Page load speed (subjective assessment)
  - Mobile optimization
  - Trust signals (security badges, guarantees, certifications)

### Landing Page Patterns
- Which landing page types perform best (inferred from ad longevity)?
- Common conversion elements across top competitors
- Gaps in competitor landing pages (what they're missing)

## Phase 5: Spend and Performance Estimation

### Activity Volume
- Count total active ads per competitor per platform
- Track ad variations (more variations = more testing = more budget)
- Note geographic spread (more countries = larger budget)

### Spend Indicators
- **High spend signals**: Many active ads, long-running campaigns, multiple creatives, broad geographic targeting
- **Low spend signals**: Few ads, short campaigns, single creative, narrow targeting
- **Testing signals**: Many variations launched recently, short-lived ads, frequent creative changes

### Competitive Positioning Map
Rank competitors by estimated ad activity:
- Heavy advertiser (50+ active ads, multi-platform, multi-country)
- Moderate advertiser (10-50 active ads, 1-2 platforms)
- Light advertiser (< 10 active ads, single platform)
- Inactive (no ads found)

## Phase 6: Strategic Insights

### Opportunity Gaps
- Platforms where competitors are absent (opportunity to be first)
- Ad formats competitors aren't using (video, carousel, UGC)
- Messaging angles nobody is covering
- Audience segments being ignored
- Landing page weaknesses you can exploit

### Threats
- Competitor ads directly targeting your brand name
- Competitors outspending in your core keywords
- Competitor offers that undercut your pricing
- Creative quality that outclasses yours

### Recommendations
For each finding, provide an actionable recommendation:
- Specific ad to counter or learn from
- Creative angle to adopt or improve upon
- Landing page element to implement
- Budget allocation adjustment needed

## Phase 7: Output

Return structured JSON:

```json
{
  "analyzed_at": "2024-01-15T14:30:00Z",
  "competitors_analyzed": ["competitor1.com", "competitor2.com"],
  "platforms_searched": ["Meta", "Google", "LinkedIn"],
  "timeframe": "last_30_days",
  "competitor_profiles": [
    {
      "competitor": "competitor1.com",
      "estimated_activity_level": "Heavy advertiser",
      "platforms_active": ["Meta", "Google"],
      "total_active_ads": 47,
      "meta_ads": {
        "active_count": 32,
        "formats": { "image": 18, "video": 10, "carousel": 4 },
        "longest_running_ad": {
          "days_active": 67,
          "primary_text": "Struggling with Shopify conversions?...",
          "headline": "Free Store Audit",
          "cta": "Sign Up",
          "landing_page": "https://competitor1.com/free-audit",
          "takeaway": "Pain point + free offer combo running 67 days -- likely profitable"
        },
        "top_messaging_themes": ["Pain point: low conversions", "Social proof: client numbers", "Offer: free audit"],
        "top_ctas": ["Sign Up", "Learn More"],
        "creative_style": "Mix of polished brand images and UGC testimonial videos"
      },
      "google_ads": {
        "active_count": 15,
        "ad_types": { "search": 12, "display": 3 },
        "keyword_themes_inferred": ["shopify agency", "ecommerce development", "CRO services"],
        "top_headlines": ["Expert Shopify Development", "Boost Your Conversions by 40%"],
        "geographic_targeting": ["India", "US"]
      },
      "linkedin_ads": null,
      "landing_pages": [
        {
          "url": "https://competitor1.com/free-audit",
          "type": "Lead gen landing page",
          "message_match": "Strong -- headline matches ad promise",
          "form_fields": 4,
          "social_proof": "3 client logos, 1 testimonial",
          "strengths": ["Clear headline", "Short form", "Strong social proof"],
          "weaknesses": ["No video", "No specific case study numbers", "Generic design"]
        }
      ]
    }
  ],
  "cross_competitor_insights": {
    "most_common_messaging": "Pain point: low conversions + offer: free audit",
    "most_common_format": "Single image on Meta, text ads on Google",
    "underused_formats": ["Video on Google", "Carousel on LinkedIn", "UGC style"],
    "underserved_platforms": ["LinkedIn -- only 1 of 3 competitors active"],
    "pricing_signals": ["Competitor1 offers free audit, Competitor2 leads with pricing"]
  },
  "opportunity_gaps": [
    "No competitor is running LinkedIn ads -- first-mover advantage",
    "No competitor is using video testimonials -- UGC opportunity",
    "All competitors use generic stock imagery -- custom visuals would stand out"
  ],
  "threats": [
    "Competitor1 has been running the same ad for 67 days -- their free audit funnel is working",
    "Competitor2 is bidding on brand keywords in Google Search"
  ],
  "recommended_actions": [
    "Launch LinkedIn ads targeting D2C founders -- no competitor presence",
    "Create UGC video testimonials to differentiate from stock-image competitors",
    "Counter Competitor1's free audit with a more specific offer (e.g., 'Free CRO Scorecard')",
    "Set up brand defense campaign on Google to protect brand keywords"
  ]
}
```

## Phase 8: Review Gate

Present findings to the user. The user may:
- Request deeper analysis on a specific competitor
- Ask for screenshots of competitor ads
- Request landing page teardowns
- Ask for specific counter-strategies

## Example Usage

Trigger phrases:
- "Spy on [competitor]'s ads"
- "What ads are [competitor] running?"
- "Competitor ad analysis for [industry]"
- "Monitor [competitor] ad campaigns"
- "Ad intelligence report on [competitor list]"

```
User: What ads are competitor1.com running?
Assistant: [searches Meta Ad Library, Google Ads Transparency, LinkedIn, analyzes all active ads, returns intelligence report with insights]
```

```
User: Competitor ad spy for Shopify agencies in India
Assistant: [identifies top Shopify agencies, searches their ads across platforms, compares strategies, returns competitive landscape report]
```

```
User: Spy on competitor1.com and competitor2.com -- focus on Meta ads
Assistant: [deep dive into Meta Ad Library for both, analyzes copy, creative, offers, landing pages, returns head-to-head comparison]
```
