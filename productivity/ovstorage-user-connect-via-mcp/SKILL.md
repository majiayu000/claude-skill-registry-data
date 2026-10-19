---
name: ovstorage-user-connect-via-mcp
description: Use when connecting an agent client to ovstorage over MCP stdio and mapping common CLI workflows to MCP tools.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, mcp, agents]
tools: [Read]
compatibility: Requires an ovstorage-mcp binary, configured plugins, and an MCP-capable agent client.
---

# Connect Via MCP

**Goal:** Configure an agent client to spawn `ovstorage-mcp`, verify the
configured backends, then choose the MCP tool that matches the user's
storage task.

## Server configuration

Register `ovstorage-mcp` as an MCP stdio server. Pass the same config
and plugin environment you would use with the CLI:

```json
{
  "command": "ovstorage-mcp",
  "env": {
    "OVSTORAGE_CONFIG": "/path/to/ovstorage.toml",
    "OVSTORAGE_PLUGIN_DIR": "/path/to/plugins"
  }
}
```

`OVSTORAGE_CONFIG` follows CLI precedence. If you intentionally want a
programmatic/no-config session, set `OVSTORAGE_MCP_NO_CONFIG=1`.

## First call

Call `ovstorage_doctor` before object I/O:

```json
{
  "tool": "ovstorage_doctor",
  "arguments": {}
}
```

Confirm the desired backend kind is among the layers this stack declares,
and that the target address root is visible, before calling
read/write/list tools. A kind absent from `backend_kinds` is a kind this
stack's config never declared a layer for.

## MCP to CLI equivalence

| MCP tool | Closest CLI command | Notes |
|---|---|---|
| `ovstorage_doctor` | `ovstorage doctor --json` | Health/config summary for agents. |
| `ovstorage_capabilities` | `ovstorage list-backends` plus `ovstorage list-routes` | MCP reports one prefix. |
| `ovstorage_stat` | `ovstorage stat ADDRESS` | Object info. |
| `ovstorage_list` | `ovstorage list PREFIX` | Use `next_page_token` for pagination. |
| `ovstorage_read` | `ovstorage read ADDRESS` | Requires `max_bytes`; bytes are base64. |
| `ovstorage_materialize` | `ovstorage read ADDRESS -o FILE` | MCP returns a leased path, not a durable caller-owned copy. |
| `ovstorage_release` | none | Releases a materialize lease. |
| `ovstorage_write` | `ovstorage write ADDRESS` | Data is base64 in MCP. |
| `ovstorage_update_metadata` | `ovstorage update-metadata ADDRESS` | Same precondition model. |
| `ovstorage_create_directory` | `ovstorage create-directory ADDRESS` | Also CLI `mkdir`. |
| `ovstorage_copy` | `ovstorage cp SRC DEST` | Source/destination preconditions are explicit. |
| `ovstorage_move` | `ovstorage mv SRC DEST` | Also CLI `rename`. |
| `ovstorage_delete` | `ovstorage delete ADDRESS` | Also CLI `rm`. |
| `ovstorage_delete_directory` | `ovstorage delete-directory ADDRESS` | Recursive and dry-run are arguments. |
| `ovstorage_connections_list` | `ovstorage list-routes` | MCP exposes configured connections. |
| `ovstorage_address_roots_list` | `ovstorage list-routes` | MCP exposes visible address roots directly. |

## Unsupported gaps

MCP v0 does not expose diff, sync, `list-versions`,
`get-latest-version`, `check-access`, `watch-directory`, or cache/state
diagnostic commands such as `cache-status`, `cache-doctor`, and
`state-status`. Use the CLI for those workflows.

## See also

- [ovstorage-user-getting-started](../ovstorage-user-getting-started/SKILL.md) — reading the
  `ovstorage_doctor` response
- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — interpreting
  `ok: false` envelopes
- [`docs/public/agent/mcp-tools.md`](../../docs/public/agent/mcp-tools.md)
  — full MCP tool reference
