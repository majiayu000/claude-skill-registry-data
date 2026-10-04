---
name: free-llm
description: Query free LLM APIs via OpenRouter, Groq, Cerebras, Google AI, and other free providers. Switch between providers and compare models.

# Trigger words that activate this skill
triggers:
  - /free-llm
  - free llm
  - openrouter
  - groq api
  - cerebras api
  - alternative llm
  - free api
---

# Free LLM API Resources

Access multiple free LLM providers directly from Claude Code.

## Supported Providers

| Provider | Command | Limites |
|----------|---------|---------|
| **OpenRouter** | `/free-llm openrouter "prompt"` | 20/min, 50/jour |
| **Groq** | `/free-llm groq "prompt"` | 1M tokens/jour |
| **Cerebras** | `/free-llm cerebras "prompt"` | Beta = gratuit |
| **Google** | `/free-llm google "prompt"` | Généreux |
| **Mistral** | `/free-llm mistral "prompt"` | 500k tokens/mois |

## Usage

### Basic Query

```claude
/free-llm openrouter "Explique la relativité restreinte"
/free-llm groq "Génère une fonction Python pour parser du JSON"
/free-llm cerebras "Résume ce texte"
```

### Compare Models

```claude
/free-llm compare "Même prompt" --providers openrouter,groq
```

### Check Status

```claude
/free-llm status
```

## Available Models

### OpenRouter
- `anthropic/claude-3.5-sonnet` (rate limits apply)
- `meta-llama/llama-3.1-70b-instruct`
- `google/gemma-2-27b-it`
- `mistralai/mistral-large`

### Groq
- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

### Cerebras
- `llama3.1-70b`
- `llama3.1-8b`

### Google
- `gemini-1.5-pro`
- `gemini-1.5-flash`

## Environment Variables

```bash
# Required for respective providers
OPENROUTER_API_KEY=sk-or-v1-...
GROQ_API_KEY=gsk_...
CEREBRAS_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
```

## Use Cases

1. **Fallback** when Claude rate limits hit
2. **Model comparison** - test same prompt across providers
3. **Cost optimization** - use free tiers for non-critical tasks
4. **Access to non-Anthropic models** - Llama, Gemma, Mistral

## Limitations

- These are for supplemental use, not replacement for Claude
- Rate limits vary by provider
- Some providers require signup
- Free tiers may have reduced capabilities

## Links

- [OpenRouter](https://openrouter.ai)
- [Groq Console](https://console.groq.com)
- [Cerebras Cloud](https://cloud.cerebras.ai)
- [Google AI Studio](https://makersuite.google.com)

---

# Implementation

When user invokes /free-llm, use the appropriate MCP server or curl command to query the selected provider.

For OpenRouter:
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/llama-3.1-70b-instruct",
    "messages": [{"role": "user", "content": "PROMPT"}]
  }'
```

For Groq:
```bash
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-70b-versatile",
    "messages": [{"role": "user", "content": "PROMPT"}]
  }'
```

For Cerebras:
```bash
curl https://api.cerebras.ai/v1/chat/completions \
  -H "Authorization: Bearer $CEREBRAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1-70b",
    "messages": [{"role": "user", "content": "PROMPT"}]
  }'
```

For Google (Gemini):
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"role": "user", "parts": [{"text": "PROMPT"}]}]
  }'
```
