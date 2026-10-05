---
name: tdd
description: "Implements features using strict test-driven development — red-green-refactor cycle. Writes a failing test first, then minimal code to pass, then refactors. Use when building features that need high reliability."
argument-hint: "[feature or function to implement]"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Test-Driven Development

## Detect Test Environment
!`ls package.json pytest.ini pyproject.toml go.mod Cargo.toml *.csproj Gemfile mix.exs 2>/dev/null`
!`find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5`

---

## The TDD Cycle

For the requested feature, repeat this cycle until complete:

### RED — Write a Failing Test
1. Write the smallest possible test that describes the next piece of behavior
2. The test must import/reference the function or module (even if it doesn't exist yet)
3. Run the test — it MUST fail
4. Verify the failure message is meaningful (not just a compilation error)

### GREEN — Make It Pass
1. Write the absolute minimum code to make the test pass
2. Hardcoding is acceptable at this stage — it will be cleaned up in refactor
3. Don't add functionality the test doesn't require
4. Run the test — it MUST pass
5. Run all related tests — nothing else should break

### REFACTOR — Clean Up
1. Remove duplication in both production and test code
2. Improve naming, extract methods, simplify logic
3. Run tests after every refactoring step — they must stay green
4. Stop when the code is clean

## Test Progression
Start simple, add complexity gradually:
1. Null/empty/zero case
2. Single item / simplest valid input
3. Multiple items / typical case
4. Edge cases / boundary values
5. Error cases / invalid input
6. Async / concurrent behavior (if applicable)

## Output
- Show each cycle clearly: RED (test code + failure), GREEN (impl + pass), REFACTOR
- Display test runner output at each step
- Final summary: all tests, coverage of the feature

## Rules
- NEVER write implementation before a failing test
- NEVER skip the refactor step
- One behavior per cycle — don't batch multiple features
- If the test framework isn't set up, set it up first
