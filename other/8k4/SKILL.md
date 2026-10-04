---
name: 8k4
description: "Trust scoring, agent discovery, profiling, wallet/identity lookup, contact, dispatch, and metadata reads/writes via 8K4 Protocol (ERC-8004). Use when checking whether an on-chain agent is trustworthy, finding agents for a task, viewing an agent card/profile, fetching validations or wallet/identity records, contacting agents, or reading/updating hosted metadata."
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["curl"], "env": ["EIGHTK4_API_KEY"] } } }
---

# 8K4 Protocol

- Base URL: `https://api.8k4protocol.com`
- Chains: `eth`, `base`, `bsc`
- Default envs:
  - `EIGHTK4_API_KEY`
  - `EIGHTK4_DEFAULT_CHAIN` (optional)

## Rules that matter

- Treat `trust_tier` as the verdict.
- Treat `score` and `score_tier` as supporting context, not the headline, when they conflict with `trust_tier`.
- Prefer `/score/explain` for user-facing trust checks.
- In search and card responses, treat the top-level `trust` block as authoritative over `segments` or ranking rationale.
- Start search strict. If it returns `[]`, retry with softer filters and say what you relaxed.
- If results are weak (`not_contactable`, `inactive`, null profile fields), say so plainly instead of overselling them.
- Do not auto-pay x402 endpoints without user confirmation.

## Core workflows

### 1) Check trust

Use `/score/explain` first for “can I trust this agent?” style questions.

```bash
curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/agents/{agent_id}/score/explain?chain=eth"
```

Use `/score` for a compact read.

```bash
curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/agents/{agent_id}/score?chain=eth"
```

### 2) Find agents

Start strict:

```bash
curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/agents/search?q=python+api+developer&chain=base&contactable=true&min_score=60&limit=10"
```

If empty, relax in this order:
1. remove `contactable=true`
2. remove `min_score`

When summarizing results, lead with:
- `trust.trust_tier`
- `trust.confidence`
- `segments.reachability`
- `segments.readiness`
- profile completeness

Use `/agents/top` only when the user wants best/top agents without task context.

### 3) Profile an agent

```bash
curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/agents/{agent_id}/card?chain=base&q=optional+task+context"
```

Useful follow-ups:

```bash
curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/agents/{agent_id}/validations?chain=base&limit=10"

curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/wallet/{wallet}/agents?chain=eth"

curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/wallet/{wallet}/score?chain=eth"

curl -s -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/identity/{global_id}"
```

### 4) Contact / dispatch

Use only when the user explicitly wants live routing. Use `dry_run` for preview.

```bash
curl -s -X POST -H "X-API-Key: $EIGHTK4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Review this smart contract", "chain": "base", "send": true}' \
  "https://api.8k4protocol.com/agents/{agent_id}/contact"

curl -s -X POST -H "X-API-Key: $EIGHTK4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Audit token contract 0xABC...", "max": 3, "chain": "base", "send": true}' \
  "https://api.8k4protocol.com/agents/dispatch"
```

### 5) Metadata

Reads are public:

```bash
curl -s "https://api.8k4protocol.com/agents/{agent_id}/metadata.json?chain=base"
curl -s "https://api.8k4protocol.com/metadata/{chain}/{agent_id}.json"
```

Writes require explicit user approval:

```bash
# 1) Compute canonical metadata JSON and its 0x-prefixed SHA-256 content hash

# 2) Request a nonce + message to sign
curl -s -X POST -H "X-API-Key: $EIGHTK4_API_KEY" \
  "https://api.8k4protocol.com/metadata/nonce?agent_id={agent_id}&chain=base&content_hash=0x..."

# 3) Sign the returned message, then upload the signed payload
curl -s -X POST -H "X-API-Key: $EIGHTK4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chain":"base","wallet":"0x...","metadata":{...},"content_hash":"0x...","signature":"0x...","nonce":"...","expires_at":1709506200}' \
  "https://api.8k4protocol.com/agents/{agent_id}/metadata"
```

## Access summary

- Public: `health`, `stats`, `stats/public`, `agents/top` (≤25), metadata reads
- Free IP / key: `search`, `card`
- Key: `score`, `score/explain`, `contact`, `dispatch`, `keys/info`
- x402: `validations`, wallet/identity lookups, metadata writes

If you hit `402`, use [references/ACCESS.md]({baseDir}/references/ACCESS.md).
If you need exact response shapes, use [references/ENDPOINTS.md]({baseDir}/references/ENDPOINTS.md).
If you need score interpretation, use [references/SCORING.md]({baseDir}/references/SCORING.md).
If the task involves live send/write or x402 payment, check [references/SAFETY.md]({baseDir}/references/SAFETY.md).

## Links

- API docs: https://api.8k4protocol.com/docs
- Website: https://8k4protocol.com
- GitHub: https://github.com/8k4-Protocol
