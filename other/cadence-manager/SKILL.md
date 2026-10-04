---
name: cadence-manager
description: >
  Orchestrates the full multi-channel outreach cadence for all active leads.
  Tracks where each lead is, generates appropriate content, manages daily
  caps, handles weekends, and coordinates across email, LinkedIn, Instagram,
  and phone.
tags: [outreach, cadence, orchestration, playbook]
---

# Cadence Manager

The central orchestrator for all outreach cadence operations. Manages the lifecycle of every lead from first touch through breakup or conversion.

## Prerequisites

- `agency.config.json` populated (outreach cadence, tools, daily caps)
- Leads in CRM at various cadence stages

## Composites & Capabilities Used

1. `follow-up-engine` composite -- process daily follow-ups
2. `outreach-draft-pipeline` composite -- generate new outreach
3. `cold-email-drafter` capability -- email content
4. `message-generator` capability -- multi-channel content
5. `crm-writer` capability -- CRM updates

## Phase 0: Cadence Overview

Read `agency.config.json outreach.cadence` and present the configured cadence:

```
YOUR OUTREACH CADENCE
---
Day 1:  Email (Touch 1) + Instagram Engage
Day 2:  LinkedIn Connection Request
Day 3:  Add to Calling Sheet
Day 4:  Email Follow-Up #1 (new angle)
Day 5:  Instagram DM Follow-Up
Day 6:  Call Follow-Up (add to sheet)
Day 7:  Email Follow-Up #2 (case study)
Day 8:  Rest
Day 9:  Email Follow-Up #3 (urgency)
Day 10: Rest
Day 11: Breakup Email

Daily caps: Email N, LinkedIn N, Instagram N, Calls N
Weekend rule: Push to Monday
```

## Phase 1: Pipeline Audit

Query CRM for all leads in cadence (stage = CONTACTED):

```
CADENCE STATUS
---
Day 1-3:   N leads (early stage)
Day 4-7:   N leads (mid stage)
Day 8-11:  N leads (late stage)
Paused:    N leads (responded, awaiting manual follow-up)
Breakup:   N leads (cadence complete)

Overdue:   N leads (missed actions, need catch-up)
```

## Phase 2: Daily Execution

Execute `follow-up-engine` to process all leads with actions due today.

Handle edge cases:
- **Weekend actions**: Auto-defer to Monday. Adjust subsequent days.
- **Over daily cap**: Prioritize by score (HOT first). Defer WARM to tomorrow.
- **Missing channel data**: Skip unavailable channels, note in CRM.
- **Lead responded**: Pause cadence immediately, flag for manual review.
- **Bounced email**: Remove from email sequence, switch to LinkedIn/Instagram only.

## Phase 3: Cadence Health

Monitor cadence performance:

```
CADENCE HEALTH REPORT
---
Response rate by touch:
- Touch 1 (Day 1): X% response rate
- Touch 2 (Day 4): X%
- Touch 3 (Day 7): X%
- Touch 4 (Day 9): X%
- Breakup (Day 11): X%

Response rate by channel:
- Email: X%
- LinkedIn: X%
- Instagram: X%
- Phone: X%

Average days to response: N
Best performing touch: Touch N (X%)
Worst performing: Touch N (X%)

Recommendations:
- [If Touch 1 < 5%]: Consider revising email subject lines or opening hooks
- [If LinkedIn > Email]: Shift more weight to LinkedIn touches
- [If breakup gets responses]: Consider extending cadence
```

## Phase 4: Adjustments

Based on performance data, suggest cadence modifications:
- If response rate is low on a specific touch, suggest changing the angle
- If a channel underperforms, suggest rebalancing
- If breakup emails get responses, suggest adding Day 14/21 touches

User approves changes. Update `agency.config.json outreach.cadence` if modified.

## Example Usage

**Trigger phrases:**
- "Show cadence status"
- "How's the outreach cadence performing?"
- "Run the cadence manager"
- "What leads need follow-up?"
- "Adjust the cadence -- add a Day 14 touch"
