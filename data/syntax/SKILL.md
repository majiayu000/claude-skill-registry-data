---
name: syntax
description: "Edits that never fail. Find functions by name, not text matching."
allowed-tools: mcp__syntax__list_symbols, mcp__syntax__read_symbol, mcp__syntax__edit_symbol, mcp__syntax__edit_lines, mcp__syntax__get_imports, mcp__syntax__get_exports, mcp__syntax__add_import, mcp__syntax__remove_unused_imports, mcp__syntax__organize_imports, mcp__syntax__search_symbols, mcp__syntax__find_references, mcp__syntax__rename_symbol, mcp__syntax__get_callers, mcp__syntax__get_callees, mcp__syntax__analyze_deps, mcp__syntax__move_file, mcp__syntax__move_symbol, mcp__syntax__extract_function, mcp__syntax__inline_function, mcp__syntax__find_unused_exports, mcp__syntax__apply_edits, mcp__syntax__batch_edit_symbols, mcp__syntax__trace, mcp__syntax__find_paths, mcp__syntax__find_dead_code
---

# syntax

**Edit code by function name, not text matching. The Edit tool fails when text isn't unique. This never does.**

## First: list_symbols

Before any edit, know what's in the file:
```
list_symbols({ file_path: 'src/api.ts' })
```

## Why This Wins

| The Problem | Built-in Failure | syntax Solution |
|-------------|------------------|-----------------|
| Edit a function | Edit fails if code appears twice | `edit_symbol` finds by AST |
| Find definition | Grep matches comments/strings | `search_symbols` finds actual symbols |
| Rename everywhere | Miss references, break imports | `rename_symbol` handles all refs |
| Move file | Broken imports everywhere | `move_file` updates all imports |

## Quick Reference

| Task | Tool |
|------|------|
| See file structure | `list_symbols` |
| Read one function | `read_symbol` |
| Change a function | `edit_symbol` |
| Change multiple symbols atomically | `batch_edit_symbols` |
| Find a symbol | `search_symbols` |
| Find all usages | `find_references` |
| Rename everywhere | `rename_symbol` |
| Move file safely | `move_file` |
| Move function | `move_symbol` |
| Who calls this? | `get_callers` |
| What does this call? | `get_callees` |
| Trace call chains | `trace` |
| Find dead code | `find_dead_code` |

## Common Workflows

### Edit a Function
```
list_symbols({ file_path: 'src/utils.ts' })
read_symbol({ file_path: 'src/utils.ts', name_path: 'formatDate' })
edit_symbol({ file_path: 'src/utils.ts', name_path: 'formatDate', new_body: '...' })
```

### Edit Multiple Symbols Atomically
When you need to change a function signature AND update all callers:
```
batch_edit_symbols({
  edits: [
    { file_path: 'src/api.ts', name_path: 'fetchUser', new_body: 'async function fetchUser(id: string, options?: Options) {...}' },
    { file_path: 'src/handlers.ts', name_path: 'handleUser', new_body: 'function handleUser() { fetchUser(id, { cache: true }); }' },
    { file_path: 'src/tests.ts', name_path: 'testFetchUser', new_body: 'test(...) { await fetchUser("123", {}); }' }
  ],
  dry_run: true  // Always preview first!
})
```
**Why batch_edit_symbols?**
- All edits validated BEFORE any are applied
- If one edit fails, NONE are applied (atomic)
- Prevents half-updated code that doesn't compile

### Safe Rename
```
rename_symbol({ old_name: 'oldName', new_name: 'newName', dry_run: true })
rename_symbol({ old_name: 'oldName', new_name: 'newName' })
```

### Move File Without Breaking Imports
```
move_file({ source: 'src/utils.ts', destination: 'src/lib/utils.ts', dry_run: true })
move_file({ source: 'src/utils.ts', destination: 'src/lib/utils.ts' })
```

### Understand Impact Before Changes
```
get_callers({ symbol_name: 'saveUser' })
trace({ symbol: 'handleRequest', direction: 'backward', depth: 3 })
```

### Clean Up After Refactoring
```
remove_unused_imports({ file_path: 'src/handler.ts' })
organize_imports({ file_path: 'src/handler.ts' })
```

## After Editing

1. `types.check_file()` - verify no type errors
2. `test-runner.run_tests()` - verify behavior unchanged

## Supports
TypeScript, JavaScript, Python, Go, Rust
