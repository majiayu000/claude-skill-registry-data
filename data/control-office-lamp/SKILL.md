---
name: control-office-lamp
description: Control office lamp via Home Assistant. Use when the user asks to turn on, turn off, or toggle their office lamp, or check its status. Triggers on phrases like "turn on my lamp", "office light on/off", "toggle the lamp", or "is my lamp on".
allowed-tools:
  - Bash
  - Read
---

# Home Assistant Office Lamp Control

Control the office lamp through Home Assistant's REST API.

## Setup (First-Time Only)

Create your config file at `~/.claude/skill-config/control-office-lamp/config.json`:

```json
{
  "url": "http://your-home-assistant:8123",
  "token": "YOUR_LONG_LIVED_ACCESS_TOKEN_HERE",
  "entity_id": "light.office_lamp"
}
```

This location persists across skill updates.

To create a Long-Lived Access Token:
1. Open Home Assistant -> Profile (bottom-left)
2. Scroll to "Long-Lived Access Tokens" -> Create Token
3. Copy the token into config.json

**Config lookup order:**
1. `HA_CONFIG_PATH` environment variable
2. `~/.claude/skill-config/control-office-lamp/config.json` (recommended)
3. `${CLAUDE_PLUGIN_ROOT}/skills/control-office-lamp/config.json` (plugin root)
4. `<script-directory>/../config.json` (fallback)

## Usage

The script is located relative to the plugin root using `${CLAUDE_PLUGIN_ROOT}`:

```bash
# Turn lamp on
uv run "${CLAUDE_PLUGIN_ROOT}/skills/control-office-lamp/scripts/lamp_control.py" on

# Turn lamp off
uv run "${CLAUDE_PLUGIN_ROOT}/skills/control-office-lamp/scripts/lamp_control.py" off

# Toggle lamp state
uv run "${CLAUDE_PLUGIN_ROOT}/skills/control-office-lamp/scripts/lamp_control.py" toggle

# Check current status
uv run "${CLAUDE_PLUGIN_ROOT}/skills/control-office-lamp/scripts/lamp_control.py" status
```

## Response Handling

**Success response:**
```json
{"success": true, "action": "turn_on", "entity_id": "light.office_lamp", "response": [...]}
```

**Error response:**
```json
{"success": false, "error": "Connection failed: ..."}
```

If errors occur, verify:
1. Home Assistant is running at the configured URL
2. The token is valid and not expired
3. The entity_id exists in Home Assistant
