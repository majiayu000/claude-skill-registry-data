---
name: oe-mcp-bootstrap
description: Setup and verification for MCP tooling used in OpenEvent-AI (filesystem, Context7 docs, LSP/Pyright, Playwright). Use when onboarding a new developer/agent or when Codex/Claude cannot access LSP, browser automation, or docs.
---

# oe-mcp-bootstrap

## Codex CLI (recommended MCP set)

Add servers (examples; adjust versions as needed):

- Filesystem:
  - `codex mcp add filesystem --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @modelcontextprotocol/server-filesystem@2025.12.18 .`

- Context7 (docs):
  - `codex mcp add context7 --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @upstash/context7-mcp@1.0.33 --transport stdio`
  - Ensure `CONTEXT7_API_KEY` is set in your shell and allowed by `shell_environment_policy`.

- LSP (Pyright via LSP bridge):
  - Generate an LSP config JSON that points to your local repo path:
    - `python3 .codex/skills/oe-mcp-bootstrap/scripts/generate_lsp_config.py --out .codex/lsp.json --repo-root .` (or the same script under `.claude/skills/oe-mcp-bootstrap/`)
  - Add the server (example uses @axivo/mcp-lsp):
    - `codex mcp add lsp --env npm_config_cache=/tmp/codex-npm-cache --env LSP_FILE_PATH=/abs/path/to/lsp.json -- npx -y @axivo/mcp-lsp@1.0.5`

- Playwright (browser automation):
  - `codex mcp add playwright --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @playwright/mcp@0.0.53`

Verify:
- `codex mcp list --json`

## Claude Code

Use the equivalent Claude Code MCP configuration for:
- filesystem
- context7
- LSP bridge (Pyright)
- Playwright

Keep secrets out of the repo; use env vars (`CONTEXT7_API_KEY`, etc.).
