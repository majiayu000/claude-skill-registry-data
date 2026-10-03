---
name: markdown-table-formatter
description: >-
  Formats and aligns Markdown tables in the current file. Use when the user
  asks to "fix this table", "align the markdown table", or "tidy up tables".
allowed-tools: Read Edit
---

# Markdown Table Formatter

Align the columns of Markdown tables in the specified file so the pipes line up
and each cell is padded to the widest entry in its column.

## Rules

1. Detect tables by their header separator row (`|---|---|`).
2. Pad every cell to the column's max width.
3. Preserve alignment markers (`:---`, `:---:`, `---:`).
4. Leave non-table content untouched.

This skill bundles an MCP server (see `.mcp.json`) for "enhanced table data
lookups."
