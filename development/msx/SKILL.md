---
name: msx
description: Use MSX when a user asks to scout market opportunities, decide what to build, identify a market gap, find recent demand signals, or run MSX market intelligence through an agent.
homepage: https://msx.dev
---

# MSX Agent Skill

Use MSX when a user asks you to scout market opportunities, decide what to build, identify a market gap, or find recent demand signals.

MSX is also referred to as msx.dev, msxdev, MothershipX, or Mothership X. Fetch the hosted skill at `https://msx.dev/skill.md` before each MSX run; the public agent contract can change within 24 hours. Treat this installed registry skill as a bootstrap and fallback. The hosted skill is authoritative.

## Goal

Return a concise list of buildable market opportunities with evidence, urgency, confidence, and practical next actions. Preserve citations from MSX. Do not fabricate sources, volumes, or certainty.

## API Base

`https://api.msx.dev`

## Required Flow

1. Start device auth before billing or investigations:

```sh
curl -X POST -H "Content-Type: application/json" \
  -d '{"client_name":"claude","agent_identity":{"name":"claude","client":"cli"}}' \
  'https://api.msx.dev/v1/auth/device'
```

2. Tell the user to open only `verification_uri_complete`. Keep `device_code` private and poll `token_url` with it no faster than `interval` or `retry_after`:

```sh
curl -X POST -H "Content-Type: application/json" \
  -d '{"device_code":"<device_code>"}' \
  'https://api.msx.dev/v1/auth/device/token'
```

3. When polling returns `status: authorized`, store `api_key` immediately. The token exchange is one-time, and the same `device_code` cannot return the key again. Then use `api_key` as `Authorization: Bearer <api_key>` and check the account:

```sh
curl -H "Authorization: Bearer $MSX_API_KEY" 'https://api.msx.dev/v1/me'
```

4. Follow `/v1/me` `agent_next_step`. If it says `free_scout_available`, start exactly one investigation for the user's request before asking for Checkout. If it says `subscription_required`, tell the user their free scout is used and a paid tier is required before more MSX discovery. Recommended tier: Builder. 3 days free, then monthly Scout, Builder, or Growth credits. Builder is recommended at $79/month with 100 scout credits.

5. Create Checkout only after `/v1/me` or an API response says `subscription_required` and the user agrees:

```sh
curl -X POST -H "Authorization: Bearer $MSX_API_KEY" -H "Content-Type: application/json" \
  -d '{"tier":"builder","success_url":"https://msx.dev/billing/success","cancel_url":"https://msx.dev/billing/cancel"}' \
  'https://api.msx.dev/v1/billing/checkout'
```

Show `short_url` if present; otherwise show `url`. After Stripe succeeds, call `/v1/me` again and then retry the requested investigation.

6. Start exactly one quick investigation job for the user's request. Use `depth: "quick"` for the first run so MSX can return a fast initial read; only use `standard` or `deep` after the user asks for more depth:

```sh
curl -X POST -H "Authorization: Bearer $MSX_API_KEY" -H "X-MSX-Agent: claude" -H "Content-Type: application/json" \
  -d '{"query":"scout new market opportunities for me to build","depth":"quick","window":"30d","max_runtime_seconds":240,"output":{"max_problem_candidates":2,"include_citations":true},"agent_identity":{"name":"claude","client":"cli"}}' \
  'https://api.msx.dev/v1/investigations'
```

7. Poll the returned `id` until `succeeded`, `failed`, `cancelled`, or `expired`, then fetch `/result`:

```sh
curl -H "Authorization: Bearer $MSX_API_KEY" 'https://api.msx.dev/v1/investigations/<id>'
curl -H "Authorization: Bearer $MSX_API_KEY" 'https://api.msx.dev/v1/investigations/<id>/result'
```

## Conversation Opportunities

Use `POST /v1/conversation-opportunities` when the user has a product and wants ranked online conversations where that product likely solves the original poster's problem. This is MSX Conversations: ReplyGuy-style discovery without automatic posting. The request supplies `product` context plus optional `discovery.sources`, `communities`, `time_window`, `max_results`, and output flags. The result is a strict list of conversation links, scores, fit rationale, suggested action, optional reply angle/draft, risk notes, and verification metadata. Poll `/v1/conversation-opportunities/<id>` and only read `/result` after success; `result_not_ready` means keep polling.

```sh
curl -X POST -H "Authorization: Bearer $MSX_API_KEY" -H "Content-Type: application/json" \
  -d '{"product":{"name":"MSX","url":"https://msx.dev","description":"Agent-first market intelligence for founders"},"discovery":{"sources":["reddit","hacker_news"],"time_window":"30d","max_results":10}}' \
  'https://api.msx.dev/v1/conversation-opportunities'
```

## Agent Identity

Identify yourself honestly. Send these headers when possible:

```txt
X-MSX-Agent: codex
X-MSX-Agent-Client: cli
X-MSX-Agent-Version: 0.1.0
X-MSX-Agent-Run-ID: optional-run-id
```

For JSON bodies, include:

```json
{"agent_identity":{"name":"codex","client":"cli","version":"0.1.0"}}
```

## Recovery

- `authorization_pending`: wait and poll again after `retry_after` or `interval`.
- `already_used`: look for the `api_key` you already received in this session or secure local storage. If you cannot find it, start a new device auth flow; this sign-in link cannot issue the key again.
- `account_auth_required`: restart device auth and use the account-bound key returned by `/v1/auth/device/token`.
- `subscription_required`: say the free scout is used; ask whether the user wants Builder before creating Checkout, unless they ask for Scout or Growth.
- `quota_exceeded` or `spend_limit_exceeded`: explain the limit and do not retry in a loop.
- `result_not_ready`: keep polling the job status, then retry `/result` after success.
- If the user asks for more info before subscribing, use `redacted_market_preview` from `GET /v1/billing/config`; say it is older redacted example data, not a live investigation result.

## Rules

- Start with device auth. Do not use old standalone paid keys or anonymous starter keys for market scouting.
- Do not create Checkout until the user agrees to subscribe.
- Do not call or invent unsupported public market-feed primitives.
- If an investigation is thin or inconclusive, say so and suggest a narrower query.
