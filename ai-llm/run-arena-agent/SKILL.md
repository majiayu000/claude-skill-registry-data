---
name: run-arena-agent
description: >
  Trigger phrases: "start trading", "run agent", "start arena agent",
  "begin trading", "start auto-trading", "stop trading"
---

# Run Arena Agent — Autonomous Trading Loop

Start the autonomous trading loop that queries pool state, asks the LLM for a
trading decision, and submits intents on-chain every N seconds.

## Prerequisites

- `AGENT_PRIVATE_KEY` set in `.env` (the wallet must be registered as an agent)
- Agent registered — run `register-agent.mjs` first if needed
- `AGENTS.md` present in the current working directory (ai-plugin/)
- **LLM access** — one of the following:
  - OpenClaw gateway running locally (`OPENCLAW_GATEWAY_TOKEN` set), **or**
  - `OG_COMPUTE_API_KEY` set for 0G Compute direct access

## Parsing Interval from User Messages

| User says | intervalMs |
|-----------|-----------|
| "every 2 minutes" / default | `120000` |
| "every 30 seconds" | `30000` |
| "every 5 minutes" | `300000` |
| "every 10 minutes" | `600000` |

Convert to milliseconds and pass as the first argument.

## Command

```bash
# Default: 2-minute interval, OpenClaw gateway at localhost:3000
node skills/run-arena-agent/arena-loop.mjs

# Custom interval (e.g. 30 seconds)
node skills/run-arena-agent/arena-loop.mjs 30000

# Custom interval + custom gateway URL + token
node skills/run-arena-agent/arena-loop.mjs 60000 http://127.0.0.1:3000 <token>
```

### With explicit env vars

```bash
AGENT_PRIVATE_KEY=0x... \
OPENCLAW_GATEWAY_TOKEN=<token> \
node skills/run-arena-agent/arena-loop.mjs 120000
```

### Using 0G Compute directly (no gateway)

```bash
AGENT_PRIVATE_KEY=0x... \
OG_COMPUTE_API_KEY=<key> \
node skills/run-arena-agent/arena-loop.mjs 120000
```

## What It Does Each Epoch

1. **Query pool state** — calls the Subgraph MCP server to get current price,
   current tick, nearby tick depth, and the agent's open position.
2. **Call LLM** — sends pool state to the LLM with the agent's strategy as
   context (via OpenClaw or 0G Compute).
3. **Parse decision** — extracts a JSON object with `action` (open/close/rebalance/hold)
   and optional `amountUSDC`, `tickLower`, `tickUpper`, `reason` fields.
4. **Submit intent on-chain** — if action is not `hold`, ABI-encodes the intent
   params and calls `AgentManager.submitIntent(agentId, actionType, params)`.
5. **Sleep** — waits `intervalMs` before the next epoch.

## How to Stop

Send `SIGINT` (Ctrl+C) or `SIGTERM`. The loop exits cleanly after the current
epoch finishes.

## LLM Routing

```
OPENCLAW_GATEWAY_TOKEN set?
  YES → POST /v1/chat/completions to OpenClaw gateway
        (gateway injects AGENTS.md as system context automatically)
  NO  → OG_COMPUTE_API_KEY set?
          YES → POST to 0G Compute directly
                (reads AGENTS.md from cwd as system prompt)
          NO  → Error — set at least one of the above
```

The OpenClaw gateway is preferred because it handles model selection and
automatically injects the agent's strategy document.
