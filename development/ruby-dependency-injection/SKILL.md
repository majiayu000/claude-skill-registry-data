---
name: ruby-dependency-injection
description: Use when an object depends on I/O, external services, time, randomness, persistence collaborators, or interchangeable implementations that should be isolated or replaced in tests.
license: MIT
---

# Ruby Dependency Injection

## Purpose

Make important collaborators explicit so object behavior is testable, replaceable, and understandable.

Ruby dependency injection usually means constructor or method injection rather than a framework container.

## Activate when

- code directly constructs external clients
- tests need network, filesystem, clock, or randomness isolation
- multiple implementations satisfy one collaborator contract
- a service has hidden global dependencies
- an adapter or strategy needs a replaceable implementation

## Repository inspection

Inspect constructor injection, factories/builders, test doubles and fakes, dependency configuration, initializer conventions, global constants, and service locators.

Prefer the repository's existing injection style.

## Decision rules

Inject dependencies when replacement, isolation, or explicit collaboration matters.

Do not inject every trivial value.

Prefer a narrow injected collaborator interface over hidden global lookup when the collaborator is a meaningful boundary.

## Implementation procedure

1. Identify the external or interchangeable dependency.
2. Determine the smallest collaborator interface required.
3. Inject it through constructor or method parameters.
4. Keep the collaborator contract narrow.
5. Use a fake or stub where the test needs isolation.
6. Preserve existing construction through a clear composition boundary.
7. Test normal behavior and dependency failure where relevant.

## Failure modes

- injection for primitive constants with no value
- passing huge dependency bags
- exposing concrete vendor APIs throughout the domain
- service locators hidden behind injection
- mocks that assert implementation details rather than behavior

## Reference example

Constructor injection with keyword collaborators: the production wiring and the test double differ only in the objects passed in.

```ruby
class InvoiceMailer
  def initialize(clock:, transport:)
    @clock = clock
    @transport = transport
  end

  def deliver(invoice)
    body = "invoice #{invoice} at #{@clock.now}"
    @transport.call(body)
  end
end

sent = []
clock = Struct.new(:now).new(Time.utc(2026, 1, 1))
transport = ->(body) { sent << body; :queued }

mailer = InvoiceMailer.new(clock: clock, transport: transport)
mailer.deliver("INV-17")
raise "not delivered" unless sent.first.include?("INV-17")
puts sent.first
```

## Agent review checklist

- Is the dependency genuinely variable or external?
- Is the injected interface narrow?
- Is construction still understandable?
- Can tests isolate the dependency without excessive mocking?
- Is the application composition boundary explicit?

## Verification

Run focused tests with fake collaborators and integration tests with the real boundary where available. Inspect for vendor leakage and hidden global dependencies.

## Source foundation

This is a repository design skill derived from the source material's emphasis on service boundaries, external interfaces, testability, and focused object responsibilities. It is not presented as a verbatim source-book pattern.
