---
name: cost-guardrail
description: LLM and cloud cost awareness — model tiering, token budgets, right-sizing, and when a cheaper model suffices. Trigger before finalising any architecture that calls LLMs, before scaling a workload, or when a cost estimate is needed.
---

# Cost Guardrail

> **The most expensive model is the one running on every request when it does not need to.**

LLM cost is not a finance problem — it is an architecture problem. The design determines the bill. This skill enforces cost-awareness as a first-class design constraint, not an afterthought.

## When to use

- Designing any system that calls an LLM (directly or via an agent)
- Before scaling a workload to higher volumes
- When a cost estimate is required for a feature or release
- When reviewing an architecture for unbounded cost vectors
- When choosing between model tiers for a given task

## Procedure

1. **Identify every LLM call in the system** — list: which agent or component makes the call, the model tier used, the approximate input and output token counts, and the call frequency (per user action / per minute / per batch).

2. **Apply the model tiering test** — for each LLM call, ask:
   - Does this task require deep reasoning, or is it classification / extraction / reformatting?
   - Can the task be completed with a smaller or faster model?
   - Is the model tier choice based on evidence (benchmark, A/B test) or assumption?

   General tiering principle (verify current pricing against your provider's documentation before relying on it):

   | Task type | Appropriate tier |
   |---|---|
   | Simple classification, extraction, summarisation | Small / fast model |
   | Complex reasoning, multi-step planning, code generation | Mid-tier model |
   | Deep analysis, architecture decisions, adversarial review | Highest-tier model |

3. **Identify unbounded cost vectors** — flag any call pattern where the token count or call volume has no upper bound:
   - Loops that call an LLM until a condition is met (with no max-iteration guard)
   - User-triggered calls with no rate limiting
   - Context windows that grow unboundedly across a conversation
   - Batch jobs with no per-run budget ceiling

4. **Estimate the monthly cost envelope** — for each LLM call:
   ```
   estimated monthly cost ≈ (input tokens × input price) + (output tokens × output price) × calls/month
   ```
   Use current published rates from your provider. Do not use rates from training data — they change.

5. **Add cost controls** — for each unbounded vector:
   - Set a max-token budget per call (trim context if needed)
   - Add rate limiting at the application layer
   - Add a budget alert at the infrastructure layer
   - Consider caching repeated calls with identical or near-identical inputs

6. **Check for caching opportunities** — LLM calls that return the same result for the same input are cacheable. Prompt caching (where supported by the provider) can reduce cost significantly on repeated prefixes.

7. **Document the cost model** — in the ADR or design doc, record: model tiers chosen, rationale, estimated monthly cost at target scale, and the controls in place.

## Outputs

- LLM call inventory: component | model tier | input tokens (est.) | output tokens (est.) | frequency | monthly cost (est.)
- Unbounded cost vectors flagged with mitigations
- Monthly cost estimate at target scale
- Recommended model tier per call with rationale

## Guardrails

- **Never use pricing from training data.** Rates change. Fetch current rates from the provider's documentation before estimating.
- **A call that "works" at low volume may be unaffordable at scale.** Always estimate at the target scale, not the current scale.
- **Caching is not optional for high-frequency repeated calls.** An uncached LLM call repeated thousands of times per day is a design flaw.
- **Token budgets are architecture decisions.** Decide them explicitly; do not let the model decide by consuming whatever context is available.

## Anti-rationalization table

| Excuse | Counter |
|---|---|
| "It's only a few cents per call" | At scale, cents become thousands of dollars. Estimate the monthly envelope. |
| "We'll optimise later" | Cost optimisation is hardest after the architecture is set. Do it now. |
| "The big model gives better results" | Verify with a test. Small models are often sufficient for structured tasks. |
| "We don't know the volume yet" | Estimate a range. A 10x cost swing between low and high volume is a design risk. |
