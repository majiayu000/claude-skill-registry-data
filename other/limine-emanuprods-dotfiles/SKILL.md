---
name: limine"
description: Installs, configures, and troubleshoots the Limine bootloader on Arch Linux and other Linux systems — limine.conf syntax, UEFI/BIOS deployment, boot entries for Linux/Windows, kernel cmdline, initramfs, UKI, Secure Boot enrollment, and automatic updating via hooks. Use when setting up Limine, editing limine.conf, adding boot entries, dual-booting, or debugging boot failures (Failed to open image, wrong ESP, missing config).
---

# Limine Bootloader

Limine is a modern, fast, and secure bootloader. This skill covers installation, `limine.conf` authoring (its own syntax, NOT GRUB/systemd-boot syntax), deployment on UEFI and BIOS, and the Arch Linux integration hooks.

## Install (Arch)

```bash
sudo pacman -S limine
# UEFI: copy the EFI executable to your ESP
sudo mkdir -p /esp/EFI/limine
sudo cp /usr/share/limine/limine-uefi-cd.bin /usr/share/limine/limine-uefi.bin /esp/EFI/limine/ 2>/dev/null || true
sudo cp /usr/share/limine/BOOTX64.EFI /esp/EFI/BOOT/ 2>/dev/null || true
# BIOS (legacy MBR systems) — write stage 3 to the disk
sudo limine bios-install /dev/sdX
```

Arch installs `limine` with a systemd unit that deploys to a detected ESP (`/efi`, `/boot`, `/boot/efi`, `/limine`) and runs `limine-update` automatically when kernels change.

## limine.conf — location & discovery

Limine searches (first match wins) on EFI: `<EFI app path>/limine.conf`, `/EFI/BOOT/limine.conf`, then per-volume `/boot/limine/limine.conf`, `/boot/limine.conf`, `/limine/limine.conf`, `/limine.conf`. On BIOS: root, `/boot`, `/limine`, `/boot/limine` of a supported partition.

- **`boot():`** in paths = the partition where `limine.conf` sits. Use `boot():/vmlinuz-linux`.
- If kernel/initramfs live on **another** partition (e.g. separate /boot that is not the ESP), use `uuid(PARTUUID):/` — the **PARTUUID** of the FAT /boot partition.
- Keep one canonical config; a stray `limine.conf` in a search path can shadow yours.

## Minimal working config

```
timeout: 5

/Arch Linux
    protocol: linux
    path: boot():/vmlinuz-linux
    cmdline: root=UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx rw
    module_path: boot():/initramfs-linux.img
```

Kernel cmdline essentials: `root=UUID=…` (filesystem UUID of `/`), `rw` (or `ro`), `quiet`, `splash`. For AMD: add `initrd=/amd-ucode.img`; Intel: `initrd=/intel-ucode.img`. **mkinitcpio ≥38 bundles microcode via the `microcode` hook** — then omit explicit initrd lines.

## Menu entries & sub-entries

- Entry starts with `/`, sub-entries with `//`, deeper with more slashes.
- A `+` between slashes and title expands a directory by default: `/+Arch Linux`.
- `default_entry`: 1-based index (`1`) or path (`OSes/Arch Linux`); duplicates: `Name#N`.
- Options are `name: value`, case-insensitive names; comments are full-line `#`.

## Global options (frequently used)

| Option | Meaning |
|--------|---------|
| `timeout` | seconds before auto-boot; `no` = wait forever; `0` = boot instantly without menu (decimals OK, capped 9999) |
| `default_entry` | auto-selected entry (index or path) |
| `remember_last_entry` | `yes` = last booted entry wins (UEFI) |
| `quiet` | `yes` = suppress output; any key during timeout shows menu |
| `graphics` | `no` = text mode menu |
| `wallpaper` | path to BMP/PNG/JPEG/QOI; multiple → random |
| `wallpaper_style` | `tiled`/`centered`/`stretched` |
| `verbose` / `terse` | debug info / suppress loading messages |
| `serial`, `serial_baudrate` | serial console (BIOS only for baudrate) |

## Dual-boot & extras

Windows (UEFI) entry:

```
/Windows
    protocol: chainload
    image_path: boot():/EFI/Microsoft/Boot/bootmgfw.efi
```

(Or use `FIND_BOOTLOADERS=yes` in `/etc/default/limine` to auto-add systemd-boot/rEFInd/default EFI loader entries.)

Memory test: `pacman -S memtest86+-efi`, then chainload its binary. Snapshots (Arch): put `//Snapshots` under a Linux entry and install `limine-snapper-sync` — it auto-generates snapshot entries; limits: `LIMIT_USAGE_PERCENT` (default 85), `MAX_SNAPSHOT_ENTRIES`.

## Arch Linux automation (drop-in)

`/etc/default/limine` overrides all drop-ins; use `+=` to append cmdline:

```
KERNEL_CMDLINE[default]+=rw root=UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
KERNEL_CMDLINE[default]+=quiet splash
ENABLE_UKI=no            # yes = boot UKIs
FIND_BOOTLOADERS=yes     # detect systemd-boot/rEFInd/default EFI loader
DRACUT_FALLBACK=no       # or a kernel name / yes
```

After manual edits: `sudo limine-update` regenerates `esp/limine.conf` from the kernel packages.

- `limine-mkinitcpio-hook`: auto-updates boot entries on kernel install/update/removal (packages `limine-mkinitcpio-hook` or `limine-dracut-support`).
- `kernel-modules-hook`: keeps the previous kernel if an upgrade fails (survive reboot).

## Secure Boot

Two protection layers (FAT is writable by anyone with access):

1. **Resource checksums**: append BLAKE2B to paths — `boot():/vmlinuz-linux#<128-char b2sum>`. Generate with `b2sum /path/to/file`.
2. **Config enrollment**: embed limine.conf's own BLAKE2B into the EFI binary:
   ```bash
   limine enroll-config /esp/EFI/limine/BOOTX64.EFI <check-sum-of-limine.conf>
   ```
   Arch automation: `ENABLE_ENROLL_LIMINE_CONFIG=yes` in `/etc/default/limine` — then sign with `sbctl sign` and enroll keys in firmware.
   ⚠️ With enrollment enabled, editing limine.conf without re-enrolling **prevents booting** (even with Secure Boot off). Keep a fallback bootloader for recovery.

## Troubleshooting

- **`Failed to open image with path: … is the path correct?`** — wrong `boot():`/`uuid():` target or firmware didn't initialize the disk during boot (fast boot). Disable fast boot or force disk init in firmware; verify the path exists on the intended partition.
- **Config ignored / wrong menu** — another `limine.conf` shadows yours (check discovery order); move/delete stray copies.
- **Timeout misbehavior** — UEFI Boot Loader Interface vars (`LoaderConfigTimeoutOneShot` from `systemctl reboot --boot-loader-menu=`) override `timeout`; persistent `bootctl set-timeout` applies only where `timeout` is unset.
- **Boot entry on another disk fails** — firmware storage init; disable fast boot.
- **Kernel upgrades don't appear in menu** — run `sudo limine-update`; verify hooks enabled.
- **Windows entry broken after update** — Windows rewrites its bootmgr; verify `image_path` and ESP PARTUUID.

## Verify after changes

1. `limine --version` — binary present.
2. `sudo limine-update` — regenerates config; inspect `esp/limine.conf`.
3. `bootctl status` (UEFI) — Limine listed as `Limine` EFI entry; check `LoaderEntryOneShot`.
4. Reboot and confirm: menu shows (or auto-selects) expected entries; Linux boots; Windows boots; snapshots work.

## Sources

- Limine config docs: https://github.com/limine-bootloader/limine/blob/trunk/CONFIG.md
- ArchWiki Limine: https://wiki.archlinux.org/title/Limine
- Limine GitHub: https://github.com/limine-bootloader/limine