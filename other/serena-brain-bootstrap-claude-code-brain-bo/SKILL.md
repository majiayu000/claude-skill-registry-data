---
name: serena
description: Use when renaming symbols across files, finding all references to a function/class, moving code between files, or inlining variables — LSP-backed atomic multi-file refactoring
user-invocable: true
disable-model-invocation: true
---

# Serena — LSP-Backed Symbol Refactoring

**MCP server key:** `serena` — tools: `mcp__serena__*`

**Core principle:** Type-aware, 100% recall. Grep finds strings; Serena finds symbols — including aliased imports, dynamic usages, and type-renamed references.

## Decision Matrix

| Question                              | Use                                           |
| ------------------------------------- | --------------------------------------------- |
| "Rename `AuthService` everywhere"     | `serena` — `rename_symbol`                    |
| "Find all callers of `login()`"       | `serena` — `find_references`                  |
| "Move `UserMapper` to another file"   | `serena` — `move_symbol`                      |
| "Inline the `MAX_RETRIES` constant"   | `serena` — `inline_symbol`                    |
| "Find code about rate limiting"       | `cocoindex-code` — semantic meaning           |
| "Who calls AuthService in the graph?" | `codebase-memory-mcp` — architecture overview |
| "Is renaming this safe to ship?"      | `code-review-graph` — blast radius            |

## Key Tools

```
mcp__serena__find_symbol(name, type?)        — find by name/type (LSP, not grep)
mcp__serena__find_references(symbol)        — all usages across the project
mcp__serena__get_symbol_info(symbol)        — signature, docstring, defined-in, refs
mcp__serena__rename_symbol(symbol, new_name) — rename everywhere atomically
mcp__serena__move_symbol(symbol, target_file) — move + fix all imports
mcp__serena__replace_symbol_body(symbol, body) — replace impl, keep signature
mcp__serena__inline_symbol(symbol)          — inline at all call sites
mcp__serena__get_call_graph(symbol)         — call graph from a symbol
```

## Standard Workflows

**Rename across codebase:**

```
1. mcp__serena__find_symbol("OldName")       → confirm it's the right symbol
2. mcp__serena__find_references("OldName")  → verify scope
3. mcp__serena__rename_symbol("OldName", "NewName")  → atomic rename
```

**Move a class to another file:**

```
1. mcp__serena__get_symbol_info("MyClass")  → see current location and imports
2. mcp__serena__move_symbol("MyClass", "src/new_module.py")
```

**Find all callers before deleting:**

```
1. mcp__serena__find_references("legacyFunction")  → if empty, safe to delete
```

## Project Config

`.serena/project.yml` (committed to repo) controls which language servers are active:

```yaml
languages:
  - python
  - typescript
  - javascript
```

Language servers are auto-installed by serena on first use (pyright, typescript-language-server).

## Token Cost

Low — on-demand per MCP call. No background indexing process. LSP server initializes on first call (~2-3s), then fast.

## When NOT to Use

- Architecture overview → `codebase-memory-mcp` (Cypher graph, whole-codebase view)
- Semantic search → `cocoindex-code` (find code by meaning when you don't know exact names)
- Change risk → `code-review-graph` (blast radius, safety score before PR)
- Simple text grep → `Grep` tool (faster for literal strings with no aliasing concern)
