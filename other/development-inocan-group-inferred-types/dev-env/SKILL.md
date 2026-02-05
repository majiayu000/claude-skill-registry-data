---
name: dev-env
description: Manage Jeremy's global dev environment (git, nvim, shell configs) and install tools. Use when asked to change global configs, add tools to the environment, or modify dotfiles.
---

# Managing Jeremy's Dev Environment

Use this skill to make changes to Jeremy's global configs (git, nvim, shell, etc) or to install new tools into Jeremy's global environment. Only do this when Jeremy explicitly asks for it.

## Repository Location

Jeremy's dev environment is managed through nix at `~/nix/public-base`.

## Directory Structure

- `config/` — Config files organized by tool:
  - `git/` — git config, ignore, attributes
  - `nvim/` — neovim configuration
  - `zsh/` — shell config
  - `ghostty/` — terminal config
  - `bat/`, `direnv/`, `starship.toml`, etc.
- `flake.nix` — Package definitions (what tools are installed)
- `scripts/` — Custom utility programs
- `scripts.nix` — Script definitions

## Workflow

### 1. Check for uncommitted changes first

```bash
git -C ~/nix/public-base status
```

If there are uncommitted changes in the same files you need to edit, stop and ask Jeremy for instructions. If uncommitted changes are elsewhere, note them but proceed.

### 2. Make your edits

Edit the appropriate files in `~/nix/public-base/`.

### 3. Install the changes

Run `i` to rebuild and install the nix environment.

### 4. Test the change

Test it yourself if possible, or ask Jeremy to test if it requires restarting the terminal or Claude Code.

### 5. Commit and push (if Jeremy approves)

Only commit your changes — don't include any pre-existing uncommitted changes.

**Important:** `git push` doesn't work due to a config issue. Use this instead:
```bash
git -C ~/nix/public-base push lol && git -C ~/nix/public-base pull
```
