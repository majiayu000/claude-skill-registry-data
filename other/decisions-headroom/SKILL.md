---
name: decisions-headroom
description: Use when a DecisionsAI, Codex, Cursor, or Claude task contains unusually large logs, files, JSON, search results, or tool output that should be compressed locally without losing access to the original.
---

# DecisionsAI Headroom

Headroom is bundled with DecisionsAI and its standalone MCP is enabled by
default in DecisionsAI, Codex, and Cursor. The MCP keeps original content in a
local store and does not require the provider traffic proxy. Use it when large
context would otherwise crowd out the task instructions or implementation
state.

## Tools

- `headroom_compress`: compress a large text payload locally and return a hash.
- `headroom_retrieve`: recover the original by hash, optionally filtered by a query.
- `headroom_stats`: inspect compression and retrieval savings.

## DecisionsAI policy

1. Keep automatic provider traffic proxying disabled. DecisionsAI callback blocks,
   work packets, acceptance criteria, and user instructions must never be
   compressed implicitly.
2. Keep the standalone MCP registered and enabled. Its on-demand compression
   and retrieval use the MCP process's local store, with proxy access only as
   an optional fallback.
3. Compress large logs, generated JSON, search results, or repeated tool output
   on demand. Do not compress short instructions or small source files.
4. Preserve the returned hash in the active task or result packet when a later
   workflow step may need the original.
5. Retrieve the original before quoting exact wording, line numbers, API values,
   or security-sensitive evidence.
6. Treat compression as a context optimization, not verification. Tests and
   direct file inspection remain authoritative.

## Recovery

- If the Headroom MCP is unavailable, continue with normal local file reads and
  targeted searches. Do not block the task.
- If an original has expired from Headroom's local store, read the source file or
  rerun the producing command instead of guessing.
