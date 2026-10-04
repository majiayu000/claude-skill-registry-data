---
name: subagent-orchestration
description: Use when designing or debugging the Master Orchestrator's routing logic, intent detection, escalation rules, or handoffs between the 4 sub-agents (customer-service / sales / lead-intake / operations).
---

# Sub-agent Orchestration skill

## When to invoke

- Touching `src/orchestrator/master.ts` or its prompt
- Adding a new sub-agent or new routing intent
- Debugging "wrong agent picked up the message"
- Modifying escalation-to-human logic

## Architecture invariants

1. **Master sees full conversation history** ג€” sub-agents see only their slice + relevant CRM context
2. **One agent active per turn** ג€” no parallel sub-agent calls for the same customer message
3. **Tool: `route_to_agent`** is the only way Master delegates ג€” never inline-respond to a customer-facing message that should go through a sub-agent
4. **Sub-agents cannot route to each other** ג€” they return to Master, Master re-routes if needed

## Routing decision tree (priority order)

1. **Compliance escalation trigger** ג†’ human, regardless of intent
2. **Existing CRM process active** ג†’ operations agent (continuity)
3. **New lead, no CRM record** ג†’ lead-intake agent
4. **Qualified lead, awaiting booking** ג†’ sales agent
5. **Existing customer, transactional question** ג†’ customer-service agent
6. **Ambiguous** ג†’ customer-service agent with explicit "ask clarifying question" instruction

## Hard rules

1. **Never lose conversation state** across routing ג€” Master passes a context object, sub-agent must acknowledge it
2. **Log every routing decision** with reasoning (which rule fired) for debugging
3. **Escalation to human is terminal** ג€” once escalated, no agent responds until human releases
4. **Hebrew intent detection** ג€” never route based on English keyword match alone; Israeli customers code-switch frequently

## Model choices (from CLAUDE.md)

- Master: `claude-opus-4-7` (sees everything, needs strongest reasoning)
- Sub-agents: `claude-sonnet-4-6` (focused scope, cost-balanced)
- Doc classification: `claude-haiku-4-5-20251001` (cheap, fast)

Do not override without good reason ג€” costs add up fast at scale.

## Common failure modes

- **Ping-pong**: Master keeps re-routing ג†’ add cycle detection, max 2 routes per customer turn
- **Wrong agent for known customer**: missing CRM lookup before routing ג€” always fetch CRM context first
- **Lost Hebrew nuance**: prompts written in English describing Hebrew intents ג€” write triggers in Hebrew with English comments