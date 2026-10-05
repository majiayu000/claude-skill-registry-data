---
name: revenue-engine
description: Use when manage revenue pipelines, track Stripe/analytics metrics, and
  automate financial reporting for SaaS businesses. Use when building revenue infrastructure.
domain: core
license: Apache-2.0
tags:
- engine
- infrastructure
- memory
- pipeline
- revenue
- self-improvement
- money
- analytics
version: 2.0.0
author: oyi77
subdomain: ''
type: core
category: core
---
## Overview

This skill manages revenue pipelines end to end: tracking Stripe and analytics metrics, and automating financial reporting for SaaS businesses. Use it when money metrics must be visible and attributable. It wires the measurement loop from raw events to the reports you act on.


# Money-Making Overview

This engine is the financial nervous system of your business. Without it, you leak 5-15% of revenue through forgotten invoices, missed renewals, and untracked metrics. With it, you capture every dollar and know exactly where to focus to grow.



## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Revenue Streams
1. **Your Own Revenue Ops** — tracking prevents leakage
2. **Revenue Dashboard Service ($2K-5K/setup)** — build for clients
3. **CFO-as-a-Service ($1K-3K/mo)** — ongoing financial monitoring

## First Action in 60 Minutes
```bash
#!/usr/bin/env bash
# Revenue engine health check
mkdir -p ~/revenue-engine/{metrics,reports,alerts}

echo "=== Revenue Health Check ==="
echo "MRR: $(curl -s https://api.stripe.com/v1/subscriptions --header "Authorization: Bearer $STRIPE_KEY" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(int(i['plan']['amount']) for i in d['data'])/100)" 2>/dev/null || echo 'Set \$STRIPE_KEY')"
echo ""
echo "Metrics to track this week:"
echo "  - MRR growth rate"
echo "  - Churn rate (exits / total)"
echo "  - LTV (avg revenue × avg months retained)"
echo "  - CAC (total sales cost / new customers)"
echo "  - Quick Ratio (new MRR + expansion MRR) / churned MRR"
```

## Revenue Pipeline Architecture

Revenue Engine is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Revenue Configuration & Integration

**Trigger phrases:**
- "revenue engine"
- "Manage revenue pipelines, track Stripe/analytics metrics, and automate financial"

Set up required environment variables and paths, configure logging level and output format, define resource limits (memory, time, API calls), enable/disable features via configuration flags.

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Revenue Intelligence & Model Routing

Different revenue tasks need different models. Route intelligently:

```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```

## When to Deploy Revenue Engine

- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available

## When NOT to Deploy

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit

## Revenue Verification Protocol

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
2. **Execute** — Run revenue engine workflow with configured parameters
3. **Verify** — Validate output meets requirements, document results

### Verification Checklist
- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings

## Verification

- Wire one revenue source and confirm events flow into the pipeline with correct amounts and attribution.
- Verify reporting: the dashboard/report totals match the sum of recorded events, and period filters work.
- Check alerting: a threshold breach triggers the documented notification with the right message.
- Confirm the pipeline handles refunds and chargebacks without corrupting totals.

## Anti-Rationalization Table

| Excuse | Truth |
|---|---|
| "I'll track revenue manually" | Manual tracking misses 10%+ of revenue |
| "I don't have enough revenue yet" | Start tracking at $0; patterns emerge early |
| "Stripe dashboard is enough" | Dashboards don't alert you to problems |

## Output Format

On completion: "MRR: $[N], Churn: [N]%, LTV: $[N], CAC: $[N], Quick Ratio: [N], Revenue Health: [GREEN/YELLOW/RED]"


## When to Use
Use this skill when working with revenue engine.


## Workflow
See the parent skill for authoritative workflow documentation.
