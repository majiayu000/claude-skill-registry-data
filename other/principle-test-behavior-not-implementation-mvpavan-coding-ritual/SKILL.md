---
name: principle-test-behavior-not-implementation
description: Apply when writing, changing or keeping any test.
disable-model-invocation: true
---

# Test behavior, not implementation

A test earns its place by catching broken behaviour and nothing else.

- Judge every test by two imagined edits: breaking the behaviour must fail
  it, and restructuring the internals must not.
- Exercise behaviour through public interfaces.
- Assert exactly what the contract promises, no less and no more; the
  contract decides whether a call, an absence, a payload or an error type is
  behaviour.
- Pair an assertion that something did not happen with a positive case
  showing the same test would see it happen.
- Watch for hollow forms: an assertion looser than the contract, a restated
  constant the code never reads, an assertion on data the test built itself.
- Judge a suite by the behaviours and edge cases it exercises, not by line
  coverage.
- When internals change, rewrite or delete tests that only protect the old
  implementation, asserting the current contract instead.
