---
name: cold-email-drafter
description: >
  Framework-based cold email composer with 3 personalization tiers.
  Generates subject line, body, and follow-up variants. Never uses templates --
  builds from frameworks (PAS, BAB, AIDA, Signal-Proof-Ask).
tags: [outreach, email, personalization]
---

# Cold Email Drafter

Generates personalized cold emails using proven copywriting frameworks. Each email is built from scratch based on lead context, not recycled templates.

## Prerequisites

- `agency.config.json` populated (outreach tone, banned phrases, case studies)
- Lead data (company, contact name, title)
- For Tier 3: personalization packet from `personalization-enricher`

## Phase 0: Intake

Read `agency.config.json` and gather:
- `outreach.tone` -- writing style
- `outreach.banned_phrases` -- never include these
- `outreach.sign_off` -- email signature
- `case_studies` -- proof points to reference
- `services` -- what we offer

Gather from user:
1. **Lead context**: company name, contact name, title, company size
2. **Signal/trigger**: what prompted this outreach (funding, job post, community post, gig listing)
3. **Personalization tier**: 1 (basic), 2 (segment), or 3 (hyper-personalized)
4. **Email position**: initial (Touch 1), follow-up (Touch 2-3), or breakup (Touch 4)
5. **Personalization packet** (Tier 3 only): CRO findings, person's recent posts, specific pain points

## Phase 1: Framework Selection

Choose the framework based on signal type and email position:

| Signal Type | Touch 1 (Day 1) | Touch 2 (Day 4) | Touch 3 (Day 7) | Breakup (Day 10) |
|------------|------------------|------------------|------------------|-------------------|
| CRO issue found | PAS | BAB | Case Study | Respectful close |
| Funding/growth signal | Signal-Proof-Ask | AIDA | Case Study | Respectful close |
| Job posting / hiring | BAB | PAS | Case Study | Respectful close |
| Community post / gig | AIDA | Signal-Proof-Ask | Case Study | Respectful close |
| No specific signal | PAS | BAB | Case Study | Respectful close |

### Framework Structures

**PAS (Problem-Agitation-Solution)**
1. Name a specific problem they have (from CRO audit or research)
2. Agitate: what it's costing them (lost revenue, missed conversions)
3. Solution: how you've fixed this before (case study reference)
4. CTA: soft ask

**BAB (Before-After-Bridge)**
1. Before: their current situation (specific observation)
2. After: what it could look like (with numbers if possible)
3. Bridge: how to get there (your service)
4. CTA: soft ask

**AIDA (Attention-Interest-Desire-Action)**
1. Attention: hook referencing something specific about them
2. Interest: relevant insight or data point
3. Desire: case study or proof of results
4. Action: clear next step

**Signal-Proof-Ask**
1. Signal: reference the specific trigger ("saw you just raised Series A")
2. Proof: relevant case study or expertise
3. Ask: one clear question or CTA

## Phase 2: Personalization by Tier

### Tier 1 -- Merge Fields (for bulk sends)
- Use: {{first_name}}, {{company_name}}, {{industry}}
- Generic but professional
- One case study reference
- 60-90 words

### Tier 2 -- Segment-Based
- Reference industry-specific pain points
- Use company-size-appropriate language (founder vs VP)
- Tailor case study to their industry
- 80-120 words

### Tier 3 -- Hyper-Personalized
- Reference their specific CRO issue ("noticed your product pages don't show reviews")
- Reference their personal activity ("loved your LinkedIn post about X")
- Reference the specific signal that triggered outreach
- Connect all three: signal + finding + proof point
- 80-120 words
- This tier requires output from `personalization-enricher`

## Phase 3: Generate Email

### Rules (non-negotiable)
- Subject line: SUPER CATCHY. Under 50 characters, curiosity-driven, attention-grabbing.
  Think viral tweet energy, not corporate email. Examples:
  - "your product pages are leaking revenue"
  - "found something on your store"
  - "quick CRO win for [company]"
  - "[name], saw your post about [topic]"
  - "re: your Shopify store"
  - "this might save you 20% in lost sales"
  DO NOT use: generic greetings, company names only, ALL CAPS, clickbait, spam triggers.
  Subject line is the single most important part of the email. Spend extra cycles on it.
- Opening: NO filler ("I hope this finds you well", "My name is"). Start with value.
- Body: Max 5 sentences. Lead with their problem, not your service.
- CTA: ONE per email. Soft ask. ("Worth a 15-min look?" / "Open to a quick chat?")
- Sign-off: from `agency.config.json outreach.sign_off`
- Never include: anything from `outreach.banned_phrases`
- Each follow-up adds NEW value (never "just bumping this up")

### Word Limits by Position
| Position | Day | Words | Tone |
|----------|-----|-------|------|
| Touch 1 (initial) | Day 1 | 60-90 | Direct, value-first |
| Touch 2 (new angle) | Day 4 | 40-60 | Different pain point, brief |
| Touch 3 (case study) | Day 7 | 60-90 | Kibi Sports case study + Plasho's work |
| Breakup | Day 10 | 30-50 | "Not a priority, thanks for your time" |

### Follow-Up Rules (Updated 10-Day Cadence)
- Touch 2 (Day 4): New pain point angle, different from Email 1. Threaded as Re:
- Touch 3 (Day 7): Kibi Sports case study with Plasho's work. Show results.
- Breakup (Day 10): "Looks like this isn't a priority right now. Thanks for your time. If things change, we're here." Keep it short, respectful, door open.
- NEVER repeat the same email angle across touches
- Each follow-up MUST add new value

## Phase 4: Output

Return JSON:
```json
{
  "subject": "email subject line",
  "body": "full email body with sign-off",
  "framework_used": "PAS",
  "personalization_tier": 3,
  "personalization_points": ["referenced CRO finding about missing reviews", "mentioned their LinkedIn post about D2C economics"],
  "word_count": 87,
  "position": "touch_1",
  "linkedin_note": "short LinkedIn connection note (under 300 chars, for Tier 2+)"
}
```

Generate 3 variants for Touch 1 (user picks the best). Single variant for follow-ups.

## Phase 5: Output Delivery

No approval gate. Generated content is passed directly to outreach-draft-pipeline for automated delivery.

Optionally log to CRM via `crm-writer` (Email Drafts tab).

## Phase 6: Delivery

All email delivery is via Chrome DevTools MCP -> Zoho webmail:
- `mcp__chrome-devtools__navigate_page` to Zoho webmail compose
- `mcp__chrome-devtools__fill` recipient, subject, body
- `mcp__chrome-devtools__click` send button

No Gmail MCP, no SMTP, no CSV export, no manual copy-paste.

## Example Usage

**Trigger phrases:**
- "Draft a cold email for [company/contact]"
- "Write the first touch email for this lead"
- "Generate a follow-up email (touch 3) for [contact]"
- "Write a breakup email for [contact]"
- "Draft emails for these 5 leads"
