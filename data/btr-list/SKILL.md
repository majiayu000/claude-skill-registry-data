---
name: btr-list
description: Browse LOCAL BTR context tree (NOT ByteRover/brv). Use when the user asks "what contexts do we have", "show all domains", "list topics in auth", "list BTR contexts", "show BTR domains", "browse BTR", or wants to explore available knowledge.
allowed-tools: Read, Glob, Bash
---

# BTR List

## ⚠️ CRITICAL: BTR ≠ ByteRover

**This skill uses `btr` (local context tree), NOT `brv` (ByteRover CLI).**

| Command | Tool | Syntax |
|---------|------|--------|
| ✓ CORRECT | `btr` | `btr query "search term"` / `btr list` / `btr stats` |
| ✗ WRONG | `brv` | Different tool, different syntax, requires auth |

**PREFER MCP tools when available:**
- `mcp__btr__query_context` - For searching
- `mcp__btr__list_contexts` - For browsing
- `mcp__btr__get_stats` - For statistics

Only use Bash `btr` commands if MCP tools are unavailable.

Browse and visualize the context tree structure.

## Quick Start

```bash
# List all domains
btr list

# List topics in a specific domain
btr list <domain>

# Show full details
btr list --verbose
```

## Instructions

1. Run the appropriate list command based on user request
2. Present the tree structure in a readable format
3. Offer to drill down into specific domains
4. Suggest relevant queries based on what's available

## Output Format

```
BTR Context Tree
=======================
auth (3 topics)
  ├── jwt-validation
  ├── oauth-google
  └── session-management

api (2 topics)
  ├── rate-limiting
  └── error-responses

database (1 topic)
  └── connection-pooling

Total: 6 contexts across 3 domains
```

## Command Variations

### List All Domains

```bash
btr list
```

Shows all domains with topic counts.

### List Topics in a Domain

```bash
btr list auth
```

Shows all topics within the specified domain with their metadata.

### Verbose Listing

```bash
btr list --verbose
```

Shows full details including:
- Topic descriptions
- Tags
- Creation date
- Last accessed date
- Retrieval count

### JSON Output

```bash
btr list --format json
```

Outputs structured JSON for programmatic use.

## Example Workflows

### Explore Before Querying

1. List all domains to see what's available:
   ```bash
   btr list
   ```

2. Drill into a relevant domain:
   ```bash
   btr list auth
   ```

3. Query for specific content:
   ```bash
   btr query "JWT refresh token flow" --domain auth
   ```

### Audit Context Coverage

Use verbose listing to identify gaps:

```bash
btr list --verbose --format json | jq '.domains | map({name: .name, count: .topics | length})'
```

### Find Recently Added Contexts

```bash
btr list --sort created --limit 10
```

## Tips

- Use `btr list` regularly to stay aware of available context
- When a domain has many topics, use `--filter` to narrow down
- Combine with `btr stats` to see which contexts are most valuable
