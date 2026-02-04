---
name: dotfiles-config
description: Use when editing ANY configuration file in this dotfiles repository. Ensures files are edited in the repo (not symlinks), identifies correct file locations, and tracks the repository structure.
---

# Dotfiles Config Skill

## Golden Rule

**ALWAYS edit files in `~/dev/dotfiles/`, NEVER edit symlinked files in `~/` or `~/.config/`.**

The files in your home directory are symlinks pointing back to this repo. Verify with:
```bash
ls -la ~/.config/ghostty/config  # Should show symlink to dotfiles
```

## Repository Structure

```
~/dev/dotfiles/
├── home/                    # Base configs (all platforms)
│   ├── .claude/             # Claude Code config (this skill lives here)
│   ├── .config/             # XDG configs
│   │   ├── alacritty/
│   │   ├── ghostty/
│   │   ├── helix/
│   │   ├── home-manager/    # Nix Home Manager (CLI tools)
│   │   ├── lazygit/
│   │   ├── nvim/
│   │   ├── yazi/
│   │   ├── zellij/
│   │   └── zsh/
│   ├── .bashrc
│   ├── .tmux.conf
│   └── .zshrc
├── home-mac/                # macOS-specific configs
│   └── Brewfile             # GUI apps via Homebrew
├── home-linux/              # Linux-specific configs
├── mac/
│   └── nix-darwin/          # macOS system settings
└── ubuntu/                  # Ubuntu-specific configs
```

## Config File Locations

| Tool | Dotfiles Location | Symlinked To |
|------|-------------------|--------------|
| Alacritty | `home/.config/alacritty/` | `~/.config/alacritty/` |
| Claude Code | `home/.claude/` | `~/.claude/` |
| Ghostty | `home/.config/ghostty/` | `~/.config/ghostty/` |
| Helix | `home/.config/helix/` | `~/.config/helix/` |
| Home Manager | `home/.config/home-manager/` | `~/.config/home-manager/` |
| Lazygit | `home/.config/lazygit/` | `~/.config/lazygit/` |
| Neovim | `home/.config/nvim/` | `~/.config/nvim/` |
| Ripgrep | `home/.config/rg/` | `~/.config/rg/` |
| Starship | `home/.config/starship.toml` | `~/.config/starship.toml` |
| Tmux | `home/.tmux.conf` | `~/.tmux.conf` |
| Yazi | `home/.config/yazi/` | `~/.config/yazi/` |
| Zellij | `home/.config/zellij/` | `~/.config/zellij/` |
| Zsh | `home/.zshrc`, `home/.config/zsh/` | `~/.zshrc`, `~/.config/zsh/` |

## Package Management

### CLI Tools (Nix Home Manager)
Edit: `home/.config/home-manager/home.nix`
Apply: `home-manager switch`

### GUI Apps (macOS Homebrew)
Edit: `home-mac/Brewfile`
Apply: `cd home-mac && brew bundle`

### Language Runtimes (mise)
Edit: `home/.config/mise/config.toml`
Apply: `mise install`

### macOS System Settings (nix-darwin)
Edit: `mac/nix-darwin/flake.nix`
Apply: `just nix-darwin-switch`

## Stow Commands

After adding new config files, re-run stow:
```bash
just stow-mac    # macOS
just stow-linux  # Linux
just stow-home   # Just base home/
```

## Skills Location

Skills live in `home/.claude/skills/` and are symlinked to `~/.claude/skills/`.

To create a new skill:
1. Create directory: `mkdir -p home/.claude/skills/skill-name`
2. Create SKILL.md with frontmatter (name, description)
3. Stow will automatically symlink it

## Common Mistakes to Avoid

1. **Editing symlinked files** - Always navigate to `~/dev/dotfiles/` first
2. **Forgetting to stow** - New files need `just stow-*` to create symlinks
3. **Wrong platform directory** - macOS GUI apps go in `home-mac/`, not `home/`
4. **Editing ~/.config directly** - These are symlinks, edit the source in dotfiles

## Verification

Before declaring a config change complete:
1. Confirm you edited the file in `~/dev/dotfiles/`
2. Check the symlink exists: `ls -la ~/.config/<tool>/`
3. Test the config works (reload app or run verification command)
