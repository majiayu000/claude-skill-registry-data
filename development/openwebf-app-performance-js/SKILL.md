---
name: openwebf-app-performance-js
description: Measure and optimize WebF app performance from the JavaScript side (performance.mark/measure, bundle size, code splitting, debouncing, CSS transforms). Use when the user mentions performance.mark/measure, JS profiling, heavy JS work, bundle size, code splitting, debouncing, or animation performance.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section
---

# OpenWebF App: Performance (JavaScript Side)

## Instructions

1. Establish a measurement baseline (prefer production builds for accuracy).
2. Add minimal instrumentation (`performance.mark/measure`) around suspected hot paths.
3. Apply high-leverage best practices:
   - reduce sync work on critical path
   - debounce expensive operations
   - split bundles and monitor size
4. Use MCP docs for recommended practices and code snippets.

If the user’s question is primarily about host-side FP/FCP/LCP wiring or `dumpLoadingState`, prefer `openwebf-host-performance-metrics`.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
