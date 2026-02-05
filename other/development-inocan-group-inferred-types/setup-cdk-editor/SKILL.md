---
name: setup-cdk-editor
description: Use when setting up VS Code or Cursor for Claude Code - configures settings, installs recommended extensions, sets up keybindings, and creates workspace templates optimized for AI-assisted development
---

# Setup CDK Editor

## Overview

Editor configuration optimized for Claude Code development. Configures VS Code or Cursor with settings, extensions, and keybindings for seamless AI-assisted workflows.

## When to Use

- Setting up VS Code or Cursor for Claude development
- User asks about editor optimization for AI workflows
- Part of `setup-claude-dev-kit` bundle
- User wants extension recommendations or keybindings

## Quick Reference

| Component | Location |
|-----------|----------|
| User Settings | `~/.config/Code/User/settings.json` (Linux) or `~/Library/Application Support/Code/User/settings.json` (macOS) |
| Cursor Settings | `~/Library/Application Support/Cursor/User/settings.json` |
| Keybindings | Same dirs, `keybindings.json` |
| Workspace Template | `.vscode/settings.json` in project |

## Installation Steps

### 1. Detect Editor

```bash
# Check for VS Code
code --version 2>/dev/null && echo "VS Code installed"

# Check for Cursor
cursor --version 2>/dev/null && echo "Cursor installed"

# Determine settings path
if [[ "$OSTYPE" == "darwin"* ]]; then
  VSCODE_SETTINGS="$HOME/Library/Application Support/Code/User"
  CURSOR_SETTINGS="$HOME/Library/Application Support/Cursor/User"
else
  VSCODE_SETTINGS="$HOME/.config/Code/User"
  CURSOR_SETTINGS="$HOME/.config/Cursor/User"
fi
```

### 2. Install Recommended Extensions

Run these commands (works for both VS Code and Cursor):

```bash
# Core productivity
code --install-extension eamodio.gitlens
code --install-extension usernamehw.errorlens
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint

# Claude-specific enhancements
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension wayou.vscode-todo-highlight
code --install-extension gruntfuggly.todo-tree

# Optional but recommended
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension bradlc.vscode-tailwindcss
```

For Cursor, replace `code` with `cursor`.

### 3. Configure User Settings

Add to `settings.json`:

```json
{
  // Editor behavior for Claude workflows
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "editor.inlineSuggest.enabled": true,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",
  "editor.rulers": [80, 120],

  // Terminal for Claude Code
  "terminal.integrated.fontFamily": "MesloLGS NF",
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.scrollback": 10000,

  // Files
  "files.autoSave": "onFocusChange",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/__pycache__": true
  },

  // Search optimization
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.git": true
  },

  // Error Lens (less intrusive)
  "errorLens.enabledDiagnosticLevels": ["error", "warning"],
  "errorLens.delay": 500,

  // GitLens (reduce noise)
  "gitlens.codeLens.enabled": false,
  "gitlens.currentLine.enabled": true,
  "gitlens.hovers.currentLine.over": "line",

  // Spell checker
  "cSpell.enableFiletypes": ["markdown", "plaintext"],
  "cSpell.words": ["claude", "anthropic", "cdk"]
}
```

### 4. Configure Keybindings

Add to `keybindings.json`:

```json
[
  // Quick terminal access (for Claude Code)
  {
    "key": "cmd+`",
    "command": "workbench.action.terminal.toggleTerminal"
  },
  // Focus terminal
  {
    "key": "cmd+shift+`",
    "command": "workbench.action.terminal.focus"
  },
  // Quick file navigation
  {
    "key": "cmd+p",
    "command": "workbench.action.quickOpen"
  },
  // Toggle sidebar (more screen space for code)
  {
    "key": "cmd+b",
    "command": "workbench.action.toggleSidebarVisibility"
  },
  // Format document
  {
    "key": "shift+alt+f",
    "command": "editor.action.formatDocument"
  },
  // Go to definition (useful when reviewing Claude changes)
  {
    "key": "cmd+click",
    "command": "editor.action.goToDeclaration"
  }
]
```

### 5. Create Workspace Template

Create `.vscode/settings.json` template for projects:

```json
{
  // Project-specific settings
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,

  // Recommended for Claude Code projects
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true
  },

  // Task runner integration
  "task.autoDetect": "on"
}
```

Create `.vscode/extensions.json` for team recommendations:

```json
{
  "recommendations": [
    "eamodio.gitlens",
    "usernamehw.errorlens",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### 6. Cursor-Specific Settings

If using Cursor, add these additional settings:

```json
{
  // Cursor AI settings
  "cursor.cpp.enableCopilot": false,

  // Tab completion behavior
  "cursor.enableTabComplete": true,

  // Reduce context window usage
  "cursor.contextFiles.maxLines": 500
}
```

## Verification

```bash
# Check extensions installed
code --list-extensions | grep -E "(gitlens|errorlens|prettier)" && echo "Core extensions installed"

# Check settings file exists
[ -f "$VSCODE_SETTINGS/settings.json" ] && echo "Settings configured"

# Check terminal font
grep -q "MesloLGS" "$VSCODE_SETTINGS/settings.json" && echo "Terminal font set"
```

## Adaptation Mode

When existing editor setup detected:

1. **Backup settings:**
```bash
mkdir -p ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)
cp "$VSCODE_SETTINGS/settings.json" ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/vscode-settings.json.bak
cp "$VSCODE_SETTINGS/keybindings.json" ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/vscode-keybindings.json.bak
```

2. **Check for conflicts:**
- Existing formatters → Ask: keep or use Prettier?
- Custom keybindings → Merge, don't overwrite
- Conflicting extensions → Warn and skip

3. **Merge settings:**
```bash
# Use jq to merge (preferred) or manual merge
# CDK settings have lower precedence than user customizations
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Extensions not installing | Run VS Code as admin or check `code` in PATH |
| Settings not applying | Restart VS Code after changes |
| Terminal font wrong | Ensure MesloLGS NF installed (see shell component) |
| Cursor conflicts | Some settings differ between Cursor versions |
| Format on save not working | Check formatter extension is installed and configured |

## Updating

```bash
# Update all extensions
code --update-extensions

# Sync settings (if using Settings Sync)
# Settings Sync is built into VS Code
```

## Extension Details

| Extension | Purpose |
|-----------|---------|
| GitLens | See git blame, history, branches inline |
| Error Lens | Show errors inline at end of line |
| Prettier | Consistent code formatting |
| ESLint | JavaScript/TypeScript linting |
| Code Spell Checker | Catch typos in docs and comments |
| Todo Tree | Track TODO/FIXME comments |
