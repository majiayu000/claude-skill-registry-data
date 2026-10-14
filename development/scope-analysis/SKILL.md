---
name: scope-analysis
description: "Trigger: scope analysis, target boundary discovery. Delimit class/package/module scope."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.2"
  status: in-progress
---

# Scope Analysis
Delimit whether the target is a class, package, or module, then keep the plan inside that boundary.

## How to inspect

- Identify the primary target file(s).
- Find public methods, exported APIs, public constructors, endpoints, and events.
- Find callers/consumers with references, imports, routes, LSP, or a code-graph index (for example, Graphify MCP/CLI) when available.
- Find existing tests by naming, package, fixtures, integration suites, and build metadata.
- Separate in-scope files from neighboring context.
- Record out-of-scope work explicitly.
