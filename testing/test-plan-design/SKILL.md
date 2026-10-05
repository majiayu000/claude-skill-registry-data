---
name: test-plan-design
description: How to design a test plan — scope and risk-based prioritization, the test pyramid, case-design techniques (equivalence partitioning, boundary values, decision tables), entry/exit criteria, coverage and requirement traceability, test data and environments. Deep reference with a runnable coverage-gap check.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Test Plan Design

A test plan is a **budget**: finite effort spent where it prevents the most expensive failures. The goal
is never "test everything" — that is impossible and economically illiterate. The goal is to make a
defensible decision about *what* to test, *at which layer*, *with which cases*, and *when you are done*.
This skill is the deep reference for that decision. Heavy detail lives in `references/`; copy-paste
material in `examples/`; a runnable traceability check in `scripts/`.

## Mental model

You are allocating scarce attention across a feature. Four questions drive every plan:

| Question | Answer comes from |
|---|---|
| What matters most? | risk = impact × likelihood (scope & prioritization) |
| At which layer do I test it? | the test pyramid (unit / integration / E2E) |
| Which concrete cases? | case-design techniques (partitions, boundaries, decision tables) |
| When am I done? | exit criteria + coverage traced to requirements |

Skip any one of these and the plan degrades: no risk ranking and you over-test trivia; no case design and
you write five tests that all exercise the same path; no traceability and you ship a requirement nobody
verified.

## 1. Scope and risk-based prioritization

Start by listing what the feature must do, then rank each item by **risk = impact × likelihood**.

- **Impact**: what does failure cost? Money movement, data loss, security, and legal/compliance are
  top-tier; cosmetic glitches are bottom-tier.
- **Likelihood**: how probable is a defect? New code, complex logic, many integrations, and unclear
  requirements raise it; stable, simple, well-understood code lowers it.

Spend the most rigor at the top of the ranked list and explicitly decide to *under*-test the bottom.
Writing down "we are not testing X because it is low-risk" is a feature of a good plan, not a gap. The
full scoring rubric and a worked heat-map live in [references/risk-prioritization.md](references/risk-prioritization.md).

## 2. The test pyramid — choosing a layer

Each behavior should be tested at the **lowest layer that can meaningfully verify it**. Lower layers are
faster, cheaper, and more precise about *where* a defect is.

```
        /\        E2E        few   — full user journeys, real-ish stack, slow & flaky
       /  \       Integration some — module + its collaborators (DB, gateway, queue)
      /____\      Unit         many — one function/class, no I/O, milliseconds
```

- **Unit**: pure logic — pricing math, validation, state machines. No network, no DB. Run in ms.
- **Integration**: a module talking to a real (or faithfully faked) collaborator — a repository hitting a
  test DB, a client calling a mocked gateway with success/decline/timeout responses.
- **E2E**: a thin layer covering only critical journeys end to end (e.g. "add to cart → pay → confirm").

The classic anti-pattern is the **inverted pyramid** (an "ice-cream cone"): many slow E2E tests and few
units. It is slow, flaky, and tells you *that* something broke but not *where*. Layer-selection heuristics
and the integration/contract-test distinction are in [references/test-pyramid.md](references/test-pyramid.md).

## 3. Case-design techniques

For each unit under test, do not invent cases ad hoc — derive them. Three techniques cover the vast
majority of input-space reasoning:

- **Equivalence partitioning**: split the input domain into classes that should behave identically, then
  test *one* representative per class. If ages 18–65 are all "standard", you need one value from that
  band, not forty.
- **Boundary value analysis**: bugs cluster at edges. For a valid range `[18, 65]`, test `17, 18, 19` and
  `64, 65, 66` — just-below, on, and just-above each boundary. Off-by-one errors live here.
- **Decision tables**: when output depends on a combination of conditions, enumerate the combinations so
  no rule is missed.

```text
Discount rules (decision table)
Member? | Cart ≥ $100 | Coupon valid | → Discount
  no    |    no       |    no         |   0%
  no    |    yes      |    no         |   5%
  yes   |    no       |    no         |  10%
  yes   |    yes      |    yes        |  25%   ← interaction case, easy to miss
```

A worked example combining all three on one function is in [references/case-design.md](references/case-design.md),
and a ready-to-fill case template is in `examples/test-case-template.md`.

## 4. Entry and exit criteria

Make "ready to test" and "ready to ship" explicit so the plan ends on data, not vibes.

- **Entry criteria** (can we start?): code merged to the test branch, build green, test environment and
  seed data available, dependencies/stubs deployed.
- **Exit criteria** (can we stop?): all planned cases executed; all CRITICAL/HIGH-risk requirements have a
  passing test; coverage target met (e.g. 80% line on changed code); zero open Sev-1/Sev-2 defects; known
  issues triaged and accepted by the owner.

Exit criteria are the contract that prevents both premature shipping and endless gold-plating.

## 5. Coverage and traceability to requirements

Coverage has two distinct meanings — track both:

1. **Code coverage** (line/branch): a *necessary* signal, not a *sufficient* one. 100% line coverage with
   zero assertions proves nothing.
2. **Requirement coverage**: every requirement maps to at least one test that verifies it. This is the one
   that catches "we built it but nobody tested it."

Maintain a traceability matrix (requirement ↔ test case). The runnable check
`scripts/coverage-gaps.mjs` takes your requirements and test cases as JSON and lists any requirement with
**no** covering test — run it in CI so an untested requirement fails the build. See
`examples/test-plan.md` for a filled matrix.

## 6. Test data and environments

- **Data**: prefer small, purpose-built fixtures over a copy of production. Cover the equivalence classes
  and boundaries from §3. Never use real PII in test data — synthesize it. Make data setup deterministic
  and self-cleaning so tests are independent and order-free.
- **Environments**: keep a dedicated, reproducible test environment (containers/IaC) so "works on my
  machine" is not a defense. Pin external dependencies via fakes/contract tests; do not let a flaky
  third-party sandbox gate your pipeline.

## Common pitfalls (failure modes)

- **Testing everything equally** — no risk ranking, so trivial getters get the same attention as the
  payment path. Rank first.
- **Inverted pyramid** — leaning on slow, flaky E2E for logic that a unit test would pin precisely.
- **Coverage theater** — chasing a line-coverage number with assertion-free tests; green bar, no safety.
- **Redundant cases** — five tests in the same equivalence class, zero at the boundary where the bug is.
- **No traceability** — a requirement ships with no test because nothing connected the two.
- **Non-deterministic data/time** — tests depend on "today" or shared mutable rows and fail intermittently.
- **Vague exit criteria** — "looks good" instead of measurable gates, so testing ends by exhaustion.

## When NOT to use / trade-offs

A heavyweight, document-driven test plan is overkill for a one-line bug fix or a throwaway spike — there,
a couple of targeted tests and a green CI run are the proportionate response. Formal test plans earn their
cost on high-risk, multi-team, regulated, or long-lived features. Likewise, exhaustive case enumeration is
wasteful on low-risk surfaces; reserve decision tables and full boundary analysis for logic where a defect
is expensive. The plan should be *proportional to risk* — a plan that costs more than the failures it
prevents is itself a failure. For ongoing change to an existing suite (what to re-run after a change, how
to fight flakiness over time), that is a different discipline — see the pairing below.

## Files in this package

- `references/risk-prioritization.md` — risk scoring rubric, impact/likelihood matrix, worked heat-map
- `references/test-pyramid.md` — layer-selection heuristics, integration vs contract tests, anti-patterns
- `references/case-design.md` — equivalence partitioning, boundary analysis, decision tables, worked example
- `examples/test-plan.md` — a complete, filled-in test plan with a traceability matrix
- `examples/test-case-template.md` — a reusable single-test-case template
- `scripts/coverage-gaps.mjs` — runnable check: lists requirements with no covering test (`--selftest`)

Pairs with the `qa-strategist` agent, the `test-author` agent, and the `regression-strategy` skill.
