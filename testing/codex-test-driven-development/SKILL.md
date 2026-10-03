---
name: codex-test-driven-development
description: Use before feature, bugfix, or refactor implementation when behavior can be tested; enforces Red-Green-Refactor discipline.
load_priority: on-demand
---

## TL;DR
Write test first → watch it fail → write minimal code to pass → watch it pass → refactor. Delete code written before tests. No exceptions. Integrate with `$gate` for automated verification. Use `$tdd` or `$red-green` to activate.

# Test-Driven Development (TDD)

## Activation

1. Activate on `$codex-test-driven-development`, `$tdd`, or `$red-green`.
2. Activate when implementing any feature or bugfix, before writing implementation code.
3. Activate when `codex-workflow-autopilot` routes to `build` or `fix` workflow.
4. Activate when `codex-intent-context-analyzer` detects implementation intent.
5. Always active as a behavioral constraint during implementation phases.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the human):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## Red-Green-Refactor Cycle

```
Task type → Implementation needed?
    |- Yes → Write failing test (RED)
    |   |- Verify it fails correctly
    |   |- Write minimal code (GREEN)
    |   |- Verify it passes + all tests pass
    |   |- Refactor (keep green)
    |   `- Next test → repeat
    |
    `- No → skip TDD
```

### RED — Write Failing Test

Write one minimal test showing what should happen.

**Good — Python:**
```python
def test_retries_failed_operations_three_times():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("fail")
        return "success"

    result = retry_operation(operation)

    assert result == "success"
    assert attempts == 3
```
Clear name, tests real behavior, one thing.

**Good — TypeScript:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

**Bad:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```
Vague name, tests mock not code.

**Requirements:**
- One behavior per test
- Clear descriptive name
- Real code (no mocks unless unavoidable)

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
# Python
python -m pytest tests/path/test_module.py::test_name -v

# JavaScript/TypeScript
npm test -- --grep "test name"

# Go
go test -run TestName -v ./...
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes immediately?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN — Minimal Code

Write simplest code to pass the test.

**Good:**
```python
async def retry_operation(fn, max_retries=3):
    for i in range(max_retries):
        try:
            return fn()
        except Exception:
            if i == max_retries - 1:
                raise
```
Just enough to pass.

**Bad:**
```python
async def retry_operation(
    fn,
    max_retries=3,
    backoff="exponential",
    on_retry=None,
    timeout=30,
    jitter=True,
):
    # YAGNI — over-engineered
```

Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
# Run specific test
python -m pytest tests/path/test_module.py::test_name -v

# Run ALL tests to check for regressions
python -m pytest tests/ -q
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test_validates_email_and_domain_and_whitespace` |
| **Clear** | Name describes behavior | `test_1`, `test_it_works` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |
| **Real code** | Tests actual implementation | Tests mock behavior |

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |
| "This is different because..." | It's not. Start with TDD. |

## Red Flags — STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately on first run
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result["error"] == "Email required"
```

**Verify RED**
```bash
$ python -m pytest tests/test_form.py::test_rejects_empty_email -v
FAIL: AssertionError: expected 'Email required', got None
```

**GREEN**
```python
def submit_form(data):
    if not data.get("email", "").strip():
        return {"error": "Email required"}
    # ...
```

**Verify GREEN**
```bash
$ python -m pytest tests/test_form.py -v
PASS (all tests)
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask the human. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## CodexAI Integration

### Gate Integration

After TDD cycle, run quality gate:

```bash
# Quick check
python codex-execution-quality-gate/scripts/auto_gate.py --mode quick --project-root <repo>

# Smart test selection for changed files
python codex-execution-quality-gate/scripts/smart_test_selector.py --project-root <repo>
```

### Workflow Integration

| Workflow Phase | TDD Requirement |
|----------------|-----------------|
| `$plan` task breakdown | Each task must include test-first steps |
| `$create` implementation | RED-GREEN-REFACTOR per feature unit |
| `$debug` bug fix | Failing reproduction test BEFORE fix attempt |
| `$review` code review | Verify TDD compliance in changeset |

## Testing Anti-Patterns

When adding mocks or test utilities, see `references/testing-anti-patterns.md` to avoid common pitfalls.

## Reference Files

- `references/testing-anti-patterns.md`: common testing mistakes and how to avoid them.

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without the human's explicit permission.
