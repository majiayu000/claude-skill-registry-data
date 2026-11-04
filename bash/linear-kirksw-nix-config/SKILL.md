---
name: linear
description: Use Linear MCPorter CLI to find, read, create, and update issues, projects, cycles, documents, initiatives, releases, and comments.
---

# Linear

Run the generated `linear` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/linear/scripts/run.mjs" list-issues --help
node "$PI_CODING_AGENT_DIR/skills/linear/scripts/run.mjs" get-issue --id ENG-123
node "$PI_CODING_AGENT_DIR/skills/linear/scripts/run.mjs" search-documentation --help
```

Prefer exact issue identifiers, team, project, assignee, cycle, or a narrow query over broad listings.
Use command-specific `--help` only when a flag is unknown.
Treat save, create, delete, merge, resolve, submit, and attachment operations as mutations.
After confirmation of the exact action, set `MCP_WRITE_CONFIRMED=1` only for that runner process.
Do not use direct MCP tools or raw MCPorter calls for normal Linear work.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- linear`, then run `nix run .#sync-agents`.
