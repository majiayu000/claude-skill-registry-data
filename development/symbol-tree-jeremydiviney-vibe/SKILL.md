---
name: symbol-tree
description: "ALWAYS USE FIRST when exploring, searching, or researching this codebase. Use symbol_tree MCP tool before grep/glob/read. Provides instant architecture overview, function relationships, and call graphs without reading full implementations."
allowed-tools: Bash
---

# Symbol Tree Analysis

Analyze TypeScript codebases using the symbol-tree CLI
This is not optional. The symbol tree tool provides:
- Instant overview of file/module structure
- Function signatures and relationships
- Call graphs showing what calls what
- Type symbols (interfaces, types, enums) with dependency graphs
- All without reading hundreds of lines of implementation

This saves tokens and gives better context faster than file searches.

## How to Run

```bash
bun run scripts/symbol-tree-mcp/src/cli.ts [path] [options]
```

### Options

| Option | Description |
|--------|-------------|
| `[path]` | Directory to analyze (default: cwd) |
| `--file <file>` | Specific file to analyze |
| `--symbol <name>` | Symbol to search for (e.g., "step", "Runtime") |
| `--pattern <glob>` | File pattern (default: "**/*.{ts,tsx,js,jsx}") |
| `--depth <n>` | Limit call graph depth |
| `--text-limit <n>` | Max output chars (default: 50000) |
| `--exports-only` | Only show exported symbols |
| `--no-files` | Hide file paths/line numbers |
| `--group-by-file` | Group by file instead of symbol type |
| `--format <fmt>` | "adjacency" (default) or "tree" |
| `--src-dir <dir>` | Source dir filter (default: "src") |

## Examples

```bash
# Analyze runtime directory
bun run scripts/symbol-tree-mcp/src/cli.ts src/runtime

# Find a specific symbol
bun run scripts/symbol-tree-mcp/src/cli.ts --symbol step

# Analyze a specific file
bun run scripts/symbol-tree-mcp/src/cli.ts --file src/runtime/state.ts

# Exports only, tree format
bun run scripts/symbol-tree-mcp/src/cli.ts --exports-only --format tree

# Full project overview
bun run scripts/symbol-tree-mcp/src/cli.ts src --exports-only
```

## Correct Workflow

1. **FIRST**: Run symbol-tree to get overview
2. **THEN**: Use the output to identify relevant files/functions
3. **ONLY THEN**: Use Read/Grep/Glob for specific details if needed

## Output Format

Each symbol shows location as: `(file:startLine-endLine)`

**Output Sections:**
- `=== CLASSES ===` - Class definitions
- `=== INTERFACES ===` - Interface definitions
- `=== TYPES ===` - Type aliases
- `=== ENUMS ===` - Enum definitions
- `=== FUNCTIONS ===` - Function signatures
- `=== TYPE DEPENDENCIES ===` - Which types extend/use other types
- `=== DEPENDENCIES ===` - Function call graphs

**Using with Read tool:**
- `offset`: Use `startLine` to begin reading at the symbol
- `limit`: Use `endLine - startLine + 1` to read only the symbol's code
