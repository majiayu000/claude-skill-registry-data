---
name: api-audit
description: |
  Protocol for auditing API surface coherence and type safety.
  Trigger when:
  - Evaluating API designs, interface type safety, or design elegance.
  - Prompt contains: /api-audit, API surface, API coherence, type safety.
---

# API Coherence Audit Protocol

A thorough, piecemeal framework for auditing code API surfaces. Designed to maintain agent coherence by working iteratively through the codebase with explicit human checkpoints.

> **Adversarial path anchor.** This lens is invoked on the Verification Dual's adversarial path ([rules.md](../../rules.md) §2 Invariant 1): when no deterministic evaluator can close an API-surface correctness condition, context-free agents using this protocol supply the decorrelated review. See [skills/refine/SKILL.md](../refine/SKILL.md) AUDIT §"Sibling Skills Consultation" for the wiring point.

> **Guiding Principle:** An ideal API is minimal, well-scoped, type-safe, elegantly composable, and monosemic. It leverages language features to make error states unrepresentable.

---

## Phase 0: Scope Definition

Before beginning, establish the audit scope with the user. Confirm: target language and version; type system strength; public API entry points; explicit exclusions (generated code, vendored deps); user-defined constraints (e.g., no breaking changes, no-std compatibility).

## **Checkpoint:** Present scope to user for approval before proceeding.

## Phase 1: Surface Discovery (Full Codebase Ingestion)

**Objective:** Build a complete mental model of the public API surface before any analysis.

### 1.1 Enumerate Public Surface

For each entry point, catalog:

- [ ] **Exported Types:** Structs, enums, classes, interfaces, type aliases
- [ ] **Exported Functions:** Free functions, associated functions, methods
- [ ] **Exported Constants:** Public constants, static values
- [ ] **Re-exports:** Items re-exported from internal modules
- [ ] **Traits/Interfaces:** Abstractions meant for external implementation

### 1.2 Generate Surface Map

Produce a structured inventory:

```
## Module: `crate::auth`
### Types
- `Principal` (struct) — L23-L45
- `AuthState` (enum) — L47-L62
### Functions
- `Principal::verify(&self, sig: &Signature) -> Result<()>` — L67
- `validate_token(token: &str) -> Result<Claims>` — L89
### Traits
- `Authenticator` — L12-L21
  - `fn authenticate(&self, credentials: &Credentials) -> Result<Session>`
```

**Checkpoint:** Present surface map to user. Ask:

1. Is this complete? Are there missing entry points?
2. Are there items here that should NOT be public?

---

## Phase 2: Iterative Component Audit

**Objective:** Audit each logical component systematically, one at a time.

> **Coherence Strategy:** Analyze ONE component per iteration. Present findings. Await user acknowledgment before proceeding to the next.

### Audit Dimensions

## For each component, evaluate against all dimensions. Rate each: `[PASS | WARN | FAIL]`

#### Dimension A: Minimal Surface (Encapsulation)

The API should expose only what external consumers need.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| A.1 | Internal implementation details are hidden | `pub` on helper functions; `_internal` prefixes on public items |
| A.2 | Configuration uses sensible defaults | Requiring 10 parameters when 2 would suffice |
| A.3 | No "god objects" with excessive responsibility | Single type with 50+ methods across unrelated concerns |
| A.4 | Private fields with controlled accessors where appropriate | All fields `pub` when mutation should be constrained |
**Remediation Patterns:**

- Use visibility modifiers (`pub(crate)`, `internal`, `private`)
- Builder pattern for complex construction
- Facade pattern to simplify overly complex subsystems

---

#### Dimension B: Type Safety & Error Unrepresentability

Leverage the type system to make invalid states impossible to construct.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| B.1 | Domain values use newtypes, not primitives | `user_id: String` instead of `UserId(String)` |
| B.2 | Enums are exhaustive over valid states | Magic strings like `status: "pending"` vs `Status::Pending` |
| B.3 | Result/Option used properly; no null/nil abuse | Returning `null` for "not found" vs `Option<T>` |
| B.4 | Builder/factory patterns prevent invalid construction | Partially-constructed objects allowed to exist |
| B.5 | Phantom types or typestate for protocol enforcement | State machine transitions not enforced at compile time |
| B.6 | Deserialization targets concrete types | Deserializing to `Map<String, Any>` then validating at runtime |
**Language-Specific Checks:**

- **Rust:** Proper `#[non_exhaustive]` usage; no unwrap in library code; correct `Send`/`Sync` bounds
- **Go:** Proper error wrapping; unexported fields for invariants; meaningful zero values
- **TypeScript:** Strict mode; no `any`; discriminated unions over string literals
- **Python:** Type hints on public API; @dataclass for structured data; no Dict[str, Any] leakage
  **Remediation Patterns:**
- Parse, don't validate (deserialize to concrete types)
- Newtype pattern for domain primitives
- Typestate pattern for state machines
- `#[must_use]` on Result-returning functions

---

#### Dimension C: Composability & Self-Reuse

Higher-level APIs should compose lower-level primitives, not duplicate logic.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| C.1 | Higher abstractions compose lower ones | Convenience function re-implements core logic |
| C.2 | Common patterns extracted to reusable utilities | Same validation logic in 5 different functions |
| C.3 | Trait/interface hierarchies are coherent | Trait with 20 methods when 3 would compose |
| C.4 | Extension points via composition, not inheritance | Deep inheritance hierarchies |
**Remediation Patterns:**

- Extract shared logic to internal helpers, call from public API
- Use decorator/wrapper types for cross-cutting concerns
- Prefer trait composition (`+ OtherTrait`) over monolithic traits

---

#### Dimension D: Monosemicity (One Path Per Concern)

Each concern should have exactly one canonical path through the API.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| D.1 | No redundant methods with overlapping functionality | `get()`, `fetch()`, `retrieve()` all doing the same thing |
| D.2 | Clear canonical path for common operations | 5 ways to create an instance, none obviously "correct" |
| D.3 | Deprecated paths actively marked and documented | Old API coexisting with new, neither marked deprecated |
| D.4 | No "stringly typed" APIs where enums would work | `method: "GET"` instead of `Method::Get` |
**Remediation Patterns:**

- Consolidate redundant methods; deprecate legacy paths
- Document the "happy path" prominently
- Use `#[deprecated]` or equivalent with migration guidance

---

#### Dimension E: Naming & Cognitive Load

Names should be precise, consistent, and minimize mental overhead.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| E.1 | Consistent naming conventions throughout | `getUserById` vs `fetch_user` vs `user.get` |
| E.2 | Names reflect precise semantics | `process()` instead of `validateAndTransformInput()` |
| E.3 | No abbreviations without project-wide glossary | `crnt_req_hdlr` instead of `current_request_handler` |
| E.4 | Boolean methods/fields use predicate naming | `valid` instead of `is_valid` or `has_permission` |
**Remediation Patterns:**

- Establish and document naming conventions in CONTRIBUTING.md
- Rename for precision; use refactoring tools for safe migration

---

#### Dimension F: Error Handling Coherence

Errors should be informative, typed, and recoverable where possible.
| Check | Description | Anti-Pattern |
|:------|:------------|:-------------|
| F.1 | Error types are domain-specific, not stringly-typed | `Error::Generic(String)` for everything |
| F.2 | Errors contain sufficient context for debugging | `"failed"` vs `"failed to parse config at line 42: expected integer"` |
| F.3 | Recoverable errors distinct from fatal panics | Panicking on user input validation failure |
| F.4 | Error variants map to distinct recovery paths | Single error type with no way to discriminate cause |
**Remediation Patterns:**

- Define enum error types per module/subsystem
- Use `thiserror`/`anyhow` (Rust), `errors.Is/As` (Go), custom error classes (TS/Python)
- Include structured context (file paths, line numbers, input values)

---

### Iteration Template

For each component, produce:

```
## Audit: `module::Component`
### Summary
Brief description of the component's purpose and surface.
### Findings
| Dimension | Rating | Notes |
|:----------|:-------|:------|
| A. Minimal Surface | PASS | — |
| B. Type Safety | WARN | Uses `String` for user_id; newtype recommended |
| C. Composability | PASS | — |
| D. Monosemicity | FAIL | Redundant `create` and `new` methods |
| E. Naming | PASS | — |
| F. Error Handling | WARN | Generic error type; consider domain errors |
### Recommended Changes
1. **[D.1]** Consolidate `create` and `new` into single `new` constructor
2. **[B.1]** Introduce `UserId(String)` newtype
3. **[F.1]** Define `ComponentError` enum with specific variants
### Open Questions for User
1. Is backwards compatibility required for the `create` method?
2. Should `UserId` validation happen at construction time?
```

## **Checkpoint:** Present findings for this component. Await acknowledgment before proceeding.

## Phase 3: Cross-Cutting Analysis

After completing component audits, assess systemic patterns.

### 3.1 Consistency Audit

- [ ] Naming conventions consistent across all modules
- [ ] Error handling strategy uniform
- [ ] Common patterns (e.g., builders, result types) applied uniformly
- [ ] Documentation style consistent

### 3.2 Layering Audit

- [ ] Clear dependency direction (lower layers don't import higher)
- [ ] No circular dependencies between modules
- [ ] Abstractions at appropriate levels (not too leaky, not too opaque)

### 3.3 Coherence Score

Rate the overall API coherence:
| Criterion | Score (1-5) | Notes |
|:----------|:------------|:------|
| Minimal Surface | | |
| Type Safety | | |
| Composability | | |
| Monosemicity | | |
| Naming Coherence | | |
| Error Handling | | |
| **Overall** | | |

---

## Phase 4: Remediation Plan

Synthesize findings into prioritized action items.

### Priority Levels

- **P0 (Critical):** Type safety gaps enabling invalid states; unhandled error conditions
- **P1 (High):** Encapsulation violations; significant duplication
- **P2 (Medium):** Naming inconsistencies; documentation gaps
- **P3 (Low):** Style preferences; minor redundancies

### Remediation Template

```
## Remediation Plan: [Project Name]
### P0 — Critical
1. [ ] [Module] Brief description — Links to finding
### P1 — High
1. [ ] [Module] Brief description — Links to finding
### P2 — Medium
1. [ ] [Module] Brief description — Links to finding
### P3 — Low
1. [ ] [Module] Brief description — Links to finding
```

## **Checkpoint:** Present remediation plan for user approval before any code changes.

## Appendix: Language-Specific Checklists

### Rust

- [ ] Public items have doc comments (`///`)
- [ ] `#[must_use]` on Result-returning functions
- [ ] `#[non_exhaustive]` on enums for future-proofing
- [ ] No `unwrap()`/`expect()` in library code paths
- [ ] Correct `Send`/`Sync` bounds on public types
- [ ] `pub(crate)` for internal-only items
- [ ] Feature flags documented with cfg_attr

### Go

- [ ] Exported types have doc comments
- [ ] Error types implement `Error` and support `Is`/`As`
- [ ] Unexported fields for invariant protection
- [ ] Meaningful zero values or require constructors
- [ ] Context propagation for cancellation
- [ ] Options pattern for configurable constructors

### TypeScript

- [ ] Strict mode enabled; no `any` in public API
- [ ] Discriminated unions over string literals
- [ ] Readonly types for immutable data
- [ ] Branded types for domain primitives
- [ ] Proper error class hierarchy
- [ ] Zod/io-ts for runtime validation of external input

### Python

- [ ] Type hints on all public functions and classes
- [ ] `@dataclass` or `pydantic` for structured data
- [ ] `Enum` for finite sets of values
- [ ] `__all__` defined in `__init__.py`
- [ ] No `Dict[str, Any]` in public signatures
- [ ] Docstrings follow consistent format (Google/NumPy/Sphinx)

---

## Workflow Execution Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: Scope Definition                                       │
│   → User approves scope                                         │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: Surface Discovery                                      │
│   → Full codebase ingestion                                     │
│   → Surface map generated                                       │
│   → User confirms completeness                                  │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: Iterative Component Audit                              │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │ For each component:                                      │  │
│   │   → Analyze against 6 dimensions                         │  │
│   │   → Present findings                                     │  │
│   │   → Await user acknowledgment                            │  │
│   │   → Proceed to next component                            │  │
│   └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ Phase 3: Cross-Cutting Analysis                                 │
│   → Consistency audit                                           │
│   → Layering audit                                              │
│   → Coherence scoring                                           │
├─────────────────────────────────────────────────────────────────┤
│ Phase 4: Remediation Plan                                       │
│   → Prioritized action items                                    │
│   → User approves before implementation                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Final Directive

This protocol enforces iterative human engagement to maintain agent coherence. **Never skip checkpoints.** If context becomes unclear or findings accumulate beyond what can be tracked, pause and summarize progress before continuing.
The goal is not merely to identify issues, but to cultivate a shared understanding of API quality between the auditor and the user.