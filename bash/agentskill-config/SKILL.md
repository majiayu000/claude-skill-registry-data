---
name: agentskill-config
description: "Stores and retrieves per-user, per-project preferences for AI skills via a unified JSON-backed CLI. Loaded by consumer skills that declare a '## Skill Config' section with keys to persist across invocations."
---

# agentskill-config

## Storage

Two-layer JSON files with per-key override priority: `project` overrides `global`; within the same layer, `<skill-name>` overrides `_shared`.

| Scope     | Path                                       |
| --------- | ------------------------------------------ |
| `global`  | `~/.agents/skill_config.json`              |
| `project` | `<project-root>/.agents/skill_config.json` |

`<project-root>` is resolved via `git rev-parse --show-toplevel`. The `project` layer path should be gitignored — personal preferences are not for team version control.

`_shared` is a reserved top-level key used when multiple skills share the same conceptual preference. Read applies a 4-layer automatic fallback:

```
1. project.<skill-name>.<key>
2. project._shared.<key>
3. global.<skill-name>.<key>
4. global._shared.<key>
```

The first non-null value is used.

---

## CLI

> `<skill>` = the agentskill-config directory (resolved from the load path by the agent); `<X>` = consumer skill name (e.g. `git-open-pr`) or `_shared`.

```bash
SC=<skill>/scripts/agentskill-config.js

# Read (auto-fallback; outputs empty string and exits 0 if not found)
value=$(node "$SC" read <X> <key>)

# Write (writes to the corresponding file by scope; mkdir -p automatically; idempotent merge)
# When writing to _shared, the CLI prints an impact-scope warning to stderr — agent should confirm with user before proceeding
node "$SC" write <X> <key> "<value>" --scope <global|project>

# List
node "$SC" list <X>            # list a specific skill / _shared
node "$SC" list                # list all

# Clean (SHOULD --dry-run first to preview)
node "$SC" clean <X> [--scope <global|project>] [--dry-run]
```

For full flag details, stdout format, and exit codes, see `references/api.md`.
