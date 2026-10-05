---
name: xhr-general
description: Handle any other xHR platform request not covered by a more specific xhr-* skill, including cross-domain workflows that span multiple xHR modules and platform language settings, by browsing the full xHR skill catalog from the root index.
---

# xHR General

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/SKILL.md`.
2. Follow only child entrypoints declared by that index.
3. Call that same MCP server's `read` tool for the single leaf that best matches the request.
4. Follow the complete leaf instructions and collect all required arguments.
5. Call that same MCP server's `exec` tool only for a script explicitly declared by the leaf.
6. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation to open the private xHR authentication window. After confirmation, call `authenticate` with no arguments, then retry the original `exec` once when authentication succeeds.
7. Never ask for or accept an access token in chat or MCP tool arguments.
8. Never guess a script path, operation, identifier, or argument.
9. Obtain explicit confirmation before an action that changes xHR data.
