---
name: mutation-testing
description: >
  Measure and improve test-suite strength with mutation testing: pick a tool (mutmut or
  cosmic-ray for Python, cargo-mutants for Rust, Stryker for JS/TS, PIT for Java), scope runs to
  changed code, interpret killed/survived/timeout/no-coverage mutants, recognize equivalent
  mutants, write the missing assertions, and set sensible score gates in CI. Use when line
  coverage is high but you doubt the assertions, when reviewing a test suite's quality for
  critical logic, or when adding a quality gate for new code. Do NOT use for writing first
  tests (unit-testing, test-driven-development), exploring input space (property-based-testing,
  fuzz-testing), or whole-repo runs on slow suites without scoping.
compatibility: >
  Agent Skills-compatible coding agents. Tool docs checked: Stryker (JS) config, PIT Maven
  plugin, cargo-mutants, mutmut 3.x. Python, Rust, JS/TS and Java projects with a passing
  baseline test suite.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "mutation-testing, mutmut, cosmic-ray, cargo-mutants, stryker, pitest, test-quality"
  topics: "software-development, testing, quality"
---

# Mutation Testing

A mutation tool makes one small change to production code (flip `<` to `<=`, delete a statement, replace a return value) and reruns the tests. If a test fails the mutant is *killed*; if all pass it *survived*, which means no test would notice that bug. Coverage says code ran; mutation testing says a test would fail if the code were wrong.

Boundaries: writing the tests themselves is `unit-testing` / `test-driven-development`; stronger input exploration is [property-based-testing](../property-based-testing/SKILL.md) and [fuzz-testing](../fuzz-testing/SKILL.md); contract tests across services are [contract-testing](../contract-testing/SKILL.md).

## Non-negotiable rules

1. The baseline suite must pass, deterministically, before mutating. A flaky baseline makes survivors meaningless. Fix or quarantine flakes first.
2. Mutation tools execute your tests many times and write mutated source to disk. Run on a clean git branch or copy (cargo-mutants and Stryker work in a temp copy by default; `mutmut apply` writes into your tree, so commit first). Never run against code with side effects on real systems (databases, cloud, payments); tests must already be hermetic.
3. A survived mutant is a question, not a defect count. Do not weaken production code or add `no mutate` pragmas just to raise the score; every exclusion needs a written reason.
4. Never chase 100%. Equivalent mutants (behavior unchanged) make it unreachable and the chase produces test-shaped noise. Gate on a threshold and on *no surviving mutants in the lines you changed that are semantically meaningful*.
5. Do not edit tests to assert implementation details (private calls, exact log strings) only to kill a mutant; assert observable behavior.

## Workflow

### 1. Decide whether and where

Good targets: pure logic with branching (pricing, validation, parsers, state transitions, permission checks). Poor targets: generated code, config, logging, thin wrappers, UI layout. Start with one module or the diff of one PR, never the whole repo first: cost is roughly (number of mutants) x (test time), so a 2-minute suite with 5,000 mutants is days unless tests are selected per mutant.

### 2. Pick the tool and run a bounded pass

| Language | Tool | Scoping / speed levers |
|---|---|---|
| Python | mutmut (3.x), cosmic-ray | mutmut: set source paths in `[tool.mutmut]` of `pyproject.toml` (or `setup.cfg`), `also_copy` for needed files, `do_not_mutate`; `# pragma: no mutate` per line. Commands include `mutmut run`, `mutmut browse`, `mutmut apply` (check `mutmut --help` for result viewing on your version). cosmic-ray: `cosmic-ray init <config.toml> <session.sqlite>`, then `cosmic-ray exec ...`, report with `cr-report` |
| Rust | cargo-mutants | `cargo mutants`; `--list` shows mutants without running; `--in-diff changes.diff` mutates only code touched by a diff (generate with `git diff`); `--package`, `--file`, `--re` / `--exclude-re` (regex filters on mutant names; run `cargo mutants --help` for your version); `--shard k/n` splits across CI jobs (all shards need identical args); `--baseline=skip` after a known-good run; `--timeout`. Results in `mutants.out`. Skip code with the `#[mutants::skip]` attribute (add the `mutants` crate) |
| JS/TS | Stryker | `stryker.config.json`: `mutate` globs (or `file:lines` ranges), `testRunner`, `coverageAnalysis` (`perTest` is the default in recent versions), `thresholds` (`high` 80 / `low` 60 / `break` null by default; set `break` to fail the build), `incremental: true` to reuse results, `ignoreStatic`, `concurrency`, `reporters` |
| Java | PIT (pitest) | Maven: `mvn test-compile org.pitest:pitest-maven:mutationCoverage`; `targetClasses`, `targetTests`, `mutationThreshold` (percent), `withHistory`, `mutators`, `timeoutConstant` (default 4000 ms) and `timeoutFactor` (default 1.25). HTML report in `target/pit-reports/` |

Always confirm option names against the installed version's `--help`/docs; these tools change defaults between majors.

### 3. Classify every survivor (this is the real work)

For each surviving mutant, in the report diff, answer in order:

1. **Equivalent?** Does the mutated program behave identically on all inputs? Examples: `i < n` to `i != n` in a loop that always exits at `n`; changing a cache-capacity hint; reordering independent statements; mutating a value that is later overwritten; `x >= 0` to `x > 0` where `x == 0` is unreachable by invariant. Equivalence is undecidable in general; judge by reasoning, and record the justification. Mark and exclude with the tool's mechanism plus a comment.
2. **Untested behavior?** (most common) Write a test that fails on the mutant and passes on the original: a boundary value, the *other* branch, an exact return value instead of `is not None`, an assertion on a side effect.
3. **Dead or redundant code?** If no input can distinguish it, simplify the code (delete the branch) instead of testing it.
4. **Test is too coarse?** The test runs the code but asserts nothing relevant (smoke test). Strengthen the assertion.
5. **Timeout?** Mutant introduced an infinite loop; tools usually count this as detected. Verify the timeout is sane; if a test genuinely hangs you have a missing test timeout.
6. **No coverage?** No test executes that line at all; add a test or accept (and document) that the code is untested/unneeded.

### 4. Kill with intent

Mutant: `if amount > limit` became `if amount >= limit` and survived. Missing test: `amount == limit`. Write it:

```python
def test_exactly_at_limit_is_allowed():
    assert check_limit(amount=100, limit=100) is True   # boundary pinned
```

Rerun only that mutant (mutmut: run for that name; cargo-mutants: `--file` or `--re`; Stryker: `mutate` line range). Confirm killed, and confirm the new test passes on the original code.

### 5. CI strategy

- PR gate: mutate only changed lines/files (cargo-mutants `--in-diff`; Stryker `--incremental` plus mutate globs; PIT `withHistory` or SCM goals; mutmut scoped to changed modules). Set `break`/`mutationThreshold` for *new code* slightly below your current score and ratchet up.
- Nightly: broader run, sharded (`cargo mutants --shard k/n` in a GitHub Actions matrix with `fail-fast: false`, archive `mutants.out`), results tracked as a trend.
- Keep a time budget: abort at N minutes and report partial results rather than silently skipping.
- Never block merges on survivors in files with no behavior change (refactors, docs).

### 6. Report with evidence

Report: tool+version, scope, mutants generated, killed/survived/timeout/no-coverage counts, score = (killed + timeouts) / (generated minus unviable and minus mutants you have justified as equivalent); timeouts count as detected, no-coverage mutants count as not detected (state this convention, since tools differ), list of survivors with disposition (killed by new test X, equivalent because Y, deferred). A score alone is not evidence.

## Worked example (Python)

```python
def apply_discount(price: int, pct: int) -> int:
    if pct < 0 or pct > 100:
        raise ValueError("pct")
    return price - price * pct // 100
```

Existing test: `assert apply_discount(200, 50) == 100`. Typical survivors: `pct > 100` to `pct >= 100` (no test at 100), `pct < 0` to `pct <= 0` (no test at 0), error-path message change (no test of exception), `//` to `/` (200*50 is exactly divisible; integer-vs-float result still `==` in Python, so only a type assertion or an indivisible case such as `apply_discount(99, 33)` exposes it).

Add tests at 0, 100, -1, 101 with `pytest.raises(ValueError)`, and `apply_discount(99, 33) == 67` (checking exact integer arithmetic: 99 - 32 = 67). Survivors now killed, except mutating the `ValueError("pct")` message. That survivor is not equivalent (behavior does change); label it an accepted survivor / unspecified behaviour, unless the message is part of the API, in which case assert it with `match=`. Record the decision either way.

## Anti-patterns

- Running everything, waiting hours, then ignoring the report.
- Optimizing the percentage: adding `no mutate` pragmas, deleting hard-to-kill code, or writing tests that mirror the implementation.
- Treating timeouts as failures of the tool and discarding them.
- Using mutation score to compare teams or as a performance metric.
- Running on a flaky or order-dependent suite; parallelization then produces false survivors.
- Forgetting that mutation tools mutate the code under test, not the test code.
- Applying mutants (`mutmut apply`) and leaving them in the working tree.

## Verification checklist

- [ ] Baseline passes cleanly and deterministically
- [ ] Scope bounded (module or diff) and time budget stated
- [ ] Every survivor has a disposition: killed, equivalent (with reason), dead code removed, or deferred
- [ ] New tests fail against the mutant and pass on original code
- [ ] No source mutations left applied; no unexplained exclusion pragmas
- [ ] CI gate threshold and ratchet plan documented

## References

- [Equivalent mutants and mutation operators](references/equivalent-mutants.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
