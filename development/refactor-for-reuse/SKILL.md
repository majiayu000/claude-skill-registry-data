---
name: refactor-for-reuse
description: Refactor changed code to eliminate duplication, extract shared logic, and remove dead code. Use after tests pass when the implementation works but contains redundancy, copy-paste logic, or unused code. Pairs with refactor-for-clarity (clarity focus).
metadata:
  version: "1.0.1"
---

# Refactor for Reuse

## Overview

Eliminate redundancy and promote reuse while preserving exact behavior. The goal is not fewer lines — it's code where every piece of logic exists once, dead code is gone, and shared patterns are extracted where they belong. Every change must pass: "Does this remove duplication or dead weight without changing what the code does?"

## When to Use

- After tests pass when the same logic appears in two or more places
- When code was written under time pressure and copy-pasted rather than extracted
- When consolidating related logic scattered across files or modules
- After merging changes that introduced duplication or inconsistency
- When dead code has accumulated — unreachable branches, unused variables, commented-out blocks
- When a wrapper, abstraction, or pattern adds no value over calling the underlying code directly

**When NOT to use:**

- The duplication is intentional — two similar things that will diverge (premature abstraction is worse than duplication)
- You don't fully understand why the code exists — apply Chesterton's Fence before extracting
- The "shared" logic would create a coupling between unrelated modules
- You're about to rewrite the module entirely — refactoring throwaway code wastes effort
- The issue is readability, naming, or structural complexity — use `refactor-for-clarity` instead

## The Four Principles

### 1. Preserve Behavior Exactly

Don't change what the code does — only how it's structured. All inputs, outputs, side effects, error behavior, and edge cases must remain identical. If you're not sure a refactor preserves behavior, don't make it.

```
ASK BEFORE EVERY CHANGE:
→ Does this produce the same output for every input?
→ Does this maintain the same error behavior?
→ Does this preserve the same side effects and ordering?
→ Do all existing tests still pass without modification?
```

### 2. Follow Project Conventions

Refactoring means making code more consistent with the codebase, not imposing external preferences. Before extracting or consolidating:

```
1. Read AGENTS.md or CLAUDE.md / project conventions
2. Study how neighboring code handles similar patterns
3. Match the project's style for:
   - Import ordering and module system
   - Function declaration style
   - Naming conventions
   - Error handling patterns
   - Type annotation depth
```

Refactoring that breaks project consistency is not improvement — it's churn.

### 3. Extract Intent, Not Coincidence

Refactoring has a failure mode: extracting things that look the same but aren't. Watch for these traps:

- **Extracting coincidental duplication** — two functions that happen to look alike now but will diverge; premature extraction creates coupling that costs more than the duplication did
- **Over-extracting small helpers** — a two-line helper used once adds indirection without reuse value
- **Merging unrelated logic** — two things that share structure but serve different purposes should stay separate
- **Optimizing for DRY as a rule** — DRY is a heuristic, not a law; the goal is reducing accidental coupling, not eliminating every repeated token

### 4. Scope to What Changed

Default to refactoring recently modified code. Avoid drive-by changes to unrelated code unless explicitly asked to broaden scope. Unscoped refactoring creates noise in diffs and risks unintended regressions.

## The Refactoring Process

### Step 1: Verify Test Coverage

Before touching anything, confirm the code you're about to refactor is covered by tests. Tests are the only proof that behavior is preserved after structural changes.

If coverage is missing: invoke **`test-driven-development`** to write characterization tests first — tests that pin the current behavior before any refactoring begins. Commit them before proceeding.

If the code's behavior is unclear before writing tests: invoke **`verify-before-claim`** — open the actual files and confirm what the code does before asserting it.

### Step 2: Understand Before Touching (Chesterton's Fence)

Before extracting or removing anything, understand why it exists.

```
BEFORE REFACTORING, ANSWER:
- What is this code's responsibility?
- What calls it? What does it call?
- Why might duplication exist here? (intentional divergence? historical copy-paste?)
- Check git blame: was this written under time pressure, or deliberately structured this way?
```

If you can't answer these, you're not ready to refactor. Read more context first.

### Step 3: Identify Redundancy

Scan for these patterns — each one is a concrete signal, not a vague smell:

| Pattern | Signal | Refactoring |
|---------|--------|-------------|
| Duplicated logic | Same 5+ lines in multiple places | Extract to a shared function |
| Dead code | Unreachable branches, unused variables, commented-out blocks | Remove (after confirming it's truly dead) |
| Unnecessary abstractions | Wrapper that adds no value | Inline the wrapper, call the underlying function directly |
| Over-engineered patterns | Factory-for-a-factory, strategy-with-one-strategy | Replace with the simple direct approach |
| Redundant type assertions | Casting to a type that's already inferred | Remove the assertion |

### Step 4: Apply Changes Incrementally

Make one refactoring at a time. Run tests after each change. **Submit refactoring changes separately from feature or bug fix changes.**

```
FOR EACH REFACTORING:
1. Make the change
2. Run the test suite
3. If tests pass → commit (or continue to next)
4. If tests fail → revert and reconsider — do NOT modify tests to force a pass
```

Avoid batching multiple changes into a single untested step. If something breaks, you need to know which change caused it.

**The Rule of 500:** If a refactoring would touch more than 500 lines, invest in automation (codemods, sed scripts, AST transforms) rather than making the changes by hand.

### Step 5: Verify the Result

After all changes, step back and evaluate the whole:

```
COMPARE BEFORE AND AFTER:
- Is the duplication actually gone, or just moved?
- Did you introduce coupling between modules that should stay independent?
- Is the diff clean and reviewable?
- Would a teammate approve this as a net improvement?
```

If the refactored version introduced coupling or complexity that wasn't there before, revert. Not every extraction improves the code.

## Language-Specific Guidance

```python
# EXTRACT: Duplicated filtering logic
# Before
class ReportGenerator:
    def monthly_report(self, data):
        rows = [d for d in data if d['active'] and d['value'] > 0]
        ...
    def weekly_report(self, data):
        rows = [d for d in data if d['active'] and d['value'] > 0]
        ...

# After
class ReportGenerator:
    def _active_positive(self, data):
        return [d for d in data if d['active'] and d['value'] > 0]

    def monthly_report(self, data):
        rows = self._active_positive(data)
        ...
    def weekly_report(self, data):
        rows = self._active_positive(data)
        ...

# INLINE: Class that only delegates
# Before
class DataProcessor:
    def process(self, data):
        return transform(data)  # no added behavior

# After — call transform(data) directly
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's working, no need to touch it" | Working code with duplication will be fixed inconsistently when it breaks — one copy gets updated, the other doesn't. Extract now. |
| "This duplication is temporary" | It never is. Temporary duplication becomes permanent the moment the next change assumes both copies exist. |
| "The two pieces are almost the same but not quite" | The difference might be intentional divergence — apply Chesterton's Fence before forcing them into one abstraction. |
| "Extracting this will make it reusable" | Reusable by whom? If there's no second caller now, you're building speculative infrastructure. Extract when the second use exists. |
| "The original author must have had a reason" | Maybe. Check git blame. But copy-paste under time pressure is the most common reason — not design. |
| "I'll refactor while adding this feature" | Separate refactoring from feature work. Mixed changes are harder to review, revert, and understand in history. |

## Red Flags

- Refactoring that requires modifying tests to pass — you likely changed behavior, not just structure
- Extracted function used in only one place — over-extraction; leave it inline
- New shared function that forces callers to handle each other's edge cases — the abstraction is wrong
- Coupling introduced between modules that were previously independent
- Dead code removal that breaks a test — it wasn't dead
- Batching many refactors into one large, hard-to-review commit
- Refactoring code outside the scope of what changed without being asked

## Verification

**Existing tests are read-only.** If a refactoring requires modifying an existing test to pass, stop — you changed behavior, not structure. New tests (characterization tests written before starting) are the only additions allowed.

After completing a refactoring pass:

- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes (no style regressions)
- [ ] Each extracted function has at least two callers — or there's an explicit reason it doesn't yet
- [ ] No new coupling introduced between previously independent modules
- [ ] Removed code was actually dead — confirmed by tests or grep, not assumption
- [ ] The diff is clean — no unrelated changes mixed in
- [ ] Refactored code follows project conventions (checked against AGENTS.md, CLAUDE.md or equivalent)
- [ ] No error handling was removed or weakened
- [ ] A teammate or review agent would approve the change as a net improvement
