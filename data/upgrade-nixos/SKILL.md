---
name: upgrade-nixos
description: |
  This skill upgrades NixOS to a new release version (e.g., 25.05 → 25.11).
  Triggers: "upgrade nixos", "upgrade to new release", "update nixos version",
  "move to nixos 25.11", "nixos release upgrade", "upgrade system version".
  Researches breaking changes, updates flake inputs, guides through upgrade.
  Not for flake.lock updates within same release (use upgrade-flake for that).
---

# Upgrade NixOS Release

Upgrade NixOS to a new stable release version. This involves updating version-pinned flake inputs and handling any breaking changes.

## Process

1. **Check current state**
   ```bash
   nixos-version
   nix --version
   ```

2. **Identify version-pinned inputs in flake/flake.nix** that need updating:
   - `nixpkgs` (e.g., `nixos-25.05` → `nixos-25.11`)
   - `home-manager` (e.g., `release-25.05` → `release-25.11`)
   - `nix-darwin` (e.g., `nix-darwin-25.05` → `nix-darwin-25.11`)
   - `stylix` (e.g., `release-25.05` → `release-25.11`)

3. **Research the target release**
   - Use web search to find the latest stable NixOS release
   - Check release notes for breaking changes relevant to this config
   - Verify release branches exist for home-manager, stylix, nix-darwin

4. **Identify breaking changes** that affect this config:
   - Scan modules for services/packages that might be affected
   - Key areas: Hyprland, Docker, Steam, Secure Boot, impermanence

5. **Create upgrade plan** (use creating-plans skill):
   - Save to `thoughts/shared/issues/NN-nixos-<version>-upgrade/plan.md`
   - Include exact file changes with line numbers
   - Include verification commands
   - Include rollback instructions

6. **Execute upgrade** (when user is ready):
   ```bash
   # Edit flake/flake.nix with new versions
   just update        # Update flake.lock
   just check         # Build without applying (safe)
   just switch        # Apply the upgrade
   ```

7. **Post-upgrade verification**:
   ```bash
   nixos-version
   nix --version
   docker --version
   systemctl status docker tailscaled
   hyprctl version
   ```

## What stays pinned (don't change)

- `lanzaboote` - explicit version pin (e.g., v0.4.2), not tied to NixOS releases
- `nixpkgs-unstable` - always tracks unstable
- Inputs that `follow` nixpkgs - automatically updated

## Rollback
Print out the instructions to:
```bash
sudo nixos-rebuild switch --rollback
git checkout flake/flake.nix flake/flake.lock
```

$ARGUMENTS
