---
name: dt-obs-predictive-analytics
description: Predictive analytics for Dynatrace — time series forecasting with the timeseries-forecast tool, capacity saturation planning, trend and anomaly detection across hosts, services, and infrastructure.
license: Apache-2.0
---

# Predictive Analytics Skill

Forecast resource saturation, detect trends, analyze anomalies, and characterize signal behavior using DQL and Dynatrace analyzer tools.

## Analysis Disciplines

| # | Discipline | Use when … |
|---|------------|-----------|
| 1 | **Forecast and Prediction** | Predicting future metric values for capacity planning, cost estimation, or proactive alerting |
| 2 | **Detecting Changes** | A metric *shifted* — find when the character of the signal changed, regardless of whether it crossed a limit |
| 3 | **Detecting Violations** | A metric is *currently out of bounds* — find entities that exceed or fall below an acceptable range |
| 4 | **Timeseries Characteristics** | Characterizing a signal's seasonality, noise level, and trend before further analysis |

---

## Choosing the Right Detection Tool

**The single most important decision**: are you asking "did this metric *change*?" or "is this metric *currently wrong*?"

| Question | Tool | Why |
|----------|------|-----|
| "Did this metric change in the last N hours?" | `timeseries-novelty-detection` | Detects *when* the signal's character changed (spike, step, trend onset, variability shift) without requiring a known acceptable limit |
| "Which services spiked or dropped recently?" | `timeseries-novelty-detection` with `SPIKE` / `CHANGE_IN_VALUES` | Finds the specific entities and timestamps where change occurred; returns empty for stable signals |
| "When did CPU start trending up?" | `timeseries-novelty-detection` with `TREND_IN_VALUES` | Pinpoints the onset of a directional shift |
| "Which hosts are currently above 90% CPU?" | `static-threshold-analyzer` | Known fixed limit — fire alerts when exceeded | Can also be done with standard DQL queries, but the tool provides built-in violation counting, sliding window and alerting logic |
| "Which services are currently above their usual load?" | `adaptive-anomaly-detector` | Learns the normal distribution from the data and flags sustained threshold violations |
| "Which services are high right now vs. their weekly pattern?" | `seasonal-baseline-anomaly-detector` | Accounts for time-of-day/day-of-week patterns before deciding what is anomalous |

### Decision rule in plain language

- **Use `timeseries-novelty-detection`** when the question contains "changed", "shifted", "spiked", "dropped", "started", "when did", or "did anything unusual happen". The tool answers *whether* a change occurred and *when*. It requires no predefined threshold.
- **Use an anomaly detector** (`adaptive`, `seasonal`, or `static`) when the question is about *ongoing* or *current* state relative to an expected range: "which are highest", "who is violating", "what is above X". These tools count violation samples inside a sliding window — they confirm *how long* something has been bad, not whether the signal changed.

> **Pitfall**: Running `adaptive-anomaly-detector` on a broad fleet to answer "which service changed load?" typically flags every service that has *any* variation, producing low-signal results. Use `timeseries-novelty-detection` first to identify entities where the load character genuinely shifted, then use the anomaly detectors to measure the severity of those specific signals.

## When to Use This Skill

- **Capacity**: "Which hosts will hit 90% CPU in the next 30 days?"
- **Forecast**: "Forecast service request volume for the next 7 days"
- **Trend**: "Is memory usage growing across our Kubernetes nodes?"
- **Anomaly**: "Which services have unusual error rates right now?"
- **Baseline**: "How does today's traffic compare to last week?"
- **Signal profile**: "Is this metric seasonal or trending before I set up alerting?"

---

## Important Constraints

**Dynatrace Forecast Analyzer supports univariate forecasting only** — predicting one metric based on its own historical values. Multivariate forecasting (using multiple metrics as inputs) requires external tools (Python, R, Azure AutoML).

**Tooling Rule**: Run analyses using Dynatrace tools: `timeseries-forecast`, `adaptive-anomaly-detector`, `seasonal-baseline-anomaly-detector`, `static-threshold-analyzer`, and `timeseries-novelty-detection`. Use `execute-dql` for DQL queries.

**Result Analysis Rule**: Always analyse and summarise results directly from the raw tool output. Derive all numbers, trends, and conclusions inline.

---

## Result Presentation Format

Always present forecast results as a structured table:

| Column | Content |
|--------|---------|
| Rank | 🥇 🥈 🥉 ordered by urgency or magnitude |
| Signal / Entity | Metric name and entity or dimension |
| Last Actual | Most recent non-null value from the historical series |
| Forecast | Point forecast at the end of the horizon |
| Range | Lower – Upper confidence band at the same horizon point |
| Trend | % change from Last Actual to Forecast: 🔴 >+20% / 🟠 +5–20% / 🟢 ±5% stable / 🔵 −5–20% declining / ⚫ <−20% sharp drop |
| Action | ✅ No action / ⚠️ Monitor / 🔴 Act now |

Always follow the table with a **Key Findings** section (3–5 bullet points, ranked by priority).

---

## Core DQL Techniques

DQL has no native `forecast` function. For forward-looking forecasts, use `timeseries-forecast` (see `references/forecasting-analyzer.md`).

### Key DQL Rules

1. `timeseries` returns arrays — one value per time slot per entity
2. `arrayLast(arr)` = most recent value; `arrayFirst(arr)` = oldest
3. Growth = `(arrayLast - arrayFirst) / number_of_intervals`
4. Always `filter isNotNull(field)` before sorting to avoid null ordering issues
5. Use `toLong()` when dividing `Long` fields to avoid type errors
6. Use `dt.smartscape.*` not deprecated `dt.entity.*` in DQL display fields; use `dt.smartscape.*` in `by:{}` grouping clauses for entity-level queries

---

## Standard Query Patterns

### Moving Average Trend

```dql
timeseries cpu = avg(dt.host.cpu.usage), from: now()-24h, interval: 1h, by: {dt.smartscape.host}
| fieldsAdd moving_avg = arrayMovingAvg(cpu, 4)
| fieldsAdd current = arrayLast(cpu)
| fieldsAdd trend = arrayLast(cpu) - arrayFirst(cpu)
| filter isNotNull(current)
| sort trend desc
| limit 20
| fields dt.smartscape.host, current, trend, moving_avg
```

### Saturation Risk Classification

```dql
timeseries cpu = avg(dt.host.cpu.usage), from: now()-7d, interval: 1h, by: {dt.smartscape.host}
| fieldsAdd p95 = arrayPercentile(cpu, 95)
| fieldsAdd saturation_risk = if(p95 > 85, "HIGH", else: if(p95 > 70, "MEDIUM", else: "LOW"))
| filter isNotNull(p95)
| sort p95 desc
| fields dt.smartscape.host, p95, saturation_risk
```

### Days to Saturation Forecast

```dql
timeseries cpu = avg(dt.host.cpu.usage), from: now()-30d, interval: 1d, by: {dt.smartscape.host}
| fieldsAdd current = arrayLast(cpu)
| fieldsAdd daily_growth = (arrayLast(cpu) - arrayFirst(cpu)) / 30
| filter isNotNull(current)
| fieldsAdd days_to_saturation = if(daily_growth > 0, toLong((90 - current) / daily_growth), else: 9999)
| sort days_to_saturation asc
| limit 20
| fields dt.smartscape.host, current, daily_growth, days_to_saturation
```

### Anomaly Scoring

```dql
timeseries cpu = avg(dt.host.cpu.usage), from: now()-24h, interval: 1h, by: {dt.smartscape.host}
| fieldsAdd baseline_avg = arrayAvg(cpu)
| fieldsAdd current = arrayLast(cpu)
| fieldsAdd anomaly_score = if(isNotNull(current) and isNotNull(baseline_avg), abs(current - baseline_avg), else: 0)
| sort anomaly_score desc
| limit 20
| fields dt.smartscape.host, current, baseline_avg, anomaly_score
```

### Metric Discovery

Before forecasting, discover available metrics by keyword:

```dql
metrics from: now() - 1h
| filter contains(metric.key, "cpu")
| summarize count(), by: {metric.key}
| sort `count()` desc
```

---

## Reference Guides

- **`references/forecasting-analyzer.md`** — `timeseries-forecast` tool:
  data requirements, parameter reference, interval selection, horizon limits, common pitfalls
- **`references/capacity-forecasting.md`** — CPU/memory/disk/K8s saturation
  forecasts; multi-resource risk scoring; days-to-saturation DQL patterns
- **`references/anomaly-scoring.md`** — `adaptive-anomaly-detector`, `seasonal-baseline-anomaly-detector`,
  `static-threshold-analyzer`; DQL deviation scoring
- **`references/novelty-detection.md`** — `timeseries-novelty-detection` tool: spike, drop, step change,
  trend onset, and variability change detection; all novelty types; parameter reference; worked examples
- **`references/trend-detection.md`** — `timeseries-novelty-detection` for trend onset and change points;
  week-over-week joins; growth rate and acceleration detection

## Related Skills

- **dt-dql-essentials** — DQL syntax, `timeseries` command rules, array function reference
- **dt-obs-hosts** — Host and process metrics catalog
- **dt-obs-services** — Service RED metrics for service-level trend analysis
- **dt-obs-problems** — Davis AI problem history for anomaly correlation
