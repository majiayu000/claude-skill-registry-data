---
name: refactor-for-clarity
description: Refactor code for clarity without changing behavior. Use when the implementation works but is harder to read, follow, or extend than it needs to be — deep nesting, unclear names, long functions, dense logic. Pairs with refactor-for-reuse (redundancy focus).
metadata:
  version: "1.0.1"
---

# Refactor for Clarity

## Overview

Refactor code so it communicates clearly — to the next developer, and to future-you. The goal is not fewer lines — it's code that's easier to read, follow, and modify without a mental detour. Every change must pass: "Would a new team member understand this faster than the original?"

## When to Use

- After a feature is working and tests pass, but the implementation feels heavier than it needs to be
- During code review when readability or complexity issues are flagged
- When you encounter deeply nested logic, long functions, or unclear names
- When refactoring code written under time pressure

**When NOT to use:**

- Code is already clean and readable — don't refactor for the sake of it
- You don't understand what the code does yet — comprehend before you refactor
- The code is performance-critical and the "simpler" version would be measurably slower
- You're about to rewrite the module entirely — refactoring throwaway code wastes effort
- The issue is duplication, dead code, or missing extraction — use `refactor-for-reuse` instead

## The Five Principles

### 1. Preserve Behavior Exactly

Don't change what the code does — only how it expresses it. All inputs, outputs, side effects, error behavior, and edge cases must remain identical. If you're not sure a refactoring preserves behavior, don't make it.

```
ASK BEFORE EVERY CHANGE:
→ Does this produce the same output for every input?
→ Does this maintain the same error behavior?
→ Does this preserve the same side effects and ordering?
→ Do all existing tests still pass without modification?
```

### 2. Follow Project Conventions

Refactoring means making code more consistent with the codebase, not imposing external preferences. Before refactoring:

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

### 3. Prefer Clarity Over Cleverness

Explicit code is better than compact code when the compact version requires a mental pause to parse.

```python
# UNCLEAR: Chained ternary
label = 'New' if item.is_new else 'Updated' if item.is_updated else 'Archived' if item.is_archived else 'Active'

# CLEAR: Readable early-return function
def get_status_label(item):
    if item.is_new:
        return 'New'
    if item.is_updated:
        return 'Updated'
    if item.is_archived:
        return 'Archived'
    return 'Active'
```

```python
# UNCLEAR: Dense one-liner accumulation
from functools import reduce
count_by_id = reduce(lambda acc, x: {**acc, x.id: acc.get(x.id, 0) + 1}, items, {})

# CLEAR: Named loop
count_by_id = {}
for item in items:
    count_by_id[item.id] = count_by_id.get(item.id, 0) + 1
```

### 4. Maintain Balance

Clarity refactoring has a failure mode: over-simplification. Watch for these traps:

- **Inlining too aggressively** — removing a helper that gave a concept a name makes the call site harder to read
- **Combining unrelated logic** — two simple functions merged into one complex function is not simpler
- **Removing "unnecessary" abstraction** — some abstractions exist for extensibility or testability, not complexity
- **Optimizing for line count** — fewer lines is not the goal; easier comprehension is

### 5. Scope to What Changed

Default to refactoring recently modified code. Avoid drive-by changes to unrelated code unless explicitly asked to broaden scope. Unscoped refactoring creates noise in diffs and risks unintended regressions.

## The Refactoring Process

### Step 1: Verify Test Coverage

Before touching anything, confirm the code you're about to refactor is covered by tests. Tests are the only proof that behavior is preserved after structural changes.

If coverage is missing: invoke **`test-driven-development`** to write characterization tests first — tests that pin the current behavior before any refactoring begins. Commit them before proceeding.

If the code's behavior is unclear before writing tests: invoke **`verify-before-claim`** — open the actual files and confirm what the code does before asserting it.

### Step 2: Understand Before Touching (Chesterton's Fence)

Before changing or removing anything, understand why it exists. This is Chesterton's Fence: if you see a fence across a road and don't understand why it's there, don't tear it down. First understand the reason, then decide if the reason still applies.

```
BEFORE REFACTORING, ANSWER:
- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define the expected behavior?
- Why might it have been written this way? (Performance? Platform constraint? Historical reason?)
- Check git blame: what was the original context for this code?
```

If you can't answer these, you're not ready to refactor. Read more context first.

### Step 3: Identify Clarity Opportunities

Scan for these patterns — each one is a concrete signal, not a vague smell:

**Structural complexity:**

| Pattern | Signal | Refactoring |
|---------|--------|----------------|
| Deep nesting (3+ levels) | Hard to follow control flow | Extract conditions into guard clauses or helper functions |
| Long functions (50+ lines) | Multiple responsibilities | Split into focused functions with descriptive names |
| Nested ternaries | Requires mental stack to parse | Replace with if/else chains, switch, or lookup objects |
| Boolean parameter flags | `doThing(true, false, true)` | Replace with options objects or separate functions |
| Repeated conditionals | Same `if` check in multiple places | Extract to a well-named predicate function |

**Naming and readability:**

| Pattern | Signal | Refactoring |
|---------|--------|----------------|
| Generic names | `data`, `result`, `temp`, `val`, `item` | Rename to describe the content: `userProfile`, `validationErrors` |
| Abbreviated names | `usr`, `cfg`, `btn`, `evt` | Use full words unless the abbreviation is universal (`id`, `url`, `api`) |
| Misleading names | Function named `get` that also mutates state | Rename to reflect actual behavior |
| Comments explaining "what" | `// increment counter` above `count++` | Delete the comment — the code is clear enough |
| Comments explaining "why" | `// Retry because the API is flaky under load` | Keep these — they carry intent the code can't express |

### Step 4: Apply Changes Incrementally

Make one change at a time. Run tests after each change. **Submit refactoring changes separately from feature or bug fix changes.**

```
FOR EACH REFACTORING:
1. Make the change
2. Run the test suite
3. If tests pass → commit (or continue to next)
4. If tests fail → revert and reconsider — do NOT modify tests to force a pass
```

Avoid batching multiple changes into a single untested step. If something breaks, you need to know which change caused it.

**The Rule of 500:** If a refactoring would touch more than 500 lines, invest in automation (codemods, sed scripts, AST transforms) rather than making the changes by hand. Manual edits at that scale are error-prone and exhausting to review.

### Step 5: Verify the Result

After all changes, step back and evaluate the whole:

```
COMPARE BEFORE AND AFTER:
- Is the refactored version genuinely easier to understand?
- Did you introduce any new patterns inconsistent with the codebase?
- Is the diff clean and reviewable?
- Would a teammate approve this change?
```

If the refactored version is harder to understand or review, revert. Not every refactoring attempt succeeds.

## Language-Specific Guidance

```python
# CLARIFY: Verbose dictionary building
# Before
result = {}
for item in items:
    result[item.id] = item.name
# After
result = {item.id: item.name for item in items}

# CLARIFY: Nested conditionals with early return
# Before
def process(data):
    if data is not None:
        if data.is_valid():
            if data.has_permission():
                return do_work(data)
            else:
                raise PermissionError("No permission")
        else:
            raise ValueError("Invalid data")
    else:
        raise TypeError("Data is None")
# After
def process(data):
    if data is None:
        raise TypeError("Data is None")
    if not data.is_valid():
        raise ValueError("Invalid data")
    if not data.has_permission():
        raise PermissionError("No permission")
    return do_work(data)
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's working, no need to touch it" | Working code that's hard to read will be hard to fix when it breaks. Refactoring for clarity now saves time on every future change. |
| "Fewer lines is always simpler" | A 1-line nested ternary is not simpler than a 5-line if/else. Simplicity is about comprehension speed, not line count. |
| "I'll just quickly refactor this unrelated code too" | Unscoped refactoring creates noisy diffs and risks regressions in code you didn't intend to change. Stay focused. |
| "The types make it self-documenting" | Types document structure, not intent. A well-named function explains *why* better than a type signature explains *what*. |
| "The original author must have had a reason" | Maybe. Check git blame — apply Chesterton's Fence. But accumulated complexity often has no reason; it's just the residue of iteration under pressure. |
| "I'll refactor while adding this feature" | Separate refactoring from feature work. Mixed changes are harder to review, revert, and understand in history. |

## Red Flags

- Refactoring that requires modifying tests to pass — you likely changed behavior, not just structure
- Refactored code that is longer and harder to follow than the original
- Renaming things to match your preferences rather than project conventions
- Removing error handling because "it makes the code cleaner"
- Refactoring code you don't fully understand
- Batching many changes into one large, hard-to-review commit
- Refactoring code outside the scope of the current task without being asked

## Verification

**Existing tests are read-only.** If a refactoring requires modifying an existing test to pass, stop — you changed behavior, not structure. New tests (characterization tests written before starting) are the only additions allowed.

After completing a refactoring pass:

- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes (no style regressions)
- [ ] Each change is a reviewable, incremental step
- [ ] The diff is clean — no unrelated changes mixed in
- [ ] Refactored code follows project conventions (checked against AGENTS.md, CLAUDE.md or equivalent)
- [ ] No error handling was removed or weakened
- [ ] No dead code was left behind (unused imports, unreachable branches)
- [ ] A teammate or review agent would approve the change as a net improvement
