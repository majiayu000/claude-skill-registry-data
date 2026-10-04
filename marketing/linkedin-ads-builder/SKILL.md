---
name: linkedin-ads-builder
description: Build LinkedIn Ads campaigns with ABM targeting, professional ad copy, and format recommendations
tags: [linkedin-ads, abm, b2b-ads, paid-social, account-based-marketing]
---

# LinkedIn Ads Builder

Builds LinkedIn Ad campaigns with ABM (Account-Based Marketing) focus: defines campaign objectives, builds precise audience targeting (job titles, company size, industry, seniority, account lists), generates professional ad copy within LinkedIn's character limits, recommends ad formats (single image, carousel, document, video, conversation ads), and defines budget and bidding strategies. Outputs a complete campaign blueprint optimized for B2B.

## Prerequisites

- WebSearch tool available for audience research and industry intelligence
- Business services, ICP details, and budget range
- Optional: `agency.config.json` for ICP, services, and targeting details
- Optional: target account list for ABM campaigns

## Capabilities Used

1. `ad-creative-intel` -- for professional creative angle research
2. `ad-spy` -- for competitor LinkedIn ad analysis
3. `landing-page-auditor` -- for ad-to-page consistency

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `icp.segments[]` for targeting: job titles, seniority, industries, company sizes.
3. Extract `services[]` for offer and messaging.
4. Extract `case_studies[]` for proof points.
5. Extract `brand_voice` for professional tone guidelines.
6. Check `tools.websearch` availability.
7. Accept parameters:
   - `business_name` -- (required) business name
   - `objective` -- (optional) `brand_awareness` | `website_visits` | `engagement` | `lead_gen` | `video_views`. Default: `lead_gen`
   - `services` -- (optional) array of services to promote. Default: derive from config
   - `landing_page` -- (optional) destination URL
   - `budget_monthly` -- (optional) monthly budget in local currency
   - `target_accounts` -- (optional) array of specific company names for ABM
   - `abm_mode` -- (optional) boolean. When true, builds account-specific campaigns. Default: false
   - `content_assets` -- (optional) list of available content (whitepapers, case studies, webinars)

## Phase 1: Campaign Objective Selection

### LinkedIn Objective Mapping

| Business Goal | LinkedIn Objective | Optimization | Best For |
|--------------|-------------------|-------------|----------|
| Brand building | Brand Awareness | Impressions | Top of funnel, new market entry |
| Content distribution | Website Visits | Link clicks | Blog posts, case studies, reports |
| Thought leadership | Engagement | Post interactions | Building credibility, social proof |
| Lead capture | Lead Gen Forms | Leads | Direct lead generation, gated content |
| Video content | Video Views | Video views | Product demos, testimonials, thought leadership |

### Campaign Structure

**Standard B2B Campaigns**
```
Campaign: [Service] - [Objective]
  Ad Set: Decision Makers - Large Enterprise
  Ad Set: Decision Makers - Mid-Market
  Ad Set: Influencers / Champions
  Ad Set: Retargeting - Website Visitors
```

**ABM Campaign Structure**
```
Campaign: ABM - [Account Tier]
  Ad Set: Tier 1 Accounts - Decision Makers
  Ad Set: Tier 1 Accounts - Influencers
  Ad Set: Tier 2 Accounts - Decision Makers
  Ad Set: Tier 2 Accounts - Influencers
```

## Phase 2: Audience Targeting

### Professional Targeting Dimensions

**Job Title Targeting**
Build layered job title targeting from ICP:
- C-suite: CEO, CTO, CMO, CFO, COO
- VP level: VP Marketing, VP Ecommerce, VP Digital, VP Engineering
- Director level: Director of Marketing, Director of Ecommerce, Head of Digital
- Manager level: Marketing Manager, Ecommerce Manager, Brand Manager
- Use "OR" within levels, layer with industry/company size

**Seniority Targeting**
- Owner/Partner
- CXO
- VP
- Director
- Manager
- Use seniority + function (Marketing, Sales, IT, Operations) for precision

**Company Size Targeting**
Segment by employee count to match ICP:
- 1-10 (micro): startups, solopreneurs
- 11-50 (small): early-stage companies
- 51-200 (mid-market): growing companies with teams
- 201-500 (upper mid-market): established with departments
- 501-1000 (enterprise): large organizations
- 1001-5000 (large enterprise): major corporations
- 5001+ (mega enterprise): global corporations

**Industry Targeting**
Select from LinkedIn's industry taxonomy:
- Primary industries from ICP
- Adjacent industries where services are relevant
- Exclude irrelevant industries to reduce waste

**Company List (ABM)**
For ABM campaigns:
- Upload target account list (company names matched to LinkedIn Company Pages)
- Tier accounts by priority: Tier 1 (highest priority, custom messaging), Tier 2 (high value), Tier 3 (broader target)
- Layer company list with job title/seniority for precision
- Minimum company list size: 300+ companies (LinkedIn requirement for matching)

### Audience Layering Strategy
Build audiences by combining dimensions:

**Narrow and Precise** (smaller audience, higher relevance)
- Job title + Industry + Company size + Geography
- Best for: ABM, high-value offers, limited budget

**Broad and Expansive** (larger audience, lower CPL)
- Seniority + Function + Geography
- Best for: Awareness, content distribution, large budget

### Exclusions
- Current customers (upload exclusion list)
- Current employees
- Competitors (exclude by company name)
- Recent converters (past 30-90 days)

### Audience Size Guidelines
- Lead Gen: 50K - 500K (sweet spot for B2B)
- Brand Awareness: 300K - 1M+
- ABM Tier 1: 5K - 50K (accept smaller sizes for high-value accounts)
- If audience < 10K, broaden targeting or combine with other segments

## Phase 3: Ad Copy Generation

### Intro Text (up to 600 characters, 150 for preview)
Write 3-5 variants:

**Variant Approaches for LinkedIn**
- **Insight lead**: Open with an industry insight or statistic
- **Challenge lead**: Open with a challenge the audience faces
- **Result lead**: Open with a client result or case study metric
- **Thought leadership lead**: Open with a perspective or opinion
- **Direct offer lead**: Open with the value proposition directly

### LinkedIn Copy Best Practices
- Professional but not corporate (conversational authority)
- First person singular ("I") for personal content, first person plural ("We") for company content
- Lead with value, not your company name
- Use line breaks every 1-2 sentences for readability
- Include a clear CTA at the end of intro text
- Hashtags: 3-5 relevant hashtags at the end (optional, improves organic reach)
- Tag relevant companies or people (when appropriate)

### Headline (max 70 characters for single image, 45 for carousel cards)
Write 3-5 headline options:
- Benefit-focused: "Increase Shopify Conversions by 40%"
- Offer-focused: "Free Ecommerce CRO Audit"
- Question-focused: "Is Your Store Losing Revenue?"
- Data-focused: "2024 D2C Conversion Benchmarks"
- Authority-focused: "Trusted by 100+ D2C Brands"

### Description (max 70 characters for sponsored content)
Write 2-3 description options:
- Supporting benefit
- Secondary CTA
- Social proof snippet

### CTA Button
LinkedIn options:
- Learn More (default, works for most)
- Sign Up (lead gen, webinars)
- Download (whitepapers, reports)
- Get Quote (services)
- Apply Now (programs, accelerators)
- Register (events, webinars)
- Subscribe (newsletters)

## Phase 4: Ad Format Recommendations

### Format Selection

**Single Image Ad**
- Best for: direct response, lead gen, simple offers
- Specs: 1200 x 627 (1.91:1) or 1080 x 1080 (1:1)
- Text on image: minimal, focus on a single message
- Works with Lead Gen Forms for frictionless conversion

**Carousel Ad (2-10 cards)**
- Best for: storytelling, multi-benefit showcase, process walkthrough
- Specs: 1080 x 1080 per card
- Each card: image + headline (45 chars)
- Strategy: problem > insight > solution > proof > CTA arc across cards
- Drives higher engagement than single image

**Document Ad (native PDF carousel)**
- Best for: thought leadership, educational content, frameworks
- Upload PDF that users swipe through in-feed
- Generates high engagement and saves
- Top format for building authority and trust
- Ideal content: industry reports, how-to guides, benchmark data, frameworks

**Video Ad**
- Best for: testimonials, product demos, thought leadership
- Specs: 1:1 or 16:9, 15-90 seconds recommended
- Captions required (most LinkedIn browsing is without sound)
- Hook in first 3 seconds
- End with CTA frame and logo

**Conversation Ad (Message Ad)**
- Best for: ABM, high-value offers, event invitations
- Delivered to LinkedIn inbox
- Multiple CTA buttons creating a choose-your-own-adventure flow
- Higher engagement than email for B2B decision makers
- Use sparingly: max 1 conversation ad per person per 30 days (LinkedIn limit)
- Best when sent from a real person's profile, not company page

**Text Ad**
- Best for: always-on brand awareness, low budget supplementary
- Small image (100 x 100) + headline (25 chars) + description (75 chars)
- Appears in right rail on desktop
- Low CPM, good for sustained visibility

### Format-to-Objective Matrix

| Objective | Primary Format | Secondary Format |
|-----------|---------------|-----------------|
| Brand Awareness | Video, Document | Carousel |
| Website Visits | Single Image | Carousel |
| Lead Gen | Single Image + Lead Form | Conversation Ad |
| Engagement | Document, Video | Carousel |
| ABM | Conversation Ad | Single Image + Lead Form |

## Phase 5: Lead Gen Form Design (if applicable)

### LinkedIn Lead Gen Form Structure
LinkedIn Lead Gen Forms are pre-filled from profile data, reducing friction:

**Recommended Fields** (auto-filled from LinkedIn profile)
- First name
- Last name
- Email address (professional email)
- Company name
- Job title
- Company size

**Optional Custom Fields** (manual entry, adds friction)
- Website URL
- Phone number
- Custom questions (dropdown, single line, multi-line)
- Hidden fields for UTM tracking

### Form Best Practices
- Keep to 3-5 fields maximum (including auto-filled)
- Lead with auto-filled fields (zero-friction experience)
- Add max 1-2 custom fields
- Include a clear privacy policy link
- Offer a thank-you page with next steps or downloadable content
- Set up CRM integration for instant lead routing

## Phase 6: Budget and Bidding

### LinkedIn Ad Costs (Benchmark Ranges)
- Average CPC: $5-12 USD (B2B average)
- Average CPM: $30-80 USD
- Average CPL (Lead Gen Form): $25-75 USD
- Minimum daily budget: $10 USD per campaign

### Budget Allocation for B2B

| Campaign Type | Budget % | Rationale |
|--------------|----------|-----------|
| Lead Gen (core offer) | 40% | Direct pipeline generation |
| Content/Engagement | 25% | Builds trust and retargeting audiences |
| ABM (Tier 1 accounts) | 20% | High-value account targeting |
| Retargeting | 15% | Re-engage warm audiences |

### Bidding Strategy
- **Lead Gen**: Maximum delivery (start), then bid cap once CPL baseline is established
- **Awareness**: Maximum delivery
- **Website visits**: Maximum delivery, monitor CPC
- **ABM**: Manual bidding, higher bids to ensure delivery to small audiences

### Optimization Schedule
- Week 1-2: Gather data, no changes (learning phase)
- Week 3: First optimization round (pause low performers, scale winners)
- Week 4+: Ongoing optimization every 5-7 days
- Creative refresh every 4-6 weeks (ad fatigue on LinkedIn is real)

## Phase 7: Output

Return structured JSON:

```json
{
  "business_name": "Example Agency",
  "built_at": "2024-01-15T14:30:00Z",
  "objective": "lead_gen",
  "abm_mode": false,
  "monthly_budget": "2000 USD",
  "campaigns": [
    {
      "campaign_name": "Lead Gen - Shopify CRO Services",
      "objective": "Lead Generation",
      "format": "Single Image + Lead Gen Form",
      "audience": {
        "job_titles": ["VP Marketing", "VP Ecommerce", "Head of Digital", "Director of Marketing", "Ecommerce Manager"],
        "seniority": ["VP", "Director", "Manager"],
        "company_size": ["51-200", "201-500", "501-1000"],
        "industries": ["Retail", "Consumer Goods", "Fashion", "Food & Beverages"],
        "geography": "India",
        "exclusions": ["Current customers", "Competitors"],
        "estimated_audience_size": "120K"
      },
      "ads": [
        {
          "ad_name": "Result Lead - Kibi Case Study",
          "format": "Single Image",
          "intro_text": "We helped a D2C sports brand increase their Shopify conversion rate by 40% in 8 weeks.\n\nThe fix wasn't a redesign. It was a systematic CRO audit that identified 23 conversion blockers across their product pages, checkout flow, and mobile experience.\n\nIf your Shopify store converts below 2%, you're leaving revenue on the table.\n\nGet a free CRO audit and see exactly what's holding your store back.\n\n#ShopifyCRO #D2C #Ecommerce",
          "headline": "Free Shopify CRO Audit",
          "description": "Find your conversion blockers",
          "cta": "Learn More",
          "creative_brief": "Clean image showing a before/after conversion rate chart. Professional, data-driven aesthetic. Brand colors."
        }
      ],
      "lead_gen_form": {
        "form_name": "Free CRO Audit Request",
        "headline": "Get Your Free CRO Audit",
        "description": "We'll analyze your Shopify store and identify the top conversion blockers. No commitment required.",
        "fields": [
          { "field": "First name", "type": "auto-filled" },
          { "field": "Last name", "type": "auto-filled" },
          { "field": "Email", "type": "auto-filled" },
          { "field": "Company name", "type": "auto-filled" },
          { "field": "Store URL", "type": "custom_single_line" }
        ],
        "privacy_policy_url": "https://example.com/privacy",
        "thank_you_message": "Thanks! We'll send your CRO audit within 48 hours."
      },
      "budget_allocation": "40%"
    }
  ],
  "abm_campaign": {
    "note": "ABM mode not enabled. To build account-specific campaigns, provide a target account list and set abm_mode: true.",
    "abm_audience_requirements": {
      "minimum_company_list_size": 300,
      "recommended_tier_structure": "Tier 1 (top 50), Tier 2 (next 100), Tier 3 (remaining)"
    }
  },
  "testing_plan": {
    "initial_variants": "2-3 per campaign",
    "learning_period": "2 weeks (minimum 15 conversions per variant)",
    "optimization_cadence": "Every 5-7 days after learning period",
    "creative_refresh": "Every 4-6 weeks"
  },
  "projected_metrics": {
    "estimated_impressions": "30K-60K per month",
    "estimated_ctr": "0.5-1.2%",
    "estimated_cpc": "$5-10 USD",
    "estimated_cpl": "$30-60 USD",
    "estimated_monthly_leads": "33-66"
  }
}
```

## Example Usage

Trigger phrases:
- "Build LinkedIn Ads for [business]"
- "LinkedIn lead gen campaign for [service]"
- "ABM campaign on LinkedIn for [account list]"
- "LinkedIn ads targeting [job titles] in [industry]"
- "Write LinkedIn ad copy for [offer]"

```
User: Build LinkedIn Ads for plasho.com targeting D2C ecommerce directors in India
Assistant: [reads config, builds job title + seniority + industry targeting, generates professional ad copy, recommends Single Image + Lead Gen Form, returns complete campaign blueprint]
```

```
User: LinkedIn ABM campaign for these 50 target accounts: [list]
Assistant: [tiers accounts by priority, builds account-list targeting with seniority layers, creates Conversation Ads for Tier 1, Single Image for Tier 2, returns ABM campaign structure]
```

```
User: Write LinkedIn ad copy for a Shopify CRO case study
Assistant: [generates 5 intro text variants, 5 headlines, 3 descriptions within LinkedIn char limits, recommends Document Ad format, returns formatted ad copy set]
```
