---
name: gig-proposal-writer
description: >
  Generates personalized proposals for freelance gigs on Upwork, Freelancer,
  PeoplePerHour, and Guru. References specific project requirements and
  includes relevant case studies.
tags: [outreach, proposals, freelance]
---

# Gig Proposal Writer

Generates tailored proposals for freelance platform gigs. Each proposal references specific requirements from the project brief, includes a relevant case study, and asks an insightful question that proves you read the brief.

## Prerequisites

- `agency.config.json` populated (services, case studies, tone)
- Gig details (title, description, budget, platform, URL)

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.tagline` -- who we are
- `case_studies` -- proof points to reference
- `outreach.tone` -- writing style
- `services` -- match gig to relevant service

Gather gig details:
1. Platform (Upwork, Freelancer, PeoplePerHour, Guru, Fiverr)
2. Project title
3. Project description (full text)
4. Budget (if specified)
5. URL to the gig listing

## Phase 1: Analyze the Brief

Read the project description and identify:
- Specific requirements (what they need built/fixed)
- Technology mentions (Shopify, WooCommerce, etc.)
- Timeline urgency signals
- Budget expectations
- Pain points or challenges mentioned
- Questions they asked or decisions they need help with

## Phase 2: Match Case Study

Select the most relevant case study from `case_studies`:
- Match by industry (sports brand -> Kibi Sports)
- Match by service type (CRO -> CRO case study)
- Match by platform (Shopify -> any Shopify case study)
- If no close match, reference expertise without naming clients

## Phase 3: Generate Proposal

### Platform-Specific Rules

**Freelancer:**
- Mention milestone-based delivery to build trust
- Include realistic bid amount and timeline
- Under 200 words

**PeoplePerHour:**
- Be concise and punchy -- PPH rewards brevity
- Under 150 words
- Highlight hourly or fixed-price preference

**Upwork:**
- Reference specific requirements from the posting
- Include 2-3 bullet points of what you'll deliver
- Ask one smart question
- Under 200 words

**Guru:**
- Highlight relevant skills and past work
- Include portfolio reference
- Under 200 words

**Fiverr:**
- Match their request to your gig offering
- Under 100 words

### Proposal Structure

1. **Hook** -- Reference something specific from their brief (proves you read it)
2. **Relevant experience** -- 1 sentence connecting your experience to their need
3. **Case study** -- Brief proof point from a similar project
4. **Approach** -- 2-3 sentences on how you'd tackle it
5. **Question** -- One insightful question that shows expertise
6. **CTA** -- Clear next step

### Rules
- NEVER start with "I" or "My name is"
- Start with their problem or a specific observation about their project
- Reference at least 2 specific details from their brief
- Include a realistic bid and timeline
- No generic boilerplate

## Phase 4: Output

Return JSON:
```json
{
  "proposalText": "the full proposal text",
  "bidAmount": "$500",
  "deliveryDays": 14,
  "personalizationPoints": ["referenced their multi-currency requirement", "matched CRO need to Kibi case study"],
  "platform": "Freelancer",
  "wordCount": 180
}
```

Generate 2 variants. User picks the best.

## Phase 5: Delivery

Based on platform:
- **Browser** (tools.browser_automation): Navigate to gig page, paste proposal, set bid
- **Manual**: Display proposal for copy-paste

Log to CRM via `crm-writer`:
- Add to `crm.tabs.outreach_log` with platform, gig URL, proposal status

## Example Usage

**Trigger phrases:**
- "Write a proposal for this Freelancer gig"
- "Draft an Upwork proposal for [gig URL]"
- "Generate proposals for today's gig finds"
