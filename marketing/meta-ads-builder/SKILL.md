---
name: meta-ads-builder
description: Build Meta/Instagram ad campaigns with audience targeting, ad copy, and creative specs
tags: [meta-ads, facebook-ads, instagram-ads, paid-social, targeting]
---

# Meta Ads Builder

Builds Meta (Facebook/Instagram) ad campaigns end-to-end: defines campaign objectives, builds audience targeting (interests, behaviors, lookalikes, custom audiences derived from ICP), generates ad copy variants for each placement, recommends creative formats and specs, defines budget allocation, and outputs a complete campaign blueprint ready for setup in Meta Ads Manager.

## Prerequisites

- WebSearch tool available for audience research and competitor ad analysis
- Business services, target audience, and budget range
- Optional: `agency.config.json` for ICP, services, and brand voice
- Optional: Meta Ad Library access via WebSearch for competitive intelligence

## Capabilities Used

1. `ad-creative-intel` -- for winning creative angles and hook patterns
2. `ad-spy` -- for competitor ad intelligence
3. `landing-page-auditor` -- for ad-to-landing-page consistency

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `icp.segments[]` for audience targeting: job titles, industries, company sizes, pain points.
3. Extract `services[]` for offer messaging.
4. Extract `case_studies[]` for social proof in ad copy.
5. Extract `brand_voice` for tone and style guidelines.
6. Check `tools.websearch` availability.
7. Accept parameters:
   - `business_name` -- (required) business name
   - `objective` -- (optional) `awareness` | `consideration` | `conversion` | `lead_gen`. Default: `lead_gen`
   - `services` -- (optional) array of services to promote. Default: derive from config
   - `landing_page` -- (optional) destination URL
   - `budget_monthly` -- (optional) monthly budget in local currency
   - `target_market` -- (optional) geographic targeting
   - `existing_assets` -- (optional) list of available creative assets (images, videos)
   - `offer` -- (optional) specific offer or lead magnet to promote

## Phase 1: Campaign Objective Selection

### Objective Mapping
Based on the goal, recommend the appropriate Meta campaign objective:

| Business Goal | Meta Objective | Optimization Event | Best For |
|--------------|---------------|-------------------|----------|
| Brand awareness | Awareness | Reach / Ad recall lift | New market entry, top of funnel |
| Website traffic | Traffic | Link clicks / Landing page views | Content promotion, blog traffic |
| Lead generation | Leads | Lead form / Conversions | B2B leads, service inquiries |
| Conversions | Sales | Purchase / Add to cart | Ecommerce, direct response |
| Engagement | Engagement | Post engagement / Video views | Community building, social proof |

### Campaign Structure
```
Campaign: [Objective] - [Service/Offer]
  Ad Set 1: Cold - Interest Targeting
  Ad Set 2: Cold - Lookalike Audience
  Ad Set 3: Warm - Website Retargeting
  Ad Set 4: Hot - Engaged Retargeting
```

## Phase 2: Audience Targeting

### Cold Audiences (Prospecting)

**Interest-Based Targeting**
Build interest targeting from ICP:
- Job title interests (CEO, Founder, Marketing Director, Ecommerce Manager)
- Industry interests (ecommerce, D2C, retail, specific verticals)
- Tool/platform interests (Shopify, WooCommerce, Magento -- indicates ecommerce involvement)
- Publication/thought leader interests (industry blogs, influencers)
- Behavior signals (business page admins, small business owners, online purchasers)
- Narrow with AND conditions to improve quality

**Lookalike Audiences**
Recommend lookalike sources:
- Website visitors (past 90 days) -- 1% lookalike
- Email list / CRM contacts -- 1% lookalike
- Lead form completers -- 1% lookalike
- Top customers (by LTV) -- 1% lookalike
- Page engagers -- 2-3% lookalike (wider)
- Video viewers (50%+) -- 2% lookalike

**Demographic Filters**
- Age range: based on ICP (typically 25-55 for B2B)
- Location: target market geography
- Language: as appropriate
- Exclude existing customers and recent converters

### Warm Audiences (Retargeting)

**Website Retargeting**
- All website visitors, last 30 days
- Specific page visitors (pricing, services, case studies), last 60 days
- Add-to-cart / initiate checkout but didn't convert, last 14 days

**Engagement Retargeting**
- Video viewers (25%, 50%, 75%), last 30 days
- Post/ad engagers, last 30 days
- Instagram profile visitors, last 30 days
- Lead form openers who didn't submit, last 30 days

### Audience Sizing
For each audience:
- Estimate audience size based on targeting parameters
- Flag audiences that are too small (< 10K) or too broad (> 10M)
- Recommend adjustments to hit the sweet spot (100K - 2M for prospecting)

## Phase 3: Ad Copy Generation

### Primary Text (up to 600 characters recommended, 125 for preview)
Write 3-5 variants for each ad set:

**Variant Types**
- **Pain point lead**: Open with the audience's biggest frustration
- **Result lead**: Open with a specific outcome or case study number
- **Question lead**: Open with a question that triggers self-identification
- **Story lead**: Open with a mini narrative or client transformation
- **Authority lead**: Open with a credibility signal or industry insight

### Headline (max 40 characters)
Write 3-5 headline options:
- Direct benefit statement
- Offer/lead magnet focused
- Social proof focused
- Curiosity/question focused
- Urgency focused

### Description (max 30 characters)
Write 2-3 description options:
- Reinforce the headline
- Add a supporting benefit
- Include a CTA variation

### CTA Button
Recommend from Meta's options:
- Learn More (awareness/consideration)
- Sign Up (lead gen)
- Get Quote (services)
- Shop Now (ecommerce)
- Book Now (appointments)
- Download (lead magnet)
- Contact Us (direct response)

### Copy Rules
- First line must hook attention (appears in preview)
- Use line breaks for readability
- Include social proof numbers where possible
- Match the ad copy tone to the audience temperature (cold = educational, warm = direct)
- No clickbait, no misleading claims
- Emojis: use sparingly and only if on-brand (max 2-3 per ad)

## Phase 4: Creative Format Recommendations

### Format Selection by Objective

| Objective | Best Formats | Why |
|-----------|-------------|-----|
| Awareness | Video (15-30s), Carousel | Video drives recall, carousel tells a story |
| Traffic | Single image, Link ad | Clear CTA, fast load |
| Lead gen | Single image, Carousel, Video | Image for simplicity, carousel for education |
| Conversion | Single image, Video, Collection | Direct response, product showcase |

### Creative Specs per Format

**Single Image**
- Recommended: 1080 x 1080 (1:1) for feed, 1080 x 1920 (9:16) for Stories/Reels
- Max file size: 30MB
- Text on image: < 20% of image area
- Clear visual hierarchy: image > headline > CTA

**Carousel (2-10 cards)**
- Each card: 1080 x 1080
- Tell a sequential story or showcase multiple benefits/services
- First card must hook, last card must CTA
- Consistent visual style across all cards

**Video**
- Feed: 1:1 or 4:5, 15-60 seconds
- Stories/Reels: 9:16, 15-30 seconds
- Hook in first 3 seconds
- Captions required (85% of video is watched without sound)
- End with clear CTA frame

**UGC Style**
- Raw, authentic look outperforms polished in many B2B contexts
- Talking head + screen recording
- Client testimonial clips
- Behind-the-scenes process footage

### Creative Brief per Ad Set
For each ad set, specify:
- Visual concept (what the image/video shows)
- Text overlay (if any)
- Mood and style (professional, casual, bold, minimal)
- Reference to `ad-creative-intel` for winning angle inspiration

## Phase 5: Budget and Bidding

### Budget Allocation Strategy
Distribute monthly budget across ad sets:

| Ad Set | Budget % | Rationale |
|--------|----------|-----------|
| Cold - Interest | 35% | Largest audience, prospecting |
| Cold - Lookalike | 25% | High-quality prospecting |
| Warm - Website Retarget | 25% | Highest conversion rate |
| Hot - Engaged Retarget | 15% | Smallest audience, most efficient |

### Bidding Strategy
- **Lead gen**: Lowest cost per result (start), then move to cost cap once CPA is established
- **Conversions**: Lowest cost, then Target ROAS
- **Awareness**: Lowest cost per 1000 impressions
- **Traffic**: Lowest cost per link click

### Testing Plan
- Start with 2-3 ad variants per ad set
- Run for 3-5 days before judging performance
- Kill underperformers (CTR < 1% on feed, CPA > 2x target)
- Scale winners by duplicating ad set with 20% budget increase

## Phase 6: Output

Return structured JSON:

```json
{
  "business_name": "Example Agency",
  "built_at": "2024-01-15T14:30:00Z",
  "objective": "lead_gen",
  "target_market": "India",
  "monthly_budget": "30000 INR",
  "campaigns": [
    {
      "campaign_name": "Lead Gen - Shopify Services",
      "objective": "Leads",
      "optimization_event": "Lead form submission",
      "ad_sets": [
        {
          "ad_set_name": "Cold - Interest Targeting",
          "audience": {
            "interests": ["Shopify", "Ecommerce", "D2C brands", "Online retail"],
            "behaviors": ["Small business owners", "Business page admins"],
            "demographics": { "age": "25-50", "location": "India" },
            "exclusions": ["Existing customers", "Recent converters"],
            "estimated_size": "500K - 1.2M"
          },
          "budget_allocation": "35%",
          "placements": ["Facebook Feed", "Instagram Feed", "Instagram Stories"],
          "ads": [
            {
              "ad_name": "Pain Point - Store Not Converting",
              "format": "Single Image",
              "primary_text": "Your Shopify store is getting traffic but not sales?\n\nMost D2C brands lose 60-70% of potential revenue to poor store UX.\n\nWe helped Kibi Sports increase conversions by 40% in 8 weeks with our CRO audit process.\n\nBook a free 15-min store audit and see exactly what's costing you sales.",
              "headline": "Free Shopify Store Audit",
              "description": "Book Your Audit Today",
              "cta": "Sign Up",
              "landing_page": "https://example.com/free-audit",
              "creative_brief": "Image of a Shopify dashboard with conversion metrics highlighted. Clean, professional, data-focused."
            }
          ]
        }
      ]
    }
  ],
  "testing_plan": {
    "initial_variants": 3,
    "evaluation_period": "5 days",
    "kill_criteria": "CTR < 0.8% or CPA > 2x target",
    "scale_criteria": "CPA < target for 3 consecutive days"
  },
  "projected_metrics": {
    "estimated_reach": "50K-100K per month",
    "estimated_cpm": "80-150 INR",
    "estimated_ctr": "1-2.5%",
    "estimated_cpl": "200-500 INR",
    "estimated_monthly_leads": "60-150"
  }
}
```

## Example Usage

Trigger phrases:
- "Build Meta ads campaigns for [business]"
- "Create Facebook ad campaigns for [service]"
- "Instagram ads for [product/service]"
- "Meta ads audience targeting for [ICP]"
- "Write Facebook ad copy for [offer]"

```
User: Build Meta ads for plasho.com -- target D2C brand founders in India for lead gen
Assistant: [reads config, builds interest + lookalike audiences from ICP, generates ad copy variants, recommends creative formats, allocates budget, returns complete campaign blueprint]
```

```
User: Write Facebook ad copy for a free Shopify audit offer
Assistant: [generates 5 primary text variants, 5 headlines, 3 descriptions, recommends CTA and creative format, returns formatted ad copy set]
```

```
User: Meta ads retargeting campaign for website visitors
Assistant: [builds retargeting audiences by engagement level, writes warm-audience copy, recommends budget allocation, returns campaign structure]
```
