---
name: mcp-toolbox
description: Use when working with or extending the local Codex MCP toolset/server that exposes HTTP endpoints for shell, filesystem, git, and Excel operations, or when a task should be executed by calling those MCP endpoints instead of local tools, especially if the MCP server is running.
---

# MCP Toolbox

Prefer MCP endpoints when they can satisfy the request and the server is reachable.

## Quick start

- Ask whether the MCP server is running if it is not already clear.
- If uncertain, do a lightweight reachability check (for example, a /shell/exec call with a harmless command) before assuming the server is unavailable.
- Use endpoint details and payload shapes from references/toolbox.md.

## Guided workflow

- Confirm the server base URL and whether it is running.
- Call /health to verify reachability; if it fails, fall back to local tools or ask to start the server.
- Use /tools/list or /openapi.json to discover tool schemas for auto-invocation.
- Use the smallest endpoint that satisfies the request; avoid local shell when /shell/exec can do it.
- Keep file paths within MCP_ALLOWED_BASE; ask for a relative path if unsure.
- Follow inspect -> read_range -> preview_write -> commit_write for Excel edits.
- Show /git/status or /git/diff before /git/commit and remind that commit stages all changes.

## Using the endpoints

- Route shell commands through /shell/exec instead of local execution when the server is live.
- Use /fs/read and /fs/write for file operations; respect the allowed base directory enforced by the server.
- Use /git/status and /git/diff before /git/commit; note that /git/commit stages all changes.
- For Excel edits, always call /excel/preview_write before /excel/commit_write to validate changes.

## Maintaining or extending the server

- Edit the tool modules in server/tools/ and wire them into server/mcp_server.py.
- Keep path resolution and safety checks aligned with server/config.py (ALLOWED_BASE_DIR and MAX_READ_BYTES).
- Update README.md if endpoints, behavior, or setup steps change.
- When adding dependencies, update server/requirements.txt.
