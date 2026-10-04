---
name: code-review
description: Use when you want a thorough code review of files, changes, or the entire project before shipping.
risk: safe
argument-hint: "[file/dir/changes]"
---

# Code Review

This skill must only be invoked from the main session, never from a subagent.

## 1. Determine Scope

a. If the user specified file paths, directories, or a description of what to review, use that as the scope.
b. If the user said "review my changes" or similar, use `git diff HEAD` (unstaged + staged) and `git diff --cached` as the scope. Include full file context for changed functions, not just the diff hunks. If no changes exist, tell the user and stop.
c. If no scope is specified, ask the user: "What should I review? Options: specific files/directories, recent changes (`git diff`), or the entire project."
d. For entire-project scope, identify all source files (exclude vendored/generated code, build artifacts, lock files, and test fixtures). Prioritize by architectural significance: import fan-in/fan-out, file size, and recent change frequency. Distribute files across agents by relevance to each agent's domain.
e. Confirm scope with the user before proceeding: "I'll code-review [scope description]. Correct?"

### Language & Project Detection

After determining scope, detect the primary language(s) and framework(s):
- Check file extensions, lock files (`package-lock.json`, `Pipfile.lock`, `Cargo.lock`), and config/module files (`tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `go.sum`)
- Set `primary_language` and note the framework(s) in use
- Inform user: "Detected [language] project using [framework] — tailoring review accordingly."
- Check for project-level or user-level rule files (`rules/<language>.md`, e.g., `rules/python.md`) and instruct agents to read them if present for project-specific conventions.

Language detection shapes agent behavior — agents should apply language-idiomatic checks:
- **Python**: mutable default arguments, bare `except:`, missing type hints on public APIs, `os.path` vs `pathlib`
- **JavaScript/TypeScript**: `==` vs `===`, `var` usage, unhandled promise rejections, missing `async`/`await` error handling, prototype pollution patterns
- **Go**: unchecked errors, goroutine leaks, missing `defer` for cleanup, context propagation
- **Rust**: unnecessary `.clone()`, missing error propagation with `?`, overly broad lifetimes
- **Java**: checked exception abuse, mutable DTOs, missing `@Override`, raw types
- Other languages: apply general software engineering principles

## 2. Round 1 — Spawn Parallel Subagents

Spawn 5 subagents on the **latest, most capable model** available — omit the per-agent `model` override so each subagent inherits the session's model rather than pinning a version-specific name. Do **not** add an override that downgrades the breadth passes (Quality/Readability, Performance, Maintainability) to a cheaper tier such as `sonnet`: measured 2026-06-11, sonnet's false-positive rate in these slots cost more main-session verification time than its savings. (`CLAUDE_CODE_SUBAGENT_MODEL`, if set in the environment Claude launches subagents under, overrides the inherited model.)

Each agent reviews from a **senior distinguished engineer's perspective** — not looking for vulnerabilities (that's `/security-audit`), but evaluating whether this code is well-designed, maintainable, and correct.

- **Agent 1 — Architecture & Design** (module-level and above):
  - Separation of concerns — are responsibilities cleanly divided?
  - Coupling & cohesion — tightly coupled modules? Classes without a single clear purpose?
  - Abstraction levels — too many layers of indirection? Too few?
  - Design patterns — used appropriately, not cargo-culted?
  - Dependency direction — do dependencies flow correctly? Circular dependencies?
  - API surface — are public interfaces minimal? Could internal details leak?
  - Over-engineering — premature abstractions, unnecessary indirection, "enterprise astronaut" patterns, features nobody asked for
  - This agent does NOT review within-function quality (that's Agent 2) or runtime correctness (that's Agent 3).

- **Agent 2 — Code Quality & Readability** (within-function and expression-level):
  - Naming — do names convey intent? Consistent conventions? Abbreviations that obscure meaning?
  - Complexity — deep nesting (guideline: >3 levels warrants extraction), long functions (guideline: >40-60 lines depending on language), long parameter lists (>4 — consider a config/options object)
  - Duplication — copy-paste code that should be extracted (3+ instances, not premature extraction for 2)
  - Dead code — unused functions, unreachable branches, commented-out code
  - Clarity over cleverness — nested ternaries, dense one-liners, magic numbers, implicit behavior
  - Consistency — inconsistent patterns within the codebase (callbacks vs promises, mixed naming conventions)
  - Spaghetti indicators — deeply nested callbacks, unclear control flow, functions with multiple unrelated responsibilities
  - This agent does NOT review module-level architecture (that's Agent 1) or whether the code is correct (that's Agent 3).

- **Agent 3 — Correctness & Robustness** (does the code actually work?):
  - Logic errors — off-by-one, wrong operator, inverted conditions, short-circuit mistakes
  - Edge cases — empty collections, null/undefined, zero values, boundary values, Unicode, large inputs
  - Error handling — swallowed errors, missing error paths, overly broad catches, unhelpful error messages
  - Type safety — implicit conversions, loose equality, unvalidated type assumptions
  - Concurrency — race conditions, shared mutable state, missing synchronization, TOCTOU
  - Resource management — unclosed handles, missing cleanup, memory leaks
  - Invariant violations — assumptions not enforced, preconditions not checked at system boundaries
  - This agent does NOT review performance characteristics (that's Agent 4) or test quality (that's Agent 5).

- **Agent 4 — Performance & Efficiency** (is it fast enough and resource-conscious?):
  - Algorithmic complexity — O(n²) when O(n) is possible, unnecessary sorting, repeated lookups that should be indexed
  - Resource waste — unnecessary allocations, string concatenation in loops, loading entire datasets when streaming works
  - N+1 queries — database access in loops, missing joins, missing eager loading
  - Caching — missing obvious cache opportunities, stale caches without invalidation strategy
  - I/O patterns — synchronous I/O blocking event loops, unbuffered reads
  - Premature optimization — flag optimizations that hurt readability without measurable benefit
  - Bundle/payload size — importing entire libraries for one function
  - This agent does NOT review code correctness (that's Agent 3) or test coverage (that's Agent 5).

- **Agent 5 — Maintainability & Testing** (can this code be changed and trusted?):
  - Test coverage — are critical paths tested? Edge cases? Testing behavior, not implementation details?
  - Test quality — brittle tests tied to implementation, missing assertions, tests that always pass, flaky patterns
  - API contracts — are interfaces stable? Would changes break consumers?
  - Configuration — hardcoded values that should be configurable, environment-specific logic not properly abstracted
  - Documentation — missing context for non-obvious decisions (why, not what), misleading comments
  - Dependency health — too many deps for the functionality, abandoned/unmaintained libraries, major version lag. Note: CVE/vulnerability scanning is `/security-audit`'s job — this agent focuses on maintenance burden only.
  - Migration difficulty — if this code needs to change, how hard will it be?
  - Mock quality — flag these anti-patterns in test files:
    - Mock-heavy tests: mock/stub setup lines outnumber assertion lines by more than 3:1 per test function. Scope: count only lines inside `it()`/`test()`/`test_*()` function bodies. Exclude `beforeEach`/`beforeAll`/`setup*`/`fixture*` at any nesting level, `describe()` wrappers, and conftest.py.
    - Missing real module import: test files that mock a module's interface but never import or exercise the real implementation
    - Behavioral-only assertions: all assertions are `toHaveBeenCalled`/`assert_called_with` with no value assertions (`assertEqual`, `toBe`, `toEqual`) — verifies wiring, not correctness
    - Over-mocked integration tests: tests labeled as "integration" that mock all external dependencies (defeating the purpose)
  - This agent does NOT review code correctness (that's Agent 3) or performance (that's Agent 4).

**Each subagent's prompt MUST be assembled verbatim from the shared fragments in `~/.claude/rules/review-output-contract.md` plus this skill's domain-specific content.** Read that file (when working inside the `claude_extensions` repo itself it is also at `rules/review-output-contract.md`) and inline the named fragment in place of each `<<shared:…>>` marker below; inline every other line exactly as written:
> <<shared:scope-and-context>>
>
> Review from a **senior distinguished engineer's perspective**. For each issue found, verify it is a genuine problem — not a reasonable trade-off for this codebase's context. Check if there is a project convention or framework constraint that justifies the pattern before flagging it.
>
> <<shared:findings-format>>
> - **Severity**: critical | major | minor
> - **Category**: short label (e.g., "Complexity", "Dead Code", "N+1 Query", "God Function", "Missing Tests")
> - **Location**: file path and line number or function name
> - **Issue**: one-sentence description of the problem and why it matters (e.g., "function handles both validation and persistence, making it impossible to test either in isolation" not just "function does too much")
> - **Risk**: HIGH | MED | LOW — blast radius of the finding. HIGH: public API surface, auth/security-critical path, data migration, or shared utility in a common/shared/utils package. MED: internal shared module (used by more than one sibling), configuration change, or test infrastructure. LOW: leaf module (single-use helper, private to one package), documentation, or cosmetic change.
> - **Suggestion**: concrete remediation — state what to do, not "consider" or "review" (e.g., "extract lines 45-80 into a `validate_input()` function" not "consider refactoring")
>
> Severity guide:
> - **critical**: Will cause bugs in production, data corruption, or makes the codebase unmaintainable. Must fix before shipping.
> - **major**: Significant design flaw, substantial tech debt, or correctness risk that will bite you later. Should fix.
> - **minor**: Style/convention issue, minor improvement, or defense-in-depth. Nice to fix but non-blocking.
>
> **Rationalizations to Reject** — Do not accept these dismissals as justification for downgrading or omitting findings:
> - "It works" — correctness is necessary but not sufficient; maintainability and clarity matter
> - "It's just a prototype / we'll refactor later" — prototypes become production; refactors rarely happen
> - "Nobody else touches this code / it's only called from one place" — people leave, teams change, call sites multiply; design for the interface, not the current caller or author
> - "The tests pass" — tests can be incomplete or wrong; passing tests don't prove correctness
> - "It's how the old code did it" — legacy patterns aren't automatically correct; evaluate on merit
> - "Performance doesn't matter here" — maybe, but O(n²) in a loop is still a bug waiting for data growth
>
> **Red Flags — STOP and Re-examine** — If you catch yourself thinking any of these, stop and reconsider:
> - "This file looks fine, I'll skim it" — STOP. Read it. Skimming misses subtle bugs.
> - "The function is small, it can't have issues" — STOP. Size doesn't correlate with correctness.
> - "I haven't read all files in scope yet, but I'll stop early" — STOP. Finish reading the full scope before concluding. Hitting the 10-item cap is fine; abandoning unread files is not.
> - "This is just boilerplate / glue code" — STOP. Glue code is where integration bugs hide.
> - "I don't fully understand this, but it looks okay" — STOP. If you don't understand it, you can't review it. Read the context.
>
> <<shared:closing-instruction>>

## 3. Synthesize Results

After all subagents complete, the main session:
- Deduplicates overlapping findings (same root cause reported by multiple agents)
- Merges related findings (e.g., multiple instances of the same pattern)
- Sorts by severity (critical > major > minor), then by risk (HIGH > MED > LOW) within same severity
- If a subagent returned zero findings, note that to the user (this is a good sign for that category)
- Present a consolidated report with:
  - **Summary**: total findings by severity, overall risk assessment. Note the detected language/framework from Section 1.
  - **Overall health**: "This codebase is [well-structured / has some debt / needs significant refactoring] because [1-2 sentence justification]" — anchor this assessment to finding counts (e.g., 0 critical + 0 major = well-structured; multiple major = has debt; any critical = needs refactoring).
  - **Findings**: the deduplicated list
  - **Positive observations**: well-implemented patterns worth noting (max 3 bullet points — keep it brief)

## 4. Remediation

If the user wants to fix issues:
- For **critical** and **major** findings: offer to fix them immediately, starting with critical
- Group related fixes into coherent batches (don't fix one naming issue at a time — batch all naming fixes together)
- For **minor** findings: list them as recommendations the user can address
- Apply fixes in the main session (not subagents), following existing code patterns
- **BEFORE/AFTER verification** for each fix:
  1. **BEFORE**: Record the current failing state. For testable findings: the specific command, test, or check that demonstrates the issue, with output. For non-testable findings (naming, dead code, structural issues): a quoted code snippet with file path and function/symbol anchor (e.g., "in function `validate_user` in `auth.py`") — do not use line numbers for BEFORE evidence, as they shift after edits. Note: the findings Location field format (which may include line numbers) is unchanged.
  2. **FIX**: Apply the fix.
  3. **AFTER**: For testable findings: re-run the same command/test/check and verify it now passes, with output as evidence. For non-testable findings: show the modified code snippet at the same location.
  4. If AFTER still fails (testable) or the code change doesn't address the finding (non-testable), the fix is incomplete — do not mark the finding as resolved.
- Run tests after each batch of fixes
- After fixing, run a targeted follow-up review (Section 5)

## 5. Follow-Up Rounds

After applying fixes, automatically verify them:
- Spawn **2 parallel subagents** that review ONLY the changed code and its immediate context, **both on the latest, most capable model** (omit the `model` override so they inherit the session model; fix verification is high-stakes — don't downgrade to a cheaper tier; `CLAUDE_CODE_SUBAGENT_MODEL` overrides if set):
  - **Agent A — Architecture, Quality & Correctness** (combines agents 1-3 focus areas)
  - **Agent B — Performance, Maintainability & Testing** (combines agents 4-5 focus areas, plus checking that fixes didn't introduce new issues)
- Each subagent's prompt MUST include the full verbatim format template from Section 2 (assembled from `~/.claude/rules/review-output-contract.md` as described there), with only the first line (the `<<shared:scope-and-context>>` fragment) replaced: "Review ONLY the following changed files/sections: [list]. Read at most 3 additional context files. Max 5 items. Also verify that the applied fixes are correct and complete — check for regressions." All other instructions (severity guide, field format, `<<shared:findings-format>>`, `<<shared:closing-instruction>>`) remain unchanged.
- Synthesize and present to user.
- **Stop condition**: a round produces **0 critical and 0 major** findings. Minor findings do not block — note them and declare the review complete.
- **Safety valve**: max 3 follow-up rounds (not counting the initial 5-agent round). If critical/major issues persist after 3 rounds, STOP — report what keeps recurring and flag that the recurring issues may require broader refactoring beyond the current review scope. Present remaining findings as a reference list.

## 6. Completion

When the stop condition is met, present a final summary:
- Findings resolved
- Remaining minor items (if any) as a reference list
- Do not begin further work unless the user explicitly requests it.

If the user does not approve fixes at any point, present the findings as a reference and end. Do not modify any files.

## Output Contract

The final synthesized report MUST include all of the following:

- **Scope summary**: what was reviewed (files, directories, changes, or entire project)
- **Findings table**: each finding with severity, risk (HIGH/MED/LOW), category, location, issue, and suggestion — sorted by severity, then risk within same severity
- **Aggregate counts**: total findings broken down by severity (critical/major/minor)
- **Verdict**: one of `pass` (0 critical, 0 major), `conditional-pass` (0 critical, 1+ major), or `fail` (1+ critical)
- **Remediation offer**: ask the user if they want to fix critical/major findings
