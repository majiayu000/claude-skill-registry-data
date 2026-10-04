---
id: javascript.pure-functions
name: JavaScript Pure Functions
description: >
  Reviews and refactors JavaScript pure functions so deterministic logic is isolated from side effects, mutation, and framework orchestration.
stack:
  - JavaScript
  - TypeScript
category: javascript
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - pure functions
  - pure function
  - immutable function
  - deterministic logic
  - mapper function
  - validator function
  - business rules
  - side effect free
compatibility:
  runtime:
    browser: true
    node: true
---

# JavaScript Pure Functions

## Purpose

Use this skill to review, refactor, or implement pure functions in JavaScript.

The goal is to isolate deterministic business logic from side effects, making the code easier to test, reuse, compose, and reason about.

A pure function returns the same output for the same input and does not mutate external state.

## When to Use

Use this skill when the task involves:

- utility functions
- mappers
- formatters
- validators
- reducers
- selectors
- calculations
- data transformations
- business rules
- testable logic extraction
- removing hidden side effects
- reducing mutation bugs

## When Not to Use

Do not use this skill when:

- the function must perform I/O by design
- the task is about API calls, DOM manipulation, storage, logging, timers, or framework lifecycle code
- the requested change is only about performance optimization without behavior changes
- purity would make the design less clear or force unnecessary abstraction
- existing impure behavior is part of an explicit contract

## Do

Identify side effects and make dependencies explicit.

Avoid mutating inputs.

Separate computation from effects.

Keep pure functions small and named by intent.

Do not over-abstract.

Preserve error behavior during refactors.

Test pure functions deterministically with input/output assertions.

Cover edge cases like empty arrays, nullish values when supported, invalid input, boundary numbers, duplicated values, nested objects, and immutability expectations.

Keep pure functions framework-agnostic.

## Do Not

Avoid mutating arrays with `.sort()`, `.reverse()`, `.splice()`, `.push()`, `.pop()`, `.shift()`, or `.unshift()` unless mutation is explicitly required.

Avoid mutating objects through direct property assignment.

Avoid reading time or randomness inside deterministic logic.

Avoid hiding I/O inside a function that looks like a mapper.

Avoid returning references that callers can accidentally mutate.

Avoid extracting tiny functions that make the code harder to read.

## Review Checklist

- [ ] The function avoids input mutation.
- [ ] Time, randomness, config, and locale are explicit inputs where needed.
- [ ] I/O is kept outside the pure function.
- [ ] Edge cases are tested.
- [ ] The function name is business-oriented.
- [ ] The abstraction is justified.

## Expected Output

1. Identify side effects.
2. Make dependencies explicit.
3. Keep computation separate from effects.
4. Preserve error behavior.
5. Add deterministic tests.
