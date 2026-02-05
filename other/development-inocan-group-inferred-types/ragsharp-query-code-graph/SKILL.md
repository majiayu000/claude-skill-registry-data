---
name: ragsharp-query-code-graph
description: |
  Query the ragsharp code graph for declarations, references, callers, callees, dependencies, and line-number evidence.
  Triggers: find usages, where defined, callers, callees, dependency path, project deps, type hierarchy, line numbers, evidence.
---
## Steps
1. Run `ragsharp graph query --type symbols --db .ragsharp/graph/index.db --limit 50 --symbol "SymbolName"`.
2. Use the JSON output to answer questions with file:line-range evidence.
