---
name: debugging
description: Systematically analyzes errors, identifies root causes, and suggests targeted fixes with regression safeguards.
---

# Debugging Skill

When debugging issues, follow a systematic approach to identify root causes efficiently and propose safe fixes.

## 1. Understand the Problem

- Read the full error message, stack trace, and any associated logs
- Identify the exact file, line number, and function where the error originates
- Determine whether the issue is a compile-time error, runtime exception, or logic bug
- Reproduce the issue mentally by tracing the code path from entry point to failure
- Check if the error message is from application code, a framework, or a third-party library

## 2. Check Common Issues First

- **Null/undefined references**: Accessing properties on null, undefined, nil, or None values
- **Type errors**: Passing wrong types, missing type coercion, incorrect generics
- **Race conditions**: Concurrent access to shared state without synchronization
- **Off-by-one errors**: Array bounds, loop conditions, pagination offsets
- **Import/dependency issues**: Missing imports, circular dependencies, version conflicts
- **Configuration errors**: Wrong environment variables, missing config files, incorrect connection strings
- **State management bugs**: Stale state, mutation of supposedly immutable data, missing state updates

## 3. Analyze the Stack Trace

- Read the stack trace bottom-up to find the originating call
- Identify the boundary between application code and library/framework code
- Look for the last application-level frame — that is usually where the bug lives
- Check if the error is thrown directly or wrapped/re-thrown from a deeper call
- For async code, check if the stack trace includes async boundaries (some frameworks lose context)

## 4. Investigate the Context

- Read the function containing the error and its callers
- Check recent changes to the affected files (git blame, git log)
- Look for related issues or known bugs in the project's issue tracker
- Check if the error occurs only under specific conditions (certain inputs, environments, timing)
- Review test coverage for the affected code — missing tests often correlate with bugs

## 5. Identify the Root Cause

- Distinguish between the symptom (where the error appears) and the cause (where the bug is)
- Trace data flow backward from the failure point to find where the invalid state was introduced
- Check preconditions: are function inputs valid? Are required fields populated?
- For intermittent bugs, look for timing dependencies, caching issues, or non-deterministic behavior
- For regression bugs, identify what changed (new code, dependency update, config change)

## 6. Propose a Fix

- Fix the root cause, not just the symptom
- Explain _why_ the fix works, not just _what_ it changes
- Keep the fix minimal — change only what is necessary to resolve the issue
- Preserve existing behavior for all paths that are not affected by the bug
- If the fix requires a design change, explain the tradeoff and alternatives considered

## 7. Prevent Regressions

- Write a test that reproduces the bug and verifies the fix
- The test should fail without the fix and pass with it
- Check if similar patterns exist elsewhere in the codebase that might have the same bug
- Consider adding runtime validation or assertions at the boundary where the bug entered
- If the bug was caused by a missing null check, consider enabling stricter null checking project-wide

## 8. Communicate Findings

- Summarize: what was the error, what caused it, and how it was fixed
- Include the file paths and line numbers of the changes
- Note any follow-up tasks (e.g., refactoring to prevent similar issues, adding monitoring)
- If the fix is a workaround, document the ideal solution and create a follow-up ticket
