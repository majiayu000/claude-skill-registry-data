---
name: ruby-api-design
description: Use when designing Ruby methods, classes, services, or library boundaries whose public inputs, outputs, errors, visibility, or compatibility contract matter.
license: MIT
---

# Ruby API Design

## Purpose

Make public Ruby APIs predictable for both callers and future maintainers.

## Activate when

- introducing a public method or class
- changing parameters or return values
- designing a service/gem/library boundary
- callers branch on result types
- an API is used from multiple places
- compatibility with existing callers matters

## Repository inspection

Inspect:

- all current callers
- tests and fixtures
- visibility
- existing error/result conventions
- supported Ruby version
- documentation/examples if the API is externally consumed

## Decision rules

Prefer:

- explicit required arguments
- keyword arguments for semantically named options
- a predictable return type or narrow family such as Thing or nil
- domain-specific exceptions or result objects when multiple failure outcomes matter
- private helpers for implementation detail

Avoid:

- unrelated return types such as object/hash/false/string
- boolean flags that switch the public method into unrelated modes
- exposing internal hashes when a domain object has stable meaning
- changing a public return contract merely to simplify implementation

## Module depth

Treat every public API as the interface of a module: a method, class, gem, or engine. Callers must learn everything the interface exposes: arguments, return family, errors, ordering constraints, and required configuration.

- Prefer **deep** modules: a small interface over a large amount of behavior. A **shallow** module whose interface is nearly as complex as its implementation adds indirection without leverage.
- **Deletion test**: imagine deleting the module and inlining it into its callers. If complexity reappears across several callers, the module earns its keep; if it vanishes, it was a pass-through.
- **The interface is the test surface.** Callers and tests cross the same seam. A test that has to reach past the interface signals the wrong shape.
- **One adapter is a hypothetical seam; two is a real one.** Do not add an injectable port or strategy until at least two implementations exist, typically production and test.

Load `references/deep-modules.md` when deciding what a module should hide, where its seam goes, how to test it through its dependencies, or when comparing alternative interfaces.

## Compatibility procedure

1. identify the current contract
2. list callers and observable behavior
3. define the intended contract
4. update tests at the public boundary
5. change implementation
6. verify failure and edge behavior
7. inspect downstream callers

## Failure modes

- accidental return-type widening
- exceptions introduced where callers expect nil/results
- optional parameters that silently alter old behavior
- public methods exposing internal state
- undocumented keyword/positional compatibility changes
- changing visibility during refactoring
- shallow wrappers that forward to one collaborator and fail the deletion test
- an injectable port with a single implementation and no test double

## Reference example

A small public API surface with explicit keyword arguments, private collaborators, and a documented deprecation path.

```ruby
class ExchangeRate
  def initialize(fetcher:)          # collaborator injected, not global
    @fetcher = fetcher
  end

  def convert(amount, from:, to:, at: :latest)
    rate = @fetcher.rate(from, to)
    (amount * rate).round(2)
  end

  # Deprecated bridge kept for one minor release, then removed.
  def convert!(amount, from, to)
    warn "convert! is deprecated; use convert(amount, from:, to:)"
    convert(amount, from: from, to: to)
  end
  private attr_reader :fetcher
end

rates = Struct.new(:table) do
  def rate(from, to) = table[[from, to]]
end.new({ [:usd, :eur] => 0.92 })
api = ExchangeRate.new(fetcher: rates)
raise "wrong conversion" unless api.convert(100, from: :usd, to: :eur) == 92.0
puts api.convert(250, from: :usd, to: :eur)
```

## Agent review checklist

- [ ] public contract is explicit
- [ ] arguments are meaningful
- [ ] return behavior is predictable
- [ ] failures have an intentional contract
- [ ] visibility is deliberate
- [ ] module passes the deletion test; no pass-through layer
- [ ] every seam has at least two real adapters, or is not a seam
- [ ] callers were checked
- [ ] compatibility tests exist where needed

## References

Load only when needed; the reference is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| deciding what a module hides, where its seam goes, how to test it through its dependencies, or comparing interfaces | [references/deep-modules.md](references/deep-modules.md) | Vocabulary; depth and leverage; dependency categories; replace-don't-layer testing; designing the interface twice | `dependency-injection`, `adapter` |

## Verification

Test successful results, invalid inputs, failure behavior, nil/empty behavior where applicable, and representative callers. For library APIs, verify the documented entry point independently of implementation classes.

## Source foundation

Grounded in the method, argument, return-value, and class API guidance in *Learn Rails 6*, with responsibility and readability principles from *Clean Ruby*.

Module depth, the deletion test, the one-adapter rule, dependency categories, and designing an interface twice are adapted, in this repository's words and with Ruby examples, from the `codebase-design` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock), which builds on John Ousterhout's *A Philosophy of Software Design* and Michael Feathers' seams. This repository keeps "boundary" as an allowed word.
