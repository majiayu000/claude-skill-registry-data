---
name: waybar
description: Manage and configure Waybar status bar. Use when user asks about waybar, status bar modules, bar layout, or wants to customize their top/bottom panel.
---

# Waybar Configuration Skill

Manage your Waybar configuration using natural language commands.

## Omarchy Integration

This system uses **Omarchy**, which provides wrapper commands and default configs for Waybar.

### Omarchy Commands

| Command | Purpose |
|---------|---------|
| `omarchy-restart-waybar` | Restart Waybar (preferred over pkill) |
| `omarchy-toggle-waybar` | Show/hide Waybar |
| `omarchy-refresh-waybar` | Reset to Omarchy defaults (creates backup) |

**IMPORTANT:** Use `omarchy-restart-waybar` instead of `pkill` or `killall` for reloading.

### Omarchy Default Config

Omarchy maintains default configs at:
- `~/.local/share/omarchy/config/waybar/config.jsonc`
- `~/.local/share/omarchy/config/waybar/style.css`

Running `omarchy-refresh-waybar` will:
1. Backup current config with timestamp (e.g., `config.jsonc.bak.1754426383`)
2. Replace with Omarchy defaults
3. Restart Waybar

### Omarchy-Specific Modules

The default config includes these Omarchy modules:

```jsonc
"custom/omarchy": {
  "format": "<span font='omarchy'>\ue900</span>",
  "on-click": "omarchy-menu",
  "on-click-right": "xdg-terminal-exec",
  "tooltip-format": "Omarchy Menu\n\nSuper + Alt + Space"
}

"custom/update": {
  "exec": "omarchy-update-available",
  "on-click": "omarchy-launch-floating-terminal-with-presentation omarchy-update",
  "signal": 7,
  "interval": 21600
}

"custom/screenrecording-indicator": {
  "on-click": "omarchy-cmd-screenrecord",
  "exec": "$OMARCHY_PATH/default/waybar/indicators/screen-recording.sh",
  "signal": 8,
  "return-type": "json"
}
```

### Omarchy Click Handlers

Many modules use Omarchy launchers for click actions:

| Handler | Purpose |
|---------|---------|
| `omarchy-menu` | Main Omarchy menu |
| `omarchy-menu power` | Power menu (shutdown, reboot, etc.) |
| `omarchy-launch-wifi` | WiFi network selector |
| `omarchy-launch-bluetooth` | Bluetooth device manager |
| `omarchy-launch-or-focus-tui btop` | System monitor |
| `omarchy-launch-or-focus-tui wiremix` | Audio mixer |
| `omarchy-launch-floating-terminal-with-presentation <cmd>` | Run command in floating terminal |
| `omarchy-cmd-screenrecord` | Toggle screen recording |
| `omarchy-tz-select` | Timezone selector |

## Configuration Location

```
~/.config/waybar/config.jsonc  # User configuration (JSONC format)
~/.config/waybar/style.css     # User styling
```

## Instructions

When the user asks to modify their Waybar config:

### 1. Always Read Current Config First

```bash
cat ~/.config/waybar/config.jsonc
```

### 2. Create Backup Before Changes

```bash
cp ~/.config/waybar/config.jsonc ~/.config/waybar/config.jsonc.bak.$(date +%s)
```

### 3. Make Changes Using Edit Tool

Use the Edit tool to modify the JSONC file. Preserve:
- Existing comments
- Formatting style
- Icon characters (Nerd Font glyphs)
- Omarchy-specific modules and handlers

### 4. Validate JSON After Edit

```bash
# Remove comments and validate JSON structure
sed 's|//.*||g' ~/.config/waybar/config.jsonc | jq . > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

### 5. Reload Waybar

```bash
omarchy-restart-waybar
```

## Core Concepts

### Bar Structure

Waybar has three module sections:
- `modules-left` - Left side (default: Omarchy menu, workspaces)
- `modules-center` - Center (default: clock, update indicator, screen recording)
- `modules-right` - Right side (default: tray, bluetooth, network, audio, cpu, battery)

### Module Types

1. **Built-in modules**: `clock`, `battery`, `cpu`, `memory`, `network`, `bluetooth`, `pulseaudio`, `tray`, `hyprland/workspaces`
2. **Custom modules**: `custom/<name>` - User-defined with exec scripts
3. **Group modules**: `group/<name>` - Container for multiple modules (e.g., `group/tray-expander`)

## Common Operations

### Add a Module

1. Add module name to the appropriate array
2. Add configuration block if new module type

Example - adding memory module:
```jsonc
// In modules-right array:
"modules-right": ["memory", "cpu", "battery"],

// Add configuration:
"memory": {
  "interval": 30,
  "format": "{percentage}% ",
  "tooltip-format": "{used:0.1f}G / {total:0.1f}G",
  "on-click": "omarchy-launch-or-focus-tui btop"
}
```

### Remove a Module

Remove from section array. Config block can remain (harmless).

### Move a Module

Remove from one section array, add to another.

### Create Custom Module

Simple text output:
```jsonc
"custom/mymodule": {
  "exec": "/path/to/script.sh",
  "interval": 10,
  "format": "{}",
  "on-click": "command-to-run"
}
```

JSON output (for dynamic text/tooltip/class):
```jsonc
"custom/mymodule": {
  "exec": "/path/to/script.sh",
  "return-type": "json",
  "interval": 10
}
```

Script outputs: `{"text": "display", "tooltip": "hover text", "class": "css-class"}`

### Signal-Based Updates

For modules that should update on events (not intervals):
```jsonc
"custom/mymodule": {
  "exec": "/path/to/script.sh",
  "signal": 9,
  "return-type": "json"
}
```

Trigger update from anywhere: `pkill -SIGRTMIN+9 waybar`

## Module Reference

### Built-in Modules

| Module | Purpose | Key Settings |
|--------|---------|--------------|
| `clock` | Time/date | `format`, `format-alt`, `timezone` |
| `battery` | Battery status | `format`, `states`, `format-icons` |
| `cpu` | CPU usage | `interval`, `format` |
| `memory` | RAM usage | `interval`, `format` |
| `network` | Network status | `format-wifi`, `format-ethernet` |
| `bluetooth` | Bluetooth | `format`, `format-connected` |
| `pulseaudio` | Audio | `format`, `format-muted`, `scroll-step` |
| `tray` | System tray | `icon-size`, `spacing` |
| `hyprland/workspaces` | Workspaces | `format`, `format-icons`, `persistent-workspaces` |

### Hyprland-Specific

| Module | Purpose |
|--------|---------|
| `hyprland/workspaces` | Workspace indicator/switcher |
| `hyprland/window` | Active window title |
| `hyprland/submap` | Current submap/mode |
| `hyprland/language` | Keyboard layout |

## Format Placeholders

**clock**: `{:%H:%M}`, `{:%A}`, `{:%d %B}`, `{:L%A %H:%M}` (locale-aware)
**battery**: `{capacity}`, `{icon}`, `{time}`, `{power}`
**cpu**: `{usage}`, `{avg_frequency}`
**memory**: `{percentage}`, `{used}`, `{total}`
**network**: `{essid}`, `{signalStrength}`, `{bandwidthDownBytes}`, `{bandwidthUpBytes}`

## Icons (Nerd Font)

Common glyphs used in this config:
- `󰍛` - CPU
- `` - Memory
- `󰂯`/`󰂱`/`󰂲` - Bluetooth off/connected/disabled
- `󰤨`/`󰤯`/`󰤮` - WiFi strong/weak/disconnected
- `󰁹`/`󰁺` - Battery full/low
- `//` - Volume levels
- `` - Volume muted
- `` - Tray expander
- `󰻂` - Screen recording

## Styling (style.css)

```css
#clock {
  color: #ffffff;
  padding: 0 10px;
}

#battery.warning {
  color: #ff0000;
}

#custom-omarchy {
  font-family: omarchy;
}
```

## Safety

- Always backup before changes
- Validate JSON after edits
- Use `omarchy-restart-waybar` to apply changes
- Keep backup files for rollback
- Don't remove `custom/omarchy` or `custom/update` unless intentional

## Reverting to Defaults

If something breaks:
```bash
# Restore from most recent backup
cp ~/.config/waybar/config.jsonc.bak.TIMESTAMP ~/.config/waybar/config.jsonc
omarchy-restart-waybar

# Or reset to Omarchy defaults (backs up current first)
omarchy-refresh-waybar
```

## Example Requests

- "Add a memory monitor to my waybar"
- "Move the clock to the left side"
- "Remove the CPU indicator"
- "Add a custom module that shows disk usage"
- "Show battery percentage"
- "Make the bar thicker"
- "Hide the system tray"
- "Add a module that shows my IP address"
