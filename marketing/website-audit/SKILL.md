---
name: website-audit
description: Full website audit for ICP alignment, messaging clarity, conversion optimization, and trust signals
tags: [website, audit, icp-alignment, conversion, messaging, ux, trust-signals]
---

# Website Audit

Performs a comprehensive website audit measuring alignment to your ICP. Evaluates homepage messaging, navigation clarity, service page completeness, social proof placement, CTA hierarchy, mobile experience, trust signals, and lead capture mechanisms. Scores the site on ICP alignment and outputs a prioritized list of fixes with expected conversion impact.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and `case_studies` sections
- Target website URL
- WebFetch tool available (for page content extraction)
- Browser automation (Claude-in-Chrome MCP) for visual assessment and mobile testing
- Optional: `visual-brand` skill for detailed brand system analysis
- Optional: `cro-auditor` skill for deeper conversion rate analysis
- Optional: `seo-auditor` skill for technical SEO layer

## Capabilities Used

1. `visual-brand` -- for extracting and evaluating the site's visual system (colors, typography, spacing)
2. `cro-auditor` -- for deeper conversion rate optimization analysis on product/service pages
3. `seo-auditor` -- for technical SEO evaluation (page speed, meta tags, structured data)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[].name`, `services[].keywords` -- what the site should communicate
   - `icp.segments[].titles`, `icp.segments[].industries` -- who the site should speak to
   - `icp.segments[].description` -- pain points and motivations to address
   - `icp.primary_keywords` -- terms that should appear naturally on the site
   - `case_studies[]` -- social proof that should be visible
   - `agency.tagline` -- core value proposition reference
3. Accept parameters:
   - `website_url` -- URL to audit (required)
   - `audit_depth` -- `quick | standard | deep` (default: standard)
   - `focus_areas` -- specific areas to emphasize: `messaging | navigation | cro | trust | mobile | seo | all` (default: all)
   - `competitor_urls` -- competitor sites for comparison (optional)
   - `page_limit` -- max pages to audit (default: 10 for standard, 5 for quick, 20 for deep)

## Phase 1: Page Inventory

### Crawl site structure:
Using WebFetch, visit the homepage and extract:
- All navigation links (primary nav, footer nav, sidebar nav)
- Key page URLs: homepage, about, services/products, pricing, contact, blog, case studies, portfolio
- Sitemap if available (check /sitemap.xml)

### Build page audit list:
Prioritize pages by ICP relevance:
1. Homepage (always audit)
2. Service/product pages matching `services[].name`
3. Case study or portfolio pages
4. About/team page
5. Contact/demo/pricing page
6. Blog landing page
7. Any pages with lead capture forms

### For each page, capture basic data:
```json
{
  "url": "Page URL",
  "page_type": "homepage | service | case_study | about | contact | pricing | blog | other",
  "title_tag": "Page title",
  "meta_description": "Meta description",
  "h1": "Main heading",
  "word_count": "Approximate word count",
  "has_form": true,
  "has_cta": true,
  "load_time": "Estimated (fast/medium/slow)"
}
```

## Phase 2: Homepage Audit

The homepage is the highest-leverage page. Audit thoroughly:

### Above-the-fold assessment:
- **Headline clarity**: Does it explain what you do, for whom, and why in under 10 words?
- **Subheadline**: Does it expand on the headline with a benefit or proof point?
- **Hero CTA**: Is there a clear primary CTA? What does it say? Is the action obvious?
- **Visual hierarchy**: Does the eye follow headline -> subheadline -> CTA naturally?
- **ICP alignment**: Would the ICP segment (from config) immediately recognize this is for them?

### Scoring rubric for above-the-fold:
- Headline mentions ICP or their pain: +15
- Headline mentions outcome or benefit: +10
- Subheadline provides proof or specificity: +10
- Primary CTA is action-oriented (not "Learn More"): +10
- Visual design supports hierarchy (not cluttered): +5
- Total possible: 50

### Below-the-fold sections (audit each):
- **Social proof section**: Logos, testimonials, case study numbers
- **Service overview**: Clear service cards or descriptions
- **How it works**: Process transparency (builds trust)
- **Results/outcomes**: Specific metrics or before/after
- **FAQ**: Addresses common objections
- **Final CTA**: Repeats primary action at bottom

### Missing elements check:
Flag if any of these are absent:
- No social proof above the fold
- No clear service descriptions
- No case study or results section
- No trust signals (logos, certifications, testimonials)
- No secondary CTA options
- No lead magnet or value-first offer
- No urgency or scarcity signals (if appropriate)

## Phase 3: Service Page Audit

For each service page matching `services[].name`:

### Content completeness:
- **Service description**: Clear, benefit-oriented explanation
- **Who it's for**: Explicitly states target audience
- **What's included**: Scope, deliverables, or feature list
- **Process**: How engagement works (timeline, steps)
- **Pricing signals**: Price, starting-at, or "request quote" (some pricing context)
- **Social proof**: Relevant case study or testimonial for this specific service
- **CTA**: Service-specific call to action

### ICP keyword presence:
Check if `icp.primary_keywords` appear naturally on each service page. Flag missing keywords that should appear.

### Scoring per service page (0-100):
- Clear benefit headline: +15
- Target audience stated: +10
- Deliverables/scope listed: +15
- Process/timeline explained: +10
- Pricing context present: +10
- Relevant social proof: +15
- Strong CTA: +10
- ICP keywords present: +15

## Phase 4: Trust Signal Audit

### Trust signal inventory:
Check across all audited pages for:

**Client logos:**
- Present? Where? How many?
- Recognizable brands vs unknown?
- Relevance to ICP industries?

**Testimonials:**
- Named individuals with title and company?
- Photo included?
- Specific results mentioned?
- From ICP-matching companies?

**Case studies:**
- Detailed (problem, solution, results)?
- Quantified outcomes?
- Matching `case_studies[]` from config?

**Certifications and badges:**
- Shopify Partner badge?
- Industry certifications?
- Awards or press mentions?

**Team/about section:**
- Real team photos (not stock)?
- Founder story?
- Experience/credentials stated?

**Security and legal:**
- Privacy policy linked?
- Terms of service?
- SSL certificate (HTTPS)?

### Trust score calculation:
Each trust signal present and well-executed: +5-10 points
Each missing critical trust signal: -10 points
Max score: 100

## Phase 5: CTA and Lead Capture Audit

### CTA hierarchy assessment:
Map all CTAs found across the site:
```json
{
  "cta_text": "Book a Demo",
  "cta_type": "primary | secondary | tertiary",
  "page": "homepage",
  "location": "hero | nav | mid-page | footer | sticky | popup",
  "destination": "URL or action",
  "visual_weight": "HIGH | MEDIUM | LOW"
}
```

### CTA quality checks:
- Is there one clear primary CTA used consistently?
- Do CTA labels describe the outcome (not generic "Submit" or "Click Here")?
- Is the primary CTA visually distinct from secondary CTAs?
- Are CTAs placed at decision points (after proof, after explanation)?
- Is there a lower-commitment alternative for visitors not ready to buy?

### Lead capture mechanisms:
- Contact form (what fields? Too many = friction)
- Chatbot or live chat
- Newsletter signup
- Lead magnet (guide, audit, tool, template)
- Cal link (Calendly, Cal.com, etc.)
- Phone number visible
- Email visible

### Conversion path clarity:
Can a visitor who lands on the homepage take the desired action within 2 clicks? Map the shortest path and flag friction points.

## Phase 6: Mobile Experience Audit

### Mobile-specific checks:
- Responsive layout (no horizontal scrolling)
- Touch targets (buttons at least 44x44px)
- Text readability (16px+ body text)
- Navigation usable (hamburger menu works, not broken)
- Forms usable on mobile (proper input types, not tiny fields)
- CTA visible without scrolling on mobile
- Images properly sized (not causing layout shifts)
- Page speed on mobile (3G simulation)

### Mobile CTA assessment:
- Is the primary CTA easily tappable on mobile?
- Is there a sticky CTA on mobile for long pages?
- Does the mobile nav include the primary CTA?
- Click-to-call enabled if phone number is shown?

## Phase 7: Navigation and Information Architecture

### Navigation clarity:
- Is the primary nav simple (5-7 items max)?
- Do nav labels match what visitors expect? (avoid jargon)
- Is the most important page (services/pricing) in the first 3 nav items?
- Does the nav include a CTA button?
- Is the footer nav comprehensive?
- Are there breadcrumbs on inner pages?

### Information architecture:
- Can a visitor find any service page within 2 clicks from homepage?
- Is there logical grouping of content?
- Are there orphan pages (no internal links pointing to them)?
- Is the blog integrated or feels separate from the main site?

## Phase 8: ICP Alignment Score

Calculate an overall ICP alignment score based on:

### Language alignment (0-25):
- Site uses language ICP segments would use: +15
- Pain points from `icp.segments[].description` are addressed: +10

### Audience clarity (0-25):
- Clear statement of who the service is for: +15
- ICP industries mentioned on the site: +10

### Proof relevance (0-25):
- Case studies from matching industries: +15
- Testimonials from ICP-matching titles: +10

### Conversion path clarity (0-25):
- Clear primary CTA matching ICP motivation: +15
- Multiple entry points for different readiness levels: +10

### ICP alignment tiers:
- **STRONG** (80-100): Site clearly speaks to and converts the ICP
- **MODERATE** (60-79): Partially aligned, specific improvements needed
- **WEAK** (40-59): Significant gaps in ICP targeting
- **MISALIGNED** (<40): Site does not speak to the ICP

## Phase 9: Output

Return structured audit report:

```json
{
  "website_audit": {
    "url": "https://example.com",
    "audit_date": "ISO date",
    "audit_depth": "standard",
    "pages_audited": 10,
    "scores": {
      "icp_alignment": 72,
      "icp_tier": "MODERATE",
      "homepage": 65,
      "service_pages_avg": 58,
      "trust_signals": 45,
      "cta_hierarchy": 70,
      "mobile_experience": 80,
      "navigation": 75,
      "overall": 66
    },
    "homepage_audit": {
      "headline": "Current headline text",
      "headline_score": 8,
      "subheadline": "Current subheadline",
      "primary_cta": "Book a Demo",
      "above_fold_score": 35,
      "sections_present": ["hero", "social_proof", "services", "cta"],
      "sections_missing": ["how_it_works", "faq", "results"]
    },
    "service_page_audits": [],
    "trust_signal_inventory": {
      "client_logos": { "present": true, "count": 5, "quality": "MEDIUM" },
      "testimonials": { "present": true, "count": 3, "quality": "LOW" },
      "case_studies": { "present": false },
      "certifications": { "present": true, "items": ["Shopify Partner"] }
    },
    "cta_map": [],
    "mobile_issues": [],
    "navigation_issues": [],
    "critical_fixes": [],
    "quick_wins": [],
    "strategic_improvements": []
  }
}
```

### Prioritized recommendations:
Categorize all findings into three tiers:

**Critical fixes (do this week):**
- Issues that directly prevent conversion
- Missing trust signals that create doubt
- Broken functionality

**Quick wins (do this month):**
- Copy improvements with high impact
- CTA optimizations
- Missing sections that are easy to add

**Strategic improvements (next quarter):**
- Major redesign recommendations
- New page creation
- Content strategy shifts

Present formatted summary:

```
WEBSITE AUDIT REPORT -- {url}
Audited: {date} | Pages: {N} | Depth: {depth}

SCORES:
ICP Alignment:     {score}/100 -- {tier}
Homepage:          {score}/100
Service Pages:     {score}/100
Trust Signals:     {score}/100
CTA & Conversion:  {score}/100
Mobile:            {score}/100
Navigation:        {score}/100
OVERALL:           {score}/100

HEADLINE ASSESSMENT:
Current: "{headline}"
Issue: {what's wrong}
Suggested: "{improved headline}"

CRITICAL FIXES ({count}):
1. [{area}] {issue} -- Impact: {HIGH/MEDIUM}
   Fix: {specific recommendation}

QUICK WINS ({count}):
1. [{area}] {issue}
   Fix: {specific recommendation}

STRATEGIC IMPROVEMENTS ({count}):
1. [{area}] {recommendation}
   Expected impact: {description}

MISSING TRUST SIGNALS:
- {signal}: {recommendation}

CTA RECOMMENDATIONS:
Primary CTA: "{current}" -> "{suggested}"
Placement: {current issues and fixes}

ICP ALIGNMENT GAPS:
- {gap}: {how to address}
```

## Example Usage

Trigger phrases:
- "Audit this website for ICP alignment"
- "Review our website's conversion optimization"
- "Full website audit for plasho.com"
- "Is our site speaking to our ICP?"
- "Audit this client's website"
- "What's wrong with our homepage?"

```
User: Audit plasho.com for ICP alignment and conversion
Assistant: [reads config, crawls site structure, audits homepage above-fold and sections, evaluates service pages, inventories trust signals, maps CTAs, checks mobile, scores ICP alignment, outputs prioritized fix list]
```

```
User: Quick audit of a prospect's website: [URL]
Assistant: [same flow at quick depth (5 pages), focuses on homepage and primary service page, outputs key findings and opportunities to discuss in sales conversation]
```
