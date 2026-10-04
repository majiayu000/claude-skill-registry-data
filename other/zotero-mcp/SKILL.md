---
name: zotero-mcp
description: "Use when Codex needs to connect to a user's Zotero library through 54yyyu/zotero-mcp or a compatible Zotero MCP server: installing or updating the local isolated runtime, generating Codex MCP configuration, checking Zotero local API readiness, searching Zotero items, reading metadata/full text/annotations/notes, using zotero-cli, or safely planning Zotero Web API / semantic-search setup without exposing secrets."
---

# Zotero MCP

## Core Boundary

Use this skill for Zotero library access through MCP, not for public paper search. Prefer `paper-review-source-intel` or web search for papers that are not already in the user's Zotero library.

Keep secrets and private library content out of Git and chat:

- Do not print, store, or commit `ZOTERO_API_KEY`, WebDAV passwords, OAuth tokens, cookies, or private Zotero exports.
- Do not write raw library dumps, full PDFs, annotations, or notes into tracked files unless the user explicitly asks and the target is appropriate.
- Treat Zotero write tools as library-modifying operations. Ask for explicit user confirmation before creating, updating, tagging, merging, or deleting Zotero items.

## Local Runtime

This machine uses a Git-ignored runtime outside the skill bundle:

```text
%LOCALAPPDATA%\Codex\zotero-mcp
```

The helper script manages:

- upstream clone: `%LOCALAPPDATA%\Codex\zotero-mcp\source\54yyyu-zotero-mcp`
- isolated venv: `%LOCALAPPDATA%\Codex\zotero-mcp\.venv`
- console commands: `zotero-mcp.exe` and `zotero-cli.exe`

Use the helper first for setup and diagnostics:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\zotero-mcp\scripts\zotero_mcp_local.ps1 status
powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\zotero-mcp\scripts\zotero_mcp_local.ps1 install
powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\zotero-mcp\scripts\zotero_mcp_local.ps1 smoke
powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\zotero-mcp\scripts\zotero_mcp_local.ps1 mcp-config
```

Read `references/local-setup.md` before changing the runtime or Codex MCP config. Read `references/upstream-provenance.md` when updating upstream version, license, or commit records.

## Codex MCP Configuration

For local read mode, the MCP server can run without a Zotero API key if Zotero Desktop is running and its local API is enabled.

The expected Codex config shape is:

```toml
[mcp_servers.zotero]
command = 'C:\Users\Administrator\AppData\Local\Codex\zotero-mcp\.venv\Scripts\zotero-mcp.exe'
args = ['serve']

[mcp_servers.zotero.env]
PYTHONIOENCODING = 'utf-8'
PYTHONUTF8 = '1'
ZOTERO_LOCAL = 'true'
```

After editing `C:\Users\Administrator\.codex\config.toml`, restart Codex. MCP servers usually are not hot-loaded into an already-running session.

For write operations or Web API mode, do not add secrets to tracked docs. Put credentials only in private environment variables or local untracked config:

```text
ZOTERO_API_KEY
ZOTERO_LIBRARY_ID
ZOTERO_LIBRARY_TYPE
```

## Zotero Desktop Readiness

Before expecting real library results:

1. Start Zotero Desktop.
2. Enable the local API in Zotero settings: Advanced -> allow other applications on this computer to communicate with Zotero.
3. Run the helper smoke check. If it reports local API unavailable, MCP may start but library calls can fail.

## Tool Routing

When the `zotero` MCP server is exposed in a future session, use MCP tools for library search and retrieval. Common tool names from 54yyyu/zotero-mcp include:

- `zotero_search_items`
- `zotero_advanced_search`
- `zotero_semantic_search`
- `zotero_get_item_metadata`
- `zotero_get_item_fulltext`
- `zotero_get_annotations`
- `zotero_get_notes`
- `zotero_search_notes`

If MCP is not loaded in the current session but the runtime exists, use `zotero-cli` for small local checks:

```powershell
& "$env:LOCALAPPDATA\Codex\zotero-mcp\.venv\Scripts\zotero-cli.exe" search "query" --limit 5
& "$env:LOCALAPPDATA\Codex\zotero-mcp\.venv\Scripts\zotero-cli.exe" get metadata ITEMKEY
```

Read `references/tool-routing.md` for search strategy and write-operation cautions.

## Validation

For this wrapper skill, validate with:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\zotero-mcp
```

For runtime smoke:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.codex\skills\zotero-mcp\scripts\zotero_mcp_local.ps1 smoke
```
