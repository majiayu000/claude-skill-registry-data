---
name: architect
description: "Use for \"architect this\", \"design this\", or any change that crosses a module boundary where jumping to code would lock in the wrong shape. Sketches types, signatures, and module layout with empty bodies, gets several candidates through arena, picks one, then fills in code against it. Throws the sketch out if implementation proves it wrong."
disable-model-invocation: true
---

# Architect

Design before you implement. Sketch the types, the function signatures, and the module boundaries, with `not implemented` bodies and pseudocode where the logic is tricky. Get more than one candidate. Pick one. Then write code against it. If the code keeps fighting the sketch, the sketch was wrong. Throw it out.

## Start

A todo list with one entry per phase: ground, sketch, agree, implement, scrap. This runs without checkpoints by default, and the list shows where you are.

## Ground

Build a real model of every system the new code touches. Run `how` on the relevant areas. If the design changes who owns what or which layer does what, run `why` on the existing shape too, so the original reasoning becomes a constraint instead of a guess.

Naming a file isn't grounding. Produce the traced explanation `how` produces.

Skip this only for genuinely greenfield work with nothing to integrate with.

## Sketch

Run `arena` with the design task and the grounding. Each runner gets `references/runner-prompt.md`. Each candidate produces a design package shaped by `references/rationale-template.md`: the caller's usage first, then the types, signatures, and module map derived from it, then the rationale.

Design it twice. At least two candidates that differ in shape, not in flavor, even when the first looks fine. A second version of the first idea doesn't count.

Screen every candidate against `references/design-red-flags.md` before picking. Shallow modules, leaked internals, modules organized by execution order, pass-through methods. Reject or revise.

Compare the survivors on how much each hides behind how small an interface. Prefer the design that pulls complexity into the callee and keeps the public interface small. A rich interface keeps call chains short by concentrating capability instead of spreading it across layers.

Arena returns one synthesized design package with its synthesis decision filled in.

## Agree

Default is no checkpoint. Go straight to implementation with the synthesized design.

The human can opt in with "architect with checkpoint" or "show me before you build". Then surface the design and wait.

Either way, the sketch can land as its own commit. Later commits read as filling in bodies against a stable contract. Planned breakage during fill-in is fine, that's `break-code-not-data`.

For adversarial pressure on the design before building, run `interrogate` on the sketch.

If the human pushes back on the shape, at a checkpoint or after, that's grounding evidence. Re-ground and re-sketch before writing more code.

## Implement

Replace `not implemented` with code, pseudocode with logic. The sketch is the contract.

A deviation from the sketch is a signal, not friction to absorb. If a function needs a parameter the sketch didn't have, ask whether the sketch was wrong, a requirement was missed, or the implementation is overreaching. Say so. Don't bolt it on.

## Scrap

If implementation keeps producing the same kind of friction the sketch can't absorb, throw the sketch out. Don't patch a wrong design.

The signal is a pattern, not one hard case:

- The same workaround shape showing up in unrelated places.
- Several unrelated edge cases each needing a special branch.
- Types that need escape hatches, `any`, casts, optional fields that are always set, to compile.
- Reaching for a lock when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internals to use it.
- Two or more implementation deviations of the same shape.

Use judgment. A few edge cases don't condemn a design. Complexity in the data isn't complexity in the design.

When you scrap:

1. Run `how` over what's been built. The lessons go in as inputs, not vibes.
2. Redesign as if the new constraints had been known on day one.
3. Remove before you add. The new sketch is smaller than the old one before it grows.
4. Back to sketch. Rerun arena.

## Output

The caller's usage first, then the type sketch derived from it. One file of new types and signatures for a small change. A module map plus type definitions for larger work. The rationale beside it, shaped by the template, including the usage sketch and the synthesis decision.
