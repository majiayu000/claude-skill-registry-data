---
name: ovstorage-user-materialize
description: Use when an object is large, needs random access, or must be handed to a tool as a stable local path.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, materialize, files]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls and a writable local cache/materialization path.
---

# Materialize for Direct File Access

**Goal:** Get a stable on-disk path for an object so you can mmap it,
seek through it, hand it to a subprocess that takes a path, or read
it many times without re-downloading.

**When to use this:** The object is large, you need random access, or
a tool you're driving (`ffmpeg`, `usdcat`, ML data loaders) wants a
filesystem path rather than a byte stream. Also when you'll read the
same object multiple times — materialize fetches once, pins, reuses.

For one-shot byte reads of small objects, use
[ovstorage-user-read-bytes](../ovstorage-user-read-bytes/SKILL.md) instead.

## Recipe

```json
{
  "tool": "ovstorage_materialize",
  "arguments": {
    "address": "s3://my-bucket/datasets/imagenet.bin",
    "ttl_seconds": 3600
  }
}
```

`ttl_seconds` is optional (default 1800 = 30 min). Pick a value that
covers your work window with margin. **No hard upper bound** — if your
training step takes 4 hours, use `ttl_seconds: 14400`.

## What success looks like

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_materialize",
  "result": {
    "path": "/var/cache/ovstorage/cas/ab/abcdef1234.bin",
    "info": {
      "address": "s3://my-bucket/datasets/imagenet.bin",
      "size": 4294967296,
      "etag": "\"abc123\""
    },
    "expires_at_unix_seconds": 1718003600
  }
}
```

Use the `path` directly. The file is pinned against eviction until
you release it or `expires_at_unix_seconds` is reached, whichever
comes first.

## Lifecycle

**Working window — do your work using `path`.**
The file stays on disk and won't be evicted.

**Refresh — extend the TTL.**
Call `ovstorage_materialize` again with the same address. The
server resets the timer to a fresh window and returns the same
`path` with a later `expires_at_unix_seconds`.

**Release — when you're done.**

```json
{
  "tool": "ovstorage_release",
  "arguments": {
    "path": "/var/cache/ovstorage/cas/ab/abcdef1234.bin"
  }
}
```

Response:

```json
{
  "v": "0.1",
  "ok": true,
  "result": {"released": true, "was_active": true}
}
```

`was_active: false` means the lease wasn't held (already released, or
the TTL expired before you got to it). Release is **idempotent** —
calling it twice or on a never-materialized path is harmless.

## Don't bother tracking handles

The `path` you got back **is** the handle. You don't need to store an
opaque lease ID; just remember the path. Other ovstorage tools that
take a `path` (release) and the file itself both use the same string.

## When things go wrong

| `error.code` | Likely cause | What to do |
|---|---|---|
| `NotFound` | Address doesn't exist | Confirm with `ovstorage_stat` |
| `NotConfigured` | No cache configured for this non-local backend | Local-file addresses materialize without a cache; remote backends need a cache configured on the host. See `next_action`. |
| `Unsupported` | The composed Stack does not provide materialization for this request | Use `ovstorage_read` with `max_bytes`, or configure a redirect follower on the host, optionally with a cache above it. A cache alone serves only what it already holds. |
| `InvalidArgument` | `ttl_seconds: 0` | Pass a positive number, or omit for the 1800s default |
| `Transient` | Backend hiccup during fetch | `retryable: true` |

## What NOT to do

- **Don't keep the path past `expires_at_unix_seconds` without refreshing.** The file may be evicted out from under you. Either refresh proactively or release explicitly when done.
- **Don't release a path you might still need.** Releasing tells the cache "I'm done with this." If you turn around and read it again, the next access may have to re-fetch.
- **Don't pass an arbitrary disk path to release.** Only the paths returned by `ovstorage_materialize` are valid; releasing other paths returns `was_active: false` but does nothing useful.

## See also

- [ovstorage-user-read-bytes](../ovstorage-user-read-bytes/SKILL.md) — alternative for small one-shot reads
- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — error structure
- [`docs/public/agent/mcp-tools.md`](../../docs/public/agent/mcp-tools.md) — full materialize/release reference
