---
name: gemini
description: Switch to Google Gemini model
tools: Bash
disable-model-invocation: true
---

# Google Gemini Model Switch

## Trigger
When user says "/gemini" or requests to switch to Gemini

## Action
Execute the Gemini model switch:

```bash
source ~/.claude/model-switch.sh && claude-gemini gemini-3-pro-preview
```

## Available Models
- **gemini-3-pro-preview** — Gemini 3 Pro (latest, most capable)
- **gemini-3-flash-preview** — Gemini 3 Flash (fast, pro-level)
- **gemini-3-pro-image-preview** — Nano Banana Pro 4K (image generation)
- **gemini-2.5-pro** — Gemini 2.5 Pro
- **gemini-2.5-flash** — Gemini 2.5 Flash (fast)
- **gemini-2.5-flash-lite** — Cheapest option

## Usage
```
/gemini          — Switch to Gemini 3 Pro (default)
/gemini fast     — Switch to Gemini 3 Flash
/gemini image    — Switch to Nano Banana Pro 4K
/gemini 2.5     — Switch to Gemini 2.5 Pro
```

## Notes
- Gemini requires the proxy server (auto-starts)
- Proxy: http://127.0.0.1:8082
- Best for: reasoning, image generation, multimodal tasks
