---
name: testing-philosophy
description: "Use when proposing, writing, or reviewing automated tests, defines what a good test is: behavior over implementation details, and the Testing Trophy with a hard floor on end-to-end coverage for user-facing features. Generalized to any language and any layer (frontend, backend, CLI, library), not just JS/React. REQUIRED BACKGROUND for skills that plan or review tests, atdd-plan, implementation-review, tdd-writer, wrap-up. Use when the user asks whether tests are good, what to test, why a test is brittle, or whether e2e is needed."
---

# Testing philosophy

This is the shared definition of "good test" that every flagrare skill which proposes or reviews tests leans on. It distils Kent Dodds' testing writing and generalizes it past his JS/React context to any language and any layer. (Grounded in [`docs/research/2026-06-11-kent-dodds-testing-philosophy.md`](../../../../docs/research/2026-06-11-kent-dodds-testing-philosophy.md).)

## The one principle

> **The more your tests resemble the way your software is used, the more confidence they can give you.** (Kent C. Dodds)

Every rule below is a corollary. The principle is already language- and layer-agnostic; "the way your software is used" just resolves to a different surface in each context. When a testing decision is unclear, return to this sentence.

## Pillar 1: Behavior over implementation details

An **implementation detail** is anything *"users of your code will not typically use, see, or even know about."* A test bound to one fails in both directions at once:

- **False negative on refactor**: you change internals without changing behavior, and the test breaks anyway. It cries wolf.
- **False positive on breakage**: you break the actual behavior, and the test stays green because it was watching the mechanism, not the result.

Dodds' framing: a test that drives your code differently from how real users drive it becomes *a third user you never wanted*, now you have to keep the end user, the calling developer, **and** the test happy.

**"User" generalizes by layer.** Assert only on what *that* user can observe; drive the code only through the surface *that* user touches:

| Layer | The user | Assert on (observable) | Do NOT touch (implementation) |
|---|---|---|---|
| Library / module | the calling developer | return values, thrown errors, public types, emitted events | private fields/methods, internal helpers, internal data-structure choices |
| Backend / API | the HTTP/RPC client | status codes, response bodies, headers, state visible *through* the API, domain events | ORM internals, service method names, query shapes, internal DTOs |
| Frontend / UI | the person clicking | rendered text, roles, what appears/disappears after an interaction | component state vars, hook internals, CSS class names, child-component names |
| CLI | the person at the prompt | stdout/stderr, exit code, files written | internal flag parsing, function call order |

**Concrete tells of an implementation-detail test** (stack-independent, flag any of these):

- Asserts on private fields, unexported functions, internal state, or internal data-structure shape.
- Asserts a particular internal function/method *was called*, spy / mock-call-count assertions on a collaborator **you own**.
- Mocks a collaborator you own, rather than mocking only at a true external boundary (network, disk, clock, OS process, third-party service).
- Its name describes a mechanism (`calls setIndex with 0`) instead of a behavior (`shows the first slide on load`).

**The acid test:** *"If I refactor the internals but keep the public contract identical, does this test break?"* If yes, it tests the wrong thing. Pair it with: *"Does this assert what a real user observes?"* If no, same problem.

## Pillar 2: The Testing Trophy, and the e2e floor

Four layers, bottom to top. Height is **confidence**; height is also **cost/time**. Testing is "return on investment where return is confidence and investment is time."

| Layer | What it is | Mock how much |
|---|---|---|
| **Static** | types + lint, correctness for free | n/a |
| **Unit** | one piece in isolation | dependencies mocked |
| **Integration** | several units working together, **the default tier** | mock only external boundaries |
| **E2E** | the whole assembled system | "as little as possible" |

"Write tests. Not too many. **Mostly integration**" puts most effort in the middle, because that's the best confidence-per-effort and most regressions live *between* units, not inside them.

**The correction that matters: "mostly integration" is not "skip e2e."** There are two opposite violations, and most reviews only catch the first:

1. **Too much e2e**: every scenario duplicated as a slow, flaky full-stack test that could be an integration test. Flag it; push it down the trophy.
2. **No e2e at all for the critical path**: every layer tested in isolation, but nothing proves they connect. This is the quieter, more common gap. Flag it just as hard.

**The e2e necessity rule:** *every user-facing feature needs at least one end-to-end (or highest-practical) test that exercises its critical happy path through the real, assembled system*, one or two paths, not one per scenario. The e2e tier proves the wiring; integration proves the behavior; unit proves the tricky pure logic; static proves the shapes. A plan or a diff that has unit + integration coverage but no wiring proof for a user-facing feature **has a gap**.

**E2e does not require a browser**: it generalizes:

| Surface | What "e2e" means |
|---|---|
| Frontend app | browser-driven test of the critical journey: load → act → see the result |
| Backend service | hit the running service over HTTP against a real (test) DB; assert response + persisted state |
| CLI | invoke the built binary as a subprocess; assert stdout / exit code / files written |
| Library | consume the published public API exactly as a downstream user would, nothing internal stubbed |

## How skills use this

**When proposing tests** (planning, ATDD): write tests behavior-first against the public surface; default to integration; reserve unit tests for pure functions with tricky logic; and **include at least one e2e/full-stack happy-path test for any user-facing feature.** Never aim at a coverage number, coverage is a side effect of testing the right behaviors.

**When reviewing tests:** run both acid-test questions on every test; flag the implementation-detail tells above; and check **both** e2e directions, overuse *and* the missing-critical-path gap.

## Anti-patterns

- Treating "mostly integration" as license to ship a user-facing feature with zero e2e coverage.
- Asserting on mock call counts / spies for collaborators you own, then calling it a behavior test.
- Test names that describe the mechanism (`calls X`) rather than the outcome the user observes.
- Snapshot tests that get rubber-stamped on update, they assert "it changed," not "it's correct."
- Chasing a coverage percentage instead of covering the behaviors that matter.
- Assuming e2e means Selenium/Cypress, for a backend or CLI the e2e is a subprocess/HTTP test, and skipping it "because there's no UI" is the gap, not an excuse.

## Source

Kent C. Dodds: [Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details), [The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications), [Write tests. Not too many. Mostly integration.](https://kentcdodds.com/blog/write-tests). Generalization and per-layer mapping captured in [`docs/research/2026-06-11-kent-dodds-testing-philosophy.md`](../../../../docs/research/2026-06-11-kent-dodds-testing-philosophy.md).
