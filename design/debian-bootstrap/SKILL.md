---
name: debian-bootstrap
description: Bootstrap a new Debian/Ubuntu system with your standard configuration. Portable dotfiles, SSH config, shell setup, and SOPS secrets - no Nix required. Use when setting up a new machine or migrating away from NixOS.
---

# Debian Bootstrap

Recreate your development environment on any Debian/Ubuntu system.

## Quick Start

```bash
cd ~/.claude/skills/debian-bootstrap
just                    # See all commands
just setup-all          # Full setup (packages + tools + dotfiles + secrets)
```

**First time?** See [BOOTSTRAP.md](BOOTSTRAP.md) for the complete checklist including manual steps (age key, secrets.yaml).

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        debian-bootstrap                          │
├─────────────────────────────────────────────────────────────────┤
│  apt (packages.txt)     │  System packages (git, curl, htop)   │
├─────────────────────────────────────────────────────────────────┤
│  mise (mise.toml)       │  Everything else:                     │
│                         │  - Languages: node, python            │
│                         │  - CLI: bat, fd, rg, delta, lazygit   │
│                         │  - Cloud: gh, hcloud, awscli          │
├─────────────────────────────────────────────────────────────────┤
│  uv                     │  Python package management            │
├─────────────────────────────────────────────────────────────────┤
│  SOPS/Age               │  Encrypted secrets                    │
└─────────────────────────────────────────────────────────────────┘
```

**Two bootstrappers, one config file:**
- `mise` manages all dev tools via `mise.toml`
- `uv` handles Python packages (10-100x faster than pip)

## What's Included

| Component | Source | Target |
|-----------|--------|--------|
| Dev tools | `mise.toml` | `~/.config/mise/config.toml` |
| SSH config | `dotfiles/ssh_config` | `~/.ssh/config` |
| Bash config | `dotfiles/bashrc` | `~/.bashrc` |
| Git config | `dotfiles/gitconfig` | `~/.gitconfig` |
| Starship prompt | `dotfiles/starship.toml` | `~/.config/starship.toml` |
| System packages | `packages.txt` | via apt |
| SOPS setup | `scripts/setup-sops.sh` | `~/.config/sops/` |

## Commands

```bash
# Full setup
just setup-all             # Everything in order

# Individual components
just install-packages      # apt packages only
just install-extras        # mise + uv + all dev tools
just install-dotfiles      # All dotfiles
just setup-sops            # SOPS/Age encryption

# Secrets & Auth
just decrypt-ssh-keys      # Extract SSH keys + add to agent
just setup-gh-auth         # Authenticate GitHub CLI
just setup-glab-auth       # Authenticate GitLab CLI

# Tool management (after setup)
mise install               # Install tools from mise.toml
mise upgrade               # Update all tools
mise list                  # Show installed tools
```

## File Structure

```
debian-bootstrap/
├── SKILL.md               # This file
├── BOOTSTRAP.md           # Step-by-step first-time setup guide
├── justfile               # All commands
├── mise.toml              # Dev tools (the source of truth)
├── packages.txt           # apt packages (system only)
├── dotfiles/
│   ├── ssh_config
│   ├── bashrc
│   ├── gitconfig
│   └── starship.toml
└── scripts/
    ├── install-extras.sh  # Installs mise, uv, then mise install
    └── setup-sops.sh      # SOPS/Age setup
```

## Adding Tools

Edit `mise.toml` and run `mise install`:

```toml
[tools]
# Languages
node = "lts"
python = "3.12"
go = "latest"

# CLI tools via ubi (GitHub releases)
"ubi:sharkdp/bat" = "latest"
"ubi:jesseduffield/lazygit" = "latest"
```

## Secrets Management

Uses SOPS with Age encryption (same as NixOS setup):

```bash
# Decrypt secrets
sops -d ~/.claude/secrets.yaml

# Edit secrets
sops ~/.claude/secrets.yaml

# Extract single secret
sops -d --extract '["github_token"]' ~/.claude/secrets.yaml
```

## Migration from NixOS

This skill was generated from your NixOS/Home Manager config.
All Nix-specific paths have been converted to standard locations.
