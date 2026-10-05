---
name: deep-review
description: Deep investigation skill for PRs and bug fixes that go beyond surface review. Use this when a standard code review isn't enough — when a fix looks correct but might be hiding the real problem, when the PR solves the symptom but not the cause, when changes touch critical paths (transactions, security, concurrency), or when previous reviews missed issues that reached production. Trigger this for any PR marked as critical, any fix for a recurring bug, or any change in legacy code where the real behavior is unclear. Do NOT use the standard code-reviewer when deep-review is more appropriate.
---

# Deep Review Skill

Investigation-first review for Spring Boot 3.x / Java 17-21. Assumes the fix may be wrong until proven otherwise.

## Core Principle

> A fix that makes the error stop appearing is not the same as a fix that solves the problem.

Standard review checks *what changed*. Deep review checks *why the change works*, *what else it affects*, and *whether the root cause is actually resolved*.

---

## Phase 1: Understand the Reported Problem

Before reading the fix, reconstruct the original problem independently.

```
1. Read the issue/ticket description
2. Identify: what was the expected behavior? what actually happened?
3. Locate the failure point in the stacktrace or logs
4. Map the execution path that leads to the failure:
   Controller → Service → Repository → DB
5. Ask: does the fix intercept the CAUSE or the SYMPTOM?
```

**Red flags at this phase:**
- Fix adds a null check where the null should never occur
- Fix catches an exception that shouldn't be thrown
- Fix adds a condition that bypasses the problematic path instead of correcting it
- No test added that would have caught the original bug

---

## Phase 2: Trace the Real Execution Flow

Do not trust method names or javadoc. Trace what the code *actually does*.

### For each modified method, verify:

```java
// Verify these — do not assume:
// 1. What is the actual return value in each branch?
// 2. Are there side effects not visible in the signature?
// 3. Does @Transactional propagate correctly through this call?
// 4. What happens when the input is null / empty / boundary value?
// 5. Is there any state mutation on a shared object?
```

### Transaction boundary audit

```java
// Check every modified service method:
// ❓ Is there a @Transactional at the right level?
// ❓ Does the transaction include ALL the writes that must be atomic?
// ❓ Are there calls to other @Transactional methods that might create nested transactions?
// ❓ Is readOnly=true used where writes happen? (silent data loss risk)

// Spring Boot 3.x — check for this common mistake:
@Transactional(readOnly = true)   // ← defined on class
public class UserService {
    public void updateUser(User u) {  // ← no override = readOnly! writes silently ignored
        userRepository.save(u);
    }
}
```

### JPA state audit

```java
// For any change touching JPA entities, verify:
// ❓ Is the entity in managed state when modified?
// ❓ Could LazyInitializationException occur in a different call path?
// ❓ Does the fix accidentally trigger N+1 in a path that wasn't tested?
// ❓ Are optimistic lock (@Version) conflicts handled?
```

---

## Phase 3: Impact Analysis

### Identify all callers of modified methods

```
For each changed method/class:
1. Find all direct callers (Grep/IDE)
2. Find all indirect callers (services that use those services)
3. For each caller: does the behavior change affect them?
4. Check if the method is called from scheduled tasks, event listeners, or async contexts
   — these have different transaction and security contexts
```

### Check for concurrency issues

```java
// Flag these patterns in modified code:
// ❌ Shared mutable state without synchronization
// ❌ Read-then-write without atomic operation or locking
// ❌ @Async methods that depend on ThreadLocal (e.g., SecurityContext, MDC)
// ❌ Virtual threads (Java 21) accessing synchronized blocks — pinning risk

// Spring Boot 3.5 with virtual threads enabled:
// @Transactional + synchronized = thread pinning — check if present
```

---

## Phase 4: Test Quality Audit

A fix without a test that would have caught the original bug is incomplete.

```
Verify the PR includes:
✅ A test that FAILS on the original code and PASSES on the fix
✅ Tests for boundary conditions (null, empty, max values)
✅ Integration test if the bug was in the interaction between layers
✅ Testcontainers for bugs that were DB-specific

Flag as incomplete if:
❌ Only happy path tests added
❌ Test mocks away the component where the bug actually was
❌ No test added at all ("it was tested manually")
```

---

## Phase 5: Root Cause Verdict

After the investigation, produce a clear verdict:

```markdown
## Deep Review Verdict

### Root cause identified: [YES / NO / PARTIAL]
[Describe what actually caused the bug, not just what the fix does]

### Fix correctness: [CORRECT / SYMPTOMATIC / INCORRECT]
- CORRECT: Fix addresses the actual root cause
- SYMPTOMATIC: Fix hides the problem without solving it
- INCORRECT: Fix introduces new problems or doesn't solve the issue

### Side effects found: [YES / NO]
[List any callers or paths affected by the change]

### Transaction safety: [SAFE / AT RISK / BROKEN]
[Specific finding about transaction boundaries]

### Test coverage: [ADEQUATE / INCOMPLETE / MISSING]
[What's covered and what's missing]

### Verdict: [APPROVE / REQUEST CHANGES / REJECT]

### Required changes before merge:
1. [Specific change with file and line reference]
2. ...

### Warnings for after merge:
- [Monitor X metric / Check Y behavior in production]
```

---

## Quick Checklist

| Check | Question |
|-------|----------|
| Root cause | Does the fix address cause, not symptom? |
| Null safety | Are null checks treating cause or masking NPE? |
| Transactions | Are all atomic operations in the same transaction? |
| readOnly | Are writes attempted inside readOnly transactions? |
| Callers | Do all callers of modified methods still work? |
| Async/Scheduled | Does the fix work in non-request thread contexts? |
| Tests | Is there a test that would have caught the original bug? |
| Logging | Are errors logged with full context before this fix? |
