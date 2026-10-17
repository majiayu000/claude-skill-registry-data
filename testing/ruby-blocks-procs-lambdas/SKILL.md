---
name: ruby-blocks-procs-lambdas
description: Use when Ruby behavior is passed as blocks, stored as Proc or lambda objects, yielded to callers, or converted with the ampersand operator.
license: MIT
---

# Ruby Blocks, Procs and Lambdas

## Purpose

Choose the simplest callable mechanism that matches the lifetime, argument contract, control-flow semantics, and repository conventions of the behavior.

## Activate when

- a method accepts a block
- behavior must be yielded to a caller
- a callback needs to be stored or passed around
- a lambda or Proc is introduced
- &, yield, block_given?, or Proc.new appears
- block/lambda return or arity behavior is causing a bug

## Repository inspection

Inspect:

- existing callback conventions
- supported Ruby version
- whether callers expect yield semantics
- whether a callable must be stored beyond one method call
- arity/return behavior used by existing tests
- performance-sensitive iteration paths

## Decision rules

Prefer a block plus yield when the behavior is local to one method call.

Prefer a lambda when the callable is a first-class value with method-like arity and return semantics.

Prefer a non-lambda Proc only when its looser arity or non-local return semantics are deliberately required.

Do not introduce a callable object merely to replace a simple block.

## Semantics

Remember:

- blocks are attached to a method invocation
- yield invokes the current block without creating a Proc
- converting with & creates/uses a Proc boundary
- lambdas enforce arguments more strictly than ordinary Procs
- return inside a lambda returns from the lambda; return inside a non-lambda Proc can return from the defining method

When the code depends on these distinctions, write tests for them.

## Anti-patterns

- wrapping a one-line block in a Proc without a lifecycle need
- using Proc/lambda syntax that obscures a straightforward Enumerable call
- relying on non-local Proc returns accidentally
- accepting arbitrary callbacks without documenting their contract
- using &block when yield is sufficient and no Proc object is needed

## Reference example

Block, Proc, and lambda differ in arity strictness and return semantics; both are shown with the failure each prevents.

```ruby
# lambda: strict arity, return exits only the lambda
strict = ->(x, y) { x + y }
begin
  strict.call(1)
rescue ArgumentError => e
  puts "lambda arity: #{e.class}"
end

# proc: lax arity (missing args become nil), return would exit the method
lax = proc { |x, y| [x, y].compact.sum }
puts "proc arity: #{lax.call(7)}"

# block: yielded, converted with & when passed along
def apply(each_item, &blk)
  each_item.map(&blk)
end
puts apply([1, 2, 3]) { |n| n * 10 }.inspect
```

## Agent review checklist

- [ ] callable lifetime is clear
- [ ] arity semantics are intentional
- [ ] return behavior is tested when relevant
- [ ] yield is preferred when a Proc object is unnecessary
- [ ] callback contract is readable
- [ ] no unnecessary abstraction was introduced

## Verification

Test normal invocation, missing/extra arguments when relevant, and return behavior for lambdas/Procs. For callback APIs, verify the caller's observable behavior rather than only checking that a Proc was accepted.

## Source foundation

Based on the blocks, lambdas, Procs, yield, and ampersand-operator material in *Learn Rails 6* and supported by Ruby closure material in *The Ruby Workshop*.

## Book integration: *The Well-Grounded Rubyist*

Chapter 14 is a reference for block/Proc/lambda distinctions, callable Method objects, closures, dynamic evaluation, threads, and subprocess interaction. Keep callable lifetime, arity, non-local return semantics, and side effects explicit. Never pass untrusted input to `eval`; prefer ordinary dispatch or a constrained parser.
