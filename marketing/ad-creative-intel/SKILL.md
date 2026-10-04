---
name: ad-creative-intel
description: Mine winning ad angles, hooks, and creative patterns from top-performing ads
tags: [ad-creative, copywriting, hooks, creative-strategy, swipe-file]
---

# Ad Creative Intel

Mines winning ad creative patterns by researching top-performing ads in the target industry via ad libraries, social feeds, and swipe file databases. Extracts hook patterns, emotional triggers, CTA styles, offer framing, and visual strategies. Categorizes by format (image, video, carousel, UGC) and intent stage. Outputs a creative playbook with reusable angle templates and hook formulas.

## Prerequisites

- WebSearch tool available for researching ad libraries and creative databases
- Browser automation tool for analyzing ad examples
- Industry or niche to research
- Optional: `agency.config.json` for service context and ICP pain points

## Capabilities Used

1. `ad-spy` -- for gathering raw competitor ad data to analyze patterns

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` for understanding what offers to frame creatively.
3. Extract `icp.segments[].pain_points` for emotional trigger mapping.
4. Extract `case_studies[]` for result-based hook material.
5. Extract `brand_voice` for creative tone guidelines.
6. Check `tools.websearch` and `tools.browser` availability.
7. Accept parameters:
   - `industry` -- (required) industry or niche to mine creatives from
   - `platforms` -- (optional) `meta` | `google` | `linkedin` | `tiktok` | `all`. Default: `all`
   - `format_focus` -- (optional) `image` | `video` | `carousel` | `ugc` | `all`. Default: `all`
   - `intent_stage` -- (optional) `awareness` | `consideration` | `conversion` | `all`. Default: `all`
   - `competitor_names` -- (optional) array of specific competitors to mine from
   - `output_style` -- (optional) `playbook` | `swipe_file` | `templates`. Default: `playbook`

## Phase 1: Ad Research and Collection

### Meta Ad Library Mining
- WebSearch: `"{{industry}}" top ads meta ad library` -- find industry ad compilations
- WebSearch: `"{{industry}}" best facebook ads 2024 2025` -- find curated lists
- WebSearch: `"{{industry}}" ad examples swipe file` -- find swipe file collections
- Search Meta Ad Library for top brands in the industry
- Collect 20-30 ads with the longest run times (longevity = performance)

### Google Ads Mining
- WebSearch: `"{{industry}}" best google ads examples`
- WebSearch: target industry keywords and capture ad copy from SERPs
- Note headlines, descriptions, and extensions that stand out
- Collect 10-15 search ad examples

### LinkedIn Ads Mining
- WebSearch: `"{{industry}}" linkedin ad examples`
- WebSearch: `"{{industry}}" sponsored content linkedin`
- Browse industry thought leaders' sponsored posts
- Collect 10-15 LinkedIn ad examples

### Creative Database Research
- WebSearch: `"{{industry}}" ad inspiration` -- find curated databases
- WebSearch: `"{{industry}}" winning ads breakdown` -- find analysis articles
- WebSearch: `"{{industry}}" swipe file` -- find creative collections
- Collect high-quality examples from creative databases

## Phase 2: Hook Pattern Extraction

### Analyze Opening Lines
For each collected ad, extract the first line (the hook) and categorize:

**Pain Point Hooks**
- "Tired of [pain point]?"
- "Still struggling with [problem]?"
- "[Pain point] is costing you [consequence]"
- "If [relatable situation], you need to read this"
- "The #1 reason [audience] fail at [goal]"

**Result/Number Hooks**
- "We helped [client] achieve [specific result]"
- "[Number]% increase in [metric] in [timeframe]"
- "From [before state] to [after state] in [timeframe]"
- "How [client] went from [X] to [Y]"

**Question Hooks**
- "What if you could [desirable outcome]?"
- "Why are top [audience] switching to [solution]?"
- "Do you know the real reason [pain point happens]?"
- "What does [desirable metric] look like for your [business]?"

**Contrarian/Pattern-Interrupt Hooks**
- "Stop [common advice everyone gives]"
- "Everything you know about [topic] is wrong"
- "[Popular strategy] is dead. Here's what works now."
- "Unpopular opinion: [contrarian take]"

**Social Proof Hooks**
- "Join [number]+ [audience] who already [benefit]"
- "[Recognizable brand] switched to us. Here's why."
- "Rated #1 by [authority source]"
- "See why [audience segment] choose [product]"

**Curiosity/Story Hooks**
- "I almost [gave up on / lost / failed at] [goal], until..."
- "The secret [top performers] don't want you to know"
- "3 things I wish I knew before [common action]"
- "A [audience member] just sent us this message..."

## Phase 3: Emotional Trigger Analysis

### Map Emotional Drivers
For each high-performing ad, identify the primary emotional trigger:

| Trigger | How It's Used | Example |
|---------|--------------|---------|
| Fear of missing out | Scarcity, urgency, social proof | "Only 5 spots left this month" |
| Fear of loss | Risk aversion, status quo danger | "You're losing $X every day without this" |
| Aspiration | Future state, transformation | "Imagine your store generating $X/month" |
| Frustration | Pain amplification, empathy | "We know how frustrating it is when..." |
| Pride/Status | Achievement, exclusivity | "Join the elite 1% of brands that..." |
| Trust/Safety | Guarantees, credentials, social proof | "Money-back guarantee. Risk-free." |
| Curiosity | Information gap, teaser | "The framework behind $10M brands" |

### Trigger-to-Funnel Mapping
- **Awareness stage**: Curiosity, aspiration, contrarian hooks
- **Consideration stage**: Fear of loss, frustration, social proof
- **Conversion stage**: FOMO, trust/safety, urgency

## Phase 4: CTA Pattern Analysis

### CTA Styles Found
Categorize CTA approaches from collected ads:

**Direct CTAs**
- "Book a free call"
- "Get your free audit"
- "Start your free trial"
- "Download the guide"

**Soft CTAs**
- "Learn how"
- "See how it works"
- "Read the case study"
- "Watch the demo"

**Urgency CTAs**
- "Claim your spot before [date]"
- "Limited time: get [offer]"
- "Only [X] left at this price"

**Value-First CTAs**
- "Get your free [valuable thing]"
- "See your personalized [result/report]"
- "Calculate your [metric]"

### CTA Performance Indicators
- Which CTAs appear in the longest-running ads?
- Which CTAs match which funnel stages?
- What free offers or lead magnets are most common in the industry?

## Phase 5: Offer Framing Analysis

### Common Offer Structures
Extract and categorize how competitors frame their offers:

- **Free + Value**: Free audit, free consultation, free trial, free guide
- **Discount**: X% off, $X off, buy-one-get-one
- **Guarantee**: Money-back, results guarantee, satisfaction guarantee
- **Exclusivity**: Limited spots, waitlist, invitation-only
- **Bundle**: Package deal, complete solution, all-in-one
- **Risk reversal**: Pay only for results, no commitment, cancel anytime

### Offer-to-Audience Mapping
- Cold audience: free value (guide, tool, audit) -- low commitment
- Warm audience: trial, demo, consultation -- medium commitment
- Hot audience: discount, guarantee, urgency -- high commitment

## Phase 6: Visual and Format Analysis

### Image Ad Patterns
- Color schemes that dominate (bold vs muted, branded vs neutral)
- Text overlay amount (heavy text vs minimal text vs no text)
- Image subjects (people vs products vs abstract vs data/charts)
- Before/after comparisons
- Screenshot/UI imagery vs lifestyle photography

### Video Ad Patterns
- Average length by platform (Meta: 15-30s, LinkedIn: 30-60s)
- Opening frame patterns (face to camera, text hook, product shot)
- Pacing (quick cuts vs slow, talking head vs b-roll)
- Caption and subtitle usage
- End screen CTA patterns

### Carousel Patterns
- Number of cards (average, optimal)
- Story arc across cards (problem > solution > proof > CTA)
- Visual consistency vs variety per card
- Text density per card

### UGC Patterns
- Testimonial style (scripted vs authentic)
- Production quality (raw phone vs semi-polished)
- Creator demographics matching ICP
- Unboxing, review, tutorial, day-in-the-life formats

## Phase 7: Output

Return structured JSON:

```json
{
  "industry": "Shopify agencies / ecommerce services",
  "mined_at": "2024-01-15T14:30:00Z",
  "ads_analyzed": 65,
  "platforms_covered": ["Meta", "Google", "LinkedIn"],
  "hook_playbook": {
    "top_performing_hooks": [
      {
        "hook": "Your Shopify store is leaking revenue. Here's proof.",
        "type": "Pain point + curiosity",
        "emotional_trigger": "Fear of loss",
        "funnel_stage": "Awareness",
        "source": "competitor1.com Meta ad (running 45+ days)",
        "why_it_works": "Combines pain with a specific promise of evidence"
      }
    ],
    "hook_templates": [
      {
        "template": "[Audience], your [asset] is [negative verb] [consequence]. Here's [what to do about it].",
        "type": "Pain point",
        "examples": [
          "D2C founders, your store is losing 60% of visitors. Here's the fix.",
          "Ecommerce brands, your checkout flow is killing conversions. Here's proof."
        ]
      }
    ]
  },
  "emotional_trigger_map": {
    "most_used": "Fear of loss (38% of ads)",
    "most_effective": "Social proof + aspiration combo (longest-running ads)",
    "underused": "Curiosity hooks (only 12% of ads)"
  },
  "cta_playbook": {
    "top_ctas_by_stage": {
      "awareness": ["Learn How", "See the Framework"],
      "consideration": ["Get Your Free Audit", "Watch the Case Study"],
      "conversion": ["Book Your Call", "Start Your Project"]
    }
  },
  "offer_playbook": {
    "most_common": "Free audit / free consultation",
    "most_unique": "Pay-for-performance guarantee",
    "recommended_for_cold": "Free CRO scorecard (low friction, high perceived value)",
    "recommended_for_warm": "Free 15-min strategy call (medium commitment, high qualification)"
  },
  "creative_format_recommendations": {
    "meta": {
      "winning_format": "UGC testimonial video (15-30s)",
      "underused_opportunity": "Carousel walkthrough of audit process",
      "creative_specs": { "image": "1080x1080", "video": "1080x1350 (4:5)", "carousel": "1080x1080 per card" }
    },
    "google": {
      "winning_format": "RSA with specific numbers in headlines",
      "underused_opportunity": "Performance Max with video assets"
    },
    "linkedin": {
      "winning_format": "Document ads (carousel PDF)",
      "underused_opportunity": "Conversation ads for ABM"
    }
  },
  "angle_templates": [
    {
      "angle_name": "The Revenue Leak",
      "hook": "Your [channel] is leaking [metric]. We found [number] issues in [timeframe].",
      "body": "Case study proof + specific fixes found",
      "cta": "Get your free [audit type]",
      "format": "Single image with data visualization",
      "best_for": "Cold audience, awareness/consideration"
    }
  ],
  "swipe_file": [
    {
      "ad_source": "competitor1.com",
      "platform": "Meta",
      "format": "Video",
      "primary_text": "[Full ad copy]",
      "headline": "[Headline]",
      "cta": "Sign Up",
      "days_running": 45,
      "takeaway": "Pain point hook + specific number + free offer = proven formula"
    }
  ]
}
```

## Example Usage

Trigger phrases:
- "Mine winning ad angles for [industry]"
- "Ad creative playbook for [niche]"
- "Find the best ad hooks for [audience]"
- "Creative inspiration for [service] ads"
- "Build a swipe file for [industry] ads"

```
User: Mine winning ad angles for Shopify agency services
Assistant: [researches 50+ ads across Meta/Google/LinkedIn, extracts hooks, triggers, CTAs, offer frames, returns creative playbook with templates]
```

```
User: Best ad hooks for targeting D2C brand founders
Assistant: [analyzes ads targeting this audience, extracts top hooks by type, maps to emotional triggers, returns hook formula library]
```

```
User: Build a swipe file for ecommerce service ads
Assistant: [collects top-performing ads, categorizes by platform and format, annotates each with takeaways, returns organized swipe file]
```
