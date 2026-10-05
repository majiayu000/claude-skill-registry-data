---
name: ctxora-setup
description: Install and configure CTXORA Engine for a repository and connect it to Codex, Claude Code, Cursor, or a generic MCP client. Use when a user asks to set up CTXORA or add its MCP server to a coding agent.
---

# CTXORA Setup

Use the public npm launcher unless the user explicitly prefers a source installation:

```bash
npx ctxora setup --workspace <repository>
npx ctxora doctor --workspace <repository>
```

Ask which client to configure if it is not clear, then use one supported profile:

```bash
npx ctxora install --workspace <repository> --profile codex
npx ctxora install --workspace <repository> --profile claude-code
npx ctxora install --workspace <repository> --profile cursor
npx ctxora install --workspace <repository> --profile generic-mcp
```

Use `--dry-run` before modifying an existing client configuration. Report the config path and mutations returned by CTXORA. Do not edit unrelated client settings manually.

CTXORA requires Node.js 18 or newer and Python 3.10–3.13. The npm launcher creates a versioned local Python environment; do not replace it with a global pip installation unless requested.
