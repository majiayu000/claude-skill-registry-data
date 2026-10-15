---
name: nix-health
description: Use this when diagnosing or fixing a user's Nix installation — checks flakes, version, caches, max-jobs, direnv, rosetta, trusted-users, and shell config
---

# Nix Health Checks

Run these checks to diagnose problems with a Nix installation. For each failing check, report the issue and suggestion to the user.

## 1. Nix Installer

Identify which installer was used:
```sh
# NixOS/nix-installer and Determinate Nix both leave a receipt:
cat /nix/receipt.json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','unknown'))" 2>/dev/null

# On macOS, check launchd service names:
ls /Library/LaunchDaemons/*nix* /Library/LaunchDaemons/*determinate* 2>/dev/null

# On Linux, check systemd:
systemctl list-units '*nix*' '*determinate*' --no-pager 2>/dev/null

# Check for determinate-nixd (Determinate Nix specific):
which determinate-nixd 2>/dev/null
```

- If `determinate-nixd` exists or `systems.determinate.*` services are present → ⚠️ **Determinate Nix** detected (proprietary fork). **Suggestion**: Switch to the official installer or [NixOS/nix-installer](https://github.com/NixOS/nix-installer) for a fully open-source Nix. See https://nixos.org/download/
- If `/nix/receipt.json` exists but no `determinate-nixd` → ℹ️ **[NixOS/nix-installer](https://github.com/NixOS/nix-installer)** (community, formerly DeterminateSystems/nix-installer)
- If no receipt and `org.nixos.nix-daemon` (macOS) or `nix-daemon.service` (Linux) → ℹ️ **Official** installer

## 2. Flakes Enabled

```sh
nix config show 2>/dev/null | grep '^experimental-features'
```

Value must contain both `flakes` and `nix-command`. If missing:
- **Suggestion**: See https://nixos.wiki/wiki/Flakes#Enable_flakes

## 3. Nix Version

```sh
nix --version
```

Version must be ≥ 2.16.0. If older:
- **Suggestion**: See https://nixos.asia/en/howto/nix-package

## 4. Max Jobs

```sh
nix config show 2>/dev/null | grep '^max-jobs'
```

Value must be > 1 (ideally `auto`). If set to 1:
- **Suggestion**: Set `max-jobs = auto` in `/etc/nix/nix.conf` (Linux) or `~/.config/nix/nix.conf` (macOS without nix-darwin). On NixOS use `nix.settings.max-jobs = "auto"`. On nix-darwin use the same option.

## 5. Caches

```sh
nix config show 2>/dev/null | grep '^substituters'
```

Must include `https://cache.nixos.org`. Also check for project-specific caches defined in:
- `nixConfig.extra-substituters` in the project's `flake.nix`
- `cache.url` in the project's `vira.hs` (Vira CI config)

If any required caches are missing from the user's substituters:
- **Suggestion**: Add missing caches to nix.conf `substituters`. For Cachix caches run `nix run nixpkgs#cachix use <name>`.

## 6. Trusted Users

```sh
nix config show 2>/dev/null | grep '^trusted-users'
whoami
```

The current user (or a group they belong to, or `*`) should appear in `trusted-users`. If missing:
- On NixOS: `nix.settings.trusted-users = [ "root" "<user>" ];`
- Otherwise: add `trusted-users = root <user>` to `/etc/nix/nix.conf` and restart the daemon (`sudo pkill nix-daemon`)

## 7. Direnv

```sh
which direnv 2>/dev/null && readlink -f "$(which direnv)"
```

Direnv should be installed and its resolved path should be inside `/nix/store/`. If not installed or installed outside Nix:
- **Suggestion**: Install direnv via Nix (home-manager). See https://github.com/juspay/nixos-unified-template

## 8. Rosetta (macOS only)

Only check on Apple Silicon Macs:
```sh
sysctl -n sysctl.proc_translated 2>/dev/null
```

If the value is `1`, Nix is running under Rosetta emulation which slows builds:
- **Suggestion**: Disable Rosetta for your terminal (Finder → Get Info → uncheck "Open using Rosetta"). Uninstall and reinstall Nix for `aarch64-darwin`. See https://nixos.asia/en/install

## 9. Homebrew (macOS only)

```sh
which brew 2>/dev/null
```

If Homebrew is installed, flag as ⚠️ — it can interfere with Nix environments (e.g. conflicting library paths, shadowed binaries).
- **Suggestion**: Prefer managing packages with Nix for better reproducibility. See https://nixos.asia/en/nix-first. Inventory existing packages with `brew list`, install equivalents via Nix, then consider removing Homebrew.

## 10. Shell Dotfiles

Check if shell config files are managed by Nix (symlinked into `/nix/store`):
```sh
# For zsh:
ls -la ~/.zshrc ~/.zshenv ~/.zprofile ~/.zlogin ~/.zlogout 2>/dev/null
# For bash:
ls -la ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
```

Any dotfile whose resolved path is **not** under `/nix/store/` is unmanaged — flag it as ⚠️.
- **Suggestion**: Use home-manager to manage shell configuration. See https://github.com/juspay/nixos-unified-template

## Reporting

Present results as a table with columns: Check, Status (✅/❌/⚠️), Details, and Suggestion (if failing). Mark checks that don't apply to the current OS as skipped.
