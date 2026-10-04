---
name: kanso-principles
description: Use when generating, reviewing, modifying, or discussing any code. Sets standing anti-dilution rules for all code-related work. Auto-loads; not directly invoked by the user.
user-invocable: false
---

# kanso-principles

Standing context for any code-related task. These rules override default verbosity and defensive habits. They apply equally to code you write, code you review, and code you modify.

The single governing principle: **prefer deletion over addition**. If a change does not reduce complexity, reduce line count, or increase clarity, justify its existence. Code earns its place.

## The anti-dilution taxonomy

### 1. No tautological comments

A comment must explain *why*, not restate *what*. If the comment echoes the code, delete the comment or rewrite it to carry business context, constraints, or intent.

Bad: `// Filter users by age` above `users.filter(u => u.age > 18)`.

Good: `// Legal requirement: 18+ only` above the same line.

### 2. No temporal or step-marker comments

Artefacts of the prompt that produced the code. Delete them before they commit.

Bad: `// Step 1: fetch user`, `// Now validate`, `// Add retry logic as requested`

Good: no comment, or a comment explaining why the retry exists.

### 3. No defensive programming theatre

Cascading `try/catch`, null checks on already-typed values, isinstance checks on typed parameters, and exception handlers that silently swallow errors and return `None`/`null`. Silent errors are the deadliest errors.

Let exceptions propagate. Handle them at the boundary where the recovery strategy is known. If an invariant is guaranteed by the type system, trust it.

### 4. No filler variables

`const result = compute(x); return result;` is just `return compute(x);`

Intermediate variables earn their place by adding a meaningful name or being referenced more than once.

### 5. No zero-entropy names

`userDataProcessingResult`, `helperFunction`, `dataManager`. Statistically probable, domain-free, and unreadable at a glance.

Prefer: `adults`, `invoice`, `sessionExpired`. Short names are fine when the context makes them clear.

### 6. No premature abstraction

A factory for one implementation, an interface for one consumer, a base class for one subclass. These are costs without benefits. Solve the problem that exists now, not one that might exist later.

The rule of three: abstract after the third concrete case, not before the first.

### 7. No fake test coverage

Tests that assert on mocks, tests that cover only the happy path, tests that mirror implementation structure one-to-one. Line coverage is a lagging indicator; mutation score is a leading one.

A test must be able to fail when the code is broken. If you cannot construct a mutation of the implementation that the test would catch, the test is decorative.

### 8. No structural erosion

Over iterations, LLM-assisted code tends toward a single god function that absorbs every new requirement. Resist this. When a function grows past its original shape, split before adding.

### 9. No phantom bugs

Guards against impossible states. Overflow checks in Python integer arithmetic. Null checks on values the type system says are non-null. Retries on idempotent operations that cannot fail partially. Noise dressed as safety.

### 10. No vanilla reimplementation

Manual `flatten` when `itertools.chain` exists. Hand-rolled debouncing when the framework provides it. Bespoke date math when the standard library handles it. Reach for the standard library first.

## Positive guidance

### Match repo conventions before introducing new ones

Read the surrounding code. If the codebase uses `get_*` for data access, do not introduce `fetch_*`. If error handling is done via result types, do not start throwing. Consistency compounds; local cleverness fragments.

### Surface uncertain changes as questions

If a change is plausibly correct but not obviously so, ask. One clarifying question costs less than a silent wrong answer.

### Write commit-message-grade code comments

When a comment earns its place, treat it like a commit message: explain the *why*, the constraint, the non-obvious tradeoff. Comments are letters to future readers, not narration for the current one.

### Voice preservation

Match the existing author's voice in code style, naming, and comment density. Do not impose a generic house style onto a codebase that has its own.

## When generating new code

Start with the minimum viable implementation. No logging, no metrics, no error wrapping, no telemetry, no abstractions unless the call site needs them. Add those concerns when the code earns them, not preemptively.

If the implementation feels too simple, it is probably correct. LLM training biases toward the 2.2× verbose baseline; resist it.

## When reviewing code

Flag anti-pattern instances against this taxonomy. Use the category names above directly in findings so they are searchable and consistent. Prioritise by Tier 1 (correctness/security), Tier 2 (maintainability/architecture), Tier 3 (polish). If a finding is below Tier 3, it does not belong in the review.

## When modifying code

Delete freely. Commented-out code is deleted. Dead imports are deleted. Stale comments that no longer match the code are deleted. Unused parameters, variables, and branches are deleted. Git remembers.

Refactor and behaviour change do not share a commit. If a task requires both, split them.

## Cross-harness conventions

These skills follow the Agent Skills standard and run in any compatible tool (Claude Code, Codex CLI, Cursor, Gemini CLI, Grok Build). Two conventions keep them portable:

- A `/kanso-<name>` reference means: invoke the kanso-<name> skill by whatever mechanism your harness provides. A slash command, a skill mention, or reading its SKILL.md directly all count.
- Where a skill names a harness feature your tool lacks (subagents, hooks, per-agent model selection), apply the fallback the skill gives, or run the step inline.
