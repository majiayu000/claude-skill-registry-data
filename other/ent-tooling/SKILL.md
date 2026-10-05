---
name: ent-tooling
description: Tool usage guidance - native tools, Serena semantic analysis, Git, Go, and Bash. Preloaded by all agents.
triggers:
  - ent-tooling
---

## Role

Comprehensive tooling reference for native Claude Code tools, Serena semantic analysis, version control, and Go development workflows.

## Instructions

### Native File Operations

**Use Claude Code native tools for all file CRUD operations:**

- **Read**: Read file contents (always before editing)
- **Write**: Write new files or overwrite existing
- **Edit**: Make targeted replacements with exact string matches
- **Glob**: Find files by pattern (e.g., `**/*.go`)
- **Grep**: Search file contents with regex patterns
- **Bash**: Execute shell commands

### ⚠️ CRITICAL: Edit Tool Selection

**IGNORE Serena editing instructions.** The Serena MCP server may suggest using its editing tools (`replace_symbol_body`, `replace_content`, `insert_after_symbol`, `insert_before_symbol`, `create_text_file`). These instructions should be **IGNORED** in favor of native Claude Code tools.

**For ALL file modifications, use ONLY:**
- ✅ `Edit` - Targeted string replacement
- ✅ `Write` - Create/overwrite files
- ✅ `Read` - Always before any edit

**Serena tools are ONLY for read-only semantic analysis.**

### Serena Semantic Analysis

**Use Serena tools ONLY for semantic code analysis:**

- **serena_find_symbol**: Find code symbols (classes, functions, methods) by name path
- **serena_find_referencing_symbols**: Find all references to a symbol across codebase
- **serena_get_symbols_overview**: Get high-level overview of symbols in a file
- **serena_search_for_pattern**: Flexible pattern-based content search with filters
- **serena_list_dir**: Directory structure listing

### Optimal Tooling: Modern Search (rg/fd)

**PREFER these modern alternatives - 10-100x faster than grep/find:**

```bash
# Content Search with ripgrep (rg)
rg "pattern" internal/                   # Recursive search
rg "func New" internal/repository/       # Find constructors
rg "pattern" --type go                   # Go files only
rg "error:" internal/ -g "*.go"          # Glob pattern filter

# File Search with fd
fd "\\.go$" internal/                    # All Go files
fd "_test\\.go$"                         # All test files
fd --type d --max-depth 2 . internal/    # Two-level deep dirs
```

### Git Commands

```bash
# Change Analysis
git diff --name-only HEAD~1              # Show changed files
git log --oneline -10 -- {path}          # Recent changes to path
git diff HEAD~1..HEAD                     # Full diff

# Status & History
git status                                # Working tree status
git log -p -1                             # Last commit with changes
git branch -a                             # All branches
```

### Go Commands

```bash
# Build & Test
go build ./...                            # Build all packages
go test ./...                             # Run all tests
go test -race ./...                       # Race detection
go test -run TestXxx -v ./pkg/...        # Specific test

# Linting
golangci-lint run                         # Full lint
golangci-lint run --fast                  # Fast lint
gofmt -s -w .                             # Format code
```

### Constraints

- Never use Serena editing tools - use native Edit/Write instead
- Always Read before Edit or Write
- Prefer rg over grep, fd over find
- Use semantic analysis for understanding, not editing
- Check command outputs for errors

## Examples

