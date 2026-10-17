---
name: ruby-clean-code
description: Use globally for Ruby/Rails implementation and review when readability, simplicity, changeability, naming, responsibility, boolean logic, or maintainability matter.
license: MIT
---

# Ruby Clean Code

## Purpose

Optimize for code that is readable, easy to change, and straightforward without turning those qualities into rigid style rules.

## Activate when

Use for every non-trivial Ruby/Rails change and especially during review/refactoring.

## Repository inspection

Before judging code quality, inspect the surrounding implementation, tests, configuration, and repository conventions.

## Primary quality model

Ask:

1. Can the next developer understand the intent quickly?
2. Can the behavior be changed without unnecessary ripple effects?
3. Is the implementation more complicated than the problem requires?

These are decision criteria, not formatting rules.

## Naming

A name should communicate role, intent, or domain meaning.

Prefer names that answer "what is this?" or "what does this do?" rather than vague names such as `data`, `info`, `thing`, `process`, or unexplained `manager`.

Naming should be consistent with the repository.

## Methods

Review:

- responsibility
- parameters
- return contract
- guard clauses
- nesting
- boolean complexity
- comments
- duplication

Do not refactor solely to reduce line count.

## Boolean logic

For complex conditions, consider:

- descriptive local variable
- predicate method
- guard clause
- simpler composition

Be especially cautious with double negatives, dense ternaries, and confusing operator precedence.

## Classes/modules

A class should have a clear role. A module should group a coherent capability or namespace.

Avoid catch-all abstractions.

When a Rails model accumulates unrelated domain roles, consider extracting the role into a focused object rather than repeatedly enlarging the model.

## Comments

A useful comment explains:

- why
- domain constraint
- compatibility constraint
- external behavior
- intentional trade-off

A poor comment repeats syntax.

If code can communicate the reason clearly through naming/structure, prefer the code.

## Simplicity / KISS

Start with the simplest solution that satisfies the contract.

Escalate to:

- inheritance
- metaprogramming
- complex patterns
- new dependencies
- broad abstractions

only when there is a concrete need.

## Refactoring discipline

```text
characterize behavior
  -> identify smell
  -> one coherent change
  -> test
  -> inspect diff
  -> repeat
```

Keep functional changes separate from opportunistic cleanup unless the cleanup is necessary for the feature.

## Quality smells

Investigate, rather than mechanically "fix":

- god methods/classes
- boolean flag methods with unrelated modes
- unexplained duplication
- generic abstractions
- deep nesting
- unstable APIs
- model/controller bloat
- comments compensating for poor structure

## Reference example

The same rule expressed twice: a condition-nested method, then the guard-clause and extract-method version reviewers should push toward.

```ruby
Order = Struct.new(:paid, :shipped, :items) do
  # before: nested conditions, mixed levels of abstraction
  def status_before
    if items.any?
      if paid
        if shipped then "closed" else "awaiting_shipment" end
      else
        "awaiting_payment"
      end
    else
      "empty"
    end
  end

  # after: guard clauses + one decision per method
  def status
    return "empty" if items.empty?
    return "awaiting_payment" unless paid
    shipped ? "closed" : "awaiting_shipment"
  end
end

order = Order.new(false, false, ["book"])
raise "mismatch" unless order.status == order.status_before
puts order.status
```

## Agent review checklist

- [ ] names reveal intent
- [ ] responsibilities are focused
- [ ] abstractions have a concrete purpose
- [ ] boolean logic is readable
- [ ] comments explain non-obvious constraints
- [ ] refactor scope is controlled
- [ ] repository conventions are respected
- [ ] tests protect behavior

## Verification

Read the final diff as a reviewer. Run relevant tests and quality checks. Confirm that the refactor made the code easier to reason about without changing unrelated behavior.

## Source foundation

This skill is directly synthesized from the three core qualities in *Clean Ruby*—readability, ease of change, and straightforwardness—and its guidance on naming, methods, boolean logic, classes, refactoring, and avoiding needless complexity. The practical Ruby syntax and Rails examples are cross-checked against *The Ruby Workshop*.

## Book cross-reference: *Clean Ruby*

Use the book's seven-chapter progression as a review lens: readable/changeable/straightforward code; naming; method contracts; Boolean logic; class responsibilities; refactoring; and TDD. Treat suggested method length or parameter count as a prompt to investigate, never as a numeric rule to satisfy mechanically. Preserve behavior and repository conventions.
