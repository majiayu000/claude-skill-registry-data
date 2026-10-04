---
name: fatfs-integration
description: Use when integrating, porting, configuring, or debugging FatFs FAT/exFAT filesystems, diskio drivers, SD cards, SPI flash disks, or embedded file I/O failures
---

# FatFs Integration

## Overview

Use this skill to integrate FatFs by proving the disk I/O layer before trusting filesystem behavior. FatFs is portable C, but the target-specific `diskio` functions, sector geometry, mount policy, and media timing decide whether it works reliably.

## When To Use

Use this skill when:

- The user wants to add or debug FatFs on SD card, eMMC, USB MSC, RAM disk, SPI flash, or block devices.
- The issue involves `f_mount`, `f_open`, `f_read`, `f_write`, `FR_DISK_ERR`, `FR_NOT_READY`, `FR_NO_FILESYSTEM`, long filenames, Unicode, or exFAT.
- The project uses `ff.c`, `ffconf.h`, `diskio.c`, or `FATFS`.

Do not use this skill when the raw block device cannot read/write sectors yet; debug the storage driver first.

## First Questions

Ask for:

- Media type and transport: SDIO, SPI SD, eMMC, USB MSC, RAM disk, or flash translation layer.
- Sector size, sector count, erase/block size, and whether writes are cached.
- `ffconf.h`, `diskio.c`, and current FatFs return code.
- RTOS or bare-metal runtime and whether reentrancy is enabled.
- Whether formatting is allowed. Formatting can destroy user data.
- Long filename, Unicode, exFAT, timestamp, and multi-volume requirements.

## Integration Checklist

1. Prove disk I/O.
   `disk_initialize`, `disk_status`, `disk_read`, `disk_write`, and `disk_ioctl` must work independently.

1. Match sector geometry.
   FatFs expects logical sectors and correct sector count. `GET_SECTOR_COUNT`, `GET_SECTOR_SIZE`, and `CTRL_SYNC` matter.

1. Mount before formatting.
   Try `f_mount` first. Ask before `f_mkfs` or any operation that can erase media.

1. Configure `ffconf.h` intentionally.
   Reentrancy, LFN buffers, exFAT, code page, relative paths, and timestamp support affect RAM and behavior.

1. Add locking if shared.
   Enable and implement synchronization when multiple tasks can access the same volume.

1. Verify persistence.
   Write, `f_sync`/`f_close`, unmount/reset, remount, and read back.

## Common Failures

- `FR_DISK_ERR` from incomplete `disk_ioctl` or bad `CTRL_SYNC`.
- `FR_NO_FILESYSTEM` from wrong sector offset or unformatted media.
- Data loss because files are not closed or synced before power loss.
- LFN stack/heap buffers exceed MCU memory.
- SD card init works at low speed but data transfer fails after clock switch.
- Multi-task access corrupts files without FatFs reentrancy support.

## Verification

Before claiming FatFs works:

- State media, sector size/count, `ffconf.h` options, and mount path.
- Confirm disk read/write/ioctl tests.
- Confirm mount behavior and whether format was skipped, approved, or performed.
- Confirm create/write/sync/readback after reset or remount.
- Confirm locking policy when RTOS is used.

## Example

User:

```text
FatFs f_mount 返回 FR_NO_FILESYSTEM。
```

Agent:

1. Asks for media type, sector offset, diskio implementation, and whether formatting is allowed.
1. Tests raw sector read and `GET_SECTOR_COUNT`.
1. Mounts before formatting and asks before `f_mkfs`.
