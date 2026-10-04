---
name: explore
description: Deep codebase exploration, architectural research, and solution discovery. Use when investigating problems, understanding complex flows, or evaluating technical approaches without jumping straight into code mutation or TDD.
mcp: codebase-memory-mcp
---

# /supergraph:explore

Investigate first. Understand deeply. No unwanted code modification.

Announce: "🧭 /supergraph:explore — investigating codebase and tracing flows..."

## When to Use

- Understanding an existing feature, module, or architecture
- Tracing end-to-end request/event lifecycles (UI → BLoC/Service → API → DB)
- Investigating bug symptoms before declaring a fix approach
- Evaluating libraries, architectural options, or technical trade-offs
- Onboarding to a new workspace or subsystem

## Workflow

### 1. Define Research Scope
- **Subject**: What system, flow, or question is being investigated?
- **Boundaries**: Known entry points, affected modules, or target concepts.
- **Target Output**: Architecture overview, flow diagram, root cause analysis, or comparison matrix.

### 2. Semantic & Graph Discovery
- **High-level map**: Use `get_architecture(project=CBM_PROJECT)` or `/zoom-out` to orient.
- **Symbol / Route discovery**: Use Serena `find_symbol`, `get_symbols_overview` or Codebase Memory `search_graph`.
- **Trace connections**: Use `trace_path` or Serena `find_referencing_symbols` / `find_implementations` to identify callers, callees, and data flow.

### 3. Targeted Source Deep-Dive
- Inspect the actual code files for key components (controller, service, repository, UI state).
- Read method implementations directly when business logic, validations, or transformations matter.
- Target reading precisely: understanding requires seeing concrete implementations, not just graph nodes.

### 4. Trace the Flow End-to-End
Trace the execution path:
1. **Entry Point**: HTTP route handler, UI widget event, CLI command, or queue consumer.
2. **Middleware / Guards**: Authentication, validation, rate limiting, interceptors.
3. **Domain Logic / Orchestration**: Service layer, state management, entity calculations.
4. **Data / External I/O**: Database queries, external API calls, cache lookups.
5. **Output / Side Effects**: Response serialization, state updates, event emissions.

### 5. Synthesize & Report Findings
Present findings in clear, structured Markdown:
- **Executive Summary**: 2-3 sentences explaining how it works or what the finding is.
- **Flow Diagram**: ASCII or Mermaid sequence/flowchart.
- **Key Files & Responsibilities**: Table of files with their exact role.
- **Critical Invariants & Edge Cases**: Hidden assumptions, potential pitfalls, race conditions.
- **Recommendations**: If leading into implementation, outline next steps (`/plan`, `/analyze`, or `/prototype`).
