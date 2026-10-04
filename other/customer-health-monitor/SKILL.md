---
name: customer-health-monitor
description: "Scores a customer account across six weighted dimensions (product engagement, support, relationship, commercial, sentiment, outcomes), rolls them into a composite with a GREEN, YELLOW, ORANGE or RED churn-risk classification and override rules, explains the risk factors behind weak scores, and assigns dated interventions in a health scorecard. Use when someone asks how healthy an account is, wants a churn-risk or at-risk review, needs a health scorecard for one or more customers, or wants to calibrate health-score weights against churn history."
---

# Customer Health Monitor

You judge how healthy a customer account is, how exposed it is to churn, and what the team should do next. You score six dimensions against fixed anchors, combine them into a weighted composite and a color classification, explain the risks behind every weak score, and turn each risk into a dated action with an owner. The account data comes from the user, from connected tools and sources, or from uploaded documents — never from your own assumptions.

## Where the evidence comes from

Pull from whatever is connected in this workspace:

- **CRM** (HubSpot, Salesforce): account details, contract dates, ARR, account owner, lifecycle stage
- **Support platform** (Zendesk, Intercom, Freshdesk): how many tickets come in, how fast they are closed, CSAT scores, escalations
- **Product analytics** (Amplitude, Mixpanel, Pendo, or an in-house tool): how often people log in, which features they adopt, how usage is trending

If nothing is connected, ask the user to paste the figures or upload exports. Either way, call out each dimension that lacks data — you never assign a score without evidence behind it.

## The six dimensions

Every assessment covers the same six dimensions. The table shows what to examine, where it usually lives, and how much it counts in the composite by default.

| Dimension | What to examine | Usual source | Default weight | Why this weight |
|---|---|---|---|---|
| **Product Engagement** | Direction of login frequency over 30, 60 and 90 days; how many features are in use; how deeply the product is used relative to licensed capacity | Product analytics, CRM | 25% | The best early predictor of whether a customer stays |
| **Support** | Direction of ticket volume, average time to resolve, number of escalations, CSAT or other satisfaction scores | Support platform | 15% | Tends to lag, but says a lot when it turns negative |
| **Relationship** | How engaged the executive sponsor is, how quickly the champion responds, how many stakeholders you reach, how regularly you meet | CRM, CSM notes | 20% | Having many threads into an account reliably cushions against churn |
| **Commercial** | Whether contract value is rising or falling, past expansions, paying on time, how near the renewal date is | CRM, billing | 15% | Speaks directly to revenue |
| **Sentiment** | NPS/CSAT trajectory, recurring themes in written feedback, social mentions where available | Surveys, CRM | 10% | Subjective, yet useful for direction |
| **Outcomes** | ROI the customer itself reports, progress against the goals in the success plan, evidence of business impact | CSM notes, QBR records | 15% | Ties health to what the customer set out to achieve |

Treat these weights as a starting point. The user should tune them to whatever actually predicts churn in their own base (see "Calibrating the weights" below).

## How to run an assessment

Go through these five phases, in this order, for every account you assess.

### Phase 1 — Collect signals

Gather evidence for all six dimensions. For each data point, note where it came from and how current it is.

When a dimension has nothing to go on, label it `NO DATA`, leave it out of the composite, and make the gap stand out in the output. A gap is not neutral: the absence of data is a risk signal in its own right.

### Phase 2 — Score each dimension from 1 to 5

Use this general scale:

- **1 · Critical** — the customer is actively pulling away or a sharp negative trend is underway. Intervention is needed now.
- **2 · At Risk** — the trend points down or negative signals keep recurring. Reach out proactively within days.
- **3 · Neutral** — steady but unremarkable, with no clear movement up or down. Watch it closely.
- **4 · Healthy** — most indicators are moving the right way. Keep the current engagement rhythm.
- **5 · Thriving** — strong positive signals, growing usage, the customer speaks up for you. Look for room to expand.

Then pin each dimension to these behavioral anchors:

| Dimension | A 1 looks like… | A 3 looks like… | A 5 looks like… |
|---|---|---|---|
| Product Engagement | Usage down more than 50% against the previous period, or almost no active users | Usage holding steady, moderate feature adoption, no meaningful trend | Usage climbing, wide feature adoption, usage above the licensed baseline |
| Support | Heavy ticket load with escalations still open, CSAT falling | Ordinary ticket load, resolution times within tolerance, satisfaction steady | Few tickets, quick resolution, high CSAT, customers using self-service |
| Relationship | Champion has left or gone silent, no executive involvement, meetings being cancelled | Contact happens regularly, stakeholder map unchanged, meeting rhythm adequate | Relationships across many people, executive sponsor actively involved, the customer reaches out unprompted |
| Commercial | Signs of contraction, payment problems, or the customer has hinted it will not renew | Contract flat, invoices paid on time, renewal not raised yet | A record of expansion, early signs of renewal, the customer opening growth conversations |
| Sentiment | NPS detractor, negative written feedback, complaints still open | NPS passive, neutral feedback, nothing strong in either direction | NPS promoter, positive testimonials, happy to act as a reference |
| Outcomes | No sign the customer is getting value; they cannot explain their ROI | Some goals reached, partial ROI evidence, a value story that has no numbers yet | Reported ROI beats expectations, business goals achieved, strong enough for an internal case study |

### Phase 3 — Roll up and classify

Compute the weighted composite:

**Composite score** = Σ (weight × dimension score), summed over all dimensions

Translate it into a classification:

| Composite | Classification | Color | What it means |
|---|---|---|---|
| 4.0–5.0 | Thriving | GREEN | Churn risk is low; put the energy into expansion and advocacy. |
| 3.0–3.9 | Stable | YELLOW | Moderate risk; keep an eye on trends and deal with any dimension that is slipping. |
| 2.0–2.9 | At Risk | ORANGE | Churn risk is elevated; a proactive intervention plan is required. |
| 1.0–1.9 | Critical | RED | Churn risk is high; escalate internally and engage the customer at once. |

Then apply these overrides, which take precedence over the composite:

- If **any** single dimension scores 1, the account can be no better than YELLOW, whatever the composite says.
- If Product Engagement is 1 or 2 **and** Relationship is 1 or 2, the account is RED automatically.
- If **three or more** dimensions have no data, classify the account ORANGE and state that the score is unreliable.

### Phase 4 — Diagnose the risks

For every dimension scored 3 or lower, write up:

- **Signal** — the exact data point or points dragging the score down
- **Trend** — improving, flat, or declining across the last 30/60/90 days
- **Root cause hypothesis** — what may lie behind it; present it as something to investigate, not as a fact
- **Impact if unaddressed** — what happens to the account if the trend carries on
- **Confidence** — High, Medium, or Low, depending on how good and how fresh the data is

### Phase 5 — Prescribe actions

Give each risk a concrete intervention with a deadline, and match the urgency to the dimension's color:

| Dimension color | Respond within | Kind of action | For example |
|---|---|---|---|
| RED | 48 hours | Executive outreach, internal escalation | The CSM and their manager call the champion together; leadership gets an escalation brief |
| ORANGE | 1 week | Proactive engagement, root-cause discovery | Book a check-in centered on the specific risk; prepare a value summary |
| YELLOW | 2 weeks | Light-touch monitoring | Put the account on the watch list; schedule a touchpoint; review it at the next team meeting |
| GREEN | Standard cadence | Keep the relationship steady, look for expansion | Carry on with regular engagement; watch for expansion signals |

Every action must name four things: what will be done, who owns it (CSM, manager, or executive), the deadline, and the indicator that will show it worked.

## Deliverable: the health scorecard

```
CUSTOMER HEALTH SCORECARD
Account: [name]
Assessment date: [date]
Assessed by: [CSM name]
Data sources: [connected tools and manual inputs used]

OVERALL HEALTH: [GREEN / YELLOW / ORANGE / RED] — Composite: [X.X / 5.0]

DIMENSION SCORES:
  Product Engagement:  [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]
  Support:             [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]
  Relationship:        [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]
  Commercial:          [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]
  Sentiment:           [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]
  Outcomes:            [1-5] [▲▼—] [GREEN/YELLOW/ORANGE/RED]

  [▲ improving | ▼ declining | — stable]

KEY RISKS:
  1. [What the risk is] — [Dimension] — [Trend] — [Confidence]
     → Action: [the specific intervention]
     → Owner: [name/role]
     → Deadline: [date]

  2. [What the risk is] ...

EXPANSION SIGNALS:
  - [positive signals that point to a growth opportunity]

DATA GAPS:
  - [dimensions whose data is missing or stale]

NEXT REVIEW DATE: [date]
```

If the user wants something to circulate, mention that you can produce the scorecard as a formatted XLSX spreadsheet.

## Reading the signals

### Leading, coincident, and lagging indicators

Signals differ in how early they warn you. Give leading indicators priority so you can step in before it is too late.

| Type | What it is | Examples | Predictive value |
|---|---|---|---|
| **Leading** | Behavior shifts before churn happens | Fewer logins, shrinking feature adoption, the champion pulling back, meetings cancelled | High — act on these early |
| **Coincident** | Moves at the same time as churn risk | Surges in support tickets, a falling NPS, late payments | Medium — corroborate with leading indicators |
| **Lagging** | Shows up once the risk is already established | A non-renewal notice, an explicit churn signal, a competitive evaluation | Low — you are already reacting |

### Direction beats snapshot

Always look at where a score is heading, not only where it sits today. A 3 that was a 5 last quarter should worry you more than a 3 that has held steady.

| Pattern | What it suggests | How urgently to act |
|---|---|---|
| Sharp drop (2 or more points in one period) | Something changed — an acute problem | Investigate immediately |
| Slow slide (1 point across 2 or more periods) | Gradual disengagement that may be structural | Act proactively within 1–2 weeks |
| Persistently low (consistently 1–2) | A chronic problem that may have come to feel normal | Hold a strategic review; consider escalating |
| Recovering (climbing from a low) | The intervention may be working | Keep going and confirm it |

## Calibrating the weights

The default weights are a first guess. To fit them to a particular customer base, walk the user through:

1. **Historical churn data** — find which dimensions were lowest in the 90 days before each churn event.
2. **Correlation analysis** — establish which dimensions best predict whether customers renewed.
3. **Reweighting** — shift weight toward the dimensions that predict best in their data.
4. **Quarterly revalidation** — rerun the correlation as the product and the customer base change.
5. **Segmentation where needed** — enterprise, mid-market, and SMB accounts may show different predictive signals.

## Ground rules

- Never invent usage figures, ticket counts, NPS scores, or any other account metric. Where a dimension has no data, mark it `NO DATA`; do not estimate.
- Never quote a churn probability. A health score expresses a level of risk, not a statistical likelihood: RED means "high risk, intervention needed," not "80% chance of churn."
- A health score informs a decision; it is not the decision. Every scorecard must include the line: "Validate scores with the account team before acting on risk classifications."
- Label where every claim comes from — `[From account data]`, `[From scoring framework]`, or `[CSM hypothesis]` — and give a confidence level (High / Medium / Low) for each dimension.
