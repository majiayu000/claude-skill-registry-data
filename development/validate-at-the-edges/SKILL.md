---
name: validate-at-the-edges
description: "Use when wiring validation, error handling, or framework adapters. Check data once where it enters the system (CLI args, config, network, external APIs, user input) and trust it everywhere inside. Keep business logic in pure functions. Errors that cross an edge are rewritten for whoever receives them. Also answers to boundary-discipline, the name the vendored typescript-best-practices skill uses for it."
disable-model-invocation: true
kind: principle
---

# Validate at the edges

Check data once, where it comes in. Inside, trust the types. Business logic lives in pure functions. The wiring around it is thin and boring.

Validation scattered through the code is noise. It repeats itself and makes you feel safe without being safe. Validate once at the edge and the inside gets to be simple.

The vendored `typescript-best-practices` skill is upstream text, and it calls this principle `boundary-discipline`. When it points you there, that is this file.

## Where the edges are

CLI arguments. Config files. User input. Network requests. External APIs. Files on disk. Anything you didn't produce yourself in this process.

- **At the edge.** Validate, parse raw data into domain types, return errors, be defensive.
- **Inside.** Typed data, errors propagate up, no re-checking. No null check deep in a call chain for something the edge already checked. If you can't name which caller passes null, don't write the check.
- **Across the edge.** Expose domain concepts, not the edge's private shape. Don't re-export transport, storage, framework, or wire types through your public API. General-purpose mechanism stays inside. Special-purpose policy sits at the edge.

## Keep logic out of the wiring

- Business logic in pure functions with no framework imports, so it can be tested without the framework.
- Parsing is a pure transform from raw bytes to typed state.
- Prompt construction is structured state in, string out.
- Scoring and assessment are pure transforms from state to results.

A function that handles errors does only that. One try block that calls one well-named function, catch blocks that do the same. Error handling shouldn't hide the logic it wraps.

## Errors crossing an edge get rewritten

An error is the next instruction for whoever hits it. Internal causes never cross an edge as is. The cause goes to the logs in full. The edge owns its own message, written for the receiver.

- **When the receiver is an agent** (our MCPs, CLIs, APIs). The error text lands in the agent's context and becomes its prompt. Include what was wrong, what was expected, a corrected example, a stable error code to branch on, whether to retry, and anything the system knows that the caller can't see, like "this org already has a default, clear it first". The test is that the agent fixes its call on the next attempt with no other help.
- **When the receiver is a person** (our UIs). Plain words, no internal vocabulary, name the thing on their screen, keep what they typed. If the cause really is on our side, say so honestly with a reference ID.

An edge that can fail with no written message is a bug, not a default.

## The tests

- "Is this data crossing an edge right now?" If not, the validation is redundant.
- "Can this be a pure function the wiring just calls?" If yes, pull it out.
- "Could the receiver take their next step from this error alone?" If not, rewrite it.
