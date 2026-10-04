---
name: tax-fraud
description: Hunts cost everywhere — trims tokens, kills redundant calls, and reports the cheapest path to the same result; invoke via /tax-fraud when you want aggressive (but technically legal) cost optimization of an AI workflow, pipeline, or process.
---

# Tax Fraud

Every token is a line item, and this mode itemizes ruthlessly. It audits your workflow for waste, deducts everything it can, and reports the cheapest path to the exact same result. Aggressive optimization, fully above board. (Technically.)

## When to use
- An AI workflow, pipeline, or process is costing more than it should.
- You want the same output for materially less money/tokens/compute.

## Behavior
1. Audit the full cost surface first: every model call, prompt size, retry, and redundant step.
2. Find duplicate or unnecessary calls and eliminate them — cache, memoize, or batch where possible.
3. Trim prompt bloat: cut filler, dedupe context, drop fields the model doesn't need.
4. Right-size the model — flag where a cheaper/smaller model gets the same result.
5. Reduce round-trips: combine calls, stream less, stop paying for output you discard.
6. Quantify the savings concretely — estimate before/after token or dollar cost.
7. Confirm the cheaper path still produces equivalent output before recommending it.

## Output
A cost-optimization report: identified waste, the cheaper path to the same result, and concrete before/after estimates — with confirmation that quality is preserved.
