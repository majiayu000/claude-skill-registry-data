---
name: plugins
description: Enable/disable Claude Code plugins on demand. Use when user wants to activate a plugin like playwright, figma, stripe, github, etc.
---

# Plugin Manager

Enable or disable plugins on demand to save tokens. Only `context7` is always-on.

## Available Plugins

| Plugin | Use Case |
|--------|----------|
| `playwright` | Browser automation, UI testing |
| `frontend-design` | UI/UX implementation |
| `figma` | Figma design integration |
| `github` | GitHub PR/issue workflows |
| `supabase` | Supabase database |
| `stripe` | Stripe payments |
| `serena` | Code analysis |
| `feature-dev` | Guided feature development |
| `agent-sdk-dev` | Claude Agent SDK |
| `security-guidance` | Security review |
| `claude-md-management` | CLAUDE.md management |

## How to Enable

To enable a plugin, edit `~/.claude/settings.json` and set the plugin to `true`:

```json
"<plugin-name>@claude-plugins-official": true
```

Then restart the session (`/exit` + reopen) for changes to take effect.

## How to Disable

Set the plugin back to `false` in `~/.claude/settings.json`.

## Quick Toggle Script

```bash
# Enable
python3 -c "
import json
with open('$HOME/.claude/settings.json','r+') as f:
    d=json.load(f); d['enabledPlugins']['PLUGIN@claude-plugins-official']=True
    f.seek(0); json.dump(d,f,indent=2); f.truncate()
"

# Disable
python3 -c "
import json
with open('$HOME/.claude/settings.json','r+') as f:
    d=json.load(f); d['enabledPlugins']['PLUGIN@claude-plugins-official']=False
    f.seek(0); json.dump(d,f,indent=2); f.truncate()
"
```

Replace `PLUGIN` with the plugin name (e.g., `playwright`, `figma`).
