---
name: prototype-ui
description: Build 2-4 visual variants of a UI to decide what something should look like, viewable together for direct comparison. Use when unsure how a component or screen should look, or choosing between layout/design approaches. For non-visual questions (state, logic, data flow), use /prototype instead.
allowed-tools: Write, Bash
model: claude-sonnet-5
---

# Prototype UI

A UI prototype produces a decision, not a proof. It needs a person to look at it and pick.

## When to use this

When you're unsure how something should look, or weighing two-plus design directions, and describing the options in prose isn't enough to decide. Not for logic or state questions — use `/prototype` for those.

## Steps

1. **State the question in one sentence.** e.g. "Should the task list be cards or a dense table?" or "Where does the priority indicator go?"

2. **Build 2-4 variants you can view together**, not sequentially. Options, roughly by effort:
   - One file, multiple components, with a toggle (buttons or a URL param) to flip between them live
   - All variants rendered at once, stacked or in a grid, if there's no interactivity to test
   - Use realistic data, not lorem ipsum — density and edge cases (long text, empty states, many items) are often the actual question

3. **Look at it and decide.** This step needs a human — don't skip straight to picking the "obviously correct" one from the code.

4. **Record the decision** — one line, where the real work is happening: which variant, and why. If the winning variant's markup is worth keeping, it can seed the real component directly; no need to rebuild it from scratch like a logic prototype's code would be.

5. **Delete the losing variants.** Keep the winner only if it's actually going into the real implementation next.

## What's different from /prototype

- The artifact has to be visible, not just runnable — a script that logs results doesn't answer a UI question
- Compare variants side-by-side or toggled, not one-at-a-time from memory
- The output is a judgment call, not a pass/fail — it needs a person to look, not just execution
- The winning code may survive into production; it isn't automatically throwaway