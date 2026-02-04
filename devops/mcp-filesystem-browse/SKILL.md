---
name: mcp-filesystem-browse
description: Browse local workspace files via MCP filesystem tools (docker-fs).
---

## When to use
- You need to inspect local files/dirs and MCP filesystem tools are available.

## Procedure
1) Use the available filesystem MCP tools (look for names like `list_directory`, `read_file`, `search_files`).
2) Keep reads small: prefer directory listings + targeted file snippets.
3) If filesystem MCP tools are not available, fall back to `file_search` / `file_read`.


