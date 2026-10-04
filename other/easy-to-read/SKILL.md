---
name: easy-to-read
description: "Use when reviewing or shaping code that's hard to follow. Count the layers between a question and its answer and the state a reader has to hold in their head. Collapse one-caller wrappers, shrink mutable scope, and make names and functions carry their own meaning."
disable-model-invocation: true
kind: principle
---

# Easy to read

Code gets read far more than it gets written. Line counts, complexity scores, and "clean architecture" are stand-ins. What matters is how much work a reader has to do to understand the code. Track two things:

1. **Layers to trace.** How many hops sit between a question and its answer.
2. **State to hold.** How much hidden or changing context the reader has to keep in their head.

They're independent. A flat file with fifty globals is as hard to follow as a six-layer adapter stack. Watch both.

## Cut layers

- **Collapse layers that don't earn their keep.** Wrappers with one caller. Adapters with no second implementation. Indirection added for a future that never came. Inline them.
- **Each layer should change the abstraction.** A layer that repeats the same methods and arguments as the one below it adds reading without adding meaning. Collapse pass-throughs.
- **Boundaries should hide real decisions.** A broad interface that hides little makes the reader learn both the interface and the implementation. Prefer a narrow boundary that hides something meaningful.
- **Before adding a layer, ask what it saves.** It has to reduce reading somewhere else by at least as much as it adds.

## Cut state

- **Prefer returns over mutations.** Pure functions where possible.
- **Keep scope small.** Locals over fields. Fields over module state. Module state over globals.
- **Derive instead of syncing.** If a value can be computed from another, compute it. Two copies that have to stay in sync are a bug waiting to happen.
- **Name an invariant once, at the boundary.** Not in every consumer. The reader learns it in one place.

## At the line level

- **Names carry the meaning.** If a name needs a comment to explain it, the name failed. `elapsedDays` beats `d`. `isEligibleForDiscount()` beats `check()`. Pronounceable, searchable, no abbreviations the reader has to decode.
- **A function does one thing.** Not one line, one thing at one level of abstraction. The test: if you can pull out another function with a name that isn't just restating the code, it's doing more than one thing.
- **Fewer arguments.** Zero is ideal, one or two is fine, three is suspicious. Never a boolean flag. `render(true)` tells the reader nothing, and it means the function does two things. Split it.
- **No side effects the name doesn't say.** A `checkPassword()` that also starts a session is lying. A function either does something or answers something, not both.
- **Don't return null. Don't pass null.** Every null is something the reader has to remember to check somewhere else. Return an empty collection, throw, or use an optional type.
- **Comments explain why, never what.** If a comment describes what the code does, rewrite the code until it doesn't need one.

## The test

Can someone new to the code answer "where does X come from?" and "what can change X?" in under thirty seconds? If not, cut layers or cut state.
