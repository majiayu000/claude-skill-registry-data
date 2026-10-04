---
name: nurture-sequence
description: >
  Builds drip email campaigns for leads not ready to buy. Determines
  segment and buying stage, selects content per stage, and generates
  a complete 5-7 email sequence over 30 days with timing and content.
tags: [email, nurture, drip-campaign, sequences, content]
---

# Nurture Sequence

Generates a complete drip email campaign for leads that are qualified but not ready to buy. Maps the lead's segment and buying stage to a content strategy, selects the right content progression (educational, case study, social proof, offer), and outputs a full 5-7 email sequence with subject lines, body copy, timing, and performance benchmarks.

## Prerequisites

- `agency.config.json` populated (services, ICP, brand voice, content library)
- Lead data with segment and qualification status
- Content library or `case_studies[]` for reference material
- Optional: `brand-voice` capability output for tone consistency

## Capabilities Used

1. `email-copywriter` -- write individual nurture emails
2. `brand-voice` -- maintain consistent tone across the sequence
3. `crm-writer` -- set up the sequence in CRM with timing
4. `cold-email-drafter` -- for the transition-to-sales emails at the end
5. `carousel-creator` -- for generating linked content assets

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- services to eventually pitch
- `case_studies[]` -- available social proof content
- `icp.segments[]` -- for segment-specific messaging
- `brand_voice` -- tone and style guidelines
- `content_library` -- available content assets (blogs, guides, videos)
- `nurture_config` -- default nurture settings if defined:
  ```json
  {
    "nurture_config": {
      "default_length": 7,
      "default_duration_days": 30,
      "max_emails_per_week": 2,
      "unsubscribe_handling": "respect_immediately",
      "send_times": {
        "preferred_days": ["tuesday", "thursday"],
        "preferred_hours": "10:00-11:00"
      }
    }
  }
  ```

Accept parameters:
- `lead` -- (required) lead object with segment and stage info
- `segment` -- ICP segment override (if not in lead data)
- `buying_stage` -- `awareness` | `consideration` | `decision`. Default: auto-detect from lead score
- `sequence_length` -- number of emails. Default: from config or 7
- `duration_days` -- total campaign duration. Default: from config or 30
- `goal` -- `book_demo` | `start_trial` | `request_proposal` | `download_resource`. Default: `book_demo`
- `include_case_study` -- boolean. Default: `true`

## Phase 1: Segment and Stage Analysis

### Determine Buying Stage
If not explicitly provided, infer from lead data:

```
Awareness stage (score 1.5-2.5):
  - Lead knows they have a problem but hasn't started evaluating solutions
  - Content focus: education, thought leadership, industry insights
  - Tone: helpful, no sales pressure

Consideration stage (score 2.5-3.5):
  - Lead is actively researching solutions and evaluating options
  - Content focus: comparisons, case studies, ROI frameworks
  - Tone: consultative, show expertise

Decision stage (score 3.5+):
  - Lead is close to choosing a partner, needs final push
  - Content focus: case studies, testimonials, specific proposals
  - Tone: confident, create urgency
```

### Segment-Specific Messaging
Map the lead's segment to relevant messaging angles:

```
Post-PMF D2C India:
  Pain points: scaling beyond 1 SKU, store doesn't match growth, basic Shopify theme
  Content angles: "scaling your D2C store", "CRO for growing brands", "catalog management for new SKUs"
  Case studies: reference similar-stage Indian D2C brands

Midmarket D2C India:
  Pain points: in-house team overwhelmed, need outside expertise, store refresh
  Content angles: "agency vs in-house", "CRO audit framework", "managing ecomm at scale"
  Case studies: reference mid-size brands with outsourced ecomm

Early-stage D2C US/UK/AU:
  Pain points: basic store, no ecomm expertise, growing fast but store is limiting
  Content angles: "store foundations for fast-growing D2C", "why CRO matters early", "Shopify best practices"
  Case studies: reference international D2C brands if available
```

## Phase 2: Content Strategy

Design the content progression for the sequence:

### Awareness Stage Sequence (7 emails, 30 days)
```
Email 1 (Day 1): Welcome + Value
  Purpose: Establish relationship, deliver immediate value
  Content: Industry insight or quick win they can implement today
  CTA: Soft -- read the full article / download the guide

Email 2 (Day 4): Educational Content
  Purpose: Position as expert, teach something useful
  Content: "3 things [segment] brands get wrong about [service area]"
  CTA: Soft -- reply with their biggest challenge

Email 3 (Day 8): Thought Leadership
  Purpose: Build trust with original perspective
  Content: Industry trend analysis or data-backed insight
  CTA: Soft -- share if useful

Email 4 (Day 13): Case Study (light)
  Purpose: Introduce social proof without hard sell
  Content: "How [similar brand] solved [problem]" -- story format, not sales format
  CTA: Medium -- read the full case study

Email 5 (Day 18): Interactive / Engagement
  Purpose: Get a response, build two-way relationship
  Content: Question, poll, or mini-audit offer ("Reply with your URL, I'll send you 3 quick wins")
  CTA: Medium -- reply to engage

Email 6 (Day 24): Value Stack
  Purpose: Demonstrate breadth of expertise
  Content: Curated resource (tools, templates, checklist relevant to their segment)
  CTA: Medium -- download or bookmark

Email 7 (Day 30): Soft Transition
  Purpose: Open the door to a conversation
  Content: Recap value delivered, mention availability for deeper help
  CTA: Strong -- book a 15-min call (no commitment framing)
```

### Consideration Stage Sequence (6 emails, 25 days)
```
Email 1 (Day 1): Welcome + Positioning
  Content: Quick intro, why they're hearing from you, one key insight
  CTA: Soft

Email 2 (Day 4): Comparison / Framework
  Content: "How to evaluate a [service] partner" or "Agency vs freelancer vs in-house"
  CTA: Soft

Email 3 (Day 9): Case Study (detailed)
  Content: Full Problem-Solution-Results with metrics
  CTA: Medium -- "Want similar results?"

Email 4 (Day 14): Social Proof Stack
  Content: 3 quick client wins (mini case studies, 2-3 sentences each)
  CTA: Medium -- book a call

Email 5 (Day 20): ROI / Value Proof
  Content: ROI calculator, cost-of-inaction framing, or audit results
  CTA: Strong -- "Let me show you what this looks like for your brand"

Email 6 (Day 25): Direct Offer
  Content: Specific proposal teaser or free audit offer
  CTA: Strong -- book demo / request proposal
```

### Decision Stage Sequence (5 emails, 14 days)
```
Email 1 (Day 1): Direct Value Proposition
  Content: "Here's exactly how we'd help [company]" -- specific to their needs
  CTA: Strong

Email 2 (Day 3): Case Study Match
  Content: Most relevant case study to their exact situation
  CTA: Strong

Email 3 (Day 6): Objection Crusher
  Content: Address the top objection for their segment (price, timing, risk)
  CTA: Strong

Email 4 (Day 10): Urgency / Scarcity
  Content: Timing element (seasonal, competitive, capacity)
  CTA: Strong -- book this week

Email 5 (Day 14): Final Touch
  Content: Respectful last touch, door stays open
  CTA: Strong but not pushy
```

## Phase 3: Email Generation

For each email in the sequence, generate using `email-copywriter`:

### Email Specifications
```
For each email:
  Subject line: [specific, benefit-driven, under 50 characters]
  Preview text: [extends the subject, under 90 characters]
  Body:
    - Opening: [hook, 1-2 sentences]
    - Value: [main content, 3-5 sentences]
    - CTA: [clear, single action]
    - Sign-off: [personal, from a human]
  Word count: 80-150 words (nurture emails must be short)
  Tone: [from brand_voice + stage-appropriate adjustments]
  Personalization tokens: [{{first_name}}, {{company}}, {{industry}}, {{detected_need}}]
```

### Content Rules
- NO sales language in awareness stage emails
- Every email delivers standalone value (reader learns something even if they don't click)
- Subject lines vary in style (question, number, statement, curiosity gap)
- Never start two consecutive emails with the same opening style
- Include a "PS:" in at least 2 emails (high readership zone)
- Link to real content when referencing articles or case studies
- Each email has a different angle -- never repeat the same message

## Phase 4: Timing and Delivery Rules

### Send Timing
```
Preferred days: [from nurture_config.send_times.preferred_days]
Preferred hours: [from nurture_config.send_times.preferred_hours]
Max per week: [from nurture_config.max_emails_per_week]
Timezone: [lead's timezone if known, else agency timezone]
```

### Spacing Rules
- Minimum 3 days between emails
- No emails on weekends (unless config overrides)
- No emails on major holidays (country-specific based on lead location)
- Respect global suppression list

### Exit Conditions
Stop the sequence if:
- Lead replies (transition to manual follow-up or `follow-up-engine`)
- Lead books a meeting (mark as converted)
- Lead unsubscribes (respect immediately)
- Lead marked as disqualified
- Sequence completes all steps

## Phase 5: Output

Return structured JSON:

```json
{
  "sequence_name": "nurture_awareness_d2c_india",
  "lead": {
    "contact_name": "Priya Mehta",
    "company_name": "FreshSkin Co",
    "segment": "Post-PMF D2C India",
    "buying_stage": "awareness"
  },
  "sequence_config": {
    "total_emails": 7,
    "duration_days": 30,
    "goal": "book_demo",
    "send_days": ["tuesday", "thursday"],
    "send_time": "10:00 IST"
  },
  "emails": [
    {
      "position": 1,
      "send_day": 1,
      "send_date": "2026-03-08",
      "type": "welcome_value",
      "subject": "The one metric most D2C brands ignore",
      "preview": "It's not conversion rate -- and it's costing you",
      "body": "[full email copy]",
      "cta": "Read the full breakdown",
      "cta_link": "[content URL]",
      "word_count": 120,
      "personalization_tokens": ["first_name", "company"]
    },
    {
      "position": 2,
      "send_day": 4,
      "send_date": "2026-03-11",
      "type": "educational",
      "subject": "3 product page mistakes killing your AOV",
      "preview": "Quick fixes that take 30 minutes",
      "body": "[full email copy]",
      "cta": "Reply with your URL for a free quick audit",
      "cta_link": null,
      "word_count": 135,
      "personalization_tokens": ["first_name", "industry"]
    }
  ],
  "exit_conditions": [
    "lead_replies",
    "meeting_booked",
    "unsubscribe",
    "disqualified",
    "sequence_complete"
  ],
  "post_sequence_action": "re_evaluate_qualification",
  "benchmarks": {
    "expected_open_rate": "35-45%",
    "expected_click_rate": "3-5%",
    "expected_reply_rate": "5-8%",
    "expected_conversion_rate": "10-15%"
  },
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 6: Review

Present the full sequence.

**APPROVAL GATE**: "[N]-email nurture sequence for [segment] leads. Review before activating?"

After approval:
- Write sequence to CRM via `crm-writer`
- Set first email send date
- Configure exit condition triggers
- Set re-evaluation reminder at sequence end

## Phase 7: Performance Tracking Setup

Set up benchmarks for `sequence-analyzer` to evaluate later:

```
SEQUENCE BENCHMARKS
---
Sequence: [name]
Created: [date]
Target metrics:
  Open rate: [benchmark]%
  Click rate: [benchmark]%
  Reply rate: [benchmark]%
  Conversion rate (booked demo): [benchmark]%
  Unsubscribe rate: < 1%
Review date: [30 days from start]
```

## Example Usage

Trigger phrases:
- "Build a nurture sequence for [lead]"
- "Create a drip campaign for awareness-stage leads in [segment]"
- "This lead isn't ready to buy, set up a nurture sequence"
- "Generate a 7-email nurture campaign for D2C brands"
- "Build a consideration-stage email sequence for [prospect]"
- "[Lead] was routed to nurture, build the sequence"
