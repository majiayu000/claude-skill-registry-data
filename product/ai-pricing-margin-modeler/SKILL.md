---
name: ai-pricing-margin-modeler
description: "Builds the unit-economics model behind Artificial Intelligence (AI) product pricing: cost per task from tokens, tool calls, retrieval, and retries; a gross-margin floor; a usage-distribution and heavy-user risk analysis; margin comparison across seat, usage, credit, hybrid, and outcome-based packaging; and price-change guardrails. Use when pricing an AI feature or AI-native product; gross margin is falling as usage grows; choosing between per-seat, usage-based, credits, or outcome-based pricing for a model-backed product; modeling the impact of a model or provider change on margin; or a few power users are consuming most of the inference budget."
---

# AI Pricing Margin Modeler

> In software, the next user is nearly free; in AI, the next task has a bill - price for the distribution of usage, not the average.

## What this skill is

A unit-cost and margin workflow for products where every request incurs variable inference cost. It builds cost per task from the bottom up, maps how usage is distributed across customers, and tests each packaging model against a gross-margin floor at the median, the 90th percentile, and the heaviest users. It complements general pricing strategy (willingness to pay, competitive positioning, value metrics) by answering the question those analyses skip: does this price still make money when the product succeeds?

## What it solves

- Flat per-seat prices that lose money on the top 5-10% of users
- Cost estimates based on average tokens that ignore retries, tool calls, long contexts, and agent loops
- Gross margin that erodes silently as customers adopt heavier features
- Credit systems that confuse buyers or that do not track real cost
- Outcome-based pricing proposed without a model of cost per attempted outcome
- Price or model changes shipped without a margin impact estimate

## When to invoke

- Setting the first price for an AI feature, add-on, or AI-native product
- Gross margin trending below target as adoption grows
- Choosing between seat, usage, credits, hybrid, or outcome-based packaging
- Evaluating a model upgrade, provider switch, or routing change
- Designing usage limits, fair-use policies, or overage pricing

## Phase 1: Build cost per task

Define 3-6 task types that represent real usage (for example: short answer, document summary, multi-step agent run). For each:

```
Cost per attempt = (input tokens x input price) + (output tokens x output price)
                 + (cached tokens x cached price) + tool and retrieval calls x cost per call
                 + compute or hosting allocation
Cost per successful task = Cost per attempt x (1 + retry rate) / success rate
```

| Task type | Input tokens | Output tokens | Tool or retrieval calls | Retry rate | Success rate | Cost per successful task |
|-----------|-------------:|--------------:|------------------------:|-----------:|-------------:|-------------------------:|

Retry rate counts automatic re-calls inside one attempt (errors, timeouts, failed output validation); success rate is the share of attempts the user accepts, so failed attempts are paid for by the successful ones.

Use measured production or beta logs where available. Add a contingency of 20-30% for prompt growth and context creep until there are 3 months of data. Include safety filtering, evaluation, and logging costs if they run per request.

## Phase 2: Usage distribution

Average usage hides the risk. Build the distribution per account or seat per month:

| Percentile | Tasks per month | Task mix | Monthly inference cost |
|------------|----------------:|----------|-----------------------:|
| Median (p50) | | | |
| p75 | | | |
| p90 | | | |
| p99 | | | |
| Max | | | |

```
Concentration = share of total inference cost from the top 10% of accounts
```

Concentration above 50% means packaging must include limits, tiers, or usage components.

## Phase 3: Set the gross-margin floor

```
Gross margin = (Revenue - inference cost - hosting - third-party fees - support allocation) / Revenue
```

| Product context | Typical target gross margin | Floor (do not price below) |
|-----------------|----------------------------:|---------------------------:|
| AI add-on to an existing Software as a Service (SaaS) product | 70-80% | 60% |
| AI-native application | 60-75% | 50% |
| Agent or heavy-compute workflow | 50-65% | 40% |

Set the floor with finance. Test it at p50 and p90, and decide explicitly whether p99 accounts are allowed below the floor.

## Phase 4: Compare packaging models

Model revenue and margin for the same customer distribution under each option:

| Model | How it charges | Margin at p50 | Margin at p90 | Margin at p99 | Buyer predictability | Risk |
|-------|---------------|--------------:|--------------:|--------------:|----------------------|------|
| Per seat (unlimited) | Fixed per user | | | | High | Heavy users destroy margin |
| Per seat with fair-use cap | Fixed plus soft limit | | | | High | Cap enforcement friction |
| Usage-based | Per task or per unit | | | | Low | Bill shock, slower adoption |
| Credits | Prepaid bundle, tasks burn credits at cost-weighted rates | | | | Medium | Confusing if credit rates are opaque |
| Hybrid | Platform fee plus included usage plus overage | | | | Medium-high | More complex to explain |
| Outcome-based | Per resolved ticket, qualified lead, completed task | | | | Medium | Cost of failed attempts carried by vendor |

For outcome-based pricing:

```
Cost per billed outcome = Cost per attempt x attempts per outcome
Price per outcome >= Cost per billed outcome / (1 - margin floor)
```

Credit rates should be proportional to cost per task type so heavy tasks cannot be arbitraged.

## Phase 5: Sensitivity and heavy-user risk

Stress the chosen model:

| Scenario | Change | Gross margin impact |
|----------|--------|--------------------:|
| Model price drop | Provider cuts token prices 50% | |
| Model upgrade | Better model at 2-3x cost per token | |
| Usage growth | Median usage doubles as adoption deepens | |
| Agent adoption | Share of multi-step runs rises from 10% to 40% | |
| Routing | 60% of tasks moved to a smaller model | |

Identify levers to protect margin: model routing by task difficulty, caching, shorter context, output length limits, batch processing, and per-tier model access.

## Phase 6: Price-change guardrails

- **Grandfathering**: existing customers keep current terms for a stated period (for example 6-12 months)
- **Notice**: at least 30 days for any usage-limit or rate change; longer for annual contracts
- **Usage visibility**: in-product meters and alerts at 50%, 80%, and 100% of included usage before overage applies
- **Spend caps**: buyer-configurable limits on usage-based plans
- **Margin trigger**: re-price or re-package if blended gross margin stays below the floor for 2 consecutive months
- **Pass-through**: decide in advance whether model price decreases are passed to customers, reinvested in quality, or retained

## Output

- Cost-per-successful-task table by task type, with assumptions and contingency
- Usage distribution with concentration metric
- Agreed gross-margin floor
- Packaging comparison with margin at p50, p90, and p99
- Sensitivity table and prioritized cost levers
- Recommended packaging with limits, overage design, and price-change guardrails

## Operating rules

**Always**
- Calculate cost per successful task, including retries and failed attempts
- Model margin at p90 and p99 usage, not only the average
- Weight credits and limits by real cost per task type
- Re-run the model after every model, provider, or routing change
- Give customers usage visibility before any overage is charged

**Never**
- Price an AI product on average token usage alone
- Offer unlimited usage without a fair-use policy and a heavy-user margin estimate
- Assume model prices will keep falling and price below the floor today
- Launch outcome-based pricing without measuring attempts per outcome
- Change limits or rates without notice and a grandfathering decision
