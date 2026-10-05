---
name: testing-strategies
description: "Three shapes get argued about as if one were correct."
---

# Testing Strategies (Verbose)

## Core Patterns

### The Shape Debate, Framed Properly

Three shapes get argued about as if one were correct. Each is a claim about where
your defects live, and that is an empirical question about your architecture — not
a matter of taste.

**The pyramid** (Mike Cohn, *Succeeding with Agile*, 2009) puts the mass at the
unit level: many fast unit tests, fewer integration tests, a thin cap of
end-to-end. It optimizes for feedback speed and failure locality. When a pyramid
test fails you usually know the function before you open the log. Its blind spot
is everything that only exists between components: serialization, transactions,
wiring, configuration, and any assumption two modules hold differently.

**The testing trophy** (Kent C. Dodds) puts the mass at integration: static
analysis at the base, some unit tests, a bulk of integration tests, a thin
end-to-end top. It optimizes for confidence per test — an integration test in a
web app exercises routing, validation, serialization, and persistence at once, so
it fails for reasons users would actually experience. It costs setup time and
gives coarser failure locality.

**The honeycomb** (Spotify) argues that in a microservice estate, most services
contain little algorithmic logic; they validate, map, and forward. The interesting
defects are at the seams, so the mass belongs in service-level integration tests,
with thin layers of unit and end-to-end either side.

The useful synthesis is a question rather than a shape: **where do defects that
reach production actually come from?** Look at the last thirty incidents.

- If they are wrong calculations, bad edge-case handling, misread rules — you have
  deep domain logic and a pyramid is right.
- If they are null in an unexpected field, a serialization mismatch, a
  transaction not committed, an env var wrong in one environment — the defects are
  at the seams, and unit tests will never see them.
- If they are "service A started sending a field service B could not parse" —
  neither shape helps; you need contract testing.

A team with a mismatch pays twice: the tests they have do not find the bugs they
get, and the tests they need feel expensive because the budget is spent elsewhere.

### Choosing the Level for a Given Behaviour

The rule: **test at the narrowest level where the behaviour is fully expressed and
the failure is unambiguous.**

```python
# Domain rule with boundaries -> unit test. Fast, exhaustive, no I/O.
@pytest.mark.parametrize(
    "days_late,expected_fee",
    [(0, Decimal(0)), (1, Decimal("5.00")), (30, Decimal("5.00")), (31, Decimal("15.00"))],
)
def test_late_fee_tiers(days_late, expected_fee):
    assert late_fee(days_late) == expected_fee
```

```python
# Behaviour that only exists when layers meet -> integration test.
def test_order_rollback_leaves_no_partial_rows(client, db):
    resp = client.post("/orders", json=payload_with_out_of_stock_item())
    assert resp.status_code == 409
    assert db.query(Order).count() == 0
    assert db.query(OrderLine).count() == 0      # no unit test can observe this
```

That second test is exactly the class the pyramid misses. The transaction boundary
is not a property of any single function; it exists only in the composition.

Corollaries worth stating explicitly:

- If a bug can only occur when two components meet, do not write unit tests for
  the glue — write the integration test and stop.
- If a behaviour is fully expressed inside one pure function, do not promote it to
  an integration test to feel safer. You are paying ten to a hundred times the
  runtime for the same assertion.
- Do not assert the same behaviour at three levels. One change then breaks three
  tests, which teaches the team that tests are noise.

### What Not to Test

The tests you decline to write are as much a part of the strategy as the ones you
write, because every test is a permanent maintenance liability.

| Do not unit test | Why |
|---|---|
| Getters, setters, `__repr__`, dataclass constructors | No logic to be wrong |
| Framework behaviour — ORM `save`, router dispatch, DI resolution | You are testing the framework's test suite |
| Third-party libraries | Test your adapter over them, not them |
| Private helpers | Covered transitively; direct tests freeze internals |
| Pure wiring and config assembly | Verified by the app starting at all |
| Generated code, migrations | Assert the outcome, not the generator |

The sharpest signal is a test whose assertion restates the implementation:

```python
# ❌ Change-detector: fails when the code changes, never when it breaks
def test_build_url():
    assert build_url("users", 5) == f"{BASE}/users/5"     # same expression as the code
```

This test cannot fail for a reason a user would care about. Delete it. The
converse case — a test that would catch a real mistake — asserts an externally
meaningful fact instead:

```python
# ✅ Encodes the contract the caller depends on
def test_build_url_escapes_path_segments():
    assert build_url("users", "a/../b") == f"{BASE}/users/a%2F..%2Fb"
```

There is a bounded exception. Trivial code that has been wrong before — a
`__eq__` used as a dict key, a comparator, a `__hash__` — earns a test, because
history is evidence.

### Contract Testing at Service Boundaries

An integration test against a stub you wrote verifies your stub. It says nothing
about whether the provider still behaves that way. This is the largest blind spot
in a microservice test strategy, and it fails in production, at deploy time,
across a team boundary.

Consumer-driven contract testing closes it. The consumer's tests run against a
mock that *records* the interactions it relied on; that pact is published; the
provider replays every consumer's recorded expectations in its own CI.

```javascript
// consumer test: this is the shape we actually depend on
await provider.addInteraction({
  state: 'customer 42 exists',
  uponReceiving: 'a request for customer 42',
  withRequest: { method: 'GET', path: '/customers/42' },
  willRespondWith: {
    status: 200,
    body: like({ id: 42, tier: 'gold', creditLimit: 500 }),
  },
});
```

```bash
# provider CI: fail the build if any published consumer expectation breaks
pact-provider-verifier \
  --provider-base-url=http://localhost:8080 \
  --pact-broker-base-url=https://pacts.internal \
  --provider=customers-api
```

Two properties make this worth the setup cost. Neither team runs the other's
stack, so the check is cheap and fast. And the provider learns it is about to
break a consumer *before* deploying, which is the only moment the information is
actionable. Note that contract tests verify the interaction shape and semantics of
the boundary — they do not verify the provider's internal business logic, which
still needs its own tests.

Use the matching `can-i-deploy` gate so a deploy is blocked when a pact between
the versions being deployed has not been verified.

### Budgets and the Cost Ledger

Give each level an explicit budget, and enforce it, or the suite degrades by
accretion — nobody ever adds the test that makes it slow.

| Level | Per test | Tier total | Runs on |
|---|---|---|---|
| Static (types, lint) | — | < 60 s | Every save / commit |
| Unit | < 10 ms | < 60 s | Every commit |
| Integration | < 2 s | < 10 min | Every PR |
| Contract | < 5 s | < 3 min | Every PR, both sides |
| End-to-end | < 60 s | < 15 min | Pre-deploy only |

Cost per defect found rises steeply up the stack, and flakiness rises with it (see
`flaky-test-remediation` for why a 1% flake rate is fatal at scale). When the
budget is blown, cut end-to-end tests first, and keep only the journeys that would
cost real money if broken: sign-up, checkout, and whatever the business calls the
core loop. Five to fifteen such tests is a normal healthy number, not a
compromise.

Related skills carry the adjacent detail: `test-aaa-structure` for the internal
shape of a test, `test-coverage-categories` for enumerating cases within a level,
`test-mocking-rules` for where to place test doubles, `mutation-testing` for
whether your tests assert anything, `load-testing` for performance under
concurrency, `security-testing-strategies` for abuse cases, and
`quality-assurance` for the process wrapper.

## Common Anti-Patterns

❌ **Adopting a shape by fashion** — a pyramid on a thin mapping service produces
hundreds of tests that verify mocks.
✅ Derive the shape from where your production defects actually originate.

❌ **Inverted pyramid: end-to-end as the main safety net** — slow, flaky, and it
reports "checkout is broken" without saying where.
✅ Push each assertion to the narrowest level that can express it.

❌ **Testing the same behaviour at unit, integration, and E2E** — one change,
three broken tests, no extra signal.
✅ Assign each question to exactly one level.

❌ **Stubbing a service and calling it integration-tested** — you verified your own
stub's fidelity to a memory of the API.
✅ Contract tests, verified by the provider in the provider's CI.

❌ **Unit-testing getters, wiring, and framework calls to raise coverage** — pure
maintenance liability.
✅ Spend the effort on branch-dense domain logic.

❌ **Mock-heavy unit tests over integration-shaped code** — the test passes while
the real components disagree.
✅ Let those components meet in a real integration test.

❌ **No runtime budget** — the suite crosses the threshold where developers stop
running it locally, and quality falls off a cliff.
✅ Publish per-tier budgets and fail the build when they are exceeded.

❌ **Coverage percentage as the strategy** — measures execution, not verification.
✅ Coverage as a floor; mutation score and escaped-defect rate as the signal.

## Testing Strategy Checklist

- [ ] Last 20–30 production defects classified by where they originated
- [ ] Test distribution matches that classification, not a diagram
- [ ] Each level has a stated question it owns, with no duplicated assertions
- [ ] Explicit list of what is deliberately not unit tested
- [ ] Change-detector tests (assertion restates implementation) removed
- [ ] Contract tests exist for every consumed and provided service boundary
- [ ] Provider CI verifies published consumer pacts; deploy gated on verification
- [ ] Per-tier runtime budgets published and enforced in CI
- [ ] End-to-end limited to revenue-critical journeys, counted and named
- [ ] Unit tier runs with no network, no database, no clock dependence
- [ ] Escaped-defect rate tracked as the outcome metric, not coverage
- [ ] Strategy reviewed when the architecture changes, not annually
