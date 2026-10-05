---
name: sales-pipeline
description: Use when aI-powered sales pipeline inside 1ai-social. Track leads, qualify
  with BANT, generate proposals, schedule follow-ups, and get daily sales analytics.
  Use when managing B2B sales pipelines.
domain: sales
license: Apache-2.0
tags:
- sales
- pipeline
- crm
- lead-scoring
- proposals
- follow-up
- b2b
- money
- revenue
version: 2.0.0
author: oyi77
subdomain: ''
type: sales
category: sales
---


# Money-Making Overview

This pipeline converts leads into cash. Each stage advance increases deal probability: NEW (5%) → CONTACTED (10%) → QUALIFIED (25%) → DEMO (40%) → PROPOSAL (60%) → NEGOTIATION (80%) → CLOSED_WON (100%). Moving 10 leads through the full pipeline per month at $2K average deal size = $20K monthly revenue.


## Overview

The sales pipeline automates B2B deal tracking from lead capture to close. It tracks leads through 7 stages (NEW → CONTACTED → QUALIFIED → DEMO → PROPOSAL → NEGOTIATION → CLOSED_WON), qualifies with BANT, generates proposals, schedules follow-ups, and provides daily sales analytics. Integrates with 1ai-engage for lead capture and 1ai-social for content-driven pipeline.

## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Revenue Streams

1. **Your Own Sales ($2K-20K/deal)** — Close your own services through the pipeline
2. **Pipeline-as-a-Service ($1K-5K/mo)** — Manage pipeline for clients: import their leads, qualify, track stages, generate proposals
3. **Sales Analytics ($500-2K/mo)** — Pipeline reporting as a service: weekly reports, conversion analysis, revenue forecasts for other businesses

## First Action in 60 Minutes

```bash
#!/usr/bin/env bash
# Pipeline audit: measure current stage distribution
echo "=== Pipeline Audit ==="
echo "Leads by stage:"
echo "  NEW: $(sqlite3 ~/1ai-social/data.db 'SELECT COUNT(*) FROM sales_leads WHERE stage="NEW"' 2>/dev/null || echo 0)"
echo "  QUALIFIED: $(sqlite3 ~/1ai-social/data.db 'SELECT COUNT(*) FROM sales_leads WHERE stage="QUALIFIED"' 2>/dev/null || echo 0)"
echo "  PROPOSAL: $(sqlite3 ~/1ai-social/data.db 'SELECT COUNT(*) FROM sales_leads WHERE stage="PROPOSAL"' 2>/dev/null || echo 0)"
echo "  CLOSED_WON: $(sqlite3 ~/1ai-social/data.db 'SELECT COUNT(*) FROM sales_leads WHERE stage="CLOSED_WON"' 2>/dev/null || echo 0)"
echo ""
echo "Revenue target for this month: \$X"
echo "Deals needed at 60% proposal stage: X"
```

---

## When to Use

**Trigger phrases:**
- "sales pipeline"
- "track deal"
- "add lead to CRM"
- "sales report"
- "follow up"
- "generate proposal"
- "lead scoring"

**Use cases:**
- Managing B2B sales pipeline from lead to close
- Scoring and qualifying leads (BANT)
- Generating proposals and outreach messages
- Tracking follow-ups and daily sales queue
- Importing 1ai-engage leads into sales pipeline

**When NOT to use:**
- For marketing/social media tasks (use other 1ai-social tools)
- For customer support (use customer-support skill)
- When the prospect is not a good fit for your product
- For markets where you have no distribution channel
- When the deal size does not justify the effort

---

## Architecture

Sales is built INTO 1ai-social as MCP tools (prefixed `sales_`).

```
1ai-social MCP Server (75 tools total)
├── Marketing tools (55) — content, social, engagement, growth
├── 1ai-engage tools — cold outreach pipeline
└── Sales tools (20) — lead → qualify → propose → close
```

---

## Pipeline Stages — The Money Funnel

```
NEW → CONTACTED → QUALIFIED → DEMO → PROPOSAL → NEGOTIATION → CLOSED_WON
 🔍      📞          📋        🎯      📄          💬           🤝
                                                           └──▶ CLOSED_LOST ❌
```

| Stage | Win Probability | Money Mindset |
|-------|-----------------|---------------|
| NEW | 5% | Cold. Needs qualification or drop. |
| CONTACTED | 10% | They know you exist. Get on their radar. |
| QUALIFIED | 25% | Budget, authority, need, timeline confirmed. Real deal. |
| DEMO | 40% | They saw value. Now prove it solves their problem. |
| PROPOSAL | 60% | Halfway there. Don't stall — follow up within 24h. |
| NEGOTIATION | 80% | Price objections. Hold value, offer options. |
| CLOSED_WON | 100% | Money in the bank. Ask for referrals. |

---

## MCP Tools (20 sales_ tools)

### Lead Management (Capture Every Prospect)

- `sales_add_lead` — Add new lead
- `sales_list_leads` — List with stage/grade filters
- `sales_get_lead` — Full details + activities + proposals
- `sales_update_lead` — Update fields

### Qualification (Filter Tire-Kickers)

- `sales_qualify_lead` — BANT qualification (auto-advances when all 4 confirmed)

**BANT Checklist:**
- **B**udget — Can they afford it? Do they have a budget allocated?
- **A**uthority — Are they the decision maker? Can they sign?
- **N**eed — Do they clearly need what you offer? Is it a priority?
- **T**imeline — When do they want to buy? Is there urgency?

A lead is qualified only when ALL 4 criteria are confirmed. Do not advance unqualified leads — they waste your pipeline capacity.

### Pipeline (Move Deals Forward)

- `sales_move_lead` — Move to specific stage
- `sales_advance_lead` — Auto-advance to next stage

### Activities (Track Every Interaction)

- `sales_log_activity` — Log call/email/meeting/note
- `sales_get_activities` — Activity history

### Proposals (Close Deals)

- `sales_create_proposal` — Create proposal
- `sales_send_proposal` — Mark as sent
- `sales_get_proposals` — List proposals
- `sales_generate_proposal_template` — AI-generated template

### Follow-ups (Don't Lose Money to Silence)

- `sales_schedule_follow_up` — Schedule with due date
- `sales_complete_follow_up` — Mark done
- `sales_get_follow_ups` — List pending

### Analytics (Measure Your Money Machine)

- `sales_pipeline_report` — Full pipeline analytics
- `sales_daily_queue` — Today's priority actions

### Integration (Feed the Pipeline)

- `sales_import_from_engage` — Guide for importing 1ai-engage leads
- `sales_generate_outreach` — Personalized email/WA/LinkedIn

---

## Workflow: 1ai-engage → Sales (Convert Cold to Cash)

```
1. engage_list_leads(status='replied')     → get warm leads
2. sales_add_lead(source='engage', ...)    → import to pipeline
3. sales_qualify_lead(budget=True, ...)    → BANT qualify
4. sales_advance_lead()                    → move through stages
5. sales_generate_proposal_template()      → generate proposal
6. sales_create_proposal() → sales_send_proposal()
7. sales_schedule_follow_up()              → track follow-ups
8. sales_pipeline_report()                 → analytics
```

---

## Anti-Rationalization Table

| Excuse | Truth |
|--------|-------|
| "Pipeline is empty this month" | Start with 10 cold outreaches RIGHT NOW |
| "I need more tools" | You have 20 tools; use them |
| "Deals always stall at proposal" | Follow up within 24h or lose the deal |
| "Cold outreach does not work" | It works when personalized and targeted. Generic spam does not. |
| "I will follow up later" | 80% of sales require 5+ follow-ups. Follow up consistently. |
| "Price is the only factor" | Value, trust, and timing matter more than price. Sell outcomes. |

---

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
2. **Execute** — Run sales pipeline workflow with configured parameters
3. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings

## Output Format

On pipeline report: "[N] leads in pipeline, $[N] total value, [N]% to next stage, [N] deals closing this week"
