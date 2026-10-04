---
name: switch
description: Interactive model picker - choose AI provider
tools: Bash
disable-model-invocation: true
---

# Model Switcher

## Trigger
When user says "/switch" or "/model" to change AI provider

## Action
Launch the interactive model picker:

```bash
source ~/.claude/model-switch.sh && claude-switch
```

## Model Options

### Direct Providers (no proxy needed)
| # | Provider | Model | Best For |
|---|----------|-------|----------|
| 1 | Claude | Anthropic (default) | General tasks |
| 2 | MiniMax | M2.5 | Peak reasoning |
| 3 | MiniMax | M2.5-lightning | Fast reasoning |
| 4 | MiniMax | M2.1 | Coding (~60 tps) |
| 5 | MiniMax | M2.1-lightning | Fast coding (~100 tps) |
| 6 | MiniMax | M2 | Agentic tasks |
| 7 | Z.AI | GLM-5 | Latest GLM |
| 8 | Z.AI | GLM-4.7 | Advanced reasoning |
| 9 | Z.AI | GLM-4.5-Air | Fast/lightweight |

### Via Proxy (auto-starts)
| # | Provider | Model | Best For |
|---|----------|-------|----------|
| 10 | Gemini | 3 Pro | Most capable |
| 11 | Gemini | 3 Flash | Fast, pro-level |
| 12 | Gemini | Nano Banana Pro 4K | Image generation |
| 13 | Gemini | 2.5 Pro | Previous gen |
| 14 | Gemini | 2.5 Flash | Previous gen fast |
| 15 | NVIDIA | Nemotron Super 49B | Open source |
| 16 | NVIDIA | Nemotron Ultra 253B | Large context |
| 17 | NVIDIA | DeepSeek R1 | Reasoning |
| 18 | Infermatic | Various | Open source models |

## Quick Commands
```
/minimax   — MiniMax M2.5 (default)
/glm       — Z.AI GLM-5
/gemini    — Gemini 3 Pro
/default   — Back to Anthropic
/status    — Show current model
```

## Utility Commands
```
s  — Show status
p  — Stop proxy
```
