---
name: code-simplifier
description: Simplify code for readability and maintainability while preserving behavior. Use for refactoring, readability requests, polishing PR diffs, or cleaning up recently modified code.
---

# Code Simplifier

Make code easier to read and maintain. Prefer explicit, straightforward code over clever compactness.

## Workflow

1. **Bound the scope.** Use the files, functions, or snippet the user named. Otherwise, inspect `git status`, `git diff`, and staged changes for recent work. For a PR or committed branch, inspect its diff against the target base (for example, `git diff <base>...HEAD`). Keep edits within that target and the adjacent lines strictly required to complete an in-scope change. Widen the refactor only when the user requests it. Finish when the target is fixed and every later edit stays inside it.

2. **Record the contract.** Read repo guidance first, then linters, formatters, and adjacent code for naming, module boundaries, error handling, and formatting. Identify the affected inputs, outputs, side effects, errors, public APIs, ordering, timing, and edge cases. Finish when the behavior and local conventions that constrain the edit are clear enough to compare before and after.

3. **Simplify locally.** Choose the smallest change that clarifies the code: flatten a branch when an early return helps, remove redundant code or abstractions, consolidate tightly related logic, or give a variable, function, or type a clearer name. Keep responsibilities focused. Express multi-branch logic with `if/else` or `switch` instead of nested ternaries. Match the naming, module boundaries, error handling, and formatting found in step 2. Keep comments that explain reasons or constraints; remove comments that merely narrate the code. After simplifying, use the `decomment` skill for a dedicated comment pass. Finish when each changed line improves clarity, follows local conventions, and preserves the recorded behavior, except for changes the user explicitly requested.

4. **Check the result.** Review the diff for scope and behavior changes. Run the smallest relevant tests, typecheck, or build available for the changed code. Fix or revert any failure introduced by the edit. Finish when the checks pass, or when unavailable checks or verified pre-existing failures are reported with the remaining risk. Summarize the meaningful structural changes and the checks run.
