---
name: finops
description: |
  Optimize cloud spend across AWS, GCP, and Azure using a structured FinOps framework covering waste detection, instance rightsizing, Reserved Instance and Savings Plan analysis, cost allocation tagging, budget thresholds, and vendor negotiation playbooks.
  Purpose: Reduces cloud bills by 20–40% with systematic, repeatable actions — not one-off fixes.
  When to trigger: (1) "Why is our cloud bill so high this month?" or "review our cloud costs," (2) "audit for waste or idle resources" — monthly or quarterly reviews, (3) "should we buy Reserved Instances or Savings Plans?" — annual planning or contract renewals, (4) "build a cost showback report by team" — finance or engineering leadership asks, (5) "unexpected spike in the billing console" — anomalies on invoices, (6) "plan costs before scaling infrastructure," (7) "prepare for a vendor contract negotiation."
  Key capabilities: A 30-day utilization rightsizing framework (highest ROI FinOps action), Savings Plan coverage ratio targets by environment, a monthly showback report template, budget alert thresholds at 50/80/90/100%, per-user cost modeling for pricing decisions, and a vendor negotiation playbook based on actual usage data.
  Ideal user/context: Cloud engineers, finance teams, DevOps leads, or founders managing AWS/GCP/Azure spend who want a repeatable process — not just a cost dashboard.
  Also for: Startup CTOs benchmarking infrastructure costs, SaaS companies building unit economics models, and teams migrating between cloud providers who need a cost comparison framework.
---

# FinOps Skill

## When to Activate

Trigger when the user asks to:
- Optimize cloud costs or analyze billing
- Rightsize instances or services
- Analyze reserved instance or Savings Plan coverage
- Build a cost allocation or showback report
- Detect cloud waste or idle resources
- Set up cloud budgets and alerts
- Plan scaling costs or vendor contracts

## Waste Detection Checklist

Run this checklist monthly:

### AWS
- [ ] Unattached EBS volumes (still accruing GB-month charges)
- [ ] Unattached Elastic IPs (charged when idle)
- [ ] EC2 instances with CPU < 20% sustained (over-provisioned)
- [ ] RDS instances with connections < 10% of max connections
- [ ] S3 buckets with no lifecycle policies (paying for old logs)
- [ ] CloudWatch custom metrics you no longer use
- [ ] NAT Gateway idle time (replaced by VPC endpoints?)
- [ ] Public S3 buckets (security + cost: data transfer charges)

### GCP
- [ ] Unused static external IPs
- [ ] Idle Cloud SQL instances
- [ ] Unused persistent disks
- [ ] Oversized machine types
- [ ] Load balancers with no backend traffic

### Azure
- [ ] Orphaned managed disks
- [ ] Idle virtual machines not deallocated
- [ ] Over-provisioned VM size
- [ ] Blob storage with no lifecycle policy

### Universal
- [ ] Snapshots older than 30 days that could be deleted
- [ ] Data transfer charges — is egress higher than expected?
- [ ] CDN misconfiguration causing origin hits
- [ ] Autoscaling not enabled on variable workloads

## Rightsizing Framework

For each EC2/GCE/Azure VM:
1. Pull 30-day CPU and memory utilization (CloudWatch / Cloud Monitoring)
2. If average CPU < 30%: downgrade to next smaller instance family
3. If CPU > 70% regularly: consider upgrade or horizontal scaling
4. Apply changes during low-traffic window; monitor for errors

Rightsizing is the highest-ROI FinOps action — a typical 30% reduction in compute spend.

## Reserved Instance / Savings Plan Analysis

### Decision Tree

```
Is usage steady-state (>1 year, consistent daily patterns)?
  YES → Buy Reserved Instances or 1-year Savings Plans
  NO  → Use Savings Plans with no commitment, or on-demand
        (flexible, convertible if patterns change)

What coverage ratio to target?
  Baseline (steady-state prod): 60–80% reserved
  Dev/test/staging: 0% reserved (on-demand or spot)
  Variable prod: savings plans with no commitment
```

### Coverage Ratio Targets

| Environment | Target Coverage |
|---|---|
| Production (steady) | 60–80% |
| Production (variable) | 30–50% (no commitment) |
| Staging / Dev | 0% |
| Disaster recovery | 0% |

## Cost Allocation

Tag everything with these dimensions:
- `Environment`: prod, staging, dev
- `Team`: engineering, data, platform
- `Project`: service name or project ID
- `CostCenter`: department or business unit

Build a monthly showback report by team:
- Total spend
- Top 3 services by spend
- Month-over-month change
- Waste identified and savings actioned

## Budget Alert Thresholds

Set budgets at:
- **50%**: informational — check if expected
- **80%**: warning — investigate immediately
- **90%**: action required — freeze non-essential provisioning
- **100%**: alert — escalate to engineering lead

Set budgets at service level AND total account level.

## Vendor Negotiation

Before any renewal:
1. Compile 12 months of actual usage data (not sticker price)
2. Research committed use discounts available (typically 30–60% off on-demand)
3. Get quotes from at least 2 competitors
4. Negotiate based on actuals, not forecasts
5. Multi-year terms for >20% additional discount — only if usage is predictable

Key ask: credits over price increases. Most vendors prefer credits to structural discounts.

## Weekly Cost Trend Report Template

```
FINOPS REPORT — Week of [date]
─────────────────────────────────────────
Total cloud spend (MTD): $[X]
vs. prior week: +/-$[Y] (+/-[Z]%)
vs. monthly budget: $[X]/$[budget] ([P]%)

TOP SPENDING SERVICES
1. EC2: $[X] — [any异常?]
2. RDS: $[X] — [any异常?]
3. S3: $[X] — [any异常?]

ANOMALIES DETECTED
- [service]: spike on [date] — [root cause or investigate]

WASTE IDENTIFIED THIS WEEK
- [resource]: $[savings]/mo — action taken / action planned

FORECAST TO END OF MONTH
$[X] projected vs. $[budget] budget — [on track / over / under]
─────────────────────────────────────────
```

## Per-User Scaling Cost Model

For every service that scales with users, build:

```
Cost model: $[X] per 1,000 MAU
Breakdown:
  - Compute (EC2/RDS): $[A] per 1,000 MAU
  - Storage (S3/RDS): $[B] per 1,000 MAU
  - Egress/CDN: $[C] per 1,000 MAU
  - Third-party APIs: $[D] per 1,000 MAU

Implication: 10,000 → 100,000 MAU = $[X * 100] incremental/month
```

Use this model to set pricing tiers and justify infrastructure investment.
