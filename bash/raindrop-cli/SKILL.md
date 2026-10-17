---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: raindrop-cli
repo: remorses/raindrop-cli
description: >
  raindrop-cli is a terminal interface for Raindrop.io bookmarks.
  It wraps the official Raindrop MCP server so you can search, save,
  update, and organize bookmarks, collections, tags, and highlights.
  ALWAYS load this skill when the user mentions raindrop-cli, rdrop,
  Raindrop.io, runs the `rdrop` binary, or asks to list or save bookmarks
  from the terminal. Load it before writing any command that touches Raindrop.
---

# raindrop-cli

Every time you use raindrop-cli, you MUST run:

```bash
rdrop --help # NEVER pipe to head/tail, read the full output
```

For a specific tool: `rdrop <command> --help`
