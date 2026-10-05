---
name: vision
description: Call vision models (Doubao, Qwen, DeepSeek, OpenAI) to analyze images. Use when you need to understand screenshots, UI layouts, diagrams, or any image content. Supports png/jpg/webp/gif.
---

# vision

Multi-provider vision tool. Call various vision models to describe images. Feed it a prompt + image path, get back a text description.

## When to use this tool

If you can already see and understand the image yourself (native multimodal model), skip this tool — analyze it directly.

A SessionStart hook normally announces this session's routing status up front. If that context isn't visible (e.g. compacted out of a long conversation, or the hook isn't installed), check before calling this tool:

```bash
python vision.py --check-routing
```

- `native` → you already have native image understanding this session; don't call this tool.
- `external` (default) → proceed with the quick start below.

## Quick start

```bash
python vision.py [--provider <name>] <image_path> <prompt>
```

When `--provider` is omitted, the provider is resolved by: `--provider` flag > `VISION_PROVIDER` env > first API key found.

## Providers

### doubao (Volcengine Ark)

- API key: `DOUBAO_API_KEY`
- Default model: `doubao-seed-2-0-pro-260215`
- Custom endpoint: `DOUBAO_BASE_URL`

### qwen (DashScope)

- API key: `DASHSCOPE_API_KEY`
- Default model: `qwen-vl-max`
- Custom endpoint: `DASHSCOPE_BASE_URL`
- Available models: `qwen-vl-max`, `qwen-vl-plus`, `qvq-max`

### deepseek (DeepSeek)

- API key: `DEEPSEEK_API_KEY`
- Default model: `deepseek-v4-flash-vision-exp`
- Custom endpoint: `DEEPSEEK_BASE_URL`
- Only `deepseek-v4-flash-vision-exp` accepts images — `deepseek-v4-flash` and `deepseek-v4-pro` are text-only and reject image input with an error.

### openai (GPT-4o)

- API key: `OPENAI_API_KEY`
- Default model: `gpt-4o`
- Custom endpoint: `OPENAI_BASE_URL`
- Also works with any OpenAI-compatible endpoint.

### anthropic (Claude)

- API key: `ANTHROPIC_API_KEY`
- Default model: `claude-sonnet-5`
- Custom endpoint: `ANTHROPIC_BASE_URL`
- Requires the `anthropic` package (`pip install anthropic`); it's imported lazily so other providers work without it.

### any custom provider

Any `--provider` name outside the built-in ones is resolved dynamically from
environment variables named after it — no code changes needed:

| Env Var | Required | Notes |
|---------|----------|-------|
| `{NAME}_API_KEY` | yes | checked at request time, same as built-ins |
| `{NAME}_BASE_URL` | yes | no default — arbitrary endpoint |
| `{NAME}_MODEL` | yes | no default (or set global `VISION_MODEL` instead) |
| `{NAME}_PROTOCOL` | no | `openai` (default) or `anthropic` — picks the request shape |

`openai` covers essentially every OpenAI-compatible endpoint (vLLM, Ollama,
LiteLLM, OpenRouter, Azure OpenAI, self-hosted proxies, ...). Use
`{NAME}_PROTOCOL=anthropic` only if the endpoint speaks the Anthropic Messages
API shape.

```bash
export MYAPI_API_KEY="sk-xxx"
export MYAPI_BASE_URL="https://my-endpoint.example.com/v1"
export MYAPI_MODEL="my-vision-model"
python vision.py --provider myapi "screenshot.png" "describe this"
```

If `{NAME}_BASE_URL` or `{NAME}_MODEL` is missing, the tool prints exactly which
variables to set instead of a generic "unknown provider" error.

## Configuration

| Env Var | Scope | Default |
|----------|-------|---------|
| `VISION_PROVIDER` | Default provider (built-in or custom name) | auto-detect (built-ins only) |
| `VISION_MODEL` | Override model (all providers) | provider default |
| `{PROVIDER}_MODEL` | Override model (per provider) | — |
| `{PROVIDER}_BASE_URL` | Override/define endpoint (per provider) | built-in default, or required for custom |
| `{PROVIDER}_PROTOCOL` | Request shape for a custom provider: `openai` \| `anthropic` | `openai` |
| `VISION_TEMPERATURE` | Response creativity 0–1 | `0` |
| `VISION_MAX_TOKENS` | Max response tokens | `4096` |

Note: auto-detect (no `--provider` / `VISION_PROVIDER` set) only scans the
built-in providers' API keys — a custom provider must always be named explicitly.

## Examples

```bash
# Auto-detect provider from API keys
python vision.py "screenshot.png" "Describe the page layout and any visible UI issues."

# Explicit provider
python vision.py --provider qwen "mockup.png" "List all components, colors, and spacing patterns."

# Custom model
QWEN_MODEL=qvq-max python vision.py --provider qwen "diagram.png" "Explain the architecture."

# GPT-4o for visual regression
python vision.py -p openai "after.png" "Compare with app design spec, flag differences."

# Fully custom provider (self-hosted, third-party proxy, any OpenAI-compatible endpoint)
MYAPI_API_KEY=sk-xxx MYAPI_BASE_URL=https://host/v1 MYAPI_MODEL=my-model \
  python vision.py --provider myapi "ui.png" "Analyze layout issues"
```
