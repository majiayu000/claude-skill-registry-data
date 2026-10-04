---
name: no-scattered-ifs
description: "Use when writing stateful logic, or when code branches a lot or repeats the same assumption about a shape across files. Put the rules of the domain into one structure instead of spreading them across conditionals."
disable-model-invocation: true
kind: principle
---

# No scattered ifs

When the rules of the thing you're modeling live in if statements spread across files, they're easy to get wrong and impossible to see in one place. Put them in a structure that matches the domain. The right structure makes invalid states impossible to write and deletes branches.

Picking the structure when you first write the code is cheap. Recovering it later reads as a refactor, and refactors get deferred.

## Reach for

- **A state machine** instead of scattered booleans, phases, and lifecycle checks.
- **A typed model** instead of loose parameters or the same shape assumption repeated in five places.
- **A map, lookup table, or discriminated union** instead of branching spread across files.
- **A reducer or command/event model** instead of ad hoc mutations.
- **A module organized around one body of knowledge** instead of a sequence of steps like load, validate, transform, save. The order things run in isn't ownership.
- **A small module boundary** that gathers repeated behavior or rules that have to stay true.
- **A queue, cache, index, tree, or normalized collection** where the way the data gets read calls for it.
- **Whatever else fits.** That list is the common cases. If none fit, work out what the code must never allow and how the data gets read, then find the structure that encodes exactly that.

## One responsibility

A module or class has one reason to change. If you describe it with "and", it's two. A class that handles orders and sends emails is two classes. Split it along the "and".

## Don't force it

Boring code is fine when the current shape is clear, local, and unlikely to grow. Be suspicious of any abstraction that adds a layer without removing branches, duplicated rules, invalid states, or lifecycle risk. Pick the obvious structure, the one another agent would assume is already there.

## The tells

- A new feature adds one more branch to an existing if/else chain.
- A second boolean that has to stay in sync with the first.
- Modules named after phases, step one, step two, that each repeat the same domain rules.
