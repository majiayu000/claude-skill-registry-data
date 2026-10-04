---
name: structure-first
description: "Use before writing logic: picking core types and data structures, deciding what to set up before features, or sharing state between agents or processes. Get the data shape right and the rest of the code gets obvious."
disable-model-invocation: true
kind: principle
---

# Structure first

Two kinds of decisions. Structural ones, like the shape of the data and what runs before what. And code-level ones, like how a function is written. Structural decisions are the expensive ones to undo. Spend your thinking there.

## Get the shape right before the logic

- **Define the core types first.** Before writing any logic, name the data and its shape. Then walk through how the code will read and write it. Pick the structure that matches the paths you'll hit most.
- **Changing a data structure late is a rewrite.** Changing it early is usually a one-line diff. That's the whole reason to do this first.
- **Pick the obvious shape.** The one another agent would assume is already there. If the shape needs a comment to explain, it's wrong.
- **Data outlives code.** Old code and new code will read your schema at the same time: a rolling deploy, a rollback, an agent halfway through a task. Every schema change has to work with both. Add first, migrate, then remove. Never a change where the code and the data have to flip at the same moment.
- **Do the napkin math.** If the shape touches scale, storage, or something metered, estimate it in one line before you commit. Rows per day, bytes moved, dollars per month. Cheap arithmetic kills expensive designs while they're still on paper.

## At code level

Keep the types and data models consistent across the codebase. Don't DRY every line. Three similar statements beat an abstraction you don't need yet. Explicit beats clever.

## Shared state

Before two agents, processes, or threads share a piece of state, ask what happens if one changes it while the other is using it. If the answer is anything other than "nothing", give each one its own copy and merge later.

## What to set up first

If something helps every later phase, do it first. CI, linting, test setup, shared types. Ask "does every step after this get easier because this exists?" If yes, it goes first. Setup before features. Tests before fixes.

Each change adds one coherent piece or deepens one that exists. Don't spread a new capability across callers as a pile of special cases.

Delete before you scaffold. Clear out the dead weight, then build on what's left.
