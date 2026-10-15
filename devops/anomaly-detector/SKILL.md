---
name: "anomaly-detector"
description: "Automated metric anomaly detection and root cause correlation for the Operations department. Monitors system metrics for deviations, correlates anomalies across services, generates alert recommendations, and feeds the ops self-improvement loop. Use when investigating metric spikes, tuning alert thresholds, reducing false positives, or running the operations UAOP pipeline."
risk: low
tags: [operations, monitoring, observability, alerting]
created: 2026-03-23
updated: 2026-03-23
---

# Anomaly Detector — Operations Intelligence Engine

Automated metric anomaly detection that reduces alert fatigue and catches real problems. UAOP Stage 1 + Stage 5 for Operations.

## When to use

- Investigating a metric spike or deviation
- Tuning alert thresholds to reduce false positives
- Post-incident — "what signals did we miss?"
- Capacity planning — "what's trending toward limits?"
- Weekly ops review — "what's abnormal this week?"

## When NOT to use

- Active incident response (use `production-monitoring` + `incident-responder`)
- Infrastructure changes (use `devops-patterns`)
- Cost analysis (use `cost-optimization`)

## Pipeline

### Step 1: Collect Baseline Metrics

Establish normal ranges for key metrics:

```
SERVICE METRICS (per service):
  - Request rate (req/s) — normal range by hour/day
  - Error rate (%) — normal baseline
  - Latency p50/p95/p99 (ms) — normal range
  - CPU/Memory utilization (%) — normal range
  - Connection pool usage (%) — normal range

INFRASTRUCTURE METRICS:
  - RDS connections active/available
  - Redis memory usage / eviction rate
  - ECS task count / desired vs running
  - Disk I/O / network throughput

BUSINESS METRICS:
  - API key usage patterns
  - Agent execution rate
  - Pipeline stage completion times
```

### Step 2: Detect Anomalies

Apply detection methods:

```
DETECTION RULES:
  Threshold: metric > X for > Y minutes
  Rate of change: metric changed >Z% in T minutes
  Statistical: metric > 2 standard deviations from rolling 7-day average
  Absence: expected metric stopped reporting
  Ratio: error_rate / request_rate > threshold
  Correlation: when metric A spikes AND metric B drops simultaneously
```

### Step 3: Correlate and Triage

```markdown
## Anomaly Report

**Detected:** [timestamp]
**Metric:** [metric name]
**Value:** [current] vs [expected range]
**Deviation:** [X]% above/below normal
**Duration:** [how long anomalous]

### Correlated Signals
| Time | Metric | Value | Normal Range | Correlation |
|------|--------|-------|-------------|-------------|
[other metrics that moved at the same time]

### Probable Root Cause
Based on correlation analysis:
1. [Most likely cause + evidence]
2. [Second most likely + evidence]

### Recommended Action
- Severity: [P0/P1/P2/P3]
- Action: [specific steps]
- Escalation: [who to notify if unresolved in X minutes]

### False Positive Check
- Is this a known pattern? [deploy window / batch job / expected spike]
- Has this threshold fired falsely before? [history]
- Confidence: [HIGH/MEDIUM/LOW]
```

### Step 4: Self-Improvement Loop

```
MEASURE:
  - Alert-to-incident ratio (alerts that were real problems)
  - False positive rate per alert rule
  - MTTD (mean time to detect real issues)
  - Anomalies missed (found in postmortem, not by detector)

REINFORCE:
  - Alert rules with high true-positive rate → keep and tighten
  - Alert rules with >10% false positive rate → retune or remove
  - Correlation patterns that identified root cause → promote

REGENERATE:
  - Update baselines as system evolves
  - Add new metrics when new services deploy
  - Adjust thresholds seasonally (traffic patterns change)
  - Feed postmortem findings into detection rules
```

## Cadence

```
CONTINUOUS: Metric collection and threshold monitoring
DAILY:      Anomaly summary (what deviated from normal)
WEEKLY:     False positive review + threshold tuning
MONTHLY:    Detection effectiveness review + baseline recalibration
```

## Agents

| Agent | Role |
|-------|------|
| performance-engineer (L2) | Owns monitoring strategy |
| observability-engineer (L3) | Configures detection rules, tunes thresholds |
| incident-responder (L4) | Acts on detected anomalies |
| performance-optimizer (L5) | Analyzes trends, recommends capacity changes |
| root-cause-analyst (L5) | Investigates correlated anomalies |

## Tools

| Tool | Purpose |
|------|---------|
| kubernetes MCP | Cluster metrics, pod status |
| github MCP | Deploy history (correlate anomalies with changes) |
| sequential MCP | Multi-step correlation reasoning |
| memory MCP | Store baselines, known patterns, false positive history |
