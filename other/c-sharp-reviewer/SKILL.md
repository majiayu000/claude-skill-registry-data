---
name: c-sharp-reviewer
description: "Language- and Unity-specific code review of C# changes: correctness, GC/allocation in hot paths, async/disposal correctness, nullable handling, MonoBehaviour lifecycle misuse, SOLID, and architecture-contract adherence. Read-only — produces a verdict, edits nothing."
argument-hint: "[path-to-file-or-directory] [optional: story-path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
model: sonnet
agent: c-sharp-reviewer
---

## Phase 1: Load Target

Read the target C# file(s) in full. Read `CLAUDE.md` + `.claude/docs/coding-standards.md`.
If a story path is given, read it for acceptance criteria and the governing
architecture contract / ADR reference.

---

## Phase 2: Contract Adherence

If an architecture sketch or ADR governs this code, confirm the implementation
matches its interfaces and dependency direction. Classify deviations:
- **ARCHITECTURAL VIOLATION (BLOCKING)** — uses a rejected pattern.
- **DRIFT (WARNING)** — diverges without a forbidden pattern.

---

## Phase 3: C# / Unity Checklist

**Correctness & safety**
- [ ] No `async void` (except event handlers); `CancellationToken` honored; no unawaited Tasks.
- [ ] `IDisposable`/native handles disposed; no leaked subscriptions/coroutines.
- [ ] Nullable handling correct; Unity-object null checks use `== null`; destroyed objects guarded.

**Performance / GC**
- [ ] No allocations in hot paths (`Update`/physics/render): no LINQ, closures, boxing, string concat.
- [ ] Components cached in `Awake`; no `GetComponent`/`Find` in `Update`.
- [ ] `NonAlloc`/pooling/`Span<T>` used where appropriate.

**Unity idioms**
- [ ] `[SerializeField] private` over public; no `Resources.Load`/`FindObjectOfType` in production.
- [ ] No singletons for mutable game state; dependencies injected; tunables data-driven.

**Architecture & SOLID**
- [ ] Correct dependency direction; no new circular asmdef refs; SRP/OCP/LSP/ISP/DIP respected.
- [ ] Public APIs have XML doc comments; methods within complexity (<10) / length (<40 lines) limits.

**Testability**
- [ ] Seams exposed for tests; logic separable from MonoBehaviour lifecycle.

Optionally run analyzers if available (`dotnet build` with warnings, `dotnet format --verify-no-changes`).

---

## Phase 4: Output

```
## C# Review: [File/System]
### Contract Adherence: [MATCHES / DRIFT / VIOLATION]
### Correctness & Safety: [CLEAN / ISSUES]
### Performance & GC: [CLEAN / ISSUES]
### Unity Idioms: [CLEAN / ISSUES]
### Architecture & SOLID: [CLEAN / ISSUES]
### Testability: [TESTABLE / GAPS]
### Positive Observations
### Required Changes      (BLOCKING + REQUIRED items, with line refs)
### Suggestions
### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

This skill is read-only — it writes no files.

---

## Phase 5: Next Steps

Use `AskUserQuestion`:
- If APPROVED: `[A] /story-done`  ·  `[B] Stop here`
- If CHANGES REQUIRED: `[A] Route fixes to /c-sharp-engineer and re-review`  ·  `[B] Stop here`
- If ARCHITECTURAL VIOLATION: fix to comply with the ADR, or run `/architecture-decision` to revise it — do not create a competing ADR.
