---
name: ruby
description: Use when writing Ruby or working in Rails codebases. Covers idiomatic object design, service objects, ActiveRecord query performance, RSpec structure, and RuboCop-clean style.
metadata:
  category: languages
  version: 1.0.0
  tags: [ruby, rails, activerecord, rspec, rubocop]
---

# Ruby

## Purpose

Write Ruby that stays readable as it grows: small objects with clear responsibilities, controllers that stay thin, and ActiveRecord queries that do not quietly issue a query per row.

## When to Use

- Writing or reviewing Ruby and Rails code.
- Refactoring fat models or fat controllers.
- Diagnosing slow endpoints caused by ActiveRecord.
- Structuring an RSpec suite.
- Designing background jobs and their retry semantics.

## Capabilities

- Object design: service objects, form objects, query objects, value objects.
- ActiveRecord: eager loading, scopes, batching, index-aware querying.
- Background processing with Sidekiq or Active Job, including idempotency.
- RSpec structure: request specs, model specs, factories, shared examples.
- RuboCop and Sorbet/RBS typing where valuable.

## Inputs

- Application source, Gemfile, Rails version.
- Slow-query or profiling data when performance is the concern.

## Outputs

- Controllers that authenticate, authorize, delegate, and render — nothing else.
- Named scopes and eager-loaded queries with no N+1.
- Specs that describe behavior rather than restate implementation.

## Workflow

1. **Locate the responsibility** — If a method touches HTTP, business rules, and persistence, split it before changing it.
2. **Extract a service object** — One public `call`, explicit dependencies, no global state.
3. **Fix the queries** — Add `includes`, convert loops into set operations, batch with `find_each`.
4. **Make jobs idempotent** — Retries are guaranteed; double-execution must be harmless.
5. **Gate** — RSpec, RuboCop, and Bullet (or equivalent) to fail the build on N+1.

## Best Practices

- Controllers do not contain business logic. If a controller action exceeds ten lines, extract.
- Callbacks (`after_save`, `before_create`) create action at a distance. Prefer explicit service calls.
- Use `find_each` for anything that could exceed a few thousand rows; `all.each` loads the table into memory.
- Every background job should be safe to run twice. Key the side effect, not the invocation.
- `rescue => e` without re-raising swallows bugs. Rescue the specific class.
- Freeze constants and prefer immutable value objects for domain concepts.

## Examples

**Service object with explicit failure:**

```ruby
# frozen_string_literal: true

class RefundOrder
  Result = Struct.new(:success?, :refund, :error, keyword_init: true)

  def initialize(gateway: PaymentGateway.new)
    @gateway = gateway
  end

  def call(order:, amount_cents:)
    return failure("order not refundable") unless order.refundable?
    return failure("amount exceeds order total") if amount_cents > order.total_cents

    refund = @gateway.refund(order.charge_id, amount_cents)
    order.update!(refunded_cents: order.refunded_cents + amount_cents)
    Result.new(success?: true, refund: refund)
  rescue PaymentGateway::Error => e
    failure(e.message)
  end

  private

  def failure(message) = Result.new(success?: false, error: message)
end
```

## Notes

- Bullet in the test environment, configured to raise, turns N+1 queries into failing tests.
- `frozen_string_literal: true` is worth adding to every file; string allocation is a real cost in hot paths.
- Sidekiq retries with exponential backoff by default. Set `sidekiq_options retry:` explicitly rather than relying on the default for anything that touches money.
