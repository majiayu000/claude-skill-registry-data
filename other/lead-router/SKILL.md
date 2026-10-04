---
name: lead-router
description: >
  Routes qualified leads to the right team member or sequence based on
  score, segment, and source. Applies configurable routing rules to assign
  leads to founder direct, SDR sequences, or nurture campaigns.
tags: [leads, routing, assignment, pipeline]
---

# Lead Router

Takes a qualified lead and routes it to the correct team member, outreach sequence, or nurture campaign based on configurable rules. Evaluates lead score, segment, source channel, deal size, and urgency to determine the optimal path. Ensures no lead falls through the cracks and every lead gets the appropriate level of attention.

## Prerequisites

- `agency.config.json` populated (routing rules, team assignments, sequences)
- Lead must have qualification data (from `lead-qualifier` or manual input)
- CRM access for writing routing decisions
- Optional: outreach sequences configured for handoff

## Capabilities Used

1. `crm-writer` -- update lead assignment and routing status
2. `lead-scorer` -- pull lead score if not already available
3. `message-generator` -- generate initial outreach based on route
4. `cold-email-drafter` -- draft first touch if routed to email sequence

## Phase 0: Intake

Read `agency.config.json`:
- `routing_rules` -- configurable routing logic:
  ```json
  {
    "routing_rules": {
      "hot_lead_threshold": 4.5,
      "warm_lead_threshold": 3.5,
      "routes": {
        "founder_direct": {
          "criteria": ["score >= 4.5", "deal_size >= 100000", "source = referral"],
          "owner": "founder",
          "sla_hours": 4,
          "first_touch": "personal_email"
        },
        "sdr_sequence": {
          "criteria": ["score >= 3.5", "score < 4.5"],
          "owner": "sdr_team",
          "sla_hours": 24,
          "first_touch": "outreach_sequence"
        },
        "nurture": {
          "criteria": ["score < 3.5", "icp_fit != NO_FIT"],
          "owner": "marketing",
          "sla_hours": 48,
          "first_touch": "nurture_email"
        },
        "disqualified": {
          "criteria": ["icp_fit = NO_FIT", "deal_breaker = true"],
          "owner": "none",
          "action": "archive"
        }
      },
      "overrides": {
        "enterprise": "founder_direct",
        "referral": "founder_direct",
        "competitor_client": "founder_direct"
      }
    }
  }
  ```
- `team[]` -- team members with roles and capacity
- `sequences[]` -- available outreach sequences
- `crm.tabs` -- CRM locations for each route

Accept parameters:
- `lead` -- (required) qualified lead object (output from `lead-qualifier` or enriched lead)
- `mode` -- `single` | `batch`. Default: `single`
- `leads` -- (required if mode = `batch`) array of qualified leads
- `dry_run` -- boolean, show routing decision without executing. Default: `false`
- `auto_first_touch` -- boolean, generate and queue first outreach. Default: `true`

## Phase 1: Lead Evaluation

Extract routing-relevant attributes from the lead:

```
ROUTING INPUTS
---
Lead: [contact name] at [company]
Qualification verdict: [SQL/MQL/NURTURE/UNQUALIFIED]
Final score: [number]
ICP segment: [segment name]
ICP fit: [STRONG/MODERATE/WEAK/NO_FIT]
Source: [inbound_form/outbound/referral/event/organic]
Estimated deal size: [monthly value]
Urgency: [immediate/near-term/medium-term/long-term]
Authority level: [decision-maker/influencer/unknown]
Industry: [vertical]
Company size: [employee range]
```

## Phase 2: Rule Matching

Apply routing rules in priority order:

### Override Check (highest priority)
Check `routing_rules.overrides` first:
- Enterprise company (500+ employees or known enterprise brand): -> `founder_direct`
- Referral source: -> `founder_direct`
- Competitor's client (switching signals): -> `founder_direct`
- Strategic account (in target account list): -> `founder_direct`

### Score-Based Routing
If no override triggered, apply score thresholds:

```
Score >= hot_lead_threshold (4.5):
  -> founder_direct
  Reasoning: High-intent, qualified lead deserves personal attention

Score >= warm_lead_threshold (3.5) AND < hot_lead_threshold:
  -> sdr_sequence
  Reasoning: Qualified but needs nurturing through sales process

Score >= 2.5 AND < warm_lead_threshold AND icp_fit != NO_FIT:
  -> nurture
  Reasoning: Potential fit but not ready to buy, keep warm

Score < 2.5 OR icp_fit = NO_FIT:
  -> disqualified
  Reasoning: Poor fit or insufficient signals
```

### Source-Based Adjustments
Modify routing based on source channel:
- **Inbound form with specific service request**: Bump urgency, consider founder_direct
- **Outbound response (replied to cold email)**: Route to whoever sent the original email
- **Referral**: Always founder_direct regardless of score
- **Event/conference lead**: Route to whoever attended the event
- **Organic (blog, SEO)**: Standard score-based routing

### Capacity Check
Before finalizing route:
- Check team member capacity (current lead load vs max)
- If assigned owner is at capacity, route to next available team member
- If all SDRs at capacity, escalate to founder with capacity alert

## Phase 3: Sequence Assignment

Based on route, assign the appropriate outreach sequence:

### Founder Direct Path
```
Sequence: personal_outreach
Steps:
  1. Personal email within SLA (4 hours)
  2. LinkedIn connection request (same day)
  3. Follow-up email (Day 3)
  4. Phone call attempt (Day 5)
  5. Value-add touchpoint (Day 7)

First touch content:
  - Mention specific signal or context
  - Reference relevant case study
  - Propose specific meeting time
  - Personal sign-off from founder
```

### SDR Sequence Path
```
Sequence: standard_outreach
Steps:
  1. Intro email (within SLA, 24 hours)
  2. LinkedIn connection (Day 2)
  3. Follow-up email with case study (Day 4)
  4. Phone call attempt (Day 6)
  5. Value email (Day 8)
  6. Breakup email (Day 11)

First touch content:
  - Template-based but personalized with enrichment data
  - Reference their industry and specific need detected
  - Include relevant case study link
  - CTA: book a call
```

### Nurture Path
```
Sequence: nurture_drip
Steps:
  - Trigger `nurture-sequence` skill with lead segment and stage
  - Educational content first (not sales)
  - 5-7 emails over 30 days
  - Re-evaluate after nurture completes

First touch content:
  - Welcome / value-first email
  - Share relevant content piece (blog, guide, video)
  - No hard CTA, soft engagement ask
```

### Disqualified Path
```
Action: archive
Steps:
  - Mark as disqualified in CRM with reason
  - No outreach
  - Add to low-priority newsletter list (if email valid)
  - Re-evaluate in 6 months (set reminder)
```

## Phase 4: First Touch Generation

If `auto_first_touch` = true:

Based on the assigned sequence, generate the first outreach:

For **founder_direct**:
- Use `message-generator` with personal tone
- Include: specific research reference, case study, calendar link
- Channel: email (draft, not send)

For **sdr_sequence**:
- Use `cold-email-drafter` with the lead's enrichment data
- Personalize based on: industry, detected needs, recent signals
- Channel: email (draft, not send)

For **nurture**:
- Use `email-copywriter` for educational content
- Tone: helpful, not salesy
- Channel: email (draft, not send)

## Phase 5: Output

Return structured JSON:

```json
{
  "routing_date": "2026-03-07",
  "lead": {
    "contact_name": "Priya Mehta",
    "company_name": "FreshSkin Co",
    "score": 4.2,
    "verdict": "SQL",
    "icp_fit": "STRONG_FIT",
    "source": "inbound_form"
  },
  "routing_decision": {
    "route": "founder_direct",
    "reason": "SQL with strong ICP fit, inbound with specific service request, estimated deal size above threshold",
    "rule_matched": "score >= 4.5 OR (score >= 3.5 AND source = inbound AND specific_request = true)",
    "override_applied": null,
    "assigned_owner": "founder",
    "sla_hours": 4,
    "sla_deadline": "2026-03-07T14:00:00+05:30"
  },
  "sequence": {
    "name": "personal_outreach",
    "total_steps": 5,
    "first_touch": {
      "channel": "email",
      "timing": "Within 4 hours",
      "draft": {
        "subject": "Your Shopify store revamp, Priya",
        "preview": "Saw FreshSkin's new serum line -- the product pages could convert much better. Here's what we did for a similar brand...",
        "status": "draft_ready"
      }
    },
    "next_steps": [
      {"day": 0, "action": "LinkedIn connection request"},
      {"day": 3, "action": "Follow-up email with case study"},
      {"day": 5, "action": "Phone call attempt"},
      {"day": 7, "action": "Value-add touchpoint"}
    ]
  },
  "capacity_check": {
    "owner_current_load": 8,
    "owner_max_capacity": 15,
    "status": "OK"
  },
  "crm_updates": {
    "stage": "ROUTED",
    "assigned_to": "founder",
    "sequence": "personal_outreach",
    "next_action": "Send first email",
    "next_action_date": "2026-03-07"
  },
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 6: Review

Present routing decision.

**APPROVAL GATE**: "[Lead] routed to [owner] via [sequence]. First touch drafted. Approve?"

If approved and `dry_run` = false:
- Update CRM via `crm-writer`
- Queue first touch email as draft
- Set up cadence reminders for subsequent touches
- Log routing decision for analytics

## Batch Mode Summary

When processing multiple leads:

```
ROUTING SUMMARY -- [Date]
===
Leads processed: N

Founder Direct: N
  1. [Lead] -- Score: [X] -- Reason: [brief]
  2. [Lead] -- Score: [X] -- Reason: [brief]

SDR Sequence: N
  1. [Lead] -- Score: [X] -- Assigned: [SDR name]
  2. [Lead] -- Score: [X] -- Assigned: [SDR name]

Nurture: N
  1. [Lead] -- Score: [X] -- Segment: [segment]

Disqualified: N
  1. [Lead] -- Reason: [brief]

Capacity alerts:
  - [SDR name] at 14/15 capacity
```

## Example Usage

Trigger phrases:
- "Route this lead: [qualified lead data]"
- "Where should [lead] go?"
- "Batch route this week's qualified leads"
- "Assign [lead] to the right sequence"
- "This lead just qualified, route them"
- "Who should handle the FreshSkin lead?"
