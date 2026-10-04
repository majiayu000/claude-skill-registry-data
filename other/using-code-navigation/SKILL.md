---
name: using-code-navigation
description: >
  Use code navigation tools for symbol-level code work instead of grep/read: finding
  classes, methods, functions, references, and cross-module wiring. Activate when
  tracing, navigating, or refactoring named code entities in an LSP-supported language,
  or for project onboarding/memory capture. Do NOT activate for plain-text searches,
  known file paths, or non-code files — use grep/glob/read there.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before any code navigation lookup (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`
- `<project-root>/docs/memory-providers.md`

Code navigation tools provide LSP-backed semantic operations (see `<project-root>/docs/code-navigation.md` in the project root). Prefer them over `grep`/`read` for symbol-level work; they are token-efficient and accurate.

## Project Activation (MANDATORY first step)

Every code navigation tool requires an active project. No exceptions.

1. List tools on the code navigation server once per session (not per call) (see `<project-root>/docs/code-navigation.md` in the project root).
2. Activate project with the project name (folder name, not full path) (see `<project-root>/docs/code-navigation.md` in the project root). Accepts full path too if unsure.
3. Read the response — it lists existing memories.

Re-activate: start of every new session, after `cwd` changes to a different repo, or if any tool returns `No active project` (pick the matching name from the error). Treating `No active project` as a server outage is a missing-activation error — activate and retry.

## When to Use Which Tool

| Situation | Operation | Notes |
|-----------|-----------|-------|
| First look at unfamiliar file | Symbol overview | Compact symbol tree; `depth=1` for method list |
| Know class/method name, want body | Find symbol with `include_body=true` | Use `name_path` like `Class/method` |
| Children of class without bodies | Find symbol with `depth=1` | Cheaper than `include_body` |
| "Where is this used?" | Find referencing symbols | Requires `name_path` + `relative_path` |
| "What implements this interface?" | Find implementations | Same args as references |
| "Where is this declared?" | Find declaration | For imports/re-exports |
| Plain-text / regex search | Search for pattern | Only when symbol name unknown |
| Rename across codebase | Rename symbol | LSP-aware, updates all references |
| Delete a symbol safely | Safe delete symbol | Returns refs if unsafe |
| Lint/type errors for a file | Get diagnostics for file | Use before/after edits |
| Persist project knowledge | Write memory | Recall with read memory / list memories |

See `<project-root>/docs/code-navigation.md` in the project root for exact tool names and arguments.

## Name Paths

`find_symbol` matches against the in-file symbol tree, not the filesystem. See `<project-root>/docs/code-navigation.md` in the project root for implementation details.

- Simple: `"method"` → any symbol named `method`
- Relative: `"Class/method"` → matches suffix
- Absolute: `"/Class/method"` → exact match only
- Overloads: append `[i]` (e.g. `"Class/method[0]"`)
- Substring on last element: `substring_matching=true` makes `"Foo/get"` match `getValue`, `getData`

## Workflow Patterns

**Understanding a new file:** Symbol overview (depth 0) → find symbol with `depth=1` on main class → find symbol with `include_body=true` on specific method(s).

**Tracing a call chain:** Find symbol to locate entry point → find referencing symbols to find callers → repeat on each caller until boundary (controller, route, queue).

**Verifying a refactor:** Find referencing symbols on the symbol → if empty, safe delete is safe → after edit, get diagnostics for file on touched files → for renames, use rename symbol instead of manual edits.

**Cross-module wiring (e.g. Laravel bindings):** Find symbol on the contract → find implementations for concrete classes → search for pattern in `ServiceProvider.php` files for binding calls.

## Memories

The code navigation tool may provide memory capabilities (see `<project-root>/docs/memory-providers.md` in the project root). Memories are persistent, per-project markdown notes in memory storage (see `<project-root>/docs/memory-providers.md` in the project root).

Memory tools require an active project (same activate project call). Write tools (write memory, edit memory, delete memory, rename memory) require `editing` mode — if they return `Tool ... is not active`, the code navigation config must include `editing` in `base_modes`/`default_modes` (see `<project-root>/docs/code-navigation.md` in the project root).

| Operation | Tool |
| --- | --- |
| List (optionally by topic) | List memories |
| Read / Write new / Update / Delete / Rename | Read memory / Write memory / Edit memory / Delete memory / Rename memory |

## Project Setup

- Activate project — switch active project by name or path
- Get current config — see active project, available projects, modes
- Onboarding — call once per project to generate initial memory
- Initial instructions — read once per session if unsure how to drive the code navigation tool

## Limits and Fallbacks

- LSP must support the language. For dynamic/eval'd symbols, Blade templates, or config arrays, fall back to `grep`/`read`.
- Find referencing symbols requires `relative_path` (a file, not a directory). Get it from a prior find symbol result. For external deps, `relative_path` is an `<ext...>` identifier — never guess it.
- Line numbers are 0-based. Adjust when reporting or matching `read` output (1-based).
- Use `depth` before `include_body=true`. Request bodies only for specific method(s) needed.
- Batch related queries — call find symbol, find references, and find implementations in parallel when independent.

