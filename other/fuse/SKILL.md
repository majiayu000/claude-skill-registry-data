---
name: fuse
description: Build, debug, and review Linux FUSE filesystems with the official libfuse userspace library. Use when implementing a FUSE filesystem, choosing between libfuse high-level vs low-level APIs, wiring callbacks, building with fuse3/pkg-config, mounting for local testing, or troubleshooting fusermount3 and permission issues.
---

# FUSE

Use the official `libfuse/libfuse` project as the baseline for Linux FUSE work.

## Quick Start

1. Confirm the task is Linux FUSE userspace work, not kernel module work.
2. Prefer the official `libfuse` interfaces and examples before suggesting wrappers.
3. Decide API style:
- Use the high-level API for simpler path-based filesystems.
- Use the low-level API for inode-level control, explicit replies, or advanced behavior.
4. Build with `pkg-config fuse3 --cflags --libs` unless the project already uses another build system.
5. For local runs, prefer foreground debug mode first: `-f -d`.

## Workflow

### 1. Choose the API

Use the high-level API when the user needs a straightforward filesystem and path callbacks are sufficient.
Read `include/fuse.h` semantics first.

Use the low-level API when the user needs inode handling, async-style explicit replies, or finer control over request lifetime.
Read `include/fuse_lowlevel.h` semantics first.

### 2. Start from official examples

Check the `example/` directory in `libfuse/libfuse` before drafting handlers from scratch.
For passthrough, mirror, hello-world, or minimal callback wiring, adapt an official example instead of inventing a new skeleton.

### 3. Build correctly

Use these defaults unless the project already defines them:

```bash
pkg-config fuse3 --cflags --libs
```

Typical manual build pattern:

```bash
gcc fs.c -o fs $(pkg-config fuse3 --cflags --libs)
```

If the project vendors `libfuse`, follow its existing Meson/Ninja setup instead of replacing the build flow.

### 4. Run and debug safely

Use a writable, non-sticky mountpoint owned by the current user.
Start in foreground debug mode first:

```bash
./fs -f -d <mountpoint>
```

If mounting fails, check:
- `fusermount3` availability
- `/etc/fuse.conf`
- `allow_other` vs `default_permissions`
- whether the mountpoint is writable by the mounting user

### 5. Troubleshoot by symptom

If callbacks are not firing, verify the mount succeeded and the process is still in foreground.
If permission behavior is surprising, inspect `default_permissions` and `allow_other`.
If the filesystem hangs, inspect whether a low-level handler failed to send a reply.
If performance is poor, check whether the design needs low-level API control, cache tuning, or fewer round trips.

## Read Next

Read `references/official-libfuse.md` when you need the official repo, docs, build flow, and the canonical places to look for examples and headers.
