---
name: code-delta
description: Visualize proposed code changes in a structured ASCII format with file tree, impact summary, syntax-highlighted diff, and rationale. Use this skill when proposing refactors, simplifications, or any code modifications.
---

# Code Delta Visualization Skill

When proposing code changes, ALWAYS present them in this structured format:

## Format Template

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Change #N: [Short descriptive title]                                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  FILE TREE                                                                   ║
║  [root path]/                                                                ║
║  ├── path/to/                                                                ║
║  │   └── file1.tsx                          [ACTION]  ±N LOC                 ║
║  └── path/to/                                                                ║
║      └── file2.ts                           [ACTION]  -N LOC                 ║
║                                             ─────────────────                ║
║                                             Total:      -N LOC               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  IMPACT SUMMARY                                                              ║
║  ┌─────────────────────┬──────────────┬──────────────┬─────────┐             ║
║  │ Metric              │ Before       │ After        │ Delta   │             ║
║  ├─────────────────────┼──────────────┼──────────────┼─────────┤             ║
║  │ LOC (this change)   │ —            │ —            │ -N      │             ║
║  │ Cyclomatic          │ N            │ N            │ -N      │             ║
║  │ Cognitive           │ N            │ N            │ -N      │             ║
║  │ Dependencies        │ [before]     │ [after]      │ [note]  │             ║
║  └─────────────────────┴──────────────┴──────────────┴─────────┘             ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DIFF                                                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
```diff
--- a/path/to/file1.tsx
+++ b/path/to/file1.tsx
-removed line
+added line
 context line

--- a/path/to/file2.ts
+++ b/path/to/file2.ts
-removed line
+added line
```
```
╔══════════════════════════════════════════════════════════════════════════════╗
║  RATIONALE                                                                   ║
║  • Reason 1                                                                  ║
║  • Reason 2                                                                  ║
║  • Reason 3                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Field Definitions

### FILE TREE
- Show relative paths from a common root
- Use tree characters: `├──`, `└──`, `│`
- Actions: `[MODIFIED]`, `[ADDED]`, `[DELETED]`, `[RENAMED]`
- Show LOC change per file: `+N LOC`, `-N LOC`, `±0 LOC`
- Include total at bottom

### IMPACT SUMMARY
Required metrics:
- **LOC (this change)**: Net lines added/removed
- **Cyclomatic Complexity**: Number of independent paths through code (if/else, switch cases, loops, &&, ||)
- **Cognitive Complexity**: How difficult code is to understand (nesting depth, breaks in linear flow, recursion)
- **Dependencies**: New imports, removed imports, or "Reuse" if using existing

Optional metrics (include when relevant):
- **Test Coverage**: If tests affected
- **Bundle Size**: If significant

### DIFF
- Use ```diff syntax for red/green highlighting
- Group by file with `--- a/` and `+++ b/` headers
- Include minimal context lines for clarity
- Separate files with blank line

### RATIONALE
- Bullet points explaining why this change improves the codebase
- Focus on: reduced duplication, reuse, readability, maintainability

## Usage

After presenting a change in this format, always end with:

```
Apply? (y/n)
```

Wait for user confirmation before making changes.