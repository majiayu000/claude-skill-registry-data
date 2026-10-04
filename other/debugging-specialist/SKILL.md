---
name: debugging-specialist
description: Systematic bug detection, root cause analysis, and error resolution across
  languages and systems. Use when code is throwing an error, a test is failing unexpectedly,
  behavior is wrong but no error is thrown, a race condition is suspected, memory
  is leaking, or you need help reading a stack trace or crash log.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: productivity
  tags:
  - debugging
  - error-analysis
  - troubleshooting
  - stack-trace
  - root-cause
---

# Debugging Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `this is throwing an error`, `why is this failing`, `help me debug`.
- The requested work fits this skill's lane: Fixing errors, reading stack traces, diagnosing unexpected behavior, race conditions, memory leaks.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Architectural refactors; security vulnerability remediation.

## First actions
1. `Read` the error message, stack trace, or failing test output in full — do not summarize it yet
2. `Glob` for the file(s) referenced in the stack trace
3. `Read` the relevant source files at the line numbers indicated

## Decision rules
- Start with the innermost / lowest-level error in a stack trace, not the top-level wrapper
- If the error is intermittent: consider race conditions, timing dependencies, or shared mutable state
- If the error only appears in production: check for environment variable differences, log level differences, or data volume differences
- If the fix requires architectural changes: note it but don't implement — surface to architecture-specialist

## Output contract
- Provide: root cause explanation → minimal reproduction (if helpful) → fix → test to prevent regression
- Always explain *why* the bug occurred, not just what to change

## Constraints
- NEVER apply a fix without understanding the root cause
- Scope boundary: if debugging reveals a security vulnerability, flag it and route to security-specialist

## Reference
- `references/legacy-agent.md`: debugging patterns, race condition detection, memory leak analysis, distributed trace debugging
