---
name: no-duplicate-logic
description: Use when adding a case, check, or branch to a function that already exists, especially after jumping straight to the insertion point.
---

## The rule

Before you add logic to a function that already exists, read the whole function. The case you're about to write is often already handled a few lines down. A second block that produces the same result doesn't replace the first — both run, and the output silently doubles. The fix you needed was usually three lines added to the block that's already there, not a new block beside it.

This is not the same as fixing in the shared layer. That's about *where* a bug lives across callers. This is narrower: don't paste a parallel branch inside one function without reading what's already in it.

## Fires when

Adding a case, branch, check, or emit to an existing function, handler, switch, or validation pass — especially when you jumped straight to the insertion point without reading the rest of the function.

## How to apply

Before adding logic that emits a result keyed by some id or name, search the whole function for that id or that result. If a block already handles it, extend that block instead of adding a new one. Read the function top to bottom before you insert anything into it.

## Worked example

A validation function already emits a "bad-name" issue for a record. You add a new block to emit "bad-name" without noticing the existing one a screen above. Now every bad-named record produces two identical issues, and a count somewhere is quietly off by a factor of two. The real change was three lines inside the block that was already there. Reading the function before inserting would have shown it.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just add the block here" | The block may already exist above; read first. |
| "It's a new case" | Check it's actually new before you write it. |
| "The function's long, I'll jump to the spot" | Jumping to the spot is how you duplicate the spot. |
