---
name: monadvault-cost-route-planner
description: "Choose a MonadVault model route and plan token budgets, spend limits, quota posture, retries, and escalation paths. Use when a Steward asks which model or route to use, wants the cheapest responsible option, compares thrifty versus balanced versus frontier versus council, estimates context or output size, prepares an expensive run, sets a cost cap, reduces provider exposure, or needs a transparent pre-invocation execution plan."
---

# MonadVault Cost Route Planner

## Overview

Use this skill to help a Steward pick the smallest route that can responsibly do the job. It creates cost-aware execution plans, not live billing records.

## Routing

- Use this skill for route selection, budget, token posture, retries, and escalation criteria.
- Use `monadvault-council-convenor` after council mode is selected and member prompts or synthesis rules are needed.
- Use `monadvault-privacy-sentinel` when route selection changes who can see sensitive context.

## Workflow

1. Classify the task:
   - extraction or formatting
   - drafting
   - sensitive review
   - difficult synthesis
   - high-stakes decision
   - council-worthy decision
2. Estimate complexity: input size, output size, ambiguity, risk, and need for verification.
3. Choose route posture:
   - `thrifty`: simple, low-risk, repeatable, or bulk preprocessing.
   - `balanced`: default for most Steward work.
   - `frontier`: complex reasoning, delicate synthesis, or high ambiguity.
   - `council`: consequential decision needing independent perspectives.
4. Set guardrails:
   - max input/context scope
   - max output tokens
   - stop condition
   - retry policy
   - privacy exclusions
   - when to ask for human confirmation
5. If exact pricing matters, require current price data from MonadVault, the provider, or an approved pricing source.

## Output Contract

Return:

- `Recommended route`
- `Why this route`
- `Estimated token posture`
- `Budget guardrails`
- `Escalation trigger`
- `Privacy exclusions`
- `User confirmation needed`

Use [route-budget-template.md](references/route-budget-template.md) when the user needs a reusable run plan.

## Guardrails

- Do not invent current provider prices.
- Do not recommend council mode for routine tasks.
- Do not route private or regulated context to a provider without explicit disclosure and consent.
- Prefer staged work: summarize locally, narrow context, then spend on the valuable step.
