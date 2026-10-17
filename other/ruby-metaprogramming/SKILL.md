---
name: ruby-metaprogramming
description: Use when reflection, dynamic dispatch, runtime method creation, open classes, monkey patches, method_missing, define_method, or controlled metaprogramming are explicitly relevant.
license: MIT
---

# Ruby Metaprogramming

## Purpose

Use Ruby's dynamic capabilities when they provide a concrete architectural benefit, while protecting discoverability, debuggability, security, and testability.

## Activate when

- method names are generated dynamically
- reflection is required
- a DSL or framework-style declaration is being implemented
- `method_missing`, `define_method`, `send`, `public_send`, `class_eval`, or `prepend` is used
- an existing class must be extended for compatibility reasons

## Default rule

Prefer ordinary Ruby first.

Metaprogramming is justified when it materially reduces duplication, implements a stable DSL/protocol, or integrates with an established framework mechanism.

## Repository inspection

Before adding dynamic behavior:

1. inspect existing conventions
2. inspect supported Ruby version
3. identify all call sites
4. inspect tests that describe dynamic behavior
5. identify security/trust boundaries
6. determine whether explicit code would be easier to maintain

## Reflection

Use:

- `respond_to?` to test protocol availability
- `method` when a callable object is needed
- `public_send` for dynamic public API invocation
- `send` only when private dispatch is intentionally required

Never pass unchecked user-controlled method names into dynamic invocation.

## method_missing

Treat `method_missing` as a protocol.

If implementing it:

- constrain accepted names
- produce a predictable result/error for unsupported names
- implement `respond_to_missing?` consistently
- test both invocation and reflection

## define_method

Use when method definitions are generated from a trusted, deterministic source.

Prefer explicit methods when the generated code would be harder to inspect.

## Open classes and monkey patches

Avoid modifying third-party/core classes unless there is a strong compatibility reason and the patch scope is explicit.

Prefer an adapter, wrapper, refinement, collaborator, or module when those express intent more safely.

## Failure modes

- magic that hides the public API
- reflection that bypasses authorization
- dynamically generated methods with inconsistent signatures
- `method_missing` that swallows unrelated typos
- monkey patches that break after dependency upgrades
- dynamic dispatch that cannot be statically searched or easily tested

## Reference example

Delegation done correctly: method_missing forwards, respond_to_missing? tells the truth, and undefined names still raise NoMethodError.

```ruby
class AuditedRecord
  FORWARD = %i[save reload].to_h { |m| [m, ->(r) { "audited #{m}" }] }.freeze

  def respond_to_missing?(name, include_private = false)
    FORWARD.key?(name) || super
  end

  def method_missing(name, *args)
    if (op = FORWARD[name])
      op.call(self)
    else
      super # preserve NoMethodError semantics
    end
  end
end

record = AuditedRecord.new
raise "respond_to? must agree" unless record.respond_to?(:save)
raise "must not claim :destroy" if record.respond_to?(:destroy)
puts record.save
begin
  record.destroy
rescue NoMethodError => e
  puts "undefined stays undefined: #{e.class}"
end
```

## Agent review checklist

- [ ] ordinary Ruby considered first
- [ ] dynamic names are trusted/validated
- [ ] public API remains discoverable
- [ ] method_missing has respond_to_missing?
- [ ] monkey patch has a compatibility reason
- [ ] tests exercise dynamic behavior
- [ ] upgrade risks are documented where necessary

## Verification

Write focused tests for generated methods, reflection, method visibility, missing-method behavior, and dependency compatibility. Exercise unsupported names to ensure failures are safe and predictable.

## Source foundation

Based on the metaprogramming, open-class, monkey-patching, and dynamic-method material in *The Ruby Workshop*. The simplicity and maintainability constraints come from *Clean Ruby*: choose the straightforward solution unless dynamic behavior has a concrete benefit.

## Book integration: dynamic boundary rule

The book demonstrates how Rails-style declarations can use runtime method generation. Treat this as a framework/library technique, not a default application technique.

Before using dynamic method generation, record:
- what input names are trusted
- which methods will be generated
- why explicit methods are insufficient
- how reflection will behave
- how unsupported names fail

Prefer explicit Ruby for ordinary application code. Dynamic behavior should remain bounded and testable.

## Book integration: *The Well-Grounded Rubyist*

Chapters 13–15 cover singleton classes, object-specific behavior, open classes/refinements, `method_missing`, hooks, and introspection. Use these techniques as implementation tools for libraries/frameworks—not defaults for ordinary application code. Require a concrete benefit, a bounded dynamic surface, predictable failure for unsupported calls, and tests for method visibility/lookup.
