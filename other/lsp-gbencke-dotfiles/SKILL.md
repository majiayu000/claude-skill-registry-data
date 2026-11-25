---
name: lsp
description: Structural code analysis, navigation, and diagnostics using ast-grep.
---

# AST-Grep LSP (Language Server Protocol)

This skill provides structural code analysis and navigation across many programming languages without requiring a full Language Server (LSP) setup for each language. It uses `ast-grep` under the hood (and `typescript-language-server` specifically for TS/TSX).

**Requires `ast-grep` (`sg`) to be installed in your system PATH.** (TS/TSX also requires `typescript-language-server`).

## Supported Languages
Python, TypeScript, TSX, JavaScript, JSX, Rust, Go, C, C++, Lua, JSON, HTML, CSS.

## Available Tools

### `lsp_hover(file, line, character)`
*   **What it does:** Shows the definition context or signature of the symbol at a given 1-based line/character position.
*   **When to use:** When you see a function or variable and want to quickly peek at its signature without navigating to its definition.

### `lsp_definition(file, line, character)`
*   **What it does:** Finds the location where the symbol under the cursor is defined.
*   **When to use:** When you need to jump to the actual source code of a function, class, or variable to read its implementation.

### `lsp_symbols(file)`
*   **What it does:** Lists all symbols (classes, functions, variables, structs, etc.) declared in a source file.
*   **When to use:** When you open a new file and want a quick high-level outline of what is defined inside it.

### `lsp_diagnostics(file, rule?, wait_ms?)`
*   **What it does:** Runs rule-based structural checks on a file or directory. 
*   **When to use:** To find code smells, security issues, or enforce project conventions. 
*   **Note:** Relies on an `sgconfig.yml` file in the project, or you can pass a specific `--rule` YAML file. For TS/TSX, it will use `typescript-language-server` to return standard TypeScript compilation errors.

### `lsp_format(file)`
*   **What it does:** Suggests the standard formatter command for the given file's language.
*   **Note:** `ast-grep` does not format code itself. This tool just tells you what CLI command to run (e.g., `prettier --write <file>`).

## Slash Commands

### `/lsp-status`
Shows the current `ast-grep` version installed and lists all file extensions supported by the current detection mapping.

## In Claude Code

Claude Code has no `lsp_*` tools. Use these instead:

| pi tool           | Claude Code                                                                             |
| ----------------- | --------------------------------------------------------------------------------------- |
| `lsp_hover`       | Built-in `LSP` tool, `hover` operation                                                  |
| `lsp_definition`  | Built-in `LSP` tool, `goToDefinition` operation                                         |
| `lsp_symbols`     | Built-in `LSP` tool, `documentSymbol` operation                                         |
| `lsp_diagnostics` | `ast-grep scan <path>` (with `--rule <file.yml>`); TS errors arrive from the LSP plugin |
| `lsp_format`      | Run the language formatter through Bash (`prettier --write`, `ruff format`, …)          |

The built-in `LSP` tool needs `ENABLE_LSP=1` and a language plugin (`typescript-lsp`, `pyright-lsp`).
