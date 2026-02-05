---
name: go-navigator-read
description: Use Go Navigator MCP to explore Go code semantically (packages, symbols, definitions/references, context, metrics, deps) and return file/line/snippets; do not modify code.
---

# Go Navigator (READ) — semantic navigation only

## Scope rules
- READ-ONLY: never call renameSymbol or rewriteAst (or any tool that changes files).
- Prefer semantic tools over raw text search.

## Defaults
- Use "dir": "." unless the user specifies another root.
- For any "package" field, use the exact import path returned by listPackages (go list style).

## Recommended workflows

### Orientation in a new repo
1) listPackages { "dir": "." }
2) getProjectSchema { "dir": ".", "depth": "standard" } (optional)
3) getMetricsSummary { "dir": ".", "package": "<pkg>" } (optional)
4) getDependencyGraph { "dir": ".", "package": "<pkg>" } (optional)

### Understand a symbol
1) getDefinitions { "dir": ".", "ident": "<Ident>" }
2) getReferences  { "dir": ".", "ident": "<Ident>" }
3) getSymbolContext { "dir": ".", "ident": "<Ident>", "kind": "<func|type|...>" } (preferred)
4) getFunctionSource / getStructInfo / getFileInfo for deeper inspection

### Interfaces & implementations
- listInterfaces { "dir": ".", "package": "<pkg>" }
- getImplementations { "dir": ".", "name": "<InterfaceOrTypeName>" }

### Complexity, dead code, summary
- getComplexityReport { "dir": ".", "package": "<pkg>" }
- getDeadCodeReport { "dir": ".", "package": "<pkg>", "limit": 10 }
- getMetricsSummary { "dir": ".", "package": "<pkg>" }

## Large result sets
- Use limit/offset pagination where supported (getDefinitions/getReferences).
- Return the most relevant files first.

## Output format
- Always include file paths + line numbers.
- Include minimal snippets (1–5 lines) unless asked for full bodies.
- Summarize findings and propose next tool calls (still read-only).
