---
name: tdd
description: Use test-driven development to build behavior or fix bugs test-first, at agreed public seams, with independent expectations, deterministic boundaries, and a red-green-refactor loop.
---

# Test-driven development

Use this skill when building a feature or fixing a bug test-first. Work in small vertical
slices: define one observable behavior, make one test red, implement the minimum that makes it
green, and refactor after Green without changing the behavior. The skill applies to unit,
integration, and end-to-end tests; choose the seam and test environment that make the behavior
real.

Before writing a test, read `CONTEXT.md` when it exists and respect the ADRs for the area. Agree
the public seam with the developer or user, or use the seam that the task already names.

## One behavior at an observable seam

A seam is the public boundary at which a caller can observe behavior. Test at the highest useful
agreed seam. Use the real internal components and value objects that participate in that behavior,
and observe the result only through the seam, so private state, private methods, and
implementation-only side channels stay hidden.

One test proves one behavior, not one assertion. A retry, transaction, workflow, or state
transition may need several actions and several assertions. Keep those steps in one test when
they describe one behavior. Separate the Arrange, Act, and Assert sections, and meaningful steps,
with blank lines so the behavior is easy to read.

Name tests with a behavior phrase that says what the caller can observe, not how the code is
implemented. Name the system under test `sut` when the local convention does not provide a clearer
name. Keep the test independent: it creates the state and data that it needs and passes in any
order.

## Red → Green → Refactor

Choose one next test from the behavior still missing, and write it after learning from the
current implementation.

1. **Red:** write the smallest test at the agreed seam. Derive its expectation independently and
   run the focused test so it fails for the intended missing behavior.
2. **Green:** make the smallest production change that satisfies the test. Do not add speculative
   behavior, remove assertions, skip the test, or weaken the expected result to obtain Green.
3. **Refactor:** after Green, improve the production or test design without changing behavior.
   Rerun the focused test and the relevant project checks after the refactor.

## Optional test-author subagent

The developer delegates the next Red test to the installed Claude Code `test-author` subagent
only after running `.claude/hooks/test-author-preflight.sh`. The preflight must return exactly
`{"status":"ok"}`. Any `disabled` result keeps the ordinary developer route; pass its sanitized
`reason` to the developer and do not spawn an unprotected test-author.

When preflight is `ok`, call the subagent before each implementation step. Give it one behavior
requirement, one scenario, the agreed public seam, the public signatures and the existing fixtures;
never give a proposed algorithm or implementation snippet as the basis of an expectation. The
subagent may write only one test in `test_paths` and may run only that test through
`.claude/hooks/run-test.sh <test-id>`. It replies in compact English with `status` (`red`,
`needs_skeleton` or `contract_gap`), the requirement, inputs, independent expectation source, test
id and, for `red`, sanitized Red evidence: the runner JSON plus the failed assertion, expectation
and actual result from the run's `log.txt`. It must not write production code or a skeleton and it
does not receive an orchestration manifest, dispatch, brief/report, approval, or ledger lifecycle.

Check the expectation against the requirement before you implement, and never weaken an accepted
expectation to reach Green; a justified contract change needs a new call and a new check. For
`needs_skeleton`, write only types and signatures without logic, then rerun the subagent. A compile,
import, fixture or environment error is not Red, and a test that is green at once does not count as
a cycle. After three consecutive failed calls on one test, stop and report a blocker. The full
protocol is in `developer.md` of the orchestration roles. The `/fast-implement` short route runs
the same protocol in one session; there the seam is the one the developer agreed before the first
test, instead of one taken from an architect brief, and an unavailable author keeps the ordinary
route with the reason stated.

For a bug fix, begin with a minimal reproducer at the seam where the bug is observable. Keep the
expectation that describes the bug. Weakening it for Green only hides the regression and leaves no
evidence that the fix is correct.

## Independent expectations

Expected values must come from a source independent of the implementation under test:

- Prefer short, known-good literals in examples.
- Use reference fixtures, documented examples, properties, or an independently sourced oracle
  when a literal is not practical.
- Use parameterization for input variants. Do not choose the expected result with an `if`, `match`,
  conditional expression, or lookup that repeats production branching inside the test.
- Do not repeat the production algorithm in an assertion or recompute the expected value by the
  same steps as the implementation.

Multiple assertions are valid when they describe different observable parts of the same behavior.
They are not a reason to split a necessary multi-step scenario into tests that no longer prove the
behavior together.

## Collaborators and unmanaged boundaries

Substitute only external unmanaged dependencies. Your own modules, internal classes, value
objects, and concrete classes stay real in the test.

At an external unmanaged boundary, distinguish commands from queries:

- A command asks the boundary to cause an effect. Test the sending contract and its observable
  effect, such as the message, request, or persisted result that the boundary receives.
- A query supplies information. Stub the response needed by the scenario. Usually do not assert
  internal call counts, call order, or the number of queries.

Keep a query stub to the fixed response that the scenario needs, and assert the public behavior
that the contract describes.

## Time, randomness, and determinism

Deterministic substitutes for time and randomness are permitted. Give domain logic explicit time
and boundary code an injectable clock or random source. Inject those substitutes through the
existing boundary and keep the public production API unchanged. Each test fixes its time,
timezone, and random source and waits on observable events instead of elapsed time, so its result
is the same on every run and in any order.

Add flaky-test policies, seed policies, property-based testing, or mutation-testing
infrastructure only when the project already requires them.

## Database and integration isolation

Test SQL, transactions, indexes, and constraints against the production database engine in an
isolated test environment. Do not replace that engine with a different in-memory engine: dialect,
transaction, locking, and constraint behavior are part of the contract. Keep the isolated
database disposable and independent for each test or test group according to the project's safe
fixture policy.

Test pure domain logic without a database. A domain test runs without persistence even when the
production adapter uses it.

## Choosing cases

Use the following order as a heuristic, not a coverage mandate:

1. no-op or empty input;
2. the typical successful case;
3. meaningful boundaries and failures;
4. invariants that must hold across the behavior.

Choose the cases that explain the contract and protect valuable behavior. Coverage is a signal,
not the goal of this skill.

## Examples

Open [examples.md](examples.md) when a test needs a worked pattern: parameterized literals, a
multi-step behavior with several assertions, a reference fixture, an independent oracle, a
boundary with a query stub, a command effect, and a fixed clock, or a deterministic random source.

## Review checklist

Before handing off a slice, confirm each item:

- The test observes one behavior through an agreed public seam with real internal components and
  value objects.
- The name is a behavior phrase, `sut` is clear, and blank lines separate Arrange, Act, Assert, and
  meaningful steps.
- Several steps or assertions, when present, describe that same behavior.
- The expectation comes from a literal, a reference fixture with a recorded origin, a property, or
  an independent oracle; variants use parameterization.
- An external command is checked through the contract it sends; an external query returns a stubbed
  response.
- Time comes from a fixed clock and randomness from a deterministic random source, both injected at
  a boundary.
- Database behavior runs on the production engine in an isolated environment; pure domain tests run
  without a database.
- The test was red for the intended reason, Green came from a minimal change with the expectation
  intact, and Refactor followed Green.
- Each case protects contract behavior rather than a coverage number, and test tooling follows the
  project's existing policy.
