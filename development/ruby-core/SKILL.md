---
name: ruby-core
description: Use when implementing, reviewing, or debugging Ruby language behavior, syntax, object semantics, truthiness, method dispatch, runtime behavior, or version-sensitive Ruby code.
license: MIT
---

# Ruby Core

## Purpose

Make the agent reason from Ruby's actual execution model instead of translating habits from statically typed languages.

## Activate when

- the task is primarily Ruby rather than Rails
- syntax or runtime semantics are uncertain
- a bug depends on receiver, return value, truthiness, coercion, scope, or dispatch
- code uses Ruby-specific features such as blocks, symbols, keyword arguments, pattern matching, or implicit returns
- the supported Ruby version may change the available behavior

## Repository inspection

Before changing code:

1. Read `.ruby-version`, `.tool-versions`, Gemfile and CI/runtime configuration.
2. Inspect neighboring code for the project's preferred Ruby idioms.
3. Identify public method contracts and important callers.
4. Read focused tests before changing semantics.

Never infer the supported Ruby version from memory.

## Decision rules

### Objects and dispatch

Treat every value as an object with behavior. Ask:

- What is the receiver?
- Which method is actually dispatched?
- Is the call public, private, delegated, or dynamically resolved?
- What does the method return on every relevant branch?

Use duck typing when a stable interface is enough. Do not add class checks merely to make dynamic code look statically typed.

### Truthiness

Ruby treats only `nil` and `false` as falsey. Empty strings, arrays, and hashes are truthy.

Do not "fix" Ruby code by assuming JavaScript-style truthiness.

### Expressions and returns

Prefer Ruby expressions and implicit returns when they improve readability. Make an explicit `return` when early exit or a return contract is materially clearer.

Do not refactor return behavior merely for style.

### Mutation

Distinguish:

- mutating methods
- non-mutating alternatives
- bang methods whose semantics are repository-specific

Never assume a bang method always mutates or that it always returns `nil`.

## Procedure

1. Resolve the runtime version.
2. Identify the precise semantic question.
3. Reduce the behavior to a small reproduction when needed.
4. Inspect the existing contract/tests.
5. Implement the smallest compatible change.
6. Run the focused test/reproduction.
7. Run relevant regression checks.
8. Inspect the diff for accidental semantic changes.

## Common failure modes

- treating empty collections as falsey
- inventing static type guarantees
- using `is_a?` branches where duck typing is sufficient
- confusing `nil` with `false`
- relying on syntax unavailable in the project's Ruby version
- changing an implicit return while refactoring unrelated code
- assuming a method mutates because its name ends in `!`

## Reference example

Object identity versus equality, dup versus clone, and freeze as a real immutability boundary for shared literals.

```ruby
a = "cfg"
b = "cfg"
puts "equal content: #{a == b}"
puts "distinct objects: #{a.equal?(b)}"

# dup copies content; clone also copies singleton state (frozen included here)
frozen = "default".freeze
soft = frozen.dup
soft << "-overridden" # dup is mutable even when source was frozen
puts soft

# a frozen object fails loudly on mutation
begin
  frozen << "x"
rescue FrozenError => e
  puts "frozen: #{e.class}"
end
```

## Agent review checklist

- [ ] Ruby version resolved
- [ ] receiver and return contract understood
- [ ] truthiness handled correctly
- [ ] mutation behavior preserved
- [ ] dynamic behavior not invented
- [ ] version-sensitive syntax verified
- [ ] focused and regression tests run

## Verification

Use a minimal reproduction for semantic questions, then run the repository's focused tests and relevant suite. Verify version-sensitive behavior against the actual runtime rather than an assumed modern Ruby.

## Source foundation

Grounded in the Ruby language fundamentals and execution-focused approach of *The Ruby Workshop*, with the quality principle from *Clean Ruby* that code should be readable, straightforward, and easy to change.

## Book integration: *The Well-Grounded Rubyist*

Use the book's object/message model to reason about receivers, method dispatch, references, return values, `self`, scope, visibility, and truthiness (principally chapters 1–7). For version-sensitive syntax and APIs, inspect the repository's Ruby constraint and verify against current Ruby documentation: this second edition describes Ruby 2.1, not today's runtime.
