---
name: tdd
description: "Use when implementing features or fixing bugs with test-driven development. Enforces RED→GREEN→REFACTOR cycle with vertical slicing and multi-agent context isolation. Triggers on: 'implement with TDD', 'write tests first', 'red green refactor', 'test-driven', '/tdd <feature>'. Supports Jest, Vitest, pytest, Go test, cargo test, RSpec, PHPUnit."
---

# TDD Skill — Red Green Refactor

Enforce disciplined RED→GREEN→REFACTOR cycles using multi-agent context isolation.
The core constraint: **Test Writer never sees implementation. Implementer never sees the spec.**
This prevents the model from leaking implementation intent into test design.

## Invocation

| Form | Behavior |
|------|----------|
| `/tdd <feature>` | Interactive — pause for approval at each checkpoint |
| `/tdd --auto <feature>` | Autonomous — run all slices, stop only on unrecoverable error |
| `/tdd --resume` | Resume from `.tdd-state.json` in project root |
| `/tdd --dry-run <feature>` | Validate pipeline, render prompts, write no code |

## Architecture

```
ORCHESTRATOR (this skill)
├─ Phase 0: Setup    — detect framework, verify baseline
├─ Phase 1: Decompose — vertical slices, user approves
│
├─ FOR EACH SLICE:
│   ├─ Phase 2 RED:      Task(Test Writer)   ← spec + API only
│   ├─ Phase 3 GREEN:    Task(Implementer)   ← failing test + error only
│   └─ Phase 4 REFACTOR: Task(Refactorer)   ← all code + green results
│
└─ Phase 5: Summary
```

### Context Boundaries

| Agent | Sees | Does NOT See |
|-------|------|--------------|
| **Test Writer** | Slice spec, public API signatures, framework conventions | Implementation code, other slices, plans |
| **Implementer** | Failing test code, error output, file tree, existing source | Original spec, slice descriptions |
| **Refactorer** | All implementation + all tests + green results | Original spec, decomposition rationale |

---

## Phase 0 — Setup

### Step 1: Detect framework

```bash
ls package.json pyproject.toml go.mod Cargo.toml Gemfile composer.json 2>/dev/null
```

Map to framework:
- `package.json` → check scripts for `jest` or `vitest`
- `pyproject.toml` or `pytest.ini` → pytest
- `go.mod` → go test
- `Cargo.toml` → cargo test
- `Gemfile` → rspec
- `composer.json` → phpunit

If ambiguous, ask: "What command runs your tests?"

### Step 2: Verify green baseline

Run the full test suite and show output:

```bash
# Jest/Vitest
npx jest --passWithNoTests 2>&1 | tail -10
# or: npx vitest run 2>&1 | tail -10

# pytest
python -m pytest -q 2>&1 | tail -10

# Go
go test ./... 2>&1 | tail -10

# Cargo
cargo test 2>&1 | tail -10

# RSpec
bundle exec rspec --format progress 2>&1 | tail -10
```

- **All pass** → proceed
- **Tests fail** → STOP. "Existing tests are failing. TDD requires a green baseline before starting."
- **No tests / error with 0 tests** → greenfield project, proceed

### Step 3: Extract public API surface

```bash
# TypeScript/JS — exported symbols
grep -rn "^export " src/ --include="*.ts" --include="*.js" 2>/dev/null | head -60

# Python — public functions/classes
grep -rn "^def \|^class " src/ --include="*.py" 2>/dev/null | grep -v "^.*test" | head -60

# Go — exported identifiers (capital-letter functions/types)
grep -rn "^func [A-Z]\|^type [A-Z]" . --include="*.go" 2>/dev/null | grep -v "_test.go" | head -60
```

Save output as `{API_SURFACE}`. Empty on greenfield — that's fine.

### Step 4: Create state file `.tdd-state.json`

```json
{
  "feature": "<user description>",
  "framework": "<jest|vitest|pytest|go|cargo|rspec|phpunit>",
  "language": "<typescript|javascript|python|go|rust|ruby|php>",
  "test_command": "<full command>",
  "source_dir": "src/",
  "auto_mode": false,
  "slices": [],
  "current_slice": 0,
  "phase": "setup",
  "files_modified": [],
  "test_files_created": []
}
```

---

## Phase 1 — Decompose into Vertical Slices

Break the feature into **ordered, testable behaviors** — one behavior per slice.

### Inside-Out Ordering

Sort slices from innermost to outermost layer:

1. **domain** — pure business logic, no dependencies, no mocks
2. **domain-service** — cross-aggregate operations using real domain objects
3. **application** — use-case orchestration with in-memory fakes for ports
4. **infrastructure** — repos, external APIs, framework adapters

**Why inside-out?** Domain slices produce real objects that later slices use directly. Minimizes mocking, catches integration issues early, ensures business rules exist before infrastructure.

Present to user:

```
I've broken this into N slices (inside-out order):

Domain:
  1. [behavior] — [what the test verifies]

Application:
  2. [behavior] — [what the test verifies]

Infrastructure:
  3. [behavior] — [what the test verifies]

Each slice: RED → GREEN → REFACTOR before the next.
Does this look right?
```

**Wait for approval** — even in `--auto` mode. Slice decomposition always needs sign-off.

Update state: write `slices` array with `layer` field on each.

---

## Phase 2 — RED: Write One Failing Test

### Step 1: Refresh API surface (re-run grep from Phase 0 Step 3)

### Step 2: Launch Test Writer

```
Task(subagent_type="general-purpose", prompt="""
You are the Test Writer. Your ONLY job is to write ONE failing test for this behavior.

BEHAVIOR TO TEST:
{SLICE_SPEC}

PUBLIC API (what you may call):
{API_SURFACE}

LANGUAGE: {LANGUAGE}
TEST FRAMEWORK: {FRAMEWORK}
TEST FILE: {TEST_FILE_PATH}
EXISTING TEST FILE CONTENT (if any): {EXISTING_TEST_CONTENT}

STRICT CONSTRAINTS:
- Write exactly ONE test function
- The test MUST fail because the behavior doesn't exist yet
- Do NOT look at or guess implementation details
- Use real objects — no mocks for domain-layer tests
- Test name must describe the behavior, not the implementation
- For domain layer: never import mocking libraries

Return ONLY a JSON object:
{
  "test_name": "descriptive_test_name",
  "test_file_path": "path/to/test_file",
  "imports_needed": ["import statements"],
  "test_code": "complete test function code",
  "description": "one sentence: what behavior this verifies"
}
""")
```

### Step 3: Write the test file

Apply the test code. If file exists, append the test function. If new, create it.

### Step 4: Run to confirm RED

```bash
# Run only the new test
# Jest: npx jest --testPathPattern=<file> -t "<test_name>"
# pytest: pytest <file>::<test_name> -v
# Go: go test -run <TestName> ./...
```

Show full output.

| Result | Action |
|--------|--------|
| Assertion failure | **Proper RED** — proceed |
| Import/module error | Create minimal stub so import resolves, re-run |
| Test passes | Behavior already exists — log "skip: already implemented", move to next slice |
| Syntax error | Fix test file, re-run. After 2 attempts, ask user |

### Step 5 (interactive only): Present checkpoint

```
RED: Test failing as expected.

Test: {test_name}
File: {test_file_path}
Failure: {error message}
Verifies: {description}

Proceed to GREEN? (or adjust the test?)
```

---

## Phase 3 — GREEN: Minimal Implementation

### Step 1: Collect context (test code + error output only)

```bash
cat {TEST_FILE_PATH}
# + failure output from Phase 2 Step 4
```

### Step 2: Build source file tree

```bash
find {SOURCE_DIR} -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.rb" -o -name "*.php" \) \
  | grep -v test | grep -v spec | grep -v node_modules | grep -v __pycache__ | head -50
```

### Step 3: Launch Implementer

```
Task(subagent_type="general-purpose", prompt="""
You are the Implementer. Your ONLY job is to make this failing test pass.

FAILING TEST:
{FAILING_TEST_CODE}

TEST FAILURE OUTPUT:
{TEST_FAILURE_OUTPUT}

SOURCE FILE TREE:
{FILE_TREE}

EXISTING SOURCE (relevant files):
{EXISTING_SOURCE}

LAYER CONSTRAINT: {LAYER}
- domain: no imports from application or infrastructure
- domain-service: may use domain objects, no infrastructure imports
- application: may use ports/interfaces, no concrete infrastructure
- infrastructure: no restrictions

STRICT CONSTRAINTS:
- Write the MINIMUM code to pass this one test
- Do NOT read the original spec or feature description
- Do NOT implement anything not required by the test
- One file change at a time where possible

Return ONLY a JSON object:
{
  "explanation": "what you implemented and why",
  "files": [
    {
      "path": "relative/path/to/file.ts",
      "action": "create|overwrite|edit",
      "content": "complete file content"
    }
  ]
}
""")
```

### Step 4: Apply changes and verify GREEN

Apply each file. Then run the specific test:

```bash
# Same command as Phase 2 Step 4
```

**Retry loop** (max 5 attempts):
- If still failing: re-launch fresh Implementer with previous attempt's explanation + new error
- If failing after 5 attempts: STOP, present to user

### Step 5: Run full suite — check for regressions

```bash
# Full test command (same as Phase 0 Step 2)
```

- Regressions found → launch fresh Implementer targeting only the regression failures, up to 3 attempts
- Still regressing after 3 → STOP, ask user

### Step 6 (interactive only): Present checkpoint

```
GREEN: Test passing.

Implementation: {explanation}
Files changed: {list}
Full suite: {N} passing, {N} failing

Proceed to REFACTOR? (or adjust?)
```

---

## Phase 4 — REFACTOR

### Step 1: Launch Refactorer

```
Task(subagent_type="general-purpose", prompt="""
You are the Refactorer. Tests are green. Improve the code without changing behavior.

GREEN TEST OUTPUT:
{GREEN_TEST_OUTPUT}

ALL TEST CODE:
{ALL_TEST_CODE}

ALL IMPLEMENTATION CODE:
{ALL_IMPLEMENTATION_CODE}

LAYER(S) TOUCHED: {SLICE_LAYERS}

YOUR JOB:
- Remove duplication
- Improve naming
- Simplify logic
- Fix dependency direction violations (inner layers must not import outer)
- Do NOT add features not tested

Return ONLY a JSON object:
{
  "suggestions": [
    {
      "priority": "high|medium|low",
      "description": "what and why",
      "file": "path/to/file",
      "old_code": "exact code to replace",
      "new_code": "replacement code"
    }
  ]
}
Return empty suggestions array if nothing needs changing.
""")
```

### Step 2: Apply suggestions one at a time (high priority first)

For each suggestion:
1. Apply the edit
2. Run full test suite
3. If any test fails → **revert immediately**, skip this suggestion
4. If all pass → keep the change

### Step 3 (interactive only): Report

```
REFACTOR: {N} applied, {N} skipped (reverted on test failure).
All tests: {count} passing.
```

---

## Phase 5 — Next Slice or Complete

- More slices → increment `current_slice`, return to Phase 2
- All slices done → present summary:

```
TDD Complete: {feature}

Slices: {N}
Tests written: {N}
Files created/modified: {list}
All tests passing: yes
```

Remove `.tdd-state.json` (ask in interactive mode, silent in `--auto`).

---

## Resume Support

`/tdd --resume`:
1. Read `.tdd-state.json`
2. Report: "Found session for '{feature}'. Slice {N}/{total}, phase: {phase}."
3. Resume from current phase of current slice

---

## Dry-Run Mode

For `--dry-run`: run Phase 0 and Phase 1 fully, then for each slice render the three agent prompts with variables filled in but **call no Task() and write no files**. Print prompt sizes and variable resolution status. Report summary. Do not clean up state file.

---

## Edge Cases

**Greenfield**: No tests yet — proceed from Phase 0. Test Writer creates test files and framework config from scratch.

**Bug fix**: Write a test demonstrating the bug (RED confirms bug exists). Fix in GREEN. Verify with `verify-before-done` skill after completing.

**Flaky test**: If a test sometimes passes/fails — stop, report, fix flakiness before continuing.

**User-provided test**: Confirm it fails (RED), skip to Phase 3 (GREEN). Do not modify without asking.

---

## Constraints

- Never write implementation before a failing test exists.
- Never modify a test to make it pass — fix the implementation.
- Never write all tests upfront — one slice at a time.
- Never skip RED phase, even for "trivial" cases.
- Domain code must never import infrastructure — dependency direction is inward only.
- After all slices: run `verify-before-done` skill before claiming done.
- On unexpected errors: use `debug-protocol` skill — do not guess fixes.

---

## Framework Quick Reference

| Framework | Single test | Full suite |
|-----------|------------|------------|
| Jest | `npx jest -t "<name>" <file>` | `npx jest` |
| Vitest | `npx vitest run <file> -t "<name>"` | `npx vitest run` |
| pytest | `pytest <file>::<name> -v` | `pytest -v` |
| Go | `go test -run <Name> ./...` | `go test ./...` |
| Cargo | `cargo test <name>` | `cargo test` |
| RSpec | `rspec <file>:<line>` | `rspec` |
| PHPUnit | `phpunit --filter <name>` | `phpunit` |

---

Attribution: Core RED→GREEN→REFACTOR orchestration pattern and context-isolation architecture adapted from glebis/claude-skills (MIT License). Rewritten for YAMTAM ENGINE — self-contained, no external scripts, integrated with verify-before-done and debug-protocol skills.
