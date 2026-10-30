---
name: mcp
description: >-
  Working with MCP (Model Context Protocol) servers in Freebuff Desktop:
  discovering tools via native search_mcp_tools / call_mcp_tool, bridging
  stdio servers via _scripts/mcp-call.py, injecting .env secrets via
  the root `.env` exporter, repairing broken servers, and building new MCP
  servers from scratch or OpenAPI specs.
---

# mcp — MCP tooling router

> Home branch in Memora: `root/skill/mcp`.
>
> Tool priority in Freebuff Desktop: (1) native `search_mcp_tools` + `call_mcp_tool`,
> (2) `python _scripts/mcp-call.py <server> <tool> '<json>'` when a stdio server is
> not yet mounted in the live session.

## Choosing a part

| Situation | Part |
|---|---|
| Discover and call MCP tools in the current session | `parts/mcp-usage/` |
| Batch install/repair servers, fix native bindings and env | `parts/mcp-batch-install-and-repair/` |
| Configure `.env` secrets via the root `.env` exporter | `parts/mcp-auth-handler/` |
| Diagnose tool-call failures, connection closed, moved paths | `parts/mcp-repair/` |
| Build a new MCP server from scratch or from an OpenAPI spec | `parts/mcp-builder/` |

## Rules

- Walk `root/skill/mcp` in Memora before changing server configs; record probe results as nodes.
- Use `ask_questions` before enabling/disabling servers in `~/.agents/mcp.json` or adding new third-party dependencies.
- Never inline plaintext tokens in `~/.agents/mcp.json` — place secrets in the root `.env` and wrap the server command with the root `.env` exporter.
- Pin package versions in `~/.agents/mcp.json` (no blind `@latest`). On-demand servers live in `_scripts/mcp-catalog-disabled.json`.
- If `read_files` returns `[BLOCKED]` on an ordinary non-secret file covered by `.gitignore` (such as `inbox/` or `_archive/`), read it via the terminal (`python` / `sed`); never bypass secret rules for `.env`.

## Related

`memory` (`memora` MCP), `research` (`searchmcp` and `parallel` MCPs), `browser` (`browsermcp` and `playwright` MCPs).
