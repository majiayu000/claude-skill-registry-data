---
name: agency-audit
description: Audit any company website and generate a pitch-ready report for agencies. Extracts real problems, competitor comparison, quick wins, and a structured service proposal. No API keys required.
---

# Agency Audit

Audit a prospect or client website end-to-end and produce a structured report an agency can use to pitch services, prioritize work, or justify recommendations.

## What this does

Six phases, each producing structured output:

1. **Web Inspection** - Extract tech stack, SEO basics, copy quality, CTAs, trust signals, performance hints
2. **Competitor Comparison** - Find 3-5 competitors, compare positioning, identify gaps
3. **Problem Map** - Rank problems by severity and impact (quick win vs. strategic)
4. **Opportunity Map** - Map problems to specific services an agency can offer
5. **Deal Strategy** - Opportunity Score, close probability, entry door service, revenue projection
6. **Proposal Draft** - Generate a pitch-ready document with problems, services, and next steps

## How to use

Pass a URL. Optionally include:
- Agency name (for branded proposal)
- Services the agency offers (to match opportunities)
- Industry context (if not obvious from the site)

Example:
```
/agency-audit https://empresa.com
```

Or with context:
```
/agency-audit https://empresa.com - somos una agencia de performance, ofrecemos SEO, Ads y diseño web
```

## Phase 1 - Web Inspection

**Goal:** Extract everything visible and structural from the website without needing server access.

```python
from scripts.web_inspector import inspect_website

data = inspect_website(url)
# Returns: tech_stack, seo_basics, copy_analysis, cta_analysis,
#          trust_signals, performance_hints, mobile_hints, social_presence
```

**What to extract and evaluate:**

### First impression (3-second test)
- Is the headline clear? Does it say who this is for and what they do?
- Is there a visible CTA above the fold?
- Does the value proposition pass the "so what?" test?

Grading:
- Clear + CTA visible: Pass
- Vague headline or buried CTA: Needs work
- No clear value prop: Critical problem

### SEO basics
Extract and evaluate:
- Title tag: present? includes brand + keyword? under 60 chars?
- Meta description: present? under 160 chars? has CTA?
- H1: present? single? matches page intent?
- H2s: logical structure?
- Image alt tags: present on main images?
- URL structure: clean or messy parameters?
- Robots.txt: accessible?
- Sitemap: linked or guessable at /sitemap.xml?

### Copy and messaging
- Does the homepage use pain-first or feature-first language?
- Are there social proof elements? (testimonials, logos, numbers)
- Is there a clear offer or is it vague ("we do marketing")?
- Are CTAs action-oriented ("Get a free audit") or passive ("Learn more")?
- Is pricing visible or hidden?

### Technical signals
- CMS/platform detected (WordPress, Webflow, Shopify, Wix, custom)
- Analytics detected? (GA4, GTM, Meta Pixel, other)
- Chat widget present?
- Cookie banner? (GDPR signal)
- HTTPS? (basic trust check)
- www redirect consistent?

### Performance hints (from HTML, no Lighthouse needed)
- Are images using modern formats (webp)?
- Are images lazy-loaded (loading="lazy")?
- Are render-blocking scripts in head?
- Is the page unusually heavy (many external scripts)?

Output format:
```
## Web Inspection

URL: [url]
Platform: [detected CMS/platform]

### First Impression
Score: [Pass / Needs Work / Critical]
Headline: "[extracted headline]"
Value prop clarity: [Pass / Fail]
Above-fold CTA: [visible / buried / missing]

### SEO Basics
Title tag: [present/missing] - "[content]"
Meta description: [present/missing]
H1: [present/missing/multiple] - "[content]"
Alt tags: [present / partial / missing]
Sitemap: [found / not found]

### Copy Quality
Pain-first language: [Yes / No]
Social proof: [Yes - describe / No]
CTA quality: [active / passive / missing]
Pricing visible: [Yes / No]

### Tech Stack
Platform: [WordPress / Webflow / Wix / Shopify / Custom / Unknown]
Analytics: [GA4 / GTM / Meta Pixel / None detected]
Chat: [detected tool or None]

### Performance Hints
Image format: [modern / legacy]
Lazy loading: [Yes / No]
Heavy scripts: [Yes / No]
```

## Phase 2 - Competitor Comparison

**Goal:** Find who competes with this company and how they compare.

```python
from scripts.competitor_finder import find_competitors, compare_positioning

competitors = find_competitors(company_name, industry, url)
comparison = compare_positioning(url, competitors[:3])
```

Find 3-5 competitors using:
- Search: "[company] alternatives", "[industry] [location] [service]"
- Industry-specific directories if applicable
- Their own "vs" pages if they exist

For each competitor, extract:
- Headline / value proposition
- Key services offered
- Social proof signals (client logos, testimonials, numbers)
- CTA approach
- Pricing transparency

**Comparison output:**
```
## Competitor Comparison

| Signal | [Company] | [Comp A] | [Comp B] | [Comp C] |
|--------|-----------|----------|----------|----------|
| Clear headline | [Y/N] | [Y/N] | [Y/N] | [Y/N] |
| Social proof | [Y/N] | [Y/N] | [Y/N] | [Y/N] |
| Pricing visible | [Y/N] | [Y/N] | [Y/N] | [Y/N] |
| Case studies | [Y/N] | [Y/N] | [Y/N] | [Y/N] |
| CTA quality | [A/P] | [A/P] | [A/P] | [A/P] |

Positioning gaps:
- [what competitors have that this company lacks]
- [what this company does better than competitors]
```

## Phase 3 - Problem Map

**Goal:** Turn raw findings into a prioritized list of real problems.

Use `references/audit-framework.md` for severity criteria.

For each problem found:
- Assign severity: Critical / Important / Quick Win / Minor
- Estimate impact: High / Medium / Low (on conversions, SEO, trust)
- Estimate effort to fix: Hours / Days / Weeks

Do not list every minor issue. Focus on the 5-8 problems that matter most.

```
## Problem Map

### Critical (fix first)
P1: [problem]
Impact: [what this is costing them]
Evidence: [what you found - exact text, screenshot description, or metric]

P2: [problem]
Impact: [...]
Evidence: [...]

### Important (fix soon)
P3: [problem]
[...]

### Quick Wins (low effort, visible result)
P4: [problem] - [what to change, takes < 1 day]
P5: [problem] - [what to change, takes < 1 day]
P6: [problem] - [what to change, takes < 1 day]
```

## Phase 4 - Opportunity Map

**Goal:** Connect problems to specific agency services.

Use `references/service-mapping.md` to map each problem to a service category.

This is not about what the company needs in theory. It is about what an agency can sell and deliver.

```
## Opportunity Map

| Problem | Service | Priority | Estimated value |
|---------|---------|----------|----------------|
| No Google Analytics | Analytics Setup | High | [estimate range] |
| Weak copy + no CTA | Copywriting / CRO | High | [estimate range] |
| 0 blog content | SEO Content | Medium | [estimate range] |
| No Meta Pixel | Paid Ads Setup | Medium | [estimate range] |
| No case studies | Content Strategy | Low | [estimate range] |
```

If the agency provided their service list, match only to those services.

Also flag: "Services this company needs but are outside typical agency scope" - so the agency knows what to refer out.

## Phase 5 - Deal Strategy

**Goal:** Turn the audit into a sales decision. Not what the company needs - what the agency should sell, in what order, at what price, and whether this prospect is worth pursuing.

This phase runs after the Opportunity Map and before the Proposal Draft. It answers three questions the agency has but the proposal cannot ask out loud:

1. Is this prospect worth our time?
2. What is the fastest path to a signed contract?
3. What is the realistic revenue over 12 months?

### Opportunity Score

Score the prospect 0-100 based on signals collected. This is not the quality of their website - it is the quality of the sales opportunity.

Scoring factors:

| Signal | Points |
|--------|--------|
| Running paid ads with no conversion tracking | +20 (money leaving without measurement = urgent) |
| Has blog/content activity but no analytics | +15 (already investing, wants to know ROI) |
| No Meta Pixel (plans or runs ads) | +15 (entry door, creates immediate dependency) |
| Wix/Squarespace on a growing B2B company | +10 (platform pain, redesign opportunity) |
| No case studies on service business | +10 (closing friction they feel) |
| Social inactive 3+ months | +8 (knows they should, guilt installed) |
| Outdated design (5+ years signals) | +8 (embarrassment pain) |
| No email capture | +5 (losing leads they paid for) |
| Already working with an agency (signals in tech stack) | -10 (switching cost, loyalty) |
| Wix free tier + no ads + solo operator | -15 (likely no budget) |
| No business signals (no phone, no address, no team) | -20 (may not be a real business) |

Score interpretation:
- 70-100: Strong opportunity, prioritize
- 40-69: Qualified, worth a conversation
- 20-39: Low priority, batch with others
- Under 20: Pass

### Close Probability

Based on the Opportunity Score and specific signals, estimate close probability:

**High probability signals:**
- Running ads without tracking (money problem, clear ROI story)
- Recent investment in website or content (they are in buying mode)
- Hired or posting for a marketing role (underserved internally)
- Competitors clearly outperform them online (competitive threat visible)

**Medium probability signals:**
- Problems exist but are not causing visible pain yet
- Wix/Squarespace frustration without a specific trigger
- Social inactive but no plans mentioned

**Low probability signals:**
- Already working with another agency
- No analytics and no ads = not measuring anything (may not value marketing)
- Very small operation (1 person, local only)

Output:
```
Close probability: [High / Medium / Low]
Reasoning: [one sentence - specific signal that drove the rating]
```

### Entry Door Service

The entry door is the first thing to sell - not the biggest opportunity, but the easiest yes.

Rules:
- Low cost (under 500€ or under 2 days work)
- Fast delivery (client sees result in under 1 week)
- Creates dependency (they need you to interpret or maintain it)
- Opens the door to the next service

Best entry doors by situation:

| Situation | Entry door | Why it opens the door |
|-----------|-----------|----------------------|
| No analytics | GA4 + GTM setup (200-400€) | They cannot read reports without you |
| No Meta Pixel | Pixel + events setup (200-300€) | Retargeting audiences start building day 1 |
| Broken tracking | Analytics audit + fix (300-500€) | Before they can run any campaign |
| Quick wins only | Homepage CTA + meta descriptions (200-300€) | Low risk, visible result fast |

```
Entry door: [service]
Price: [range]
Delivery: [X days]
Why it works: [one sentence - what dependency it creates]
```

### Revenue Projection

Estimate realistic revenue from this client over 12 months:

```
Month 1: [entry door service] - [price range]
Months 2-4: [next service] - [price range/month]
Months 5-12: [retainer potential] - [price range/month]

12-month projection: [low estimate] - [high estimate]
Annual contract value: [range]
```

Do not inflate projections. Base them on what the Opportunity Map shows. If the company only needs 2 services, say so.

### Deal Summary

```
Opportunity Score: [0-100]
Close probability: [High / Medium / Low]
Reasoning: [specific signal]

Entry door: [service] - [price]
Priority services: [1, 2, 3 in order]
Estimated ticket (project): [range]
Retainer potential: [range/month]
12-month value: [range]

Recommended approach:
[One sentence: how to open the conversation based on the strongest signal found]
```

## Phase 6 - Proposal Draft

**Goal:** Produce a document the agency can customize and send. Not a raw report - a pitch.

Use `references/proposal-structure.md` for the format.
Use `templates/audit-report.md` for the full output template.

The proposal must:
- Open with the company's situation (not the agency's credentials)
- List 3-4 specific problems found (with evidence, not opinions)
- Present 2-3 recommended services with clear outcomes
- End with a specific next step (call, audit delivery, proposal meeting)

**Tone rules:**
- Never say "your website is bad" - say "we found X issue that is likely costing you Y"
- Lead with their problem, not your service
- Be specific - "your H1 says 'Welcome' with no keyword" not "your SEO needs work"
- No agency jargon (no "KPIs", "deliverables", "synergies")

## Data sources

The audit runs on what is publicly visible:
- HTML/DOM of the website (Scrapling)
- Google Search results for competitor discovery (ddgs)
- Structured data (schema.org if present)
- Social media presence (public profiles, linked from site)

Does NOT require:
- Google Analytics access
- Server logs
- Backend access
- Any API keys

Optional enhancement if available:
- `PAGESPEED_API_KEY` - enables Core Web Vitals data from PageSpeed Insights API

## References

- `references/audit-framework.md` - severity criteria, what to check per dimension
- `references/proposal-structure.md` - proposal format, tone guide, section order
- `references/service-mapping.md` - problem to service mapping with value ranges
- `references/quick-wins.md` - 20 common quick wins with fix instructions

## Output principles

1. Lead with evidence - every problem must have a specific finding, not an opinion
2. Prioritize ruthlessly - 5 real problems beat a list of 30 minor issues
3. Translate to business impact - "missing meta description" means nothing; "search results show no description which reduces click-through rate" means something
4. Match services to what the agency actually does - do not pitch services they cannot deliver
5. Proposal tone is consultative, not salesy - they hired a consultant, not a vendor
6. Quick wins section is always present - agencies need something to show fast
7. Never invent problems - if the site is well-built in an area, say so
