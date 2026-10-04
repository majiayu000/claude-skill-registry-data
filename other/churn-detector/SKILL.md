---
name: churn-detector
description: >
  Weekly churn risk detection across active client accounts. Scans for signals
  like decreased engagement, missed meetings, delayed payments, and competitor
  mentions. Scores risk 1-10 and outputs prioritized alert list.
tags: [account-management, churn, risk-detection, retention]
---

# Churn Detector

Scans all active client accounts for churn risk signals on a weekly cadence. Aggregates behavioral, financial, and communication indicators into a composite risk score (1-10) and generates an actionable alert list with recommended interventions.

## Prerequisites

- `agency.config.json` populated (services, CRM config)
- Active client accounts tracked in CRM with engagement history
- At least 4 weeks of historical data for trend analysis
- Optional: billing/invoice data for payment signal detection

## Capabilities Used

1. `crm-writer` -- read client engagement data from CRM
2. `company-researcher` -- detect competitor or market signals
3. `message-generator` -- draft retention outreach messages

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- map active services per client
- `crm.tabs` -- locate client pipeline and engagement data
- `agency.name` -- for output attribution

Accept parameters:
- `scan_scope` -- `all_active` | `specific_client`. Default: `all_active`
- `client_name` -- (required if scope = `specific_client`)
- `lookback_weeks` -- number of weeks to analyze. Default: `4`
- `alert_threshold` -- minimum risk score to flag. Default: `5`
- `include_recommendations` -- boolean. Default: `true`

## Phase 1: Client Inventory

Query CRM for all active client accounts:
- Client name, contract start date, renewal date
- Active services (mapped to `services[]`)
- Primary contact person
- Account owner / relationship manager
- Monthly retainer value
- Last interaction date

Build the scan list. If `scan_scope` = `specific_client`, filter to that account only.

## Phase 2: Signal Detection

For each client, scan across five signal categories:

### 2a: Engagement Signals
- **Meeting frequency change**: Compare meetings held in last 4 weeks vs prior 4 weeks. Flag if >30% decline.
- **Response time degradation**: Average time to reply to emails/messages. Flag if >2x slower than baseline.
- **Meeting no-shows**: Any missed or cancelled meetings in the lookback period.
- **Reduced scope requests**: Fewer tasks, projects, or requests submitted vs baseline.
- **Silence periods**: No communication for 7+ consecutive days (excluding holidays).

Score each signal 0-2:
- 0 = Normal
- 1 = Mild concern
- 2 = Strong signal

### 2b: Financial Signals
- **Late payments**: Invoices paid after due date. Flag days overdue.
- **Payment disputes**: Any invoice questioned or contested.
- **Budget discussions**: Mentions of "budget cuts", "cost reduction", "pausing spend".
- **Scope reductions**: Active services reduced or paused.
- **Contract non-renewal signals**: Approaching renewal with no renewal conversation initiated.

Score each signal 0-2.

### 2c: Satisfaction Signals
- **Negative feedback**: Explicit complaints, dissatisfaction expressed in any channel.
- **Escalation frequency**: Issues escalated beyond normal contact.
- **Deliverable rejection rate**: Percentage of deliverables requiring major revisions.
- **Tone shift**: Communication tone becoming more formal, shorter, or less friendly.
- **Praise absence**: No positive feedback in the lookback period (absence of signal).

Score each signal 0-2.

### 2d: Competitive Signals
Run `company-researcher` (quick depth) to check:
- **Competitor mentions**: Client mentions or follows competing agencies on LinkedIn.
- **Job postings**: Client hiring for roles that overlap with agency services (e.g., "Shopify developer", "CRO specialist").
- **RFP activity**: Signs the client is shopping for alternatives.
- **New vendor announcements**: Client announces partnership with another agency.

Score each signal 0-3 (competitive signals carry higher weight).

### 2e: Usage Signals
- **Dashboard/tool logins**: If client has access to shared dashboards, check login frequency.
- **Report engagement**: Are they opening and reviewing shared reports?
- **Feature adoption**: Are they using all contracted services or ignoring some?
- **Support ticket volume**: Sudden drop may indicate disengagement; sudden spike may indicate frustration.

Score each signal 0-2.

## Phase 3: Risk Scoring

Calculate composite risk score per client:

```
engagement_score = sum(2a signals) / max_possible * 3.0
financial_score = sum(2b signals) / max_possible * 2.5
satisfaction_score = sum(2c signals) / max_possible * 2.0
competitive_score = sum(2d signals) / max_possible * 1.5
usage_score = sum(2e signals) / max_possible * 1.0

raw_total = engagement + financial + satisfaction + competitive + usage
risk_score = round(raw_total, 1)  # Scale 1-10
```

Risk tiers:
- **1-3**: LOW -- healthy account, no action needed
- **4-5**: WATCH -- minor signals, monitor closely
- **6-7**: ELEVATED -- multiple signals, proactive outreach recommended
- **8-9**: HIGH -- significant risk, immediate intervention required
- **10**: CRITICAL -- likely churning, executive escalation needed

## Phase 4: Intervention Recommendations

For each client at or above `alert_threshold`, generate recommendations:

| Risk Tier | Recommended Action |
|-----------|-------------------|
| WATCH (4-5) | Schedule casual check-in call, share a quick win or insight |
| ELEVATED (6-7) | Schedule strategy session, present new value (audit, report), address specific concerns |
| HIGH (8-9) | Executive-level outreach from founder, prepare retention offer, address root causes directly |
| CRITICAL (10) | Immediate call from founder, prepare save plan with concessions if warranted, document lessons |

For each recommendation, draft a brief outreach message using `message-generator`:
- Tone: warm, proactive, value-first (not defensive)
- Content: specific to the detected signals
- CTA: concrete next step (meeting, call, review)

## Phase 5: Alert Report

```
CHURN RISK REPORT -- Week of [Date]
Scanned: N active accounts
---
CRITICAL (1):
  [Client] -- Score: 10/10
  Signals: [top 3 signals]
  Action: [recommendation]

HIGH (2):
  [Client] -- Score: 8.5/10
  Signals: [top 3 signals]
  Action: [recommendation]

ELEVATED (1):
  [Client] -- Score: 6.2/10
  Signals: [top 3 signals]
  Action: [recommendation]

WATCH (3):
  [Client] -- Score: 4.1/10
  [Client] -- Score: 4.0/10
  [Client] -- Score: 4.0/10

HEALTHY (8):
  All clear, no action needed.
---
Total at risk: N accounts
Estimated MRR at risk: INR [amount]
```

## Phase 6: Output

Return structured JSON:

```json
{
  "report_date": "2026-03-07",
  "lookback_weeks": 4,
  "accounts_scanned": 12,
  "alert_threshold": 5,
  "alerts": [
    {
      "client_name": "BrandX",
      "risk_score": 8.5,
      "risk_tier": "HIGH",
      "signals": {
        "engagement": {"score": 2.4, "flags": ["2 missed meetings", "10-day silence period"]},
        "financial": {"score": 2.0, "flags": ["Invoice 15 days overdue"]},
        "satisfaction": {"score": 1.5, "flags": ["Tone shift detected in last 3 emails"]},
        "competitive": {"score": 1.5, "flags": ["Hiring for Shopify developer role"]},
        "usage": {"score": 1.1, "flags": ["Report open rate dropped to 20%"]}
      },
      "top_signals": [
        "2 consecutive meetings cancelled",
        "Invoice 15 days overdue",
        "Hiring for in-house Shopify developer"
      ],
      "recommendation": {
        "action": "Executive outreach from founder",
        "urgency": "This week",
        "message_draft": "Quick note -- noticed we haven't connected in a couple weeks...",
        "next_step": "Schedule 30-min strategy call"
      },
      "mrr_at_risk": 75000,
      "contract_renewal_date": "2026-06-01",
      "days_until_renewal": 86
    }
  ],
  "summary": {
    "critical": 0,
    "high": 1,
    "elevated": 2,
    "watch": 3,
    "healthy": 6,
    "total_mrr_at_risk": 225000
  },
  "generated_at": "2026-03-07T09:00:00Z"
}
```

## Example Usage

**Trigger phrases:**
- "Run churn detection this week"
- "Which clients are at risk of churning?"
- "Check account health across all clients"
- "Is [client] showing churn signals?"
- "Weekly retention scan"
- "Flag at-risk accounts"
