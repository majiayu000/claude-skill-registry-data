---
name: linux-dual-boot
description: Dual-boot Linux alongside Windows. Prep, install, boot.
---

# Linux Dual-Boot (Windows + Linux)

## Overview

Install a Linux distro alongside an existing Windows install on the same machine. Covers the pre-flight checklist that prevents the classic failures, the partition layout, and boot manager setup. Written from the Aug 2026 CachyOS research for Tyler's laptop test-drive.

## Pre-flight checklist (do these BEFORE booting the installer)

Order matters — do them in this order:

1. **Disable Secure Boot** — required by most distros (CachyOS lists it as an official prerequisite). ASUS ROG: Boot tab → Secure Boot → OS Type = **Other OS** (this is the actual toggle on ASUS boards, not a checkbox labeled "Secure Boot").
2. **Disable Windows Fast Startup** — Control Panel → Power Options → "Choose what the power buttons do" → uncheck "Turn on fast startup". Windows hibernates its kernel on shutdown otherwise, leaving NTFS "dirty" for Linux → filesystem corruption risk.
3. **Pause BitLocker / Device Encryption** — Settings → Privacy & Security → Device encryption → Pause. Laptops especially default to BitLocker on. Skipping this = recovery-key wall after resizing.
4. **Shrink C: from Windows** — `Win+R` → `diskmgmt.msc` → right-click C: → Shrink Volume → at least 30720 MB (30 GiB). Do this in Windows, not from the installer.

### The shrink wall: "I can only shrink 2 GB" (verified Aug 3, 2026)

Windows' built-in shrink can report a tiny max (e.g. 2 GiB) even when the disk
has plenty of free space. That's NOT the disk being full — it's **unmovable
files** parked at the end of the volume that Windows refuses to move:

1. **Hibernation file** (`hiberfil.sys`) — the #1 culprit, can be several GiB.
2. **Pagefile** (`pagefile.sys`) — unmovable while active.
3. **System Restore points / shadow copies** — unmovable.

Unblock in an **admin PowerShell**, in this order (fastest first):
```powershell
powercfg /h off    # deletes hiberfil.sys instantly — often the whole unlock
```
If still stuck: move the pagefile off C: (Settings → System → About →
Advanced system settings → Performance → Advanced → Virtual memory → set C: to
"No paging file" → Apply → reboot → shrink → put it back), and delete old
restore points (System Protection → Configure → Delete) before retrying.

**Escape hatch:** if the machine you wanted to dual-boot is a test-drive rig and
a second machine already has Linux on it, the shrink fight is often not worth
it — go all-in on the machine that's already partitioned and keep the gaming
rig untouched. Tyler chose this (laptop all-in over fighting the gaming PC's
NVMe) and it was the right call for an experiment.

## Install flow (GUI installer)

1. Boot the USB → launch installer
2. Language / region / timezone → **manual partitioning**
3. Create in the free space:
   - **EFI/boot**: FAT32, ≥2048 MiB (systemd-boot) or ≥4096 MiB (Limine), mount `/boot`, flag `boot`
   - **Root**: ≥20000 MiB, mount `/`, any filesystem (BTRFS defaults are fine)
4. Pick desktop, create user, Install Now

## Boot manager — adding Windows to the menu

### Choosing a boot manager (CachyOS installer offers 4)

| Option | Best for | Dual-boot Windows | Verdict |
|--------|----------|-------------------|---------|
| **Limine** | Modern, fast, Btrfs snapshots in boot menu | `limine-scan` one-liner | ✅ **Default pick** — most tested, reliable on UEFI |
| **GRUB** | Encrypted /boot, BIOS, widest FS support | os-prober setup needed | Good fallback |
| **rEFInd** | Polished graphical menu, auto-detects all OSes | Automatic | Nice, slightly less tested on CachyOS |
| **rEFInd + AI** | New experimental (CachyOS AI SDK) boot picker | New, least tested | Skip for a first install; can switch later |

For a **test drive**: Limine. It's CachyOS's default, handles Windows dual-boot cleanly with `limine-scan`, has Btrfs snapshot integration out of the box, and works reliably on UEFI. The "rEFInd + AI" option was just added (per CachyOS GUI installer changelog) — tempting but not what you want for a first install; boot managers can be swapped later.

### Limine (CachyOS default)
```bash
sudo limine-scan
# find the Windows EFI partition (FAT32/vfat, no Linux mountpoint):
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT
sudo mkdir /mnt/WinBoot && sudo mount /dev/<win-efi> /mnt/WinBoot
sudo cp -r /mnt/WinBoot/EFI/Microsoft/ /boot/EFI
sudo umount /mnt/WinBoot && sudo rmdir /mnt/WinBoot
```

### GRUB
```bash
sudo pacman -S os-prober
# set GRUB_DISABLE_OS_PROBER=false in /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

## NVIDIA GPUs

- CachyOS builds NVIDIA into the kernel (monolithic) — on some installs nothing
  to install. Verify: `nvidia-smi`
- **Intel CPU + NVIDIA discrete GPU (gaming desktop) — verified Aug 3, 2026:**
  the fresh CachyOS install did NOT have drivers out of the box, and the
  installer's package-selection screen had NO nvidia/recommended options (the
  package list bottomed out at desktop choices + printing). Install manually:
  ```bash
  sudo pacman -S nvidia-dkms nvidia-utils lib32-nvidia-utils   # lib32 REQUIRED for Steam/Proton
  sudo pacman -S cachyos-nvidia-conf                           # CachyOS's nvidia auto-config
  sudo pacman -S vulkan-intel intel-media-driver lib32-vulkan-intel  # Intel iGPU: video decode + Vulkan
  ```
  Then reboot and verify with `nvidia-smi` (shows GPU, driver, VRAM) and
  `glxinfo | grep renderer` (should show the NVIDIA card).
- If drivers don't work: `sudo chwd --list-installed` first, then `sudo chwd -a`
- **Hybrid Intel+NVIDIA laptops** may need `nvidia-prime` for GPU switching;
  pure discrete desktops don't.

## Pitfalls

- **"Install alongside" auto-mode FAILS on small Windows ESPs (verified Aug 3, 2026).** The CachyOS auto-shrink flow tries to reuse the Windows EFI partition for CachyOS's bootloader and errors out: *"The EFI system partition is too small (recommended 4096 MiB), please use manual partition."* Windows ESPs are typically 260 MiB — fine for GRUB/systemd-boot, NOT for Limine (needs a 4096 MiB /boot). **Fix: choose "Manual partitioning" and create a dedicated 4 GiB FAT32 /boot partition in the free space** (mount /boot, flag boot) plus a btrfs root. Leave every Windows partition (SYSTEM/MSR/OS/RECOVERY/RESTORE/MYASUS) untouched.
- **Resizing from the installer's "Install alongside" worked fine** — it shrank the NTFS OS partition (926 GiB → 834 GiB) and freed 91 GiB without issues. The earlier advice to always shrink from Windows is overly cautious; the installer CAN do it cleanly. (Fast Startup/BitLocker pre-flight still matters.)
- **User created without admin = sudo rejects every password (verified Aug 3, 2026).** The CachyOS installer has an easy-to-miss "make this user administrator" toggle (wheel group). If skipped, login works but `sudo` fails with the correct password. Fix from a live USB: `sudo mount /dev/<root-part> /mnt && sudo chroot /mnt usermod -aG wheel <username>`. Or try `su -` first — if root login works, the fix is one `usermod` without the USB.
- **CachyOS installer account screen — the admin checkbox is labeled differently (verified Aug 3, 2026).** The user-creation page has NO explicit "admin" checkbox; instead there's a **"use the same password for admin account"** toggle. If you CHECK that, the root password = your user password, which means after first boot `su -` + `usermod -aG wheel <user>` works in two commands from the terminal — no live-USB chroot needed. This is the intended fast path; the wheel-group membership still has to be added manually either way.
- **CachyOS package-selection screen: keep it lean (verified Aug 3, 2026).** The post-install package picker (CachyOS Hello) lists every DE + WM. Best practice for a gaming/test install: keep the checked defaults (CachyOS packages, base-devel, KDE-Plasma, Firefox) plus Printing-Support if you might print; skip all other desktops/WMs (installable later with one `pacman -S`), skip HP printer support unless you own an HP. One desktop is enough — extra DEs are GBs of cruft. No Nvidia/driver section exists on this screen; drivers are handled post-boot (see NVIDIA section above).
- **Windows Updates can eat the bootloader** — rare but real; fix with a live USB + reinstall bootloader (5 min)
- **Clock fight** — Linux uses UTC RTC, Windows uses local time. Fix on Linux: `timedatectl set-local-rtc 1`
- **Don't jump straight to dual-boot on the main rig** — test-drive on a laptop or VM first (Tyler's plan). VMs (VirtualBox/KVM) need no Secure Boot changes at all.
- **Anti-cheat games** (Valorant, Fortnite) require Secure Boot ON — if those matter on the same machine, prefer VM/live-USB testing instead of dual-boot.
- If you shrink from Windows and the installer can't see the free space, reboot Windows once so the partition table settles.

## References
- `references/cachyos-aug2026.md` — the specific research findings for CachyOS (sources, config details).

## Related
- `windows-maintenance` (devops) — Windows-side cleanup before partitioning
- `windows-ssh-tunnel-setup` (devops) — remote Windows access if needed during install
