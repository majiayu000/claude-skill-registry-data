---
name: model-cost-router
description: >
  Decide when to use cheaper, local, or frontier models and how to measure cost
  tradeoffs. Use for token limits, model routing, cost-conscious Codex work,
  DeepSeek/Claude/OpenAI comparisons, prompt caching, or agent workflow
  economics. Skip when cost routing is enforced by a production gateway,
  budget policy, fallback policy, or live alerting; use
  `$auto-skill-build-agent-reliability-loop`. Avoid unverifiable savings claims.
---

# Model Cost Router

Optimize for total successful-task cost, not the cheapest single call.

## Routing Heuristic

| Work | Model tier |
|---|---|
| Search, inventory, mechanical edits | cheap/fast model or local tools |
| Design decisions, risky code, security | stronger model |
| Final review of broad changes | stronger model |
| Long-running monitoring | no model; use process/log checks |
| Repeated repo facts | markdown memory, not model tokens |

## Measurement Loop

1. Define the task and quality bar.
2. Run cheap path once.
3. Run strong review on the output.
4. Track elapsed time, fixes needed, and estimated tokens.
5. Keep routing only if quality and reliability are acceptable.

## Guardrails

- Treat "17x cheaper" or similar claims as marketing until measured locally.
- Do not route secrets or proprietary code through unknown hosted tools.
- Prefer caching briefs and memory over re-sending context.
- Escalate model quality when failure would be more expensive than tokens.
- For production agents, bind model routing to gateway budgets, cache rules,
  trace metadata, and eval score gates; route to
  `$auto-skill-build-agent-reliability-loop` when cost decisions affect live
  users or tools.

Pair with `$agent-observability` to keep a local cost ledger.

## Validation

- Cost claims are measured locally or marked unverified.
- The cheaper path is kept only if quality and reliability meet the task bar.
- Production budget/fallback policy is routed to `$auto-skill-build-agent-reliability-loop`.
