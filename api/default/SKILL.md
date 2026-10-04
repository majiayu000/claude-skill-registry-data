---
name: default
description: Switch back to Anthropic Claude default
tools: Bash
disable-model-invocation: true
---

# Default Model Switch

## Trigger
When user says "/default" or requests to switch back to Claude

## Action
Execute the default model switch:

```bash
source ~/.claude/model-switch.sh && claude-default
```

## What It Does
- Switches back to Anthropic Claude default
- Uses standard Anthropic API endpoint
- Restores original API key

## Available Models (Anthropic)
- **opus** — Most capable, complex reasoning
- **sonnet** — Balanced, general purpose
- **haiku** — Fast, lightweight

## Usage
```
/default     — Switch to default Claude
/opus       — Switch to Claude Opus
/sonnet     — Switch to Claude Sonnet
/haiku      — Switch to Claude Haiku
```

## Notes
- Default uses Anthropic's API directly
- Best for: general tasks, compatibility
