---
name: steel-threads
description: "Order a plan's phases so the first one is a steel thread: the thinnest path through every layer the feature touches, working and shipped, that later phases widen. Use when writing or revising a phase plan in `project-docs/`, splitting a feature into phases or pull requests, or reviewing a plan whose early phases deliver nothing a user can run."
---

# Steel threads in a phase plan

A steel thread is the thinnest slice of a feature that crosses every layer it will touch and does one real thing for a user. It's built to the same standard as everything else and kept: later phases widen it, and none replaces it. The point is to meet the integration problems in the first phase, while they're small, instead of in the phase that finally joins the layers.

This skill is about the order of a plan's phases. It doesn't change what a plan contains: follow the newest plan in `project-docs/` for the sections a plan's README and its phase files have.

## When it applies

Use it when a feature crosses several of Ascribe's layers (the language, the content model, resolve, check, emit, a command, the language server, the MCP server, the extension, Astro, the elements, review) and at least one seam between them is unproven.

Don't force it when:

- the feature lives in one layer (a new check, a new command over what's already resolved);
- the work is a clean-up, which changes no output and has nothing to thread;
- every seam is already in use by something else and the only question is how much there is to build.

Say in the plan which case it is. "No thread: one layer" is a fine answer.

## Choosing the thread

1. **List the layers the finished feature touches,** by crate and package. [ARCHITECTURE.md](../../../ARCHITECTURE.md) says which owns what.
2. **Name the riskiest seam.** The one where an assumption could be wrong and change the design: a source map that has to survive a transformation, another tool's output, something the binary has never linked, the two renderers agreeing, Windows paths.
3. **Pick one use case that crosses the listed layers and goes through that seam.** One page, one build, one rule, one command. It must be something a person or an agent can run and see a result from.
4. **Cut everything the use case doesn't need.** Other cases, options, the second surface that would show the same result, speed.

A thread chosen because it's easy, and that avoids the risky seam, proves nothing.

## What may be narrow, and what may not

Narrow the scope, never the standard.

- **Narrow:** which cases are handled, which surfaces show the result, how many options exist. What isn't handled yet is said plainly, in the docs or in a diagnostic, not left to fail oddly.
- **Not narrow:** the rules in [AGENTS.md](../../../AGENTS.md). The thread has its conformance case, its docs page, its changelog entry in `changes/`, and passes every check. Libraries still don't print or panic, and project files are still read through `FileSystem`.
- **Contracts are the exception to "start small and change it later".** The language, the outputs, the commands' JSON, and the published APIs don't move once shipped. A thread may add to one; it may not ship a shape the plan expects to change. If the thread needs a contract choice that isn't made, a decision by the maintainer comes before it, as its own phase.

## Ordering the phases

- **Phase 1 is the thread,** unless a decision or a move with no behavior change has to come first. Those may precede it, and each says why it can't wait.
- **Each later phase widens the thread** by a use case, a surface, or a kind of input, through as many layers as that takes. A phase that finishes one layer for cases no other layer handles yet is the pattern to avoid.
- **Every phase's result is something a user can do.** If a phase's line in the plan's table reads "the server answers…" or "the types exist", and nothing a user runs has changed, it's a layer, not a slice: join it with the phase that first uses it.
- **Order the widening by risk, then by value.** What might still change the design goes early.

## What to write in the plan

In the plan's README, before the phase table, a short section named "The thread":

- the use case, in one sentence a user would recognize;
- the layers it crosses;
- the seam it tests, and what would be learned if it fails;
- what is deliberately left out, and which phase adds each thing back.

In phase 1's acceptance criteria, the command or the editor action that shows the thread working end to end.

## Checking a plan

- After phase 1 alone, what can someone run, and what do they see?
- Which phase first exercises the riskiest seam? If it isn't the first, why not?
- Could phases 1 to N all land and still leave the feature unusable? Then the join is too late.
- Does any phase ship a contract shape a later phase changes?

## Background

Jade Rubick, [Steel threads are a technique that will make you a better engineer](https://www.rubick.com/steel-threads/). The same idea is called a tracer bullet (*The Pragmatic Programmer*) and a walking skeleton (Alistair Cockburn).
