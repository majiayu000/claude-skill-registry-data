---
name: minimax
description: Switch to MiniMax AI model
tools: Bash
disable-model-invocation: true
---

# MiniMax Model Switch

## Trigger
When user says "/minimax" or requests to switch to MiniMax

## Action
Execute the MiniMax model switch:

```bash
source ~/.claude/model-switch.sh && claude-minimax MiniMax-M2.5
```

## Available Models
- **MiniMax-M2.5** — Peak performance, complex reasoning (default)
- **MiniMax-M2.5-lightning** — Same quality, faster output
- **MiniMax-M2.1** — Multi-language coding (~60 tps)
- **MiniMax-M2.1-lightning** — Fast coding (~100 tps)
- **MiniMax-M2** — Agentic capabilities

## Usage
```
/minimax           — Switch to MiniMax M2.5 (default)
/minimax lightning — Switch to MiniMax M2.5-lightning
/minimax fast      — Switch to MiniMax M2.1-lightning
/minimax coding    — Switch to MiniMax M2.1
```

## Notes
- MiniMax is Anthropic-compatible (no proxy needed)
- API: https://api.minimax.io/anthropic
- Best for: coding, reasoning, general tasks
