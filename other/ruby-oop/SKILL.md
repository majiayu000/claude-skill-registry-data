---
name: ruby-oop
description: Use when designing Ruby classes, state ownership, encapsulation, inheritance, polymorphism, composition, or domain object boundaries.
license: MIT
---

# Ruby Object-Oriented Design

## Purpose

Use objects to represent concepts with meaningful state, behavior, identity, or collaboration.

## Activate when

- a task introduces or refactors a class
- a data structure has accumulated behavior
- multiple methods manipulate the same state
- inheritance or polymorphism is under consideration
- a domain concept needs a stable API
- a Rails model is becoming a catch-all

## Repository inspection

Inspect:

- existing domain/model classes
- collaborators
- public APIs
- tests
- dependency direction
- naming conventions
- persistence responsibilities

Do not create classes simply because "OOP" was requested.

## Class versus module

Use a class when the concept has identity/state/lifecycle or needs instances.

Use a module when the grouped behavior is a coherent capability or namespace rather than an instance concept.

## Encapsulation

Prefer behavior over raw state access.

Before adding an accessor, ask whether callers really need direct mutation. Broad accessors can turn objects into data bags and make invariants harder to protect.

Keep implementation details private where practical.

## Composition

Prefer composition when a behavior can be assembled from collaborators and when the relationship does not require substitutability.

A class should own the behavior it can naturally own and delegate behavior it does not own.

## Inheritance

Use inheritance only when:

- subtype substitution is valid
- the parent contract is stable
- shared behavior is genuinely polymorphic

Consider composition first when inheritance only exists to reuse implementation.

## Polymorphism

Prefer stable interfaces over repeated type checks when the domain supports it.

Define the minimum collaborator interface the caller needs.

## Initialization

Keep `initialize` focused on establishing valid object state.

Validate required inputs early when appropriate. Avoid constructors with many unrelated dependencies.

## Rails boundary

Do not automatically place every piece of business logic in an Active Record model. A persistence model owns persistence-related behavior; a domain/application concept may deserve its own object.

## Evaluation design

When a task explicitly requires OOP, evaluate:

- responsibility
- state ownership
- collaboration
- encapsulation
- extensibility
- testability

Do not grade merely on the number of classes created.

## Anti-patterns

- god objects
- data bags with dozens of accessors
- inheritance for simple code reuse
- generic `Manager` classes with unrelated responsibilities
- domain logic hidden in controllers/views
- classes created solely to satisfy a rubric

## Reference example

Subtypes honor the base contract (LSP) and callers depend on behavior, not concrete classes (duck typing).

```ruby
class Notifier
  def notify(user, message) = raise NotImplementedError
end

class EmailNotifier < Notifier
  def notify(user, message) = "email to #{user}: #{message}"
end

class SmsNotifier < Notifier
  def notify(user, message) = "sms to #{user}: #{message}" # same contract, no surprises
end

# callers accept anything that quacks like notify(user, message)
def blast(channel, user, message) = channel.notify(user, message)

puts blast(EmailNotifier.new, "ada", "deployed")
puts blast(SmsNotifier.new, "ada", "deployed")
```

## Agent review checklist

- [ ] class represents a real concept
- [ ] responsibility is focused
- [ ] state ownership is clear
- [ ] public API is small
- [ ] composition considered
- [ ] inheritance is genuinely polymorphic
- [ ] collaborators have clear contracts

## Verification

Test public behavior and important collaborations. Exercise invalid state transitions when the object owns invariants. Avoid tests coupled to private implementation details.

## Source foundation

Based on the OOP material in *The Ruby Workshop* and the class/module/refactoring guidance in *Clean Ruby*, especially the emphasis on clear class purpose, limited responsibilities, encapsulation, and restrained inheritance.

## Book integration: *The Well-Grounded Rubyist*

Use chapters 2–5 and 13 to reason about instance state, initialization, instance versus class methods, constants, `self`, visibility, inheritance, and method lookup. The book's object-centered model complements this skill's responsibility and composition rules: Ruby's dynamic capabilities do not by themselves justify more classes, inheritance, or runtime mutation.
