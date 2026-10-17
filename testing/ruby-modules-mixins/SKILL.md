---
name: ruby-modules-mixins
description: Use for Ruby modules, namespaces, shared behavior, include, extend, prepend, callbacks, and method lookup design.
license: MIT
---

# Ruby Modules and Mixins

## Purpose

Use modules for coherent capabilities or namespacing while keeping method lookup understandable.

## Activate when

- behavior is shared by multiple classes
- a namespace is needed
- `include`, `extend`, or `prepend` appears
- a module callback changes class behavior
- inheritance is being considered as a code-reuse mechanism

## Repository inspection

Inspect:

- ancestor chains
- existing modules
- inclusion/extension callbacks
- method visibility
- tests around shared behavior
- naming and namespace conventions

Use a small reproduction when method lookup is unclear.

## Module versus class

Use a module for:

- shared behavior
- a coherent capability
- namespacing

Use a class when identity/state/lifecycle is central.

Do not create a module that is merely a miscellaneous helper bucket.

## include / extend / prepend

- `include` contributes instance methods through the ancestor chain.
- `extend` adds module methods to a receiving object.
- `prepend` changes lookup order and can intercept or wrap behavior.

When using these, reason explicitly about the resulting ancestor chain and super calls.

## Cohesion

A module should group one understandable concept.

If you cannot explain the module in one sentence without "and also", reconsider the boundary.

## Callbacks

Inclusion/extension callbacks are powerful but implicit.

Use them only when the callback contract is stable, tested, and clearer than explicit configuration.

## Namespaces

Keep namespace depth proportional to the domain. Avoid namespacing purely for ceremony.

## Shared behavior versus configuration

Do not use a module when a collaborator object or dependency would make the behavior explicit and independently testable.

## Anti-patterns

- `Utils` or `Helpers` catch-alls
- excessive mixin stacks
- hidden callbacks
- prepend without tests for lookup/order
- modules that carry unrelated domain state
- mixins used only to avoid writing a collaborator

## Reference example

A mixin that stays honest: an included hook documents the contract, and prepend composes around the including class.

```ruby
module Timestamped
  def self.included(base)
    base.attr_accessor :created_at
  end

  def record_timestamp!
    self.created_at = Time.now
    self
  end
end

module AuditTrail
  def save
    [:"audit", super].join(":") # prepend wraps the original
  end
end

class Document
  include Timestamped
  prepend AuditTrail

  def save = "saved"
end

doc = Document.new.record_timestamp!
raise "timestamp missing" if doc.created_at.nil?
puts doc.save
```

## Agent review checklist

- [ ] module has one coherent purpose
- [ ] class/module decision is explicit
- [ ] ancestor chain is understood
- [ ] include/extend/prepend choice is intentional
- [ ] callback behavior is tested
- [ ] composition was considered

## Verification

Test the consumer classes, method lookup, visibility, and `super` behavior where relevant. A focused ancestor-chain reproduction is appropriate for subtle lookup problems.

## Source foundation

Grounded in the modules, mixins, inheritance, encapsulation, and polymorphism material of *The Ruby Workshop*, combined with *Clean Ruby* guidance to split modules until the grouped concept is clear.

## Book integration: *The Well-Grounded Rubyist*

Chapters 4–5 and 13 cover modules, mixins, `include`/`prepend`, `super`, method lookup, and refinements. Before changing shared behavior, inspect the ancestor chain and affected consumers. Prefer a coherent namespace or mixin contract; use refinements or monkey patches only when their scope and compatibility consequences are explicit and tested.
