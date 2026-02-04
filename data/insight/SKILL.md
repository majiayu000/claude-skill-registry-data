---
name: insight
description: "Understand code in one call. Structure, relationships, history - all at once."
allowed-tools: mcp__insight__insight, mcp__insight__suggest_refactoring
---

# insight

**One call to understand anything. No more 5+ tool calls to figure out what a file does.**

## First: insight

```
insight({ target: 'src/TaskRunner.ts' })
```

Returns everything you need:
- Structure (symbols, imports, exports)
- Relationships (callers, callees, dependencies)
- Recent changes (git history)
- Metrics and notes

## Why This Wins

| The Problem | Multiple Tools | insight Solution |
|-------------|----------------|------------------|
| Understand a file | list_symbols + get_imports + git_log + ... | One `insight` call |
| Understand a class | read_symbol + get_callers + find_references + ... | One `insight` call |
| Understand a module | Read each file + trace dependencies + ... | One `insight` call |

## What You Get

### For a File
- Language and summary
- All symbols with kinds and lines
- Imports and exports
- Who imports this file
- Recent git changes
- Complexity metrics
- Notes (warnings, suggestions)

### For a Directory
- Summary of the module
- Files and subdirectories
- Entry points (index files)
- Key exported symbols
- External and internal dependencies
- Recent changes across all files

### For a Symbol
- Kind, file, line
- Code (truncated for large symbols >50 lines)
- Function signature
- **Methods section for classes** (constructors and methods)
- What it calls (filtered - excludes noisy built-ins like push, map, slice)
- What calls it
- Related symbols in same file
- Recent changes

### Smart Handling
- **Ambiguous names**: Shows disambiguation when multiple symbols match
- **Better errors**: Suggests similar symbols when exact match not found
- **Large code**: Truncated with line count to prevent context overflow

## Examples

### Understand a file
```
insight({ target: 'src/server.ts' })
insight({ target: 'packages/syntax/src/tools/listSymbols.ts' })
```

### Understand a directory
```
insight({ target: 'src/utils' })
insight({ target: 'packages/task-runner' })
```

### Understand a symbol
```
insight({ target: 'TaskRunner' })
insight({ target: 'handleRequest' })
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| includeCode | true | Include source code in output |
| maxChanges | 5 | Max recent git commits to show |

## When to Use

- Starting work on unfamiliar code
- Before making changes (understand impact)
- Reviewing what a module does
- Getting oriented in a new codebase

---

## suggest_refactoring

**Find tech debt and improvement opportunities before you start working.**

```
suggest_refactoring({ target: 'src/api.ts' })
```

Returns prioritized suggestions:
- **High Priority** - Should fix now (long functions, high coupling)
- **Medium Priority** - Worth addressing (large files, many symbols)
- **Low Priority** - Nice to have (naming, minor cleanup)

### What It Detects

| Issue | Detection | Suggestion |
|-------|-----------|------------|
| Long functions (>50 lines) | Code analysis | Extract smaller functions |
| Large files (>500 lines) | Metrics | Split into modules |
| High coupling (>15 imports) | Import analysis | Reduce dependencies |
| Unused functions | Call graph | Remove dead code |
| Complex symbols (many callees) | Call analysis | Simplify |
| Poor naming | Pattern matching | Rename suggestions |

### Focus Your Analysis

```
suggest_refactoring({ target: 'src/', focus: 'coupling' })
suggest_refactoring({ target: 'src/', focus: 'complexity' })
suggest_refactoring({ target: 'src/', focus: 'unused' })
```

Focus options: `all`, `complexity`, `coupling`, `unused`, `tests`, `naming`

### When to Use suggest_refactoring

- **Before major changes** - understand existing tech debt
- **Code review** - get automated quality feedback
- **Planning refactoring** - prioritize what to fix
- **Learning a codebase** - find the problem areas

## Derived, Not Stored

Everything is computed fresh from current code. Never stale.
