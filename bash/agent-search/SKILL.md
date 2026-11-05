---
name: agent-search
description: >-
  Choose and run the right search tool: rg vs grep vs ast-grep vs fd vs fzf.
  Bounded repo navigation with ripgrep, fd, tree, bat, and structural search.
  Use when finding symbols, files, syntax patterns, or deciding which CLI
  search to use before reading or editing code.
---

# Agent search

Text and structural search with low memory and bounded output.

## Purpose

Locate files and code quickly using the right CLI tool for the job — before opening large files or running embedding indexes.

## Tool selection (read first)

**Full matrix:** [references/tool-selection.md](references/tool-selection.md)

1. **Default order:** `fd` (filename) → `rg` (content) → `ast-grep` (syntax) → `bat`/`sed` (read slice).
2. **Prefer `rg` over `grep`** — gitignore-aware, faster; use `grep` only if `rg` is missing or piping one stream.
3. **`fd`** when hunting **files by name/path/extension** — not file contents.
4. **`ast-grep`** when the query is **syntax shape** (exports, JSX patterns, call shapes) — not plain strings.
5. **`fzf`** is optional for humans — agents narrow with path prefix + `rg --max-count` instead.
6. **`tree`/`eza`** for directory layout only — not content search.
7. **Cursor IDE:** Grep tool ≈ `rg`; SemanticSearch for meaning; Glob ≈ `fd`.
8. **fff MCP:** When **project** `fff-gallery` is connected, prefer `grep`/`find_files`/`multi_grep` for repeated repo search; one-off probes may still use `rg`/`fd` — see [tool-selection.md](references/tool-selection.md) and [AGENTS.md § fff](../../../AGENTS.md).

## When to use (scenario → tool)

| Scenario | Tool |
|----------|------|
| Find files by name or extension | `fd` |
| Find literal text or regex in code | `rg` |
| `rg` unavailable | `grep` (fallback, avoid `-r` on repo root) |
| Match function/class/JSX structure | `ast-grep` |
| Security or rule-pack scan | `semgrep --dryrun` |
| Orient in unfamiliar directory | `tree -L 2` |
| Read lines after locating file | `bat --line-range` or `sed -n` |
| Too many hits | Narrow path, `--max-count`, or `-g` glob |

## Required tools

- **Text:** `rg`, `fd`, `tree` (or `eza`), optional `fzf`, `bat`, `zoxide`, `delta`
- **Structural:** `ast-grep` (`sg`), optional `semgrep`, `tree-sitter`, `universal-ctags`

Install: [agent-cli-hub/references/install-blocks.md](../agent-cli-hub/references/install-blocks.md)

## Common commands

### Text search (gallery globs)

```bash
rg "ipcMain.handle" electron/ -n --glob '!node_modules'
rg "useGalleryStore" src/ -n --max-count 30
fd "\.tsx$" src/components
tree -L 2 src/
```

### Interactive pick (optional, human only)

```bash
rg --files | fzf
fd . -t f | fzf
```

### Bounded file read

```bash
bat --line-range 1:80 electron/main.ts
sed -n '40,100p' src/App.tsx
```

### Structural (ast-grep)

```bash
ast-grep --pattern 'export function $NAME($$$)' --lang ts src/
semgrep --config auto --dryrun src/
```

### Tags (optional)

```bash
ctags -R src electron
```

PowerShell:

```powershell
rg "ipcMain" electron/ -n
fd "\.tsx$" src
Get-Content .\electron\main.ts -TotalCount 80
```

## Agent-safe patterns

- Always pass `--glob '!node_modules'`, `'!dist'`, `'!mcp-server/dist'` on broad searches.
- Cap matches: `--max-count`, `-m`, or narrow path prefix (`src/`, `electron/`).
- Run `rg` before `cat`; use `bat --line-range` or `sed -n` for slices.
- Prefer `ast-grep --dry-run` / `semgrep --dryrun` before rewrite modes.

## Commands requiring confirmation

- `ast-grep -U` (rewrite), `semgrep --autofix` — see [commands-requiring-confirmation.md](../agent-cli-hub/references/commands-requiring-confirmation.md).

## Troubleshooting

- **No matches:** Try case-insensitive `rg -i`; check wrong folder or generated `dist/`.
- **Wrong tool:** See [tool-selection.md](references/tool-selection.md) — filename vs content vs syntax.
- **ast-grep missing:** `npm i -g @ast-grep/cli` or see install blocks.
- **WSL fd:** Use `fdfind` or symlink to `fd`.

## Verification checklist

```bash
rg --version && fd --version
rg "export" src/ -n --max-count 3
```
