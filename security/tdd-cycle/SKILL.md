---
name: tdd-cycle
description: "Red-Green-Refactor TDD loop with mandatory false-positive check. Use when: test, TDD, red-green, failing test, write test first, test-driven."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/tdd-cycle.skill.md"
  tags: "typescript, javascript, python, php, go, rust, java, core"
  core: "true"
  context_cost: "low"
---
# TDD Cycle Skill

## Goal
Implement any feature using strict Test-Driven Development: write the failing test first, implement minimal code to pass it, then refactor. The false-positive check is mandatory.

## Steps

### Phase 1 — Red (Failing Test)

1. **Understand the requirement**
   - Read the relevant task from project/TASKS.md or the user's description
   - Identify the expected behavior as a verifiable predicate
   - Write the requirement in EARS format if not already: "WHEN [X] THE SYSTEM SHALL [Y]"

2. **Write the failing test**
   - Create the test file if it doesn't exist (mirrors source file path in tests/ directory)
   - Write the minimal test that captures the expected behavior
   - Use descriptive test names: `"should return 422 when email is invalid"`
   - Test ONE behavior per test case (single assertion focus)

3. **Run the test — MUST FAIL**
   - Run: `[test command from AGENTS.md]`
   - Confirm the test fails with the expected error (not a different error)
   - **FALSE POSITIVE CHECK:** If the test passes immediately with NO implementation → the test is broken
     - Common causes: wrong file path, wrong import, test assertion always true
     - Fix the test until it genuinely fails for the right reason
   - Record: what error message confirms the correct failure

### Phase 2 — Green (Minimal Implementation)

4. **Write minimal implementation**
   - Write only the code needed to make the failing test pass
   - Do NOT add code for features not tested yet
   - Do NOT optimize prematurely
   - If implementation requires new dependencies: invoke knowledge-gap.skill first

5. **Run the test — MUST PASS**
   - Run: `[test command from AGENTS.md]`
   - Confirm the specific test now passes
   - Confirm ALL other tests still pass (no regressions)
   - If tests fail: invoke self-heal.skill (max 5 attempts before escalation)

### Phase 3 — Refactor

6. **Refactor while green**
   - Improve code quality: extract long functions, improve naming, remove duplication
   - Check: Cyclomatic complexity < 10
   - Check: function length < 30 lines
   - Check: no dead code introduced
   - Run tests after EVERY change — must stay green throughout

7. **Verify final state**
   - Run: `[test command]` → all pass
   - Run: `[typecheck command]` → zero errors
   - Run: `[lint command]` → zero errors
   - Run: `agentic-linter` boundary check → no violations

8. **Mark done**
   - Update task status in project/TASKS.md → DONE
   - Write entry to AUDIT_LOG.md: what was implemented and verified

## Constraints
- NEVER write implementation before the failing test exists
- NEVER skip the false-positive check
- NEVER mark a task DONE if tests are red or lint fails
- NEVER implement more than what is tested

## Output Format
Working implementation with passing tests. Test file and source file updated.
Report: "DONE — [test name] passes. All [N] tests passing. Coverage: [X]%"

## Security & Guardrails

### 1. Skill Security (TDD Cycle)
- **Trivial Red Phase (The Illusion of Failure)**: In Phase 1, the agent must write a failing test. If the agent writes a test that expects a specific string error ("Invalid email format"), but the code fails by throwing a generic NullPointerException, the test is "Red," but for the *wrong reason*. The agent must semantically verify that the Red state directly maps to the exact EARS requirement, rejecting tests that fail due to arbitrary syntax or unrelated setup errors.
- **The "Over-Mocked" Green Phase**: To achieve the "Green" state quickly (Phase 2), the agent might rely entirely on deeply mocking the surrounding architecture (mocking the DB, mocking the auth layer, mocking the validation). While this passes the unit test, it creates a massive blind spot where integration vulnerabilities (like SQL injection) emerge in reality. The agent must limit mocking to true external boundaries, testing business logic against real or purely in-memory data structures whenever possible.

### 2. System Integration Security
- **Test-Induced State Ruin**: When running tests locally or in a shared CI environment, a poorly written failing test might permanently mutate a shared development database or leave dangling file locks, disrupting other team members or parallel sub-agents. The agent must rigorously implement setup/teardown hooks (`beforeEach`/`afterEach`) that cryptographically guarantee environmental state isolation and cleanup, regardless of whether the test passes or fails.
- **Coverage Masking**: In Phase 2, the agent might write the minimum code to pass. If the test only checks the "Happy Path," the "minimal" implementation will completely omit error handling, input validation, and boundary checks. This artificially inflates test coverage while leaving the application highly vulnerable. The agent must be forced to write separate, explicit "Red" tests for edge cases, null states, and malicious inputs before the TDD cycle is considered complete for a feature.

### 3. LLM & Agent Guardrails
- **The Self-Heal Infinite Loop**: In Phase 2 (Step 5), if tests fail, `self-heal.skill` is invoked. An LLM stuck on a logical error might enter a loop of tweaking variables, running tests, failing, and tweaking again without understanding the underlying math or architecture. The orchestrator must strictly enforce the `max 5 attempts` limit. Upon hitting the limit, the agent must physically lock the task and immediately escalate to human review.
- **Hallucinated Test Framework Syntax**: The LLM might confidently generate test syntax that belongs to a different framework (e.g., writing Jest assertions in a Pytest file, or attempting to use `.resolves` on a synchronous function). This creates a syntax error rather than a genuine "Red" test failure. The agent must strictly validate its generated test syntax against the project's explicit testing ecosystem (Vitest/Jest/Pest) before classifying the failure state.
