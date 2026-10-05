---
name: slt
description: Toggle the statusline quota pace indicator (mode/theme)
when_to_use: "statusline, quota indicator, toggle display, slt, slt bar, slt theme, cycle mode, status bar emoji, dragon theme, quota pace, progress bar in status line"
argument-hint: '[symbol|percent|number|bar|off] [theme [name]]'
user_invocable: true
---

# Statusline Toggle

Cycles the display mode of the quota pace indicator in the Claude Code status line.

## Modes

`symbol` → `percent` → `number` → `bar` → `off` → back to `symbol`

## Usage

```
/slt                    # Cycle to next mode
/slt theme              # Show available themes
/slt theme <name>       # Set theme (circles, bird, moon, weather, mood, coffee, rocket, ocean, dragon)
/slt symbol|percent|number|bar|off   # Set specific mode
```
