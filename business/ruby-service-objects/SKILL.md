---
name: ruby-service-objects
description: Use when an application workflow coordinates several steps and does not belong naturally to one model or controller.
license: MIT
---

# Ruby Service Objects

## Purpose

Represent a cohesive application operation as a focused object with an explicit public contract.

A service object should orchestrate work, not become a dumping ground for unrelated business behavior.

## Activate when

- a workflow has multiple meaningful steps
- controller or job orchestration is difficult to test
- an operation spans multiple collaborators or models
- a domain action has a clear command-like boundary
- the repository already uses service objects consistently

## Boundary with related design skills

Use `ruby-service-objects` when the primary problem is an application operation/workflow. Use `ruby-poro` for the framework-independent object substrate, `ruby-dependency-injection` for collaborator replacement, and `ruby-api-design` for the public operation contract. Do not activate all four automatically when one skill is sufficient.

## Repository inspection

Inspect app/services or its equivalent, ApplicationService conventions, public entry points such as call/perform/execute/run, namespacing such as Post::Creator, result/error conventions, and existing service tests.

Use repository convention before imposing a generic service API.

## Decision rules

A service should represent an operation, not a noun-shaped collection of unrelated methods.

Prefer names such as Post::Creator, Payment::Capture, or Account::Close over broad UserService, OrderManager, or ApplicationProcessor classes.

A one-public-method convention is useful, but the repository's established entry point wins.

## Implementation procedure

1. Name the operation explicitly.
2. Define inputs and observable output/error behavior.
3. Move orchestration into the service.
4. Inject external collaborators when replacement or isolation matters.
5. Keep domain invariants in the appropriate domain object.
6. Keep the public entry point narrow.
7. Make failure behavior explicit.
8. Add focused service tests.
9. Keep the caller thin and preserve existing behavior.

## Failure modes

- service classes with many unrelated operations
- services that duplicate model validations
- hidden global dependencies
- controllers that still contain the workflow
- inconsistent return types
- speculative extraction of trivial behavior
- deep service-to-service chains with unclear ownership

## Reference example

One public call, an explicit result object instead of exceptions for expected failure, and dependencies injected for testing.

```ruby
Result = Struct.new(:ok?, :value, :error, keyword_init: true) do
  def self.success(value) = new(ok?: true, value: value)
  def self.failure(error) = new(ok?: false, error: error)
end

class ChargeCard
  def initialize(gateway:) = @gateway = gateway

  def call(amount_cents:)
    return Result.failure("amount must be positive") unless amount_cents.positive?

    txn = @gateway.charge(amount_cents)
    txn[:approved] ? Result.success(txn[:id]) : Result.failure(txn[:reason])
  end
end

gateway = Struct.new(:decline_above) do
  def charge(cents)
    cents < decline_above ? { approved: true, id: "txn_1" } : { approved: false, reason: "declined" }
  end
end.new(10_000)
service = ChargeCard.new(gateway: gateway)

declined = service.call(amount_cents: 20_000)
raise "decline must be a failure" if declined.ok?
puts declined.error

approved = service.call(amount_cents: 5_000)
puts "charged: #{approved.value}"
```

## Agent review checklist

- Does the service have one coherent operation?
- Is its public API explicit?
- Does it own orchestration rather than unrelated business rules?
- Are dependencies visible?
- Is failure behavior testable?
- Does naming communicate the action?

## Verification

Run service-level tests, caller/request tests, and relevant regression tests. Inspect whether extraction reduced complexity rather than merely relocating it.

## Source foundation

The uploaded Ruby/Rails material explicitly discusses service objects as POROs, focused actionable work, common entry-point methods, and the distinction between stateful service objects and stateless modules. Repository conventions should still be inspected before implementation.
