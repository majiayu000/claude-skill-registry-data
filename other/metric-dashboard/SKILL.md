---
name: metric-dashboard
description: "Design metric dashboards and KPI tracking plans for products and features. Defines what to measure, how to measure it, alert thresholds, and dashboard layout. Covers product, business, and technical metrics."
argument-hint: "[product, feature, or area to build metrics for]"
---

# Metric Dashboard Skill

Design a comprehensive metric dashboard and KPI tracking plan for any product or feature.

## When to Use
- User needs to define metrics for a new product or feature
- User is setting up monitoring and alerting
- User needs to design a dashboard layout
- User says `/metric-dashboard` followed by the product/feature
- Any time measurement strategy needs to be defined

## Framework: Metric Dashboard Design (5 Steps)

### Step 1: Define the Metric Hierarchy

**North Star Metric (NSM)**:
The single metric that best captures the value your product delivers.
- Must reflect user value, not just business value
- Must be measurable with current instrumentation
- Formula: NSM = [engagement unit] per [user segment] per [time period]

**Decompose into a metric tree:**
```
North Star Metric
├── Input Metric A (e.g., new users)
│   ├── Sub-metric A1
│   └── Sub-metric A2
├── Input Metric B (e.g., activation rate)
│   ├── Sub-metric B1
│   └── Sub-metric B2
└── Input Metric C (e.g., retention)
    ├── Sub-metric C1
    └── Sub-metric C2
```

### Step 2: Categorize Metrics

**Product Metrics:**
- Acquisition: How users find you (sign-ups, installs, registrations)
- Activation: First value moment (onboarding completion, first action)
- Engagement: Core usage (DAU/MAU, session length, feature adoption)
- Retention: Coming back (D1/D7/D30, cohort retention curves)
- Revenue: Monetization (ARPU, conversion, LTV, churn)

**Technical Metrics:**
- Performance: Latency (p50, p95, p99), throughput, error rate
- Reliability: Uptime, incident count, MTTR
- Infrastructure: CPU/memory utilization, cost per request

**AI/ML Metrics (if applicable):**
- Quality: Accuracy, hallucination rate, eval scores
- Safety: Content policy violation rate, false refusal rate
- Cost: Cost per inference, token usage
- Latency: Time to first token, tokens per second

**Business Metrics:**
- Revenue: MRR, ARR, revenue growth rate
- Unit economics: CAC, LTV, LTV/CAC ratio
- Market: Market share, competitive win rate

### Step 3: Set Targets & Alerts

For each metric, define:

| Metric | Current | Target | Alert Threshold | Owner |
|--------|---------|--------|----------------|-------|
| NSM | X | Y | Z | PM |
| Metric A | | | | |
| Metric B | | | | |

**Alert levels:**
- **Warning** (yellow): Metric trending below target — investigate
- **Critical** (red): Metric below threshold — immediate action required
- **Anomaly**: Unexpected spike or drop — auto-detect and notify

### Step 4: Design Dashboard Layout

**Executive Dashboard** (1 screen):
- NSM trend (last 30/90 days) — large, prominent
- 4-6 key metrics with sparklines and trend arrows
- Traffic light status (green/yellow/red) for each area
- Notable events annotated on the timeline

**Operational Dashboard** (detailed):
- Real-time metrics for the current day/hour
- Breakdowns by segment (platform, geography, user type)
- Funnel visualization (acquisition → activation → retention)
- Experiment results (A/B test outcomes)

**Technical Dashboard** (if applicable):
- System health (latency, error rate, uptime)
- Model performance (eval scores, cost, throughput)
- Infrastructure utilization and cost

### Step 5: Measurement Plan

For each metric, document:
- **Definition**: Exact formula, including/excluding criteria
- **Data source**: Which event, table, or API
- **Instrumentation**: What needs to be logged/tracked
- **Granularity**: How often updated (real-time, hourly, daily)
- **Segments**: Key breakdowns (platform, country, user tier)
- **Owner**: Who monitors this metric

## Output Format
Generate a complete metric plan in markdown with:
1. Metric hierarchy (tree diagram)
2. Metric definitions table
3. Targets and alert thresholds
4. Dashboard layout description
5. Measurement plan

## Common Pitfalls to Avoid
- **Vanity metrics**: Big numbers that don't reflect value (total sign-ups vs. active users)
- **Too many metrics**: 5-8 key metrics max on the exec dashboard
- **No baselines**: Always show current state before setting targets
- **Missing guardrails**: Every optimization metric needs a counter-metric
- **No segmentation**: Averages hide problems — always break down by segment
