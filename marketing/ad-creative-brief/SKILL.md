---
name: ad-creative-brief
description: Generate structured creative briefs for ad designers with brand-consistent direction
tags: [advertising, creative-brief, design, ads, marketing]
---

# Ad Creative Brief Generator

Produces structured creative briefs for ad designers across all formats: social ads (Meta, LinkedIn, Instagram), display ads, Google Ads, and video ads. Each brief includes objective, target audience, key message, tone, mandatory elements, format specifications, reference examples, and do's/don'ts. References `brand-voice` and `visual-brand` from config for brand consistency.

## Prerequisites

- `agency.config.json` in the project root
- Campaign objective and target audience from user
- Optional: `visual-brand` output for style constraints
- Optional: existing ad performance data for optimization context

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract `agency.name`, `agency.tagline`, `agency.domain` for branding.
3. Extract `outreach.tone` for voice direction.
4. Extract `icp.segments[]` for audience targeting context.
5. Extract `case_studies[]` for proof points available to reference.
6. Extract `services[]` for offer framing.
7. Collect inputs from the user:
   - **Campaign objective**: awareness, traffic, leads, conversions, retargeting
   - **Product/service**: what is being advertised
   - **Target audience**: segment, demographics, psychographics
   - **Platform(s)**: Meta, LinkedIn, Google Display, Instagram, YouTube
   - **Budget tier**: low (<$1K/mo), medium ($1K-5K), high ($5K+)
   - **Key offer**: discount, free trial, free audit, case study, webinar
   - **Competitor context**: who else is advertising to this audience
   - **Timeline**: when does the campaign launch

## Phase 1: Audience and Messaging Strategy

Define the creative strategy before generating the brief:

**Audience profile:**
```
TARGET AUDIENCE:
---
Segment: [from ICP or custom]
Job titles: [decision maker titles]
Pain points:
1. [Primary pain -- what keeps them up at night]
2. [Secondary pain -- what frustrates them daily]
3. [Aspirational gap -- where they want to be vs where they are]

Awareness level: [unaware / problem-aware / solution-aware / product-aware / most-aware]
```

**Message hierarchy:**
```
MESSAGE FRAMEWORK:
---
Primary message: [One sentence. The single thing they should remember.]
Supporting proof: [Data point, case study, or social proof that backs the primary message.]
CTA: [Specific action. "Book a free CRO audit" not "Learn more".]
Urgency driver: [Why now? Limited spots, seasonal, competitor pressure, or none.]
```

**Tone calibration:**
- Match `outreach.tone` from config
- Adjust for platform (LinkedIn: professional, Instagram: casual, Meta: direct)
- Adjust for awareness level (unaware: educate, aware: persuade, most-aware: convert)

## Phase 2: Format Specifications

For each requested platform, define creative specs:

**Meta Ads (Facebook/Instagram feed):**
```
FORMAT: Meta Feed Ad
Sizes: 1080x1080 (square), 1080x1350 (portrait), 1200x628 (landscape)
Text overlay: <20% of image area
Primary text: 125 chars (above fold), 250 max
Headline: 40 chars max
Description: 30 chars max
CTA button: [Shop Now / Learn More / Book Now / Sign Up / Get Offer]
```

**Instagram Stories/Reels:**
```
FORMAT: Instagram Stories
Size: 1080x1920 (9:16)
Duration: 5-15 seconds (static with motion), 15-60 seconds (video)
Safe zone: keep text within center 80%
Sound: optional but recommended for Reels
```

**LinkedIn Ads:**
```
FORMAT: LinkedIn Sponsored Content
Sizes: 1200x627 (single image), 1080x1080 (carousel card)
Introductory text: 150 chars (above fold), 600 max
Headline: 70 chars max
Description: 100 chars max (optional)
CTA button: [Learn More / Sign Up / Register / Download / Apply]
```

**Google Display:**
```
FORMAT: Google Display Network
Sizes: 300x250, 336x280, 728x90, 160x600, 320x50 (mobile)
Text limits: headline (30 chars), description (90 chars)
Logo: required, clear at small sizes
```

## Phase 3: Creative Brief Document

Generate the complete brief:

```
CREATIVE BRIEF
===
Campaign: [Campaign name]
Date: [Brief date]
Prepared by: [agency.name]

OBJECTIVE:
[What this campaign needs to achieve. One sentence. Measurable.]

TARGET AUDIENCE:
[Audience profile from Phase 1]

KEY MESSAGE:
[Primary message. What do we want them to think/feel/do?]

PROOF POINT:
[Case study result, data point, or testimonial to reference]

TONE & VOICE:
[2-3 adjectives. Example: "confident, helpful, no-BS"]

MANDATORY ELEMENTS:
- Logo placement: [position and size]
- Brand colors: [primary, secondary hex codes]
- Font: [heading and body fonts]
- URL/CTA: [specific URL or CTA text]
- Legal: [disclaimers, trademark symbols if needed]

FORMAT & SIZES:
[From Phase 2 -- all required sizes and specs]

VISUAL DIRECTION:
- Hero element: [product shot / lifestyle image / illustration / data visualization]
- Background: [solid color / gradient / image / pattern]
- Layout: [centered / asymmetric / grid / full-bleed image with text overlay]
- Motion: [static / subtle animation / video -- specify if animated]

COPY DIRECTION:
- Headline options:
  1. [Option A -- benefit-led]
  2. [Option B -- pain-led]
  3. [Option C -- proof-led]
- Body copy: [Key phrases or full copy if needed]
- CTA: [Button text]

REFERENCE EXAMPLES:
1. [Description of reference ad 1 -- what to take from it]
2. [Description of reference ad 2 -- what to take from it]

DO'S:
- [Specific instruction 1]
- [Specific instruction 2]
- [Specific instruction 3]

DON'TS:
- [Anti-pattern 1 -- e.g., "No stock photos of handshakes"]
- [Anti-pattern 2 -- e.g., "No more than 3 font sizes"]
- [Anti-pattern 3 -- e.g., "No blue CTA buttons (competitor color)"]

DELIVERABLES:
- [List every size/format needed with file format (PNG, JPG, MP4)]
- [Number of variations needed]
- [Deadline]
```

## Phase 4: Variation Strategy

Recommend A/B test variations:

```
A/B TEST PLAN:
---
Variable: [What changes between variations]

Version A: [Description -- e.g., "benefit headline + product image"]
Version B: [Description -- e.g., "pain headline + lifestyle image"]
Version C: [Description -- e.g., "social proof headline + data visual"]

Split: [Equal 33/33/33 or 50/50 for two variants]
Success metric: [CTR / CPA / conversion rate]
Minimum sample: [Impressions needed for significance]
```

## Phase 5: Output

Return the complete creative brief as structured JSON:

```json
{
  "creative_brief": {
    "campaign_name": "",
    "date": "",
    "objective": "",
    "target_audience": {
      "segment": "",
      "titles": [],
      "pain_points": [],
      "awareness_level": ""
    },
    "messaging": {
      "primary_message": "",
      "proof_point": "",
      "cta": "",
      "urgency": "",
      "headline_options": [],
      "body_copy": ""
    },
    "tone": "",
    "brand_elements": {
      "colors": {},
      "fonts": {},
      "logo_placement": "",
      "mandatory_url": ""
    },
    "formats": [
      {
        "platform": "",
        "size": "",
        "text_limits": {},
        "cta_button": ""
      }
    ],
    "visual_direction": {
      "hero_element": "",
      "background": "",
      "layout": "",
      "motion": ""
    },
    "references": [],
    "dos": [],
    "donts": [],
    "ab_test": {
      "variable": "",
      "versions": [],
      "success_metric": ""
    },
    "deliverables": [],
    "deadline": ""
  }
}
```

## Example Usage

**Trigger phrases:**
- "Create an ad brief for our Meta campaign"
- "I need a creative brief for LinkedIn ads targeting D2C founders"
- "Generate ad creative direction for the Kibi Sports case study"
- "Brief the designer for Instagram story ads"
- "Write a creative brief for Google Display retargeting"

```
User: Create a Meta ad brief to promote our CRO audit service
Assistant: [reads config, builds audience profile from ICP, generates complete brief with 3 headline options, visual direction, format specs, and A/B test plan]
```

```
User: I need LinkedIn ad creatives for US D2C brands
Assistant: [targets US/UK/AU segment, adjusts tone for LinkedIn, generates professional brief with sponsored content specs and carousel options]
```
