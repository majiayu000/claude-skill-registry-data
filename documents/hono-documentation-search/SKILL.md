---
name: Hono Documentation Search
description: Use the hono CLI to search and view Hono framework documentation.
allowed-tools: Bash(hono:*), Bash(jq:*), Bash(which hono), Task
---

# Hono

Use the `hono` CLI for efficient development. View all commands with `hono --help`.

## Instructions

Use `hono docs` and `hono search` commands to access Hono documentation and answer questions about the Hono framework.

- **`hono docs [path]`** - Browse Hono documentation
- **`hono search <query>`** - Search documentation

## Examples

### Search for topics

```bash
hono search middleware
hono search "getting started"
```

### View documentation

```bash
hono docs /docs/api/context
hono docs /docs/guides/middleware
```

### Pipelines

```bash
hono search "middleware" | jq '.results[0].path' | hono docs
hono search "routing" | jq '.results[0].path' | hono docs
```
