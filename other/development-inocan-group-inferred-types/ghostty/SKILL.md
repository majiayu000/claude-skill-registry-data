---
name: ghostty
description: Configure and manage Ghostty terminal emulator settings. Use when modifying ghostty config, validating configuration, checking window settings, themes, fonts, keybindings, or troubleshooting ghostty startup behavior.
allowed-tools: [Read, Edit, Bash]
---

# ghostty

Terminal emulator configuration and management.

## Config location

- user config: `~/.config/ghostty/config`
- terminfo: `~/.config/ghostty/term.tic`
- binary: `/Applications/Ghostty.app/Contents/MacOS/ghostty`

## Common actions

### validate config

```bash
ghostty +validate-config
```

Validates configuration syntax and reports errors for unknown fields or invalid values.

### show current config

``` bash
ghostty +show-config
```

Displays the effective configuration, including defaults and user overrides.

### list available options

Common configuration categories:

- window: `window-decoration`, `window-theme`, `maximize`, `fullscreen`
- fonts: `font-family`, `font-size`, `font-style`
- appearance: `background-opacity`, `theme`, `cursor-style`
- behavior: `shell-integration`, `mouse-hide-while-typing`, `clipboard-write`
- macos: `macos-option-as-alt`, `macos-non-native-fullscreen`
- keybindings: `keybind = <key>=<action>`

### other useful commands

``` bash
ghostty +list-fonts          # show available fonts
ghostty +list-themes         # show available themes
ghostty +list-keybinds       # show current keybindings
ghostty +list-actions        # show available actions for keybindings
ghostty +edit-config         # open config in editor
```

## Config format

Plain text file with `key = value` syntax. Comments start with `#`.

``` conf
# window settings
window-decoration = false
window-theme = "dark"
maximize = true

# fonts and appearance
font-size = 14
theme = "GitHub Dark Colorblind"
cursor-style = "block"

# keybindings
keybind = cmd+v=paste_from_clipboard
keybind = cmd+c=copy_to_clipboard
```

## Common settings

### window modes

- `maximize = true` - start window maximized (fills screen, not fullscreen)
- `fullscreen = true` - start window in fullscreen mode
- `window-decoration = false` - hide window title bar
- `macos-non-native-fullscreen = "padded-notch"` - fullscreen with notch padding

### shell integration

- `shell-integration = "zsh"` - enable shell integration for zsh
- terminfo must be installed: `tic -x ~/.config/ghostty/term.tic`

### keybindings

Format: `keybind = <modifier>+<key>=<action>`

Modifiers:

- `cmd` / `super` - command key
- `ctrl` - control key
- `shift` - shift key
- `alt` / `option` - option key

Use `unbind` to remove default bindings:

``` conf
keybind = cmd+t=unbind
```

## Troubleshooting

### config validation fails

Run `ghostty +validate-config` to see specific error messages. Common issues:

- unknown field names (check spelling, refer to documentation)
- invalid values for enum types
- missing quotes around string values with spaces

### changes not taking effect

- restart ghostty completely (not just new window)
- check `ghostty +show-config` to verify effective configuration
- ensure no typos in config file path

### PATH setup

Already added to `~/.zshenv`:

``` zsh
path=(
  "/Applications/Ghostty.app/Contents/MacOS"
  $path
)
```

## Documentation

Official docs: <https://ghostty.org/docs>
