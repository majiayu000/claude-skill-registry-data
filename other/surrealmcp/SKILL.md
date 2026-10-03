---
name: surrealmcp
description: "SurrealDB MCP for AI agents: built-in server (SurrealDB 3.1+ `surreal mcp`) and standalone surrealmcp (surrealdb/surrealmcp v0.4.0). Part of the surreal-skills collection."
license: MIT
metadata:
  version: "1.7.1"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-06-17"
  upstream:
    repo: "surrealdb/surrealmcp"
    release: "v0.4.0"
    builtin_since: "surrealdb v3.1.0"
---

# SurrealDB MCP for AI Agents

Two MCP surfaces exist as of SurrealDB 3.1:

| Surface | When to use |
|---|---|
| **Built-in** (`surreal mcp`, HTTP `/mcp`) | Local IDE hosts; simplest setup with the main `surreal` binary |
| **Standalone** (`surrealmcp start`) | Extended tool catalog, cloud helpers, multi-endpoint switching |

## Built-in MCP (SurrealDB 3.1+)

```bash
# stdio — typical MCP host config
surreal mcp --endpoint ws://127.0.0.1:8000/rpc --ns test --db test \
  --user root --pass root
```

**Security:** stdio MCP grants owner-level tool access with no login step. Do not
expose to untrusted hosts. HTTP `/mcp` requires normal SurrealDB authentication.

See [rules/surrealmcp.md](../../rules/surrealmcp.md) for env vars and tool hints.

## Standalone surrealmcp (v0.4.0)

Not published to crates.io or npm. Install from source or Docker:

```bash
git clone https://github.com/surrealdb/surrealmcp
cd surrealmcp && cargo install --path .

# Or Docker
docker run --rm -i --pull always surrealdb/surrealmcp:latest start \
  --endpoint ws://localhost:8000/rpc --ns test --db test
```

The `start` subcommand is mandatory. Full tool catalog and host wiring:
[rules/surrealmcp.md](../../rules/surrealmcp.md).
