---
name: ubuntu-zfs-mirror-install
description: Install Ubuntu Server onto a 2-disk ZFS mirror root (rpool→/) plus a striped data pool (dpool→/data) via debootstrap + ZFSBootMenu, or fall back to a plain single-disk ext4 install (GRUB-EFI) when there aren't two equal-size disks. Use when asked to install Ubuntu on ZFS, build a ZFS mirror root / rpool+dpool layout, set up root-on-ZFS with ZFSBootMenu, or do a scripted Ubuntu Server install on a UEFI x86 server with one or two SSDs/NVMes.
---

# Ubuntu ZFS-mirror (or ext4) Server Install

Validated end-to-end (proven on an 8-GPU ASUS ESC8000-E12P). Every fix that makes the ZFS path
boot **hands-free and reboot-safe** is baked into the scripts — see [REFERENCE.md](REFERENCE.md)
for what they are and how to recover if something's off.

## Decision rule (choose the path from the disks)

- **Exactly two fixed disks of the SAME size → ZFS mirror** (`scripts/install.sh`):
  per disk `ESP | rpool-member | dpool-member`; `rpool` mirror → `/`, `dpool` stripe → `/data` (no redundancy).
- **One disk, or two disks of different sizes → plain ext4 single-disk** (`scripts/install-ext4.sh`):
  `ESP | ext4 root`, GRUB-EFI. (`install.sh` refuses unequal/single disks and points here.)

## Prerequisites

- Target booted into an **Ubuntu Server LIVE** environment (24.04+/26.04), **UEFI** mode (CSM off).
- A **root shell** on it (local console, or SSH — enable `ssh` + set a password in the live env).
- **Internet** reachable from the live env (debootstrap + ZFSBootMenu download).
- Copy `scripts/` to the target (e.g. `scp -r scripts root@<live-ip>:`).

## Workflow

1. **List disks:** `sudo bash scripts/install.sh --list` — shows fixed disks with by-id paths + sizes; the live/USB medium is marked `[LIVE MEDIUM, do NOT pick]`.
2. **Gather settings from the user** (ask; defaults in parens):
   | Setting | Notes |
   |---|---|
   | disk(s) | by-id path(s); count+size decides ZFS vs ext4 |
   | rpool size *(ZFS only)* | **128 / 256 / 512 / 1024 GB** → `RPOOL_SIZE=+128G/+256G/+512G/+1T` (default `+1T`) |
   | admin username | default **`developer`** |
   | admin password | default **`passw0rd`** (root gets the same) |
   | SSH public key | optional; if set, admin is key-only (password auth off) |
   | hostname | default **`ubuntu`** |
   | timezone | optional (default `Etc/UTC`) |
3. **Run the matching installer** (type `ERASE` when prompted, or pass `--yes` once the user has confirmed):
   ```bash
   # ZFS mirror (two equal disks):
   DISK1=<by-id> DISK2=<by-id> RPOOL_SIZE=+1T ADMIN_USER=developer INSTALL_PASSWORD='...' \
     SSH_AUTHORIZED_KEY='ssh-ed25519 ...' HOSTNAME=ubuntu sudo -E bash scripts/install.sh
   # ext4 single disk:
   DISK1=<by-id> ADMIN_USER=developer INSTALL_PASSWORD='...' HOSTNAME=ubuntu sudo -E bash scripts/install-ext4.sh
   ```
   Takes ~10–20 min (debootstrap dominates). Over a flaky SSH link, run **detached** and tail the log:
   `… nohup bash scripts/install.sh --yes >/root/install.log 2>&1 & ` then `tail -f /root/install.log`.
4. **Reboot** — remove the install media (or set the target disk first in UEFI boot order). It should
   boot ZFSBootMenu → Ubuntu (or GRUB → Ubuntu) **hands-free**, with `/` and `/data` (ZFS) mounted.
5. **Validate:** `sudo bash scripts/validate.sh` — expect pools/`/data` ONLINE (ZFS) or `/` ext4, and
   `systemctl is-system-running` = `running`, 0 failed units.

## Safety

- **Destructive.** The installers refuse a disk that has mounted partitions (the live medium) and
  require typing `ERASE` (skip only with `--yes` after the user explicitly confirms the disks).
- Single-NVMe failure on the ZFS layout: `rpool` stays bootable (degraded), **`dpool`/`/data` is lost** (no redundancy by design).
- ZFS path has **no GRUB** — the kernel cmdline lives in the `org.zfsbootmenu:commandline` ZFS property
  (it's set to `quiet zfs_force=1`; keep `zfs_force=1` if you append e.g. `intel_iommu=on iommu=pt`).

See [REFERENCE.md](REFERENCE.md) for the baked-in fixes, recovery steps, and hardware notes (incl. ASUS ESC8000 BMC quirks).
