---
name: ovstorage-user-read-bytes
description: Use when loading one bounded object into memory to parse, inspect, hash, or hand its bytes to another tool.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, read, bytes]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls and an already-configured backend route.
---

# Read Bytes Safely

**Goal:** Load an object's contents into memory with a bounded size.

**When to use this:** You need the bytes of one object — to parse it,
inspect it, hash it, or hand it to another tool. The object fits in
memory.

For larger objects (multi-GB, or unknown size), use
[ovstorage-user-materialize](../ovstorage-user-materialize/SKILL.md) to get a stable on-disk path
instead — that lets you stream / mmap without buffering everything.

## Recipe

`max_bytes` is **required**. Pick a cap large enough for the work but
small enough to fail fast on accidental giants.

```json
{
  "tool": "ovstorage_read",
  "arguments": {
    "address": "s3://my-bucket/data/report.json",
    "max_bytes": 1048576
  }
}
```

## What success looks like

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_read",
  "result": {
    "data_base64": "ewogICJyZW...",
    "info": {
      "address": "s3://my-bucket/data/report.json",
      "size": 4231,
      "etag": "\"abc123\"",
      "version": null,
      "mtime_unix_nanos": 1718000000000000000
    }
  }
}
```

`data_base64` is the object's bytes, base64-encoded (MCP results
are JSON-shaped; binary data must be encoded). Decode in whatever
language you're using.

## Optional parameters

- **`if_match`** — precondition. Pass the bare etag string (e.g. `"abc123"`) from a prior `stat` to atomically verify the object hasn't changed. Mismatch surfaces as `ObjectModified`.
- **`range_start` + `range_end`** — byte-range read (both inclusive). Useful when you only need a slice (e.g., the header of a large file).

## When things go wrong

| `error.code` | Likely cause | What to do |
|---|---|---|
| `NotFound` | Address doesn't exist | Confirm spelling; check `ovstorage_list` of the parent prefix |
| `ResourceExhausted` | Object is larger than `max_bytes` | Either raise `max_bytes`, narrow with `range_start`/`range_end`, or switch to [ovstorage-user-materialize](../ovstorage-user-materialize/SKILL.md) |
| `PermissionDenied` | Credentials can't read this object | Check `ovstorage_doctor` — connection's `auth_state_kind` |
| `NoRoute` | No backend serves this address and no anonymous fallback is granted for its scheme | See [ovstorage-user-getting-started](../ovstorage-user-getting-started/SKILL.md) |
| `ObjectModified` | `if_match` didn't match | Re-stat to get current identity, then decide whether to retry |
| `Transient` | Backend hiccup | `retryable: true` — retry once or twice with backoff |

## See also

- [ovstorage-user-list-and-paginate](../ovstorage-user-list-and-paginate/SKILL.md) — find the address first
- [ovstorage-user-materialize](../ovstorage-user-materialize/SKILL.md) — for large or unknown-size objects
- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — full envelope error shape
