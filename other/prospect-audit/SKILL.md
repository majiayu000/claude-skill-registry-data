---
name: prospect-audit
description: >
  Generate full prospect audit as a sales tool before demos. Combines
  company research, CRO audit, and person intel into a presentable
  document with talking points and opportunity sizing.
tags: [demo-prep, audit, sales-tool, playbook]
---

# Prospect Audit

Pre-demo sales preparation tool. Generates a comprehensive audit document for a specific prospect, combining company intelligence, CRO findings, and decision-maker research into a conversation-ready deliverable. Use this before every demo to walk in with authority.

## Prerequisites

- `agency.config.json` fully populated with case studies and service offerings
- Tool stack configured (Apollo for person research, web access for CRO audit)
- Company website must be live and accessible

## Composites & Capabilities Used

1. `company-researcher` -- deep company intelligence gathering
2. `cro-auditor` -- full store audit across all page types
3. `person-researcher` -- decision-maker background and activity
4. `decision-maker-finder` -- identify additional stakeholders

## Phase 0: Intake

Accept the following inputs:
- **Company name**: the prospect's business name
- **Website URL**: their primary website (Shopify store preferred)
- **Contact name**: the person the demo is scheduled with
- **Demo date**: when the demo is happening

Validate that the website is accessible before proceeding. If the site is down or behind a password wall, flag immediately and proceed with company research only.

## Phase 1: Company Deep Dive

Execute `company-researcher` with depth: "deep"

Gather:
- Business overview: what they sell, their positioning, target market
- Tech stack: Shopify plan, theme, apps installed, payment providers, analytics tools
- Social presence: Instagram followers, engagement rate, LinkedIn company page, Twitter/X
- Recent news: funding rounds, product launches, leadership changes, press mentions
- Growth signals: hiring activity, new market expansion, ad spend changes
- Competitive landscape: who are their direct competitors, how do they compare
- Reviews and reputation: Trustpilot, Google reviews, app store reviews if applicable

## Phase 2: CRO Audit

Execute `cro-auditor` with depth: "deep"

Audit the following areas:
- **Homepage**: hero, value proposition, trust signals, navigation, above-the-fold CTA
- **Product pages**: imagery, descriptions, variant selection, add-to-cart UX, social proof
- **Collection pages**: filtering, sorting, product card design, pagination
- **Mobile experience**: responsive behavior, thumb-zone CTA placement, load time
- **Cart and checkout**: cart drawer vs page, upsells, trust badges, shipping clarity
- **Site speed**: Core Web Vitals, image optimization, script bloat
- **SEO basics**: meta titles, descriptions, structured data, internal linking

Score each area out of 10. Calculate an overall score. Rank findings by impact (revenue at stake) and effort (implementation complexity).

## Phase 3: Person Research

Execute `person-researcher` on the demo contact:
- LinkedIn profile summary and headline
- Recent LinkedIn posts and articles (last 3 months)
- Conference talks, podcast appearances, media quotes
- Career trajectory: previous roles, time at current company, promotions
- Topics they engage with: what they like, comment on, share
- Mutual connections or shared interests
- Communication style indicators (formal vs casual, data-driven vs narrative)

## Phase 4: Compile Audit Document

Structure the output as a presentable audit:

```
PROSPECT AUDIT: [Company Name]
Prepared for: [Contact Name], [Title]
Date: [Demo Date]
Prepared by: Plasho

=== EXECUTIVE SUMMARY ===
[2-3 sentence overview: what the company does, what we found, what's at stake]

=== COMPANY OVERVIEW ===
- Business: [summary]
- Platform: [tech stack]
- Team: [size if discoverable]
- Recent news: [funding, launches, hires]
- Social footprint: [Instagram Nk, LinkedIn Nk]

=== STORE AUDIT FINDINGS ===
Overall Score: X/10

Finding 1: [Issue Title]
- What: [Description of the issue]
- Impact: [What it's costing them -- quantified where possible]
- Fix: [Specific recommendation]
- Effort: [Low / Medium / High]
- Priority: [P1 / P2 / P3]

Finding 2: [Issue Title]
- What: [Description]
- Impact: [Cost]
- Fix: [Recommendation]
- Effort: [Level]
- Priority: [Level]

[Continue for top 5-7 findings, ordered by impact]

=== STRENGTHS ===
- [What they're doing well -- always start the conversation positive]
- [Specific things to compliment]
- [Areas where they're ahead of competitors]

=== OPPORTUNITY SIZING ===
Based on industry benchmarks:
- Current estimated conversion rate: X%
- Potential with fixes: Y%
- Revenue impact: Z% increase in online revenue
- If monthly revenue is ~$A, the gap is ~$B/month

=== RELEVANT CASE STUDY ===
[Most relevant case study from agency.config.json case_studies]
- Client: [name]
- Challenge: [what they faced]
- Solution: [what was done]
- Result: [metrics and outcomes]
- Relevance: [why this matters to the prospect]

=== TALKING POINTS FOR DEMO ===
1. [Personalized opening based on person-researcher -- reference their recent post or talk]
2. [Key finding to lead with -- the highest-impact issue from the audit]
3. [Discovery question to ask them -- something that shows you've done homework]
4. [Case study to reference -- tie it to their specific situation]
5. [CTA / next step to propose -- clear, specific, time-bound]
```

## Phase 5: Output

Return the audit in two formats:
1. **Structured text**: the full document as formatted above, ready to read or paste
2. **JSON**: machine-readable version with all fields for programmatic use or CRM storage

```json
{
  "company": {
    "name": "",
    "website": "",
    "industry": "",
    "tech_stack": [],
    "social": {},
    "news": []
  },
  "contact": {
    "name": "",
    "title": "",
    "linkedin": "",
    "talking_points": []
  },
  "audit": {
    "overall_score": 0,
    "findings": [],
    "strengths": [],
    "opportunity": {}
  },
  "demo_prep": {
    "opening": "",
    "key_finding": "",
    "discovery_question": "",
    "case_study": "",
    "cta": ""
  }
}
```

Optionally: save the audit to CRM notes for the lead, and export as HTML for sharing with the team.

## Example Usage

**Trigger phrases:**
- "Audit [company] before my demo"
- "Prep for demo with [contact] at [company]"
- "Run prospect audit for [website]"
- "Generate sales prep for tomorrow's demo"
