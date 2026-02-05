---
name: hyprland
description: "Comprehensive Hyprland Wayland compositor configuration skill. Use when users need help with: (1) Creating or modifying Hyprland config files, (2) Setting up keybindings, window rules, monitors, or animations, (3) Troubleshooting Hyprland configuration issues, (4) Searching for valid config variables and values, (5) Understanding Hyprland syntax and structure, (6) Setting up multi-monitor configurations, (7) Configuring input devices, decorations, or layouts, or (8) Any other Hyprland-related configuration tasks."
---

# Hyprland Configuration Skill

This skill provides comprehensive support for configuring Hyprland, a dynamic tiling Wayland compositor.

## Quick Start

When helping with Hyprland configuration:

1. **Read references first** - Load `references/config_reference.md` for syntax and variables, `references/examples.md` for practical patterns
2. **Search documentation** - Use `scripts/search_hyprland_docs.py` to find specific config variables or features
3. **Apply best practices** - Follow Hyprland conventions for config structure and naming
4. **Test configurations** - Validate syntax and provide working examples

## Tool: Documentation Search

Use the search script to find configuration variables, keybindings, and documentation:

```bash
# Search for any config variable or feature
python3 scripts/search_hyprland_docs.py "gaps_in"
python3 scripts/search_hyprland_docs.py "border_size"
python3 scripts/search_hyprland_docs.py "animation"

# List all documentation sections
python3 scripts/search_hyprland_docs.py --list
```

The script searches across:
- Variables (general, decoration, input, etc.)
- Keywords (monitor, bind, exec, etc.)
- Binds and keybindings
- Animations
- Dispatchers
- Window rules
- Monitor configuration

**How it works:** The search script uses local markdown documentation files stored in `references/docs/` that were downloaded from the official Hyprland wiki using the jina.ai markdown converter (`https://r.jina.ai/$URL`). This provides:
- **Fast offline access** - No network calls needed
- **Clean markdown format** - Easy to read and parse
- **Up-to-date content** - Downloaded from wiki.hypr.land

## Documentation Index

The skill includes complete local copies of official Hyprland documentation:

| Section | File | Source |
|---------|------|--------|
| Variables | `references/docs/variables.md` | [wiki.hypr.land/Configuring/Variables/](https://wiki.hypr.land/Configuring/Variables/) |
| Keywords | `references/docs/keywords.md` | [wiki.hypr.land/Configuring/Keywords/](https://wiki.hypr.land/Configuring/Keywords/) |
| Binds | `references/docs/binds.md` | [wiki.hypr.land/Configuring/Binds/](https://wiki.hypr.land/Configuring/Binds/) |
| Animations | `references/docs/animations.md` | [wiki.hypr.land/Configuring/Animations/](https://wiki.hypr.land/Configuring/Animations/) |
| Dispatchers | `references/docs/dispatchers.md` | [wiki.hypr.land/Configuring/Dispatchers/](https://wiki.hypr.land/Configuring/Dispatchers/) |
| Window Rules | `references/docs/window-rules.md` | [wiki.hypr.land/Configuring/Window-Rules/](https://wiki.hypr.land/Configuring/Window-Rules/) |
| Monitors | `references/docs/monitors.md` | [wiki.hypr.land/Configuring/Monitors/](https://wiki.hypr.land/Configuring/Monitors/) |

**Updating documentation:** To refresh the local docs with the latest from the wiki:

```bash
cd references/docs
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Variables/" -o variables.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Keywords/" -o keywords.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Binds/" -o binds.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Animations/" -o animations.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Dispatchers/" -o dispatchers.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Window-Rules/" -o window-rules.md
curl -s "https://r.jina.ai/https://wiki.hypr.land/Configuring/Monitors/" -o monitors.md
```

## Configuration Workflow

### 1. Understanding the Request

Determine what the user needs:
- **New configuration**: Start from scratch or use minimal template
- **Modification**: Edit existing config (ask user to provide current config)
- **Troubleshooting**: Identify syntax errors or config issues
- **Feature addition**: Add specific functionality (keybinds, rules, etc.)
- **Optimization**: Improve performance or aesthetics

### 2. Gathering Context

Ask clarifying questions when needed:
- Monitor setup (resolution, refresh rate, arrangement)
- Preferred keybinding modifier (SUPER, ALT, CTRL)
- Desired layout (dwindle, master)
- Aesthetic preferences (gaps, rounding, animations)
- Hardware specifics (NVIDIA GPU, laptop, touchpad)

### 3. Loading References

Always load the appropriate reference files:

```bash
# For syntax and all config variables
view references/config_reference.md

# For practical examples and patterns
view references/examples.md
```

**When to load each:**
- `config_reference.md`: For understanding syntax, all available variables, and their options
- `examples.md`: For complete working configurations and common patterns

### 4. Searching Documentation

If the references don't contain the needed information, or if you need the latest documentation:

```bash
python3 scripts/search_hyprland_docs.py "<query>"
```

Search for:
- Specific variable names (e.g., "gaps_in", "col.active_border")
- Features (e.g., "blur", "animations", "gestures")
- Keybinding options
- Window rule syntax

### 5. Creating Configuration

Follow these principles:

**Config file location**: `~/.config/hypr/hyprland.conf`

**Structure**:
```conf
# Comments start with #
# Sections use curly braces
general {
    variable = value
}

# Keywords at root level
monitor = DP-1, 1920x1080@60, 0x0, 1
bind = SUPER, Return, exec, kitty
```

**Best practices**:
- Use variables for commonly repeated values: `$mainMod = SUPER`
- Comment sections clearly
- Group related settings together
- Use `source` to split large configs into files
- Test configuration with `hyprctl reload` or restart Hyprland

## Common Tasks

### Creating a New Configuration

1. Load `references/examples.md` and find the "Complete Minimal Configuration"
2. Customize based on user's needs
3. Add monitor setup if multi-monitor
4. Configure keybindings with user's preferred modifier
5. Add autostart applications

### Adding Keybindings

1. Check `references/config_reference.md` for bind syntax
2. Use `$mainMod` variable for consistency
3. Common bind types:
   - `bind` - Normal bind
   - `bindm` - Mouse bind
   - `binde` - Repeating bind
   - `bindr` - Release bind
   - `bindl` - Locked bind (works when locked)

### Configuring Window Rules

1. Check `references/config_reference.md` for windowrule syntax
2. Use `windowrulev2` for modern syntax
3. Test rules with: `hyprctl clients` (lists window classes)
4. Common patterns in `references/examples.md`

### Multi-Monitor Setup

1. Load the multi-monitor example from `references/examples.md`
2. Adjust monitor positions and resolutions
3. Configure workspace-to-monitor assignments
4. Add monitor-specific settings

### Troubleshooting

**Common issues**:
- Syntax errors: Check for missing commas, brackets, or quotes
- Wrong variable names: Search documentation to verify
- Monitor not detected: Try `hyprctl monitors` to list available monitors
- Keybinds not working: Ensure no conflicts, check modifier keys
- Performance issues: Reduce blur passes, disable animations, check `misc.vfr`

**Debugging commands**:
```bash
# List all monitors
hyprctl monitors

# List all windows with classes
hyprctl clients

# Reload config
hyprctl reload

# Get keyword value
hyprctl getoption general:border_size

# Set keyword value (temporary)
hyprctl keyword general:border_size 3
```

## Configuration Patterns

### Minimal Configuration
Use for: New users, testing, simple setups
See: `references/examples.md` - "Complete Minimal Configuration"

### Multi-Monitor Productivity
Use for: Workstation setups, multiple displays
See: `references/examples.md` - "Multi-Monitor Setup" and "Productivity Setup"

### Gaming Configuration
Use for: Gamers, low-latency needs
See: `references/examples.md` - "Gaming Configuration"

### Laptop Configuration
Use for: Laptops, touchpads, battery optimization
See: `references/examples.md` - "Laptop-Specific Configuration"

### Rice/Beautiful Desktop
Use for: Aesthetic focus, eye candy
See: `references/examples.md` - "Rice (Beautiful Desktop) Configuration"

### Tiling WM Workflow
Use for: Power users, keyboard-driven workflow
See: `references/examples.md` - "Tiling Window Manager Workflow"

## Special Considerations

### NVIDIA GPUs

Always include NVIDIA environment variables and specific settings. See `references/examples.md` - "NVIDIA GPU Configuration" for the complete setup.

### High DPI Displays

```conf
monitor = eDP-1, 3840x2160@60, 0x0, 2  # 2x scaling
env = XCURSOR_SIZE,48  # Larger cursor
```

### Modular Configurations

For large configs, split into multiple files:
```conf
source = ~/.config/hypr/monitors.conf
source = ~/.config/hypr/keybinds.conf
source = ~/.config/hypr/windowrules.conf
```

### Performance Optimization

For slower systems:
- Reduce `blur.size` and `blur.passes`
- Disable shadows: `drop_shadow = false`
- Reduce animations: Lower animation speeds or disable
- Enable VFR: `misc.vfr = true`

## Output Guidelines

When providing configurations:

1. **Always include comments** explaining sections and non-obvious settings
2. **Use proper syntax** - verify with references before providing
3. **Provide complete sections** - don't leave partial configurations
4. **Test configurations mentally** - ensure they would work as written
5. **Explain what you've done** - help the user understand the config
6. **Offer alternatives** - suggest variations when relevant

**File creation**:
- For new configs: Create complete file at `~/.config/hypr/hyprland.conf`
- For modifications: Show the changes clearly with comments
- For additions: Provide the exact lines to add with location guidance

## Reference Documentation

The skill includes comprehensive reference files:

- **config_reference.md**: Complete syntax guide, all variables, and their options
- **examples.md**: Practical working configurations for common use cases

Always consult these before searching online documentation, as they provide immediate, reliable information.

## Validation

Before finalizing configurations:

1. Check syntax matches reference patterns
2. Verify variable names are correct
3. Ensure no duplicate keybindings
4. Validate monitor names and resolutions
5. Test critical paths (if possible)

Use `hyprctl` commands to validate when working with existing systems.

## Additional Resources

Official documentation sections (search with the script):
- Variables: All configuration variables
- Keywords: Core Hyprland keywords (monitor, bind, exec, etc.)
- Dispatchers: Actions for keybindings
- Window Rules: Rules for controlling windows
- Animations: Animation configuration
- Binds: Keybinding reference

Search any of these with: `python3 scripts/search_hyprland_docs.py "<topic>"`
