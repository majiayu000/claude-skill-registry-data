---
name: serena
description: Serena code intelligence — LSP-powered symbol navigation, diagnostics, and targeted code surgery. Activate before complex refactors, cross-file analysis, or when graph tools need symbol-level depth.
---

# /supergraph:serena

Activate Serena MCP for LSP-powered code intelligence: symbol navigation, type diagnostics, and safe code surgery.

**CRITICAL:** Call `initial_instructions` first when starting any Serena work — it loads the Serena Instructions Manual with project-specific context.

## When to Use

- Before complex refactors: rename across codebase, API signature changes
- When blast radius is unclear and graph tools lack symbol-level depth
- Before review: verify all call sites of changed symbols are updated
- During fix: triage type errors before running test suite
- After architectural changes: verify no orphaned references remain
- Large-scale refactors: safe_delete_symbol, rename_symbol across entire project

## Setup

### 1. Load instructions (MANDATORY first step)

```
mcp__plugin_serena_serena__initial_instructions()
# or
mcp__serena__initial_instructions()
```

### 2. Activate project

```
mcp__plugin_serena_serena__activate_project()
```

### 3. Get project overview

```
mcp__plugin_serena_serena__get_symbols_overview()
```

Returns top-level symbols, classes, functions — fast structural map of the codebase.

## Tool Reference

### Navigation

| Tool | Use case |
|------|----------|
| `find_symbol` | Locate a symbol by name across codebase |
| `find_declaration` | Jump to where a symbol is declared |
| `find_implementations` | Find all implementations of an interface / abstract class |
| `find_referencing_symbols` | Find all callers and usages of a symbol |

### Setup / Lifecycle

| Tool | Use case |
|------|----------|
| `activate_project` | Register project with Serena — requires `mcp__plugin_serena_serena__` namespace |
| `get_current_config` | Read Serena's current project configuration |
| `open_dashboard` | Open the Serena dashboard UI |
| `execute_shell_command` | Run shell commands (use with caution — confirm before destructive ops) |

### Diagnostics

| Tool | Use case |
|------|----------|
| `get_diagnostics_for_file` | IDE-level type errors, lint warnings for a specific file |
| `get_symbols_overview` | Project structure overview — top-level symbols map |

### Code Surgery (prefer over raw text edits)

| Tool | Use case |
|------|----------|
| `replace_symbol_body` | Replace function/method body — exact, no regex risk |
| `insert_after_symbol` | Insert code after a symbol definition |
| `insert_before_symbol` | Insert code before a symbol definition |
| `rename_symbol` | Safe rename across entire codebase |
| `safe_delete_symbol` | Delete symbol, verify no remaining references |

### File Operations

| Tool | Use case |
|------|----------|
| `find_file` | Find files by name pattern |
| `list_dir` | List directory contents |
| `read_file` | Read file content |
| `search_for_pattern` | Regex search across files |
| `replace_content` | Replace text content in file |
| `create_text_file` | Create a new text file |

### Memory (cross-session context)

| Tool | Use case |
|------|----------|
| `write_memory` | Save analysis findings for future sessions |
| `read_memory` | Recall prior analysis |
| `list_memories` | List all saved memories |
| `edit_memory` | Update an existing memory |
| `rename_memory` | Rename an existing memory entry |
| `delete_memory` | Remove stale memory |

## Memory Workflow

Use Serena memory to persist analysis state across sessions — avoids re-deriving complex blast radius mappings:

```
# Save findings after analysis:
mcp__serena__write_memory(title="auth-refactor-callers", content="find_referencing_symbols(login) = [A, B, C]")

# Recall in next session:
mcp__serena__read_memory(title="auth-refactor-callers")
```

## Integration Points in Other Skills

Serena is invoked as optional hooks inside other supergraph skills:

| Skill | Hook | Tools used |
|-------|------|------------|
| `scan` | Step 2b/3b | `activate_project`, `get_symbols_overview` |
| `plan` | Step 3b | `find_referencing_symbols`, `find_implementations`, `write_memory` |
| `analyze` | Step 2b | `find_referencing_symbols`, `find_implementations` |
| `tdd` | After RED, after GREEN, refactor | `get_diagnostics_for_file`, `replace_symbol_body`, `rename_symbol` |
| `execute` | Code surgery, post-execution | `replace_symbol_body`, `rename_symbol`, `insert_after_symbol`, `find_referencing_symbols` |
| `fix` | Pre-loop + each iteration | `get_diagnostics_for_file`, `replace_symbol_body`, `rename_symbol` |
| `verify` | Step 3b | `get_diagnostics_for_file` |
| `review` | Step 3b | `find_referencing_symbols`, `find_implementations`, `get_diagnostics_for_file`, `write_memory` |
| `integration` | Post-test | `find_referencing_symbols`, `get_diagnostics_for_file` |
| `architecture` | Step 2 | `get_symbols_overview` |
| `database-migrations` | Impact check | `find_referencing_symbols` |
| `webapp-testing` | Component impact | `find_referencing_symbols` |
| `flutter-dart-code-review` | MCP-Integrated Review | `get_diagnostics_for_file`, `find_referencing_symbols`, `find_implementations` |

## MCP Tool Name Variants

Two variants may be present depending on project setup:

```
# Plugin variant (full feature set — file ops + symbol nav):
mcp__plugin_serena_serena__<tool>

# Direct variant (symbol navigation focus):
mcp__serena__<tool>
```

Use whichever responds. If both are available: prefer `mcp__plugin_serena_serena__` for file operations, `mcp__serena__` for symbol navigation.

## Fallback

If Serena MCP is not available:
- Log: "Serena unavailable, skipping symbol intelligence step"
- Do NOT block workflow — all Serena steps are optional enhancements
- Fall back to graph MCP tools + Read/Bash/grep for the same purpose

## Rules

- Always call `initial_instructions` before any other Serena tool
- Prefer `replace_symbol_body` and `rename_symbol` over raw text edits for code changes
- Use `safe_delete_symbol` instead of manual deletion — it verifies no remaining references
- Save complex analysis to Serena memory when it may be needed across sessions
- Never use `execute_shell_command` for destructive operations without user confirmation
