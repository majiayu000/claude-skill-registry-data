---
name: Homelab
description: NixOS homelab infrastructure management for the home repository. USE WHEN working with NixOS systems, home-manager configs, networking, services, or personal infrastructure.
---

# Homelab Management Skill

## Purpose
Expert assistance managing personal NixOS infrastructure in the home repository.

### Context Detection

**This skill activates when:**
- Current working directory is `/home/vincent/src/home` or subdirectories
- User asks about specific hosts (kyushu, aomi, demeter, rhea, athena, etc.)
- User mentions home repository infrastructure, services, or configurations
- Files in `/systems`, `/home/common`, or `/modules` directories are referenced
- User asks about DNS management, VPN, or homelab services

## Repository Structure
- **Repository location**: ~/src/home
- **System configs**: /systems/<hostname>/
- **Home configs**: /home/common/
- **Custom packages**: /pkgs/
- **Globals**: globals.nix (machine definitions, DNS zones, VPN)
- **Tools**: /tools/ (custom Go tools)
- **Modules**: /modules/ (custom NixOS modules)
- **Keyboards**: /keyboards/ (QMK/ZMK firmware)
- **Imperative**: /imperative/ (non-NixOS host configs)

## Key Machines

### Unstable Systems (nixos-unstable)
- **kyushu**: Desktop/workstation
- **aomi**: Laptop/portable
- **sakhalin**: Development
- **foobar**: Testing

### Stable Systems (25.05)
- **athena**: Production server
- **demeter**: Infrastructure server
- **aix**: Raspberry Pi 4
- **aion**: Raspberry Pi 4
- **rhea**: Raspberry Pi 4
- **kerkouane**: Raspberry Pi 4

### Desktop Types
- **sway**: Traditional tiling window manager
- **niri**: Modern scrollable tiling window manager

## Services and Infrastructure

### DNS Management
- Managed via `globals.nix` zones
- Update tool: `tools/update-gandi-dns.sh`
- Provider: Gandi LiveDNS API
- Domains: demeester.fr, sbr.pm, openshift-pipelines.org, etc.

### VPN Configuration
- Wireguard configurations in `/modules/`
- Client module: `modules/wireguard-client`
- Server module: `modules/wireguard-server`
- Network topology in `globals.nix`

### Container Services
- Docker/Podman setups
- System-manager for containerized services
- Service definitions per host

### Secrets Management
- **agenix** for encrypted secrets
- Yubikeys for age encryption
- Host SSH keys for system-level decryption
- Secrets defined in `secrets.nix`

## Common Operations

### Building and Deploying
```bash
# Build and switch current system
make switch

# Build and activate on next boot
make boot

# Test build without switching
make dry-build

# Build specific remote host
make host/<hostname>/build

# Deploy to remote host (boot) - ALWAYS ASK FIRST
make host/<hostname>/boot

# Deploy to remote host (switch) - ALWAYS ASK FIRST
make host/<hostname>/switch
```

### Package Management
```bash
# Build a package
nix build .#<package-name>

# Install a package
nix profile install .#<package-name>

# List available packages
nix flake show
```

### Maintenance
```bash
# Format Nix files
make fmt

# Clean old generations (>15 days) and build results
make clean

# Update flake inputs
nix flake update

# Run pre-commit checks
make pre-commit
```

### Keyboard Firmware
```bash
# Build Moonlander QMK firmware
make keyboards/moonlander/build

# Build Eyelash Corne ZMK firmware
make keyboards/eyelash_corne/build

# Generate keymap visualizations
make keyboards/draw
make keyboards/<name>/draw
```

### DNS Operations
```bash
# Show current DNS records
./tools/show-dns.sh

# Update Gandi DNS (requires GANDIV5_PERSONAL_TOKEN)
make dns-update-gandi
```

## Safety Protocols

### Deployment Safety
- **ALWAYS** ask before deploying to remote hosts
- **ALWAYS** dry-build before deploying
- **ALWAYS** confirm target host explicitly
- Check service dependencies before deployment
- Never deploy automatically

### Git Operations
- NEVER update git config without asking
- NEVER run destructive git commands (force push, hard reset) without explicit request
- NEVER skip hooks (--no-verify) unless explicitly requested
- NEVER force push to main/master without warning

### Secrets and Security
- Do not commit files with secrets (.env, credentials.json)
- Warn if attempting to commit sensitive files
- Use agenix for all secret management
- Verify secrets are encrypted before committing

## Architecture Patterns

### Host Configuration
Each host has:
- `boot.nix`: Boot configuration (bootloader, initrd, kernel modules)
- `hardware.nix`: Hardware-specific settings (mounts, hardware imports)
- `extra.nix` (optional): Additional host-specific config
- `home.nix` (optional): Host-specific home-manager config

### Adding a New Host
1. Create `/systems/<hostname>` directory with `boot.nix` and `hardware.nix`
2. Add host entry in `flake.nix` nixosConfigurations using `libx.mkHost`
3. Add machine metadata to `globals.nix` (IPs, SSH keys, syncthing ID)
4. Update `secrets.nix` with host SSH key if using secrets

### Adding a New Package
1. Create package directory in `/pkgs/<package-name>` with `default.nix`
2. Add entry to `/pkgs/default.nix` using `pkgs.callPackage`
3. Package available via `nix build .#<package-name>`

## Pre-commit Hooks

Configured in `flake.nix`:
- **Go**: gofmt formatting
- **Nix**: nixfmt-rfc-style formatting, deadnix linting
- **Python**: flake8, ruff linting
- **Shell**: shellcheck

Install hooks: `make install-hooks`

## Testing

### Go Tools
```bash
cd tools/<tool-name>
go test ./...
```

### NixOS Configurations
```bash
# Build test
nixos-rebuild build --flake .#<hostname>

# Dry run
nixos-rebuild dry-build --flake .#<hostname>
```

## Troubleshooting

### Build Failures
1. Check `nix flake check` for issues
2. Review recent changes with `git diff`
3. Verify flake.lock is up to date
4. Check for syntax errors with `nixfmt`

### Deployment Issues
1. Verify SSH access to target host
2. Check network connectivity
3. Review target host logs
4. Ensure secrets are properly decrypted

### Service Issues
1. Check systemd status: `systemctl status <service>`
2. Review logs: `journalctl -u <service>`
3. Verify configuration in globals.nix
4. Check dependencies are running

## Quick Reference

### File Locations
- Machine definitions: `globals.nix`
- Flake configuration: `flake.nix`
- Library functions: `lib/default.nix`
- Overlays: `overlays/default.nix`
- Common system modules: `systems/common/`
- Common home modules: `home/common/`

### Environment Variables
- `XDG_CONFIG_HOME`: `~/.config` (XDG base directories enabled)
- Nix config: `~/.config/nix/nix.conf`

### Binary Caches
- vdemeester.cachix.org
- chapeau-rouge.cachix.org
- nixos-raspberrypi.cachix.org

Remember: This is a production infrastructure. Always prioritize safety and ask for confirmation before making changes to remote systems.

## Examples

**Example 1: Deploying NixOS configuration**
```
User: "Deploy the updated config to kyushu"
→ Checks current configuration in home repository
→ Reviews changes with git diff
→ Builds configuration with nixos-rebuild build
→ Confirms target host is correct (kyushu)
→ Deploys with nixos-rebuild switch --target-host
→ Result: Configuration safely deployed to homelab server
```

**Example 2: Managing services**
```
User: "Restart the wireguard service on all hosts"
→ Checks which hosts run wireguard in globals.nix
→ SSHs to each host
→ Restarts systemd service: systemctl restart wg-quick-wg0
→ Verifies service is running
→ Checks VPN connectivity
→ Result: All wireguard tunnels restored
```

**Example 3: Troubleshooting DNS issues**
```
User: "Why can't I reach home.example.com?"
→ Checks DNS configuration in globals.nix
→ Verifies Pi-hole is running
→ Tests DNS resolution: dig home.example.com
→ Checks firewall rules and port forwarding
→ Reviews service logs for errors
→ Result: DNS issue identified and resolved
```
