---
name: simplify-java
description: Use when Java / Spring Boot code works but is hard to follow. Clarify branches, names, and duplication without changing behavior. Understand why the code exists before deciding how to simplify it.
metadata:
  language: en
  translation_of: simplify-java-cn
  version: 0.2.1
---

# Java Code Simplification

Inspiration: [Addy Osmani](https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification).

## Overview

Reduce complexity while preserving behavior exactly. The goal is not fewer lines, but code that is easier to read, understand, modify, and debug.

Every simplification should answer: would a new teammate understand this code faster than before?

## When to Use

- Functionality works and tests pass, but the implementation is more complex than necessary.
- Code review identifies readability or complexity problems.
- There is deep nesting, a long method, or unclear naming.
- Cleaning up code written under time pressure.
- Consolidating scattered logic that belongs to the same responsibility.
- Merged changes introduced duplication or inconsistency.

When not to use:

- Code is already clear; do not change it merely to simplify.
- Behavior is not yet understood; gather context first.
- A simpler implementation would cause a known, unacceptable performance regression.
- The module will be rewritten entirely; do not clean up code about to be deleted.

## The Five Principles

### 1. Preserve Behavior Exactly

Change how the code expresses its work, not what it does.

Preserve inputs, outputs, side effects, error behavior, and edge cases.
Caller-dependent ordering, mutability, serialization, and framework behavior are also part of the contract.

Before every change, check:

- Does the same input produce the same result?
- Is error behavior unchanged?
- Are side effects and necessary execution order preserved?
- Do existing behavioral tests still pass?

Do not make a simplification when equivalence cannot be established.
Report defects if found, but do not mix behavior fixes into refactoring.

### 2. Follow Project Conventions

Simplification should make code fit the project, not introduce external preferences.

Before changing code:

1. Read applicable AGENTS.md, CLAUDE.md, and project conventions.
2. Study how neighboring code handles similar problems.
3. Confirm the actual Java release and Spring Boot version.
4. Follow the project's package structure, naming, exception handling, null conventions,
   bean wiring, and checking tools.

Do not create churn for personal style, upgrade dependencies, or enable preview features as part of simplification.

### 3. Prefer Clarity Over Cleverness

Prefer explicit expression when compact code requires a mental pause to decipher.

Clarity does not mean expanding everything into more statements. For existing mutually exclusive states,
an exhaustive switch can be clearer than nested ternaries.

Use existing types and preserve null handling, branch priority, fallback results, and exceptions.
Evaluate data-model changes separately.

### 4. Maintain Balance

Simplification can go too far:

- **Aggressive inlining:** Removing a helper that names a business concept can make the call site harder to read.
- **Combining unrelated logic:** Turning two simple methods into one complex method is not simplification.
- **Removing useful abstractions:** Some boundaries support replacement, testing, or framework responsibilities.
- **Optimizing for line count:** Compact expression can increase comprehension cost.

Confirm responsibility before extracting or deleting structure.
Similar-looking code does not necessarily represent the same business rule.

Preserve real seams: places where dependencies can be replaced without rewriting consumers.
An existing injection point may suffice; do not add Java interfaces merely for layering.

Preserve deep modules: simple contracts that encapsulate complex implementations.
If deleting a module spreads internal details across callers, its encapsulation still has value.

Use these judgments to support the current simplification, not to launch architecture redesign.

### 5. Scope to What Changed

Prioritize code specified by the user; otherwise default to recently changed code.

Avoid drive-by refactoring of unrelated code.
Unbounded cleanup adds review noise and regression risk.

## The Simplification Process

### Step 1: Understand Before Touching

Understand why a structure exists before removing it.

Answer:

- What is this code's responsibility?
- What calls it, and what does it call?
- What are the edge cases and error paths?
- Which tests define expected behavior?
- Are there performance, framework, or historical compatibility reasons?
- When necessary, can git blame and commit history explain the reason?

If you cannot answer, read more relevant context first.

When only a snippet is available, state what can be established.
Do not invent project conventions, callers, or verification results.

### Step 2: Identify Simplification Opportunities

These are inspection signals, not mandatory change thresholds.

**Structural complexity**

| Pattern | Signal | Possible simplification |
| --- | --- | --- |
| Deep nesting | Control flow is hard to follow | Guard clauses or named helpers |
| Long method | Contains multiple independent intentions | Split by responsibility, not line count |
| Nested ternaries | Branch priority is hard to see | if/else or an appropriate switch |
| Boolean parameter strings | Caller intent is unclear | Consider named methods or existing enums after checking caller contracts |
| Repeated conditions | One decision is scattered | Extract a named predicate within the same responsibility |

**Naming and readability**

| Pattern | Signal | Possible simplification |
| --- | --- | --- |
| Generic names | Names do not explain contents | Use specific domain names |
| Unnecessary abbreviations | Reading requires decoding | Use full words while retaining universal abbreviations |
| Misleading names | Names hide side effects | Reflect actual behavior |
| Comments explaining what | Repeat clear code | Remove redundant comments |
| Comments explaining why | Record constraints and tradeoffs | Keep them |

**Redundancy**

| Pattern | Signal | Possible simplification |
| --- | --- | --- |
| Duplicate logic | Multiple implementations of one rule | Extract after confirming shared responsibility |
| Dead code | Unreachable branches, unused variables, old commented code | Remove after confirming it is truly unused |
| Valueless wrappers | Forward without a contract or runtime responsibility | Inline or call directly |
| Over-engineering | Layered factories or strategies without actual use | Replace with a direct expression meeting current needs |
| Redundant casts | A cast appears unnecessary | Remove only if overload resolution and runtime checks stay unchanged |

### Step 3: Apply Changes Incrementally

Complete one independently understandable and verifiable simplification at a time.

1. Run relevant tests to establish a baseline.
2. Make the smallest change.
3. Run corresponding tests and checks.
4. Continue if they pass; otherwise undo this change or reconsider its cause.

If evidence is insufficient, first add characterization tests.
Confirm that the original and changed implementations satisfy the same behavioral expectations.

Test setup may change with internal structure.
Do not change expectations, weaken assertions, or skip failing cases to make refactoring pass.

Separate simplification from new features and bug fixes.
Use IDE refactoring or AST tools for large mechanical changes where useful,
but still review diffs and verify results.

### Step 4: Verify the Overall Result

Compare before and after:

- Is the result easier to understand?
- Were patterns introduced that conflict with project conventions?
- Was complexity transferred to callers?
- Is the diff focused, clear, and reviewable?

Undo simplification if the result is harder to understand or maintain.
Not every attempt is worth keeping.

## Language and Framework Guidance

### Java 21

Use stable features supported by the project's actual version, not newer syntax for its own sake.

- **Pattern matching and switch:** Can reduce repeated checks and casts,
  but preserve null handling, branch priority, guards, fallback results, and exceptions.
- **Record patterns:** Can reduce destructuring boilerplate,
  but check nested nulls, accessor calls, and exception behavior.
- **Records:** Not a mechanical replacement for ordinary classes.
  Check public access, equality, mutability, construction, and framework contracts before conversion.
- **Collections:** Preserve order, empty-collection behavior, mutability, and aliasing.
  A reversed() view is not an independent copy.
- **Stream and Optional:** Do not mechanically replace loops or conditions.
  Preserve evaluation timing, short-circuiting, side effects, and result-collection semantics;
  orElse and orElseGet are not automatically equivalent.

Virtual threads, parallelization, and asynchronous execution can change capacity, timing, and consistency.
Do not use them as default simplification techniques.

### Spring Boot 3 / 4

Check the project’s exact versions and dependencies before choosing an approach.
Do not carry defaults, package names, or wiring assumptions from one version to another; handle upgrades separately.
The same method body does not necessarily mean the framework behaves the same way.

- **Proxies:** Before moving or inlining methods, check transactions, rollback, authorization,
  validation, caching, and asynchronous interception. Proxy calls and self-invocation differ.
- **Wiring:** Before removing beans, dependencies, or configuration, check conditional wiring,
  auto-configuration, and runtime uses. No explicit reference does not mean no use.
- **External contracts:** Preserve HTTP statuses, exception mapping, serialization,
  client configuration, and persistence behavior. Confirm the mapper and clients actually used.
- **Validation:** Non-null annotations alone do not prove runtime checks redundant.
  Do not hide invalid input with defaults or apply a blanket ban on null.

When touching these boundaries, use tests covering actual wiring behavior.
Testing method bodies alone may miss regressions.

### High-Risk Changes

For money, sensitive data, shared state, or cross-system operations, one successful run is not enough.
Check only the guarantees this change may affect:

- **Did the meaning change?** Preserve business rules and the meaning of amounts, time, data, and states.
- **Are the boundaries intact?** Preserve identity, authorization, and data isolation; do not let implementation details or sensitive information cross existing boundaries.
- **What happens after failure?** Existing consistency, idempotency, and recovery guarantees must still hold under concurrency, retries, interruption, and unknown outcomes.
- **Will it hold under load?** Preserve capacity, resource lifecycles, and degradation constraints; do not turn a local simplification into a systemic risk.
- **Can versions coexist and events be traced?** Consider historical data, external consumers, and mixed versions. Preserve auditing and monitoring; rolling back code cannot undo business effects that already occurred.

Identify what provides each guarantee and how the change could break it, then choose scenarios that test it.
If a guarantee depends on configuration or external systems, follow the call path to establish it. When uncertain, keep the original.

## Common Rationalizations

| Rationalization | Judgment |
| --- | --- |
| Working code needs no changes | Hard-to-read code merits improvement; clear code can stay |
| Fewer lines are simpler | Simplicity depends on comprehension cost |
| I will clean up nearby code too | Unrelated changes add noise and risk |
| Types explain everything | Types do not fully express intent and side effects |
| This abstraction may be useful later | Justify value with current uses, not hypothetical needs |
| The original author must have had a reason | Investigate the reason, then decide whether it still applies |
| Refactoring while adding a feature saves time | Separate changes for easier verification and rollback |

## Red Flags

- Behavioral expectations must change for the modification to pass tests.
- Code is shorter but requires more navigation or framework knowledge.
- Error handling, security controls, or necessary validation are removed for neatness.
- Abstractions, configuration, or dependencies are deleted before their purpose is understood.
- Feature, migration, or execution-model changes are presented as simplification.
- Multiple changes are bundled without independent verification.
- Scope expands without being asked.

## Verification

After completing a pass, confirm:

- [ ] Behavioral expectations are unchanged, and relevant tests actually ran and passed.
- [ ] The build and existing project checks pass with no new issues.
- [ ] The diff is reviewable and contains no unrelated changes.
- [ ] Error handling and affected framework, data, and external contracts remain intact.
- [ ] Comprehension improves concretely without transferring complexity or adding valueless abstractions.
- [ ] Unperformed checks and unconfirmed behavior were explicitly reported.

When touching security boundaries, consult the relevant sections by topic
and confirm that simplification does not weaken applicable controls:

- [Oracle Secure Coding Guidelines for Java SE](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

Explain applicable guidance and code facts; links do not substitute for checking.
If sources cannot be accessed, report that they were not checked. Do not expand into a full security audit.

For performance-sensitive paths, examine complexity, query or remote-call counts,
allocations, and resource use. Compare under representative loads when necessary,
using project targets to judge acceptability.
Ordinary local changes do not require benchmarks, and shorter code does not prove greater speed.

Briefly report changes, simplification reasons, verification results, and limitations.
Having no changes worth retaining can also be the correct result.
