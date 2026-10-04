---
name: metrics-anomaly-investigator
description: "Investigate metric anomalies — build a ranked hypothesis framework and stakeholder narrative from a plain-language description. Use when a dashboard number drops or spikes unexpectedly. Triggers: 'investigate metric anomaly', 'my metric dropped', 'расследуй аномалию метрики', 'у меня упала метрика'."
version: 1.0.0
---

# Metrics Anomaly Investigator

This skill takes a plain-language description of a metric anomaly (metric name, time period, delta, and any available context) and produces a structured investigation framework with ranked hypotheses and a ready-to-send stakeholder narrative. No database access or code required — designed for product managers working in Cowork.

**Input:**
- Free-form description of the anomaly: metric name, observed period, magnitude of change, and any context (recent releases, campaigns, external events)

**Output:**
- Markdown response with Anomaly Summary, Investigation Framework table, Priority Checks, and Draft Stakeholder Narrative

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user provided at minimum:
   - A metric name (or description of what was measured)
   - An observed change (delta, direction, or time period)
   - If either is missing: stop and respond: "To investigate the anomaly I need at minimum: (1) metric name, (2) time period, (3) observed change. Please provide these details." Do not generate a framework.

2. If the input is vague (e.g., "our metrics are bad" with no specific anomaly):
   - Ask the user to identify one specific metric and its observed change before proceeding.

3. Note what context is available:
   - Recent product changes, feature releases, or experiments
   - Marketing campaigns or traffic source changes
   - Seasonality or external events
   - Related metrics (correlated changes)
   - If no context provided: proceed, flag assumptions explicitly in output, and add a closing line at the end of the response asking the user to share any recent product changes, campaigns, or external events that may be relevant.

### Step 2: Classify the Anomaly

1. Determine the anomaly type:
   - **Direction:** spike (unexpected increase) vs. drop (unexpected decrease)
   - **Shape:** sharp (1–2 day change) vs. gradual (trend over days/weeks)
   - **Scope:** isolated (single metric) vs. correlated (multiple metrics moving together)

2. If the user describes a gradual trend: note that short-term hypotheses (e.g., tracking bug, one-off event) are lower priority; focus on structural factors.

3. If multiple metrics changed simultaneously: reframe as a systemic investigation and add cross-metric hypotheses.

### Step 3: Generate Investigation Framework

Generate 5–7 ranked hypotheses covering four investigation axes:

**Axis 1 — Data / Tracking issues** (always include, check first)
- Tracking code broken or missing on key pages
- Metric definition or aggregation logic changed
- Data pipeline delay or processing error
- Segment filter or attribution window changed

**Axis 2 — Product changes**
- Feature release or rollback in the relevant period
- A/B test or experiment affecting the metric
- UI change affecting user flow
- Pricing or access change

**Axis 3 — External / Traffic factors**
- Organic traffic source change (SEO, social, referral)
- Marketing campaign launched or paused
- Competitor action, press coverage, or viral event
- Platform algorithm change (App Store, Google, social)

**Axis 4 — User behaviour shifts**
- Seasonal pattern or day-of-week effect
- User cohort mix shift (new vs. returning users ratio)
- Device or geography mix change
- Onboarding or activation funnel change upstream

For each hypothesis:
- Assign likelihood: **High / Medium / Low** (based on context provided)
- Specify one concrete validation step

### Step 4: Identify Priority Checks

1. Select the top 2–3 hypotheses most consistent with the provided context.
2. For each, write one sentence explaining why this is a priority given the specific anomaly described.
3. If no context was provided: default priority order is Data/Tracking → Product changes → External factors → Behaviour shifts.

### Step 5: Draft Stakeholder Narrative

Write a 5–8 sentence narrative in Slack/email format covering:
- What happened (metric, period, magnitude)
- Current status of investigation (just started / hypotheses identified / root cause found)
- Top hypotheses being checked
- Next steps and who is responsible (use placeholder [owner] if not specified)
- ETA for the next update

**Edge Cases:**

- If anomaly is a gradual trend (weeks): prioritise structural hypotheses (cohort mix, SEO, product flow); downweight single-event hypotheses.
- If multiple metrics changed: add a "Correlated pattern" note to the Anomaly Summary; include cross-metric hypotheses in the framework.
- If delta is small (<5%): note that significance depends on baseline variance; prioritise Data/Tracking hypotheses first.
- If no context provided: proceed with full hypothesis set and explicitly state "No context provided — all four axes are equally prioritised." At the end of the response, add: "To help narrow down the hypotheses, please share any recent product changes, campaigns, or external events that occurred around the time of the anomaly."

---

## Negative Cases

- **No metric name or delta:** Do not generate a framework. Respond with a clear request for the minimum required information.
- **Input is only "metrics are bad" or similarly vague:** Ask the user to name one specific metric and its observed change before proceeding.

---

## Output Format

```markdown
## Anomaly Summary
- **Metric:** [metric name]
- **Period:** [time range]
- **Change:** [delta — e.g., "-23% vs. prior week"]
- **Type:** [spike / drop] — [sharp / gradual] — [isolated / correlated]
- **Context provided:** [summary of user-provided context, or "none"]

---

## Investigation Framework

| # | Hypothesis | Axis | Likelihood | How to validate |
|---|-----------|------|------------|-----------------|
| 1 | [hypothesis] | Data/Tracking | High | [specific check] |
| 2 | [hypothesis] | Product | Medium | [specific check] |
| 3 | [hypothesis] | External | Low | [specific check] |
| ... | | | | |

---

## Priority Checks

1. **[Hypothesis name]** — [1 sentence: why this is most consistent with the described anomaly]
2. **[Hypothesis name]** — [1 sentence rationale]
3. **[Hypothesis name]** — [1 sentence rationale]

---

## Draft Stakeholder Narrative

**To:** [channel / team]
**Status:** Investigating

We noticed [metric] [dropped/increased] by [delta] over [period]. We are currently investigating the root cause and have identified [N] hypotheses. The most likely causes are [top 2 hypotheses]. [Owner] is checking [specific validation steps] and we expect initial findings by [timeframe]. We will share an update by [date/time]. No action required from your side at this stage.
```
