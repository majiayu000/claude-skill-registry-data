---
name: principle-type-system-discipline
description: "Apply when designing typed Luau state or function contracts. Model variants explicitly, narrow boundary data, avoid dishonest casts, and derive shared shapes from one authority."
---

# Typed Luau discipline

Use Luau types to expose domain choices and catch shape drift. Do not pretend Luau can prove runtime Instance classes, attributes, remote payloads, or persisted data without validation.

- Model mutually exclusive states as tagged table variants instead of a table full of optional fields and booleans.
- Give semantic identifiers and records distinct exported types when mixing them would cause a real bug.
- Treat remote payloads, DataStore values, attributes, configuration, and decoded JSON as unknown until the boundary validates and narrows them.
- Prefer narrow function signatures and total returns. Use explicit result variants when failure is part of the contract.
- Avoid `any`, broad casts, and assertion helpers that merely silence the checker. Validate, narrow, or improve the model.
- Handle every tagged variant. Add an explicit impossible-state failure so new variants do not disappear silently.
- Derive shared client/server types from the same definition module. Do not maintain parallel handwritten payload shapes.
- Strengthen a type where partial behavior appears. Stop when extra precision adds ceremony without preventing a failure.

The proof is a smaller set of representable bad states plus boundary checks for facts Luau cannot know.
