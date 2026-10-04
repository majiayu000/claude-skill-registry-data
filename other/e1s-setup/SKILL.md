---
name: e1s-setup
description: Use when the user asks to "set up e1s", "configure e1s", "e1s theme",
  "e1s AWS ECS", or needs to install/configure the e1s terminal UI for AWS ECS.
---

## Context

`e1s` is a terminal UI for browsing and managing AWS ECS resources.
Config lives at `~/.config/e1s/config.yml` (XDG), managed via stow.

The zsh function in `.zshrc` wraps `e1s` to always prompt for an AWS SSO profile via fzf and run `aws sso login` before launching.

## File layout in dotfiles

| Path | Purpose |
|---|---|
| `e1s/e1s/config.yml` | Theme + settings, stowed to `~/.config/e1s/` |

Stowed as a regular XDG package — no special `.stowrc` changes needed.

## Brewfile

```
brew "keidarcy/tap/e1s"
```

## config.yml

Current config uses **Catppuccin Macchiato** colors:

```yaml
refresh: 30

colors:
  BgColor: "#24273a"     # Base
  FgColor: "#cad3f5"     # Text
  BorderColor: "#8aadf4" # Blue
  Black: "#24273a"       # Base
  Red: "#ed8796"         # Red
  Green: "#a6da95"       # Green
  Yellow: "#eed49f"      # Yellow
  Blue: "#8aadf4"        # Blue
  Magenta: "#c6a0f6"     # Mauve
  Cyan: "#8bd5ca"        # Teal
  Gray: "#6e738d"        # Overlay0
```

All available color keys: `BgColor`, `FgColor`, `BorderColor`, `Black`, `Red`, `Green`, `Yellow`, `Blue`, `Magenta`, `Cyan`, `Gray`.
Hex colors and W3C named colors are both supported. Built-in named themes (e.g. `dracula`, `rose-pine`) can be set via `theme:` key instead.

## zsh wrapper (in zsh/zsh/config/aliases.zsh or similar)

```zsh
e1s () {
  local profile
  profile=$(grep '^\[profile' ~/.aws/config | sed 's/\[profile //;s/\]//' | fzf --prompt="AWS profile for e1s: " --height=40%)
  [[ -z "$profile" ]] && return 1
  aws sso login --profile "$profile"
  command e1s --profile "$profile" "$@"
}
```

## Adding a new machine

```zsh
cd ~/Progetti/dotfiles
stow .   # picks up e1s/ automatically
```
