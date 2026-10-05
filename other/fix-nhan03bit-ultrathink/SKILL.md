---
name: fix
description: Apply targeted, verified fixes with minimal blast radius and rollback safety
layer: hub
category: workflow
triggers:
  - "/fix"
  - "fix this"
  - "apply the fix"
  - "patch this"
  - "correct this"
inputs:
  - diagnosis: Root cause analysis (from debug skill or user-provided)
  - target: Specific file(s) and location(s) to modify
  - constraints: Any constraints on the fix approach (backwards compatibility, no new dependencies, etc.)
outputs:
  - changes: List of files modified with descriptions of each change
  - verification: Results of post-fix verification
  - regressionRisk: Assessment of what might break
linksTo:
  - test
  - code-review
  - debug
linkedFrom:
  - debug
  - cook
  - team
  - ship
preferredNextSkills:
  - test
  - code-review
fallbackSkills:
  - debug
  - refactor
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Modifies source code files
  - May modify test files
  - May run tests to verify
---

# Fix Skill

## Purpose

Apply targeted, minimal, verified code fixes. This skill takes a diagnosed problem (typically from `debug`) and implements the smallest correct change that resolves it. The emphasis is on precision, safety, and verification -- not on improvement or refactoring.

A fix is not a feature. A fix is not a refactor. A fix changes the minimum code necessary to make the incorrect behavior correct.

## Workflow

### Phase 1: Fix Planning

1. **Confirm the diagnosis** -- Restate the root cause. If coming from `debug`, validate that the diagnosis is specific enough to act on. If the diagnosis is vague (e.g., "something wrong with auth"), send back to `debug`.

2. **Identify the fix location(s)** -- Determine exactly which file(s) and line(s) need to change. Read each file to confirm current state.

3. **Design the minimal fix** -- What is the smallest change that corrects the behavior?
   - Prefer fixing the root cause over patching the symptom
   - Prefer additive changes (adding a check) over structural changes (reorganizing code)
   - Prefer consistent changes (matching existing patterns in the codebase)

4. **Assess blast radius**
   - What other code calls/uses the code being changed?
   - Could the fix break any of those callers?
   - Are there tests that will need updating?
   - Is there a migration or deployment concern?

5. **Choose fix strategy**:
   - **Direct fix**: Change the buggy code directly (most common)
   - **Guard fix**: Add a defensive check upstream of the bug
   - **Data fix**: Correct invalid data that is causing the bug
   - **Configuration fix**: Change config/environment rather than code
   - **Workaround**: Temporary mitigation when the root fix is too risky right now (must be clearly marked as temporary)

### Phase 2: Implementation

6. **Read the target file(s)** completely (or the relevant sections for large files).

7. **Apply the fix** using the Edit tool with precise `old_string` / `new_string` replacements.
   - Change ONLY what needs to change
   - Preserve existing code style (indentation, naming, patterns)
   - Add a brief comment only if the fix is non-obvious (do not over-comment)
   - If a workaround, add a `// TODO: [description of proper fix]` comment

8. **If multiple files need changes**, apply them in dependency order (shared code first, then consumers).

### Phase 3: Verification

9. **Self-review the changes**
   - Re-read each modified file to confirm the change is correct
   - Verify no unintended changes were introduced
   - Check that the fix addresses the root cause, not just the symptom

10. **Run relevant tests** (if they exist)
    - Run the specific test file(s) for the affected code
    - Run the broader test suite if the change could have ripple effects
    - If no tests exist, note this and recommend test creation

11. **Manual verification** (if applicable)
    - If the fix is for a UI issue, describe how to visually verify
    - If the fix is for an API issue, describe how to test the endpoint
    - If the fix is for a data issue, describe how to verify data integrity

### Phase 4: Report

12. **Produce the fix report** using the template below.
13. **Recommend next steps** -- typically `test` to add regression tests, or `code-review` for complex fixes.

## Fix Report Template

```markdown
# Fix Report

## Root Cause
[One sentence restating the diagnosed issue]

## Changes Made
### [filename]
- **What changed**: [description]
- **Why**: [reasoning]
- **Lines affected**: [line range]

### [filename 2] (if applicable)
- ...

## Verification
- [ ] Self-review: Changes match intent
- [ ] Tests pass: [test command and result]
- [ ] Manual check: [what was checked]

## Blast Radius
- **Direct impact**: [what is directly affected]
- **Indirect risk**: [what might be affected]
- **Confidence**: High | Medium | Low

## Regression Risk
[What could this fix break? What should be watched?]

## Recommended Follow-up
- [ ] Add regression test via `test` skill
- [ ] Review via `code-review` skill (if high risk)
```

## Usage

### After debugging
```
/fix Apply the fix identified in the debug report
```

### Direct fix request
```
/fix The getUserById function in src/lib/users.ts returns null instead of throwing NotFoundError when the user does not exist
```

### With constraints
```
/fix The date parsing is wrong in the invoice generator. Must maintain backwards compatibility with existing invoices.
```

### Quick fix
```
/fix Typo in the error message on line 42 of src/app/api/auth/route.ts: "authenication" should be "authentication"
```

## Examples

### Example: Null check fix

**Diagnosis**: `UserList` component crashes because API returns `{ error: "..." }` without `items` field on failure.

**Fix**:
```typescript
// Before
const items = data.items.map(...)

// After
const items = (data.items ?? []).map(...)
```

**Plus** add proper error handling:
```typescript
if (data.error) {
  return <ErrorDisplay message={data.error} />
}
const items = data.items.map(...)
```

### Example: Destructuring fix

**Diagnosis**: `createOrder()` does not include `discount` in destructured input.

**Fix**:
```typescript
// Before
const { customerId, items, total } = input

// After
const { customerId, items, total, discount } = input
```

And ensure `discount` is passed to the database create call.

### Example: Configuration fix

**Diagnosis**: CORS errors in production because allowed origins list does not include the new domain.

**Fix**: Add the domain to the CORS configuration, not to the code. This is a configuration fix, not a code fix.

## Guidelines

- **Minimal changes only** -- The fix should be the smallest correct change. Resist the urge to improve adjacent code.
- **Match existing style** -- The fix should look like it was written by the same developer who wrote the surrounding code.
- **Never fix without understanding** -- If you do not understand why the code is broken, go back to `debug`. Blind fixes create new bugs.
- **Test after fixing** -- Always verify the fix works. "It compiles" is not verification.
- **One fix per invocation** -- Do not bundle multiple unrelated fixes. Each fix should address one specific issue.
- **Workarounds are temporary** -- If a workaround is needed, mark it clearly with a TODO and a description of the proper fix.
- **Preserve backwards compatibility** -- Unless explicitly told otherwise, a fix should not change the external behavior of correct code paths.
- **Document non-obvious fixes** -- If someone reading the code would wonder "why is this check here?", add a comment explaining the bug it prevents.
