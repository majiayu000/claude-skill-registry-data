---
name: littlefs-integration
description: Use when integrating, porting, configuring, or debugging littlefs on MCU flash, external NOR/NAND, SD-backed block devices, bare-metal, or RTOS projects
---

# littlefs Integration

## Overview

Use this skill to integrate littlefs safely on embedded block devices. The core task is to make the `lfs_config` match the real storage geometry and prove mount, format, write, sync, power-loss, and remount behavior.

## When To Use

Use this skill when:

- The user wants to add or debug littlefs on MCU internal flash, external SPI/QSPI NOR, NAND-like storage, EEPROM emulation, SD-backed block devices, or RTOS storage.
- The issue involves mount failures, `LFS_ERR_CORRUPT`, read/write errors, wear leveling, block geometry, formatting, or data loss after reboot.
- The project uses `lfs.h`, `lfs_file_*`, `lfs_dir_*`, or `struct lfs_config`.

Do not use this skill for generic flash programming failures before the block device driver works. Use `mcu-flashing-debug` first.

## First Questions

Ask for:

- Storage type, size, erase block size, program size, read size, and erase value.
- Whether storage is internal flash, external NOR/NAND, SD card, RAM disk, or simulator.
- Existing `lfs_config`, block device read/prog/erase/sync functions, and error codes.
- RTOS or bare-metal environment, locking needs, and whether dynamic allocation is allowed.
- Whether formatting is allowed. Formatting can destroy existing data.
- Current symptom and exact littlefs error code.

## Integration Checklist

1. Confirm block geometry.
   Set `read_size`, `prog_size`, `block_size`, `block_count`, `cache_size`, `lookahead_size`, and `block_cycles` from the real storage device, not guesses.

1. Validate block operations.
   `read`, `prog`, `erase`, and `sync` must use block-relative offsets correctly and return negative error codes on failure.

1. Respect flash rules.
   Programming can only change erased bits in the supported direction, writes must be aligned, and erase must cover whole erase blocks.

1. Decide mount policy.
   Try `lfs_mount` first. Only call `lfs_format` after explicit user approval or when the product policy allows first-boot formatting.

1. Add locking if needed.
   Protect littlefs calls with a mutex if multiple tasks, interrupt contexts, or shell commands can access the filesystem.

1. Prove persistence.
   Write a file, close/sync it, unmount if possible, reset, remount, and read back.

## Porting Checks

- `context` points to the storage driver state if needed.
- Block index and offset are translated to physical address correctly.
- Erase block size matches the physical erase granularity.
- Cache size is a multiple of read/prog sizes and fits RAM budget.
- Lookahead size is valid and large enough for block count.
- Bad-block behavior is understood if using NAND-like storage.
- Interrupts or power loss cannot interrupt a critical flash operation without product-level recovery handling.

## Common Failures

- Mount fails because `block_size` or `block_count` does not match the actual partition.
- Verify/readback fails because program alignment is wrong.
- Data disappears after reboot because file was not closed or synced.
- Filesystem corruption is caused by two tasks accessing littlefs without locking.
- Internal flash writes corrupt running code because the partition overlaps firmware.
- Formatting on every boot erases user data.

## Verification

Before claiming littlefs works:

- State the storage geometry and `lfs_config` values.
- Confirm mount behavior and whether format was skipped, approved, or performed.
- Confirm create/write/close/readback succeeds.
- Confirm data survives reset or remount.
- If RTOS is used, confirm the locking policy.
- List any destructive operations avoided or approved.

## Example

User:

```text
littlefs 挂载总是 LFS_ERR_CORRUPT。
```

Agent:

1. Asks for storage geometry, `lfs_config`, block driver functions, partition address, and whether format is allowed.
1. Checks block size/count and read/prog/erase alignment.
1. Mounts before formatting, and asks before erasing existing data.
1. Verifies write, sync, reboot, remount, and readback.
