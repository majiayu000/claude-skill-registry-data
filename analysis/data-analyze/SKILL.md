---
name: data-analyze
version: 1.0.0
description: Answer any data question, scaling effort from a one-number lookup to a full stakeholder-ready analysis with a recommendation.
author: matrixx0070
tags: [data, analysis, reporting, insights, decision-support, diagnostics]
capabilities: []
---

# data-analyze

## When to use

Use this when someone asks a question a dataset can answer — from "what was revenue last month?" to "why did churn spike in Q3 and what do we do?" Right-size the effort to the ask.

**Not for:** profiling an unfamiliar dataset (use data-explore first), writing the SQL itself (use data-write-query), formal significance testing (use data-statistical-analysis), or QA of a finished analysis (use data-validate).

## Method

1. **Classify the tier and say which you chose:** (a) lookup — one metric; (b) comparison — segment/time deltas; (c) diagnostic — why X changed; (d) stakeholder — decision + recommendation. Decision point: if the ask implies an action, it is tier (d), not (a).
2. **Restate the question precisely:** metric definition, grain, time window, filters, population. Surface hidden assumptions before computing.
3. **Locate and confirm the source.** Verify the grain and reconcile one total against a known figure before trusting any number.
4. **Compute the smallest correct operation for the tier.** Show the query or transformation.
5. **Interpret:** magnitude, direction, and signal vs noise. For diagnostics, decompose the change by segment, mix, and rate to find the driver.
6. **Recommend — tier (d) only.** Tie each insight to one concrete action and its expected impact.

## Example

Ask: "Why did Q3 revenue drop 8%?" (tier c). Decompose: revenue = customers × ARPU. Customers fell 2%, ARPU fell 6%. ARPU decline concentrates in the SMB segment (−14%), where a March discount campaign expired and was replaced by higher churn among discounted accounts. Finding: the drop is an SMB retention problem, not a pricing or volume problem across the board.

## Pitfalls

- Building a 5-section report for a one-number lookup, or answering a strategic ask with one bare figure.
- Reporting a delta without checking it is meaningful rather than normal fluctuation.
- Skipping reconciliation, then presenting a number from an incomplete extract.
- Claiming a cause from a single correlated segment without decomposing alternatives.

## Output format

```
Answer:  <number + units + time window>, first line.
How:     <one-line method + source, reproducible>
Context: <comparison / trend / benchmark that gives it meaning>
Caveats: <data gaps, definitions, confidence limits>
Recommendation: <tier (d) only — action → expected impact>
```

Lead with the answer; never bury the number under methodology. If the data cannot answer the question, say so and state exactly what would be needed.
