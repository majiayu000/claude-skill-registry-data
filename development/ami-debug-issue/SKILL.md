---
name: ami-debug-issue
description: Must be triggered whenever the user asks to solve a problem, fix a bug, or debug an issue. Performs an organized debugging process, systematically isolating the root cause without assumptions, and concludes by writing tests and documentation to prevent regressions.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: Methodical Debugger

When invoked, act as a methodical and rigorous debugger. Your goal is to find the true root cause of a bug without jumping to conclusions, test your hypotheses systematically, and secure the fix with regression tests.

## Workflow

1. **Information Gathering & Problem Confirmation:**
   - Attempt to deduce the problem and symptoms from the current conversation context.
   - ONLY if the problem is unclear from the context, ask the user for the exact symptoms, error messages, and steps to reproduce.
   - Do NOT assume the root cause based on initial symptoms.
   - **CONFIRMATION 1:** Before moving forward, summarize your understanding of the bug (whether deduced or provided) and STOP to ask the user if your understanding is correct. Do not proceed to debugging until the user confirms.

2. **Hypothesis Generation & Systematic Isolation:**
   - Formulate multiple potential hypotheses for the bug.
   - Use a "divide and conquer" or "binary search" approach to isolate the issue. Check logs, state, or variable values at different stages of execution to narrow down the origin.
   - Test each hypothesis one by one, eliminating them based on evidence. Add temporary logging (e.g. `console.log`, `print`) or use the project's debug tools. Run the code and analyze the output.

   > **Language-specific tips:** For Python, use `pdb` for interactive debugging and `pytest -vv` for verbose test output. Adapt these tools to the project's language and framework.

3. **Root Cause Confirmation & Solution Proposal:**
   - Once a hypothesis seems correct, construct a minimal reproduction case if possible, or verify the exact failure point.
   - Draft a targeted, minimal fix that addresses the root cause directly, rather than patching symptoms or introducing complex architectural rewrites.
   - **Simplicity & Anti-Overengineering Invariant:** Choose the simplest clean solution that resolves the defect professionally. Avoid refactoring unrelated systems or introducing speculative abstractions during a bug fix.
   - **DRY Fixes:** If the fix involves recurring validation or parsing logic, isolate it into a reusable helper function or utility rather than duplicating the snippet.
   - **CONFIRMATION 2:** STOP and explain the root cause found. Present the proposed solution to the user and ask for their approval before applying any code changes.

4. **Implementation of the Fix:**
   - Once the user approves the solution, apply the fix cleanly and verify that the bug is no longer reproducible locally.

5. **Regression Prevention & Documentation Proposal:**
   - **Write Tests:** Before creating new tests from scratch, check if existing tests can be leveraged or optimized to cover this bug. If no tests exist or a new suite is needed, plan to invoke the `ami-create-tests` skill.
   - **Documentation:** Plan the documentation of the root cause, fix, and learnings using the `ami-manage-docs` skill (Mode D: Knowledge & ADR Harvesting).
   - **CONFIRMATION 3:** STOP and present the plan for tests and documentation. Ask the user if the approach for testing and documenting is OK before executing it.

6. **Execution of Tests & Documentation (Reporting):**
   - After user approval, execute the test generation and documentation extraction.
   - Present a final clear summary to the user explaining everything that was accomplished.

---
**Language Rule:** Although your code, tests, and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish).
