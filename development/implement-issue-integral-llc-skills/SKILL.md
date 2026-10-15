---
name: implement-issue
description: Implement a GitHub issue with principal-engineer-grade code quality. Reads the issue and its full comment thread, linked issues and PRs as the spec, discovers project linting/formatting/type rules, ships the smallest diff that satisfies the issue with no speculative abstractions, holds DRY/SOLID/GoF as paramount on every line it does write, routes any AI-judgment work through the TypeSafe skill, and produces code that passes lint, type check, and formatting on first commit. Use when the user points at a GitHub issue number or URL and wants production implementation - not a prototype.
---

# Implement GitHub Issue

This skill takes a GitHub issue (number, URL, or "the issue about X") and produces production-grade implementation. The issue - including its comment thread, linked issues, and referenced PRs - is the spec. The output must read like it was written by a principal engineer with 20 years of experience, not an LLM, not a junior, not a "good enough" mid-level.

You may skip steps if the project context is already known or if the user explicitly tells you to.

---

## Prime Directive: Ship the Smallest Change That Closes the Issue

This outranks every other instruction in this skill. The phases below are a thinking checklist, not a list of artifacts you owe anyone. The correct output for a one-line bug is a one-line diff plus a test, produced by a short session - not a module, not an interface, not a design writeup.

Before every file you create and every abstraction you introduce, answer out loud: **which acceptance criterion fails if I leave this out?** No answer means it does not get written.

Hard limits, no exceptions without the user saying so:

- **No new file** when the change fits in an existing one. New files need a named reason.
- **No new abstraction, interface, base class, config flag, or plugin point** that has exactly one implementation today. One caller means write the function.
- **No generalization of a specific request.** "Fix the CSV date parser" means fix the CSV date parser, not build a pluggable format-detection layer.
- **No new dependency, new service, new table, new endpoint, or new build step** unless the issue asks for it by name.
- **No rewrite of code that already works.** Smallest correct edit to the existing shape, even when you dislike the shape.
- **No speculative error handling, caching, retries, batching, or metrics** for problems the issue does not report.
- **No refactor riding along with the fix.** Separate it, note it, leave it.

Effort is scaled to the issue, not to this document. A typo fix does not get a risk assessment. A schema migration does. Read the issue, pick the weight, and say which you picked.

If the minimal fix is genuinely wrong - it papers over a real defect, or the third copy of the same bug is the signal to extract - say that in one or two sentences, give the user the small version and the larger option, and let them choose. Do not silently build the larger one.

## Second Directive: DRY, SOLID and GoF Are Paramount Inside That Scope

The two directives govern different axes and never actually collide:

- **Minimum scope decides HOW MUCH code exists.** Fewest files, fewest moving parts.
- **DRY, SOLID and GoF decide WHAT THAT CODE LOOKS LIKE.** Non-negotiable, on every line you do write.

A small diff is not an excuse for a sloppy one. The rules below are mandatory, not aspirational:

- **DRY is mandatory where knowledge repeats.** If your change makes a rule, constant, validation, query shape, or error message live in two places, you have failed - extract it, even inside a three-line diff. DRY is about knowledge, not about text that happens to look alike (see 3.2).
- **SOLID is mandatory on what you touch.** A function that grew a second reason to change gets split. An `if isinstance(...)` chain that a polymorphic call would erase gets the polymorphic call. Depend on the abstraction at real boundaries: I/O, external services, anything you mock.
- **A GoF pattern is mandatory when the problem already IS that pattern.** Two algorithms chosen at runtime is Strategy. Bridging an interface you do not control is Adapter. Complex conditional construction is Factory. Use the named pattern and the domain name, and do not hand-roll a worse version of it.

The test is the same in both directions: **the code is actively worse without it.** Worse today, in this diff, for this issue - not worse in an imagined future. That standard forbids inventing a Strategy for one algorithm, and it equally forbids pasting the same validation into a second handler because "it is only four lines".

When minimal scope and these principles genuinely pull apart, scope wins on quantity and the principles win on shape: do not add a file to satisfy a principle, apply the principle inside the file you were already editing.

---

## Phase 0: Issue Acquisition

Do this first. You cannot scope work you have not read.

### 0.1 - Resolve the Issue Reference

The user may give you `#1234`, a full URL, a branch name containing a number, or a description. Resolve it to `<owner>/<repo>#<number>` before anything else.

```bash
gh issue view <number> -R <owner>/<repo> --json number,title,state,body,labels,assignees,milestone,url,closedAt
```

If the repo is not stated, infer it from the git remote of the working directory:

```bash
gh repo view --json nameWithOwner --jq .nameWithOwner
```

If the user described the issue instead of numbering it, search before guessing:

```bash
gh issue list -R <owner>/<repo> --search "<keywords>" --state all --limit 20 --json number,title,labels,state
```

Confirm the resolved issue with the user when the match is not exact. Implementing the wrong issue wastes the whole session.

**Auth note:** if `gh` returns 404 on a repo you know exists, you are authenticated as the wrong account. Check `gh auth status` and switch (`gh auth switch --user <login>`) or set `GH_TOKEN` before concluding the issue is missing.

### 0.2 - Read the Whole Thread, Not Just the Body

An issue body is the opening argument. The comments are where the requirements actually get decided, reversed, and narrowed.

```bash
gh issue view <number> -R <owner>/<repo> --comments
```

Read every comment in order and extract:

- **Amendments**: requirements added, changed, or dropped after the body was written. The last word wins over the body.
- **Decisions**: "we agreed to X", "let's not do Y for now", "this is out of scope".
- **Constraints**: deadlines, deploy windows, compatibility requirements, data migration concerns.
- **Rejected approaches**: someone already tried something and it did not work. Do not repeat it.
- **Open questions nobody answered.** These become your clarifying questions in Phase 1.4.

Note who said what. A maintainer's "do it this way" outranks a drive-by suggestion.

### 0.3 - Follow the Graph

Issues are rarely self-contained. Pull in:

- **Linked/parent/child issues and tracking lists.** Checkbox lists of `#123` references in the body are sub-tasks; confirm which ones are in your scope.
- **Referenced PRs.** A closed PR referencing this issue is a prior attempt. Read its diff and its review comments - that is the fastest way to learn what the reviewers will reject.
- **Cross-referenced timeline events.**

```bash
gh api repos/<owner>/<repo>/issues/<number>/timeline --paginate \
  --jq '.[] | select(.event=="cross-referenced" or .event=="connected") | {event, src: .source.issue.html_url, title: .source.issue.title}'
```

- **Labels as signal.** `bug` means reproduce first. `breaking-change` means the risk surface in Phase 1.3 is mandatory, not optional. `good-first-issue` means the fix is expected to be small; if your plan is large, you have misread the issue.

### 0.4 - Reproduce Before You Fix (Bugs Only)

If the issue is a bug report, do not write a fix until you have reproduced the failure. Turn the reproduction into a failing test first. A fix without a red-then-green test is a guess.

If you cannot reproduce it, say so explicitly and ask for the missing environment, input, or version before proceeding.

### 0.5 - Check Whether It Is Already Done or Stale

Issues rot. Before implementing, verify the problem still exists on the current default branch. Check `closedAt`, check whether a recent commit already addressed it (`git log --oneline --grep "#<number>"`), and check whether the code the issue describes still exists. Report a stale issue to the user rather than implementing dead work.

---

## Phase 1: Toolchain Discovery

Before writing a single line of code, you MUST understand the project's quality gates. These are non-negotiable constraints, not suggestions.

### 1.1 - Detect the Language and Runtime

Scan the project root and common config locations:

- `package.json`, `tsconfig.json`, `deno.json` -> TypeScript/JavaScript
- `pyproject.toml`, `setup.py`, `setup.cfg`, `ruff.toml` -> Python
- `go.mod` -> Go
- `Cargo.toml` -> Rust
- `*.csproj`, `*.sln`, `Directory.Build.props` -> C#/.NET
- `pom.xml`, `build.gradle`, `build.gradle.kts` -> Java/Kotlin
- `Package.swift` -> Swift

### 1.2 - Extract Lint Rules (READ THEM, DON'T ASSUME)

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

### 1.3 - Extract Formatting Rules

Find and READ:
- `.prettierrc*`, `.prettierignore` -> Prettier config
- `.editorconfig` -> universal editor config
- `biome.json` formatter section
- `rustfmt.toml`
- `gofmt`/`goimports` (Go is opinionated - follow it)
- `black`, `ruff format` config sections
- `csharpier`, `.editorconfig` for C#

Note: tabs vs spaces, line length, trailing commas, quote style, semicolons. These are not opinions during implementation - they are laws.

### 1.4 - Check for Pre-commit Hooks and CI Gates

- `.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- Look for what CI actually runs: lint, type-check, test, build. Your code must survive all of these.
- Check `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `CODEOWNERS`. The issue is the what; these are the how the repo expects it delivered.

### 1.5 - Study Existing Patterns in the Codebase

Before implementing anything new, spend time reading existing code. Specifically:

- How are modules structured? Barrel files? Index re-exports? Flat?
- How are errors handled? Custom error classes? Result types? Try-catch patterns?
- How are dependencies injected? Constructor injection? Module-level? IoC container?
- How is state managed? What ORM/data layer? Repository pattern? Direct queries?
- How are interfaces/types organized? Co-located? Centralized? Per-feature?
- What naming conventions are used? `camelCase`, `snake_case`, `PascalCase` for what?
- How are async operations handled? Promises? Observables? Channels? Async/await?
- What test framework is in use? How are tests structured? Where do they live?

**CRITICAL: Match existing patterns. Do not introduce a new pattern unless the issue explicitly calls for it or the existing pattern is fundamentally broken. Consistency across a codebase beats theoretical perfection in one file.**

---

## Phase 2: Scope and Risk

### 2.1 - Derive Acceptance Criteria

An issue rarely ships with a clean acceptance list. Build one. Merge the body, the thread amendments from Phase 0.2, and any checkbox list into a single explicit set of criteria, each one verifiable by a test or an observable behavior.

Write it down and show it to the user. This list is what you will report against in the Output phase. If a criterion cannot be verified, it is not a criterion, it is a wish - push back on it now.

### 2.2 - Identify the Scope Boundary

List explicitly:
- What you WILL build
- What you WILL NOT build (including anything the thread explicitly deferred)
- What already exists that you will modify
- What already exists that you must NOT modify (shared interfaces, public APIs with consumers)

Issues attract scope creep in the comments. Someone always says "while you're in there...". That is a new issue, not this one. Say so.

### 2.3 - Identify the Risk Surface

Before writing code, identify:
- Which changes touch shared/public interfaces? These need the most care.
- Which changes touch data persistence or schema? These are irreversible in production.
- Which changes have concurrency implications? Race conditions, deadlocks, starvation.
- Which changes affect performance on the critical path?
- What happens during deploy when old and new code coexist?
- Does the change span more than one service, repo, pipeline, or config? The hard failures are not inside one function, they are the unintended consequence at the seam. Trace the whole path, not the file you edited.
- Does the change introduce or widen a credential, role, token, scope, or IAM permission? Grant the least that makes the criteria pass, and say what you granted.

Present this risk assessment to the user. Get explicit confirmation before proceeding.

### 2.4 - Name the Security Assumptions the Issue Left Out

Most security defects are not sloppy code. They are correct code built on a wrong assumption about who and what. An issue says what to build and almost never says who may see the result, so answer these before coding and add the answers to the criteria in 2.1:

- **Who is allowed to call this, and who is not?** Name the check that enforces it, not the intention.
- **What data does this path return, log, or persist?** If it hands back more fields than the criteria need, that is exposure, not convenience.
- **What actions does it permit?** Read versus write versus delete, and on whose records.
- **What must stay hidden** - secrets, tokens, PII, other tenants' rows, internal errors that describe the schema to a caller.
- **What business rule governs it** that a reader of the code would not guess.

Where the answer is not in the issue, in the thread, or in the existing code, ask. A guess here produces code that passes every test and still violates policy.

### 2.5 - Ask the Unanswered Questions

If Phase 0.2 surfaced open questions that change the shape of the implementation, ask the user now, before coding. Ask in the chat. Do not post a comment on the issue unless the user explicitly tells you to - anything posted under their name goes out on their say-so only.

### 2.6 - Align on the Mechanism Before You Build It

An issue names an outcome. It rarely names the mechanism, and for some changes the mechanism is the whole decision. Choosing one alone and revealing it in a pull request is how a reviewer's disagreement costs you the work instead of an afternoon.

Stop and align when the change decides any of these:

- **Where control lives.** Which process, replica, or task starts, stops, resumes, or owns a piece of work.
- **How a signal crosses a boundary.** Polling, notification, queue, shared row, in-process call - and what happens when that path is down.
- **What happens on abnormal termination.** Cancellation, timeout, crash, deploy in the middle of a run.
- **Who is the source of truth** for a state that two components both observe.
- **A new invariant on an existing hot path** that every later feature inherits whether it wants it or not.

The alignment is short, not a design document: name the mechanism you intend, the one you rejected, and the single property that decides between them. Show it to the user. Where the issue or the code has a named owner, get their ack before you write the implementation. Post it on the issue only if the user tells you to.

A mechanism the reviewer meets for the first time in the diff is an argument you scheduled for the worst possible moment.

### 2.7 - Branch Before You Edit

Create a working branch off the default branch before the first edit, named to the repo's convention (check `git branch -a` for the house style; common forms are `fix/<n>-slug`, `feat/<slug>`).

Verify which branch you are actually on at commit time - a shared worktree can be switched under you. Never commit or push without an explicit instruction from the user, and never merge a PR.

---

## Phase 3: Architecture and Design

### 3.1 - Module Decomposition

**Default: no new modules.** Most issues are satisfied by editing existing code. Decompose only when the change genuinely does not fit anywhere that exists, and say which acceptance criterion forced it.

When it is warranted, for each module:
- Define the public interface (what callers see)
- Define the internal complexity it hides
- Identify its dependencies (what it needs from other modules)

**Deep modules over shallow modules.** A class with 3 public methods that hides 500 lines of complexity is better than 10 classes with 2 methods each that just delegate to each other.

### 3.2 - Apply Design Principles (Mandatory, Not Dogmatic)

These principles are required on every line you write; how far you take them is judgement. Apply them where they reduce complexity, and never as decoration where they add it. The notes below are what each one actually means, so you apply the real rule rather than its cargo-cult version.

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

### 3.3 - Error Handling Strategy

Before writing code, decide:
- What is an expected failure? (User input validation, network timeout, not found) -> Handle gracefully with proper error types.
- What is an unexpected failure? (Null where you proved non-null, corrupted state) -> Crash immediately. Don't try to recover from impossible states.
- What is a retryable failure? (Transient network error, deadlock) -> Implement retry with backoff, jitter, and a circuit breaker.
- Where do errors cross boundaries? (Library -> application, service -> client) -> Translate error types at boundaries. Don't leak internal implementation errors to callers, including stack traces, queries, and file paths.
- **Which way does it fail?** Every auth, permission, validation, quota, and timeout path fails closed. A branch that denies on success and allows on error is a vulnerability, not a bug. Write the test that proves the deny.

### 3.4 - Work That Needs Judgment: Use the TypeSafe Skill

**Mandatory.** When the issue needs semantic understanding rather than a rule you can write down, invoke the installed skill (`/typesafe:typesafe-ai`) and build on TypeSafe. Do not hand-roll a prompt-and-parse step, a regex pile, or a heuristic scorer for work that is a typed judgment.

Triggers - any of these in the issue means invoke the skill before designing:

- Classifying, routing, ranking, reranking, or matching by meaning rather than by key.
- Extracting or selecting a value out of messy text, a document, or a user message.
- Verifying a claim or a field against its evidence, or deciding when to escalate to a person.
- An existing prompt-and-parse call, or fragile parsing code the issue asks you to make less brittle.
- Anything where the honest answer is "it depends what the text means".

What the skill gives you, and why you invoke it rather than working from memory: current API contracts, the three primitives, cookbooks, and prompting guidance. **The live docs are the source of truth and are read as part of the task** - a stale reading is how invented fields get written. Keep the plugin updated (`/reload-plugins` after an update).

House rules on top of the skill's own guidance, so the result survives review here:

- **Talk the design out before coding.** Work the decomposition with the skill, show the plan, and confirm it is sound. Validate what the skill assumes rather than accepting it; a plausible question that does not match the domain produces confident wrong answers.
- **One home for questions and thresholds.** Every question definition and every confidence threshold lives in a single reviewable module, named, never inline at the call site and never a bare number in a branch. This is the existing no-magic-numbers and DRY rule, and it is what makes the behavior auditable later.
- **Pick the primitive by what the answer means:** Choice for one of a defined set, Noul for whether a condition holds, Score for degree along a described dimension. Include a no-match outcome where nothing may fit.
- **Thresholds are evidence, not taste.** Filter on a threshold you evaluated against real data and the real cost of being wrong. When you are only picking the best of several options, take the highest confidence and skip the threshold.
- **Keep code doing code's job.** Known rules, calculations, exact lookups, and execution stay in code. Judgment goes where meaning is needed, and nowhere else. Ask independent questions over the same state in one request.
- **Typed output guarantees the interface, not the truth.** Run cheap test queries against representative cases, including the ones you expect to fail, and check the resulting application behavior rather than the raw answer.
- **Credentials stay server-side.** The API key never reaches a browser bundle or a client-side call.

This section does not relax the prime directive. If the issue asks for a fixed rule, write the fixed rule. Reach for judgment when the issue genuinely needs it, not to make a small change interesting.

### 3.5 - Make the Mechanism Visible Where It Surprises

Code whose control flow leaves the local path - another replica stops this task, a background watcher acts on an event, a row in a table is what ends this loop - reads as in-process to every reviewer who lands on the line. Two cheap things prevent the misread:

- **Give the mechanism a name.** One collaborator or type that owns it, named for what it does in the domain, rather than four private methods bolted onto a class that already has five reasons to change. That name is the documentation that survives the next edit.
- **Say it at the statement that surprises.** One line, at the call that stops the work or reads the state, naming where the signal came from. A docstring three methods up and a paragraph in the PR description do not reach the reader who is looking at the cancel.

Treat a review comment that misreads your code as a defect in the code, not in the reviewer. When two comments misread the same seam, the seam is wrong.

---

## Phase 4: Implementation

### 4.1 - Implementation Order

Implement in vertical slices, not horizontal layers:
1. For a bug: start from the failing test written in Phase 0.4 and make it pass.
2. For a feature: start with the thinnest possible end-to-end path that proves the architecture works.
3. Add behavior slice by slice, each one independently verifiable against one acceptance criterion from Phase 2.1.
4. Refactor only after the current slice is working and tested.

### 4.2 - Code Quality Gates (Enforce on Every File You Touch)

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
- [ ] Before naming a constant, grep for its siblings. If the equivalent value elsewhere is still an inline literal, either follow the existing style or lift them all in this diff. Half a convention is worse than either whole one, and it is the first thing a reviewer notices.
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

### 4.3 - Concurrency Checklist (If Applicable)

- [ ] Shared mutable state is protected (mutex, lock, atomic, synchronized)
- [ ] Lock ordering is consistent to prevent deadlocks
- [ ] No time-of-check-to-time-of-use (TOCTOU) bugs
- [ ] Async operations that must be sequential use `await`, not fire-and-forget
- [ ] Connection pools / resource pools have bounded sizes and timeouts
- [ ] Every path that can be stopped from outside (cancel, timeout, shutdown, deploy) has a defined stopping point, and the work between two stopping points is safe to abandon
- [ ] Teardown after an abnormal stop actually runs and actually completes - a cancelled task still holds leases, claims, sandboxes, connections, and temp state that something has to release
- [ ] Forced stop (task cancellation, kill) is a backstop behind a cooperative stop, not the only mechanism, wherever the work holds an external resource
- [ ] A signal that arrives while the work is between steps is not lost - the receiver re-reads state when it starts, not only when it is notified

### 4.4 - Performance Awareness (Not Premature Optimization)

- [ ] No N+1 queries (batch/join instead of loop-and-fetch)
- [ ] No unnecessary serialization/deserialization in hot paths
- [ ] Collections are sized appropriately (don't allocate a 10,000-element array for 3 items)
- [ ] Expensive computations that are repeated with the same inputs are memoized or cached
- [ ] No blocking I/O on the main thread / event loop

---

## Phase 5: Verification

### 5.1 - Run the Actual Toolchain

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
6. **Security tooling the repo already has** - run it now rather than letting CI find it after you have handed the work back. Whatever is configured: secret scanning (`gitleaks`, `detect-secrets`, the pre-commit hook), dependency audit (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`), SAST (CodeQL, `bandit`, `gosec`, `semgrep`). Finding it here costs minutes; finding it in review or production costs a great deal more.

### 5.2 - The 99% Rule

Your code must pass AT LEAST 99% of lint/type/format checks on first run. This means:
- Zero type errors
- Zero formatter diffs after running the formatter
- Lint errors only from rules that conflict with each other (document these) or pre-existing violations in files you didn't modify

If you can't hit 99%, something is wrong with your understanding of the toolchain. Go back to Phase 1 and re-read the configs.

### 5.3 - Verify Against the Acceptance Criteria

Green tests prove the code runs. They do not prove it is correct or safe: generated code compiles, passes, and still leaks. Verify the outcome, not the fact that it executed.

Walk the list from Phase 2.1 one criterion at a time and name the test, command output, or observed behavior that proves it. "Should be fine" is not evidence. A criterion you cannot demonstrate is a criterion you did not deliver - say so out loud rather than letting it pass silently.

For a bug issue, re-run the original reproduction from Phase 0.4 and show it now passes.

### 5.4 - Name What the Tests Stand In For

A test that replaces the real subject with a stand-in proves the wiring around it, not the thing itself. That is a legitimate test and a dishonest claim if you stop there. For every stand-in in a new test, say in one line what stays unproven, then ask whether the unproven part is where the risk actually sits.

It usually is, because the risk lives on the ugly path: what the real unit does when it is stopped, not that the stop signal reached it. If a criterion says the work stops cleanly, something has to observe the aftermath - resources released, claims cleared, no half-written state - against something closer to the real thing than a coroutine that sleeps.

### 5.5 - Self-Review Checklist

Read your own diff as if you're reviewing someone else's PR. Check for:

- [ ] No dead code introduced (unused imports, unreachable branches, unused parameters)
- [ ] No TODO/FIXME/HACK comments that aren't tracked in an issue
- [ ] No hardcoded secrets, API keys, or environment-specific values
- [ ] No console.log / print / System.out.println left in production code (use the project's logger)
- [ ] No changes to files outside the scope of this issue
- [ ] Every public function/method has documentation if the project convention requires it
- [ ] Test coverage exists for every new code path that matters (critical paths, error paths, edge cases)
- [ ] Every new file, type, interface, and parameter maps to an acceptance criterion that fails without it
- [ ] No abstraction with a single implementation, no config flag with a single value, no extension point nobody extends
- [ ] The diff is the smallest one that passes the criteria - re-read it and delete what the issue did not ask for
- [ ] No knowledge duplicated by this diff: no rule, constant, validation, query shape, or message now living in two places
- [ ] Nothing you touched carries a second reason to change, and no conditional-on-type chain was left where polymorphism belongs
- [ ] Any mechanism decision from 2.6 was aligned before the code existed, not revealed by the diff
- [ ] Control flow a reader would not expect is named at the line where it happens, not only in a docstring or the PR description
- [ ] Every stand-in in the new tests has a stated gap, and the abnormal-termination path is covered against something real
- [ ] Where the problem is a known pattern (Strategy, Adapter, Factory, Decorator, Repository), that pattern is used by name rather than hand-rolled
- [ ] Every new or changed entry point enforces the access rule from 2.4, and a test proves the unauthorized caller is refused
- [ ] Nothing returned, logged, or persisted by this path exposes more than the criteria require
- [ ] Hostile and malformed input on the new path was actually exercised, not assumed
- [ ] Every dependency added is on purpose and was checked (maintained, no known CVEs, compatible licence, the package you meant and not a lookalike)
- [ ] Any judgment work went through the TypeSafe skill, with questions and thresholds in one named module and no hand-rolled prompt-and-parse left behind

---

## Phase 6: Handing It Back

Stop at a working tree that is green. Commits, pushes, PRs, issue comments, and status changes happen only when the user asks for them.

When the user does ask:

- **Commit** with the repo's message convention. Reference the issue in the commit body (`Refs #<n>`), not in the subject. Commit only the files this issue touched - no planning artifacts, no agent configs, no unrelated fixes. No AI or tool attribution, ever.
- **PR body**: put `Closes #<n>` in the PR description only if the user wants auto-close on merge. Keep the description short and scaled to the diff. If the change settled a mechanism from 2.6, put it in one sentence near the top, in the reviewer's terms: where the work runs, what stops it, what happens when that path fails.
- **Issue comment or board status**: only on explicit instruction. Draft it, show it, post it after approval.
- **Never merge the PR.** Get it green, report status, stop.

---

## Anti-Patterns: Things You Must NOT Do

1. **Do not implement from the issue title.** Titles lie, get edited, and lag behind the thread. Read the body and every comment.
2. **Do not silently absorb scope from the comments.** If a commenter asked for something beyond the issue's stated goal, name it and let the user decide. Note it as a follow-up issue instead.
3. **Do not generate boilerplate just because you can.** If a pattern requires 4 files to add one behavior, the pattern is wrong for this use case.
4. **Do not add abstractions "for future extensibility."** YAGNI. Build what the issue asks for. If the issue says "support multiple payment providers," abstract it. If the issue says "integrate Stripe," don't build a payment provider abstraction.
5. **Do not refactor code outside the scope of this issue.** Note it, suggest it to the user, but don't do it. Scope creep kills projects.
6. **Do not introduce new dependencies without justification.** Every dependency is a liability, and a dependency you did not read is an unreviewed contributor. If the functionality is < 50 lines to implement, write it yourself. If you do add one, check it as carefully as you check your own diff: maintained, no known CVEs, compatible licence, the real package rather than a typosquat, and pinned the way the repo pins things. Its transitive dependencies ship too.
7. **Do not write clever code.** Clever code is code that makes you feel smart when you write it and makes everyone else feel stupid when they read it. Write boring code. Boring code ships.
8. **Do not name things after patterns.** Name things after what they do in the domain. `OrderProcessor`, not `OrderStrategyFactoryAdapter`. The pattern is an implementation detail.
9. **Do not over-engineer error handling.** Not every function needs a custom error type. Use the project's existing error handling conventions. Only create new error types at meaningful boundaries.
10. **Do not ignore the existing codebase style.** Consistency within a codebase is more important than any individual style preference. If the codebase uses classes, use classes. If it uses functions, use functions. Save the paradigm shift for a separate refactoring PR.
11. **Do not post on the issue on your own initiative.** Comments, label edits, closing, and board moves are the user's call, under the user's name.
12. **Do not treat green CI and silent bots as a review.** Automated reviewers check shape - syntax, lint, the obvious null. They cannot tell you the responsibility sits in the wrong class or that the mechanism is not the one the owner wanted. Zero bot comments means you are ready for a human to disagree, nothing more.
13. **Do not widen a public surface to satisfy a bot comment.** Fix the cause it pointed at. If the fix needs a seam for a test, use a module constant or an injected collaborator, not a new constructor parameter that every caller and reader now carries for the sake of one assertion.

---

## Output

When implementation is complete, present to the user:

1. **Issue** - `<owner>/<repo>#<number>` and its title, so it is on the record which spec you built against.
2. **Acceptance criteria table** - each criterion from Phase 2.1 with its evidence: passing test name, command output, or observed behavior. Anything not met is listed as not met.
3. **Summary of changes** - What was built, which files were created/modified.
4. **Toolchain results** - Output of formatter, linter, type checker, tests, build. All green or explain why not.
5. **Design decisions** - Any architectural choices you made that weren't specified in the issue, with rationale.
6. **Thread items not implemented** - Requests that came up in the comments and were deliberately left out, with why.
7. **Known limitations** - Anything the issue asked for that you couldn't fully deliver, and why.
8. **Follow-up suggestions** - Things that should be done next but were out of scope, phrased as candidate new issues.
