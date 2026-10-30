---
name: codegraph
description: In a repository with a CodeGraph index, use the code graph before grep or find to locate symbol definitions, call paths, and dependencies.
---

# codegraph: graph before grep

## Precondition

Check for a `.codegraph/` directory at the repository root.

- Present: use this skill before grep or find.
- Absent: use normal search. A full index build is the agent's decision: build one only when the task needs many symbol lookups, and keep `.codegraph/` out of commits.

## Commands

```bash
codegraph explore "<symbol names or a question>"   # verbatim source of the relevant symbols and the call paths between them
codegraph node <symbol-or-file-path>                # one symbol's full source and its callers, or a whole file with line numbers
```

Examples: `codegraph explore "ServiceRegistry"`, `codegraph node common/core/registry.py`.

## Rules

1. For "where is X defined", "who calls Y", and "what is the module topology", run `codegraph explore` first.
2. The output already holds the source. Do not read the same files again.
3. Cite the exact symbol and line number that the graph confirmed. Do not guess.
