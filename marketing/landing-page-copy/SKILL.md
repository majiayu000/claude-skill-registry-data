---
name: landing-page-copy
description: Generate conversion-focused landing page copy section by section using proven frameworks
tags: [content, copywriting, landing-page, conversion, cro, marketing]
---

# Landing Page Copy

Generates conversion-optimized landing page copy organized into standard high-converting sections: hero, problem/solution, social proof, features/benefits, FAQ, and CTA. Uses frameworks like PAS, AIDA, and StoryBrand to structure messaging. Tailors copy to the target audience using ICP data from config. Outputs section-by-section copy ready for design implementation.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `services`, `case_studies`, `icp`, and `outreach` sections
- Page purpose and target audience
- Optional: specific service or offer the page promotes
- Optional: existing landing page URL (for competitive reference or rewrite)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for brand references
   - `agency.tagline` -- for messaging alignment
   - `agency.domain` -- for CTA links
   - `services[]` -- to align copy with specific offerings
   - `case_studies[]` -- for social proof sections
   - `icp.segments[]` -- to tailor language, pain points, and aspirations to the target audience
   - `outreach.tone` -- voice and style for all copy
   - `outreach.banned_phrases` -- phrases to avoid
3. Accept parameters:
   - `page_purpose` -- (required) what the page sells or promotes: `service`, `lead-magnet`, `consultation`, `webinar`, `product`, `case-study`, `pricing`
   - `offer` -- (required) the specific offer: "Free CRO audit", "Shopify store development", etc.
   - `target_audience` -- which ICP segment. Default: primary segment from config
   - `primary_cta` -- the main conversion action: `book-call`, `download`, `sign-up`, `get-quote`, `start-trial`
   - `framework` -- copy framework: `PAS`, `AIDA`, `StoryBrand`, `BAB`. Default: `PAS`
   - `sections` -- (optional) array of section types to include. Default: all standard sections
   - `competitor_url` -- (optional) competitor page to reference for positioning
   - `tone_override` -- (optional) override: `authoritative`, `friendly`, `urgent`, `aspirational`
   - `word_limit` -- (optional) max total words across all sections. Default: 1500-2500

## Phase 1: Audience and Messaging Foundation

Before writing any copy, build the messaging foundation:

**Audience profile (from ICP config):**
- Primary pain points (3-5 specific problems they face)
- Aspirations (what success looks like for them)
- Current alternatives (what they are doing now instead)
- Objections (top 3-5 reasons they would NOT buy)
- Language patterns (words and phrases this audience uses)
- Decision criteria (what matters most: price, speed, quality, trust)

**Positioning statement:**
```
For [target audience] who [pain point],
[agency/service] is the [category] that [key differentiator],
unlike [alternatives] which [limitation of alternatives].
```

**Value proposition hierarchy:**
1. Primary benefit (the #1 reason to convert)
2. Supporting benefits (3-4 additional reasons)
3. Proof points (data, testimonials, case studies that validate each benefit)

**Framework application:**

| Framework | Section Flow |
|-----------|-------------|
| PAS | Problem -> Agitation -> Solution -> Proof -> CTA |
| AIDA | Attention -> Interest -> Desire -> Action |
| StoryBrand | Character -> Problem -> Guide -> Plan -> Action -> Success -> Failure |
| BAB | Before -> After -> Bridge -> Proof -> CTA |

Compile:
```
MESSAGING FOUNDATION:
---
Audience: [segment name]
Primary pain: [the #1 problem]
Primary benefit: [the #1 reason to convert]
Positioning: [one-sentence positioning statement]
Framework: [selected framework]
CTA: [primary conversion action]
```

## Phase 2: Hero Section

The hero section is the highest-impact area of the page. It must communicate what you do, who it is for, and why they should care -- in under 5 seconds.

**Hero components:**

| Component | Length | Rules |
|-----------|--------|-------|
| Headline | 6-12 words | Benefit-first or pain-first. No clever wordplay. Must be instantly clear. |
| Subheadline | 15-25 words | Expand on the headline. Add specificity: who, what result, how. |
| Primary CTA | 2-5 words | Action verb + benefit: "Book Your Free Audit", "Get Your Growth Plan" |
| Secondary CTA | 2-5 words | Lower commitment: "See Our Work", "Watch Demo" |
| Trust indicators | N/A | Client logos, "trusted by X brands", star rating, or certification badges |

**Headline formulas (generate 3 variants):**

1. **Benefit headline**: "[Desired outcome] for [audience]"
   - "Higher Conversions for D2C Shopify Brands"
2. **Pain headline**: "Stop [pain point]. Start [desired outcome]."
   - "Stop Losing Revenue to a Bad Product Page."
3. **Proof headline**: "[Result] for [client]. We Will Do the Same for You."
   - "34% More Conversions for Kibi Sports. You Are Next."

Generate all three. Recommend one based on framework alignment.

## Phase 3: Problem/Solution Section

Establish the gap between where the reader is and where they want to be.

**Problem block (150-200 words):**
- Name 3-4 specific symptoms the audience recognizes ("Your product pages have high traffic but low add-to-cart rates")
- Use their language, not industry jargon
- Agitate: what happens if they do not fix it (revenue loss, competitor advantage, wasted ad spend)
- Do NOT mention your service yet

**Solution block (100-150 words):**
- Introduce your approach as the bridge
- Focus on the methodology or approach, not features
- Connect each pain point to a specific part of your solution
- Use "you" language, not "we" language

**Transition to proof**: end with a line that leads into social proof ("Don't take our word for it" or "Here is what happened when [client] made the switch")

## Phase 4: Social Proof Section

Build trust through evidence. This section converts skeptics.

**Components (include at least 3):**

1. **Case study spotlight (100-150 words):**
   - Client name and context (from `case_studies[]` in config)
   - The problem they had (specific, relatable)
   - What you did (brief, 1-2 sentences)
   - The result (specific numbers: percentages, revenue, time saved)
   - Format: before/after or problem/solution/result

2. **Testimonial quotes (2-3):**
   - Direct quote format with attribution (name, title, company)
   - If no real testimonials available, note "[placeholder -- insert real testimonial]"
   - Each testimonial should address a different objection

3. **Trust metrics:**
   - Number of clients served
   - Years of experience
   - Industry-specific credentials
   - Platform partnerships (Shopify Partner, etc.)

4. **Logo bar:**
   - "[Insert client logos here]" placeholder
   - "Trusted by X+ brands" tagline

## Phase 5: Features/Benefits Section

Translate service features into audience benefits. Never list features without connecting them to outcomes.

**Structure: 4-6 benefit blocks, each containing:**

| Component | Length | Example |
|-----------|--------|---------|
| Benefit headline | 4-8 words | "Product Pages That Actually Convert" |
| Benefit description | 25-40 words | Explain how this benefit solves their specific problem |
| Proof point | 10-20 words | Data point or mini case study that validates the claim |

**Rules:**
- Lead with the benefit, not the feature ("Faster page load" not "CDN optimization")
- Each benefit block addresses a different pain point from the audience profile
- Use concrete specifics: "15-25% revenue uplift" not "better performance"
- Include at least one benefit that addresses the #1 objection
- Order by importance: strongest benefit first, weakest last

**Anti-feature dump rule**: if a section reads like a feature list, rewrite it as outcome-focused copy.

## Phase 6: How It Works / Process Section

Reduce anxiety by making the engagement process clear and simple.

**Structure: 3-5 steps**

| Step | Name | Description (15-25 words) |
|------|------|---------------------------|
| 1 | Discovery | What happens first (book a call, submit info, etc.) |
| 2 | Analysis | What you do with their input (audit, research, strategy) |
| 3 | Execution | How you deliver the work |
| 4 | Results | What they get and when |
| (5) | Ongoing | Optional: ongoing support or optimization |

**Rules:**
- Max 5 steps -- more than that feels heavy
- Each step has a clear, jargon-free name
- Include timeline hints ("Within 48 hours", "Week 1-2")
- The first step must be low-commitment ("Book a free call" not "Sign the contract")

## Phase 7: FAQ Section

Address objections disguised as questions. Every FAQ answer is a miniature sales argument.

**Generate 6-8 FAQs using this framework:**

| Objection Type | Question Pattern |
|----------------|-----------------|
| Price | "How much does this cost?" / "What is included?" |
| Time | "How long does it take?" / "When will I see results?" |
| Trust | "Have you worked with brands like mine?" / "What if it does not work?" |
| Process | "What do you need from me?" / "How involved do I need to be?" |
| Comparison | "How is this different from [alternative]?" / "Why not hire in-house?" |
| Technical | Service-specific technical questions |

**FAQ answer rules:**
- Max 75 words per answer
- Start by validating the question (do not dismiss concerns)
- Answer directly, then support with proof or specifics
- End each answer by subtly reinforcing a benefit
- Include at least one FAQ that re-states the primary CTA

## Phase 8: Final CTA Section

The closing CTA section must create urgency and remove remaining friction.

**Components:**

| Component | Length | Rules |
|-----------|--------|-------|
| CTA headline | 6-12 words | Restate the primary benefit as an invitation |
| CTA subtext | 15-30 words | Address the #1 remaining objection. Add urgency if genuine. |
| CTA button | 2-5 words | Same as hero CTA for consistency |
| Risk reversal | 10-20 words | "Free consultation", "No commitment", "Cancel anytime" |
| Scarcity | 10-15 words | Only if genuine: "Limited to 3 new clients per month" |

**CTA formulas:**
- "Ready to [desired outcome]? [Action]."
- "[Desired outcome] starts with a conversation."
- "Your competitors are not waiting. [Action] today."

## Phase 9: SEO Metadata

Generate page-level SEO elements:

| Element | Length | Rules |
|---------|--------|-------|
| Title tag | 50-60 chars | Primary keyword + benefit + brand |
| Meta description | 150-160 chars | CTA-oriented summary with primary keyword |
| H1 | Same as hero headline | One per page, contains primary keyword |
| H2s | Section subheadings | Include secondary keywords where natural |
| URL slug | 3-5 words | Lowercase, hyphenated, keyword-rich |
| Primary keyword | 1-3 words | The main search term this page targets |
| Secondary keywords | 3-5 phrases | Related terms to weave into body copy |

## Phase 10: Output

Return structured JSON:

```json
{
  "page_metadata": {
    "purpose": "service",
    "offer": "CRO audit and optimization for Shopify stores",
    "audience": "India D2C",
    "framework": "PAS",
    "total_word_count": 1850,
    "estimated_read_time": "7 min"
  },
  "seo": {
    "title_tag": "Shopify CRO Audit for D2C Brands | Agency Name",
    "meta_description": "Stop losing revenue to poor product pages. Get a free CRO audit for your Shopify store. Proven results with D2C brands.",
    "h1": "Higher Conversions for D2C Shopify Brands",
    "url_slug": "shopify-cro-audit",
    "primary_keyword": "Shopify CRO audit",
    "secondary_keywords": ["ecommerce conversion optimization", "D2C shopify expert", "product page optimization"]
  },
  "messaging_foundation": {
    "positioning": "For D2C brands losing revenue to poor Shopify UX, we are the CRO specialists who find and fix conversion leaks, unlike generic agencies who redesign without data.",
    "primary_pain": "High traffic but low conversion rates",
    "primary_benefit": "Measurable revenue uplift from data-driven CRO"
  },
  "sections": {
    "hero": {
      "headline_variants": [
        {"type": "benefit", "text": "Higher Conversions for D2C Shopify Brands"},
        {"type": "pain", "text": "Stop Losing Revenue to a Bad Product Page"},
        {"type": "proof", "text": "34% More Conversions for Kibi Sports. You Are Next."}
      ],
      "recommended_headline": 0,
      "subheadline": "We audit, redesign, and optimize your Shopify store to turn browsers into buyers. Data-driven CRO for D2C brands.",
      "primary_cta": "Book Your Free Audit",
      "secondary_cta": "See Our Results",
      "trust_indicators": ["Shopify Partner", "X+ brands served", "[client logos]"]
    },
    "problem_solution": {
      "problem": "Full problem block copy...",
      "solution": "Full solution block copy...",
      "transition": "Don't take our word for it."
    },
    "social_proof": {
      "case_study": {
        "client": "Kibi Sports",
        "problem": "...",
        "solution": "...",
        "result": "...",
        "word_count": 120
      },
      "testimonials": [
        {"quote": "...", "name": "...", "title": "...", "company": "..."}
      ],
      "trust_metrics": ["X clients", "Y years", "Z% average uplift"]
    },
    "features_benefits": [
      {"headline": "...", "description": "...", "proof_point": "..."}
    ],
    "how_it_works": [
      {"step": 1, "name": "Book a Call", "description": "...", "timeline": "Day 1"}
    ],
    "faq": [
      {"question": "How much does this cost?", "answer": "...", "objection_type": "price"}
    ],
    "final_cta": {
      "headline": "Ready to Stop Losing Revenue?",
      "subtext": "Book a free 30-minute CRO audit. No commitment, no pitch -- just actionable insights.",
      "cta_button": "Book Your Free Audit",
      "risk_reversal": "Free consultation. No commitment required.",
      "scarcity": null
    }
  },
  "quality_checks": {
    "tone_compliant": true,
    "banned_phrases_clear": true,
    "cta_consistent": true,
    "benefit_over_features": true,
    "objections_addressed": 5,
    "word_count_in_range": true
  }
}
```

## Phase 11: Review

Present the landing page copy to the user:

1. Show messaging foundation and positioning
2. Show hero section with all 3 headline variants
3. Walk through each section in order
4. Highlight FAQ answers that address key objections
5. Show SEO metadata
6. Ask for approval or revision requests

After approval, optionally:
- Export as a structured document for the designer/developer
- Hand off to `content-seo-optimizer` for keyword density and readability tuning
- Feed the hero copy into `carousel-creator` or `content-repurposer` for promotional assets

## Example Usage

Trigger phrases:
- "Write landing page copy for our CRO audit service"
- "Generate copy for a lead magnet landing page"
- "Create a service page for Shopify development"
- "Write a landing page targeting US D2C brands"
- "Draft conversion copy for our consultation booking page"
- "Rewrite our landing page using the StoryBrand framework"

```
User: Write landing page copy for our Shopify CRO audit service targeting D2C brands in India
Assistant: [reads config, builds messaging foundation, generates hero with 3 variants, writes all sections using PAS framework, includes Kibi Sports case study, generates FAQ addressing top objections, returns structured JSON]
```

```
User: Create a lead magnet landing page for a free Shopify CRO checklist
Assistant: [reads config, adapts messaging for lead magnet, writes shorter sections focused on download conversion, uses AIDA framework, returns structured JSON]
```
