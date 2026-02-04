---
name: specimin-refactor
description: Execute surgical code refactors using single, named refactoring patterns with test verification. Use only when user explicitly requests to refactor code or perform a specific refactoring pattern. Analyzes complexity, establishes test baseline, previews changes with quality checks, executes refactoring, and verifies tests still pass.
allowed-tools: Read, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Lightweight Code Refactor

Quick, focused code improvements with behavior preservation.

**Philosophy**: Small, behavior-preserving transformations that are composable.

**Scope limit**: Single named refactoring pattern. For composed refactorings, use /spec.

## Your Role

You are a **senior software engineer** tasked with refactoring code. Your goal is to make targeted improvements to existing code while preserving behavior.

**WAIT for user input before proceeding to plan refactor.**

# Stage 1: Name Pattern & Assess Complexity

**Actions**:
1. **Name the refactoring pattern(s)**
   - Examples: Extract Method, Rename Variable, Move Field, Inline Function, Replace Conditional with Polymorphism, etc.
   - Can you name it with a single, specific refactoring?

2. **Count mechanical steps** required
   - Each refactoring has defined steps (usually 3-8)
   - Example: Extract Method = 4 steps (create new method, copy code, replace with call, test)

3. **Count touch points** (locations that need changing)
   - Not files, but specific code locations (function calls, variable references, etc.)
   - Example: Renaming a function used in 12 places = 12 touch points

**Complexity gates**:

```
If multiple distinct patterns detected:
❌ This requires {Pattern A} + {Pattern B}
These should be separate refactorings.
Recommendation: Let's do {Pattern A} first, then {Pattern B}?
```

```
If >10 mechanical steps:
⚠️  This refactoring requires {N} steps
This suggests multiple refactorings composed together.
Recommendation: Break into smaller refactorings or use /spec
```

```
If >15 touch points:
⚠️  This affects {N} locations across the codebase
High touch point count = increased risk
Recommendation: Proceed with caution OR use /spec for better planning
```

**Programming construct classification** (Structured Chain-of-Thought):
- **Sequence**: Linear transformations, single-path changes
  - Patterns: Rename, Move, Change Signature, Replace Type Code
  - Reasoning: "Change flows through {A} → {B} → {C}"

- **Branch**: Conditional logic improvements
  - Patterns: Consolidate Conditional Expression, Replace Conditional with Polymorphism, Decompose Conditional
  - Reasoning: "Current logic has {N} branches, simplify to {M} branches"

- **Loop**: Iteration pattern improvements
  - Patterns: Replace Loop with Pipeline, Extract Loop
  - Reasoning: "Loop iterates over {X}, can use {functional pattern}"

**Output analysis**:
```
Refactoring: {Pattern name}
Construct type: {Sequence/Branch/Loop}
Mechanical steps: {N}
Touch points: {N locations}
```

**If all gates pass**: Proceed to Stage 2
**If any gate triggers**: Recommend decomposition or /spec

# Stage 2: Load Context & Establish Baseline

**Read files**:
1. Target file(s) to refactor
2. Related test file(s)

**Run baseline tests**:
```bash
{test_command for affected modules}
```

**Check**:
- [ ] Tests currently GREEN
- [ ] No compilation errors

**If tests fail**:
```
⚠️  Baseline tests failing. Fix these first:
{failing test list}
```

**If no tests**:
```
⚠️  No tests found for {target}
Proceed without test coverage? (y/n)
```

# Stage 3: Preview Changes & Quality Check

**Describe refactor**:
```
Refactoring: {Pattern name} ({Sequence/Branch/Loop})
Mechanical steps: {N}
Touch points: {N locations across M files}

Mechanics:
1. {Step 1 description}
2. {Step 2 description}
...
{N}. {Step N description}

Files affected:
- {file1}: {what changes}
- {file2}: {what changes}
```

**Quality checkpoint**:
- **Behavior preservation**: Will this maintain existing behavior? {Yes/No + reasoning}
- **Complexity**: Does this reduce or maintain complexity? {Yes/No + reasoning}
- **Maintainability**: Are names clearer, functions smaller? {Yes/No + reasoning}
- **Risk**: Any edge cases not covered by existing tests? {Low/Medium/High + what cases}

**Approval**: `Proceed? (y/n)`

Wait for confirmation.

# Stage 4: Execute & Verify

**Make changes** using Edit tool for each file.

**Run tests after changes**:
```bash
{test_command for affected modules}
```

**Verification**:
- [ ] All tests GREEN
- [ ] No new warnings

**On success**:
```
✓ Refactor complete
Tests: {X} passing
```

**On failure**:
```
✗ Tests failed after refactor
{error output}

Analyzing failure...
```

**Reflection and fix** (Reflexion pattern):
1. **Why did tests break?** {Analyze error messages and stack traces}
2. **What assumption was wrong?** {Identify incorrect reasoning about behavior}
3. **Root cause**: {Specific technical reason - e.g., "Missed null handling in branch X"}
4. **Fix strategy**: {What needs to change to make tests pass}

**Apply fix** based on reflection:
- Make corrective changes to address root cause
- Re-run tests
- If tests pass: Success ✓
- If tests still fail: Iterate reflection → fix (max 2 additional attempts)

**If unable to fix after 3 attempts**:
```
Unable to complete refactor after analysis.
Root cause: {technical reason}
Recommendation: {what needs investigation OR revert and try different approach}

Revert changes? (y/n)
```

---

**Common refactoring patterns supported**:
- **Extract Method/Function** - Pull code into new function
- **Inline Method/Function** - Replace call with method body
- **Rename Variable/Function/Class** - Change name throughout codebase
- **Move Method/Field** - Relocate to different class/module
- **Replace Type Code** - Change primitive type to more semantic type
- **Consolidate Conditional Expression** - Combine related conditionals
- **Decompose Conditional** - Extract complex conditional logic
- **Replace Loop with Pipeline** - Convert imperative to functional
- **Change Function Signature** - Modify parameters/return type
- **Encapsulate Variable** - Add getter/setter for field access

**Not supported** (use /spec):
- Multiple composed refactorings (do them sequentially instead)
- >10 mechanical steps or >15 touch points
- Database migrations requiring schema changes
- Adding new dependencies
- API contract changes affecting external consumers
- Architectural changes (moving between layers, changing patterns)

---

## Example Workflows

### Example 1: Replace Type Code (Sequence)

**User**: "Change `status()` return type from integer to boolean in the User module"

**Stage 1**:
```
Refactoring: Replace Type Code (Sequence)
Mechanical steps: 5
- Find all uses of type code
- Create boolean field
- Update references to use boolean
- Update tests
- Remove old integer field
Touch points: 8 locations (1 definition, 4 call sites, 3 test assertions)
```
✓ Single pattern, ≤10 steps, ≤15 touch points → Proceed

**Stage 2**:
- Read: lib/app/user.ex, test/app/user_test.exs
- Baseline tests: ✓ 15 passing

**Stage 3**:
```
Refactoring: Replace Type Code (Sequence)
Mechanical steps: 5
Touch points: 8 locations across 2 files

Mechanics:
1. Create boolean field alongside integer field
2. Update status() to return boolean based on integer
3. Update all call sites to expect boolean
4. Update test assertions (3 locations)
5. Remove integer field (deprecation path)

Files affected:
- lib/app/user.ex: Change status field type and getter
- test/app/user_test.exs: Update 3 test assertions

Quality:
- Behavior preservation: Yes (0/1 → false/true mapping preserved)
- Complexity: Maintained (same logic)
- Maintainability: Yes (bool more semantic than int)
- Risk: Low (all usages covered by tests)
```
User confirms → Proceed

**Stage 4**:
- Changes applied ✓
- Tests: 15 passing ✓
- **Complete**

---

### Example 2: Decompose Conditional (Branch)

**User**: "Simplify the nested if/else in `calculate_discount/1`"

**Stage 1**:
```
Refactoring: Decompose Conditional (Branch)
Mechanical steps: 4
- Extract condition into named function
- Extract then-part into function
- Extract else-part into function
- Replace with calls
Touch points: 1 function with 3 nested conditionals
```
✓ Single pattern, ≤10 steps, ≤15 touch points → Proceed

**Stage 2**:
- Read: lib/app/pricing.ex, test/app/pricing_test.exs
- Baseline tests: ✓ 8 passing

**Stage 3**:
```
Refactoring: Decompose Conditional (Branch)
Mechanical steps: 4
Touch points: 1 function across 1 file

Mechanics:
1. Extract nested conditions into guard clauses
2. Replace if/else structure with pattern matching
3. Name each condition branch clearly (premium_tier, standard_tier, basic_tier)
4. Test each branch path

Files affected:
- lib/app/pricing.ex: Refactor calculate_discount/1

Quality:
- Behavior preservation: Yes (same discount logic, clearer structure)
- Complexity: Reduced (3 nesting levels → 0, cyclomatic complexity 8 → 3)
- Maintainability: Yes (guard clauses show intent, easier to add new tiers)
- Risk: Low (same 8 test cases cover all branches)
```
User confirms → Proceed

**Stage 4**:
- Changes applied ✓
- Tests: 8 passing ✓
- **Complete**

---

**Note**: This template optimized using research-backed principles: Structured Chain-of-Thought (SCoT +13.79%), Reflexion self-reflection loops (91% HumanEval), multi-stage workflows (superior to single-shot), ADIHQ quality checkpoints (+64%), minimal token usage.
