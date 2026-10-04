---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** if you didn't watch the test fail, you don't know it tests the right thing.

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (confirm with the user first):** throwaway prototypes, generated code, pure configuration files.

Thinking "skip TDD just this once"? That's the rationalization to catch, not follow.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it and start over — don't keep it "as reference" and don't adapt it while writing the test around it. Implement fresh from the test.

## Red-Green-Refactor

1. **RED — write one minimal failing test.** One behavior, a clear name, real code paths (mock only what's unavoidable).
2. **Verify RED.** Run it. Confirm it *fails* (not errors), and fails for the expected reason — missing feature, not a typo. If it passes, you're testing existing behavior; fix the test.
3. **GREEN — write the simplest code that passes.** No extra options, no "while I'm here" features. Just enough to satisfy the test.
4. **Verify GREEN.** Run the full relevant suite. Confirm this test passes, nothing else broke, output is clean.
5. **REFACTOR.** Only after green: remove duplication, improve names, extract helpers. Keep tests green; don't add behavior here.
6. Repeat for the next behavior.

### Example (TypeScript / Jest — this repo's `agent` and `consumer` packages use Jest)

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
npm test -- path/to/form.test.ts
# FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
npm test -- path/to/form.test.ts
# PASS
```

For `client/` (Angular, Jasmine/Karma), the same cycle applies with `ng test` / `npm run test:ci` in place of `npm test`.

## Good Tests

| Quality | Good | Bad |
|---|---|---|
| Minimal | One behavior per test | `test('validates email and domain and whitespace')` |
| Clear | Name describes the behavior | `test('test1')` |
| Honest | Asserts on real behavior | Asserts on a mock's call count instead of an outcome |

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks too; the test takes 30 seconds |
| "I'll test after" | Tests written after pass immediately, which proves nothing — you never watched them catch the bug |
| "Already manually tested" | Manual testing leaves no record and doesn't re-run when the code changes later |
| "Sunk N hours already, deleting is wasteful" | That time is spent either way — the choice is rewrite with TDD (trustworthy) vs. bolt tests onto untested code (not) |
| "TDD will slow me down" | Debugging an untested regression in prod is slower than writing the test first |
| "Test is hard to write" | That's the design telling you something — hard to test usually means hard to use |

## Red Flags — Stop and Restart

- Code written before its test
- A new test that passes on the first run
- Can't explain why the test failed before the fix
- "I already manually verified it, the test is just formality"

## Verification Checklist

Before calling implementation work done:
- [ ] Every new function/behavior has a test
- [ ] Watched each test fail before implementing
- [ ] Each failed for the right reason (missing feature, not a typo)
- [ ] Wrote minimal code to pass
- [ ] Full suite passes, output is clean
- [ ] Edge cases and error paths are covered

## When Stuck

| Problem | Try |
|---|---|
| Don't know how to test it | Write the API you wish existed; write the assertion first |
| Test setup is huge | Extract helpers; if still huge, the design is too coupled |
| Must mock everything | The code under test is too tightly coupled — consider dependency injection |

Bug found in existing code? Write a failing test that reproduces it first, then fix under the same cycle — never patch a bug without a regression test proving it's fixed.
