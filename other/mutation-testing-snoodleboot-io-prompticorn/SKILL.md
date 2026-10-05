---
name: mutation-testing
description: "Line coverage answers \"did this line execute during the test run\"."
---

# Mutation Testing (Verbose)

## Core Patterns

### Why Coverage Is the Wrong Question

Line coverage answers "did this line execute during the test run". That is a much
weaker claim than "if this line were wrong, a test would fail" — and the second is
the only claim anyone actually cares about. The gap between them is where escaped
bugs live.

Mutation testing closes the gap operationally. It edits the production code in
small, syntactically valid ways — a *mutant* — reruns the tests, and asks whether
anything went red. A mutant that causes a failure is **killed**. A mutant that
leaves the suite green **survived**, and a survivor is direct evidence that the
behaviour it changed is unverified.

The canonical demonstration:

```python
def apply_discount(total: Decimal, is_member: bool) -> Decimal:
    if total > 100 and is_member:
        return total * Decimal("0.9")
    return total
```

```python
def test_member_gets_discount():
    assert apply_discount(Decimal(150), True) == Decimal(135)
```

That test reports 100% line and 100% branch coverage of the function on many
tools' definitions of the taken path. Now generate mutants:

| # | Mutation | Result | Verdict |
|---|---|---|---|
| 1 | `total > 100` → `total >= 100` | test still passes | **survived** |
| 2 | `and` → `or` | test still passes | **survived** |
| 3 | `Decimal("0.9")` → `Decimal("1.1")` | 165 ≠ 135 | killed |
| 4 | `return total` → `return None` | never reached by the test | **survived** |

Three of four survive. Mutant 1 says the boundary at exactly 100 is untested.
Mutant 2 says no test ever supplies a non-member, so the conjunction could be a
disjunction and nobody would know — a real pricing bug that gives every
big-basket guest a 10% discount. Mutant 4 says the no-discount path has no test
at all despite the coverage report. The tests needed:

```python
@pytest.mark.parametrize(
    "total,is_member,expected",
    [
        (Decimal(100), True,  Decimal(100)),   # kills mutant 1: boundary is exclusive
        (Decimal(101), True,  Decimal("90.9")),
        (Decimal(150), False, Decimal(150)),   # kills mutant 2: non-member pays full
        (Decimal(50),  True,  Decimal(50)),    # kills mutant 4: fall-through returns total
    ],
)
def test_discount_rules(total, is_member, expected):
    assert apply_discount(total, is_member) == expected
```

This is why mutation testing is described as testing the tests. It converts a
vague "are our tests any good" into a concrete, reviewable list of behaviours
nobody checks.

### The Operators

Mutation tools apply a fixed catalogue of small edits. Knowing the catalogue lets
you predict what a run will find before you pay for it.

| Class | Mutation | What a survivor proves |
|---|---|---|
| Conditional boundary | `<` → `<=`, `>` → `>=` | Off-by-one at the boundary is unobserved |
| Negate conditional | `==` → `!=`, `<` → `>=` | The branch predicate is never both-ways tested |
| Logical connector | `and` → `or` | One operand is never varied independently |
| Arithmetic | `+` → `-`, `*` → `/` | The computed value is not asserted, only its type or truthiness |
| Constant | `0` → `1`, `""` → `"XX"`, `True` → `False` | A literal is load-bearing but unverified |
| Return value | `return x` → `return None` | The return is never inspected on that path |
| Statement removal | delete a call, e.g. `audit.log(...)` | A side effect is claimed but never asserted |
| Collection | `[]` → `[None]`, break slice bounds | Empty/edge collection handling untested |

Removed-call mutants are the most consistently instructive. If deleting
`audit.log(event)` or `cache.invalidate(key)` kills nothing, then the side effect
your feature exists to produce is not under test.

### Reading the Score

```
mutation score = killed / (generated - equivalent)
```

An **equivalent mutant** is a syntactic change with no semantic effect, so no test
can possibly kill it. The classic:

```python
i = 0
while i < n:       # mutated to: while i != n
    i += 1
```

With `i` starting at 0 and incrementing by exactly 1, the two loops are
indistinguishable. Detecting equivalence in general reduces to deciding program
equivalence, which is undecidable — no tool will ever do this for you. Practical
consequences:

- **100% is not the goal.** Chasing it means writing tests to kill mutants that
  cannot be killed.
- 80%+ on core domain logic is a strong result. 60% suite-wide is respectable.
- The score is a trend line, not a grade. The *survivor list* is the deliverable.
- Mark confirmed equivalents so they stop reappearing — a Stryker
  `// Stryker disable next-line ...` comment, or a triage file — otherwise every
  run re-litigates the same handful.

Set the CI threshold below your current score so the build breaks on regression,
not on ambition:

```json
{
  "mutate": ["src/pricing/**/*.ts", "src/entitlements/**/*.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress"],
  "thresholds": { "high": 80, "low": 65, "break": 60 }
}
```

### Cost, and Therefore Scope

Mutation testing is expensive in a way that is structural, not incidental. The
work is approximately:

```
runtime  ≈  mutants × (tests covering the mutated line) × per-test time
```

A 2,000-line module typically yields 600–1,200 mutants. Against a suite where the
covering subset takes 3 seconds, that is 30–60 minutes for one module; run against
a whole repo with a 40-second suite, it is comfortably a day. Tools mitigate with
coverage-based test selection (run only tests that touch the mutated line),
parallel workers, and early exit on first kill — but the product form never goes
away.

So scope deliberately:

1. **Restrict to changed files.** Stryker supports git-diff scoping directly:
   ```bash
   npx stryker run --since=main --incremental
   ```
   The incremental report is cached and reused, so a PR pays only for its own diff.
2. **Restrict to code where being wrong is expensive** — pricing, permissions,
   tax, quota enforcement, state machines, retry/idempotency logic.
3. **Run the broad sweep nightly or weekly**, never in the per-commit gate. A
   mutation job in the merge path gets disabled within a month for being slow, and
   then you have neither the job nor the discipline.
4. **Exclude the low-yield areas**: generated code, migrations, serializers,
   dependency wiring, `__repr__`. Mutants there survive for uninteresting reasons
   and drown the signal.

```python
# setup.cfg
[mutmut]
paths_to_mutate = src/billing/,src/entitlements/
tests_dir = tests/unit/
```

```bash
mutmut run
mutmut results          # summary by status
mutmut show 47          # the exact diff of survivor 47
```

### Turning Survivors Into Tests

Triage each survivor into one of four buckets:

1. **Missing assertion.** The line ran, its effect was never checked. Strengthen
   the existing test — this is the most common and the cheapest fix.
2. **Missing input class.** No test supplies the input that distinguishes the
   mutant. Add a parametrized case, not a new test function.
3. **Equivalent.** Mark it, with a one-line reason. Do not write a test.
4. **Dead code.** Nothing can reach it. Delete the code — a survivor is sometimes
   telling you the branch is unreachable, which is a better finding than a test.

Bucket 1 dominates in suites that were written to a coverage target, because a
coverage target rewards execution and is indifferent to assertions. That is the
same failure mode `test-coverage-categories` addresses from the other direction:
mutation testing finds the gaps empirically, coverage categories prevent them by
construction.

## Common Anti-Patterns

❌ **Treating the mutation score as the goal** — drives tests written to kill
mutants rather than to describe behaviour.
✅ Use the score as a regression guard; use the survivor list as the work item.

❌ **Running mutation testing on the whole repo in the PR gate** — hours of CI, so
it gets switched off.
✅ Diff-scoped and incremental per PR; full sweep nightly on selected packages.

❌ **Chasing 100%** — spends effort on undecidable equivalents.
✅ Set the break threshold just under current score and ratchet it upward.

❌ **Mutating serializers, migrations, and generated code** — survivors that mean
nothing bury survivors that mean everything.
✅ Point it at domain logic where a wrong answer costs money or leaks data.

❌ **Killing a mutant with an over-specific assertion** — e.g. asserting an exact
log string to kill a removed-call mutant, which then breaks on any copy edit.
✅ Assert that the effect happened and carries the right key fields.

❌ **Re-triaging the same equivalents every run** — the survivor list stops being
read.
✅ Record equivalents inline or in a triage file with a stated reason.

❌ **Interpreting a low score as "write more tests"** — volume is rarely the
problem.
✅ Read the diffs; the usual answer is stronger assertions in tests you already
have.

## Mutation Testing Checklist

- [ ] Tool wired up for the language (mutmut / cosmic-ray, Stryker, PIT)
- [ ] `paths_to_mutate` scoped to high-consequence domain logic
- [ ] Generated code, migrations, and serializers excluded
- [ ] Diff-scoped incremental run available for PRs
- [ ] Full sweep scheduled nightly or weekly, outside the merge gate
- [ ] Break threshold set just below the current score, ratcheted upward
- [ ] Survivor list reviewed by a human, not just the aggregate score
- [ ] Each survivor triaged: missing assertion / missing input / equivalent / dead
- [ ] Confirmed equivalent mutants recorded with a reason so they stop recurring
- [ ] Removed-call mutants specifically checked — side effects are the usual gap
- [ ] Boundary mutants closed with both-sides parametrized cases
- [ ] Score tracked over time as a trend, not reported as a grade
