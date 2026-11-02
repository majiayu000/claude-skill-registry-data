---
name: beyond-solid-principles
version: 1.0.0
description: >
  This skill should be used when the user asks to "check architecture principles",
  "audit system design", "review code for coupling", "find architecture smells", or
  "improve system-level design". Also triggers when the user mentions a principle by
  name (e.g., "check separation of concerns", "is this violating DRY?", "Law of
  Demeter", "KISS", "YAGNI", "resilience", "evolvability", "loose coupling"). Supports
  checking all ten principles at once or focusing on a single principle.
disable-model-invocation: true
---

# Beyond SOLID — System-Level Architecture Principles

Analyze source code and system architecture for violations of ten foundational design
principles that govern how modules, services, layers, and components are structured
and interact. Produce actionable findings with severity ratings, code/architecture
locations, and concrete remediation suggestions.

These principles operate at the architecture scale — modules, services, bounded
contexts, layers, APIs — complementing the class-level SOLID principles.

## Subcommands

Request a full audit or focus on a single principle:

| Command Pattern | Principle | Reference |
|----------------|-----------|-----------|
| `sw-soc` | Separation of Concerns | `references/soc.md` |
| `sw-srp-sys` | Single Responsibility (system-level) | `references/srp-sys.md` |
| `sw-dry` | Don't Repeat Yourself (DRY) | `references/dry.md` |
| `sw-demeter` | Law of Demeter / Principle of Least Knowledge | `references/demeter.md` |
| `sw-coupling` | Loose Coupling, High Cohesion | `references/coupling.md` |
| `sw-evolvability` | Build for Change (Evolvability) | `references/evolvability.md` |
| `sw-resilience` | Design for Failure / Resilience | `references/resilience.md` |
| `sw-kiss` | KISS — Keep It Simple | `references/kiss.md` |
| `sw-pola` | Principle of Least Surprise (POLA) | `references/pola.md` |
| `sw-yagni` | YAGNI at Architecture Level | `references/yagni.md` |
| `beyond-solid-principles` | All ten principles | All references |

When no subcommand is specified, default to checking all ten principles.
When a principle is mentioned by name (even without the command prefix), match it to
the appropriate subcommand.

## Workflow

### 1. Identify Target Code

Determine what code or architecture to analyze:
- When files or a directory are provided, use those.
- When a service, module, or component is referenced by name, locate it.
- When ambiguous, ask which files, directories, or services to scan.

These principles apply to any language and any architecture style — monoliths,
modular monoliths, microservices, serverless, event-driven, layered, hexagonal, etc.
Adapt the principle checks to the idioms and scale of the target system.

For smaller codebases, focus on module/package boundaries, dependency direction,
and internal layering. For distributed systems, also consider service boundaries,
API contracts, data ownership, messaging patterns, and operational resilience.

### 2. Load Principle References

Before analyzing, read the reference file(s) for the requested principle(s):

- [`references/soc.md`](references/soc.md) for Separation of Concerns
- [`references/srp-sys.md`](references/srp-sys.md) for Single Responsibility (system-level)
- [`references/dry.md`](references/dry.md) for DRY
- [`references/demeter.md`](references/demeter.md) for Law of Demeter
- [`references/coupling.md`](references/coupling.md) for Loose Coupling, High Cohesion
- [`references/evolvability.md`](references/evolvability.md) for Build for Change
- [`references/resilience.md`](references/resilience.md) for Design for Failure
- [`references/kiss.md`](references/kiss.md) for KISS
- [`references/pola.md`](references/pola.md) for Principle of Least Surprise
- [`references/yagni.md`](references/yagni.md) for YAGNI

For a full audit (`beyond-solid-principles`), read all ten.

### 3. Analyze

For each target file, module, or service boundary, apply the violation patterns from
the loaded references. Think carefully about each pattern — not every heuristic match
is a true violation. Consider context, system scale, team size, and maturity.

Key analysis dimensions:
- **Static structure**: dependency direction, import graphs, layer boundaries.
- **Change patterns**: which files/modules change together (if VCS history is available).
- **Runtime topology**: service call chains, data flow, failure propagation paths.
- **API contracts**: consistency, encapsulation, versioning, naming conventions.
- **Operational posture**: timeouts, retries, circuit breakers, health checks.

### 4. Report Findings

Present findings using this structure:

#### Per Violation

```
**[PRINCIPLE] Violation — Severity: HIGH | MEDIUM | LOW**
Location: `filename` or `service/module`, lines ~XX-YY (if applicable)
Issue: Clear description of what violates the principle and why it matters.
Suggestion: Concrete remediation approach with brief code or architecture sketch if helpful.
```

Severity guidelines:
- **HIGH**: Active maintenance pain, production risk, blocks independent evolution,
  or causes cascading failures.
- **MEDIUM**: Architecture smell that will cause problems as the system grows or
  as more teams contribute.
- **LOW**: Minor design impurity, worth noting but fine to defer.

#### Summary

After all findings, provide:
- A count table: `| Principle | HIGH | MEDIUM | LOW |`
- Top 3 priorities: which violations to fix first and why.
- Overall assessment: one paragraph on the system's structural health and
  evolvability posture.

### 5. Refactor Mode (Optional)

When a fix or refactoring is requested (e.g., "fix this", "refactor it",
"show me the clean version"), produce refactored code or an architecture proposal
that resolves the identified violations. Explain each change briefly.

## Pragmatism Guidelines

These are guidelines, not laws. Apply judgment:

- Small projects and prototypes get a lighter touch. Don't flag a weekend project
  for lacking circuit breakers or API versioning.
- Some "violations" are conscious trade-offs. When a rationale is documented (e.g.,
  in an ADR), acknowledge it rather than insisting on purity.
- Scale matters. A single-service CRUD app does not need the same architectural rigor
  as a platform serving millions of requests. Calibrate severity to context.
- Principles have productive tensions. DRY conflicts with loose coupling across service
  boundaries. KISS conflicts with resilience patterns. YAGNI conflicts with evolvability.
  Flag the tension and offer judgment, not dogma.
- Prefer actionable findings over exhaustive catalogs. Five important findings
  beat twenty trivial ones.

## Example Interaction

**User**: `sw-coupling` (with a codebase directory)

**Claude**:
1. Reads `references/coupling.md`
2. Analyzes the directory for coupling/cohesion violations
3. Reports findings with locations, severity, and suggestions
4. Provides a summary with priorities

---
From `florianbuetow/claude-code`, MIT — https://github.com/florianbuetow/claude-code
