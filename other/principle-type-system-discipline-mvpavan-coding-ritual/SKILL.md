---
name: principle-type-system-discipline
description: Apply when designing types or a function signature in a typed language.
disable-model-invocation: true
---

# Type-system discipline

Let the checker carry the rules the code would otherwise test at runtime.

- Shape types so the checker rejects impossible states; define special cases
  out of existence instead of handling them.
- Handle every variant of a closed type so the checker reports a variant left
  unhandled.
- Give values that mean different things but share a primitive type their own
  types, validated once when created and trusted afterwards.
- Derive a type from the authoritative schema that owns its shape instead of
  hand-writing a parallel one.
- Where raw input becomes typed values is `principle-boundary-discipline`'s
  rule.
