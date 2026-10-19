---
name: ovstorage-user-write-safely
description: Use when writing a new object without clobbering or updating an existing object with optimistic concurrency.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, write, safety]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls and an already-configured backend route with write permission.
---

# Write Safely (No Clobbering)

**Goal:** Upload an object's bytes to a path. By default, fail
loudly if the destination already exists rather than silently
overwriting.

**When to use this:** You're writing something new and the destination
should not exist yet, OR you're updating an existing object and want
to verify it hasn't changed since you last looked.

## Recipe — new file, refuse to clobber

Pass `if_dest: { "kind": "fail" }` to refuse to overwrite. The call
fails with `AlreadyExists` if the address is taken.

```json
{
  "tool": "ovstorage_write",
  "arguments": {
    "address": "s3://my-bucket/output/report.json",
    "data_base64": "ewogICJyZXN1bHQiOiAib2sifQo=",
    "if_dest": { "kind": "fail" }
  }
}
```

## Recipe — update with optimistic concurrency

Pass `if_dest: { "kind": "match_etag", "etag": "<s>" }` with the etag
you read earlier. If another writer has changed the object since then,
the call fails with `PreconditionFailed` and you can decide whether to
merge or restart. Nothing was written — the destination is checked
before anything is committed.

```json
{
  "tool": "ovstorage_write",
  "arguments": {
    "address": "s3://my-bucket/state/counter.json",
    "data_base64": "eyJjIjogN30=",
    "if_dest": { "kind": "match_etag", "etag": "\"abc123\"" }
  }
}
```

## Recipe — intentional overwrite

The default behavior when `if_dest` is omitted is to overwrite. Pass
`if_dest: { "kind": "overwrite" }` explicitly to document intent.

```json
{
  "tool": "ovstorage_write",
  "arguments": {
    "address": "s3://my-bucket/cache/latest.json",
    "data_base64": "...",
    "if_dest": { "kind": "overwrite" }
  }
}
```

## What success looks like

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_write",
  "result": {
    "info": {
      "address": "s3://my-bucket/output/report.json",
      "size": 4231,
      "etag": "\"def456\"",
      "version": null
    }
  }
}
```

Save `info.etag` (and `info.version` if your backend has it) — you
need them for any later optimistic-concurrency write or `if_match`
read.

## Optional parameters

- **`user_metadata`** — map of `{key: value}` strings attached to the object. Treated as opaque by ovstorage; the backend persists what it can.
- **`message`** — an annotation associated with the write (used as a commit message by backends that version objects, e.g. Nucleus checkpoints).

## When things go wrong

| `error.code` | Likely cause | What to do |
|---|---|---|
| `AlreadyExists` | `if_dest: {"kind": "fail"}` and the destination exists | Pick a different address, or drop `if_dest` (or set `{"kind": "overwrite"}`) after confirming you really want to clobber |
| `PreconditionFailed` | `if_dest: {"kind": "match_etag", ...}` didn't match current identity; nothing was written | Re-read with `ovstorage_stat`, decide whether to merge, retry with the new etag |
| `ObjectModified` | The object moved *during* a call that had already started — a read whose bytes shifted, or a copy source replaced after staging | Retry the whole call; the new etag rides `Error.context` as `Identity { new_etag }` |
| `PermissionDenied` | Credentials can't write here | Check `ovstorage_doctor` connection state |
| `IntegrityFailure` | Bytes received didn't match a checksum (rare) | Retry the write |
| `Transient` | Backend hiccup | `retryable: true` — try again |
| `Unsupported` | Backend doesn't support etag-conditional writes | Drop `if_dest` (or use `{"kind": "overwrite"}`); you lose the concurrency guarantee. Check `ovstorage_capabilities` to verify in advance |

## See also

- [ovstorage-user-read-bytes](../ovstorage-user-read-bytes/SKILL.md) — read identity (`info.etag`) for `if_match`
- [ovstorage-user-delete-safely](../ovstorage-user-delete-safely/SKILL.md) — symmetric concern for removal
- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — error structure
