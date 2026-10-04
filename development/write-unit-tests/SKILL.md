---
name: write-unit-tests
description: "Writes unit tests, and only when the user has asked for them. Invoked as /write-unit-tests <scope>, or when the user asks in their own words for unit tests to be written or an existing suite extended. Reads the source in scope, separates business logic from helper code, selects only the edge cases and unwanted behaviors worth pinning, holds the plan under an estimated-coverage ceiling, then writes the Go or Node tests. Nothing else starts it: a feature landing, a bug fix, a refactor, a PR being prepared, and a _test.go or *.test.js file sitting in the diff are not requests for tests. Also the reference a code review reads when auditing an existing suite."
user-invocable: true
---

# Write Unit Tests

**Tests are written on request and never on initiative, and the ones written pin the behavior that can actually break.**

## When this skill runs

The user asking for unit tests is the only thing that starts this skill, whether by name or in their own words. Development carries no test step, so a session that was never asked for tests finishes with none.

A code review reads this skill to judge a suite that already exists. That reading produces findings, never tests, because a review that starts writing has stopped being a review.

The scope is whatever the user named. When they named none, it is the current work stream: the session's changes, the branch, or the pull request.

## The method

Five steps, each feeding the next, ending in a list of cases before any test file is opened. The steps are worked through rather than reported. The user asked for tests, so the deliverable is the tests and not an account of how they were chosen.

The rules below are applied, not argued with. A case that needs an argument to qualify has already failed, because the reasoning that admits it will admit anything and the result is a suite that asserts the implementation back to itself.

### Step 1: Read the source in scope

Read the implementation before considering a single case. What is being read for is the intended behavior, since a test derived from the code passes by construction and locks any bug in place. Both the code and its tests answer to what the code was supposed to do.

### Step 2: Separate the true functionality from the helpers

Name the functionalities the scope delivers, then sort every function into one of two piles.

True functionality is the decision logic: the branching, the validation, the state transitions, the parsing, the ordering, the error paths. Helper functionality is everything that carries data between those decisions.

A function with no decision logic of its own gets no test. A thin wrapper over a directory creation call, a getter, or plain arithmetic exercises the language and the standard library rather than your code, and a failure there is not one you can act on.

Only the true-functionality pile continues to Step 3.

### Step 3: Select the cases

Two kinds of case qualify, and each has to point at something concrete in the code read in Step 1.

- **An unwanted behavior that has to stay impossible.** The malformed input that must be rejected, the boundary that must not be crossed, the state that must never be written. It qualifies when the code contains the specific guard against it.
- **A positive behavior at an edge.** Empty and nil or undefined input, zero-length and single-element collections, the first and last element, the boundary value on both sides, concurrent access, overflow. It qualifies when the code handles that edge deliberately.

What qualifies is what is glaringly obvious from the source or genuinely unique to this situation. Enumerating every input a function could theoretically receive is the failure mode this step exists to prevent, because the set of possible bad inputs has no end and a suite that chases it stops being about the code.

Judge each case by whether it can fail for a real reason. The test to apply is naming the change to the implementation that would make it fail; a case with no such change is a happy-path assertion wearing an edge case's name.

### Step 4: Estimate the coverage, then cut

Before writing anything, estimate what fraction of the statements in the packages under scope the planned cases would execute.

| Estimate | Reading |
|---|---|
| At or under 25% | The selection held. Proceed. |
| 25% to 35% | Acceptable. Proceed if every case survives the Step 3 test. |
| Over 35% | The selection was stretched. Cut. |

A figure above 35% is a direct indicator that cases were admitted by justification rather than by the rules, so it is treated as evidence about the plan rather than as a result about the code.

Cutting is done in one pass rather than one case at a time: work out how many cases have to go to land at or under 25%, drop that many weakest cases together, then re-estimate. Removing one and re-checking preserves whatever reasoning inflated the list in the first place.

### Step 5: Write them

Write only the surviving cases. Finish the implementation first, because tests written against a half-built function describe the scaffolding rather than the behavior.

Unit tests exercise one package or module in isolation. Standing up a server, opening a socket, or crossing package boundaries end to end belongs to a separate script, since a unit suite that needs a listening port fails for reasons unrelated to the logic under test.

Table-driven tests are the default shape, because adding the eighth case should cost one line rather than one function.

Mocks are verified once against public documentation or a real response, then committed and pinned as a fixture. A test that reaches a live service at run time is slow and flaky, and one written from memory asserts a shape the service may never have had.

## Go mechanics

Tests live in the package they cover, in the same directory, as `package foo` or `package foo_test`.

One `_test.go` file per package is enough. Collect that package's cases into a single file rather than mirroring each source file, and split only when one file becomes genuinely unwieldy.

`t.Context()` supplies a test's context, rather than `context.WithCancel(context.Background())`, since it is cancelled when the test ends without a `defer` of your own.

`for b.Loop()` drives the main benchmark loop rather than `for i := 0; i < b.N; i++`, because it excludes setup from the timed region automatically.

`omitzero` rather than `omitempty` in JSON struct tags for `time.Time`, `time.Duration`, structs, slices, and maps. `omitempty` never omits a zero `time.Time`, so the field ships as a meaningless timestamp.

```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        in      string
        want    Result
        wantErr bool
    }{
        {"empty input", "", Result{}, true},
        {"only separator", ",", Result{}, true},
        {"trailing separator", "a,", Result{Items: []string{"a"}}, false},
        {"single element", "a", Result{Items: []string{"a"}}, false},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(t.Context(), tt.in)
            if (err != nil) != tt.wantErr {
                t.Fatalf("Parse(%q) err = %v, wantErr %v", tt.in, err, tt.wantErr)
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("Parse(%q) = %v, want %v", tt.in, got, tt.want)
            }
        })
    }
}
```

## Node mechanics

Tests live under `test/` as `*.test.js`, or colocated as `*.test.js` beside the module. They run with `node --test`, and `node --test --watch` during development.

The built-in runner covers this, so no test-framework dependency is added. `node:assert/strict` is the assertion import, since the loose variants treat `1` and `'1'` as equal and hide exactly the coercion bugs a test should catch.

A live end-to-end script, such as `test/e2e.mjs` booting the server over HTTP and WebSocket, stays separate from the unit suite and stays optional. Running it as part of `node --test` makes every unit run depend on a free port.

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parse } from '../src/parse.js';

test('parse', async (t) => {
  const cases = [
    { name: 'empty input', in: '', want: [], throws: true },
    { name: 'only separator', in: ',', want: [], throws: true },
    { name: 'trailing separator', in: 'a,', want: ['a'], throws: false },
    { name: 'single element', in: 'a', want: ['a'], throws: false },
  ];
  for (const c of cases) {
    await t.test(c.name, () => {
      if (c.throws) {
        assert.throws(() => parse(c.in));
        return;
      }
      assert.deepEqual(parse(c.in), c.want);
    });
  }
});
```

Async setup and teardown hang off `before` and `after` inside the test:

```js
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';

test('handler', async (t) => {
  let store;
  before(() => { store = new Map(); });
  after(() => { store.clear(); });

  await t.test('rejects unknown id', () => {
    assert.throws(() => lookup(store, 'nope'), /not found/);
  });
});
```
