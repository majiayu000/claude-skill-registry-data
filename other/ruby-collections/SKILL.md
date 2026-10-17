---
name: ruby-collections
description: Use for Ruby Array/Hash data structures and collection algorithms, especially when representation, mutation, indexing, ordering, or algorithmic complexity is the primary concern. Use `ruby-enumerables` when the primary concern is selecting or composing Enumerable transformations.
license: MIT
---

# Ruby Collections

## Purpose

Use Ruby collection abstractions when they express the required transformation without hiding important complexity or mutation.

## Activate when

- manipulating arrays or hashes
- using Enumerable
- filtering, mapping, grouping, counting, sorting, or deduplicating
- designing an array algorithm
- reviewing collection performance or mutation

## Repository inspection

Check:

- supported Ruby version
- collection shape and element contract
- ordering guarantees
- whether mutation is expected
- existing Enumerable conventions
- performance-sensitive callers/tests

## Boundary with ruby-enumerables

This skill answers **which data structure or algorithm should represent the collection problem**. `ruby-enumerables` answers **which traversal/transformation operation expresses an already-chosen collection representation**. When both apply, use both but keep their responsibilities distinct.

## Preferred operations

Use the operation that communicates intent:

- `map` — transform every element
- `select` — keep matching elements
- `reject` — remove matching elements
- `find` — return one matching element
- `any?`, `all?`, `none?`, `include?` — predicates
- `each` — side effects
- `group_by`, `tally` — grouping/counting when supported and appropriate
- `uniq` — deduplication
- `sort`, `sort_by` — ordering

Do not choose an operation only because it is shorter.

## Complexity discipline

For non-trivial collection work, state expected:

- time complexity
- auxiliary space
- ordering behavior
- mutation behavior

A collection pipeline can hide repeated traversal or allocation. Inspect the full pipeline before declaring it efficient.

## Mutation

Default to non-mutating transformations unless the contract requires mutation.

When mutating:

- make ownership explicit
- avoid modifying caller-owned collections unexpectedly
- use bang methods only when their semantics are clear

## Hashes as indexes

A hash is often the right structure for membership/counting/indexing problems. Use it when the additional space is acceptable.

When an evaluation explicitly requires `O(1)` auxiliary space, do not replace the requested algorithm with a hash-based shortcut.

## Readability

Expand a pipeline when a reader must reconstruct several intermediate concepts. Small, well-named steps are often easier for an agent and a human to maintain than a dense chain.

## Anti-patterns

- repeated `select`/`map` passes when one traversal is required
- accidental quadratic lookup
- mutating the input without a contract
- relying on undocumented ordering
- allocating large temporary collections unnecessarily
- using Enumerable to obscure a required algorithm

## Reference example

Pick the container by access pattern; require set for membership, and prefer the expressive iterators over manual accumulation.

```ruby
require "set"

# membership semantics, not just deduplication
allowed = Set.new(%w[index show])
puts "show allowed: #{allowed.include?("show")}"
puts "destroy blocked: #{!allowed.include?("destroy")}"

# iterator intent beats manual accumulator loops
words = %w[alpha beta gamma delta]
grouped = words.each_with_object({}) { |w, acc| acc[w[0]] ||= []; acc[w[0]] << w }
counts  = words.tally
puts grouped.inspect
puts counts.inspect
```

## Agent review checklist

- [ ] collection contract is clear
- [ ] nil/empty behavior is known
- [ ] order is preserved or intentionally changed
- [ ] mutation is explicit
- [ ] complexity is appropriate
- [ ] pipeline is readable

## Verification

Test empty, singleton, duplicate, nil-relevant, ordered, and large-input cases as applicable. For benchmark tasks, verify complexity and auxiliary-space requirements independently from output correctness.

## Source foundation

Grounded in the arrays, hashes, and collection operations of *The Ruby Workshop*, with *Clean Ruby* principles favoring readable, simple, changeable code.

## Book integration: *The Well-Grounded Rubyist*

Chapters 9–10 are useful when deciding between Array, Hash, Range, Set, and Enumerable. Choose the representation from the access, membership, ordering, and mutation contract—not from habit. Keep algorithmic requirements explicit; an idiomatic built-in operation must not silently violate a stated time- or space-complexity constraint.
