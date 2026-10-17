---
name: rails-test-engineering
description: Use when designing, reviewing, debugging, optimizing, or scaling a Rails test suite across unit, model, request, integration, system, job, mailer, Action Cable, parallel, and CI boundaries. Also covers deciding where model, request, system, and service tests belong for a routine change.
license: MIT
---

# Rails Test Engineering

## Purpose
Treat the test suite as an engineered system with contracts for behavior, isolation, determinism, speed, parallel safety, and production-relevant confidence.

Core model:

test boundary
-> arrange controlled state
-> execute real contract
-> assert observable behavior
-> isolate external dependencies
-> clean state
-> run deterministically
-> integrate into CI

Primary current Rails references:
- https://guides.rubyonrails.org/testing.html
- https://guides.rubyonrails.org/active_job_basics.html

## Activate when
- choosing or reviewing model/request/integration/system/job tests
- changing test helpers, fixtures, factories, or test database setup
- diagnosing flaky tests
- defining or running Rails Local CI with `config/ci.rb` and `bin/ci`
- enabling or tuning parallel tests
- changing transactional test behavior
- testing asynchronous jobs/mailers
- testing time-dependent behavior
- adding system/browser tests
- changing external-service stubs/fakes
- measuring slow tests or test-suite boot time
- reviewing CI test coverage
- introducing a second test framework or test library
- testing reload/eager-load behavior

Choosing or reviewing the test for an ordinary behavior change also routes here; start from `references/routine-test-placement.md`.

## Repository inspection
Inspect:
1. test framework: Minitest, RSpec, or another stack;
2. test directory conventions;
3. test_helper and shared helpers;
4. fixtures/factories/builders;
5. transactional test configuration;
6. database-cleaning strategy;
7. request/system/job/mailbox/channel test conventions;
8. external HTTP/service stubs;
9. time helpers;
10. CI commands and parallelization;
11. test environment configuration;
12. eager-load configuration in CI;
13. current test runtime and flaky-test history when available.

Do not introduce factories, VCR-like tools, a second test framework, or custom cleaning infrastructure until existing repository conventions are understood.

## Test boundary selection
Use the smallest boundary that proves the behavior:

model/domain invariant
-> model/domain test

service/application workflow
-> focused service/domain test

HTTP contract
-> request/integration test

cross-controller workflow
-> integration test

real user/browser interaction
-> system test

job behavior
-> ActiveJob::TestCase

job enqueue from caller
-> caller test with ActiveJob::TestHelper

mail delivery behavior
-> mailer test plus request/system coverage when triggered by user behavior

Action Cable protocol
-> connection/channel tests and broadcast assertions

Use more than one level when the tests prove different contracts. Do not duplicate the same assertion at every layer merely for coverage count.

Rails' current testing guide distinguishes unit/model, functional, integration, system, job, mailer, Action Cable, and other test types. Integration tests are intended for interactions between multiple application components, while system tests exercise the application as a user would.

## Decision rules

1. Detect the suite (Minitest, RSpec, or both) and its conventions before writing a test.
2. Select the owning test boundary above, then load the matching reference below for the technique: data and doubles, request/system/job/mail tests, determinism and flakiness, parallelism/performance/CI, or RSpec.
3. Routine placement questions for a model, controller, job, or mailer change load `references/routine-test-placement.md`.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| writing assertions, fixtures, factories, or builders, isolating database state, or introducing test doubles | [references/assertions-data-and-doubles.md](references/assertions-data-and-doubles.md) | Contract-focused assertions; Fixtures, factories, and builders; Database isolation; Test doubles; Contract and integration tests | none |
| testing requests, browser flows, Active Job enqueue/perform, or mailers and external side effects | [references/request-system-job-mail-tests.md](references/request-system-job-mail-tests.md) | Request and integration tests; System tests; Active Job testing; Mailers and external side effects | `system-test-contract` |
| a test is flaky or order-dependent, or depends on time, time zones, randomness, or external state | [references/determinism-and-flakiness.md](references/determinism-and-flakiness.md) | Determinism; Flaky test diagnosis; Test order; Time and timezone | `flaky-test-diagnosis` |
| a change enables or debugs parallel tests, speeds up the suite, changes CI test strategy, or adds an eager-loading test | [references/parallelism-performance-ci.md](references/parallelism-performance-ci.md) | Parallel test safety; Parallel database tests; Test parallelization threshold; Test performance; CI strategy; Eager-loading test | `parallel-safe-test`, `parallel-database-test`, `test-performance-budget` |
| the repository uses RSpec | [references/rspec.md](references/rspec.md) | RSpec | `rspec-request-spec`, `rspec-job-and-mail-enqueue`, `rspec-mailer-spec`, `rspec-factory-traits`, `rspec-shared-examples-contract`, `rspec-verifying-doubles` |
| deciding where a test belongs for a routine model, controller, job, or mailer change | [references/routine-test-placement.md](references/routine-test-placement.md) | Test placement for routine changes | `test-boundary-selection` |

## Test anti-patterns
- sleep-based synchronization
- global disable of transactional tests
- retrying flaky tests until CI turns green
- direct job.perform as the only job test
- controller tests for HTTP contracts when request tests are available
- system tests for every unit-level rule
- mocking every collaborator
- factories with hidden business state
- tests depending on order
- hard-coded local time zone
- shared fixed ports/files
- broad helper globbing without boot-time measurement
- parallelizing stateful tests without isolation
- deleting assertions to reduce runtime

## Reference example

A deterministic system test: time frozen, browser headless, and the assertion on user-visible state rather than implementation.

```ruby
class CheckoutFlowTest < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome, screen_size: [1400, 900]

  test "guest completes checkout within the offer window" do
    travel_to Time.utc(2026, 1, 15, 12) do
      visit product_path(products(:teapot))
      click_on t("products.add_to_cart")
      click_on t("carts.checkout")

      fill_in t("orders.email"), with: "guest@example.com"
      click_on t("orders.place")

      assert_text t("orders.confirmation", email: "guest@example.com")
      assert_equal 1, Order.count # user-visible outcome, then one state check
    end
  end
end

# test_helper.rb:
#   parallelize(workers: :number_of_processors)
#   # transactional fixtures per worker keep parallel runs isolated
```

## Agent review checklist
- [ ] test framework/conventions identified
- [ ] smallest owning test boundary selected
- [ ] request/system/job layering is deliberate
- [ ] fixtures/factories are explicit and bounded
- [ ] database isolation is understood
- [ ] time is deterministic
- [ ] external boundaries are isolated
- [ ] parallel safety is considered
- [ ] flaky behavior is investigated rather than retried blindly
- [ ] test runtime is measured before optimization
- [ ] CI includes the required test classes
- [ ] eager loading is verified when relevant
- [ ] tests assert contracts instead of incidental implementation

## Verification
Run focused tests first, then the affected suite, then broader CI-equivalent checks. When changing parallelization, transactional tests, system tests, job testing, or test infrastructure, verify the runtime behavior of the test system itself.

## Rails 8.1 current framework considerations

- Rails 8.1 provides Local CI through `config/ci.rb` and `bin/ci`. Treat local CI as part of the repository's executable verification contract when present.
- Keep local and hosted CI commands aligned on security checks, test setup, and required gates; avoid having `bin/ci` silently exercise a weaker contract than the hosted workflow.

## Source foundation
Primary source: Rails Testing Applications guide: https://guides.rubyonrails.org/testing.html
Supporting source: Rails Active Job Basics: https://guides.rubyonrails.org/active_job_basics.html
Framework version notes must be resolved from the target repository and installed Rails version.

## Rails test engineering changes

For testing changes:
- resolve the repository's test framework and conventions first;
- select the smallest boundary that proves the contract;
- keep fixtures/factories explicit and bounded;
- preserve deterministic time, randomness, network, and filesystem behavior;
- diagnose flaky tests from seed/order/parallel/runtime evidence instead of adding blind retries;
- treat parallel tests as an isolation and capacity problem;
- disable transactional tests only at the narrow case that requires independent transactions;
- test Active Job enqueue and execution at the relevant boundaries;
- measure test runtime before optimizing;
- keep CI coverage for system tests and eager-loading where the repository requires them.

## Book cross-reference: *Modern Front-End Development for Rails*

Chapters 14–15 introduce Cypress configuration, end-to-end tests, troubleshooting, and testing Rails/React interactions. Apply these ideas only when Cypress is part of the repository's toolchain. Preserve a layered test strategy: fast unit/component tests for local logic, Rails request/system tests for server contracts, and E2E tests for important cross-boundary user journeys.
