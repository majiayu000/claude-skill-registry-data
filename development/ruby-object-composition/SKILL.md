---
name: ruby-object-composition
description: Use when behavior can be assembled from collaborating objects and inheritance is creating coupling, branching, or fragile extension points.
license: MIT
---

# Ruby Object Composition

## Purpose

Prefer small collaborating objects when behavior varies independently or inheritance would create unnecessary coupling.

## Activate when

- subclasses override behavior in several places
- inheritance branches are growing
- behavior needs to vary independently of object identity
- multiple collaborators can express behavior more directly
- a strategy or adapter boundary is emerging

## Repository inspection

Inspect inheritance hierarchies, overridden methods, modules/mixins, strategy objects, dependency injection, and composition already used in the repository.

Do not replace stable inheritance simply because composition is fashionable.

## Pattern-selection guardrail

Composition is a design option, not a target. First prove that behavior varies independently, that inheritance is creating coupling, or that a collaborator boundary materially improves testability/extensibility. If the existing inheritance is a stable subtype relationship and simple, leave it alone.

## Decision rules

Prefer composition when behavior changes independently from the object's core identity.

Use inheritance when there is a genuine stable subtype relationship and the inherited contract is intentionally shared.

Use Strategy for algorithmic variation, Adapter for external interface variation, and Decorator for layered behavior around an existing interface.

## Implementation procedure

1. Map the current inheritance responsibilities.
2. Identify independently varying behavior.
3. Extract the smallest collaborator interface.
4. Inject or construct the collaborator at a clear composition boundary.
5. Preserve existing public behavior.
6. Remove obsolete inheritance only after tests prove the replacement.
7. Add tests for meaningful collaborator variations.

## Failure modes

- composition with excessive forwarding methods
- one object for every line of code
- replacing simple inheritance with needless indirection
- leaking concrete collaborator types
- changing behavior during an architectural refactor

## Reference example

Composition over inheritance: behavior assembled from collaborators, with explicit delegation instead of an is-a chain.

```ruby
require "forwardable"

class Report
  extend Forwardable
  def_delegators :@source, :rows  # narrow, declared surface

  def initialize(source, formatter:)
    @source = source
    @formatter = formatter
  end

  def render = @formatter.(rows)
end

csv = Struct.new(:rows).new([%w[a b], %w[c d]])
html = ->(rows) { "<table>#{rows.size} rows</table>" }
puts Report.new(csv, formatter: html).render
puts Report.new(csv, formatter: html).rows.inspect
```

## Agent review checklist

- Is the variation genuinely independent?
- Does composition reduce coupling?
- Is the collaborator interface smaller than the inherited surface?
- Can behavior be tested independently?
- Is the resulting design simpler?

## Verification

Run characterization tests before refactoring, focused collaborator tests after extraction, and the relevant regression suite.

## Source foundation

The source material emphasizes responsibility, maintainability, modules, and object-oriented design. Composition-over-inheritance is an explicit repository design principle built from those concepts rather than a claim that the uploaded books prescribe this exact rule.
