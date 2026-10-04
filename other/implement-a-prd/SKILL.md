---
name: implement-a-prd
description: Implement a PRD with principal-engineer-grade code quality. Discovers project linting/formatting/type rules, enforces SOLID/DRY/GoF patterns, and produces code that passes lint, type check, and formatting on first commit. Use when user has a PRD, spec, or issue and wants production implementation - not a prototype.
---

# Implement PRD

This skill takes a PRD (or spec, or issue, or detailed feature description) and produces production-grade implementation. The output must read like it was written by a principal engineer with 20 years of experience - not an LLM, not a junior, not a "good enough" mid-level.

You may skip steps if the project context is already known or if the user explicitly tells you to.

---

## Phase 0: Toolchain Discovery

Before writing a single line of code, you MUST understand the project's quality gates. These are non-negotiable constraints, not suggestions.

### 0.1 - Detect the Language and Runtime

Scan the project root and common config locations:

- `package.json`, `tsconfig.json`, `deno.json` -> TypeScript/JavaScript
- `pyproject.toml`, `setup.py`, `setup.cfg`, `ruff.toml` -> Python
- `go.mod` -> Go
- `Cargo.toml` -> Rust
- `*.csproj`, `*.sln`, `Directory.Build.props` -> C#/.NET
- `pom.xml`, `build.gradle`, `build.gradle.kts` -> Java/Kotlin
- `Package.swift` -> Swift

### 0.2 - Extract Lint Rules (READ THEM, DON'T ASSUME)

Find and READ the actual config files. Do not assume defaults.

**TypeScript/JavaScript:**
- `.eslintrc.*`, `eslint.config.*` (flat config), `.eslintignore`
- `biome.json`, `biome.jsonc`
- Read the `rules` object. Note every rule set to `error`. Those are the hard gates.
- Check for plugin-specific rules: `@typescript-eslint/*`, `import/*`, `react/*`, `react-hooks/*`, `jsx-a11y/*`
- Check `tsconfig.json` for `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`, `noFallthroughCasesInSwitch`

**Python:**
- `ruff.toml`, `pyproject.toml [tool.ruff]`, `pyproject.toml [tool.pylint]`
- `.flake8`, `setup.cfg [flake8]`
- `mypy.ini`, `pyproject.toml [tool.mypy]` - check `strict`, `disallow_untyped_defs`, `disallow_any_generics`
- `pyright` config in `pyrightconfig.json` or `pyproject.toml`

**Go:**
- `golangci-lint` config: `.golangci.yml`, `.golangci.yaml`
- Check enabled linters: `govet`, `staticcheck`, `errcheck`, `gosec`, `exhaustive`

**Rust:**
- `clippy.toml`, `#![deny(clippy::all)]` directives in `lib.rs`/`main.rs`

**C#/.NET:**
- `.editorconfig` rules, `Directory.Build.props` analyzer settings
- `<TreatWarningsAsErrors>`, `<Nullable>enable</Nullable>`, `<WarningLevel>`

### 0.3 - Extract Formatting Rules

Find and READ:
- `.prettierrc*`, `.prettierignore` -> Prettier config
- `.editorconfig` -> universal editor config
- `biome.json` formatter section
- `rustfmt.toml`
- `gofmt`/`goimports` (Go is opinionated - follow it)
- `black`, `ruff format` config sections
- `csharpier`, `.editorconfig` for C#

Note: tabs vs spaces, line length, trailing commas, quote style, semicolons. These are not opinions during implementation - they are laws.

### 0.4 - Check for Pre-commit Hooks and CI Gates

- `.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- Look for what CI actually runs: lint, type-check, test, build. Your code must survive all of these.

### 0.5 - Study Existing Patterns in the Codebase

Before implementing anything new, spend time reading existing code. Specifically:

- How are modules structured? Barrel files? Index re-exports? Flat?
- How are errors handled? Custom error classes? Result types? Try-catch patterns?
- How are dependencies injected? Constructor injection? Module-level? IoC container?
- How is state managed? What ORM/data layer? Repository pattern? Direct queries?
- How are interfaces/types organized? Co-located? Centralized? Per-feature?
- What naming conventions are used? `camelCase`, `snake_case`, `PascalCase` for what?
- How are async operations handled? Promises? Observables? Channels? Async/await?
- What test framework is in use? How are tests structured? Where do they live?

**CRITICAL: Match existing patterns. Do not introduce a new pattern unless the PRD explicitly calls for it or the existing pattern is fundamentally broken. Consistency across a codebase beats theoretical perfection in one file.**

---

## Phase 1: PRD Comprehension

### 1.1 - Read the PRD in Full

Read every section. If the PRD references other documents, issues, or specs, read those too.

### 1.2 - Identify the Scope Boundary

List explicitly:
- What you WILL build
- What you WILL NOT build
- What already exists that you will modify
- What already exists that you must NOT modify (shared interfaces, public APIs with consumers)

### 1.3 - Identify the Risk Surface

Before writing code, identify:
- Which changes touch shared/public interfaces? These need the most care.
- Which changes touch data persistence or schema? These are irreversible in production.
- Which changes have concurrency implications? Race conditions, deadlocks, starvation.
- Which changes affect performance on the critical path?

Present this risk assessment to the user. Get explicit confirmation before proceeding.

---

## Phase 2: Architecture and Design

### 2.1 - Module Decomposition

Break the implementation into modules. For each module:
- Define the public interface (what callers see)
- Define the internal complexity it hides
- Identify its dependencies (what it needs from other modules)

**Deep modules over shallow modules.** A class with 3 public methods that hides 500 lines of complexity is better than 10 classes with 2 methods each that just delegate to each other.

### 2.2 - Apply Design Principles (Not Dogmatically)

These are thinking tools, not religion. Apply them when they reduce complexity. Ignore them when they add it.

**SOLID:**
- **S** - Single Responsibility: One reason to change. Not "one thing" - one *axis of change*.
- **O** - Open/Closed: Extend behavior through composition or polymorphism, not by editing existing switch statements. But if a switch statement with 3 cases is the clearest solution, use it.
- **L** - Liskov Substitution: Subtypes must honor the contracts of their parent types. No surprises.
- **I** - Interface Segregation: Don't force consumers to depend on methods they don't call. But don't fragment a cohesive interface into 12 single-method interfaces either.
- **D** - Dependency Inversion: Depend on abstractions for boundaries that matter (I/O, external services, things you'd mock in tests). Don't create an interface for every class - that's cargo culting.

**DRY - applied correctly:**
- DRY means "Every piece of *knowledge* must have a single, unambiguous, authoritative representation."
- DRY does NOT mean "never repeat code." Two functions with identical code that change for different reasons are NOT duplication - they are coincidence. Merging them creates coupling.
- The wrong abstraction is far worse than duplicated code. If you can't name the abstraction clearly, you probably shouldn't extract it.

**GoF Patterns - use when the problem fits:**
- Strategy: When you have multiple algorithms for the same operation and need to swap at runtime.
- Observer/Pub-Sub: When producers and consumers should be decoupled. But if there's one producer and one consumer, just call the function.
- Factory: When construction logic is complex or varies by context. Not for creating simple objects.
- Adapter: When you need to bridge between two incompatible interfaces you don't control.
- Decorator: When you need to add behavior to objects without modifying their class.
- Repository: When you need to abstract data access. But don't put a repository in front of a simple key-value lookup.
- Do NOT use a pattern just because you can identify where it would fit. Use it because the code is actively worse without it.

**From Knuth (The Art of Computer Programming) and Kernighan:**
- Correctness first. Optimize later. Premature optimization remains the root of all evil.
- But know your data structures. Using O(n) lookup in a hot loop when a hash map exists is not "premature optimization" - it's negligence.
- Make the common case fast and the edge case correct.
- Clarity is not opposed to performance. Clear code is easier to optimize because you can see what it does.

**From Martin Fowler / Kent Beck:**
- Code tells you how; comments tell you why. If you need a comment to explain what the code does, the code is wrong.
- But DO write comments for: non-obvious business rules, workarounds for known bugs in dependencies, performance-critical sections where the "obvious" approach was measured and found wanting.

**Defensive Programming:**
- Validate at system boundaries (API endpoints, CLI input, file reads, deserialization). Trust nothing from outside your process.
- Inside the system boundary, use types and contracts to make invalid states unrepresentable. Don't re-validate at every function call.
- Fail fast and fail loud. Silent failures are production incidents waiting to happen.

### 2.3 - Error Handling Strategy

Before writing code, decide:
- What is an expected failure? (User input validation, network timeout, not found) -> Handle gracefully with proper error types.
- What is an unexpected failure? (Null where you proved non-null, corrupted state) -> Crash immediately. Don't try to recover from impossible states.
- What is a retryable failure? (Transient network error, deadlock) -> Implement retry with backoff, jitter, and a circuit breaker.
- Where do errors cross boundaries? (Library -> application, service -> client) -> Translate error types at boundaries. Don't leak internal implementation errors to callers.

---

## Phase 3: Implementation

### 3.1 - Implementation Order

Implement in vertical slices, not horizontal layers:
1. Start with the thinnest possible end-to-end path that proves the architecture works.
2. Add behavior slice by slice, each one independently verifiable.
3. Refactor only after the current slice is working and tested.

### 3.2 - Code Quality Gates (Enforce on Every File You Touch)

Before considering a file done, verify ALL of the following:

**Naming:**
- [ ] Variables/functions/methods describe WHAT, not HOW (`getUserProfile`, not `queryDatabaseForUser`)
- [ ] Boolean variables read as assertions (`isActive`, `hasPermission`, `canEdit`, not `flag`, `status`, `check`)
- [ ] Collections are plural (`users`, `orderItems`), single items are singular
- [ ] No abbreviations except universally understood ones (`id`, `url`, `http`, `db`)
- [ ] No generic names (`data`, `info`, `result`, `temp`, `item`, `thing`, `obj`, `val`) unless scope is less than 5 lines
- [ ] Match the naming convention already used in the codebase (camelCase/snake_case/PascalCase)

**Structure:**
- [ ] No function exceeds 40 lines (excluding type definitions and config objects). If it does, it's doing too much.
- [ ] No file exceeds 300 lines. If it does, it contains more than one concept.
- [ ] No more than 3 levels of nesting. Use early returns, guard clauses, and extraction.
- [ ] No more than 4 parameters per function. Use an options/config object if you need more.
- [ ] No magic numbers or magic strings. Extract to named constants.
- [ ] No commented-out code. Version control exists.

**Types (for typed languages):**
- [ ] No `any` / `object` / `dynamic` / `interface{}` unless wrapping a genuinely untyped boundary (FFI, JSON parsing before validation)
- [ ] No type assertions / force casts unless immediately preceded by a runtime check
- [ ] Discriminated unions over boolean flags when a value changes meaning based on state
- [ ] Return types are explicit on all exported/public functions
- [ ] Null/undefined/nil is handled at the point of introduction, not propagated through 5 call layers

**Immutability and Side Effects:**
- [ ] Prefer `const`/`final`/`val`/`let` (immutable) over mutable bindings
- [ ] Functions that compute should not mutate. Functions that mutate should not compute. Separate queries from commands.
- [ ] Side effects (I/O, logging, metrics, state mutation) are pushed to the edges, not buried in pure logic

**Error Handling:**
- [ ] No swallowed errors (empty catch blocks, ignored Result types, unchecked error returns)
- [ ] Error messages include context: what operation failed, what input caused it, what the caller can do about it
- [ ] Async error paths are tested (rejected promises, failed futures, error channels)

### 3.3 - Concurrency Checklist (If Applicable)

- [ ] Shared mutable state is protected (mutex, lock, atomic, synchronized)
- [ ] Lock ordering is consistent to prevent deadlocks
- [ ] No time-of-check-to-time-of-use (TOCTOU) bugs
- [ ] Async operations that must be sequential use `await`, not fire-and-forget
- [ ] Connection pools / resource pools have bounded sizes and timeouts

### 3.4 - Performance Awareness (Not Premature Optimization)

- [ ] No N+1 queries (batch/join instead of loop-and-fetch)
- [ ] No unnecessary serialization/deserialization in hot paths
- [ ] Collections are sized appropriately (don't allocate a 10,000-element array for 3 items)
- [ ] Expensive computations that are repeated with the same inputs are memoized or cached
- [ ] No blocking I/O on the main thread / event loop

---

## Phase 4: Verification

### 4.1 - Run the Actual Toolchain

After implementation, run EVERY quality gate that exists in the project. Do not skip any.

**Run in this order:**

1. **Formatter** - Run the project's formatter. Fix every formatting issue.
   - `npx prettier --write .` / `cargo fmt` / `go fmt ./...` / `ruff format .` / `dotnet format`
2. **Linter** - Run the project's linter. Fix every error. Fix every warning unless the warning is a known false positive (document why).
   - `npx eslint .` / `cargo clippy` / `golangci-lint run` / `ruff check .` / `dotnet build /warnaserror`
3. **Type checker** - Run the type checker. Zero errors.
   - `npx tsc --noEmit` / `mypy .` / `pyright` / (Go and Rust: built into the compiler)
4. **Tests** - Run the test suite. All existing tests must pass. New tests must exist for new behavior.
   - If you broke an existing test, you either introduced a regression (fix your code) or the test was testing implementation details (fix the test, but confirm with the user first).
5. **Build** - Run the build. It must succeed.
   - `npm run build` / `cargo build` / `go build ./...` / `dotnet build`

### 4.2 - The 99% Rule

Your code must pass AT LEAST 99% of lint/type/format checks on first run. This means:
- Zero type errors
- Zero formatter diffs after running the formatter
- Lint errors only from rules that conflict with each other (document these) or pre-existing violations in files you didn't modify

If you can't hit 99%, something is wrong with your understanding of the toolchain. Go back to Phase 0 and re-read the configs.

### 4.3 - Self-Review Checklist

Read your own diff as if you're reviewing someone else's PR. Check for:

- [ ] No dead code introduced (unused imports, unreachable branches, unused parameters)
- [ ] No TODO/FIXME/HACK comments that aren't tracked in an issue
- [ ] No hardcoded secrets, API keys, or environment-specific values
- [ ] No console.log / print / System.out.println left in production code (use the project's logger)
- [ ] No changes to files outside the scope of this PRD
- [ ] Every public function/method has documentation if the project convention requires it
- [ ] Test coverage exists for every new code path that matters (critical paths, error paths, edge cases)

---

## Anti-Patterns: Things You Must NOT Do

1. **Do not generate boilerplate just because you can.** If a pattern requires 4 files to add one behavior, the pattern is wrong for this use case.
2. **Do not add abstractions "for future extensibility."** YAGNI. Build what the PRD asks for. If the PRD says "support multiple payment providers," abstract it. If the PRD says "integrate Stripe," don't build a payment provider abstraction.
3. **Do not refactor code outside the scope of this PRD.** Note it, suggest it in a comment to the user, but don't do it. Scope creep kills projects.
4. **Do not introduce new dependencies without justification.** Every dependency is a liability. If the functionality is < 50 lines to implement, write it yourself. If you do add a dependency, verify it's maintained, has no known CVEs, and is licensed compatibly.
5. **Do not write clever code.** Clever code is code that makes you feel smart when you write it and makes everyone else feel stupid when they read it. Write boring code. Boring code ships.
6. **Do not name things after patterns.** Name things after what they do in the domain. `OrderProcessor`, not `OrderStrategyFactoryAdapter`. The pattern is an implementation detail.
7. **Do not over-engineer error handling.** Not every function needs a custom error type. Use the project's existing error handling conventions. Only create new error types at meaningful boundaries.
8. **Do not ignore the existing codebase style.** Consistency within a codebase is more important than any individual style preference. If the codebase uses classes, use classes. If it uses functions, use functions. Save the paradigm shift for a separate refactoring PR.

---

## Output

When implementation is complete, present to the user:

1. **Summary of changes** - What was built, which files were created/modified.
2. **Toolchain results** - Output of formatter, linter, type checker, tests, build. All green or explain why not.
3. **Design decisions** - Any architectural choices you made that weren't specified in the PRD, with rationale.
4. **Known limitations** - Anything the PRD asked for that you couldn't fully deliver, and why.
5. **Follow-up suggestions** - Things that should be done next but were out of scope.