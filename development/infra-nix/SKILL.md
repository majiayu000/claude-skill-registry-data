---
name: infra-nix
description: Use when working with Nix in the infra monorepo - devShells, devbox NixOS container, and Home-Manager user config.
---

# Infra Nix Patterns

## Overview

This repo uses Nix for development environments and the devbox container. See the global `nix` skill for general Nix knowledge.

## DevShells

| Shell | Purpose | Enter |
|-------|---------|-------|
| default | Terraform, Ansible, SOPS | `nix develop` or `direnv allow` |
| media-pipeline | Go development | `nix develop .#media-pipeline` |
| session-manager | Bash/shellcheck | `nix develop .#session-manager` |

### Add Package to DevShell

Edit `flake.nix`, find the relevant shell:

```nix
default = pkgsUnfree.mkShell {
  buildInputs = with pkgsUnfree; [
    # existing...
    newpackage  # Add here
  ];
};
```

Then: `direnv reload` or re-enter shell.

**Note:** Use `pkgsUnfree` for unfree packages (terraform), `pkgs` for everything else.

## Devbox Container

The only NixOS host. Runs in Proxmox LXC (CTID 320, IP .140).

### Key Files

```
flake.nix                              # Flake entry point
nixos/hosts/devbox/configuration.nix   # System config
home/users/cuiv/                       # Home-Manager config
  ├── default.nix                      # Main user config
  ├── git.nix                          # Git configuration
  ├── tools.nix                        # CLI tools
  └── shell.nix                        # Shell configuration
```

### Rebuild

From within devbox (SSH first):

```bash
ssh devbox
cd /path/to/infra

# Build and switch
sudo nixos-rebuild switch --flake .#devbox

# Build only (test)
nixos-rebuild build --flake .#devbox

# Rollback if broken
sudo nixos-rebuild switch --rollback
```

### Add System Package

Edit `nixos/hosts/devbox/configuration.nix`:

```nix
environment.systemPackages = with pkgs; [
  # existing...
  newpackage
];
```

### Add User Package

Edit `home/users/cuiv/tools.nix` (or create new module):

```nix
home.packages = with pkgs; [
  newpackage
];
```

## Workflow

1. Make changes to flake.nix or NixOS/Home-Manager configs
2. Format: `nix fmt` (uses nixfmt-rfc-style)
3. Check: `nix flake check`
4. If devShell change: `direnv reload`
5. If devbox change: SSH to devbox, run rebuild
6. Commit both `flake.nix` and `flake.lock`

## Never Do

- Edit `flake.lock` manually
- Change `system.stateVersion` or `home.stateVersion`
- Commit flake.nix without testing the change first
- Delete all old generations before verifying new config works
