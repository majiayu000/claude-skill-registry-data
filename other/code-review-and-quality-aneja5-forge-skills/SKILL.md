---
name: code-review-and-quality
description: Use when a task is complete and ready for review, when reviewing a PR, when validating an implementation against its contract, when checking quality before merging, or when a five-axis quality gate is needed before approving code.
---

# Code Review and Quality

## Overview

Five-axis review: correctness, contract compliance, readability, security, performance. Each finding is categorized as Critical / Important / Suggestion. Contract compliance is the forge-specific axis — implementations must match `.forge/contracts/` exactly.

## When to Use

- A task from `.forge/tasks.yaml` is marked done and needs review
- A PR is ready for merge review
- User asks to review a specific change or file

## When NOT to Use

- Code hasn't been tested yet — run `tdd` first
- Looking for performance profiling — that's a separate investigation
- Security audit with threat modeling — use `security-auditor` agent persona

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "It passes tests so it's correct" | Tests don't prove correctness — they prove what was tested |
| "I'll leave style comments but not block" | Style inconsistencies compound into readability debt |
| "The contract is close enough" | Contracts exist precisely to prevent "close enough" |
| "Security issues are edge cases" | Edge cases are where attackers operate |
| "We can optimize later" | Performance regressions rarely get addressed later |

## Red Flags

- Implementation ignores an error type defined in the contract
- Function signature differs from contract's typed schema
- Invariant in contract is not enforced in implementation
- Input validation missing at module boundary (contract says it's not caller's job)
- Magic numbers with no explanation
- Error paths return 200 with error message in body

## Five-Axis Review

### Axis 1: Contract Compliance (forge-specific)

For each module touched, check against `.forge/contracts/<module>.md`:
- [ ] Input types match contract schema exactly
- [ ] Output types match contract schema exactly
- [ ] Every error type in the contract is handled
- [ ] Every invariant in the contract is enforced
- [ ] "Not responsible for" items are not implemented here

### Axis 2: Correctness

- [ ] All acceptance criteria from the task are satisfied
- [ ] Edge cases and error paths handled
- [ ] No off-by-one, null deref, or race condition visible
- [ ] Side effects are intentional and documented

### Axis 3: Readability

- [ ] Names describe what, not how
- [ ] Complex logic has a comment explaining WHY (not WHAT)
- [ ] No dead code or commented-out blocks
- [ ] Function length: if it doesn't fit in one screen, it should be decomposed

### Axis 4: Security

- [ ] All user input validated before use
- [ ] No SQL/command/HTML injection vectors
- [ ] Secrets not logged, not in error messages
- [ ] Authentication checked before authorization checked before business logic

### Axis 5: Performance

- [ ] No N+1 queries introduced
- [ ] No synchronous blocking in async paths
- [ ] No unbounded operations on user-controlled input size

## Finding Format

```
[CRITICAL] Contract violation: UserService.create() returns `userId: string` per contract
           but implementation returns `id: number`. Callers will break at runtime.
           File: src/user/service.ts:47

[IMPORTANT] Missing error handling: `RateLimitError` is defined in AuthService contract
            but never caught — will surface as unhandled exception.
            File: src/auth/middleware.ts:23

[SUGGESTION] Variable name `d` on line 12 — consider `durationMs` for clarity.
```

## Verification

- [ ] All five axes reviewed
- [ ] Contract compliance checked against `.forge/contracts/` for each touched module
- [ ] Every Critical finding listed (must be fixed before merge)
- [ ] Every Important finding listed (should be fixed or explicitly deferred)
- [ ] Findings cite file:line for each issue
- [ ] Suggestions separated from required changes
