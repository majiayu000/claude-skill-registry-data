---
name: testing-philosophy
description: >-
  Guide test design, writing, review, and repair. Use for coverage, TDD, flaky
  tests, mocks, test layers, snapshots, property tests, regressions,
  concurrency, or any change that adds, weakens, skips, or deletes tests.
  Prefer behavior through stable seams and honor a user-specified test layer.
---

# Testing Philosophy

Choose tests that catch behavior regressions and survive implementation changes. Start with the
caller-visible guarantee, test it through a stable boundary, and keep the path deterministic. Treat
the guidance below as defaults with reasons; explain a deliberate trade-off when you depart from it.

## Work the decision in order

1. **Name the guarantee.** State what a caller or user should observe: a result, error, response,
   persisted value, or event. Choose a public or otherwise stable seam. Ask whether the test would
   still make sense after replacing the implementation with a different one that preserves that
   guarantee. If not, it is probably pinned to implementation shape.
2. **Honor a requested layer.** If the caller names integration, scenario, E2E, or service-start
   coverage, deliver that layer. A unit test, one mocked interaction, or a recording fake around one
   component can support it, but cannot stand in for it. If the harness is missing, identify the
   blocker and say what coverage remains owed. When no layer is named, choose the highest-purity
   test that still exercises the real behavior; widen to real services or end-to-end wiring when the
   risk lives there, such as persistence, migrations, money, or cross-service contracts.
3. **Keep the behavior real and push I/O outward.** Prefer the functional core / imperative shell
   and sans-I/O patterns. Substitute at genuine boundaries such as disk, network, clock, randomness,
   or external processes. Use a fake there when practical; avoid mocking your own business modules.
   Use interaction assertions only when the interaction is the behavior ("charge the payment API
   exactly once"); asserting on internal call sequences is not. Extent (how much application code
   runs) and purity (how much I/O or nondeterminism occurs) are separate: broad in-memory tests can
   be fast and refactor-safe.
4. **Choose the smallest useful form.** Start with examples in a table and a thin shared `check`
   helper. Add properties, exhaustive cases, fuzzing, snapshots, differential tests, or fault
   injection when the input space, output, or failure risk makes that technique useful. Load
   [`REFERENCE.md`](REFERENCE.md) when applying one of these techniques or making a non-obvious
   trade-off.
5. **Make failures reproducible and readable.** Control clocks, random seeds, ordering, locale, and
   environment. Await background work through a real completion signal; never use sleeps as
   synchronization. Assert on observable outcomes and specific expected errors. Keep snapshots and
   golden diffs small enough to review. Gate slow tests at runtime (skip unless an env var is set,
   and print how to enable them), not behind build tags that hide compile errors.
6. **Prove the test matters.** For a regression, reproduce the bug first when practical and confirm
   the test fails for the expected reason. Read test failures and generated diffs before changing
   expectations. Never make a suite green by deleting, skipping, or weakening a valid assertion.

## Choose effort by risk

Use many fast, mostly pure tests at their natural extent and a thin shell of slower integration
coverage. Put more effort into core logic, money, authorization, data integrity, migrations,
concurrency, parsers, and public compatibility. A trivial pass-through, generated code, or throwaway
spike may not need a test when a cheaper check covers its risk; state that trade-off. “Hard to test”
usually points to a boundary or design problem worth addressing.

Coverage is diagnostic: use it to find untested branches, not as a quality target. Line execution does
not show that assertions catch defects; mutation testing can expose assertions that do not bite.
Flakiness is a bug to diagnose at its source, not a reason to add retries. A test that observes only
private state or incidental logs is usually brittle; introduce a deliberate observable contract when
the behavior truly needs inspection.

## Review checklist

- Does the test protect a named caller-visible behavior and fail for the plausible regression?
- Does it exercise the requested layer and real behavior, substituting only at actual boundaries?
- Is the test deterministic, quick enough for its lane, and clear when it fails?
- Are changed snapshots/goldens reviewed, and are removed or weakened assertions accounted for?
- Were relevant tests run, with unrun layers and residual risk stated plainly?

## Anti-patterns

- Testing private internals or asserting on internal call order.
- Over-mocking: mocking your own code, or asserting "method X was called with Y."
- Asserting on logs or incidental output to infer behavior.
- Blindly checked-in snapshots nobody reads.
- Tests that restate the code (`assert add(2,3) == 2+3`) or assert nothing ("doesn't throw").
- Ice-cream-cone suites: mostly slow end-to-end tests, few fast ones.
- Coverage as a target: it shows untested lines, not whether tested lines are tested well.
- Sleeps and unawaited background work; ignored flaky tests; build-tag-hidden slow tests.
- Deleting, skipping, weakening, or loosening a test to make a suite go green.

## Agent conduct

Optimize for *true*, not for green.

- Never silence a failure to pass: no deleting or skipping a failing test, loosening an assertion,
  widening a tolerance, or wrapping the body in a blanket catch. If the test is genuinely wrong, fix
  it deliberately and say why.
- Read the actual failure output before reacting. Never blanket-update snapshots or accept generated
  expectations without reading the diff.
- Verify your test can fail. A test you have only seen pass might assert nothing: break the code
  once to confirm it goes red, then revert.
- Match the repo's conventions (its `check` helpers, fixtures, naming, layout) and run the relevant
  suite the way the project runs it before adding a new framework.
- Never claim tests pass without running them. State residual risk plainly when you skipped slow or
  integration tests or could not run the full suite.

## Examples

For “add an E2E scenario for tracing and consumption,” drive trace ingestion through the requested
scenario and assert externally visible consumption telemetry. A client-level recording fake is only
supporting coverage. For “add tests for kept/dropped span accounting” with no layer specified, exercise
the real accounting logic in memory and fake only its I/O boundary; use a broader layer only if the
risk depends on wiring or persistence.

```python
# Brittle: welded to internals. Breaks when you rename _bucket_for or switch to a tree.
def test_cache_uses_lru_bucket():
    c = Cache(); c._buckets[c._bucket_for("k")] = Node("k", 1)
    assert c._evict_candidate()._key == "k"

# Behavioral: states a guarantee a caller relies on. Survives any rewrite that keeps it.
def test_lru_evicts_least_recently_used():
    c = Cache(capacity=2)
    c.put("a", 1); c.put("b", 2); c.get("a"); c.put("c", 3)  # "b" is now coldest
    assert c.get("b") is None
    assert c.get("a") == 1 and c.get("c") == 3
```

Funnel each kind of test through one `check` helper that owns the call shape, so a signature change
is a one-place fix and every case inherits the same failure message:

```go
func check(t *testing.T, input string, want []Token) {
    t.Helper()
    got := Lex(input)
    if !reflect.DeepEqual(got, want) { t.Fatalf("Lex(%q)\n got: %v\nwant: %v", input, got, want) }
}

func TestLexer(t *testing.T) {
    check(t, "", nil)
    check(t, "1+2", []Token{Num("1"), Plus, Num("2")})
}
```

## Deeper material

[`REFERENCE.md`](REFERENCE.md) covers each technique in depth with examples and failure modes, the
test-double taxonomy (dummy / stub / fake / spy / mock), property-discovery patterns, determinism
patterns for time / concurrency / network, coverage / MC/DC / mutation testing, robustness and fault
injection, a seam-by-system chooser, a per-language cheat sheet, a workflow for diagnosing a bad
suite, and case studies (SQLite, compiler/IDE suites, sans-I/O). Load it when applying a specific
technique or making a non-obvious trade-off, not for routine "write a sensible test" work.
