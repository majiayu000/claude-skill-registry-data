---
name: tidy
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
  - Workflow
description: TDD Production Code Refactoring Process. Triggers on 'tidy up', 'tidy this', 'clean up code'. Use for refactoring production code with test coverage.
metadata:
  author: Fishbowl Team
  version: "0.2.0"
---

# TDD Production Code Refactoring Process

STARTER_CHARACTER = 🟣

**NEVER** make changes to Test code in this process.

This process is for refactoring production code with test coverage.

## Initial Setup

1. **Locate Test File Proactively**
   - If user provides a file path, search for its test file using common patterns:
     - `filename.test.ext`, `filename.spec.ext`
     - `__tests__/filename.ext`
     - `tests/filename.ext`
     - Mirror path with `/test/` instead of `/src/`
   - Use Glob and Grep to search multiple patterns in parallel
   - If multiple test files found, show options and ask which one
   - If no test file found, inform user and ask them to provide the test file path
   - **Only ask user if ambiguous or not found** - otherwise proceed automatically

2. **Verify Tests Pass**
   - Run the test suite to establish baseline
   - If tests fail initially, stop and report to user

3. **Scan for Refactoring Opportunities**
   - Read the production code file thoroughly
   - Identify ALL refactoring opportunities by priority:
     1. Dead code (commented code, unused variables)
     2. Poor names (unclear variables/methods)
     3. Long methods (> 25 lines)
     4. Duplication (repeated code blocks)
     5. Complex conditionals (nested ifs, no guard clauses)
     6. Unnecessary locals (single-use variables)
     7. Unused imports
   - **Present numbered list** of all findings to user
   - **Ask user which ones to proceed with** (e.g., "all", "1-5", "2,4,7")
   - Wait for user confirmation before starting refactoring

## Refactoring Loop

The approval is interactive and **stays here** (Initial Setup step 3): you present the
numbered findings, ask which to proceed with, and wait for user confirmation. Only the
deterministic apply → green-gate → commit/revert loop is encoded as a **Workflow**, so the
strike cap, green gate, and exact commit-message format run reliably instead of by prose.

Once the user has confirmed the subset, invoke the `Workflow` tool with the bundled script,
passing the human-approved refactor list (in priority order):

```
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/skills/tidy/workflow.js",
  args: {
    refactors: ["<approved refactor 1>", "<approved refactor 2>", ...],  // priority order
    testCommand: "<how to run the suite>",   // optional; agent infers if omitted
    productionFile: "<path>",                 // optional; the file being tidied
    testFile: "<path>"                        // optional; NEVER modified
  }
})
```

For each approved refactor the workflow runs:

1. An agent applies **only that one** refactoring (one at a time, in priority order) to
   **production code** — it **NEVER touches test code** — and returns the diff.
2. A gate agent (Haiku) runs the test suite and returns `{ passed, output }`.
3. If `passed === true`: commit with message format `"- r <refactoring>"` (quotes must
   include the - r). The loop **does not commit until the gate reports `passed === true`**.
4. If tests fail: revert this attempt's changes and retry — up to **three** attempts.

It returns `{ total, attempted, committed, halted, outcomes }`, where each outcome carries
`{ index, refactor, committed, commitMessage, attempts, halted }`. Give a brief status
update after each refactor from the returned outcomes.

**Stop conditions:**
- If a refactor fails three times (the workflow halts and returns `halted: true`)
- If no further refactoring opportunities found
- Pause and check with user

When the workflow returns `halted: true`, **pause and check with the user** before doing
anything else — report which refactor failed and its attempt output; do not continue to the
next refactor on your own.

## Code Style Guidelines

- Prefer self-explanatory, readable code over comments
- Use functional helper methods for clarity
- Remove comments and dead code
- Extract paragraphs into methods
- Use better variable names
- Remove unused imports
- Remove unhelpful local variables
- Methods should be small and focused (ideally < 25 lines)

## Common Refactorings (in priority order)

1. **Remove dead code** - commented code, unused variables
2. **Better names** - rename unclear variables/methods
3. **Extract methods** - break up long methods
4. **Remove duplication** - DRY principle
5. **Simplify conditionals** - reduce nesting, use guard clauses
6. **Remove unnecessary locals** - inline single-use variables
7. **Clean imports** - remove unused imports
