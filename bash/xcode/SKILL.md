---
name: xcode
description: Use the bounded Xcode MCPorter CLI to inspect, build, test, and diagnose the project open in Xcode.
---

# Xcode

Run Xcode MCP tools through the generated CLI and shared bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/home-mcp/scripts/run.mjs" xcode <command> [flags]
```

Xcode must be running with the target project or workspace open.
Use `<command> --help` only when a command's flags are unknown.
Prefer focused file, issue, build, or test queries over broad project dumps.
Do not invoke `xcrun mcpbridge` directly for normal Xcode work.

Treat commands that create, delete, move, update, or write project content as mutations.
Obtain confirmation for the exact mutation, then set `MCP_WRITE_CONFIRMED=1` only for that runner process.
Builds, tests, previews, and documentation searches do not require mutation confirmation unless they also change source or project configuration.
