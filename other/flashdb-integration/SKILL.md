---
name: flashdb-integration
description: Use when integrating, porting, configuring, or debugging FlashDB KVDB or TSDB on MCU flash, filesystems, RTOS, or bare-metal projects
---

# FlashDB Integration

## Overview

Use this skill to integrate FlashDB as an embedded key-value or time-series database. The agent should confirm storage mode, flash/file backend, sector geometry, erase policy, and data-retention requirements before formatting or deleting database sectors.

## When To Use

Use this skill when:

- The user wants to add FlashDB KVDB or TSDB for parameters, configuration, logs, events, or time-series records.
- The issue involves init failure, sector size, erase errors, lost keys, database full, migration, blob values, timestamps, or flash wear.
- The project mentions FlashDB, `fdb_kvdb`, `fdb_tsdb`, KVDB, TSDB, `fdb_cfg`, or `fdb_port`.

Do not use this skill for raw filesystem work without FlashDB. Use `littlefs-integration` or storage-specific skills instead.

## First Questions

Ask for:

- Database type: KVDB, TSDB, or both.
- Backend: raw flash, FAL partition, filesystem, or vendor storage layer.
- Sector size, partition size, erase value, write alignment, and flash driver status.
- RTOS or bare-metal environment and locking requirements.
- Whether existing database data must be preserved.
- Current error log, assert, return code, or database output.

## Integration Checklist

1. Confirm database purpose.
   Use KVDB for named settings and TSDB for append-style time records. Do not force both if one is enough.

1. Confirm storage backend.
   Identify whether FlashDB talks to raw flash, FAL, filesystem, or a custom port.

1. Match sector geometry.
   Sector size and partition boundaries must match the real erase granularity and FlashDB configuration.

1. Preserve data by default.
   Do not format, clean, or recreate the database unless the user approves data loss or confirms it is a first-boot path.

1. Add locking when shared.
   Protect database operations if multiple tasks, shell commands, logging callbacks, or ISRs can access it.

1. Verify both metadata and values.
   Read back keys or TSDB records after reboot, not only immediately after write.

## Porting Checks

- Flash read/write/erase operations return correct status.
- Write alignment and erased-state assumptions match the chip.
- Partition does not overlap firmware, bootloader, littlefs, logs, or calibration data.
- Default KV values and schema migration strategy are explicit.
- Blob size and RAM buffer requirements fit the target.
- TSDB timestamp source is monotonic enough for the product.
- Database full behavior is understood: rollover, cleanup, or failure.

## Common Failures

- Database init formats existing production data unexpectedly.
- KV values disappear because default table reinitializes them incorrectly.
- TSDB records have bad order because timestamp source is wrong.
- Database full is handled as a generic write failure.
- Flash sector size in config differs from real erase size.
- Concurrent shell/log/task access corrupts records without locking.

## Verification

Before claiming FlashDB works:

- State database type, backend, partition, sector size, and preservation policy.
- Confirm init result without unapproved formatting.
- Confirm write/read/delete or append/query behavior for the target use case.
- Confirm data survives reset or remount.
- Confirm full-database and migration behavior is defined or explicitly deferred.

## Example

User:

```text
想用 FlashDB 存设备参数，重启后有时候读不到。
```

Agent:

1. Asks for KVDB config, backend, sector size, flash driver, default table, and data preservation requirement.
1. Checks whether init path reformats or overwrites defaults.
1. Verifies set/get after reboot and confirms locking if shell or tasks can modify parameters.
