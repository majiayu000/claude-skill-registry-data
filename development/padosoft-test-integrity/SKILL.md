---
name: padosoft-test-integrity
description: >-
  Use this skill when writing or reviewing a test, and whenever a suite is suspicious: a test that passes
  whatever the code does, one that went green without the fix, an ordering test that never fails, a suite
  that passes alone and fails in sequence or in a different order, a flaky test blamed on CI. It checks that
  the body exercises what the name promises, that ordering assertions are strict, that global state is
  restored, that a failure-path test actually fires the failure, and that the assertion could fail at all.
  Do not use it to choose a test framework, to design a test strategy or coverage targets, or to debug a
  failing application bug.
license: MIT
compatibility: >-
  Language-agnostic. Examples use PHPUnit and a JS testing library because that is where the cases came from.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: A test that cannot fail is worse than no test.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: testing, assertions, flaky, teardown, phpunit, vitest, jest, review
---

# Test integrity

**A test that cannot fail is worse than no test**: it costs the same to run, and it buys a confidence nobody
earned. These are the ways a test passes without testing anything — all found in real review, all green.

---

## 1. The name and the body must match

The assertion on the last line is the direct consequence of the action on the first.

```tsx
// ❌ nothing is edited, so "after edit" is never exercised
it("enables Save after edit", () => {
    render(<Form />);
    expect(screen.getByRole("button", { name: "Save" })).toBeDisabled();
});
// ✅
it("enables Save after edit", async () => {
    render(<Form />);
    await user.type(screen.getByLabelText("Title"), "x");
    expect(screen.getByRole("button", { name: "Save" })).toBeEnabled();
});
```

A name that promises a transition (`after`, `when`, `once`, `on`) and a body with no action is the single
most common instance.

## 2. Ordering tests need strict comparisons and monotonic fixtures

```ts
// ❌ passes under either order
expect(last).toBeGreaterThanOrEqual(first);
// ✅ fails if the order reverses
expect(second).toBeGreaterThan(first);
```

And the **fixtures must be strictly monotonic**: three rows with the same timestamp make any ordering
assertion vacuous, however strict the operator. The test to run on yourself: *reverse the expected order in
the fake response — does the test fail?* If it does not, it is not testing ordering.

## 3. Global state is restored

Environment variables, container bindings, `window.location`, the clock, `fetch` patches, static singletons,
feature flags: captured before, restored after.

```php
protected function tearDown(): void {
    Env::getRepository()->clear('FEATURE_X');
    parent::tearDown();          // and let the framework do its own teardown
}
```

An unrestored mutation does not break this test — it breaks **a different one, later, sometimes**. That is
where "flaky, it's CI" comes from. The check: run the file alone, then the whole suite, then the suite in a
different order.

⚠️ Order matters in teardown: undo your own state **before** handing control to the framework's teardown, or
the mock/DI layer may be gone when you try to touch it.

## 3b. The test harness can destroy the database it was pointed at

A trait that rebuilds the schema — dropping every table and re-running the migrations — is destructive by
design. It is safe exactly as long as the test connection points where you think it does, and that
assumption fails on a mistyped variable, a cached configuration, or a suite run from the wrong directory.
When it fails, every table is gone, and the loss is not recoverable from the test run.

**Prefer the trait that wraps each test in a transaction and rolls it back.** It leaves nothing behind, it
is faster, and it is harmless even against the wrong database — the schema has to exist already, which is
the point: creating it is the migrations' job, not the test's.

- If a test genuinely needs a rebuilt schema, that is a decision to take deliberately, with the reason
  written in the test.
- **A test that creates its own tables in setup is hiding a missing migration.** Fix the migration.
- Before running a suite against anything shared, check two things: which connection the tests resolve to,
  and whether any test in the set uses a destructive trait. If either is uncertain, stop and ask — "it will
  probably use the test environment" is the sentence that precedes the loss.

## 4. A failure-path test must actually fire the failure

```ts
// ❌ the stub is never reached: nothing triggers the request
it("surfaces a 422 inline", () => {
    stub(api.save).returns(422);
    render(<Form />);
    expect(screen.getByRole("alert")).toBeInTheDocument();
});
```

Stubbing an error is not provoking it. Click the button, post the invalid body, take the dependency down.
"Render and assert the error UI is absent" asserts nothing: it was absent before the test started.

## 5. Assert on the thing, not on a proxy for it

- An empty-state test looks for the **empty-state marker**, not for `data-state="ready"` with zero children:
  ready is not empty.
- A "no call was made" test asserts the expectation on the double (`shouldNotReceive`, `not.toHaveBeenCalled`)
  — not the absence of a side effect that has other causes.
- An exact-match check for a sentinel beats a substring check that a longer message also satisfies.

## 5b. A negative fixture is only valid if it fails for the named reason

A test that asserts "this input is rejected" passes just as well when the input is rejected for the **wrong**
reason — a stray blank line, a missing file, a parse error earlier than the thing under test. It is green,
and it proves nothing about the rule it is named after.

So: **observe the expected RED, and read the message.** If the failure text is not the one the test is about,
the fixture is wrong, not the code.

Three shapes that produce a right-answer-wrong-reason pass:

- **An unbounded mutation.** A fixture that edits "up to the next marker" crosses into the following section
  once validation gets stricter, and starts failing for that instead. Bound the edit by the next boundary.
- **A regex for the expected diagnostic.** Punctuation in the message then decides the outcome, and a
  reworded error flips a test that has nothing to do with wording. Compare the expected diagnostic
  **literally**.
- **A fixture that only exercises the clean path of the parser.** If the strict parser rejects malformed
  input before your rule runs, the rule is untested. Give it input that reaches it.

## 6. Could this assertion ever fail?

The last question before closing the test. Concretely:

1. **Break the implementation on purpose** — invert a condition, return the wrong constant. The test must go
   red. If it stays green, it is measuring nothing.
2. If a test never failed during development, be suspicious: a test written after the fix, that was green on
   the first run, has never proven it detects the bug.
3. Count the assertions. Zero is a smoke test — fine, if named as one.

---

## How to find it in a diff

```bash
# weak ordering assertions
rg -n "toBeGreaterThanOrEqual|toBeLessThanOrEqual|greaterThanOrEqualTo|lessThanOrEqualTo" tests/ src/
# global mutations without a restore in sight
rg -n "Object\.defineProperty\(window,\s*['\"]location" -A 5 src/
rg -n "detectEnvironment\(|putenv\(|Carbon::setTestNow\(" tests/
# tests with no assertion at all
rg -n "(it|test)\(" -A 6 src/ | rg -B 6 "^\s*\}\)" | rg -c "expect\(" || true
# stubs never triggered: an error stub with no interaction in the body
rg -n "(mockRejectedValue|shouldReceive.*andThrow|returns\(4[0-9]{2}\))" -A 8 tests/ src/
```

Every hit is a **candidate**. The real check is reading the body against the name.

## Gotchas

- **Coverage does not see this.** All of these execute the code: they are covered and they assert nothing
  useful. Coverage measures what ran, not what was checked.
- **A green suite on a bug report is information.** If the bug is real and the suite is green, the suite has
  a hole exactly there — write that test first, watch it fail, then fix.
- **"It's flaky" is a diagnosis nobody made.** Almost always it is §3: shared state, or a dependency on
  execution order.
- **A test written to make CI green is not a test.** If the assertion was weakened until it passed, the
  weakening is the change that needs reviewing.
- **Snapshot tests approve whatever they are given.** Regenerating a snapshot to make it pass records the
  bug as the expectation.

## Checklist

- [ ] Every test name matches what its body actually does
- [ ] Ordering: strict comparisons **and** strictly monotonic fixtures; reversing the fixture fails the test
- [ ] Global state captured and restored; own state undone before the framework's teardown
- [ ] Failure-path tests trigger the failure, not just stub it
- [ ] Assertions on the thing, not on a proxy
- [ ] The implementation was broken on purpose at least once and the test went red
- [ ] No destructive database trait; the test connection verified before running against anything shared
- [ ] Performance claims measured on a production-like dataset, not a development one

## Final report

```
Test review: <n> files, <n> tests
Name/body mismatch: none | <file:line>
Vacuous ordering: none | <file:line>
Unrestored global state: none | <file:line>
Failure never fired: none | <file:line>
Falsifiability check: done on <which tests> | not done
```
