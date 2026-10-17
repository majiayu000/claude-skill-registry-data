---
name: ruby-control-flow
description: Use when implementing or refactoring Ruby conditionals, case expressions, loops, boolean branches, guards, or repetitive program flow.
license: MIT
---

# Ruby Control Flow

## Purpose

Express decisions and repetition so the happy path, edge cases, and termination behavior are obvious.

## Activate when

- adding or changing `if`, `unless`, `case`, loops, guards, or boolean expressions
- simplifying nested control flow
- implementing an algorithm with explicit complexity constraints
- debugging skipped branches or unexpected evaluation

## Repository inspection

Read the relevant method and tests first. Check Ruby version and nearby style before using newer control-flow syntax.

## Decision rules

### Choose the construct

- Use `if`/conditional expressions for boolean decisions.
- Use `case` when selecting among meaningful alternatives or patterns.
- Use `each` for side effects.
- Use `map`, `select`, `reject`, `find`, and related Enumerable methods when the collection intent is clearer.
- Use `while`/`until` when the termination condition is naturally state-driven.
- Use `for` only when the repository explicitly prefers it or its semantics are required.

### Guard clauses

Use guard clauses when they remove unnecessary nesting and make preconditions explicit.

Do not turn every conditional into a guard merely to reduce line count.

### Boolean logic

Prefer named predicates or variables when complex conditions require mental parsing.

Be precise about:

- `&&` versus `&`
- `||` versus `|`
- operator precedence
- short-circuit evaluation
- double negatives
- nil/false behavior
- ternary readability

A boolean expression should communicate a business or algorithmic decision, not merely pack tokens onto one line.

### Algorithms

Record:

- input/output contract
- mutation
- time complexity
- auxiliary space
- loop invariant where useful
- termination condition
- edge cases

Do not replace a required algorithm with a convenient abstraction that violates the stated complexity.

## Refactoring procedure

1. Map the current branches.
2. Identify the happy path.
3. Identify guards and failure paths.
4. Name complicated predicates.
5. Simplify one branch at a time.
6. Preserve evaluation order when it affects behavior.
7. Add boundary tests.
8. Run regression tests.

## Common failure modes

- nested conditionals that hide the primary path
- conditions whose precedence is unclear
- changing `&&` to `&` or vice versa without understanding evaluation
- loops with ambiguous termination
- algorithmic code that silently allocates additional space
- clever one-line transformations that obscure control flow

## Reference example

case/in pattern matching for structure dispatch, guard clauses for early exit, and loop-with-break for unbounded streams.

```ruby
Event = Struct.new(:kind, :payload)

def handle(event)
  case event
  in { kind: :order, payload: { total: Integer => t } } if t > 0
    "charge #{t}"
  in { kind: :order, payload: { total: 0 } }
    "free order"
  in { kind: :refund, payload: { id: } }
    "refund #{id}"
  else
    "unhandled"
  end
end

puts handle(Event.new(:order, { total: 420 }))
puts handle(Event.new(:order, { total: 0 }))
puts handle(Event.new(:refund, { id: "r_9" }))

# bounded consumption loop
stream = [1, 2, 3, nil, 4].each
collected = []
loop do
  item = stream.next
  break if item.nil?
  collected << item
end
puts collected.inspect
```

## Agent review checklist

- [ ] branch structure is obvious
- [ ] evaluation order is preserved
- [ ] guard clauses improve, rather than merely shorten, the method
- [ ] loop termination is obvious
- [ ] algorithmic constraints are respected
- [ ] boundary cases are tested

## Verification

Exercise every meaningful branch and boundary. For algorithmic work, use tests or instrumentation to substantiate stated complexity constraints when practical.

## Source foundation

Based on the program-flow material in *The Ruby Workshop* and the boolean-logic/readability guidance in *Clean Ruby*, which emphasizes making complex boolean decisions understandable rather than merely compact.

## Book integration: *The Well-Grounded Rubyist*

Chapter 6 connects conditionals, loops, iterators/blocks, and exceptions. Prefer explicit branching and clear termination conditions over clever control flow. Use exceptions for exceptional or failed operations rather than as ordinary branching when a direct return/predicate contract is clearer.
