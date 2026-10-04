---
name: spec-from-intent
description: How to turn an intent.md into a spec.md in this repository, with the standing policies applied while writing rather than discovered in review. Use whenever asked to write, review or revise a spec, and at the start of any design conversation that has an intent behind it.
---

# Intent to spec

Input: an `intent/NNNN-name/intent.md`. Output: `spec.md` beside it, in the
shape of `intent/0000-template/spec.md`. This is Stage 2, and its job is to
apply the policies while the design is still free — the alternative is finding
out in review, when the design is a diff and moving it is expensive.

## Apply these while writing, not afterwards

Read the intent, then walk the constraints in this order, because they
disqualify designs at very different costs:

1. **Determinism** (`determinism-review`). Does the proposed behaviour observe
   time, randomness or ordering? Everything does eventually — say how it reaches
   `f_env::Env`. A design that cannot is not a design yet.
2. **The frame** (`frame-and-unsafe`). Does this need `unsafe`? If so it lives
   in `abi/`, `ring/` or `kernel/`, and if the intent puts it elsewhere the spec
   has to move it or argue for an RFC.
3. **The licence boundary** (`licence-boundary`). Does it touch imported code?
   Then the interface is a ring, and that shapes the whole design, not the last
   paragraph of it.
4. **Evidence** (`claims-registry`). What observation closes this? A named test,
   a claim with a threshold, or a document that can now say something it could
   not. Write it in the spec, because a spec whose evidence section is written
   afterwards gets the evidence that happened to be available.
5. **Decisions** (`rfc-author`). Does this contradict something written down, or
   would somebody reasonably re-litigate it? Name the RFC the change will need.

## What a good spec does that a bad one does not

- Names what it is **not** doing, and where that work goes instead. This is the
  section that stops scope growing during the build.
- States the failure it expects. "Most likely to be wrong here" is a real
  section, and an empty one usually means nobody looked for it.
- Stays in the repository's terms. `intent.md` is written by whoever wanted the
  thing, possibly in their own vocabulary; the spec is where that becomes crate
  names, milestones and `TODO.md` IDs.
- Is shorter than the conversation that produced it, and longer than the intent.

## Boundaries

The spec goes back to the originator before `plan.md` starts. Flag anything you
had to decide on their behalf, in a list, at the end — those are the places a
review is actually worth their time. Do not silently resolve an entry from the
intent's *Open questions*: either answer it with a reason, or carry it forward.
