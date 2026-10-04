---
name: glm
description: Switch to Z.AI GLM model
tools: Bash
disable-model-invocation: true
---

# Z.AI GLM Model Switch

## Trigger
When user says "/glm" or requests to switch to GLM/Z.AI

## Action
Execute the GLM model switch:

```bash
source ~/.claude/model-switch.sh && claude-zai GLM-5
```

## Available Models
- **GLM-5** — Latest generation (replaces Opus/Sonnet)
- **GLM-4.7** — Advanced reasoning
- **GLM-4.6** — Standard
- **GLM-4.5-Air** — Lightweight, fast (replaces Haiku)

## Vision & Generation
- Vision: GLM-4.6V, GLM-4.5V
- Image: GLM-Image, CogView-4
- Video: CogVideoX-3, Vidu-Q1, Vidu-2

## Usage
```
/glm          — Switch to GLM-5 (default)
/glm fast     — Switch to GLM-4.5-Air
/glm vision   — Switch to GLM-4.6V
```

## Notes
- Z.AI is Anthropic-compatible (no proxy needed)
- API: https://api.z.ai/api/anthropic
- Best for: vision tasks, image generation, cheap pricing
