---
name: ovstorage-user-delete-safely
description: Use when removing objects safely, especially recursive directories or targets that need a dry-run first.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, delete, safety]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls and an already-configured backend route.
---

# Delete Safely

**Goal:** Remove objects without losing data you didn't mean to lose.

**When to use this:** Cleaning up after a job, removing stale state,
or implementing user-initiated delete. Especially when the target is
a directory or you're not 100% sure what's underneath it.

## Single-object delete

Removes one object. Low risk — there's exactly one thing to delete.

```json
{
  "tool": "ovstorage_delete",
  "arguments": {
    "address": "s3://my-bucket/temp/scratch.bin"
  }
}
```

Successful response:

```json
{"v": "0.1", "ok": true, "operation": "ovstorage_delete", "result": {"ok": true}}
```

## Directory delete: always dry-run first

Recursive directory deletes are dangerous. The tool **requires** an
explicit `dry_run` parameter. Always run with `dry_run: true` first
and review the plan.

### Step 1: dry-run

```json
{
  "tool": "ovstorage_delete_directory",
  "arguments": {
    "address": "s3://my-bucket/old-results/",
    "recursive": true,
    "dry_run": true
  }
}
```

Response shows what *would* be deleted:

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_delete_directory",
  "result": {
    "dry_run": true,
    "would_delete_count": 47,
    "would_delete_paths": [
      "s3://my-bucket/old-results/run-001/output.json",
      "s3://my-bucket/old-results/run-001/log.txt",
      "..."
    ]
  }
}
```

Read the count. Read enough of `would_delete_paths` to confirm the
shape matches your intent. **If anything surprises you, stop.**

### Step 2: execute

If the plan is right, repeat the call with `dry_run: false`:

```json
{
  "tool": "ovstorage_delete_directory",
  "arguments": {
    "address": "s3://my-bucket/old-results/",
    "recursive": true,
    "dry_run": false
  }
}
```

Response:

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_delete_directory",
  "result": {"dry_run": false, "deleted": true}
}
```

## Non-recursive directory delete

If you just want to remove an empty directory marker:

```json
{
  "tool": "ovstorage_delete_directory",
  "arguments": {
    "address": "s3://my-bucket/empty/",
    "recursive": false,
    "dry_run": false
  }
}
```

This fails with `DirectoryNotEmpty` if anything's underneath.

## What NOT to do

- **Don't skip the dry-run.** Even for "just a temp folder" — the dry-run is 100ms of work to catch a mistake that's hours of work to recover from.
- **Don't paginate past 100k entries.** The tool caps dry-run enumeration at 100,000 entries. If your prefix has more than that, you've targeted the wrong prefix or you need to delete in batches.
- **Don't pass `dry_run: false` to "skip the confirmation."** That's exactly what it does, and that's exactly the bug.

## When things go wrong

| `error.code` | Likely cause | What to do |
|---|---|---|
| `NotFound` | Address doesn't exist | Already gone — your work here is done |
| `DirectoryNotEmpty` | Non-recursive delete on a non-empty directory | Either drop the contents first, or use `recursive: true` (with dry-run!) |
| `PermissionDenied` | Credentials can't delete | Check `ovstorage_doctor` |
| `Unsupported` | Backend doesn't support delete | Rare — check `ovstorage_capabilities` for that prefix |
| `Internal` | Dry-run found >100k entries — a fixed cap on one call, not a passing shortage, so retrying hits it again | Target a narrower prefix and delete in batches |

## See also

- [ovstorage-user-list-and-paginate](../ovstorage-user-list-and-paginate/SKILL.md) — dry-run reuses list internally
- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — when errors surface mid-operation
