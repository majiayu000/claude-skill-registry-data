---
name: ruby-tdd-refactoring
description: Use when changing Ruby/Rails behavior, fixing bugs, adding coverage, refactoring, or working under a regression-risk constraint.
license: MIT
---

# Ruby TDD and Refactoring

## Purpose

Use tests as executable behavior contracts and keep structural changes small enough to verify continuously.

## Activate when

- behavior changes
- a bug is fixed
- a public method/API is modified
- code is refactored
- missing edge-case coverage is discovered
- a task explicitly requires TDD

## Repository inspection

Before writing tests:

- identify RSpec/Minitest/other stack
- inspect existing test organization
- inspect fixtures/factories/helpers
- inspect CI commands
- identify integration/system/request coverage
- reuse existing matchers and conventions

Do not introduce a second test framework without a reason.

## Test seams

A seam is the public interface a test exercises: the place where behavior is observable without reaching inside. Before writing the first test, write down the seams under test and confirm them with the user when they are available. Prefer existing seams and the highest seam that still gives a fast, precise signal; for Rails that is often a request, job, or model public method rather than a private helper.

When the interface itself is in question (how much it should hide, where the seam belongs), load `ruby-api-design` and its deep-module reference before writing tests.

## TDD loop

When practical, work in vertical slices: one test, the minimal code to pass it, then the next test.

```text
agree seams
  -> red: one failing test at an agreed seam
  -> green: the smallest code that passes it
  -> refactor on green, one structural change at a time
  -> next slice
  -> regression suite
```

- Write the failing test first and only enough code to pass it; do not anticipate later tests.
- Do not write a batch of tests before any implementation. Tests written ahead of the code test an imagined shape and stop responding to what each slice teaches.
- Refactor only on green, as its own step, and keep structural changes out of the red → green step.

For an existing bug, a regression test should demonstrate the defect before the fix when feasible.

TDD is a development discipline, not a requirement to force a literal red/green sequence when working in a constrained production/debugging workflow.

## Test quality

A test should make the behavior easy to understand.

Prefer behavior-focused expectations.

Cover:

- normal behavior
- boundaries
- invalid input
- failure behavior
- important side effects
- regression conditions

Avoid coupling tests to incidental private implementation details.

Take expected values from an independent source: a known literal, a worked example, or the requirement. A test that recomputes the expected value the way the code does passes by construction and can never catch a bug.

Double only at system boundaries you do not control (external HTTP APIs, payment and mail providers, time, randomness). Use the real objects you own. Load `references/test-quality.md` for Ruby examples of good and bad tests and for mocking rules.

## RSpec readability

When the repository uses RSpec, organize related examples with meaningful `describe`/`context` structure and descriptions that state behavior.

Use existing repository conventions for `subject`, helpers, shared examples, and factories.

## Refactoring

A refactor changes structure without intentionally changing observable behavior.

Sequence:

1. characterize current behavior
2. add missing coverage
3. make one structural change
4. run focused tests
5. inspect diff
6. repeat
7. run regression suite

Characterization gate:
- Before the first structural change, pin current observable behavior with characterization tests. Pin what the code does today, including known bugs: mark those as known, and do not fix them.
- Run the characterization tests on the unchanged code; they must pass. A characterization test that fails before any change is describing the wrong behavior.
- Never combine a structural change and a behavior change in one commit. A bug found during the refactor gets its own commit, with its own failing test first, before or after the refactor.

## Algorithm evaluations

When an algorithm requirement gives complexity targets, tests must prove output while a separate check/review substantiates complexity and auxiliary space.

Include:

- empty input
- singleton
- duplicates
- already sorted/reverse-sorted
- boundary values
- impossible/no-result cases

## Failure modes

- tests that pass despite broken behavior
- tautological tests whose expected value is recomputed with the implementation's own logic
- over-mocking the system under test
- asserting implementation details, private methods, call counts, or database rows instead of the public interface
- writing every test before any implementation (horizontal slicing)
- tests at seams nobody agreed to
- one huge integration test for every behavior
- adding tests after a broad refactor with no characterization coverage
- changing tests simply to make a failing implementation pass

## Completion contract

A task is complete only when:

- intended behavior is implemented
- relevant tests pass
- regression coverage passes
- applicable static/lint/CI checks pass
- final diff has no accidental scope expansion
- any unrun verification is disclosed

## Reference example

Red-green-refactor as an executable loop: the test states the behavior first, then the implementation earns it.

```ruby
require "minitest/autorun"

# red: written first, fails against an empty implementation
class SlugTest < Minitest::Test
  def test_slugifies_title_cased_input
    assert_equal "four-great-ruby-books", Slug.call("Four Great Ruby Books!")
  end

  def test_collapses_repeated_separators
    assert_equal "a-b", Slug.call("a --  b")
  end
end

class Slug
  def self.call(title) = title.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")
end

# green: run `ruby slug_test.rb` - both assertions pass, no app code was touched first.
```

## Agent review checklist

- [ ] repository test stack identified
- [ ] seams under test agreed before the first test
- [ ] contract expressed by tests at those seams
- [ ] expected values come from an independent source, not recomputed
- [ ] doubles used only at system boundaries
- [ ] edge/failure paths considered
- [ ] regression case added when appropriate
- [ ] focused tests pass
- [ ] broader checks run where appropriate
- [ ] tests remain readable

## References

Load only when needed; the reference is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| writing or reviewing test assertions, doubles, or mocks | [references/test-quality.md](references/test-quality.md) | Good and bad tests; tautological tests; verifying through the interface; when to mock; designing for doubles | `regression-test`, `rspec-verifying-doubles` |

## Verification

Run the smallest useful test first, then the affected suite, then broader regression checks as justified by the change.

## Source foundation

Grounded in the TDD and clean-test material of *Clean Ruby*, including the emphasis on behavior clarity and readable RSpec structure, and reinforced by the exercise-driven Ruby practice model of *The Ruby Workshop*.

Agreed test seams, vertical slices, the tautological and implementation-coupled test anti-patterns, and mocking only at system boundaries are adapted, in this repository's words and with Ruby examples, from the `tdd` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). This skill keeps refactoring inside the loop, on green, where that skill moves it to review.

## Book cross-reference: *Clean Ruby*

Chapters 6–7 emphasize small refactorings, single responsibility, writing tests first, and keeping tests understandable. Translate that into a behavior-preserving loop: establish a failing regression test when feasible, make the smallest passing change, refactor only on green, and run focused plus relevant regression tests. Do not copy the book's example implementation when an original example is clearer for this repository.
