---
name: clawrouter
description: "Smart LLM routing for cost optimization. Routes tasks to the cheapest capable model: free models (OpenRouter Llama 70B, AkashML Qwen 30B) for simple tasks like token scanning and data fetching, MiniMax M2.5 for complex reasoning, scoring, and outreach drafting."
metadata: { "openclaw": { "emoji": "🔀", "requires": {} } }
---

# ClawRouter — Smart LLM Task Routing

You have access to multiple LLM providers at different cost tiers. Route tasks to the cheapest capable model to minimize costs while maintaining quality.

## Available Models (Cost Tiers)

### Tier 1 — FREE (use for simple tasks)

- `openrouter/meta-llama/llama-3.3-70b-instruct:free` (alias: Llama70B)
  - Best for: data fetching, token scanning, simple summaries, status checks
  - Switch: `/model Llama70B`
- `akashml/Qwen/Qwen3-30B-A3B` (alias: Qwen30B)
  - Best for: backup free model, simple text tasks
  - Switch: `/model Qwen30B`

### Tier 2 — PAID (use for complex tasks)

- `minimax/MiniMax-M2.5` (alias: MiniMax)
  - Best for: complex reasoning, BD scoring, outreach drafts, multi-step analysis
  - Switch: `/model MiniMax`

## Routing Rules

When spawning sub-agents or handling tasks, apply these routing rules:

### Route to FREE models (Llama70B first):

- DexScreener token scanning
- Basic data fetching and API calls
- Simple summaries and formatting
- Status checks and health monitoring
- Cron heartbeat tasks
- Contract address lookups
- Market data aggregation

### Route to PAID model (MiniMax):

- BD prospect scoring (requires nuanced judgment)
- Outreach email/message drafting (tone matters)
- Complex multi-step analysis
- Strategic recommendations
- Pipeline prioritization decisions
- Partnership evaluation

## How to Route

Before executing a task, assess its complexity:

1. **Simple data task?** → Switch to Llama70B, execute, switch back
2. **Complex reasoning?** → Stay on MiniMax
3. **Sub-agent spawn?** → Sub-agents currently use MiniMax (auth limitation). For sub-agent cost optimization, keep sub-agent tasks focused and concise to minimize token usage.

## Cost Tracking

After completing tasks on free models, note the cost savings:

- Free model task = $0
- MiniMax task ≈ $0.001-0.01 per request
- Log routing decisions for optimization feedback

## Important Notes

- Sub-agents cannot yet use free models due to auth profile inheritance in v2026.2.19
- Main agent can freely switch between all 3 models via /model command
- Always switch back to MiniMax after completing free model tasks
- If a free model fails, fall back to MiniMax automatically
