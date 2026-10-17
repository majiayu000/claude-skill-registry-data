---
name: ruby-enumerables
description: Use when choosing or reviewing Ruby Enumerable traversal and transformation semantics after the underlying collection representation is understood.
license: MIT
---

# Ruby Enumerables

## Purpose

Use Enumerable methods to express collection intent clearly while preserving correctness, allocation behavior, ordering, and complexity.

## Activate when

- a collection is transformed or filtered
- several Enumerable operations are chained
- grouping or counting is needed
- a manual loop could be replaced by a standard operation
- a collection pipeline is suspected to be inefficient or opaque

## Repository inspection

Inspect:

- collection size and expected cardinality
- ordering guarantees
- mutation requirements
- Ruby version and available Enumerable APIs
- existing code style
- performance-sensitive callers/tests

## Boundary with ruby-collections

This skill focuses on traversal semantics, pipeline clarity, allocation, and Enumerable complexity. Use `ruby-collections` when the primary design question is Array/Hash choice, indexing, mutation, or an explicit algorithm/data-structure constraint.

## Decision rules

Use:

- map for one-to-one transformation
- select/filter for membership by predicate
- reject for inverse filtering
- find/find_index for first match
- group_by for partitioning by a key
- tally for frequency counting when the supported Ruby version allows it
- each_with_object for building one accumulator deliberately
- reduce when an accumulated value is the actual abstraction
- any?, all?, none?, one? for predicates
- lazy only when deferred traversal materially helps

Do not choose a shorter pipeline when it makes the domain operation harder to understand.

## Complexity and allocation

Count traversals.

A chain such as select(...).map(...).sort may be correct while still allocating intermediate collections. Preserve clarity, then optimize only when evidence requires it.

When an evaluation specifies an algorithm or auxiliary-space target, follow that contract instead of replacing it with a convenient Enumerable shortcut.

## Mutation

Prefer non-mutating Enumerable transformations unless the repository contract explicitly requires mutation.

Do not mutate a caller-owned collection merely because an Enumerable alternative exists on the same object.

## Failure modes

- repeated passes over a large collection without justification
- using reduce where sum, count, group_by, or another direct operation communicates intent better
- relying on incidental ordering
- hiding an O(n²) operation inside a block
- converting to arrays unnecessarily
- using Enumerable to bypass a benchmark's required algorithm

## Reference example

Including Enumerable is a one-method contract; lazy pipelines defer work until the terminal operation.

```ruby
class ReadingLog
  include Enumerable

  def initialize(entries) = @entries = entries
  def each(&blk) = @entries.each(&blk)
end

log = ReadingLog.new(%w[ok ok err ok warn err])
puts log.count { |e| e == "err" }
puts log.tally.inspect

# lazy: no intermediate 1M-element array is materialized
squares = (1..Float::INFINITY).lazy.map { |n| n * n }.select(&:even?).first(3)
puts squares.inspect
```

## Agent review checklist

- [ ] operation matches intent
- [ ] ordering is explicit
- [ ] mutation is explicit
- [ ] traversal/allocation cost is understood
- [ ] empty input behavior is correct
- [ ] repository/Ruby-version support is checked

## Verification

Cover empty, singleton, duplicate, ordering, and representative large-input cases. For performance-sensitive code, inspect traversal count and allocation behavior in addition to output.

## Source foundation

Grounded in the Enumerable, Array, Hash, and collection material in *Learn Rails 6* and reinforced by the collection/design material already represented in this repository.

## Book integration: *The Well-Grounded Rubyist*

Use chapter 10 for the distinction between iteration, Enumerable, Enumerator, chaining, reduction, and lazy traversal. Treat laziness as a change in evaluation timing, not as an automatic speed improvement. Verify supported APIs against the repository's Ruby version and test ordering, empty-input, mutation, and termination behavior.
