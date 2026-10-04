---
name: switch-modes
description: Switch between AI models dynamically to optimize costs and performance. Use when the user says mode commands like "eco mode", "balanced mode", "smart mode", or "max mode", or when they want to check their current mode with "/modes status" or configure modes with "/modes setup".
license: MIT
metadata:
  author: serudda
  version: "1.0.0"
---

# Switch Modes

Dynamically switch between AI models to optimize costs and performance.

## When to Use This Skill

Activate this skill when the user mentions:

- Mode switching commands: `eco mode`, `balanced mode`, `smart mode`, `max mode`
- Status check: `/modes status`
- Configuration: `/modes setup`

## How It Works

The skill manages 4 predefined modes, each mapped to a specific model:

- **eco** → Cheapest model (for summaries, quick questions)
- **balanced** → Daily driver model (for general work)
- **smart** → Powerful model (for complex reasoning)
- **max** → Most powerful model (for critical tasks)

Configuration is stored in `~/.openclaw/workspace/switch-modes.json`.

## Step-by-Step Instructions

### 1. Detect Mode Commands

When the user message contains any of these patterns:

- `eco mode` or `eco` (standalone)
- `balanced mode` or `balanced`
- `smart mode` or `smart`
- `max mode` or `max`
- `/modes status`
- `/modes setup`

### 2. Handle Setup Command (`/modes setup`)

If the configuration file doesn't exist or user requests setup:

1. Use `AskUserQuestion` to gather model preferences for each mode:
   - **ECO mode**: Recommend `anthropic/claude-3.5-haiku`
   - **BALANCED mode**: Recommend `anthropic/claude-sonnet-4-5`
   - **SMART mode**: Recommend `anthropic/claude-opus-4-5`
   - **MAX mode**: Recommend `anthropic/claude-opus-4-6` or `openai/o1-pro`

2. Create/update `~/.openclaw/workspace/switch-modes.json` with the structure:

```json
{
	"eco": "model-id",
	"balanced": "model-id",
	"smart": "model-id",
	"max": "model-id"
}
```

3. Confirm setup completion to the user.

### 3. Handle Status Command (`/modes status`)

1. Read the OpenClaw config at `~/.openclaw/openclaw.json` to get current model
2. Read `~/.openclaw/workspace/switch-modes.json` to get mode mappings
3. Determine which mode is currently active by matching the current model
4. Display: `✅ Currently in [MODE] mode using [MODEL_ID]`

### 4. Handle Mode Switch Commands

When user requests a mode switch:

1. **Read configuration**:

   ```bash
   cat ~/.openclaw/workspace/switch-modes.json
   ```

   If file doesn't exist, prompt user to run `/modes setup` first.

2. **Get the target model** from the config based on requested mode (eco/balanced/smart/max)

3. **Update OpenClaw config**:
   - Read current config: `~/.openclaw/openclaw.json`
   - Update the `model` field with the new model ID
   - Write back to `~/.openclaw/openclaw.json`

4. **Confirm to user**:
   ```
   ✅ [MODE] mode activated
   Now using: [MODEL_ID]
   ```

## Examples

### Example 1: Mode Switch

```
User: eco mode
Agent: [reads switch-modes.json, gets model for "eco"]
Agent: [updates openclaw.json with new model]
Agent: ✅ ECO mode activated
      Now using: anthropic/claude-3.5-haiku
```

### Example 2: Status Check

```
User: /modes status
Agent: [reads openclaw.json for current model]
Agent: [reads switch-modes.json for mode mappings]
Agent: ✅ Currently in BALANCED mode using anthropic/claude-sonnet-4-5
```

### Example 3: First Time Setup

```
User: /modes setup
Agent: [uses AskUserQuestion for each mode]
Agent: [creates ~/.openclaw/workspace/switch-modes.json]
Agent: ✅ Setup complete! You can now use:
      - eco mode
      - balanced mode
      - smart mode
      - max mode
```

## File Locations

- **Configuration**: `~/.openclaw/workspace/switch-modes.json`
- **OpenClaw Config**: `~/.openclaw/openclaw.json`
- **Example Config**: See `example-config.json` in skill directory

## Common Edge Cases

1. **Config file missing**: Prompt user to run `/modes setup`
2. **Invalid model ID**: Show error and ask user to reconfigure that mode
3. **Model not available**: Suggest checking API keys and model access in OpenClaw
4. **Ambiguous input**: If just "eco" or "smart" without "mode", still treat as mode switch command
5. **Case insensitive**: Accept "ECO MODE", "Eco Mode", "eco mode" all the same

## Important Notes

- Mode switching is instant - no restart required
- Changes only affect the current session's default model
- Preserve all other settings in `openclaw.json` when updating model
- Always validate JSON before writing config files
- Use absolute paths: `~/.openclaw/...` not relative paths

## Reference

For detailed troubleshooting, supported models list, and FAQ, see [./REFERENCE.md](references/REFERENCE.md).
