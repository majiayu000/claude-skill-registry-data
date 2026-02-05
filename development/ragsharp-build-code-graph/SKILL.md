---
name: ragsharp-build-code-graph
description: |
  Build or update a code graph index for C#/.NET repositories using ragsharp-graph.
  Triggers: build index, update index, refresh index, code graph, dependency graph, static analysis, Roslyn, line numbers.
---
## Steps
1. Run `ragsharp graph doctor --root .`.
2. Run `ragsharp graph index --root . --db .ragsharp/graph/index.db --state .ragsharp/graph/state.json`.
3. For incremental updates, run `ragsharp graph update --root . --db .ragsharp/graph/index.db --state .ragsharp/graph/state.json`.

## Expected Results
- `.ragsharp/graph/index.db` exists.
- `.ragsharp/graph/state.json` is updated.
- Output goes to stderr, JSON is emitted only for query commands.
