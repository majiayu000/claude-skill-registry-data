---
name: lsp
description: Code intelligence via Language Server Protocol — hover, definition, references, diagnostics, completion, symbols, formatting. Use for semantic code navigation, type inspection, and error detection that goes beyond text search.
---

Use `lsp` for semantic code intelligence. Prefer `grep`, `ast-grep`, or `ripgrep` for textual or structural search. Use `lsp` when you need **type information**, **go-to-definition**, **find-all-references**, **compiler diagnostics**, or **code structure**.

## Session lifecycle

LSP servers are long-lived. Start a session before querying and stop it when done.

```sh
# Start a session — auto-detects project root from VCS markers (.git, .jj)
lsp session start --lsp gopls

# Query
lsp hover --lsp gopls main.go 15 8
lsp definition --lsp gopls main.go 15 8

# Stop when done
lsp session stop --lsp gopls
```

Only one `{project, lsp}` pair at a time — starting gopls twice in the same project reuses the running session.

## When to start a session

Start an LSP session when you will perform multiple queries against the same project. If you only need one quick check, still start a session — LSP servers require initialization.

## Which LSP to use

| LSP name | Languages | Key project markers |
| --- | --- | --- |
| `gopls` | Go | `go.mod` |
| `typescript-language-server` | TypeScript, JavaScript | `tsconfig.json`, `package.json` |
| `pyright` | Python | `pyproject.toml`, `setup.py` |
| `nixd` | Nix | `flake.nix`, `default.nix` |
| `clangd` | C, C++ | `compile_commands.json`, `CMakeLists.txt` |
| `rust-analyzer` | Rust | `Cargo.toml` |
| `bash-language-server` | Bash, Shell | `.git`, `.jj` |
| `yaml-language-server` | YAML | `.git`, `.jj` |
| `intelephense` | PHP | `composer.json`, `index.php` |

## Position format

Line and character (column) are **0-indexed**. Example: first character of line 1 is `0 0`.

## Recipes

### Get type info at a position

```sh
lsp session start --lsp gopls
lsp hover --lsp gopls main.go 15 8
```

### Go to definition

```sh
lsp definition --lsp gopls main.go 15 8
# Returns list of locations: [{uri, range: {start, end}}]
```

### Find all references

```sh
lsp references --lsp gopls main.go 15 8
# Returns list of locations
```

### Get diagnostics

```sh
# All diagnostics for the project
lsp diagnostics --lsp gopls

# For a specific file
lsp diagnostics --lsp gopls main.go
```

### Get code structure

```sh
# Document symbols (outline)
lsp symbols --lsp gopls main.go

# Workspace-wide symbol search
lsp symbols --lsp gopls
```

### Get completions

```sh
lsp completion --lsp gopls main.go 15 8
```

### Format a file

```sh
lsp format --lsp gopls main.go
```

## Common mistakes to avoid

- Forgetting to start a session before querying.
- Using 1-indexed line/column numbers (LSP uses 0-indexed).
- Not stopping sessions when done (LSP servers consume memory).
- Using `lsp` for text search — use `grep` or `rg` instead.
- Querying a file outside the project root.

## Command reference

### Session commands

- `lsp session start --lsp NAME [--root DIR]` — start LSP server for project
- `lsp session stop --lsp NAME [--root DIR]` — stop LSP server
- `lsp session list` — list active sessions (JSON)

### Query commands

All require `--lsp NAME`. Optional `--root DIR` overrides project root.

- `lsp hover --lsp NAME FILE LINE CHAR`
- `lsp definition --lsp NAME FILE LINE CHAR`
- `lsp references --lsp NAME FILE LINE CHAR`
- `lsp diagnostics --lsp NAME [FILE]`
- `lsp completion --lsp NAME FILE LINE CHAR`
- `lsp symbols --lsp NAME [FILE]`
- `lsp format --lsp NAME FILE`
