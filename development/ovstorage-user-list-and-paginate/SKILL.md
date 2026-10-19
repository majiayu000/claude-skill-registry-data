---
name: ovstorage-user-list-and-paginate
description: Use when enumerating objects under a prefix without buffering the whole result set into memory.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, listing, pagination]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls and an already-configured backend route.
---

# List and Paginate

**Goal:** Enumerate the objects under a prefix without buffering the
whole list into memory.

**When to use this:** Anytime you need to walk objects — copying a
tree, building an index, finding the latest, summarizing a directory.

## Recipe

`ovstorage_list` returns one page. You drive pagination by passing
`next_page_token` from the prior response back as `page_token` on the
next call. Stop when `next_page_token` is absent (or null).

```json
{
  "tool": "ovstorage_list",
  "arguments": {
    "prefix": "s3://my-bucket/logs/",
    "recursive": false,
    "max_results": 200
  }
}
```

To traverse all children at any depth, pass `recursive: true`.

## What success looks like

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_list",
  "result": {
    "items": [
      {"kind": "Object", "address": "s3://my-bucket/logs/2026-05-14.json", "size": 4231, "etag": "..."},
      {"kind": "Directory", "address": "s3://my-bucket/logs/archive/", "size": null, "etag": null}
    ],
    "next_page_token": "AAEY...zM="
  }
}
```

To get the next page, call again with the same arguments plus
`page_token: "AAEY...zM="`. When the response has no
`next_page_token`, you've reached the end.

## Pagination loop

In Python (over MCP):

```python
items = []
page_token = None
while True:
    res = call_tool("ovstorage_list", {
        "prefix": "s3://my-bucket/logs/",
        "recursive": True,
        "max_results": 1000,
        "page_token": page_token,
    })
    items.extend(res["result"]["items"])
    page_token = res["result"].get("next_page_token")
    if page_token is None:
        break
```

**Always set `max_results`** even if it's a generous number (e.g.,
1000). Backends have their own upper bounds, but a missing
`max_results` makes performance characteristics hard to reason about.

## What NOT to do

- **Don't ignore `next_page_token`.** Doing so silently truncates the
  list to the first page — usually the worst kind of bug because the
  partial result looks valid.
- **Don't recursively list a prefix with millions of entries
  unbounded.** Cap the loop yourself or work in batches.

## When things go wrong

| `error.code` | Likely cause | What to do |
|---|---|---|
| `NotFound` | Prefix doesn't exist | Check that the prefix exists with `ovstorage_stat` |
| `PermissionDenied` | Credentials can't list this prefix | See `auth_state_kind` in `ovstorage_doctor` |
| `Unsupported` | Backend doesn't support recursive listing | Drop `recursive: true`, walk manually one level at a time |
| `Transient` | Backend hiccup | Retry the *same* page with the same `page_token` — pagination is idempotent |

## See also

- [ovstorage-user-getting-started](../ovstorage-user-getting-started/SKILL.md) — confirm what prefixes are addressable
- [ovstorage-user-read-bytes](../ovstorage-user-read-bytes/SKILL.md) — once you've found the address you want
- [ovstorage-user-delete-safely](../ovstorage-user-delete-safely/SKILL.md) — `delete-directory --dry-run` builds on list internally
