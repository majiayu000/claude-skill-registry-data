---
name: refactor
description: "Analyzes code for smells and structural issues, proposes a safe refactoring plan, and executes it with test verification. Use when code is hard to read, maintain, or extend."
argument-hint: "[file, function, or module to refactor]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Safe Code Refactoring

## Context
!`git status --short 2>/dev/null`
!`git stash list 2>/dev/null`

---

## Refactoring Process

### Step 1: Analyze — Identify Code Smells
Read the target code and identify issues from this list:

- **Long Method/Function** (>40 lines): Extract smaller, focused functions
- **Deep Nesting** (>3 levels): Use early returns, guard clauses, or extract methods
- **Code Duplication**: Extract shared logic into reusable functions
- **God Class/Module**: Split into focused, single-responsibility modules
- **Feature Envy**: Move logic to the class/module that owns the data
- **Primitive Obsession**: Replace related primitives with a proper type/struct/class
- **Long Parameter List** (>4 params): Use an options/config object or builder pattern
- **Dead Code**: Remove unused functions, imports, variables, and commented-out code
- **Magic Numbers/Strings**: Extract into named constants
- **Inconsistent Naming**: Align with project conventions
- **Missing Abstractions**: Introduce interfaces/traits where concrete types are overused
- **Tight Coupling**: Introduce dependency injection or interface boundaries

### Step 2: Plan — Define the Refactoring Strategy
For each identified issue:
1. Name the specific refactoring technique (Extract Method, Move Function, Introduce Parameter Object, etc.)
2. Describe the before and after state
3. Assess the risk (High/Medium/Low) — does it touch public API? Does it cross module boundaries?
4. List affected files

**Present the plan to the user before executing.**

### Step 3: Verify — Check for Existing Tests
- Find all tests that cover the code being refactored
- Run them to establish a green baseline
- If no tests exist, flag this as a risk and recommend writing tests first

### Step 4: Execute — Apply Changes
- Make one refactoring change at a time
- After each change, verify:
  - The code still compiles/parses
  - Existing tests still pass
  - No new linting errors
- If a change breaks something, revert it immediately

### Step 5: Validate — Final Checks
- Run the full test suite for the affected area
- Verify no regressions via `git diff`
- Ensure the refactored code is actually simpler/cleaner than before
- If it isn't, consider reverting — refactoring should reduce complexity, not just move it

---

## Rules
- **Never change behavior** — refactoring is about structure, not features
- **Never skip tests** — if tests don't exist, say so and suggest writing them first
- **Small steps** — one technique per commit if possible
- **Respect scope** — don't refactor code outside the requested area
- **Keep the diff minimal** — don't reformat untouched code
