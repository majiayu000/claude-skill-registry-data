---
name: 1password
description: Use 1Password MCPorter CLI for authenticated environment, variable, and local env-file operations when the user explicitly requests 1Password access.
---

# 1Password

Run the generated `1password` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/1password/scripts/run.mjs" list-environments
node "$PI_CODING_AGENT_DIR/skills/1password/scripts/run.mjs" list-variables --help
```

Use command-specific `--help` before supplying unfamiliar flags.
Minimize secret exposure: return names and references unless the user explicitly needs a value, and never include secret values in summaries or logs.
Treat environment, variable, and env-file changes as mutations.
After confirmation of the exact action, set `MCP_WRITE_CONFIRMED=1` only for that runner process.
Use `authenticate` only when 1Password access is required and the desktop app is available.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- 1password`, then run `nix run .#sync-agents`.
