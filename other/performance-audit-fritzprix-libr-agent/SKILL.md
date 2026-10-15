---
name: performance-audit
description: >
  Analyze and identify performance bottlenecks across the full stack (Rust concurrency and memory,
  Tauri IPC, React rendering, SQLite queries), and generate a prioritized action plan report (P0-P2)
  with concrete Before/After code solutions. Use when asked to audit performance, investigate UI lag or
  freezes, optimize Rust async/locks or memory allocations, eliminate React re-render cascades, diagnose
  slow SQLite queries or IPC serialization overhead, or when user triggers: "성능상의 개선점 분석",
  "성능 감사", "성능 최적화", "병목 분석", "performance audit", "perf audit", "profile bottlenecks".
---

# Performance Audit

Systematically identify performance bottlenecks, CPU/memory hotspots, and latency culprits across LibrAgent's full stack, then generate a prioritized action plan (P0-P2) with actionable Before/After code solutions.

## Scope & Diagnostic Domains

LibrAgent is a local desktop application (Tauri + Rust + React/TypeScript + SQLite). Performance issues primarily fall into four domains:

1. **Rust Concurrency & Memory**:
   - Synchronous blocking inside Tokio async tasks
   - Lock contention and extended guard scopes (`Mutex`, `RwLock`)
   - Unnecessary cloning, large buffer allocations, and non-streaming file/payload processing
2. **Tauri IPC Boundary**:
   - Massive JSON payload serialization across IPC
   - Chatty, unbatched command invocations
   - Unreleased event listeners causing leaks
3. **Frontend (React / TypeScript)**:
   - Re-render cascades and unmemoized heavy computations in render paths
   - Unstable object/callback references invalidating child memoization
   - Unvirtualized long lists (chat items, logs, file trees)
4. **SQLite & Data Access**:
   - N+1 queries and missing index full-table scans
   - Unbatched bulk inserts/updates outside transactions
   - Connection pool contention and non-WAL mode operations

Detailed checklist: see [references/checklist-fullstack.md](references/checklist-fullstack.md).

---

## Performance Audit Workflow

```
1. Target Hot Path ➔ 2. Inspect Code ➔ 3. Classify Priority (P0-P2) ➔ 4. Draft Before/After ➔ 5. Action Plan Report
```

### 1. Identify Target Scope
- Clarify or identify the target module, feature, or flow under investigation (e.g., chat stream rendering, session transcript loading, tool execution pipeline, history search).
- Examine relevant source files directly without guessing.

### 2. Systematic Code Inspection
Cross-examine the target against the [Full-Stack Checklist](references/checklist-fullstack.md):
- Check Tokio task safety: Are there `std::fs` calls or sync loops in async functions?
- Check lock granularity: Is a `Mutex` locked across an `.await` or around long iterations?
- Check React render trees: Is parent state triggering re-renders of heavy children without memoization?
- Check SQLite access: Are queries executed in loops? Are `WHERE`/`ORDER BY` columns indexed?

### 3. Priority Classification
Classify all identified bottlenecks strictly by impact:

- **P0 (Critical)**:
  - Freezes main/UI thread for >100ms
  - OOM risks, memory leaks, or potential deadlocks
  - Tokio runtime starvation (sync blocking on worker threads)
- **P1 (High)**:
  - Noticeable UI stutter or rendering cascades (e.g., 50+ child components re-rendering on every keystroke/token)
  - N+1 SQLite queries or missing indexes on growing tables
  - Uncompressed/unpaginated multi-megabyte IPC serialization
- **P2 (Medium / Low)**:
  - Micro-optimizations (redundant clones, small heap allocations)
  - Opportunities to use `Vec::with_capacity` or pass references instead of owned values

### 4. Provide Concrete Before/After Solutions
For each finding:
- Specify exact code location: `relative/path/to/file.ext:line`.
- Explain the precise root cause (why it degrades performance).
- Provide minimal, idiomatic **Before** and **After** code snippets.
- Verify that the fix does not introduce architectural bloat (KISS/YAGNI).

### 5. Generate Action Plan Report
Write the final audit to `.libragent/work/perf_audit_<target>_<YYYYMMDD>.md` (or present directly to user) following [references/reporting-template.md](references/reporting-template.md).

---

## Critical Rules & Guardrails

- **No Raw Cargo Execution**: NEVER execute raw `cargo test`, `cargo build`, or `cargo clippy`. These cause OOM and system freezes. If verification is needed, only use lightweight commands (`pnpm rust:check`, `pnpm rust:fmt:check`).
- **No Unauthorized Test Runs**: Static analysis and diff-based inspection are primary. Do not run heavy test suites unless explicitly directed by the user.
- **KISS / YAGNI (No Over-Engineering)**:
  - Do NOT introduce dual-ID / dual-state caching mechanisms to "save a few bytes" or "optimize lookups".
  - Do NOT build distributed-scale caching layers for a local SQLite desktop app.
- **Evidence-Based Citing**: Every bottleneck must cite specific file paths, line ranges, or measurable complexity. Never invent theoretical speedups (e.g. "will make it 300% faster") without concrete measurements.
