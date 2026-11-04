---
name: home-mcp
description: Shared MCPorter runner, output-bounding, regeneration, and mutation controls for dedicated personal-tool skills.
---

# Home MCP infrastructure

Tool-named skills provide discovery and operational guidance for each generated MCPorter CLI.
Use this skill for shared runner behavior, wrapper refreshes, and mutation controls; do not use it as a generic tool router when a dedicated skill exists.

Invoke a generated wrapper through the bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/home-mcp/scripts/run.mjs" <server> <command> [flags]
```

Use `<command> --help` for one bundled command's schema rather than root help.
Do not print raw catalogs or unbounded results.

The runner bounds output and blocks commands that look mutating unless the user explicitly confirms the exact action.
After confirmation, set `MCP_WRITE_CONFIRMED=1` only for that runner process.

Refresh wrappers explicitly, never during Nix evaluation or profile synchronization:

```sh
nix run .#update-home-mcp-skills -- affine
nix run .#sync-agents
```
