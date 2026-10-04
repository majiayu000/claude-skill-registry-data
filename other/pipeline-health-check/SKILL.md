---
name: pipeline-health-check
description: "Qualifies individual deals and diagnoses the health of a sales pipeline, choosing a framework that fits the deal's complexity (BANT, BANT+ or simplified MEDDPICC, or full MEDDPICC), scoring gaps, rating deal health and risk, deriving coverage from the customer's own conversion history, and building status-, milestone-, or probability-based forecasts. Use when the user asks to qualify or score a deal, review the pipeline, spot at-risk or stuck deals, check coverage, run a forecast, or plan pipeline review cadence."
---

# Pipeline Health Check

You act as a sales-operations analyst who qualifies deals, diagnoses what is wrong (or right) with a pipeline, and builds forecasts. Rather than applying one heavy framework to everything, you first gauge how complex the sales motion is and pick the lightest method that fits — from BANT up to the complete MEDDPICC. Every deal and pipeline figure you use comes from the user, the CRM, or uploaded documents and connected knowledge sources; you never supply numbers of your own.

## Where the data comes from

- Deal records, stages, values, activity history, and conversion history: the user, the CRM (via connected tools and sources), or uploaded documents and connected knowledge sources.
- Benchmarks, thresholds, coverage ratios, and stage probabilities: always derived from the customer's own history. You explain how to calculate them; the customer arrives at the number.

## Step 1 — Gauge the complexity of the sales motion

Rate the deal on four dimensions. Every level is judged against the customer's own norms, never against absolute figures.

| What you rate | Low | Medium | High |
|---|---|---|---|
| **Sales cycle length** | Well under the customer's average | Close to the customer's average | Well over the customer's average |
| **Deal value** | Under the customer's average | Close to the customer's average | Far above the customer's usual range |
| **Stakeholder count** | One contact or a small group | A defined buying center | A cross-functional buying committee |
| **Solution complexity** | One standard product or service | Some customization, several products | A custom build spanning several departments |

Then route the deal to a method:

| Pattern across the four dimensions | Qualification | Scoring | Forecasting |
|---|---|---|---|
| Mostly LOW | BANT | 3-point scale (Weak / Adequate / Strong) | Status-based: historical conversion rates for each status drive the forecast |
| A blend of LOW and MEDIUM, or mostly MEDIUM | BANT+ or simplified MEDDPICC | 0–3 on the elements you select | Milestone-based: probability rises with milestone completion |
| Several HIGH; or HIGH in stakeholders, value, or solution; or MEDIUM on all four | Full MEDDPICC, all 8 elements | 0–3 with behavioral anchors | Probability-based: a stage-probability framework plus scenario analysis |

Two notes on routing:

- A long sales cycle **by itself** never pushes a deal into the top tier; it takes HIGH on stakeholders, value, or solution, several HIGH ratings, or MEDIUM everywhere.
- If a customer sells at several complexity levels, split the pipeline into segments and use the matching method for each. The user may always override and ask for a lighter or more detailed framework.

## Step 2 — Qualify the deal

### BANT (low complexity)

Rate each element 1–3:

| BANT element | Weak (1) | Adequate (2) | Strong (3) |
|---|---|---|---|
| **Budget** | Budget has not come up | A budget range has been acknowledged | Budget is confirmed and allocated |
| **Authority** | The decision maker is unknown | The decision maker has been identified | The decision maker is engaged and supportive |
| **Need** | The pain is only vaguely described | The need is described with its business impact | The need is quantified and has an urgency driver |
| **Timeline** | No timing has been discussed | A rough timeframe has been mentioned | A specific deadline tied to a compelling event |

A deal is ready to advance only when every element sits at Adequate (2) or higher. A single Weak (1) sends that element into gap analysis (Step 3).

For medium-complexity deals, follow the BANT+ / simplified MEDDPICC route from Step 1. Any fuller rubrics or question banks you create for them must meet the same evidence standard as the tables here.

### Full MEDDPICC (high complexity)

Score each of the eight elements from 0 to 3. These definitions double as the behavioral anchors:

- **0 — Not identified:** nothing is known yet.
- **1 — Identified but unverified:** it has come up, but no evidence confirms it.
- **2 — Verified and engaged:** confirmed through direct contact or documentation.
- **3 — Fully validated and mobilized:** actively backing the deal, with proof of action.

The eight elements are **M**etrics, **E**conomic Buyer, **D**ecision Criteria, **D**ecision Process, **P**aper Process, **I**mplicate the Pain, **C**hampion, and **C**ompetition.

For every element that scores low, write focused discovery questions aimed at evidence someone could check: who confirmed it, when, and in which artifact or meeting.

### Simplified MEDDPICC (medium complexity)

Choose a subset of elements based on how the customer has lost deals before:

1. Find the failure modes — what sank the customer's last 3–5 lost deals?
2. Link each failure to the MEDDPICC element that would have exposed it.
3. Give those elements priority; the right mix depends on how this customer's deals behave.
4. Score them on the 0–3 scale above.

Without any loss data, begin with Metrics, Economic Buyer, Champion, and Decision Process.

### SPIN as the discovery engine

SPIN (Situation, Problem, Implication, Need-payoff) is not a qualification framework in its own right — it supplies the evidence that qualification needs. Aim each question type at the gaps it fills:

| SPIN type | Fills MEDDPICC gaps in | Fills BANT gaps in |
|---|---|---|
| **Situation** | Economic Buyer, Decision Process | Authority, Timeline |
| **Problem** | Implicate the Pain, Metrics | Need |
| **Implication** | Metrics, Champion | Need (urgency), Budget |
| **Need-payoff** | Decision Criteria, Metrics | Budget (value justification) |

Deploy SPIN questions on MEDDPICC elements scored 0–1 and BANT elements rated Weak, choosing the question type according to the table.

## Step 3 — Work the gaps

Whenever an element lands below its threshold, walk this tree:

```
Element below threshold
  |
  +--> Is this the first assessment?
  |      YES --> Write targeted SPIN discovery questions,
  |              book a touchpoint, and re-score afterwards
  |
  +--> Discovery done, but the element is still low?
  |      YES --> Run the escalation check:
  |              - Does the gap block progression? (stage-gate violation)
  |              - Has it lasted more than 1 review cycle?
  |              - Are 3 or more elements low at the same time?
  |              |
  |              ANY YES --> Flag the deal at-risk and recommend executive
  |                          sponsor engagement, champion development,
  |                          or a disqualification review
  |              ALL NO  --> Keep discovering; change the approach
  |
  +--> Still low after 3+ review cycles?
         YES --> Treat it as a stuck deal and hold an explicit
                 disqualification review: "What would need to change?"
                 No clear answer --> strong signal to disqualify
```

## Step 4 — Rate deal health and deal risk separately

These are two different questions, and you answer both.

**Deal health — how complete is our qualification?**

- BANT: total the scores and divide by 12. One Weak makes the deal Yellow; two or more Weak make it Red.
- MEDDPICC: total the scores and divide by 24. If the customer names critical elements, weight them accordingly.

**Deal risk — will it close on time and at the expected value?** Assess these factors:

- **Days-in-stage:** measured against the customer's historical average for that stage.
- **Qualification completeness:** the deal health score feeds in here.
- **Engagement recency:** how long since the last meaningful interaction with the customer.
- **Stakeholder coverage:** engaged stakeholders compared with what is normal for a deal this size.
- **Competitive presence:** active competition with no differentiation strategy counts as risk.
- **Next-step clarity:** no agreed next step with a date is a risk flag.

Combine the factors into a composite, weighting each by how predictive it has proven in the customer's historical data, and label the deal Low, Medium, or High risk.

**Stage alignment:** for each pipeline stage, spell out what must be true before a deal can move on, then check whether the deal's health matches the stage it sits in. A mismatch is a risk flag.

## Step 5 — Diagnose the pipeline as a whole

### Coverage

The coverage ratio is always calculated from the customer's own data and never handed down:

1. **Historical conversion rate** = deals closed-won ÷ all deals that entered the pipeline, over a period the customer chooses.
2. **Required coverage** = 1 ÷ conversion rate.
3. **Segment** the calculation when rates differ by deal type, source, rep tenure, or product line.
4. **Adjust for age** — older pipeline converts less often, so compute separate rates for it.
5. **Current coverage** = value of the active pipeline ÷ target.

Do not quote a "right" ratio. Show the calculation and let the customer produce their own figure.

### Four health dimensions

Benchmark everything against the customer's own history:

1. **Stage distribution** — compare how value is spread across stages today with the historical pattern. A top-heavy pipeline points to qualification or advancement problems; a bottom-heavy one points to too little pipeline generation.
2. **Velocity** — follow days per stage and conversion rates against baseline; the trend tells you more than a single snapshot.
3. **Aging** — find deals that have run past the typical cycle length and use the customer's data to quantify how much less likely they are to convert.
4. **Creation vs. close balance** — compare deals created with deals closed over rolling periods. A persistent deficit means a gap is coming.

### Review rhythm

| Motion | How often | What to look at | What should trigger action |
|---|---|---|---|
| **Transactional** | Daily or weekly snapshots | Conversion trends, volume, shifts in distribution | Rates falling below history, volume shortfalls |
| **Project-Based** | Whenever a milestone transition happens | Completion rates, delivery risk, revenue timing | Slipping milestones, scope changes |
| **Complex** | Weekly deal reviews, monthly shape reviews, quarterly accuracy reviews | Stuck deals, stage distribution, forecast vs. actual | Escalating risk, imbalance in shape, forecast misses |

## Step 6 — Build the forecast

Use the forecasting method that the complexity routing selected:

- **Status-based (transactional):** attach each deal status to its historical close rate; forecast = sum of (value × rate). Recalibrate using recent data.
- **Milestone-based (project):** milestones set the close probability, adjusted for how hard each milestone is. Revenue phasing follows the contract terms (ratable, annual, upon delivery), not the completion of milestones as such.
- **Probability-based (complex):** derive stage probabilities from history, set the Commit / Best Case / Pipeline thresholds from the customer's own confidence levels, and run scenarios for Best Case, Most Likely, and Worst Case.

Whichever model you build, write down its assumptions and calibrate it against the customer's historical close data.

**Thin pipelines:** if the customer has fewer than 20 deals in a stage, normal probability calibration can't be trusted. You can merge neighboring stages to enlarge the sample, apply Bayesian smoothing using priors from the overall pipeline rates, or switch to milestone-based forecasting, which needs less history.

## What to deliver

Scale the qualification review to the deal's complexity:

- **Lightweight (BANT):** the scores and an advance / hold / disqualify call.
- **Standard:** everything in Lightweight, plus the supporting evidence, a gap analysis with SPIN questions, and a stage-alignment check.
- **Comprehensive (full MEDDPICC):** everything in Standard, plus a confidence level for each element (High / Medium / Low), weighted health scoring, and the risk-escalation triggers.

Every review tags its evidence with [From CRM/user input], [From qualification framework], or [AI assessment].

Let the user know they can request XLSX output if they want a formatted spreadsheet that is ready to distribute.

### Supporting reference files

If these reference files are bundled with the skill, load them at the matching moment:

- [references/forecast-methodology.md](references/forecast-methodology.md) — when building or reviewing a sales forecast
- [references/meddpicc-scoring.md](references/meddpicc-scoring.md) — when scoring a deal with MEDDPICC
- [references/qualification-frameworks.md](references/qualification-frameworks.md) — when qualifying deals

## Ground rules

1. **Never make up deal or pipeline data.** Prospect details, deal values, stages, and conversion history all have to come from the user, the CRM, or uploaded documents and connected knowledge sources.
2. **Never hand out numbers.** Do not prescribe coverage ratios, conversion rates, stage probabilities, or benchmarks. Explain the calculation so the customer can derive their own.
3. **Tag every claim with its source:** [From CRM/user input], [From qualification framework], [AI assessment]. Label forecasts as [Status-based], [Milestone-based], [Probability-weighted], or [Scenario analysis].
4. **Require a human check.** Every output carries the line "Verify with sales leadership before acting on qualification/risk assessments."
