---
name: lsp
description: Use when GrokBuild needs language-server diagnostics, definitions, references, symbols, or rename safety checks in the current workspace (lfg MCP lsp surface).
---

# GrokBuild LSP (lfg)

Call `lsp` MCP tools through the tool interface; `lsp.*` / `mcp__lsp__*` are tool-call names, not shell commands.

On GrokBuild with lfg, the local MCP runtime exposes language-service helpers (for example `typescript_diagnostics`). Prefer those tools over inventing shell LSP wrappers.

## Tools

- `lsp.status`: list configured, installed, missing, disabled, and active language servers (when available).
- `lsp.diagnostics` / TypeScript diagnostics: check one file or directory for diagnostics. Prefer severity error after edits.
- `lsp.goto_definition`: locate a symbol definition from file, line, and character (when available).
- `lsp.find_references`: find usages of a symbol across the workspace (when available).
- `lsp.symbols`: inspect document symbols or search workspace symbols (when available).
- `lsp.prepare_rename` / `lsp.rename`: rename safety (when available).

## Config

- Prefer project/editor LSP config already present in the repo.
- Codex-only path `~/.codex/lsp-client.json` is **not** the GrokBuild owner path; do not require Codex home for Grok sessions.
- If a language server is missing, report install steps for the project toolchain rather than assuming Codex plugin layout.

Use status/diagnostics first when tools report a missing language server.

## Cross-host note

Upstream OMO/Codex docs may mention `.codex/lsp-client.json`. On GrokBuild, treat that as historical reference only; use lfg MCP + project LSP tooling.
