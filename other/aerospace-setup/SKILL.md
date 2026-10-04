---
name: aerospace-setup
description: Use when user asks to "configure aerospace", "add app to workspace", "set floating layout", "configure jankyborders", "recover aerospace config", or needs to manage AeroSpace workspace rules, borders, or keybindings.
---

## Config location

`dotfiles/aerospace/aerospace.toml` → stowed to `~/.config/aerospace/aerospace.toml`.
After any change, reload with `alt+shift+; → esc` (no restart needed).
Restart required only for `after-startup-command` changes (e.g. borders).

## Recovering from git history

```bash
git log --all --oneline -- aerospace/
git checkout <commit> -- aerospace/aerospace.toml
```

## Stowing

`stow .` from dotfiles root — aerospace follows XDG convention, no special handling.
Verify: `ls -la ~/.config/aerospace/`

## JankyBorders

Launched via `after-startup-command`, not as a service.
Some apps (Safari, Bitwarden) don't show borders — native/custom rendering limitation, not a config bug.
Colors use `0xff<hex>` format (0xff prefix = full opacity).
Catppuccin Macchiato reference: Peach=f5a97f, Lavender=b7bdf8, Surface2=494d64.

## Workspace rules

Group floating apps in one block using array syntax:

```toml
[[on-window-detected]]
if.app-id = ['com.apple.finder', 'com.apple.systempreferences']
run = 'layout floating'
```

Apps with both workspace assignment and layout need separate blocks.

## Key keybinding patterns

| Action                            | Shortcut                    |
| --------------------------------- | --------------------------- |
| Focus window                      | `alt+hjkl`                  |
| Move window                       | `alt+shift+hjkl`            |
| Switch workspace                  | `alt+<letter/number>`       |
| Move window to workspace          | `alt+shift+<letter/number>` |
| Move workspace to monitor         | `alt+shift+tab`             |
| Move window to monitor            | `alt+shift+period`          |
| Service mode                      | `alt+shift+;`               |
| Service: reload config            | `esc`                       |
| Service: reset layout             | `r`                         |
| Service: toggle float             | `f`                         |
| Service: join-with (nest windows) | `alt+shift+hjkl`            |

## Nesting windows (asymmetric layouts)

`join-with` nests two windows into a sub-container. Example: A left, B+C stacked vertically right:

1. Focus B
2. `alt+shift+;` → `alt+shift+j` (join-with down toward C)
3. B and C become a vertical container; A stays as left column

`move` (`alt+shift+hjkl` in normal mode) moves within the root container — it does NOT nest. Use `join-with` in service mode for nesting.

## Common app bundle IDs

| App                | Bundle ID                     |
| ------------------ | ----------------------------- |
| Kitty              | `net.kovidgoyal.kitty`        |
| Safari             | `com.apple.Safari`            |
| Mail               | `com.apple.mail`              |
| Obsidian           | `md.obsidian`                 |
| Finder             | `com.apple.finder`            |
| System Preferences | `com.apple.systempreferences` |
| Music              | `com.apple.Music`             |
| WhatsApp           | `net.whatsapp.WhatsApp`       |

## Fullscreen

`fullscreen` triggers macOS native fullscreen. Assign like any other command:

```toml
alt-shift-z = 'fullscreen'
```

## Keybinding conflicts: workspace letters

Each workspace letter occupies two slots simultaneously:

- `alt+<letter>` → switch to workspace
- `alt+shift+<letter>` → move window to workspace

To reassign `alt-shift-Z` to something else, remove `alt-Z` too (otherwise the workspace still exists but is unreachable).

## Modifier conflicts

`alt+k` = focus up → can't use K as workspace letter with alt modifier.
Workaround: use a different letter (T for Terminal instead of K).
