---
name: flutter-dart-code-review
description: Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture.
mcp: codebase-memory-mcp
---

# /supergraph:flutter-dart-code-review

Library-agnostic Flutter/Dart code review. Graph-first, then checklist.

Announce: "🐦 /supergraph:flutter-dart-code-review — reviewing Flutter/Dart code..."

## Steps

### 1. Graph analysis (surface hotspots before manual review)

Use `CBM_PROJECT`: call `get_architecture` with `hotspots`, then validated
`hubs`, `cycles`, `complexity`, `cross-boundary`, and `test-gaps` recipes. Apply
the existing Flutter thresholds: `build()` over 80–100 lines, complexity limits,
10+ dependents, circular DI, unexpected layer coupling, and untested files.

**Serena (optional — if available):**
```
mcp__serena__get_diagnostics_for_file(<file>)      # type errors, null safety violations
mcp__serena__find_referencing_symbols(<symbol>)    # callers of changed public APIs
mcp__serena__find_implementations(<interface>)     # subclasses after interface change
```
Skip if Serena unavailable.

### 2. Manual checklist review

Work through [CHECKLIST.md](./CHECKLIST.md) — 15 sections covering:
General health · Dart pitfalls · Widgets · State management · Performance · Testing · Accessibility · Platform · Security · Dependencies · Navigation · Error handling · l10n · DI · Static analysis

Focus on areas flagged by step 1 first.

### 3. Report

```
## Flutter/Dart Review
- Graph hotspots: [list/none]
- Serena diagnostics: [issues/clean/skipped]
- Checklist: PASS | ISSUES (list critical items)
- Next: /supergraph:fix → /supergraph:verify
```

## Rules

- Run graph analysis before opening checklist — prioritize hotspots
- Serena diagnostics catch null safety / type errors manual review misses
- State management rules apply to ALL solutions (BLoC, Riverpod, GetX, MobX, Signals)
- Full checklist in [CHECKLIST.md](./CHECKLIST.md)
