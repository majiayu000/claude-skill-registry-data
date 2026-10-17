---
name: ruby-boolean-logic
description: Use when implementing or refactoring complex Ruby predicates, conditional expressions, guard clauses, truthiness, or boolean combinations.
license: MIT
---

# Ruby Boolean Logic

## Purpose

Turn conditional logic into explicit, testable domain decisions without changing truthiness or short-circuit behavior.

## Activate when

- a condition contains multiple &&/|| clauses
- nested conditionals are hard to read
- a double negative appears
- a predicate is repeated
- authorization/eligibility/business rules are encoded as raw boolean expressions

## Repository inspection

Inspect:

- current predicate names
- nil/truthy/falsey behavior
- side effects inside conditions
- existing domain vocabulary
- tests for boundary conditions
- whether short-circuit evaluation is relied upon

## Decision rules

Prefer positive, domain-named predicates when a condition tells a meaningful business story.

Prefer guard clauses when they reduce nesting without obscuring the happy path.

Be cautious with unless when multiple logical operators are present; if with a positive predicate is often easier to reason about.

Never add !! merely for style. Use it only when the API explicitly requires a real Boolean.

## Truthiness

Ruby treats only nil and false as falsey. Do not import JavaScript-like assumptions that 0, empty strings, or empty arrays are falsey.

Preserve short-circuiting where the right-hand side may have side effects or may be nil-sensitive.

## Failure modes

- double negatives
- nested conditionals with duplicated checks
- changing if/unless semantics during cleanup
- assuming non-Ruby truthiness
- hidden side effects inside boolean expressions
- extracting trivial predicates until the flow becomes fragmented

## Reference example

Only nil and false are falsy; extract compound conditions into named predicates instead of leaving boolean soup inline.

```ruby
Request = Struct.new(:user, :tenant) do
  # named predicates keep the call site declarative
  def deletable?
    owned_by_actor? && actor_is_admin?
  end

  private

  def owned_by_actor?  = user && user.owner
  def actor_is_admin?  = user && user.admin
end

User = Struct.new(:owner, :admin)
actor = Request.new(User.new(true, true))
raise "should be deletable" unless actor.deletable?
anonymous = Request.new(nil, nil)

# truthiness: 0 and "" are truthy in Ruby, unlike C/JS
puts "0 is truthy: #{!!0}"
puts "empty string is truthy: #{!!""}"
puts "anonymous is deletable: #{!!anonymous.deletable?}"
```

## Agent review checklist

- [ ] business condition has a meaningful name where needed
- [ ] truthiness semantics are correct for Ruby
- [ ] short-circuit behavior is preserved
- [ ] no unnecessary negation
- [ ] guards improve rather than obscure the flow
- [ ] boundary cases are tested

## Verification

Test each meaningful branch and boundary value. When refactoring conditionals, preserve truth-table behavior and any short-circuit dependency.

## Source foundation

Grounded in the Boolean, if/unless, truthiness, comparison, and logical-operator material in *Learn Rails 6*, with readability guidance from *Clean Ruby*.
