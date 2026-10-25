---
name: ami-create-tests
description: Must be triggered when new functionality is added and no existing tests cover the changes. Automatically generates tests for modified code.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: PR Test Creator

When invoked, act as a Test Automation Engineer to ensure the repository has adequate test coverage before a PR is published.

## Workflow

1. **Assess Coverage:**
   - Review the modified or target files (from the PR, working tree, or as specified by the user).
   - Scan the repository for corresponding test files (e.g., look for `*test.py`, `*.spec.js`, `*_test.go`).
   - Determine if the modified logic is adequately covered by existing tests.

2. **Generate Tests (If Needed):**
   - If tests are missing or insufficient, determine the exact test cases needed.
   - **CRITICAL:** Before writing any tests to disk, you MUST present a summary to the user in the chat explaining *what* exactly you are going to test, the *amount* of tests you will write, and any suggested changes to the existing test structure to better cover the new cases.
   - Ask for the user's explicit permission to proceed.
   - Upon approval, automatically generate the missing tests:
     - Use the appropriate testing framework for the project (e.g., pytest, jest, vitest, etc.).
     - **Keep Tests Lean & Pragmatic:** Write clear, direct assertions. Avoid unnecessary mock frameworks or overly complex test abstraction layers for simple test scenarios.
     - **DRY Test Setup:** Extract common fixture setup, recurring sample payloads, or teardown logic into shared test helper modules instead of copy-pasting setup blocks across tests.
     - Create or update the relevant test files, verifying both the happy path and critical edge cases.

3. **Reporting:**
   - If tests were created or updated, output the list of test files modified.
   - If coverage was already sufficient, output: **"TEST COVERAGE SUFFICIENT - NO NEW TESTS NEEDED"**.


---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
