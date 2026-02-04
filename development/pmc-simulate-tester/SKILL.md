---
name: pmc-simulate-tester
description: Simulate the tester workflow step-by-step with real ticket system. Executes test loading, running, verification, and merging with explicit ENTER/EXIT stage declarations. Use this skill to debug, understand, or manually run the tester workflow.
---

# PMC Simulate Tester

Manually simulate the tester workflow step-by-step, executing shell scripts and test operations with explicit stage declarations.

## Required Context

Before starting, you need:
- `ticket_id`: Ticket ID (e.g., T00001)
- `mode`: Test mode - `all` | `single` | `ticket-completion` (default: all)
- `test_id`: Specific test ID (required for mode=single)
- `working_dir`: Project working directory

## Workflow Overview

```
tester.workflow
├── load_tests (shell) ─────────────→ run_tests
├── run_tests (claude) ─────────────→ verification_setup
├── verification_setup (shell) ─────→ verify
├── verify (claude) ────────────────→ merge
├── merge (shell) ──────────────────→ report
├── report (shell) ─────────────────→ terminal_success
└── terminal_error (on any failure)
```

## Execution Instructions

For each state, declare entry and exit explicitly:

```
ENTER STAGE: tester.workflow.{state_name}
  [perform actions]
EXIT STAGE: tester.workflow.{state_name} → {next_state} (reason: {why})
```

---

## State: load_tests

**Type:** shell
**Script:** `load-tests.sh`

```
ENTER STAGE: tester.workflow.load_tests
```

**Execute this logic:**

1. Set paths:
   ```
   TESTS_DIR = {working_dir}/docs/3-tests/tickets/{ticket_id}
   DEFINITION_FILE = TESTS_DIR/tests-definition.json
   PROGRESS_FILE = TESTS_DIR/tests-in-progress.json
   VERIFICATION_FILE = TESTS_DIR/tests-in-verification.json
   ```

2. Check `tests-definition.json` exists:
   - If NOT exists → `terminal_error`

3. Remove working files if they exist:
   - Delete `tests-in-progress.json`
   - Delete `tests-in-verification.json`

4. Load and filter tests based on mode:

   | Mode | Filter Logic |
   |------|--------------|
   | `all` | Include all tests |
   | `single` | Include only test where `id == test_id` |
   | `ticket-completion` | Include only tests where `ticket-completion == true` |

5. Write filtered tests to `tests-in-progress.json`:
   ```json
   {
     "ticket": "{ticket_id}",
     "title": "...",
     "tests": [filtered tests]
   }
   ```

6. Report: `Loaded {N} tests (mode: {mode})`

```
EXIT STAGE: tester.workflow.load_tests → run_tests (loaded: {N} tests)
```

**Error:** If tests-definition.json not found:
```
EXIT STAGE: tester.workflow.load_tests → terminal_error (tests-definition.json not found)
```

---

## State: run_tests

**Type:** claude
**Session:** start

```
ENTER STAGE: tester.workflow.run_tests
```

**Use the `run-tests` skill** to execute tests for ticket {ticket_id}.

The run-tests skill will:
1. Read `tests-in-progress.json`
2. Execute each test step
3. Record trajectory (actions taken)
4. Mark `passes: true/false` for each test
5. Update `tests-in-progress.json` with results

**Output JSON:**
```json
{
  "tests_executed": N,
  "tests_passed": N,
  "tests_failed": N,
  "tests_blocked": N
}
```

```
EXIT STAGE: tester.workflow.run_tests → verification_setup (executed: {N}, passed: {N})
```

---

## State: verification_setup

**Type:** shell
**Script:** `verification-setup.sh`

```
ENTER STAGE: tester.workflow.verification_setup
```

**Execute this logic:**

1. Check `tests-in-progress.json` exists:
   - If NOT exists → `terminal_error`

2. Copy to `tests-in-verification.json` with field resets:

   | Field | Action |
   |-------|--------|
   | `passes` | Reset to `false` |
   | `blocked` | Reset to `false` |
   | `step.verified` | Reset to `false` for each step |
   | `step.trajectory` | **Keep intact** (don't reset) |

3. Write `tests-in-verification.json`

4. Report: `Created tests-in-verification.json, reset verified/passes for {N} tests`

```
EXIT STAGE: tester.workflow.verification_setup → verify (tests prepared: {N})
```

**Error:** If tests-in-progress.json not found:
```
EXIT STAGE: tester.workflow.verification_setup → terminal_error (tests-in-progress.json not found)
```

---

## State: verify

**Type:** claude
**Session:** start

```
ENTER STAGE: tester.workflow.verify
```

**Use the `verify-tests` skill** to verify tests for ticket {ticket_id}.

The verify-tests skill will:
1. Read `tests-in-verification.json`
2. Follow recorded trajectories from run phase
3. Independently verify each step
4. Mark `verified: true/false` for each step
5. Mark `passes: true/false` for each test
6. Note any discrepancies between run and verify
7. Update `tests-in-verification.json` with results

**Output JSON:**
```json
{
  "tests_verified": N,
  "tests_passed": N,
  "tests_failed": N,
  "tests_blocked": N,
  "discrepancies": ["test_id: description of discrepancy", ...]
}
```

```
EXIT STAGE: tester.workflow.verify → merge (verified: {N}, discrepancies: {N})
```

---

## State: merge

**Type:** shell
**Script:** `merge-results.sh`

```
ENTER STAGE: tester.workflow.merge
```

**Execute this logic:**

1. Check `tests-in-verification.json` exists:
   - If NOT exists → `terminal_error`

2. If `tests-results.json` doesn't exist:
   - If `tests-definition.json` exists → copy to create results
   - Else → `terminal_error`

3. Merge verification results into results:
   ```python
   # Pseudocode
   results_by_id = {t['id']: t for t in results_tests}

   for verified_test in verification_tests:
       results_by_id[verified_test['id']] = verified_test

   results['tests'] = list(results_by_id.values())
   ```

4. Write merged `tests-results.json`

5. Report: `Merged {N} tests into tests-results.json`

```
EXIT STAGE: tester.workflow.merge → report (merged: {N} tests)
```

**Error:** If required files not found:
```
EXIT STAGE: tester.workflow.merge → terminal_error (missing files)
```

---

## State: report

**Type:** shell
**Script:** `report.sh`

```
ENTER STAGE: tester.workflow.report
```

**Execute this logic:**

1. Read `tests-in-verification.json`

2. Calculate statistics:
   ```
   total = len(tests)
   passed = count where passes == true
   blocked = count where blocked == true
   failed = total - passed

   # Ticket-completion subset
   tc_tests = tests where ticket-completion == true
   tc_total = len(tc_tests)
   tc_passed = count where passes == true
   tc_blocked = count where blocked == true
   ```

3. Identify test lists:
   ```
   failed_tests = [id for tests where passes==false and blocked==false]
   blocked_tests = [id for tests where blocked==true]
   ```

4. Generate report:
   ```json
   {
     "total": N,
     "passed": N,
     "failed": N,
     "blocked": N,
     "ticket_completion_total": N,
     "ticket_completion_passed": N,
     "ticket_completion_blocked": N,
     "failed_tests": ["id", ...],
     "blocked_tests": ["id", ...],
     "all_passed": true|false,
     "ticket_completion_done": true|false
   }
   ```

5. Print report JSON

```
EXIT STAGE: tester.workflow.report → terminal_success
```

---

## Terminal States

```
ENTER STAGE: tester.workflow.terminal_success
  Status: success
  [Workflow completed successfully]
EXIT STAGE: tester.workflow.terminal_success (workflow complete)

ENTER STAGE: tester.workflow.terminal_error
  Status: failure
  Message: "Tester workflow failed"
EXIT STAGE: tester.workflow.terminal_error (workflow failed)
```

---

## File Flow Diagram

```
tests-definition.json (READ-ONLY source)
        │
        ▼ load_tests (filter by mode)
tests-in-progress.json
        │
        ▼ run_tests (execute, record trajectory)
tests-in-progress.json (updated with trajectory, passes)
        │
        ▼ verification_setup (copy, reset passes/verified)
tests-in-verification.json
        │
        ▼ verify (follow trajectory, verify independently)
tests-in-verification.json (updated with verified, passes)
        │
        ▼ merge (merge into results by test id)
tests-results.json (final merged results)
        │
        ▼ report (generate summary)
[JSON report output]
```

---

## Example Simulation Output

```
=== TESTER WORKFLOW SIMULATION ===
Context: ticket_id=T00001, mode=single, test_id=T00001-03, working_dir=/project

ENTER STAGE: tester.workflow.load_tests
  TESTS_DIR: /project/docs/3-tests/tickets/T00001
  tests-definition.json exists: YES
  Removing tests-in-progress.json: DONE
  Removing tests-in-verification.json: DONE
  Mode: single, test_id: T00001-03
  Filtered: 1 test
  Writing tests-in-progress.json
EXIT STAGE: tester.workflow.load_tests → run_tests (loaded: 1 tests)

ENTER STAGE: tester.workflow.run_tests
  Using run-tests skill...
  Executing test T00001-03: "User can save document"
  Step 1: Open application → DONE (trajectory recorded)
  Step 2: Create new document → DONE (trajectory recorded)
  Step 3: Click save button → DONE (trajectory recorded)
  Step 4: Verify file exists → DONE (trajectory recorded)
  Test result: PASSED
EXIT STAGE: tester.workflow.run_tests → verification_setup (executed: 1, passed: 1)

ENTER STAGE: tester.workflow.verification_setup
  tests-in-progress.json exists: YES
  Creating tests-in-verification.json
  Reset passes=false, verified=false for 1 test
  Keeping trajectory intact
EXIT STAGE: tester.workflow.verification_setup → verify (tests prepared: 1)

ENTER STAGE: tester.workflow.verify
  Using verify-tests skill...
  Following trajectory for T00001-03...
  Step 1: Open application → verified: YES
  Step 2: Create new document → verified: YES
  Step 3: Click save button → verified: YES
  Step 4: Verify file exists → verified: YES
  Test result: PASSED (verified independently)
EXIT STAGE: tester.workflow.verify → merge (verified: 1, discrepancies: 0)

ENTER STAGE: tester.workflow.merge
  tests-in-verification.json exists: YES
  tests-results.json exists: YES
  Merging 1 test by id
  Writing tests-results.json
EXIT STAGE: tester.workflow.merge → report (merged: 1 tests)

ENTER STAGE: tester.workflow.report
  Reading tests-in-verification.json
  Report:
  {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "blocked": 0,
    "ticket_completion_total": 1,
    "ticket_completion_passed": 1,
    "all_passed": true,
    "ticket_completion_done": true
  }
EXIT STAGE: tester.workflow.report → terminal_success

ENTER STAGE: tester.workflow.terminal_success
EXIT STAGE: tester.workflow.terminal_success (workflow complete)
```

---

## Quick Reference

| State | Type | Exit Code → Target |
|-------|------|-------------------|
| load_tests | shell | 0 → run_tests, else → terminal_error |
| run_tests | claude | default → verification_setup |
| verification_setup | shell | 0 → verify, else → terminal_error |
| verify | claude | default → merge |
| merge | shell | 0 → report, else → terminal_error |
| report | shell | default → terminal_success |

## Test Mode Reference

| Mode | Description | Use Case |
|------|-------------|----------|
| `all` | Run all tests in definition | Full test suite |
| `single` | Run one specific test | After implementing a feature |
| `ticket-completion` | Run only completion tests | Final verification before completion |
