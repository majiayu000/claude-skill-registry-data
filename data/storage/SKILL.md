---
name: storage
description: |
  Storage management for Bazzite. Automounting drives (BTRFS/EXT4, Framework, SteamOS),
  BTRFS deduplication, rmlint disk trimming, and snapper snapshots. Use when users
  need to configure disk and partition management.
---

# Storage - Bazzite Storage Management

## Overview

Bazzite supports automatic mounting of drives, BTRFS features like deduplication and snapshots, and disk optimization with rmlint.

## Quick Reference

### Automounting

| Command | Description |
|---------|-------------|
| `ujust enable-automounting` | Enable BTRFS/EXT4 automount |
| `ujust disable-automounting` | Disable BTRFS/EXT4 automount |
| `ujust enable-framework-automount` | Enable Framework laptop automount |
| `ujust disable-framework-automount` | Disable Framework automount |
| `ujust enable-steamos-automount` | Enable SteamOS automount |
| `ujust disable-steamos-automount` | Disable SteamOS automount |
| `ujust enable-automount-all` | Enable all automounting |
| `ujust disable-automount-all` | Disable all automounting |

### BTRFS Features

| Command | Description |
|---------|-------------|
| `ujust enable-deduplication` | Enable BTRFS dedup for /var/home |
| `ujust enable-rmlint` | Enable/disable rmlint trim |
| `ujust config-snapshots` | Enable/disable snapper snapshots |

## Automounting

### Standard Automounting

```bash
# Enable automounting for BTRFS/EXT4 labeled partitions
ujust enable-automounting

# Disable
ujust disable-automounting
```

Mounts drives with recognized labels at:
- `/run/media/$USER/<label>`

### Framework Laptop

```bash
# Enable Framework-specific automounting
ujust enable-framework-automount

# Disable
ujust disable-framework-automount
```

Handles Framework expansion cards and storage modules.

### SteamOS Mounts

```bash
# Enable SteamOS-style automounting
ujust enable-steamos-automount

# Disable
ujust disable-steamos-automount
```

Compatibility with SteamOS mount paths.

### All Automounting

```bash
# Enable everything
ujust enable-automount-all

# Disable everything
ujust disable-automount-all
```

## BTRFS Deduplication

### Enable Deduplication

```bash
# Enable BTRFS deduplication for /var/home
ujust enable-deduplication
```

**Benefits:**
- Saves space with duplicate files
- Runs in background
- Minimal performance impact

**Note:** Only for BTRFS partitions.

## Disk Trimming

### Enable rmlint

```bash
# Enable/disable rmlint trim feature
ujust enable-rmlint
```

rmlint finds and removes:
- Duplicate files
- Empty directories
- Broken symlinks
- Other disk clutter

## Snapshots

### Configure Snapper

```bash
# Enable/disable snapper snapshots for /var/home
ujust config-snapshots
```

**Snapper:**
- Creates automatic snapshots
- Allows rollback of /var/home
- Timeline-based retention

**Warning:** Snapshots use disk space.

## Common Workflows

### Add External Drive

```bash
# Enable automounting
ujust enable-automounting

# Plug in drive - mounts automatically
# Access at /run/media/$USER/<label>
```

### Space Optimization

```bash
# Enable deduplication
ujust enable-deduplication

# Enable rmlint for cleanup
ujust enable-rmlint
```

### Backup with Snapshots

```bash
# Enable snapshots
ujust config-snapshots

# View snapshots
snapper list

# Rollback
snapper rollback <number>
```

### Framework Setup

```bash
# Enable Framework automounting
ujust enable-framework-automount

# Expansion cards auto-mount when inserted
```

## Manual Mount Management

### Mount Manually

```bash
# Create mount point
sudo mkdir -p /mnt/data

# Mount
sudo mount /dev/sdb1 /mnt/data

# Mount BTRFS with options
sudo mount -o compress=zstd /dev/sdb1 /mnt/data
```

### Add to fstab

```bash
# Get UUID
lsblk -o NAME,UUID,FSTYPE

# Edit fstab
sudo nano /etc/fstab

# Add line:
# UUID=<uuid> /mnt/data btrfs defaults,compress=zstd 0 0
```

## Verification

### Check Mounts

```bash
# List mounts
mount | grep -E "/dev/sd|/dev/nvme"

# List block devices
lsblk

# Check BTRFS usage
btrfs filesystem usage /var/home
```

### Check Deduplication

```bash
# Check dedup status
btrfs filesystem df /var/home
```

### Check Snapshots

```bash
# List snapshots
snapper list

# Snapshot details
snapper status <number>
```

## Troubleshooting

### Drive Not Automounting

**Check label:**

```bash
lsblk -o NAME,LABEL,FSTYPE
```

**Check automount status:**

```bash
# Is automounting enabled?
gsettings get org.gnome.desktop.media-handling automount
```

**Manual mount to test:**

```bash
sudo mount /dev/sdb1 /mnt/test
```

### Deduplication Not Working

**Verify BTRFS:**

```bash
# Must be BTRFS
df -T /var/home | grep btrfs
```

**Check status:**

```bash
btrfs filesystem du -s /var/home
```

### Snapshots Filling Disk

**List and clean:**

```bash
# List snapshots
snapper list

# Delete old snapshots
snapper delete <number>

# Or disable entirely
ujust config-snapshots
```

## Cross-References

- **bazzite:system** - System cleanup
- **bazzite:security** - LUKS encryption
- **bazzite-ai:configure** - Docker/Podman storage

## When to Use This Skill

Use when the user asks about:
- "mount drive", "automount", "external drive"
- "Framework storage", "expansion card", "SteamOS mount"
- "BTRFS dedup", "deduplication", "save space"
- "disk trim", "rmlint", "cleanup duplicates"
- "snapshots", "snapper", "backup home", "rollback"
- "partition mount", "fstab", "mount on boot"
