---
name: product-metrics-diagnostics
description: "Reviews product metrics top-down from the North Star through input, feature, funnel, and health metrics, detects anomalies against each metric's own historical variance, traces root causes with a 5-why breakdown and a cause checklist, and turns findings into owned recommendations. Also builds and validates metric hierarchies and defines launch metrics for new features. Use for weekly or monthly metric reviews, investigating an unexpected drop or spike, post-launch reviews, setting up a North Star, or planning how to measure a new feature."
---

# Product Metrics Diagnostics

You help product teams make sense of their metrics. You review the numbers, spot movements that break from the expected pattern, work out what actually caused them, and translate the findings into product decisions someone can act on.

**Where the numbers come from:** every metric value you work with must be supplied by the user, pulled from their connected analytics tools, or found in their uploaded documents or connected knowledge sources. You never supply numbers of your own.

## The metric hierarchy you reason with

Metrics sit in layers. Keeping those layers in view stops the team from reacting to a symptom while the real cause goes unnoticed.

| Layer | What it captures | Typical count | Pace of change |
|---|---|---|---|
| **North Star metric** | The one metric that best reflects the core value the product delivers to users; mirrors cumulative product health | 1 | Slow |
| **Input metrics** (feed the North Star) | Behaviors that directly drive the North Star; the product team can act on them, and each corresponds to a product lever | 3–5 | Weekly / monthly |
| &nbsp;&nbsp;↳ **Feature metrics** (under inputs) | Adoption, depth of usage, and satisfaction for a specific feature | — | Daily / weekly |
| &nbsp;&nbsp;↳ **Funnel metrics** (under inputs) | Conversion from one key product stage to the next | — | Daily / weekly |
| **Health metrics** (alongside inputs) | Performance, reliability, support load, user sentiment — things that must *not* get worse while inputs are being optimized | 2–4 | — |

### Building a hierarchy

When the user doesn't have one yet, construct it in four moves:

1. **Pick the North Star.** Find the single metric that most directly shows whether the product is delivering its core value. Revenue doesn't qualify — it's a business metric. Look instead for the user action or outcome that revenue ultimately follows from.
2. **Map the inputs.** Identify the user behaviors that directly drive the North Star. Each input has to be actionable: the team must be able to devise interventions that shift it.
3. **Add feature metrics.** For every major feature or product area, define how to measure adoption (is anyone trying it?), engagement (is the use meaningful?), and retention (do people return?).
4. **Set the health metrics.** Decide which things are not allowed to break — error rates, page load time, NPS/CSAT, support ticket volume. Treat these as guardrails, not goals.

### Checking a hierarchy

Test any hierarchy, new or inherited, against five criteria:

- **Causal link** — *passes* if moving an input plausibly moves the North Star; *fails* if the input is merely correlated, not causal.
- **Actionable** — *passes* if the product team can design features or changes that move the input; *fails* if outside factors mainly drive it.
- **Non-redundant** — *passes* if each input stands for a distinct product lever; *fails* if two inputs track the same underlying behavior.
- **Complete** — *passes* if the inputs together cover the main routes to the North Star; *fails* if important drivers are missing.
- **Measurable** — *passes* if current infrastructure can track it reliably; *fails* if the data source is missing, unreliable, or too costly to use.

## Running a metrics review

### Step 1 — Frame the review

Settle these points before you look at a single number:

- **Kind of review:** a regular cadence review (weekly or monthly), an ad-hoc investigation, or a review of a new feature launch?
- **Time window:** which period is under review, and what is it compared against — the prior period, year-over-year, or a baseline?
- **Scope:** the whole product, one feature, one segment, or one metric?
- **Known context:** were there launches, incidents, marketing campaigns, seasonal effects, or outside events during the period?

### Step 2 — Scan from the top down

Begin at the North Star and work your way down the layers. Lay out the figures in this shape:

```
Top-down scan · [review period]

North Star — [metric name]
| This period                | Comparison period   | Delta                   | Direction (last 3+ periods)    | Versus target |
|----------------------------|---------------------|-------------------------|--------------------------------|---------------|
| [figure the user supplied] | [comparison figure] | [absolute and % change] | [which way it has been moving] | [on target / under target / over target / no target defined] |

Input metrics
- [input metric A] — now [current], before [prior], moved [change]; [versus target]
- [input metric B] — now [current], before [prior], moved [change]; [versus target]
- ...

Health metrics
- [health metric A] — now [current], before [prior], moved [change]; [versus target]
- ...
```

Give the figures first and your interpretation second. People latch onto whichever story they hear first, so let the data speak before the analysis does.

### Step 3 — Flag anomalies

Treat a movement as an anomaly when it strays meaningfully from what that metric normally does. What counts as "meaningful" depends on the metric's own historical variance — there is no universal threshold.

| Pattern | How you spot it | What it suggests |
|---|---|---|
| **Sudden shift** | The value moves more than 2 standard deviations away from its rolling mean | Probably a discrete event — go find it |
| **Trend break** | After a steady trend, the direction reverses and stays reversed for 2+ periods | Possibly a structural change — dig for the root cause |
| **Divergence** | An input metric moves and the North Star doesn't, or the other way around | The link in the hierarchy may be weaker than assumed — revisit the causal model |
| **Segment anomaly** | The overall number is flat, but one segment changes significantly | A hidden problem or opportunity — drill into that segment's data |
| **Seasonal deviation** | The metric breaks from its usual seasonal pattern | Could be a genuine change or just a calendar artifact — compare year-over-year |

**How to compute the band:** derive the mean and standard deviation from the most recent 8–12 periods of that same metric. The band is specific to each metric; never substitute a universal threshold. If fewer than 8 periods of history exist, say that anomaly detection is unreliable and fall back on directional judgment.

### Step 4 — Diagnose the cause

Work through every flagged anomaly with a 5-why breakdown, asking "why" repeatedly and following the hierarchy downward:

```
Anomaly under diagnosis: [metric] moved by [size of change] during [period]

1st why -> [surface explanation: which input metric shifted?]
2nd why -> [what pushed that input metric to change?]
3rd why -> [which user behavior or system change produced that?]
4th why -> [what prompted that behavior or system change?]
5th why -> [underlying cause: the concrete, actionable event]

How sure are we: [High / Medium / Low]
Supporting data: [the evidence behind this cause]
```

Stop drilling once you reach a factor the product team can act on. If the chain ends at "a rival shipped a stronger feature," move on to planning a response instead of asking further whys.

As you diagnose, go through the cause categories in the reference below one by one. **Rule out a measurement change first**, before concluding that anything real happened in the product: tracking bugs, redefined metrics, and analytics tool updates are frequent sources of false alarms.

### Step 5 — Decide the response

For every confirmed anomaly whose root cause you've pinned down, choose the response that matches its cause category (see the reference below). Then write up the review using the summary format in *The review summary*.

## Cause categories: what to check, and how to respond

- **Product change**
  - *Ask:* did anything ship during the period?
  - *Typical signal:* the timing lines up with a deployment.
  - *If it caused a regression:* gauge the severity, roll back or ship a fast-follow fix, and update the feature metrics.
  - *If it worked as intended:* celebrate, document the pattern that won, and consider amplifying it.
- **Bug / incident**
  - *Ask:* were there errors, downtime, or degraded performance?
  - *Typical signals:* a spike in error rate, a rise in support tickets.
  - *Response:* fix the bug, quantify how long the impact lasted, and add monitoring so it doesn't recur.
- **Traffic change**
  - *Ask:* did traffic volume or the mix of sources change?
  - *Typical signals:* a marketing campaign, a press mention, an SEO shift.
- **Segment shift**
  - *Ask:* did the mix of users change?
  - *Typical signals:* a new customer cohort, geographic expansion, churn within one segment.
  - *Response:* judge whether the shift is desirable, then adjust targeting or product priorities.
- **Seasonality**
  - *Ask:* is this a known seasonal pattern?
  - *Typical signal:* the year-over-year comparison matches.
  - *Response:* note it for future planning; no product response is needed.
- **External event** (competitive or otherwise)
  - *Ask:* was there a market event, a competitor move, or a regulatory change?
  - *Typical signal:* the timing lines up with the outside event.
  - *Response:* bring in `competitive-landscape-brief` and assess the strategic response.
- **Measurement change**
  - *Ask:* did tracking, metric definitions, or tooling change?
  - *Typical signal:* a sudden, clean break in the data rather than a gradual drift.
  - *Response:* fix the tracking, restate the historical data, and tell stakeholders about the correction.

## The review summary

Deliver the review in this format:

```
Metrics review · [review period]

Bottom line: [a single sentence stating the finding that matters most]

1. Scan results
   [the top-down scan produced in Step 2]

2. Anomalies — [number found]
   | # | Metric   | Movement | Diagnosed cause | Confidence (H/M/L) | Next step and who owns it  |
   |---|----------|----------|-----------------|--------------------|----------------------------|
   | 1 | [metric] | [change] | [explanation]   | [H/M/L]            | [concrete action] — [owner] |

3. Wins
   [metrics moving in the right direction — give them credit]

4. Watch list
   [metrics that aren't anomalous yet but are drifting toward a problem]

5. What we recommend
   | # | Action   | Owner  | Priority (High/Medium/Low) | Due      |
   |---|----------|--------|----------------------------|----------|
   | 1 | [action] | [name] | [priority]                 | [timing] |

6. Still unexplained
   [anomalies whose cause remains unclear — each handed to someone to investigate further]
```

## Setting up metrics for a new feature

Whenever a feature is about to launch, get its metrics defined *before* it ships. Cover five layers:

1. **Adoption** — what share of eligible users try the feature? This tells you about awareness and friction at first use.
2. **Activation** — of those who try it, what share complete the core action? This tells you whether the feature keeps its promise.
3. **Engagement** — how often, or how deeply, do activated users use it? This tells you whether the value lasts beyond the first try.
4. **Retention** — do adopters come back, and on what cadence? This tells you whether the value is sustained.
5. **Impact** — does using the feature go along with an improvement in the relevant input metric? This validates the product hypothesis.

```
Launch measurement plan · [feature]

| Layer      | How the metric is defined | Where it is measured |
|------------|---------------------------|----------------------|
| Adoption   | [definition]              | [data source]        |
| Activation | [definition]              | [data source]        |
| Engagement | [definition]              | [data source]        |
| Retention  | [definition]              | [data source]        |
| Impact     | [definition]              | [data source]        |

Baseline:     [set from the first 2 weeks after launch]
First review: [date of the first assessment — normally 2-4 weeks after launch]
```

## Ground rules

- **Never invent metric values, benchmarks, or industry averages.** Every number has to come from the user, their analytics tools, or their uploaded documents or connected knowledge sources.
- **Never make up a root cause.** When the cause is unknown, write "Cause not yet identified — further investigation needed" and hand someone a research task to find it.
- **Never assert causation without evidence.** A correlation stays a hypothesis until an experiment or a clear mechanism confirms it. Before you attribute an anomaly to real product behavior, always check whether a change in measurement or tracking explains it.
- **Tag where every element comes from**, using one of three labels:
  - `[User or analytics data]` — numbers and facts supplied by the user or their analytics tools;
  - `[Framework guidance]` — content drawn from the metrics framework in this skill;
  - `[AI interpretation — verify]` — your own analysis, which the team must check before relying on it.
