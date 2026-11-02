---
name: slice-and-estimate
description: Use when planning a feature or estimating work — a thin vertical tracer-bullet slice first, prototype only the unknown, and estimate in ranges before committing.
---

# Slice and Estimate

Plans a feature as a thin vertical slice and estimates in ranges (The Pragmatic Programmer). It is the
"small PRs" and "reversible by default" companion to
[engineering-principles.md](../../core/_shared/engineering-principles.md).

## 1. Tracer bullet first

Build the thinnest end-to-end slice that touches every layer once (UI → logic → data → back), even if it
does almost nothing. A tracer bullet proves the seams connect and de-risks the architecture before the
feature fills in. It is kept, not thrown away — unlike a prototype.

- A tracer bullet = a minimal but *kept* vertical slice that proves the whole path works.
- A prototype = disposable code to answer one unknown (a perf question, a library's API); it is thrown
  away, and the throwaway is stated up front.

## 2. Prototype only the unknown

Spike only the part you cannot estimate because you have never done it. Everything else is known work:
estimate it directly. Do not let the unknown part hide the cost of the known part.

## 3. Estimate in ranges

- Break the work into steps you can see, then estimate each step; a range (best–likely–worst) beats a
  point.
- Estimate by *scope* and *steps*, and sanity-check against an order of magnitude ("is this a day or a
  week?"). Multiply by what the last similar piece actually took, not what it should have taken.
- Track estimate vs actual as you go; the error is the learning, so the next estimate tightens.

## Verify

The tracer bullet runs end-to-end and is kept; the prototype's question is answered and the prototype is
deleted; the plan states each step with a range and names the one unknown being spiked. State the plan in
the note.

## When to deviate

- A small, well-understood change: estimate it in one line and skip the tracer ceremony.
- A deadline that is fixed by an outside commitment: estimate to reveal the scope, so the scope can be
  cut honestly rather than the estimate fudged.
