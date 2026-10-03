---
name: hermes-custom-vision-provider
description: Configure custom/OpenAI-compatible vision providers in Hermes Agent (Kimi, DeepSeek, Azure, etc.)
---

# Hermes Custom Vision Provider Setup

## When to Use
When you want to use a custom/OpenAI-compatible vision provider (Kimi/Moonshot, DeepSeek, Azure, etc.) instead of the default OpenRouter auto-detection.

## The Provider Key Insight

**`provider: openai` ≠ "use an OpenAI-compatible endpoint".**

It resolves `openai` through `_PROVIDER_ALIASES` and routes to the **actual OpenAI provider**, which:
- Ignores your `base_url` setting
- Ignores `api_key_env` references
- Uses only the `OPENAI_API_KEY` from `.env`

**For custom endpoints, use `provider: custom`.**

Only `provider: custom` activates the code path that reads:
- `base_url`
- `model`
- `api_key` OR `api_key_env`

## Config Structure

```yaml
auxiliary:
  vision:
    provider: custom          # NOT "openai"
    model: moonshot-v1-8k-vision-preview
    base_url: https://api.moonshot.cn/v1
    api_key_env: MOONSHOT_API_KEY   # Reference .env var, NOT hardcoded key
    timeout: 120
```

## Common Pitfalls

### 1. Empty api_key overrides api_key_env
```yaml
# WRONG — empty string is truthy and overrides the env reference
api_key: ''
api_key_env: MOONSHOT_API_KEY

# CORRECT — omit api_key entirely when using api_key_env
api_key_env: MOONSHOT_API_KEY
```

### 2. provider: openai goes to OpenAI, not your endpoint
```yaml
# WRONG — uses OpenAI's API key, ignores base_url
provider: openai
base_url: https://api.moonshot.cn/v1

# CORRECT — activates custom endpoint path
provider: custom
base_url: https://api.moonshot.cn/v1
```

## How to Debug Vision Auth Issues

When vision returns 401 on Telegram but works in CLI:
1. Check `errors.log` — if it says `Invalid Authentication` with an OpenAI-style error body, the gateway is using the wrong API key
2. The gateway process loads config at startup — config changes require a restart
3. Use `provider: custom` with `api_key_env` pointing to your `.env` variable

## Restarting the Gateway

```bash
# Find running gateway processes
ps aux | grep "hermes_cli.main gateway"

# Kill and restart (--replace prevents "token already in use")
kill <PID>
nohup ~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace > ~/.hermes/logs/gateway.log 2>&1 &
```

## Available Kimi/Moonshot Vision Models

```
moonshot-v1-8k-vision-preview   (8k context)
moonshot-v1-32k-vision-preview  (32k context)
moonshot-v1-128k-vision-preview (128k context)
kimi-k2.5                       (latest multimodal, requires temperature=1)
```

Note: `kimi-k2.5` requires `temperature=1` exactly, but `vision_tools.py` hardcodes `temperature: 0.1`, so it will fail with `invalid temperature`. Use `moonshot-v1-8k-vision-preview` instead.
