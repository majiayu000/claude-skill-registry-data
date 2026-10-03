---
name: solidifier
description: Apply SOLID principles and design patterns to backend code with judgment and restraint. Use this skill whenever the user asks to refactor, review, clean up, restructure, or improve the design of backend code (services, APIs, domain logic, data access, handlers, jobs) — or mentions SOLID, design patterns, coupling, separation of concerns, testability, or "this code is hard to change/test." Also use when generating new backend modules that should be well-structured. Works in any backend language (Python, TypeScript/Node, Java, Go, C#, etc.). It scopes changes to specified parts of the codebase and reads a configurable rigor level so the depth of refactoring matches what the user wants.
---

This skill guides the application of SOLID principles and design patterns to backend codebases. Its job is not to maximize the number of principles and patterns visible in the code — it is to make code **easier to understand and cheaper to change**, using SOLID and patterns *only where they pay for themselves*.

The user provides backend code (a file, module, service, or a target area) and wants it improved, reviewed, or built well. They may also specify how invasive the work should be.

## Prime directive: design serves change, not the other way around

SOLID and design patterns are means, not ends. The goal is always the same: code that a competent engineer can read, reason about, test, and modify without fear. Before introducing *any* abstraction, interface, or pattern, it must earn its place by reducing real, present complexity or absorbing a real, likely-to-occur axis of change.

The most common failure mode in backend design is **over-engineering**: interfaces with a single permanent implementation, factories that wrap a single constructor, strategy hierarchies for variation that does not exist, layers of indirection that hide logic rather than clarify it. This is "design slop" and it is just as bad as tangled spaghetti — sometimes worse, because it looks principled.

Two rules that override everything else:
- **YAGNI** — Do not add extension points, interfaces, or patterns for change that has not arrived and is not concretely anticipated. Speculative generality is a defect.
- **KISS** — The simplest design that satisfies SRP and is testable wins. If a plain function or a small class is clearer than a pattern, use the plain function.

If a refactor adds more indirection than it removes complexity, **do not do it** — explain why instead.

## Workflow

1. **Read the configuration** (see `references/configuration.md`). Look for a `.solidifier.json` (or `solidifier` key in the project config) in the target area or project root. If none exists, use the defaults below and mention that the user can create one to tune behavior. The config sets the rigor level, the scope, and any principle/pattern toggles.

2. **Scope the work.** Apply changes *only* to the files, directories, or modules the user named or the config's `scope` globs cover. Do not refactor adjacent code, do not reorganize the whole project, and do not rename things outside the target unless required for the change to compile. State the scope you're operating on before making changes.

3. **Diagnose before prescribing.** Read the target code and identify *actual* design problems — name the specific SOLID violation or the specific smell, and say what concrete pain it causes (hard to test, change ripples, duplicated logic, etc.). A principle is not violated just because the code is simple. Skip code that is already fine; "already well-structured, no change needed" is a valid and valuable outcome.

4. **Apply with restraint, matched to the rigor level.** For each problem worth fixing, choose the lightest intervention that resolves it. Prefer extracting a function over a class, a class over an interface, an interface over a pattern, a known pattern over a bespoke framework. Honor the configured rigor level (below).

5. **Justify every change.** For each refactor, state in one or two sentences: which principle/pattern, what problem it fixes, and what it costs. If you introduced an abstraction, name the second concrete use case that justifies it. If you can't name one, reconsider.

6. **Preserve behavior.** Refactoring must not change observable behavior. Keep public contracts stable unless the user asked otherwise. If tests exist, they must still pass; if they don't, note which behaviors a test should pin down.

## Rigor levels (the configurable dial)

The dial controls **how invasive the work is and how high the justification bar sits** — not how many patterns to cram in. Restraint applies at every level. Default is `conservative`.

- **`advisory`** — Do not modify code. Produce a review: list violations and smells, ranked by the pain they cause, each with a concrete suggested refactor and its tradeoff. Use this for audits and learning.
- **`conservative`** (default) — Fix only unambiguous violations where the refactor clearly reduces total complexity (e.g., a class doing four unrelated jobs, a direct dependency on a concrete DB client buried in business logic). Bias strongly toward leaving working code alone. Introduce a pattern only when the absence of one is actively causing duplication or untestability *right now*.
- **`standard`** — Apply SOLID where violations cause real friction, and introduce a design pattern when a clear, named, present need exists (e.g., three payment providers behind a `switch` → Strategy). Moderate refactoring within scope. Still refuse speculative abstraction.
- **`thorough`** — Refactor the target area comprehensively toward SOLID and introduce patterns proactively where they are *defensible* — but every abstraction still requires a stated, concrete justification. Thorough means careful and complete, **not** maximalist. Even here, an interface with one permanent implementation is wrong. Warn the user if the target genuinely doesn't need this much work.

There is intentionally no "maximize patterns" level. Maximizing pattern usage is an anti-goal.

## SOLID quick reference

Full treatment with backend examples, violation smells, and the over-application smell for each is in `references/solid.md` — read it when applying or explaining SOLID.

- **S — Single Responsibility.** A module should have one reason to change. Split code that mixes concerns (validation + business rules + persistence + I/O). *Counter-smell:* anemic one-method classes and shattering cohesive logic into fragments that always change together.
- **O — Open/Closed.** Open for extension, closed for modification — add new behavior without editing stable code, usually via polymorphism. *Counter-smell:* building plugin points for variation that does not exist.
- **L — Liskov Substitution.** Subtypes must honor the base type's contract (no strengthened preconditions, no surprise exceptions, no weakened guarantees). Applies hard to repository/handler implementations behind a shared interface.
- **I — Interface Segregation.** Clients shouldn't depend on methods they don't use. Split fat "God" interfaces by consumer need. *Counter-smell:* one interface per method, exploding the type count.
- **D — Dependency Inversion.** High-level policy depends on abstractions, not concrete details; wire concretes in at the edges (DI). *Counter-smell:* an interface for everything, including types with exactly one forever-implementation.

## Design patterns

A catalog organized by category — each with intent, *use when*, and the critical **avoid when / sign of misuse** — is in `references/patterns.md`. Read it before introducing or recommending any pattern. The "avoid when" guidance is the part that prevents slop; do not skip it.

Quick selection heuristic: name the *axis of variation or the specific pain* first, then pick the lightest pattern that addresses exactly that. If you cannot name the axis of variation, you do not need a pattern yet.

## Output

- When modifying code: make the edits within scope, then give a short, plain summary — what changed, which principle/pattern, what problem it fixed, what it cost. No lecturing.
- When in `advisory` mode: a ranked list of findings, each with location, the named principle/smell, the concrete pain, a suggested fix, and its tradeoff.
- Always be honest when the right answer is "leave it alone." Recommending no change on already-sound code is a successful use of this skill.
