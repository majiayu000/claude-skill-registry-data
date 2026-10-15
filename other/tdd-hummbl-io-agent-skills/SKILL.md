---
name: tdd
description: RED-GREEN-REFACTOR cycle enforcement for test-driven development.
version: 0.1.0
execution-mode: remedial
argument-hint: <description of feature or fix>
category: dev-tools
status: candidate
---
# TDD Command

Enforce a strict RED-GREEN-REFACTOR test-driven development cycle.

## Usage

```bash
[tdd] Add retry logic to circuit breaker
[tdd] Fix delegation token expiry off-by-one
```

## Execution

### Phase 1: RED (Write a failing test)

1. **Ask** the user to clarify the expected behavior if `$ARGUMENTS` is ambiguous.
2. **Write the test first** in the appropriate test file under `$PROJECT_ROOT/tests/`.
3. **Run the test** and verify it **FAILS**:
   ```bash
   python -m pytest <test_file>::<test_function> -v
   ```
4. **Hard gate**: The test MUST fail. If it passes, the behavior already exists -- inform the user and stop.
5. **Commit** with message: `test: add failing test for <description>`

### Phase 2: GREEN (Minimal implementation)

1. Write the **minimum code** to make the test pass. No extras.
2. **Run the test** and verify it **PASSES**:
   ```bash
   python -m pytest <test_file>::<test_function> -v
   ```
3. **Hard gate**: The test MUST pass. If it fails, fix the implementation (not the test).
4. **Run the full suite** to check for regressions:
   ```bash
   python -m pytest $PROJECT_ROOT/tests/ -x -q
   ```
5. **Commit** with message: `feat: implement <description>` or `fix: <description>`

### Phase 3: REFACTOR (Clean up)

1. Review the implementation for clarity, duplication, naming.
2. Make improvements **without changing behavior** (tests must still pass).
3. **Run the full suite** again to confirm no regressions.
4. **Commit** with message: `refactor: clean up <description>`

## Output Format

Report status at each phase gate:

```
TDD Cycle | <description>
═════════════════════════

🔴 RED    — Test written: <test_file>::<test_name>
           Result: FAIL (expected) ✓

🟢 GREEN  — Implementation: <file>:<lines>
           Result: PASS ✓
           Regressions: 0

🔵 REFACTOR — Changes: <summary>
              Result: PASS ✓
              Regressions: 0
```

## Constraints

- **Never skip a phase.** The gates are mandatory.
- Write the test BEFORE any implementation code.
- The GREEN phase implements the MINIMUM to pass -- no gold-plating.
- If the user asks to skip RED, explain why it matters but comply if they insist.
- All commits use conventional commit format.
