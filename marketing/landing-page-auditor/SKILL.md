---
name: landing-page-auditor
description: Audit ad-to-landing-page message match, conversion elements, and UX friction
tags: [landing-page, cro, message-match, conversion, ad-alignment]
---

# Landing Page Auditor

Audits the alignment between ad copy and its destination landing page by analyzing message match (headline alignment, offer consistency, CTA continuity), page conversion elements (above-fold content, social proof, form friction, trust signals), mobile experience, and page speed indicators. Scores overall ad-to-page alignment and page conversion readiness. Outputs specific fixes with priority rankings.

## Prerequisites

- Browser automation tool for visiting and analyzing the landing page
- WebSearch tool for competitive benchmarking
- Ad copy text (the ad driving traffic to this page)
- Landing page URL
- Optional: `agency.config.json` for client context

## Capabilities Used

1. `content-seo-optimizer` -- for on-page content optimization of the landing page
2. `schema-generator` -- for adding structured data to the landing page

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` for understanding the service being promoted.
3. Extract `case_studies[]` for identifying available social proof.
4. Extract `brand_voice` for tone consistency checks.
5. Check `tools.browser` and `tools.websearch` availability.
6. Accept parameters:
   - `landing_page_url` -- (required) the landing page URL to audit
   - `ad_copy` -- (required) the ad text driving traffic to this page. Object with fields: `headline`, `description`, `primary_text`, `cta`, `offer`
   - `ad_platform` -- (optional) `google` | `meta` | `linkedin` | `other`. Default: auto-detect from ad copy format
   - `traffic_type` -- (optional) `cold` | `warm` | `retargeting`. Default: `cold`
   - `goal` -- (optional) `lead_gen` | `purchase` | `signup` | `download` | `demo_booking`. Default: auto-detect

## Phase 1: Ad Copy Analysis

### Parse the Ad
Extract from the provided ad copy:
- **Primary promise**: What does the ad promise the user will get?
- **Primary keyword/topic**: What is the ad about?
- **Offer**: What specific offer is made? (free audit, discount, trial, download)
- **CTA**: What action was the user told to take?
- **Emotional trigger**: What emotion does the ad appeal to?
- **Audience signal**: Who is this ad speaking to?
- **Proof claims**: Any specific numbers, testimonials, or authority claims in the ad?

### Expectation Map
Build a list of what the user expects to find on the landing page based on the ad:
1. Headline matching the ad's primary promise
2. The same offer mentioned in the ad
3. The same CTA action (if ad says "Book a Demo", page should have a demo booking form)
4. Proof backing up any claims made in the ad
5. Content relevant to the topic/keyword
6. Consistent tone and visual style

## Phase 2: Landing Page Analysis

### Above-Fold Content (first screen, no scrolling)
Visit the landing page via browser automation. Assess:

**Headline**
- Is there a clear H1 headline?
- Does it match the ad's primary promise?
- Is it specific and benefit-driven (not vague)?
- Character length: short enough to read in 2 seconds?
- Score: 1-10 for message match with the ad

**Subheadline**
- Is there a supporting subheadline?
- Does it elaborate on the headline's promise?
- Does it address the audience directly?

**Hero Visual**
- Is there a relevant image, video, or illustration?
- Does it reinforce the message (not just decoration)?
- Is the visual professional and on-brand?
- Video: does it auto-play with captions?

**Primary CTA**
- Is there a visible CTA above the fold?
- Does the CTA text match the ad's CTA? (consistency)
- Is the CTA button visually prominent? (color contrast, size)
- Does the CTA communicate value? ("Get Your Free Audit" > "Submit")

**Overall Above-Fold Assessment**
- Can a user understand the offer within 5 seconds of landing?
- Is there a clear visual hierarchy: headline > subheadline > CTA?
- Is the above-fold section clean and uncluttered?

### Social Proof Elements
Scan the entire page for:
- **Testimonials**: customer quotes with names and photos
- **Client logos**: recognizable brand logos
- **Case study numbers**: specific metrics (e.g., "40% increase in conversions")
- **Reviews/ratings**: star ratings, review counts
- **Trust badges**: certifications, security badges, awards
- **Media mentions**: "As seen in" logos
- **User count**: "Trusted by X+ businesses"
- Count and quality-score each social proof element

### Form and Conversion Mechanism
If the page has a form:
- Number of fields (each field adds friction)
- Field types: name, email, phone, company, message, custom
- Is the form above the fold or below?
- Multi-step form or single form?
- Is there a privacy notice near the form?
- Form CTA button text: value-driven or generic?
- Auto-fill support for common fields

If the page uses a different conversion mechanism (Calendly, chat, phone):
- Is the mechanism easy to find?
- Is it mobile-friendly?
- Does it load quickly?

### Page Content Quality
Below-the-fold content assessment:
- Is the content structure logical? (problem > solution > proof > CTA)
- Are benefits clearly stated (not just features)?
- Is there a FAQ section addressing common objections?
- Are there multiple CTAs throughout the page (not just one)?
- Is the content length appropriate for the offer (not too thin, not overwhelming)?
- Is the reading level appropriate for the audience?

### Objection Handling
Check if the page addresses common buyer objections:
- "How much does it cost?" -- pricing transparency or "free" messaging
- "Will this work for me?" -- case studies or testimonials from similar businesses
- "What if I don't like it?" -- guarantee, refund policy, risk reversal
- "Why should I trust you?" -- credentials, experience, social proof
- "What happens next?" -- clear next steps after conversion

## Phase 3: Mobile Experience Audit

### Mobile Layout
Visit the page on a mobile viewport:
- Does the layout adapt properly? (no horizontal scroll)
- Is the text readable without zooming? (min 16px body text)
- Are touch targets large enough? (min 44x44px for buttons)
- Is the mobile menu functional?
- Does the hero image/video resize appropriately?

### Mobile Form Experience
- Are form fields large enough to tap easily?
- Does the keyboard type match the field? (numeric for phone, email for email)
- Is the form easily accessible on mobile? (not buried below fold)
- Does the submit button stay visible while filling the form?

### Mobile Speed Indicators
- Does the page load within 3 seconds on mobile? (subjective assessment)
- Are images lazy-loaded?
- Is there visible layout shift during load?
- Are heavy animations disabled on mobile?

## Phase 4: Message Match Scoring

Score each dimension of message match from 1-10:

| Dimension | Description | Score |
|-----------|-------------|-------|
| Headline Match | Landing page headline mirrors ad promise | ?/10 |
| Offer Match | The exact offer from the ad is prominent on page | ?/10 |
| CTA Match | Landing page CTA matches ad CTA action | ?/10 |
| Tone Match | Page tone matches ad tone (professional, casual, urgent) | ?/10 |
| Visual Match | Page visual style matches ad creative style | ?/10 |
| Proof Match | Claims made in ad are backed up on page | ?/10 |
| Audience Match | Page speaks to the same audience as the ad | ?/10 |

**Overall Message Match Score**: weighted average

Scoring guide:
- 9-10: Seamless transition from ad to page, user never feels confused
- 7-8: Minor gaps but overall consistent experience
- 5-6: Noticeable disconnects, some users will bounce
- 3-4: Significant mismatch, high bounce rate expected
- 1-2: Almost no connection between ad and page

## Phase 5: Conversion Readiness Scoring

Score the page's conversion elements from 1-10:

| Element | Weight | Score |
|---------|--------|-------|
| Above-fold clarity | 20% | ?/10 |
| CTA prominence | 15% | ?/10 |
| Social proof | 15% | ?/10 |
| Form friction | 15% | ?/10 |
| Mobile experience | 15% | ?/10 |
| Objection handling | 10% | ?/10 |
| Page speed | 10% | ?/10 |

**Overall Conversion Readiness Score**: weighted average

## Phase 6: Output

Return structured JSON:

```json
{
  "landing_page_url": "https://example.com/free-audit",
  "ad_platform": "Meta",
  "audited_at": "2024-01-15T14:30:00Z",
  "traffic_type": "cold",
  "message_match_score": "6.5/10",
  "conversion_readiness_score": "5.8/10",
  "overall_score": "6.1/10",
  "message_match_breakdown": {
    "headline_match": { "score": 5, "ad_headline": "Free Shopify Store Audit", "page_headline": "We Build Great Shopify Stores", "issue": "Page headline does not mention the free audit offer from the ad", "fix": "Change H1 to 'Get Your Free Shopify Store Audit'" },
    "offer_match": { "score": 7, "issue": "Offer mentioned but not prominent enough above fold", "fix": "Move audit offer details above the fold" },
    "cta_match": { "score": 8, "ad_cta": "Sign Up", "page_cta": "Get Your Free Audit", "note": "Page CTA is actually better than ad CTA -- consider updating the ad" },
    "tone_match": { "score": 7, "note": "Generally consistent, page slightly more formal than ad" },
    "visual_match": { "score": 6, "issue": "Ad uses warm colors, page uses cool tones", "fix": "Align page color palette with ad creative" },
    "proof_match": { "score": 4, "issue": "Ad claims '100+ brands served' but page shows no client count or logos", "fix": "Add client logos section and '100+ brands' counter above fold" },
    "audience_match": { "score": 8, "note": "Page clearly speaks to D2C brand founders" }
  },
  "conversion_readiness_breakdown": {
    "above_fold_clarity": { "score": 5, "issues": ["Headline too vague", "No subheadline", "CTA below fold on mobile"] },
    "cta_prominence": { "score": 6, "issues": ["Only 1 CTA on the entire page", "Button color doesn't contrast enough"] },
    "social_proof": { "score": 4, "issues": ["No testimonials", "No client logos", "No specific result numbers"] },
    "form_friction": { "score": 7, "notes": ["4 fields (name, email, URL, message)", "Could reduce to 3 by removing message field"] },
    "mobile_experience": { "score": 6, "issues": ["Form fields slightly small on mobile", "Hero image overlaps text on smaller screens"] },
    "objection_handling": { "score": 5, "missing_objections": ["No pricing context", "No 'what happens next' section", "No guarantee/risk reversal"] },
    "page_speed": { "score": 7, "notes": ["Loads in ~2.5 seconds", "Some render-blocking CSS"] }
  },
  "priority_fixes": [
    {
      "priority": "Critical",
      "issue": "Headline does not match ad promise",
      "fix": "Rewrite H1 to mirror the ad offer: 'Get Your Free Shopify Store Audit'",
      "impact": "Reducing bounce rate by aligning expectations",
      "effort": "15 minutes"
    },
    {
      "priority": "High",
      "issue": "No social proof above fold",
      "fix": "Add client logos bar and one testimonial above the fold",
      "impact": "Increases trust for cold traffic",
      "effort": "1 hour"
    },
    {
      "priority": "High",
      "issue": "Only one CTA on page",
      "fix": "Add CTA after social proof section and in page footer",
      "impact": "Captures users who scroll past the initial CTA",
      "effort": "30 minutes"
    },
    {
      "priority": "Medium",
      "issue": "No objection handling",
      "fix": "Add FAQ section addressing cost, timeline, and what's included",
      "impact": "Reduces hesitation for users considering the form",
      "effort": "2 hours"
    }
  ],
  "strengths": [
    "CTA button text is value-driven ('Get Your Free Audit')",
    "Form is relatively short (4 fields)",
    "Page clearly identifies the target audience"
  ],
  "competitor_benchmark": {
    "note": "Top competitor landing pages for similar offers average 7.5/10 message match",
    "gaps": ["Competitors use video testimonials", "Competitors show specific audit examples"]
  }
}
```

## Phase 7: Review Gate

Present findings to the user. The user may:
- Request specific fix implementations
- Ask for A/B test suggestions
- Request competitor landing page comparisons
- Ask for help rewriting specific sections

## Example Usage

Trigger phrases:
- "Audit my landing page against this ad"
- "Check message match: [ad copy] -> [landing page URL]"
- "Landing page review for [URL]"
- "Why is my landing page not converting?"
- "Ad-to-page alignment check for [campaign]"

```
User: Audit plasho.com/free-audit against this Meta ad: "Your Shopify store is leaking revenue. Book a free CRO audit today."
Assistant: [visits landing page, analyzes message match against ad copy, scores all elements, returns prioritized fix list]
```

```
User: Why is my Google Ads landing page not converting? URL: example.com/services
Assistant: [analyzes page conversion elements, identifies friction points, checks mobile experience, returns diagnosis with fixes]
```

```
User: Check if my landing page matches my LinkedIn ad campaign
Assistant: [compares ad copy elements against landing page content, scores alignment, identifies gaps, returns specific recommendations]
```
