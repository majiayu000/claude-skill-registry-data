---
name: tdd-workflow
description: Drives test-driven development through a strict RED-GREEN-REFACTOR cycle with test-runner detection, a "fails for the right reason" gate, checkpoint commits, and a short evidence report. Use when implementing a feature, fixing a bug, or refactoring logic where the expected behaviour can be written as a test before the code exists.
---

# TDD Workflow

Tests come first. The failing test is the specification; the passing test is the proof.
This skill gives the cycle enough structure that "I wrote tests" always means
"a test failed, then passed, and here is the evidence".

## When to use

- New behaviour with definable inputs and outputs (business logic, parsers, API handlers, validators, state machines).
- Bug fixes: the reproducer test is the first artefact, always.
- Refactors of logic that already has tests (the tests are the safety net) or should have them.
- A task in a plan produced by `opm:writing-plans` whose `verify` step names a test.

Skip TDD (write tests afterwards, or not at all) for: pure layout and styling, throwaway prototypes,
one-off scripts, configuration edits, glue with no logic. The heuristic: can you write
`expect(fn(input)).toBe(output)` before writing `fn`? If yes, use this skill.

## Step 0: Detect the test runner

Never assume `npm test`. Resolve the commands once, before writing any test.

**Node / TypeScript.** Package manager comes from the lockfile or `package.json` `packageManager`:
`pnpm-lock.yaml` -> pnpm, `yarn.lock` -> yarn, `bun.lock`/`bun.lockb` -> bun, otherwise npm.
The runner comes from `package.json` `scripts.test` and the test imports (`vitest`, `jest`, `bun:test`).
The package manager and the runner are different things: a bun-installed project may still run vitest.

| Stack | `<test>` | `<test-one>` | `<coverage>` |
|---|---|---|---|
| vitest | `<pm> test` or `npx vitest run` | `npx vitest run path/to/file.test.ts` | `npx vitest run --coverage` |
| jest | `<pm> test` or `npx jest` | `npx jest path/to/file.test.ts` | `npx jest --coverage` |
| bun native (`bun:test`) | `bun test` | `bun test path/to/file.test.ts` | `bun test --coverage` |
| pytest | `uv run pytest` or `pytest` | `pytest tests/test_x.py::test_name` | `pytest --cov=<pkg>` |
| flutter | `flutter test` | `flutter test test/x_test.dart` | `flutter test --coverage` |
| dart (no Flutter) | `dart test` | `dart test test/x_test.dart` | `dart test --coverage=coverage` |

`bun test` (native runner) and `bun run test` (runs the package script) are not interchangeable.
Confirm which one the project expects before the RED gate.

Substitute the resolved commands wherever `<test>`, `<test-one>`, `<coverage>` appear below.

## Step 1: State the behaviour

Write the guarantee in one sentence before writing code or tests:

```
As a <role>, I want <action>, so that <benefit>.
```

Turn each guarantee into named test cases: happy path, at least one edge (empty, null, boundary),
at least one error path. If the work comes from a plan, reuse its acceptance criteria rather than
inventing new ones. Keep a running map of `behaviour -> test -> RED evidence -> GREEN evidence`;
it becomes the evidence report in Step 5.

## Step 2: RED - write the test and watch it fail correctly

Write one test (or one small group) for one behaviour. Run `<test-one>`.

**The RED gate.** Production code may only be touched once one of these holds:

- **Runtime RED**: the test file compiles/imports, the new test actually executes, and it fails
  on the assertion or on the missing behaviour.
- **Compile-time RED**: the new test references a symbol or code path that does not yet exist,
  and that missing symbol is exactly the thing you are about to build.

In both cases the failure must be caused by the missing or wrong behaviour, not by:
a typo in the test, a missing import, broken fixtures, a missing dependency, or an unrelated regression.
Read the failure message and confirm it names the right thing. A test that was written but never run is not RED.

If the test passes immediately, stop: either the behaviour already exists, or the test does not test
what you think. Fix the test before proceeding.

**Checkpoint commit** (when the repo is under git):
`test: add failing test for <behaviour>`.

## Step 3: GREEN - minimal code to pass

Write the smallest change that makes the failing test pass. Hardcoding is allowed when it is the
simplest thing; the next test will force generalisation. Do not add behaviour no test asked for.

Run `<test-one>` again and confirm it passes. Then run `<test>` for the whole relevant target to
confirm nothing else broke. Only a GREEN run of the same test that was RED counts.

**Checkpoint commit:** `feat: <behaviour>` or `fix: <bug>`.

## Step 4: REFACTOR - clean up under a green bar

With tests passing, improve the code: remove duplication, rename for clarity, extract functions,
simplify conditionals. Run `<test>` after each meaningful change. Do not add behaviour during refactor;
if you discover a missing case, write it down and go back to Step 2 for it.

**Checkpoint commit** (only if something changed): `refactor: <what was cleaned up>`.

Repeat Steps 2-4 for the next behaviour in the map.

## Checkpoint commit rules

- One commit per stage, on the current branch, in sequence: test -> feat/fix -> refactor.
- Do not squash or rewrite them until the workflow is complete and the evidence report exists.
- The RED commit is valid evidence only if the test was compiled, run, and failed for the intended reason.
- The GREEN commit is valid evidence only if the same test target was rerun and passed.
- If commits are later squashed, copy the RED/GREEN/refactor summary into the PR body or the
  evidence report so a reviewer can still answer "what was verified and how".

## Step 5: Evidence report

After the last GREEN, produce a short report. Put it in the PR description, the task summary, or a
project doc location if one is established (for example `docs/tdd/<task>.md`). Include:

1. **Behaviours** - the sentences from Step 1.
2. **Test table**:

```markdown
| # | Guarantee | Test | RED evidence | GREEN evidence |
|---|-----------|------|--------------|----------------|
| 1 | Empty query returns [] without throwing | src/search.test.ts > "returns [] for empty query" | `npx vitest run src/search.test.ts` -> FAIL: searchItems is not a function | same command -> 1 passed |
| 2 | Limit above 100 is rejected with 400 | tests/test_api.py::test_limit_rejected | `pytest tests/test_api.py::test_limit_rejected` -> AssertionError 200 != 400 | same -> 1 passed |
```

3. **Coverage** (if the project measures it): command and the resulting number, plus any intentional gaps.
4. **Commits**: the checkpoint hashes in order.

Quote real commands and real output excerpts. Never record PASS for a test that was not run.
The final claim of "done" then goes through `opm:verification-before-completion`.

## Examples

### TypeScript (vitest)

```ts
// src/slugify.test.ts  -- RED: slugify does not exist yet
import { describe, it, expect } from "vitest";
import { slugify } from "./slugify";

describe("slugify", () => {
  it("lowercases and hyphenates words", () => {
    expect(slugify("Hello World")).toBe("hello-world");
  });
  it("collapses repeated separators", () => {
    expect(slugify("a  --  b")).toBe("a-b");
  });
  it("returns empty string for blank input", () => {
    expect(slugify("   ")).toBe("");
  });
});
```

```ts
// src/slugify.ts  -- GREEN: minimal implementation
export function slugify(input: string): string {
  return input
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
```

RED run: `npx vitest run src/slugify.test.ts` -> `Error: Failed to resolve import "./slugify"` (compile-time RED, correct reason).
GREEN run: same command -> `3 passed`.

### Python (pytest)

```python
# tests/test_pagination.py  -- RED
import pytest
from app.pagination import clamp_limit

def test_default_limit_when_none():
    assert clamp_limit(None) == 20

def test_limit_is_capped():
    assert clamp_limit(500) == 100

def test_negative_limit_rejected():
    with pytest.raises(ValueError):
        clamp_limit(-1)
```

```python
# app/pagination.py  -- GREEN
DEFAULT_LIMIT = 20
MAX_LIMIT = 100

def clamp_limit(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_LIMIT
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return min(limit, MAX_LIMIT)
```

RED run: `uv run pytest tests/test_pagination.py` -> `ModuleNotFoundError: No module named 'app.pagination'`.
GREEN run: same -> `3 passed`.

### Dart (flutter test)

```dart
// test/cart_total_test.dart  -- RED
import 'package:flutter_test/flutter_test.dart';
import 'package:shop/cart.dart';

void main() {
  test('empty cart totals zero', () {
    expect(cartTotal(const []), 0);
  });
  test('sums price times quantity', () {
    const items = [CartItem(price: 250, quantity: 2), CartItem(price: 100, quantity: 1)];
    expect(cartTotal(items), 600);
  });
}
```

```dart
// lib/cart.dart  -- GREEN
class CartItem {
  const CartItem({required this.price, required this.quantity});
  final int price;
  final int quantity;
}

int cartTotal(List<CartItem> items) =>
    items.fold(0, (sum, item) => sum + item.price * item.quantity);
```

RED run: `flutter test test/cart_total_test.dart` -> `Error: Method not found: 'cartTotal'`.
GREEN run: same -> `All tests passed!`.

## Testing habits that keep the cycle honest

- Test observable behaviour, not internals (`screen.getByText("Count: 5")`, not `component.state.count`).
- One behaviour per test; the test name states the guarantee.
- Each test creates its own data; no ordering dependencies between tests.
- Mock only at true boundaries (network, clock, filesystem, third-party SDKs). Mocking your own modules hides bugs.
- Prefer semantic selectors and public APIs over CSS classes and private members.
- Keep unit tests fast; slow suites get skipped, and skipped suites rot.
- Never leave `.skip`, `.only`, `xit`, or `@pytest.mark.skip` in a commit without a linked reason.

## Common failure modes

| Symptom | What went wrong | Fix |
|---|---|---|
| Test passes on first run | Behaviour already exists or the assertion is vacuous | Strengthen the assertion or delete the redundant test |
| RED caused by import typo | Not a valid RED | Fix the test, rerun, confirm failure names the missing behaviour |
| Wrote three functions to pass one test | Skipped "minimal" | Revert to the smallest change; let the next test drive the rest |
| Refactor changed behaviour | Refactor and feature mixed | Split: commit the refactor under green first, then a new RED |
| Evidence report says PASS for an unrun test | Fabricated evidence | Rerun and paste the real output, or mark it "not run" |

## Related skills

- `opm:verification-before-completion` - the final gate before claiming the work is done.
- `opm:executing-plans` - how TDD tasks fit inside a plan's task loop.
- `opm:compound-learnings` - capture a surprising root cause after the bug is fixed.

<!-- Adapted from affaan-m/ecc (MIT) -->
