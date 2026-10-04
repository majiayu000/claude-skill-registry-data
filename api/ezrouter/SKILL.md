---
name: ezrouter
description: Set up and use EZRouter — unified LLM API with one key for Claude, GPT, and Gemini. 2x credits on every purchase. Native API compatibility for each provider.
---

# EZRouter — Unified LLM API

EZRouter gives you **one API key** to access Claude, GPT, and Gemini models through **native API-compatible** endpoints. Pay once, get **2x credits**, with automatic failover across providers.

**Dashboard:** https://openrouter.ezsite.ai

---

## Quick Setup

1. Sign up at https://openrouter.ezsite.ai
2. Add credits (you get **2x** what you pay — $5 becomes $10)
3. Create an API key (prefix: `cr_`)
4. Use the appropriate base URL for your tool or provider

---

## Base URLs

| Provider | Base URL | Use With |
|----------|----------|----------|
| **Claude / Anthropic** | `https://openrouter.ezsite.ai/api/claude` | Claude Code, Anthropic SDK |
| **OpenAI** | `https://openrouter.ezsite.ai/api/openai/v1` | Cursor, OpenAI SDK, ChatGPT-compatible tools |
| **Gemini** | `https://openrouter.ezsite.ai/api/gemini` | Gemini SDK, Google AI tools |

---

## Integration Examples

### Claude Code

```bash
# Set environment variables
export ANTHROPIC_BASE_URL=https://openrouter.ezsite.ai/api/claude
export ANTHROPIC_API_KEY=your_cr_key_here

# Run Claude Code as usual
claude
```

### OpenClaw

```jsonc
// openclaw.json
{
  "models": {
    "providers": {
      "ezrouter": {
        "baseUrl": "https://openrouter.ezsite.ai/api/claude",
        "apiKey": "${EZROUTER_API_KEY}",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-sonnet-4-6-20250627",
            "name": "Claude Sonnet 4.6",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 64000
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": "ezrouter/claude-sonnet-4-6-20250627"
    }
  }
}
```

```bash
export EZROUTER_API_KEY=your_cr_key_here
```

### Cursor / OpenAI-Compatible Tools

```
API Base URL: https://openrouter.ezsite.ai/api/openai/v1
API Key:      your_cr_key_here
```

---

## Native API Examples

### Claude — Messages API

```bash
curl https://openrouter.ezsite.ai/api/claude/v1/messages \
  -H "Authorization: Bearer your_cr_key_here" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### OpenAI — Responses API

```bash
curl https://openrouter.ezsite.ai/api/openai/v1/responses \
  -H "Authorization: Bearer your_cr_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "input": [
      {
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": "Hello"}]
      }
    ]
  }'
```

### OpenAI — Chat Completions API

```bash
curl https://openrouter.ezsite.ai/api/openai/v1/chat/completions \
  -H "Authorization: Bearer your_cr_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Gemini — GenerateContent API

```bash
curl https://openrouter.ezsite.ai/api/gemini/v1beta/models/gemini-2.5-flash:generateContent \
  -H "Authorization: Bearer your_cr_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"role": "user", "parts": [{"text": "Hello"}]}]
  }'
```

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_cr_key_here",
    base_url="https://openrouter.ezsite.ai/api/openai/v1"
)

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Python (Anthropic SDK)

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your_cr_key_here",
    base_url="https://openrouter.ezsite.ai/api/claude"
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

### TypeScript (OpenAI SDK)

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your_cr_key_here",
  baseURL: "https://openrouter.ezsite.ai/api/openai/v1",
});

const response = await client.chat.completions.create({
  model: "gpt-5",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

---

## Available Models

Models are updated dynamically. Query the models endpoint for each provider to get the current list:

```bash
# EZRouter format (no auth required) — includes pricing info
curl https://openrouter.ezsite.ai/api/model/list

# OpenAI format
curl https://openrouter.ezsite.ai/api/openai/v1/models \
  -H "Authorization: Bearer your_cr_key_here"

# Claude / Anthropic format
curl https://openrouter.ezsite.ai/api/claude/v1/models \
  -H "Authorization: Bearer your_cr_key_here"

# Gemini format
curl https://openrouter.ezsite.ai/api/gemini/v1beta/models \
  -H "Authorization: Bearer your_cr_key_here"
```

Supported providers: **Claude** (Opus, Sonnet, Haiku), **OpenAI** (GPT-5.x, GPT-4.1, GPT-4o, o3/o4, Codex), **Google Gemini** (Pro, Flash, Flash-Lite).

---

## Pricing

- **2x Credits:** Pay $5, get $10 in credits. Every dollar goes further.
- **Same rates as providers:** No markup on per-token pricing.
- **Pay-as-you-go:** No subscriptions. Add credits when you need them.
- **Minimum purchase:** $5 | **Maximum:** $1,000

---

## Links

- **Dashboard:** https://openrouter.ezsite.ai
- **Claude API:** https://openrouter.ezsite.ai/api/claude
- **OpenAI API:** https://openrouter.ezsite.ai/api/openai/v1
- **Gemini API:** https://openrouter.ezsite.ai/api/gemini
