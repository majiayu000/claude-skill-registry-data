---
name: context7
description: Search the Context7 library index and fetch high-quality, version-accurate documentation snippets.
---

# Context7 Documentation Search

This skill provides direct access to the Context7 library index, allowing you to quickly look up verified documentation and usage snippets for a wide variety of frameworks, libraries, and tools.

**Requires `CONTEXT7_API_KEY` to be set in your environment.**

## Available Tools

### `context7_search(query, limit?)`

Use this tool to find the exact ID of a library in the Context7 database.

*   **When to use:** When you need documentation for a library but you don't know its exact Context7 `libraryId`.
*   **Example:** `context7_search({ query: "react hooks" })`
*   **Returns:** A list of matching libraries, their IDs (e.g., `reactjs/react.dev`), descriptions, and trust scores.

### `context7_docs(libraryId, topic?, tokens?)`

Use this tool to actually read the documentation snippets for a specific library.

*   **When to use:** Once you know the `libraryId` from a previous search, use this to extract the relevant text.
*   **Parameters:**
    *   `libraryId`: The exact ID of the library (e.g., `tiangolo/fastapi`).
    *   `topic` (optional): Focus the returned snippets on a specific topic like `authentication`, `routing`, or `hooks`.
    *   `tokens` (optional): Max tokens to return (default 5000).
*   **Example:** `context7_docs({ libraryId: "reactjs/react.dev", topic: "useEffect" })`

## Workflow

1. Always run `context7_search` first if you are unsure of the exact library ID.
2. Review the search results and pick the most relevant library ID.
3. Run `context7_docs` using the chosen ID, optionally specifying a topic to narrow down the context.

## In Claude Code

Claude Code reaches Context7 through its MCP server (`claude mcp add -s user context7 -- npx -y @upstash/context7-mcp`). The tools have different names there:

| pi tool           | Claude Code MCP tool                |
| ----------------- | ----------------------------------- |
| `context7_search` | `mcp__context7__resolve-library-id` |
| `context7_docs`   | `mcp__context7__query-docs`         |

The workflow stays the same: resolve the library ID first, then query its docs. The MCP server works without `CONTEXT7_API_KEY` at a lower rate limit and reads the key from the environment when set.
