---
name: test-driven-development
description: Drives production code from failing tests. Writes the smallest test that asserts one behaviour, watches it fail for the expected reason, writes the minimum code to pass, then refactors with the suite holding the result still. Picks the right scope (unit, integration, contract, end-to-end), names tests as specifications, and uses fakes, stubs, mocks, and spies for the reason each exists. Audits suites for assertion-free tests, tests that mirror implementation, shared fixtures, ordering dependencies, flakiness, and coverage that measures lines instead of behaviour. Triggers on "tdd", "test-driven development", "red green refactor", "test first", "failing test", "write a test", "unit test", "integration test", "contract test", "e2e test", "test pyramid", "test double", "mock", "stub", "fake", "spy", "arrange act assert", "given when then", "test naming", "flaky test", "test smell", "characterisation test", "snapshot test", "property-based test", "mutation testing", "coverage".
---

# Test-Driven Development

Production code exists because a failing test asked for it. Every change passes through Red → Green → Refactor in that order, and the loop is small enough that the next failure is never more than a few minutes away.

The discipline has two layers. **Cycle** is the per-behaviour loop: one test, one reason it fails, the smallest code that turns it green, then refactor. **Suite** is the standing test asset: what each test proves, what it costs to run, what it costs to maintain, what it lets the team change without fear.

## Mode Router

Pick one mode per invocation. If the request spans modes, sequence them.

| Mode | Use when | Output |
|------|----------|--------|
| **Cycle** | A new behaviour is being added or changed | One failing test, the minimum implementation that passes it, the refactor that cleans the result, with each step shown separately |
| **Plan** | A feature or change touches several behaviours | Ordered list of behaviours, the test scope for each, the order they will be driven, and the seams that need to exist before the first test can be written |
| **Recover** | Production code exists without tests and must change | Characterisation tests that pin current behaviour, then the cycle resumes from a known-green baseline |
| **Audit** | An existing suite is slow, brittle, or untrusted | Tiered findings (Blocker / High / Medium) citing the smell each test exhibits and the smallest change that fixes it |

## The cycle

One behaviour at a time. Do not start a second test while a first is red. Do not skip refactor because the test is green.

### 1. Red — write a test that fails for the reason you expect

State the behaviour in one sentence before writing the test. If the sentence needs an "and", split into two tests.

- Name the test as a specification: `<subject>_<expected behaviour>_<condition>`. The name reads as a sentence a stakeholder would recognise.
- Arrange the smallest setup that triggers the behaviour. Reuse only fixtures whose purpose the reader can guess from their name.
- Assert one observable outcome — a return value, a thrown error, a state change, an event emitted, a call made across a boundary. Multiple assertions are acceptable only when they describe one behaviour from different angles.
- Run the test. Confirm it fails, and confirm the failure message names the missing behaviour. A test that fails because of a typo, import error, or unrelated null is not yet red — fix the test until the failure points at the work to be done.

A test that passes on the first run is not red. Delete it or change its assertion until it fails — otherwise the implementation may already exist, or the test asserts nothing, and neither will be discovered until later.

### 2. Green — write the minimum code that turns the test green

The bar is "smallest legal change that makes this one test pass". Future tests will demand more; let them.

- Return the literal the test expects, if that passes. The next test will force generalisation.
- Hardcode now, generalise on the next red. Two passing tests with the same hardcoded answer is the cue to extract the rule.
- Do not add error handling, validation, logging, or branches that no current test exercises.
- Do not edit unrelated code. Note the urge; address it in the refactor step or in its own cycle.
- Run the full local suite, not only the new test. A green new test plus a red old test is a regression, not progress.

### 3. Refactor — improve the code with the suite holding it still

Refactor is mandatory, not optional. The window where the design is fresh and the tests are green is the cheapest time to improve it.

- Move in small, behaviour-preserving steps. Run the tests after each step.
- Rename anything the cycle just exposed as poorly named — variables, helpers, test names, file names.
- Remove duplication that appeared between the production code and the test, between two tests, or between two pieces of production code.
- Stop refactoring when the next change would alter behaviour. Behaviour changes belong in the next red.

If the tests turn red during refactor, the refactor changed behaviour. Revert to green and take a smaller step.

## Test scope

Pick the scope that proves the behaviour under change without dragging in concerns the change does not own. Wrong scope is the largest source of slow, flaky, or coupled tests.

| Scope | Proves | Boundaries | When to reach for it |
|-------|--------|------------|----------------------|
| **Unit** | One function, class, or module behaves correctly in isolation | Real collaborators inside the unit; test doubles for everything that crosses a process, network, disk, clock, or randomness boundary | The behaviour is a decision, calculation, transformation, or state transition |
| **Integration** | Two or more real components agree on a contract — typically code plus a real dependency such as a database, message bus, cache, or filesystem | Real dependency, ideally in a container or local instance; no test doubles for the dependency under test | The behaviour depends on the dependency's actual semantics (SQL constraints, transaction isolation, queue ordering, file locking) |
| **Contract** | Two services agree on a wire format and protocol without running both at once | Provider verifies a recorded expectation produced by the consumer | Crosses a process boundary owned by another team, deploy, or repository |
| **End-to-end** | A complete user journey works against a fully wired stack | No test doubles; production-shaped environment | Smoke-level confidence that the assembled system runs at all; never as the default place to drive behaviour |

Default to the smallest scope that can fail for the reason you are testing. If a unit test cannot fail when the behaviour breaks, the seam is missing — extract one before widening the scope.

### The pyramid

Many fast unit tests, fewer integration tests, very few end-to-end tests. Inversions of this shape (an ice-cream cone: many slow end-to-end tests, few units) are the standing signal that seams are missing and that the suite will become too slow to run on every change.

### What these scopes mean in a component library

There is no database, message bus, or wire format here, so the table above maps
onto different things. The whole suite is Vitest + jsdom and runs in ~40s; the
axis that matters is **how much of the component tree a test mounts**, not how
much infrastructure it starts.

| Generic scope | Here | Suffix |
|---|---|---|
| Unit | A pure helper or hook — `calendarUtils`, `timePickerUtils`, `usePagination`, a `.styles.ts` class map | `.test.ts`, `.styles.test.ts` |
| Unit (rendered) | One component mounted alone, asserted through its accessible output | `.test.tsx` |
| Contract | The prop → rendered-class mapping is exhaustive and stable — the library's real "wire format", since consumers depend on it | `.contract.test.ts` |
| Integration | Several components composed, or a compound component with its context | `.integration.test.tsx` |
| End-to-end | Not applicable. The consuming application owns that. Stories with `play()` are the closest thing — and they now gate as well as document, since the `storybook` Vitest project runs them in a real browser. A story you write is a test you own. | `.stories.tsx` |

Two scopes have no generic counterpart and are worth reaching for deliberately:

- **`.boundary.test.tsx`** — empty, null, extreme, and conflicting props. In a library these are not edge cases; they are what consumers will actually pass, because you cannot see their call sites.
- **`.mutation.test.tsx`** — an assertion aimed at a specific subtle change that would otherwise slip through (an inverted comparison, a dropped `!`). Write one when a bug was subtle enough that the existing tests stayed green.

The bar for a published component is higher than for application code: **you
cannot grep for the call sites.** A behaviour that is not pinned by a test is a
behaviour a consumer may already depend on and you may break without noticing.

## Naming and structure

A test is a specification of intent. A reader who has never seen the production code must be able to predict what the code does from the test name alone.

- **Subject_behaviour_condition.** `transfer_rejects_negative_amount`, `cache_evicts_least_recently_used_entry_when_full`, `parser_returns_none_on_unterminated_string`. Drop pronouns; lead with the subject.
  - **In this repo the convention is `it('should …')`** — `it('should focus the next item on ArrowDown')`. ~4.2k tests follow it; match it rather than introducing snake_case names. The underlying rule is the same: the name states the behaviour and its condition.
- **One behaviour per test.** A test that asserts "creates the user *and* sends the welcome email *and* logs an event" hides three failure modes behind one red bar. Split.
- **Arrange / Act / Assert** (or **Given / When / Then**) — visible in the structure of the test, not necessarily in comments. Blank lines between the three are usually enough.
- **No conditionals in tests.** No `if`, no `for`, no `try` around the act. A branch in a test means the test is two tests fused together; split them. A loop means parameterise.
- **Parameterise repetition; do not abstract intent.** Table-driven tests for "same behaviour across many inputs" are good. Helper functions that hide which assertion will fire are bad — when the test fails, the reader must be able to see the cause without stepping into a helper.

A failing test should print enough to diagnose the failure from the message alone. Custom assertion messages, structured equality diffs, and named-fixture identifiers are cheap; debugger sessions are not.

## Test doubles — by purpose

Each kind of double exists for a different reason. Choosing by name ("I'll mock it") instead of by purpose is the largest cause of brittle suites.

| Double | Replaces | Use when | Asserts |
|--------|----------|----------|---------|
| **Dummy** | A collaborator that must exist for the signature but is never used | The argument is required but irrelevant to the behaviour | Nothing |
| **Stub** | Inbound queries — returns canned answers | The unit under test needs an answer from a collaborator, and the answer is the input being varied | Nothing about the collaborator; only the outcome the unit produces |
| **Fake** | A real-but-simpler implementation | The collaborator is expensive (database, network), but the unit depends on its semantics, not just its return value | The outcome the unit produces, against the fake's state |
| **Spy** | Outbound commands — records calls for later inspection | The unit's job is to *cause* a side effect at a boundary, and the test must prove the side effect happened | That the call happened, with the right arguments, the right number of times |
| **Mock** | Outbound commands — pre-programmed with expectations that fail the test if unmet | The interaction is the specification, and absence of the call is a defect | The interaction itself, declared up front |

Rules that hold across all of them:

1. **Double the role, not the type.** A `Clock` is a role; `java.time.Clock` is a type. Tests that double types break when the type changes; tests that double roles survive.
2. **Do not double types you do not own.** Wrap third-party libraries behind a small interface, double the interface. Doubling a foreign library couples the test to the library's internals and rots whenever the library upgrades.
3. **Verify behaviour at one boundary per test.** A test that stubs three collaborators and spies on a fourth is testing four things at once.
4. **Stubs answer; spies record; mocks demand.** If the test does not need to assert the interaction, do not use a mock — a stub is enough.
5. **Prefer fakes over mocks for stateful collaborators.** A fake repository that holds a dictionary is honest about state. A mock repository pretending to be stateful through programmed responses is a maintenance bill.

If a unit needs more than two test doubles to be tested, the unit is doing too much. Decompose it.

## When code is hard to test

Hard-to-test code is design feedback, not a testing problem. The fix is almost always in the production code.

| Symptom | Underlying defect | Move |
|---------|-------------------|------|
| Cannot construct the unit without spinning up a database, a server, or a framework | The unit conflates a decision with its delivery mechanism | Extract the decision into a pure function or class that takes its dependencies as parameters |
| The test must use reflection or monkey-patching to inject a dependency | The dependency is hidden inside the constructor or imported as a module-level global | Inject the dependency through the public constructor or method signature |
| The same setup repeats across many tests in a long, opaque block | The unit demands a wide context to do anything | Narrow the unit's contract or introduce a builder that names the context |
| Tests pass in isolation and fail in a suite, or vice versa | Shared mutable state — module globals, singletons, a test database not reset between cases | Make the state explicit; reset it between tests; or eliminate it |
| The test asserts that a private method was called | The test is reaching past the public contract to verify implementation | Assert on the observable outcome; if no outcome is observable, the behaviour is unobservable and should not exist |
| Adding a small feature breaks many tests in unrelated files | Tests over-specify the implementation, or one production seam carries too many responsibilities | Tighten the test's scope, or split the seam |

A test forced to know the production code's structure is a test that will break the next time the structure changes — even if the behaviour does not.

## Recovering an untested codebase

When code exists without tests and must change, do not begin with the change. Begin with a characterisation step.

1. **Pin current behaviour.** Write tests that assert what the code does today, including any quirks. Use approval or golden-output tests if the output is large and not obviously specifiable. These tests do not prove the behaviour is correct — they prove it does not change accidentally.
2. **Find the seam.** Identify the smallest place that can be replaced with a test double without rewriting the surrounding code. Common seams: a method, a constructor parameter, a module-level import, a subclass override.
3. **Move to a green baseline.** Run the characterisation tests. They must all pass before any production change.
4. **Resume the cycle.** From green, write the next failing test for the new or changed behaviour and proceed normally.
5. **Replace characterisation tests when superseded.** Once a piece of behaviour is covered by a proper specification-style test, the characterisation test is dead weight. Delete it.

Characterisation tests are scaffolding. They exist to let the cycle resume, not to live forever.

## Suite health

A test suite is a long-lived asset. It must be fast enough to run on every change, deterministic enough to trust, and clear enough to change without fear.

### Speed

- Unit suites should complete in seconds, not minutes. A unit test that takes more than tens of milliseconds is doing integration work in disguise.
- Integration suites should be parallelisable. Tests that share state cannot be parallelised; that is a defect, not a property.
- Profile periodically. A handful of slow tests dominate total runtime; finding and fixing them is a high-leverage activity.

### Determinism

A flaky test is not a flaky test — it is a real bug, in either the code or the test. The cost of treating flakes as noise is that real bugs hide inside the noise.

Common causes:

- Dependence on time, randomness, network latency, file-system ordering, or thread interleaving without controlled injection.
- Shared mutable state between tests — module globals, class attributes set in earlier tests, fixtures with side effects.
- Implicit ordering assumptions — test A passes only because test B ran first.
- Race conditions in the code, surfaced only under load.

Fix or quarantine — never ignore. Quarantined tests get an issue, an owner, and a deadline.

### Coverage

Line and branch coverage measure what was executed, not what was specified. A unit can have 100% line coverage and zero assertions — the suite proves only that the code runs without crashing.

- Use coverage to find untested code, not to certify tested code. A coverage gap is a question worth asking; a high coverage number is not an answer.
- Mutation testing is the harder, truer measure: small edits to the production code that should fail a test and don't reveal tests that execute code without specifying its behaviour. Run it periodically on important modules.

### Maintenance

- A test that fails when behaviour changes is paying its rent.
- A test that fails when implementation changes but behaviour does not is a liability. Tighten its assertions to the observable outcome or delete it.
- A test that no one knows how to read is a test no one will fix when it breaks. Rename it, restructure it, or delete it.

## Audit signals

| Signal | Defect | Move |
|--------|--------|------|
| Test name describes the implementation (`uses_cache_when_present`) | Specification of mechanism, not behaviour | Rename to the observable outcome (`returns_cached_value_within_ttl`) |
| Test asserts on a private method's call | Reaching past the public contract | Assert on the public outcome; if none exists, the private method's behaviour is unobservable and the test is invalid |
| Test passes when assertions are commented out | Assertion-free test, or assertions inside an unreached branch | Make the assertion the last line of the act; add one assertion the test cannot reach without the behaviour |
| `if`, `for`, `try` inside the test body | Two tests fused, or implicit specification | Split into separate tests or a parameterised table |
| Many tests share a long `setUp` / `beforeEach` | Wide implicit context, hidden coupling between tests | Inline the setup each test actually needs; reuse only named, intention-revealing builders |
| Test mutates a module-level global | Shared mutable state — order-dependent suite | Inject the state through the constructor or function signature; reset between tests |
| Tests fail under `--shuffle` or parallel run | Hidden ordering dependency | Find and remove the shared state; do not retry the test until it passes |
| One test fails three production files | One test verifies many behaviours, or the unit owns many responsibilities | Split the test; split the unit if needed |
| `@retry`, `@flaky`, `sleep` in tests | Race or timing bug being papered over | Inject the clock or the synchronisation primitive; assert on the event, not on the wall-clock wait |
| Mock returns are programmed across five layers of collaborators | Unit under test orchestrates too much | Push behaviour into the collaborators or into a single coordinator; test the coordinator with fakes |
| Snapshot/approval tests grow without review | Tests now accept whatever the code emits | Treat the snapshot as a specification: review it on every change, or replace with assertion-style tests |

## Anti-patterns

- **Writing the implementation first, then the test.** The test reflects what the code happens to do, not what was specified. Bugs in the implementation become bugs in the test.
- **Skipping refactor because the test is green.** The smell that prompted the cycle remains; the next cycle starts from a worse position. Refactor is the deliverable, not the bonus.
- **Catching all exceptions in tests.** `try ... pass` around the act hides the fact that the wrong exception type is thrown. Assert the specific exception.
- **`assert True` or `expect(x).toBeDefined()` as the sole assertion.** The test passes whenever the code does not crash. Assert the value.
- **Hidden helpers that perform the assertion.** A helper named `do_the_thing(case)` that internally asserts something the reader cannot see. When the test fails, the message points at the helper, not the behaviour. Inline or rename.
- **Snapshot tests as a substitute for specification.** A snapshot freezes output without saying why it is the right output. Useful for large structural payloads; harmful as the default place to assert behaviour.
- **Test inheritance hierarchies.** A base test class whose subclasses run inherited tests is a near-guaranteed source of ordering bugs and obscure failures. Prefer composition: shared builders and helpers, not shared test cases.
- **One-test-per-method.** Tests organised around production methods, not behaviours. Refactoring the method renames or deletes the test even when behaviour is unchanged. Organise around behaviours.
- **Coupled fixtures.** Test A relies on fixture data created by test B's setup. Move shared fixtures to explicit factories that produce minimal, named state per test.
- **Mocking what you don't own.** Doubling a third-party type directly. The double rots when the library upgrades. Wrap the library in a thin interface and double the interface.
- **Testing through the UI by default.** End-to-end tests for behaviour that can be specified at a lower layer. Drives slow, flaky suites and inverts the pyramid.
- **Coverage as a target.** Teams write tests that hit lines without asserting outcomes. Coverage rises, defects do not fall. Use coverage to ask questions, not to score work.
