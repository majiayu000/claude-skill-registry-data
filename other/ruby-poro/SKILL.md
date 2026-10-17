---
name: ruby-poro
description: Use when behavior can be represented by a plain Ruby object independent of persistence, controllers, or framework lifecycle.
license: MIT
---

# Ruby PORO

## Purpose

Use plain Ruby objects to isolate cohesive behavior from framework-managed objects when the behavior has its own state, collaborators, or domain contract.

A PORO is an implementation substrate, not a design pattern by itself. Choose the narrower object pattern that matches the responsibility.

## Activate when

- behavior is growing inside a controller, model, helper, or job
- an object needs focused state and collaborators
- logic can be expressed without persistence lifecycle concerns
- a domain concept deserves an explicit Ruby object
- testing is difficult because behavior is coupled to framework infrastructure

## Boundary with related design skills

PORO describes the implementation substrate, not the reason for the abstraction. If the object exists primarily to execute an operation, decide with `ruby-service-objects`; if it represents a business concept, use `ruby-domain-modeling`; if it wraps an external interface, use an adapter; if it is only a value, consider a value object. Avoid treating PORO as a catch-all category.

## Repository inspection

Inspect existing PORO directories, service/policy/query/form/presenter/command objects, dependency injection conventions, construction lifecycle, and tests.

Do not create a new directory convention if the repository already has one.

## Decision rules

Use a PORO when the behavior has a coherent responsibility and does not require Active Record lifecycle behavior.

Choose a more specific shape when appropriate: value object for an immutable domain value, service/command for an application operation, policy/specification for a business decision, strategy for interchangeable behavior, adapter for an external interface, query object for complex reads, form object for multi-model input, or presenter for presentation transformation.

Do not use POROs merely to increase the class count.

## Implementation procedure

1. Identify the responsibility and public contract.
2. Separate framework concerns from domain/application behavior.
3. Define the smallest useful object API.
4. Inject collaborators that should remain replaceable or testable.
5. Keep state private unless it is part of the public contract.
6. Follow repository construction conventions.
7. Add focused tests for observable behavior.
8. Integrate it into the existing caller without unnecessary architectural churn.

## Failure modes

- creating a PORO for a trivial method
- duplicating Active Record responsibilities outside the model
- hiding global dependencies
- exposing mutable internal state unnecessarily
- generic Manager or Processor classes with unclear responsibility
- extraction solely to satisfy a pattern name

## Reference example

A PORO extracted from a controller: plain object, explicit dependencies, no framework ancestors required.

```ruby
# app/models or app/poros - no ActiveRecord inheritance anywhere
class CartTotal
  def initialize(items, tax_rate:)
    @items = items
    @tax_rate = tax_rate
  end

  def gross = @items.sum(&:price)
  def total = (gross * (1 + @tax_rate)).round(2)

  def breakdown
    { items: @items.size, gross: gross, tax: (total - gross).round(2), total: total }
  end
end

Item = Struct.new(:price, keyword_init: true)
cart = CartTotal.new([Item.new(price: 10.0), Item.new(price: 5.5)], tax_rate: 0.1)
raise "total wrong" unless cart.total == 17.05
puts cart.breakdown.inspect
```

## Agent review checklist

- Is the object framework-independent where appropriate?
- Does it have one coherent responsibility?
- Is its public API small and explicit?
- Are collaborators injected where useful?
- Does the repository already contain an equivalent abstraction?
- Would keeping the behavior where it is be simpler?

## Verification

Run focused object tests, affected application tests, and regression checks. Inspect the diff for unnecessary extraction, duplicated domain rules, and hidden dependencies.

## Source foundation

The Ruby/Rails training material supports plain Ruby service/domain objects, separation of responsibilities, and focused testing. The specific PORO taxonomy here is repository synthesis rather than a claim that every listed object type is explicitly named in the source books.
