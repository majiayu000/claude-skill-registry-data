---
name: wezterm-config
description: Complete WezTerm terminal emulator configuration assistant. Use for any WezTerm configuration task including appearance, fonts, colors, keybindings, mouse bindings, tabs, panes, SSH domains, multiplexing, serial ports, plugins, events, window management, performance, platform-specific settings, Lua scripting, or any terminal customization.
---

# WezTerm Configuration Assistant

This skill provides comprehensive assistance for configuring WezTerm terminal emulator. WezTerm uses Lua 5.4 for configuration and offers extensive customization across all aspects of terminal behavior, appearance, input handling, networking, and advanced features.

## Configuration Location

**Config Directory:** `/Users/alex/.config/wezterm`
**Main Config File:** `/Users/alex/.config/wezterm/wezterm.lua`

Alternative locations: `~/.wezterm.lua` or paths specified via `$WEZTERM_CONFIG_FILE`

## Core Principles

### ALWAYS Follow This Workflow

1. **Read Current Config**: Use Read tool to examine existing configuration
2. **Fetch Documentation**: Use WebFetch to get current documentation for the specific feature
3. **Research Thoroughly**: Check multiple doc pages if needed for complex features
4. **Implement Carefully**: Preserve existing config, validate Lua syntax
5. **Explain Clearly**: Document what changed and why
6. **Guide Testing**: Explain how to reload config (Ctrl+Shift+R or restart)

### Documentation Strategy

**Never embed documentation text.** Always use WebFetch to retrieve current information from https://wezterm.org/

WezTerm documentation is comprehensive and continuously updated. The configuration system supports hundreds of options across many domains.

## Full Configuration Capabilities

WezTerm supports configuration across these comprehensive areas. For each request, fetch the relevant documentation:

### 1. Visual Appearance & Display
- **Colors & Schemes**: Color schemes, palette customization, dynamic colors
  - https://wezterm.org/config/appearance.html
  - https://wezterm.org/colorschemes/
  - https://wezterm.org/config/lua/wezterm.color/
- **Fonts**: Font families, size, weight, fallback, shaping, ligatures, harfbuzz
  - https://wezterm.org/config/fonts.html
  - https://wezterm.org/config/lua/wezterm/font.html
- **Cursor**: Style, blinking, colors, thickness
- **Window**: Decorations, opacity, blur, padding, dimensions, background
- **Tab Bar**: Styling, position, colors, custom rendering
  - https://wezterm.org/config/lua/config/tab_bar_style.html
- **Rendering**: GPU settings, WebGPU, FreeType options, anti-aliasing
  - https://wezterm.org/config/lua/config/front_end.html

### 2. Input & Interaction
- **Keyboard Bindings**: Key assignments, key tables, leader keys
  - https://wezterm.org/config/keyboard-concepts.html
  - https://wezterm.org/config/keys.html
  - https://wezterm.org/config/lua/keyassignment/
- **Mouse Bindings**: Click actions, drag behavior, scrolling
  - https://wezterm.org/config/mouse.html
- **Copy Mode**: Quick select patterns, search mode, selection patterns
  - https://wezterm.org/copymode.html
- **IME**: Input method editor settings for international input

### 3. Window & Pane Management
- **Panes**: Splitting, navigation, focus, sizing
  - https://wezterm.org/config/lua/pane/
- **Tabs**: Creation, navigation, renaming, styling
  - https://wezterm.org/config/lua/MuxTab/
- **Windows**: Multiple windows, positioning, fullscreen
  - https://wezterm.org/config/lua/window/
  - https://wezterm.org/config/lua/gui-events/
- **Workspaces**: Workspace management and switching
  - https://wezterm.org/config/lua/wezterm.mux/

### 4. Terminal Behavior
- **Scrollback**: Buffer size, history management
- **Bell**: Visual and audible notifications
- **Exit Behavior**: Close confirmation, hold on exit
- **Text Processing**: Blink animation, semantic zones
- **Clipboard**: Paste behavior, bracketed paste
- **Shell Integration**: OSC sequences, semantic prompts
  - https://wezterm.org/shell-integration.html

### 5. Advanced Connectivity
- **SSH Client**: Native SSH integration, SSH domains, connection management
  - https://wezterm.org/config/lua/SshDomain.html
  - https://wezterm.org/ssh.html
- **Multiplexing**: Unix domain sockets, TCP connections, TLS
  - https://wezterm.org/multiplexing.html
  - https://wezterm.org/config/lua/mux-events/
- **Serial Ports**: Serial device connections
  - https://wezterm.org/config/lua/SerialDomain.html
- **WSL Integration**: Windows Subsystem for Linux domains
  - https://wezterm.org/config/lua/WslDomain.html
- **TLS**: Certificate management, client/server TLS settings

### 6. Events & Scripting
- **Event Handlers**: GUI events, mux events, window events
  - https://wezterm.org/config/lua/window-events/
  - https://wezterm.org/config/lua/gui-events/
  - https://wezterm.org/config/lua/mux-events/
- **Custom Actions**: wezterm.action, emit events, custom logic
- **Status Bar**: Custom status line rendering
  - https://wezterm.org/config/lua/window-events/update-status.html
- **Tab Formatting**: Custom tab title and appearance
- **Lua Modules**: wezterm.color, wezterm.gui, wezterm.mux, wezterm.time, wezterm.serde
  - https://wezterm.org/config/lua/general.html

### 7. Platform-Specific Features
- **macOS**: Native fullscreen, window blur, decorations
  - https://wezterm.org/config/lua/config/macos_window_background_blur.html
- **Windows**: Acrylic effects, backdrop blur, WSL
- **Linux**: Wayland support, desktop environment detection
- **FreeBSD/NetBSD**: Platform-specific optimizations

### 8. Graphics & Media
- **Image Protocol**: iTerm2 image protocol, imgcat
  - https://wezterm.org/imgcat.html
- **Kitty Graphics**: Kitty graphics protocol support
- **Sixel**: Sixel graphics rendering

### 9. Launcher & Command Palette
- **Launcher Menu**: Custom launcher items, domain launching
  - https://wezterm.org/config/launch.html
- **Command Palette**: Custom palette commands
  - https://wezterm.org/config/lua/keyassignment/ActivateCommandPalette.html

### 10. Plugin System
- **Plugin Loading**: Plugin management and configuration
  - https://wezterm.org/config/lua/wezterm.plugin/

### 11. Performance & Optimization
- **Frame Rate**: Animation FPS, performance tuning
- **Scrollback Limits**: Memory management
- **GPU Selection**: Renderer preferences, hardware acceleration

### 12. Advanced Configuration Patterns
- **Config Builder**: Using wezterm.config_builder()
  - https://wezterm.org/config/files.html
- **Modular Configs**: Splitting config across multiple Lua files
- **Per-Window Overrides**: window:set_config_overrides()
- **CLI Overrides**: Command-line configuration parameters
- **Conditional Logic**: Platform detection, environment-based config
- **Hot Reloading**: Automatic config reload on file change

## Configuration File Structure

Modern WezTerm configs use the config_builder pattern:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- All configuration options
config.option_name = value

return config
```

Legacy pattern (still valid):
```lua
local wezterm = require 'wezterm'
return {
  option_name = value,
}
```

## Finding Documentation

For ANY configuration request:

1. **Main Documentation Hub**: https://wezterm.org/
2. **Full Config Reference**: https://wezterm.org/config/lua/config/index.html
3. **Lua API Reference**: https://wezterm.org/config/lua/general.html
4. **Search Strategy**: Use WebFetch to retrieve specific pages for:
   - The main feature category
   - Specific config options
   - Related examples or patterns
   - Event handlers if dynamic behavior needed

## Research Process for Each Request

When user requests any configuration change:

1. **Identify Category**: Determine which configuration area(s) are involved
2. **Fetch Core Docs**: Get main documentation page for that category
3. **Fetch Specifics**: If needed, get specific API reference or examples
4. **Check Events**: If dynamic behavior needed, fetch event documentation
5. **Verify Syntax**: Check Lua API docs for correct object/method usage
6. **Cross-Reference**: Look at related features that might enhance the solution

## Implementation Guidelines

### Code Quality
- Use clear variable names and comments
- Follow Lua best practices
- Validate syntax before suggesting
- Use wezterm.config_builder() for new configs

### Config Organization
- Group related settings together
- Add section comments for clarity
- Consider suggesting modular organization for complex configs
- Preserve user's existing organizational structure

### Error Prevention
- Avoid side effects in config (no unconditional process launches)
- Check for config file existence before editing
- Validate that Lua syntax is correct
- Test edge cases in suggestions

### User Guidance
- Explain what each change does
- Link to relevant documentation pages
- Suggest how to test changes (Ctrl+Shift+R)
- Offer related enhancements when appropriate
- Mention platform-specific considerations if relevant

## Advanced Scenarios

### Creating Helper Modules
For complex configs, suggest creating helper modules in the config directory that can be required and reused.

### Event-Driven Configuration
When dynamic behavior is needed, use event handlers rather than static config.

### Conditional Configuration
Use Lua conditionals for platform-specific or environment-based settings.

### Performance Optimization
Consider performance implications of suggestions (e.g., scrollback size, animation settings).

## Troubleshooting Support

When issues arise:
- Check the changelog for version-specific features
- Verify config syntax with wezterm.config_builder()
- Look for deprecation warnings in docs
- Suggest using wezterm CLI tools for debugging
- Reference https://wezterm.org/troubleshooting.html

## Remember

- **Never paste documentation** - always use WebFetch
- **Always read config first** - understand existing setup
- **Research thoroughly** - fetch multiple doc pages if needed
- **Explain clearly** - user should understand the changes
- **Link resources** - provide documentation URLs for reference
- **Test guidance** - explain how to verify changes work

WezTerm is feature-rich and constantly evolving. When in doubt, fetch the documentation.
