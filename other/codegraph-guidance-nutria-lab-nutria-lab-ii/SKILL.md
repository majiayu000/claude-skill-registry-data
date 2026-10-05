---
name: codegraph-guidance
description: "Trigger: architecture, codebase map, call flow, dependency, symbol, impact, affected files. Use CodeGraph before broad filesystem exploration."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use before answering or changing structural codebase questions.

# Hard Rules
- Resolve the project root, confirm it is a project, then check `.codegraph/`.
- Initialize once only when the index is missing in a real project.
- Prefer `codegraph_explore`; use `codegraph explore` only if MCP is unavailable.
- Do not use administrative/destructive lifecycle commands in ordinary work.

# Execution Steps
1. Run `git rev-parse --show-toplevel || pwd`.
2. Check `<root>/.codegraph/`; if absent, run `codegraph init <root>`.
3. Ask one focused explore question for symbols, path, callers/callees and blast radius.
4. Fall back to filesystem search only if CodeGraph fails; state the fallback.

# Output Contract
Return the indexed evidence, call path/blast radius, and affected files. Do not claim structural facts from intuition.
