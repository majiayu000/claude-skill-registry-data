---
name: device-maintenance
description: "Use for Windows, CachyOS, and TLS trust-store maintenance."
version: 1.0.0
author: Vesper
license: MIT
platforms: [linux, windows]
metadata:
  hermes:
    tags: [windows, cachyos, asus, zephyrus, linux, gaming, proton, tls, certificates, trust-store, maintenance]
---

# Device Maintenance — OS, Hardware, and Trust Stores

Class-level umbrella for machine upkeep across Tyler's boxes: the Windows
desktop, the ASUS Zephyrus G16 on CachyOS, and TLS trust-store audits.
Deep per-topic detail lives in the reference files below; the archived
original skills retain full session history.

## When to Use

- Windows reinstall/upgrade blocked by ghost drivers, debloat, service tuning,
  audio routing, or remote-control setup
- CachyOS laptop power, trackpad, SSH, dual-boot, or gaming (Proton/Legendary)
- A CA compromise or certificate-trust question on any machine/client

## Windows Maintenance (distilled)

- **Ghost drivers blocking upgrades:** `pnputil /enum-drivers`, find the
  `oemXX.inf`, then `pnputil /delete-driver oemXX.inf /uninstall /force`.
- **Debloat/perf:** disable telemetry, Game Bar, Cortana; analyze RAM/startup;
  remove bloatware via PowerShell.
- **Audio/routing:** Discord mic/VST chain and HTTP screenshot+input remote
  desktop servers are part of this lane.
- **Event-log forensics** for crash/root-cause work; SSH/tunnel setup for
  remote access.
- Full procedures and scripts are in the archived `windows-maintenance` skill.

## CachyOS Laptop — ASUS Zephyrus G16 (distilled)

- **Battery:** the real battery is `BAT1`, not `BAT0` (silent no-op on BAT0).
  Persist 80% via systemd oneshot writing
  `/sys/class/power_supply/BAT1/charge_control_end_threshold`; or
  `asusctl battery limit 80`.
- **Trackpad:** KDE Wayland `ClickMethod=clickfinger` in `kcminputrc` for the
  `ASUP1207:00 093A:3012 Touchpad` section (two-finger right-click only).
- **Shell is fish** — no heredocs; use `printf`. SSH:
  `ssh -i ~/.ssh/cachyos_laptop tyler@192.168.0.34`.
- **Dual-boot:** manual partitioning with ~4 GiB FAT32 /boot (Limine); Windows
  ESPs are too small. Disable Secure Boot + Fast Startup; pause BitLocker.
- **Gaming:** per-game GE-Proton via ProtonUp-Qt; shader-cache corruption shows
  as a 33% hang every launch; Epic via Legendary + umu-run (not Heroic).
  See `references/proton-gaming.md`.
- **Power management detail:** `references/power-management.md`.

## TLS Trust Audit (distilled)

- **Test each client separately** with a revoked test host plus a control host;
  exit codes: 0 = connected/vulnerable, 35/60 = rejected/good.
- **Map root inclusion per program first** (Apple/Chrome/Microsoft/Mozilla) —
  a root absent from a program means that client was never exposed.
- Walk every client store: OS, curl, Python `certifi` (per venv), Node
  (compiled-in), Git's `ca-bundle.crt`, Java/.NET/Go, Docker images.
- Use `--cacert` to test a specific bundle; grep hits are leads, not verdicts.
- Fixes are per layer (OS package, `pip`/`uv` certifi per venv, Node
  `--use-openssl-ca`, Git upgrade, container rebuild).
- Always re-run the same test after fixing and show the flip.

## Reference Files

- `references/power-management.md` — ASUS battery limits, trackpad fix, asusctl,
  SSH, fish-shell pitfalls
- `references/proton-gaming.md` — Proton/GE-Proton, Legendary/Epic, Game Pass,
  saves, shader caches

## Related

- `gaming/rs3-coop-play` — RuneScape co-op play plan
- `devops/cities-skylines-modding` — CS1 mod stack (carries xCloud note)

*-every store tested, with the control alongside-*
