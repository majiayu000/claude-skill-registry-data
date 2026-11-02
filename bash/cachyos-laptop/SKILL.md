---
name: cachyos-laptop
description: "Use for ASUS Zephyrus on CachyOS: battery, install, game."
version: 1.0.0
author: Vesper
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [cachyos, asus, zephyrus, laptop, linux, gaming, proton, dual-boot, power-management]
    related_skills: [windows-maintenance, cities-skylines-modding]
---

# CachyOS Laptop — Tyler's ASUS Zephyrus G16

Tyler's daily driver: **ASUS Zephyrus G16 on CachyOS**. This umbrella skill covers the full lifecycle — from initial installation (dual-boot) through everyday management (battery limits, trackpad, SSH) to gaming (Proton, Epic, Legendary, shader fixes).

## Architecture: Setup → Manage → Game

### 1. Installation & Dual-Boot

See `references/dual-boot-install.md` for the full flow. Key steps:
- Pre-flight: disable Secure Boot (ASUS: Boot → OS Type = Other OS), disable Windows Fast Startup, pause BitLocker
- Shrink C: from Windows (Disk Management); if stuck at 2GB, `powercfg /h off` in admin PowerShell
- Use **Manual partitioning** in the CachyOS installer — create a ~4 GiB FAT32 /boot (Limine needs space) + btrfs root
- Boot manager: Limine (CachyOS default, works with Windows dual-boot via `limine-scan`)
- NVIDIA driver install: `sudo pacman -S nvidia-dkms nvidia-utils lib32-nvidia-utils cachyos-nvidia-conf`
- **Pitfall:** Windows ESPs (260 MiB) are too small for Limine — use manual partitioning with a dedicated ~4 GiB /boot partition

### 2. Power & Hardware Management

See `references/power-management.md` for full detail.

**Battery charge limit** — verified BAT1, not BAT0. Persist via systemd oneshot service:
```bash
echo 80 | sudo tee /sys/class/power_supply/BAT1/charge_control_end_threshold
```
Create and enable `battery-limit.service` (oneshot, WantedBy=multi-user.target).

**asusctl CLI** — uses subcommands, not flags: `asusctl battery limit 80`, `asusctl battery info`.

**Trackpad accidental right-click** — KDE Wayland: set `ClickMethod=clickfinger` in `~/.config/kcminputrc` under the device section for `ASUP1207:00 093A:3012 Touchpad`. Two-finger click only, takes effect on relogin.

**SSH access** — `ssh -i ~/.ssh/cachyos_laptop tyler@192.168.0.34` (LAN-only, IP may change). Laptop shell is **fish** (no heredocs; use `printf`). UFW: `sudo ufw allow ssh`.

### 3. Gaming (Proton & Steam Play)

See `references/proton-gaming.md` for full detail.

**ProtonUp-Qt + GE-Proton**: Install via CachyOS repos, select GE-Proton in ProtonUp-Qt, force per-game in Steam Properties → Compatibility. Per-game is better than global (native Linux games may work better without Proton).

**Vulkan shader compilation**: First launch takes 10+ min — one-time tax unless cache corrupts. 33% hang = corrupted cache; clear via Steam Settings → Downloads → Clear Shader Cache, or delete `compatdata/<appid>/pfx/drive_c/.../DXVK/*.dxvk-cache`.

**Epic Games via Legendary** (no Heroic):
```bash
curl -L -o ~/legendary https://github.com/legendary-gl/legendary/releases/latest/download/legendary_linux_x64
chmod +x ~/legendary && ~/legendary auth
GAMEID=<appid> ~/legendary launch "Game Name" --wine umu-run
```
- **KDE power management doesn't track gamepads** — wrap with `kde-inhibit --power` or `systemd-inhibit --what=idle:sleep --`
- **CPU melt after 15-20 min** = DXVK async config fix in prefix's DXVK config
- **Shader cache** doesn't persist per-launch — set `DXVK_STATE_CACHE_PATH` to a persistent dir

**Xbox Game Pass**: Native app doesn't work — xCloud streaming in browser does.

### App installs beyond gaming

See `references/app-installs.md` for the "target not found" playbook — checking
repo membership before advising, and the vendor-tarball `pacman -U` route
(Zoom recipe verified 9/29).

**Non-Steam games (RuneScape 3)**: Bolt launcher (`paru -S bolt-launcher`), needs `gtk2` + `openssl-1.1`. Or the official flatpak `com.jagex.RuneScape`.

## Verification

- Battery limit: `cat /sys/class/power_supply/BAT1/charge_control_end_threshold` → 80
- Trackpad: right-click requires two fingers (no corner zones)
- Proton game: launches with GE-Proton via Steam
- Legendary: `~/legendary list-installed` shows downloaded games

## Pitfalls

- The laptop's shell is **fish** — no heredocs, no bash `for` loops. Use `printf` for file writes.
- Dual-boot Limine needs a 4 GiB /boot — Windows ESPs are only 260 MiB
- GE-Proton shows as "unused" in ProtonUp-Qt after install — normal
- Fish hard-errors on unmatched globs in `cp`/`rm`
- KDE power management doesn't track gamepad input — use `kde-inhibit --power` or Caffeine

## Reference Files

- `references/dual-boot-install.md` — Full CachyOS dual-boot install walkthrough
- `references/power-management.md` — ASUS battery limits, trackpad fix, asusctl, SSH
- `references/proton-gaming.md` — Proton/GE-Proton, Legendary/Epic, Game Pass, saves