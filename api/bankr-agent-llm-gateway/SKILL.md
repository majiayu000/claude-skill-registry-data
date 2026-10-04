---
name: Bankr Agent - LLM Gateway
description: This skill should be used when the user asks about "LLM gateway", "Bankr LLM", "LLM credits", "top up credits", "auto top-up", "llm.bankr.bot", "Claude Code gateway", "OpenClaw setup", "Cursor setup", "OpenCode setup", "LLM models", or any LLM gateway configuration or usage topic.
version: 1.0.0
---

# LLM Gateway

The Bankr LLM Gateway is a unified API for Claude, Gemini, GPT, and other models — multi-provider access, cost tracking, automatic failover, and SDK compatibility through a single endpoint.

**Base URL:** `https://llm.bankr.bot`

## Authentication

Uses your **LLM key**. Resolution order:

1. `BANKR_LLM_KEY` environment variable
2. `llmKey` in `~/.bankr/config.json`
3. Falls back to `BANKR_API_KEY`

Most users only need one key for both agent API and LLM gateway.

## Credits

**New wallets start with $0 LLM credits.** Top up before first use or all requests return HTTP 402.

LLM credits (USD) and trading wallet (crypto) are **completely separate balances**.

```bash
bankr llm credits                          # Check balance
bankr llm credits add 25                   # Top up $25 (USDC)
bankr llm credits add 50 --token 0x...     # Top up from specific token
bankr llm credits auto --enable --amount 25 --threshold 5 --tokens USDC  # Auto top-up
bankr llm credits auto --disable           # Disable auto top-up
```

## Available Models

| Model | Provider | Best For |
|-------|----------|----------|
| `claude-opus-4.6` | Anthropic | Most capable, advanced reasoning |
| `claude-sonnet-4.6` | Anthropic | Balanced speed and quality |
| `claude-haiku-4.5` | Anthropic | Fast, cost-effective |
| `gemini-3-pro` | Google | Long context (2M tokens) |
| `gemini-3-flash` | Google | High throughput |
| `gpt-5.2` | OpenAI | Advanced reasoning |
| `gpt-5-mini` | OpenAI | Fast, economical |
| `kimi-k2.5` | Moonshot AI | Long-context reasoning |
| `qwen3-coder` | Alibaba | Code generation |

```bash
bankr llm models   # Fetch live model list
```

## Tool Integrations

### Claude Code

```bash
# Launch directly (recommended)
bankr llm claude
bankr llm claude --model claude-sonnet-4.6

# Or set env vars
bankr llm setup claude
# Outputs: export ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN
```

### OpenClaw

```bash
bankr llm setup openclaw --install   # Auto-install provider config
```

In OpenClaw, prefix model IDs with `bankr/` (e.g. `bankr/claude-sonnet-4.6`).

### OpenCode

```bash
bankr llm setup opencode --install   # Auto-install provider config
```

### Cursor

```bash
bankr llm setup cursor   # Get step-by-step setup instructions
```

## Direct SDK Usage

The gateway works with standard OpenAI and Anthropic SDKs — just override the base URL.

**OpenAI format:**
```bash
curl -X POST "https://llm.bankr.bot/v1/chat/completions" \
  -H "Authorization: Bearer $BANKR_LLM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4.6", "messages": [{"role": "user", "content": "Hello"}]}'
```

**Anthropic format:**
```bash
curl -X POST "https://llm.bankr.bot/v1/messages" \
  -H "x-api-key: $BANKR_LLM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4.6", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello"}]}'
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Verify key: `bankr config get llmKey` |
| 402 Payment Required | Top up credits: `bankr llm credits add 25` |
| Model not found | Check exact ID: `bankr llm models` |
| Claude Code not found | Install Claude Code separately |
