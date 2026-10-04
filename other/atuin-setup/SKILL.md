---
name: atuin-setup
description: Use when the user asks to "set up atuin", "stow atuin config", "disable atuin sync", "remove atuin server", or needs to manage atuin history sync settings in dotfiles.
---

# Atuin Setup

## Stowing the config

Atuin creates `~/.config/atuin/` at first run with its own files (config.toml, themes/, etc.).
Stow cannot link into an existing directory that contains files — it silently skips them.

**Fix**: remove the directory before stowing:
```zsh
rm -rf ~/.config/atuin
cd ~/Progetti/dotfiles && stow .
```

Atuin will recreate missing files (e.g. `session`, `key`) on first run.

## Circular symlink trap

If `~/.config/atuin` is already a symlink to the repo (stow linked the whole directory),
never create a manual symlink `config.toml → .../dotfiles/atuin/config.toml`:
that creates a loop (`~/.config/atuin` → `dotfiles/atuin` → `config.toml` → `~/.config/atuin/config.toml` → loop).

Always check first:
```zsh
ls -la ~/.config/ | grep atuin        # symlink to dir? → write directly in repo
ls -la ~/.config/atuin/config.toml   # symlink to file? → ok
```

If `~/.config/atuin` is a symlink to the repo directory, editing
`~/Progetti/dotfiles/atuin/config.toml` and `~/.config/atuin/config.toml`
are the same thing — no manual symlinks needed.

## Disabling centralized sync

To decommission an atuin server (self-hosted or cloud):

1. `atuin logout` — removes the local session (history is untouched)
2. In `atuin/config.toml`:
   ```toml
   auto_sync = false
   # sync_address = "https://..."
   # sync_frequency = "10m"
   ```
3. Verify with `atuin info` that the config is loaded correctly.

## Catppuccin theme

The theme file lives in the repo at `atuin/themes/catppuccin-macchiato-sky.toml`.
Atuin looks for themes in the same directory as the config. With stow active, the theme
is automatically available via symlink.

In `config.toml`:
```toml
[theme]
name = "catppuccin-macchiato-sky"
```
