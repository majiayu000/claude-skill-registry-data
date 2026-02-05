---
name: peekaboo
description: "macOS UI automation and screenshot capture tool. Use when working with macOS applications and needing to: (1) Capture screenshots with UI element annotations, (2) Automate UI interactions (clicking, typing, scrolling), (3) Control applications and windows programmatically, (4) Navigate menus and dialogs, (5) Perform visual analysis of screens, (6) Create multi-step automation workflows. Requires macOS 15.0+ with Screen Recording and Accessibility permissions."
---

# Peekaboo

Peekaboo is a macOS CLI tool that enables AI agents to capture screenshots, interact with UI elements, and automate macOS applications through accessibility APIs.

## Overview

Peekaboo provides programmatic control over macOS UI through three main capabilities:

1. **Screen Capture** - Capture screenshots with annotated UI elements and accessibility IDs
2. **UI Automation** - Click, type, scroll, and interact with UI elements by identifier or natural language
3. **Application Control** - Manage windows, applications, menus, and system dialogs

## Prerequisites

**Installation:**
```bash
brew install steipete/tap/peekaboo
```

**Required Permissions:**
- Screen Recording permission
- Accessibility permission

Check permissions:
```bash
peekaboo permissions status
peekaboo permissions grant
```

## Quick Start

### Capture Screenshot with Element Annotations

```bash
# Capture current screen with UI element IDs
peekaboo see --mode screen

# Capture specific application
peekaboo see --app Safari

# Get JSON output for programmatic use
peekaboo see --app "Visual Studio Code" --json-output
```

### Click UI Elements

```bash
# Click by element text/identifier
peekaboo click --on "Reload this page"

# Click using snapshot ID for accuracy
peekaboo see --app Safari --json-output > output.json
SNAPSHOT=$(jq -r '.data.snapshot_id' output.json)
peekaboo click --on "Submit" --snapshot "$SNAPSHOT"
```

### Type Text

```bash
# Type into focused element
peekaboo type --text "Hello World"

# Clear field first, then type
peekaboo type --text "user@example.com" --clear

# Type with delay between keystrokes
peekaboo type --text "password" --delay-ms 50
```

### Natural Language Automation

```bash
# Use AI agent for multi-step tasks
peekaboo agent "Open Notes and create a TODO list with three items"

# Shorthand syntax
peekaboo "Take a screenshot of Safari and save to Desktop"

# Dry run to see planned steps
peekaboo agent "Organize Desktop files" --dry-run
```

## Core Capabilities

### 1. Screen Capture & Analysis

**See UI Elements:**
```bash
peekaboo see --app Safari --retina
```

Captures screen with accessibility annotations, returning element IDs that can be used for clicking/interaction.

**Static Screenshots:**
```bash
peekaboo image --mode screen --path ~/Desktop/screenshot.png
peekaboo image --mode window --retina --analyze
```

Options: `screen`, `window`, `menu` modes with optional AI analysis.

### 2. Mouse & Keyboard Automation

**Click elements:**
```bash
peekaboo click --on "button_id"
peekaboo click --on "Submit Form"
```

**Type text:**
```bash
peekaboo type --text "Search query"
```

**Press special keys:**
```bash
peekaboo press return
peekaboo press tab --repeat 3
peekaboo press escape
```

**Keyboard shortcuts:**
```bash
peekaboo hotkey cmd,s
peekaboo hotkey cmd,shift,t
```

**Mouse movements:**
```bash
peekaboo move --to 500,500
peekaboo drag --from 100,200 --to 300,400
peekaboo scroll --direction down --ticks 5
```

### 3. Window & Application Management

**Launch/quit applications:**
```bash
peekaboo app launch Safari
peekaboo app quit "Google Chrome"
peekaboo app switch Terminal
```

**Control windows:**
```bash
peekaboo window list
peekaboo window move --x 100 --y 100
peekaboo window resize --width 800 --height 600
peekaboo window set-bounds --x 0 --y 0 --width 1920 --height 1080
```

**Navigate Spaces:**
```bash
peekaboo space list
peekaboo space switch 2
peekaboo space move-window 3
```

### 4. Menu & Dialog Interaction

**Application menus:**
```bash
peekaboo menu list --app Safari
peekaboo menu click --app Safari --path "File > New Window"
```

**Menu bar (status bar):**
```bash
peekaboo menubar list
peekaboo menubar click "WiFi"
```

**Dock operations:**
```bash
peekaboo dock list
peekaboo dock launch Safari
peekaboo dock right-click Terminal
```

**System dialogs:**
```bash
peekaboo dialog list
peekaboo dialog click "OK"
peekaboo dialog input --text "filename.txt"
peekaboo dialog file --path "/Users/user/document.pdf"
```

### 5. Workflow Automation

**Scripted workflows:**
```bash
peekaboo run workflow.peekaboo.json
```

Workflow file format:
```json
{
  "name": "My Workflow",
  "steps": [
    {"action": "launch", "app": "Safari"},
    {"action": "type", "text": "https://example.com"},
    {"action": "press", "key": "return"},
    {"action": "sleep", "duration": 1000}
  ]
}
```

**AI-powered automation:**
```bash
peekaboo agent "Open Calculator and compute 15 * 23"
peekaboo agent "Create a new document in Pages" --model openai/gpt-5.1
```

## Common Patterns

### Element-Based Interaction Workflow

When interacting with specific UI elements, use this pattern:

1. Capture screen with element annotations
2. Extract snapshot ID
3. Use snapshot ID for accurate element targeting

```bash
# Step 1: Capture with annotations
peekaboo see --app Safari --json-output > ui.json

# Step 2: Extract snapshot
SNAPSHOT=$(jq -r '.data.snapshot_id' ui.json)

# Step 3: Interact with elements
peekaboo click --on "Reload" --snapshot "$SNAPSHOT"
peekaboo click --on "Search" --snapshot "$SNAPSHOT"
```

### Application Setup Workflow

```bash
# Launch and configure application window
peekaboo app launch Safari
peekaboo sleep --duration 500
peekaboo window set-bounds --x 0 --y 0 --width 1920 --height 1080
peekaboo sleep --duration 200
peekaboo menu click --app Safari --path "View > Show Toolbar"
```

### Screenshot & Analysis

```bash
# Capture retina screenshot with AI analysis
peekaboo image --mode screen --retina --analyze --path analysis.png
```

### Multi-Step Form Filling

```bash
peekaboo click --on "Name field"
peekaboo type --text "John Doe" --clear
peekaboo press tab
peekaboo type --text "john@example.com"
peekaboo press tab
peekaboo type --text "Message content here"
peekaboo click --on "Submit"
```

## AI Model Integration

Peekaboo can use AI models for visual question answering and intelligent automation.

**Supported Providers:**
- OpenAI (gpt-5.1, gpt-4o)
- Anthropic (claude-opus-4, claude-sonnet-4)
- xAI (grok-4-fast)
- Google (gemini-2.5-flash, gemini-2.5-pro)
- Local Ollama models

**Configure providers:**
```bash
export PEEKABOO_AI_PROVIDERS="openai/gpt-5.1,anthropic/claude-opus-4"

# Or use interactive configuration
peekaboo config add
```

## Utility Commands

**List system resources:**
```bash
peekaboo list apps
peekaboo list windows
peekaboo list screens
peekaboo list menubar
```

**Manage snapshots:**
```bash
peekaboo clean --all-snapshots
peekaboo clean --older-than 7
```

**Add delays:**
```bash
peekaboo sleep --duration 1000  # 1 second
```

## Complete Command Reference

For detailed documentation of all commands, options, and parameters, see:
- [CLI Reference](references/cli_reference.md) - Complete command documentation

## Best Practices

1. **Always check permissions first** - Run `peekaboo permissions status` before automation
2. **Use snapshots for reliability** - Capture UI state before clicking elements for accurate targeting
3. **Add appropriate delays** - Use `sleep` between commands to allow UI to update
4. **Use JSON output** - When scripting, use `--json-output` for structured data parsing
5. **Test in dry-run mode** - Use `--dry-run` with agent commands to preview automation steps
6. **Prefer natural language** - Use `peekaboo agent` for complex multi-step tasks
7. **Handle errors gracefully** - Check exit codes and permission status when automation fails

## Troubleshooting

**Permission Issues:**
```bash
peekaboo permissions status
peekaboo permissions grant
```

**Element Not Found:**
- Capture fresh snapshot with `peekaboo see`
- Use `--wait` option to allow UI to load
- Try natural language description instead of exact text

**Command Fails:**
- Check application is running: `peekaboo list apps`
- Verify window is visible: `peekaboo list windows`
- Ensure sufficient delays between commands
