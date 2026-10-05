---
name: code-quality
description: >
  Deep code quality analysis: performance (Big-O, hot paths, resource management),
  security (injection, secrets, auth, input validation), testability (coverage gaps,
  untestable design, DI), architecture (SOLID, coupling, abstraction leaks, layering).
  Language-agnostic with language-specific patterns from references. Trigger on:
  "code quality", "performance audit", "security review", "OWASP", "SOLID", "coupling",
  "testability", "technical debt", "code smell", "architecture review", "Big-O",
  "complexity analysis", "hot path", "memory leak", "injection", "vulnerability",
  "dependency injection", "clean architecture", "is this code good", or "can this be
  better". Also triggers on escalation from code-consistency quality triage.
---

# Code Quality Skill

Deep analysis of code quality across four domains. Works alongside `code-consistency`
which handles surface-level triage; this skill goes deep.

---

## Domains

| Domain | Reference | Focus |
|---|---|---|
| Performance | `references/performance.md` | Algorithmic complexity, resource management, concurrency |
| Security | `references/security.md` | Injection, auth, secrets, input validation, attack surface |
| Testability | `references/testability.md` | Design for testing, coverage strategy, dependency management |
| Architecture | `references/architecture.md` | SOLID, coupling/cohesion, layering, abstraction quality |

---

## Workflow

### Step 1 — Scope the Analysis
Determine which domain(s) the user needs. If unspecified, do a quick scan across
all four and focus on the domain(s) with the most findings.

| Trigger | Domain(s) to load |
|---|---|
| "Is this fast enough?" / "optimize" / "slow" | Performance |
| "Is this secure?" / "vulnerability" / "audit" | Security |
| "How do I test this?" / "hard to mock" / "coverage" | Testability |
| "Is this well-designed?" / "refactor" / "clean up" | Architecture |
| "Review this code" / "is this good?" / "can this be better" | All four (quick scan) |
| Escalation from code-consistency quality triage | Flagged domain(s) |

### Step 2 — Load Reference Files
Read the reference file(s) for the relevant domain(s) before analysis.

### Step 3 — Analyze
Apply the domain-specific checklists and patterns from the reference files.
Always consider:
- **Context:** Library vs application, hot path vs cold path, prototype vs production
- **Language:** Apply language-specific patterns where they exist
- **Trade-offs:** Every suggestion has a cost. Name it explicitly.

### Step 4 — Report

#### Quick Scan Report (all four domains)
When scanning broadly, output a summary table:

```
| Domain        | Grade | Critical | Suggested | Notes                    |
|---------------|-------|----------|-----------|--------------------------|
| Performance   | B     | 1        | 3         | O(n²) in event loop      |
| Security      | A-    | 0        | 2         | Missing rate limiting     |
| Testability   | C     | 2        | 4         | God class, hidden deps    |
| Architecture  | B+    | 0        | 3         | Minor SRP violations      |
```

Then detail the critical findings. Suggested findings go in a collapsible section
or follow-up if the user wants them.

#### Deep Dive Report (single domain)
When analyzing one domain deeply:
1. **Executive summary** — 2-3 sentences on overall quality
2. **Critical findings** — numbered, with code references and fix examples
3. **Suggested improvements** — grouped by impact
4. **Trade-off analysis** — what you'd gain and lose from each suggestion
5. **Recommended next steps** — prioritized action list

### Grading Scale

| Grade | Meaning |
|---|---|
| A | Production-quality. Minor style suggestions only. |
| B | Good. A few real issues but fundamentally sound. |
| C | Functional but concerning. Multiple issues that will compound. |
| D | Significant problems. Refactoring recommended before shipping. |
| F | Dangerous. Critical issues (security holes, data loss risk, severe perf). |

Use +/- modifiers. Grade relative to the stated context (prototype gets more
lenient grading than production code).

---

## Severity Levels

Same as code-consistency for interoperability:

| Level | Label | Meaning |
|---|---|---|
| 🔴 | **CRITICAL** | Must fix. Bug risk, security hole, or severe performance issue. |
| 🟡 | **SUGGEST** | Should fix. Real improvement but not blocking. |
| 🔵 | **NOTE** | Informational. Context or trade-off acknowledgment. |

---

## Cross-Domain Patterns

These apply across all four domains:

- **Dead code:** Unreachable branches, unused imports, commented-out code blocks
- **Complexity:** Cyclomatic complexity >10 in a single function, nesting >3 levels
- **Duplication:** Same logic in 3+ places without abstraction
- **Naming/intent mismatch:** Function name promises one thing, implementation does another
- **Missing documentation:** Public API without doc comments, complex algorithms without
  explanation, non-obvious business rules without context

---

## Reference Files

Read before deep-diving into a domain:

- **`references/performance.md`** — Complexity analysis, memory/allocation patterns,
  concurrency, I/O optimization, profiling strategies
- **`references/security.md`** — OWASP patterns, injection prevention, auth/authz,
  secrets management, input validation, supply chain
- **`references/testability.md`** — Dependency injection, seam identification, mock
  strategies, coverage analysis, test pyramid, design-for-test patterns
- **`references/architecture.md`** — SOLID deep-dive, coupling metrics, layering
  patterns, abstraction quality, module boundaries, technical debt indicators
