---
name: desktop
description: >-
  Desktop and workstation environment: Windows dev-env patterns, system
  optimization and cleanup, console encoding fixes (cp1251/CRLF), Windows 11
  theming for Linux tools, Wine and game setup on Linux, Firefox performance
  and extensions, zram swap, disk formatting, and PipeWire mic noise suppression.
---

# desktop — workstation environment

> Home branch in Memora: `root/skill/desktop`.
>
> Host anchor: this workstation runs Windows (`windows-*` parts apply directly;
> Fedora/Linux parts are reference playbooks for Linux targets or VMs).

## Choosing a part

| Task | Part |
|---|---|
| Console stdout encoding (`cp1251` vs `UTF-8`), CRLF/LF when writing files (Windows host) | `parts/windows-encoding-fixes/` |
| Windows dev-env patterns: paths, `winget`/`choco`, shell differences (Windows host) | `parts/windows-env/` |
| Windows system optimization and cleanup: temp/cache, autostart, services (Windows host) | `parts/windows-optimize/` |
| Make Linux desktop tools look like Windows 11 (Dolphin, Konsole, omp TUI) | `parts/themes/` |
| Full Wine setup on Fedora/Linux for Windows games and repacks | `parts/wine-setup/` |
| GTA IV under Wine playbook (RGL error, FusionFix, DXVK, shaders) | `parts/gta4-wine-fix/` |
| Firefox performance and `about:config` tuning (`user.js`, hardware acceleration) | `parts/firefox-optimization/` |
| Verified Firefox extension bundle (YourCodecs H.264, uBlock Origin, dark backgrounds) | `parts/firefox-extensions/` |
| `zram` compressed swap on Linux (`systemd-zram-generator`) | `parts/zram-optimize/` |
| Format, repartition, and mount disks on Linux (`ext4`, `btrfs`, `NTFS`, `exFAT`) | `parts/disk-formatting/` |
| Fix a noisy microphone on Linux with PipeWire (`EasyEffects` + `RNNoise`) | `parts/mic-noise-suppression/` |
| Fedora GNOME (Wayland) display warmth and gamma tuning | `parts/fedora-warm-colors/` |

## Rules

- Walk `root/skill/desktop` in Memora before making system-level changes.
- Confirm any registry, service, startup, or partition change via `ask_questions`, and use `request_elevation` when OS administrator rights are required.
- Keep Windows host steps separate from Linux/Fedora target steps; never run Linux-only commands on the Windows host.

## Related

`dev` (application build and coding style), `prompt-to-exe` (packaging Python apps into Windows `.exe` bundles), `security` (`skills/security/parts/windows-ad/`).
