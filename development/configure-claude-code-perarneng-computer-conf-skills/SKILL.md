---
name: configure-claude-code
description: Applies personalized Claude Code settings. Use when setting up Claude Code preferences on a new machine.
---

## Prerequisites
- Claude Code installed
- jq installed (for JSON manipulation)

## Configuration

### Settings to apply

| Setting | Value | Description |
|---------|-------|-------------|
| `includeCoAuthoredBy` | `false` | Disable co-authored-by line in commits |
| `statusLine` | custom command | Custom status line using ~/.claude/statusline.sh |

## Installation

### 1. Ensure settings directory exists

```bash
mkdir -p ~/.claude
```

### 2. Install status line script

Copy the status line script from this repository:

```bash
cp scripts/status_line.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

### 3. Apply settings

If `~/.claude/settings.json` doesn't exist, create it:

```bash
echo '{}' > ~/.claude/settings.json
```

Update the settings using jq:

```bash
jq '. + {"includeCoAuthoredBy": false, "statusLine": {"type": "command", "command": "~/.claude/statusline.sh", "padding": 0}}' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

## Verify

```bash
cat ~/.claude/settings.json | jq '.includeCoAuthoredBy'
```

Should output: `false`

```bash
cat ~/.claude/settings.json | jq '.statusLine'
```

Should output the statusLine configuration object.

```bash
ls -la ~/.claude/statusline.sh
```

Should show the script with execute permissions.

## Update

Re-run the installation steps to apply any new settings added to this skill.

## Uninstall

Remove the settings or reset to defaults:

```bash
jq 'del(.includeCoAuthoredBy, .statusLine)' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```
