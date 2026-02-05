---
name: upgrade-nixos
description: Upgrade NixOS to a new release version (e.g., 25.05 → 25.11) - researches breaking changes, updates flake inputs, and guides through the upgrade process
---

# Upgrade NixOS Release

Upgrade NixOS to a new stable release version. This involves updating version-pinned flake inputs and handling any breaking changes.

## Process

1. **Check current state**
   ```bash
   nixos-version
   nix --version
   ```

2. **Identify version-pinned inputs in flake.nix** that need updating:
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
   - Save to `scratch/plans/YYYY-MM-DD-nixos-<version>-upgrade.md`
   - Include exact file changes with line numbers
   - Include verification commands
   - Include rollback instructions

6. **Execute upgrade** (when user is ready):
   ```bash
   # Edit flake.nix with new versions
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
git checkout flake.nix flake.lock
```

$ARGUMENTS
