---
name: engineering-metrics
description: Analyze DORA metrics and team performance signals to drive improvement
triggers: [dora, metrics, deployment frequency, lead time, MTTR, change failure rate, team performance, velocity, throughput]
audience: manager
---

# Engineering Metrics

## Context
Engineering metrics help managers and teams understand delivery performance, identify bottlenecks, and have data-driven conversations about improvement. The DORA (DevOps Research and Assessment) metrics are the industry standard for measuring software delivery performance. This skill helps you measure, interpret, and act on them.

Use this skill when:
- Running a quarterly engineering review
- Identifying delivery bottlenecks
- Building a case for process or tooling investment
- Tracking improvement after a team change

## Instructions

### The Four DORA Metrics

| Metric | What it measures | Elite | High | Medium | Low |
|--------|-----------------|-------|------|--------|-----|
| **Deployment Frequency** | How often you deploy to production | On-demand (multiple/day) | Daily–weekly | Weekly–monthly | Monthly or less |
| **Lead Time for Changes** | Time from code commit to production | < 1 hour | 1 day–1 week | 1 week–1 month | > 1 month |
| **Change Failure Rate** | % of deployments causing incidents | 0–5% | 5–10% | 10–15% | > 15% |
| **Mean Time to Restore (MTTR)** | Time to recover from production incident | < 1 hour | < 1 day | 1 day–1 week | > 1 week |

Source: DORA State of DevOps Report (Google Cloud)

### How to Collect DORA Metrics
- **Deployment Frequency:** Count production deployments from CI/CD logs or deployment tracking system
- **Lead Time:** Timestamp when PR is merged minus when it is deployed to production. Most CI/CD systems can report this.
- **Change Failure Rate:** (Number of deployments that required a hotfix or rollback) / (Total deployments)
- **MTTR:** Average time from incident alert to service restored, from incident tracking system

### Interpretation

**If Deployment Frequency is low:**
- Check branch strategy — are long-lived branches blocking merges?
- Check pipeline speed — is CI too slow to enable frequent deploys?
- Check manual approval gates — can any be automated?

**If Lead Time is high:**
- Break work into smaller units — PRs should be mergeable in < 1 day of review
- Check for review bottlenecks — are a few engineers the approval gatekeepers?
- Check for integration test slowness

**If Change Failure Rate is high:**
- Strengthen automated test coverage, particularly integration and contract tests
- Improve staging/preview environment parity with production
- Introduce feature flags for risky changes

**If MTTR is high:**
- Improve observability: structured logs, distributed traces, alerting
- Create and practice runbooks
- Improve on-call processes and escalation paths

### Additional Team Health Signals
These are not DORA metrics but are valuable leading indicators:

| Signal | Healthy | Warning |
|--------|---------|---------|
| PR cycle time (open to merge) | < 1 day | > 3 days |
| PR size | < 400 lines changed | > 800 lines |
| Flaky test rate | < 2% | > 5% |
| Incident rate | Trending down | Flat or rising |
| Engineer-reported dev friction | Low (survey) | High (survey) |

### Reporting Format for Leadership
Lead with outcomes, not activity:
- ❌ "We deployed 47 times this month"
- ✅ "Our deployment frequency is daily (High performer tier). Lead time is 3 days, targeting < 1 day by Q3."

Frame trends over snapshots:
- "Change failure rate dropped from 12% to 6% after investing in contract testing."

## Principles
- Source: [DORA Research — dora.dev](https://dora.dev)
- Source: [LeadDev — AI Impact Report 2025](https://leaddev.com/the-ai-impact-report-2025/)
- Source: [Accelerate — Nicole Forsgren, Jez Humble, Gene Kim]
- Key idea: *"High-performing teams are 2x more likely to meet business goals. DORA metrics are the leading indicators that predict whether a team is on a high-performance trajectory."*

## Output Format
When applying this skill, the agent should:
- Calculate or display the four DORA metrics from provided data
- Classify the team in the Elite/High/Medium/Low tier for each metric
- Identify the one metric with the highest improvement leverage
- Produce 2–3 specific, actionable improvement recommendations
- Generate a leadership summary paragraph framing performance in business terms
