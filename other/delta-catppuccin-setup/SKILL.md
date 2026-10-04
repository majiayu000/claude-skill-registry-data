---
name: delta-catppuccin-setup
description: This skill should be used when the user asks to "configure delta theme", "add catppuccin to delta", "set up delta colors", "update catppuccin.gitconfig", or needs to install or update the Catppuccin Macchiato theme for git-delta.
---

# Delta Catppuccin Setup

## File structure

- `git/catppuccin.gitconfig` — stowed to `~/.config/git/catppuccin.gitconfig` via `stow .`
- `gitconfig/.gitconfig` — contains `[include]` and `[delta] features`

## Installation

1. Download the official catppuccin/delta file:
```bash
gh api repos/catppuccin/delta/contents/catppuccin.gitconfig --jq '.content' | base64 -d > dotfiles/git/catppuccin.gitconfig
```

2. Stow via XDG package (`stow .` already covers the `git/` dir):
```bash
stow .
# → ~/.config/git/catppuccin.gitconfig
```

3. In `gitconfig/.gitconfig`:
```gitconfig
[include]
    path = ~/.config/git/catppuccin.gitconfig

[delta]
    features = catppuccin-macchiato
```

## Prerequisites

- `git-delta` and `bat` in `Brewfile` (already present)
- bat theme "Catppuccin Macchiato" in `bat/config` (official catppuccin/delta requirement)

## Delta flags to remember

- **No `--no-side-by-side`** — disable side-by-side by not passing `-s`/`--side-by-side`
- **No `--side-by-side=false`** — syntax not supported
- `--no-gitconfig` — resets all gitconfig (useful for context-specific overrides)
- `--syntax-theme` not needed when using the `features` method (already included in the feature block)

## FZF_GIT_PAGER

For fzf-git diff previews (panel too narrow for side-by-side), in `zsh/fzf.zsh`:
```zsh
export FZF_GIT_PAGER="delta --no-gitconfig --line-numbers --dark --syntax-theme 'Catppuccin Macchiato'"
```

- `--no-gitconfig` disables side-by-side that would otherwise be read from gitconfig
- Explicit `--syntax-theme` required: `--no-gitconfig` bypasses the feature block
