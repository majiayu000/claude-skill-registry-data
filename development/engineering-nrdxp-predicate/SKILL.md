---
name: engineering
description: |
  Core technical, safety, and maintainability rules for codebase edits.
  Trigger when:
  - Writing code, refactoring, modifying files, or creating unit tests.
  - Proposing commits, reviewing git history, or auditing code quality.
  - Modifying files in any programming language (e.g. *.go, *.rs, *.py, *.ts, *.js, *.c, *.cpp).
  - Prompt contains keywords: refactor, build, compile, lint, test, git, commit, rule priority, type safety, error handling, defensive programming.
---

# Engineering

## Always-On Principles

These constraints bind every code edit without skill invocation. They are the
standing SWE law promoted into the always-on conditioning layer; deviation
requires explicit justification and human approval. Detailed elaboration follows
in the [By-Moment Reference](#by-moment-reference) below.

### Root Cause — Never a Band-Aid

A fix that papers over a symptom — a compatibility shim, a workaround that lets
a broken design survive, an exception added to silence a warning — is a defect,
not a solution. The cause MUST be fixed. If the fix requires more than local
changes, HALT and discuss the scope before proceeding; do not re-architect
silently.

Compatibility hacks are forbidden. Additions beyond the stated task are
forbidden (the Cutting Imperative: do not add features, abstractions, or cleanup
not present in the task). When removing code, cut completely — compatibility
scaffolding for removed code is entropy that must later be audited for meaning.

### No Silent Failures

Every error path MUST be handled or propagated, preserving the causal chain.
Error messages MUST state **what** failed, **why**, and **where** — opaque
messages such as "invalid input" are forbidden. Library code MUST NOT panic; it
MUST return `Result`/`Option` to the caller. Application entry points convert
errors to exit codes with clear messages. Secrets, tokens, and PII MUST NOT
appear in logs.

### Validate at Boundaries; Trust Internal Invariants

All external inputs MUST be validated at system entry points (user input, API
responses, file contents, IPC). Internal call sites MUST NOT add defensive
guards against conditions the type system or framework invariants already rule
out — that is unnecessary error handling that obscures where the real boundaries
are. Validate the perimeter; trust what the perimeter enforced.

### Strong Typing — No Escape Hatches

Use the type system to enforce invariants. `any`, `interface{}`, or their
language equivalents MUST NOT be used unless genuinely necessary; when used, the
specific reason MUST be documented inline. Library code MUST NOT panic.

### Discrepancy Resolution — Never Silent

When specification, tests, and code disagree, HALT immediately. Present the
discrepancy with evidence from each source and propose a resolution. Do not
silently pick a winner; do not proceed until the conflict is resolved.

### Trajectory Freeze Conditions

Stop generating and query for boundary updates whenever:

- Goal or context is contradictory or missing (uncertainty > 0.0).
- Environment state diverges from planned invariants (expected files missing,
  API mismatch).
- Verification tools fail to converge after the corrective loop.
- Multiple valid paths exist with no constraint selecting among them.

Generating under unvalidated assumptions is forbidden. Guessing a corrective
edit from ambiguous feedback is forbidden. Halting to receive parameters is
faster than correcting trajectory drift.

---

## By-Moment Reference

The sections below elaborate *how* to apply the always-on principles in
practice: clarification protocols, uncertainty thresholds, language-specific
rules, and conventions. Load this reference when actively writing or reviewing
code.

---

### Clarification Triggers

Invoke clarification under these conditions:

1. **Undefined Scope:** The request could range from trivial to architecturally significant.
2. **Missing Acceptance Criteria:** There is no clear definition of "done."
3. **Implicit Assumptions:** The request relies on unstated assumptions about the codebase or domain.
4. **Conflicting Constraints:** The request appears to conflict with an existing rule or prior decision.

### Uncertainty Thresholds

| Uncertainty Level | Criteria                                              | Action                                                                          |
| :---------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------ |
| **None (0.0)**    | Clear requirement, established pattern, no ambiguity. | Proceed. If the change is API-breaking, still confirm.                          |
| **Low (0.1-0.3)** | Explicit constraints with minor implementation ambiguities. | Present implementation path and query for targeted constraint boundaries before proceeding. |
| **High (>0.3)**   | Multiple valid interpretations, conflicting constraints. | Halt sequence walk and request specific boundary parameter corrections.           |

When in doubt, err toward halting. Wasted clarification is cheaper than trajectory drift.

> [!NOTE]
> This table applies to general execution. In C.O.R.E. planning, the
> ambiguity gate uses a qualitative `OBSTACLES` list: the list must be
> empty before the sequence may advance from CLARIFY to PLAN. There is
> no numeric uncertainty field in the C.O.R.E. grammar.

---

### Rule 0: Context Acquisition (The "Read-First" Rule)

Before writing code, understand the existing landscape:

1. **Outline First:** Read file outlines to understand structure.
2. **Targeted Read:** Read specific functions, modules, or types relevant to the change.
3. **Contextual Files:** Read related files (tests, interfaces, callers) to understand usage patterns.
4. **Full Read:** Only for small files (<500 lines) or major refactors.

**Pattern Matching:** Mimic existing directory structure and coding style strictly. Do not introduce foreign idioms. When uncertain, search for prior art in the repo (e.g., "How are errors handled elsewhere?") and follow established patterns.

> **Tip:** If MCP tools are available, use them first for structural insight before reading individual files.

### Rule 1: Root Cause Analysis

Never apply band-aid fixes. Analyze root causes; re-architect if the foundation is flawed. If a fix requires more than local changes, stop and discuss the broader implications.

### Rule 2: Implementation Scope

- **Completeness:** Never leave core logic as `// TODO` within the scope of the current task.
- **Out-of-Scope Stubs:** Must return a clear error and be tracked in the plan.
- **Scope Creep:** If implementation reveals additional work, stop and renegotiate scope.

### Rule 3: API Stability (Version-Aware)

Check the project version in `Cargo.toml`, `package.json`, `go.mod`, or equivalent manifest:

- **Pre-1.0 (`0.x.x`):** Stability is secondary. Prefer correct design over backward compatibility.
- **Post-1.0 (`1.0.0+`):** Breaking changes to public APIs are forbidden without explicit user approval. Present trade-offs and await confirmation.

### Rule 4: The "Stop-and-Ask" Protocol

- **Ambiguity Intolerance:** If a requirement can be interpreted in multiple ways, stop and ask.
- **Architectural Crossroads:** If a solution requires a significant new dependency, a major refactor, or a choice between valid approaches, propose options and await confirmation.

### Rule 5: Discrepancy Resolution

When specification, tests, and code disagree:

1. **Alert immediately.** Do not silently pick a winner.
2. **Present the discrepancy** with evidence from each source.
3. **Propose a resolution**, but await confirmation. The spec is often authoritative, but sometimes the spec itself is ambiguous or wrong.

This is a collaborative investigation, not a unilateral decision.

### Rule 6: Scope Negotiation (Minimal Viable Slice)

Before beginning any non-trivial task:

1. State your understanding of the scope.
2. If ambiguous, propose a **Minimal Viable Slice (MVS)** — the smallest unit of work that delivers demonstrable value.
3. Await confirmation before proceeding.

### Rule 7: Testing Strategy

- **Concurrent Testing:** Tests are written with implementation, not after.
- **Robust-Testing Guidelines:** Concurrently design tests adhering to [robust-testing](../robust-testing/SKILL.md). Do not rely solely on simple, example-based happy-path unit tests, as they lead to self-deception in AI-generated code.
- **Test Integrity:** Never modify a valid test to force a passing result. Similarly, don't revert a valid bug-fix to satisfy a malformed test. Tests should represent semantic correctness, not just a check-mark.
- **Specification Traceability & Refinement:** If a specification or model exists, tests MUST trace directly to its constraints. The test suite itself must be iteratively refined toward coherence (assuring proper baseline failure and complete input domain coverage).
- **Domain-Specific Verification:** Select appropriate testing methods (Property-Based Testing for algebraic domains, Fuzzing for security/parsing boundaries, Metamorphic Testing for oracle-less systems, and Integration/E2E testing for multi-module integration) to ensure high-fidelity verification gates.
- **Descriptive Naming:** Test names describe the scenario and expected outcome (e.g., `test_login_fails_with_invalid_credentials`).
- **Meaningful Coverage:** Focus on business logic, edge cases, error handling, and multi-component E2E integration paths rather than isolated mocks.
- **Cross-Implementation Sanity:** For protocols with multiple implementations, maintain language-agnostic test vectors.

### Rule 8: Maintainability & Clean Code

- **SOLID Principles:** Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
- **Modularity:** Refactor functions exceeding ~50 lines or with deep nesting.
- **Strong Typing:** Use the type system to enforce invariants. Avoid `any` / `interface{}` unless necessary.
- **Dependency Minimalism:** Prefer standard library solutions.
- **Concurrency Awareness:** When working with concurrent/async code, explicitly consider shared state, race conditions, deadlocks, and cancellation semantics.

#### 8.1. Spacetime of Code

Code goes wrong along two axes, not one. A single-lens review audits half the code.

- **Structural simplicity** (spatial axis): Are independent concerns interleaved? Two ideas braided into one module, one function, or one match arm so that touching one forces you to touch the other = complected. The fix is separation. The dual — one domain concept shattered across multiple locations whose coherence depends on an unenforced rule — is fragmentation. The fix is reunification. See `/hickey` for the full evaluation procedure.

- **Volatility alignment** (temporal axis): Do boundaries encapsulate axes of change, or do they just group related functionality? Code that *works* today but places a decision in the wrong layer — where it will rev on a different clock than its neighbors — is a volatility time-bomb. Functional decomposition maximizes the blast radius of change; volatility-based decomposition contains it. See `/lowy` for the full evaluation procedure.

When reviewing architectural decisions, run both lenses. Findings will predominantly be single-axis. When both lenses converge on the same location, the signal is particularly acute.

### Rule 9: Security, Reliability & Observability

#### Input Validation

Validate external inputs at system boundaries. Never trust user input, API responses, or file contents without validation. Fail fast with clear error messages.

#### Error Handling

- **No Silent Failures:** All errors must be handled or propagated.
- **Error Chaining:** Preserve the causal chain (`thiserror`, `fmt.Errorf("%w", ...)`).
- **Error Quality:** Messages must include **what** failed, **why**, and **where** (the input/value that caused it). No opaque errors like "invalid input."

#### Panic Policy

| Context               | `panic`/`unwrap` Allowed? | Guidance                                          |
| :-------------------- | :------------------------ | :------------------------------------------------ |
| **Library Code**      | ❌ No                     | Return `Result`/`Option`. Never panic.            |
| **Application Entry** | ✅ Limited                | Convert `Result` to exit code with clear message. |
| **Test Code**         | ✅ Yes                    | Panic = test failure; acceptable for brevity.     |
| **Initialization**    | ✅ If Unrecoverable       | Use `expect("clear message")`.                    |

#### Logging & Output

**Libraries:** No direct output. Return errors/results to the caller.

**CLI Applications:**

- **stdout:** Reserved for requested program output (pipeable, parseable).
- **stderr:** Reserved for diagnostics (errors, warnings, progress).

**Web/Server Applications:**

- Use structured logging (JSON) with severity levels.
- Never log secrets, tokens, or PII.

### Rule 10: Documentation

Update comments and documentation **immediately** when logic changes. Stale documentation is a bug.

### Rule 11: Git Hygiene & Atomic Commits

Git hygiene matters to engineering for the same reason type safety does: a
clean, human-reviewable history is the durable interface between the work and
the reviewer who must reconstruct its reasoning from `git log` alone. The rules
that produce that history are not restated here — they have a single authority:

- **Commit boundaries and messages:** atomic one-change-per-commit discipline,
  the spaghetti-diff anti-pattern, and message format follow
  [commit-hygiene](../commit-hygiene/SKILL.md).
- **The commit gate and hard rails:** when an agent may commit at all (the
  closed-loop verification and authorization that gate every commit), and the
  absolute prohibitions on `git push` and history rewriting, are the
  [Commit Gate in rules.md](../../rules.md#3-the-commit-gate).

Engineering's only addition: a diff that compiles and passes tests but smears
several logical changes together is still a defect by this skill's standards,
not merely a hygiene nit. Atomicity is part of production-grade correctness, not
a separable formality.

### Rule 12: Plan & Task Tracking

For multi-step work:

1. Reference an implementation plan and task list.
2. Check off work as you go.
3. Add changes **additively** — do not destructively mutate the plan's history.

---

## Failure Recovery

When a mistake is discovered or you find yourself confused:

1. **Stop.** Do not continue down an uncertain path.
2. **Acknowledge explicitly.** Do not silently correct.
3. **Analyze:** Consider where you made a bad assumption or wrong generalization.
4. **Query for targeted clarification** to locate the root cause.
5. **Propose a correction** with an explicit uncertainty level (None/Low/High) and justification for that level.

---

## Upstream Modification

When modifying an upstream dependency appears to be the correct solution:

1. **Alert explicitly.** Do not assume control over the upstream.
2. Propose the upstream change and its rationale.
3. If approved, use separate commits for upstream vs. downstream changes.

---

## Rule Priority

When rules appear to conflict, use this hierarchy as a **guideline**, but remain context-aware:

1. **Security & Correctness** — Non-negotiable.
2. **Explicit User Decision** — If the user has stated a preference, it supersedes defaults.
3. **API Stability** — Per version-awareness rules above.
4. **Maintainability** — Prefer clean solutions over expedient ones.
5. **Performance** — Optimize only when measurably necessary. Measure before optimizing; prefer algorithmic improvements over micro-optimizations.
