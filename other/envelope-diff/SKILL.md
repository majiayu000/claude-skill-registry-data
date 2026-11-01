---
name: envelope-diff
description: "Compares two versions of an envelope assembly or detail and reports what the change does rather than what it looks like: which control layer moved, what continuity was gained or lost, which junction details are now wrong, and whether the drying direction changed. Built for the moment a contractor proposes an alternate, a manufacturer's detail replaces yours, or a value-engineering round comes back, because those changes arrive one layer at a time and their consequences arrive at the junctions. Trigger on \"what changed in this assembly\", \"they proposed a different build-up\", \"compare these two sections\", \"is this substitution equivalent\", \"envelope-diff\", or two versions of an envelope construction handed over together. Carries no values; every figure comes with the versions. `document-diff` compares written documents and `drawing-diff` drawing revisions; this compares what an assembly does. It does not replace the enclosure consultant or the Architect of Record."
license: MIT
metadata:
  title: "Envelope Diff"
  summary: "Compare two versions of an assembly or a detail and price the change"
  discipline: "envelope-performance"
  tags: "Review, Analysis"
---

# Envelope Diff

An assembly change looks small. One layer swapped, one thickness reduced, one
membrane moved to the other side of the sheathing. The consequence is never in
the section: it is at the twenty junction details drawn against the old one, and
nobody re-opens those.

## Scope and limits — read first

**What this does.** Compares two versions of an assembly or a detail and reports
what the change does to the four control layers, to continuity, to the junctions
drawn against the old version, and to the drying direction.

**What this does not do.**

- **It carries no values.** Every figure comes with the two versions. A change
  from a named product to another named product with no data is reported as
  unquantified.
- **It does not run the arithmetic.** Whether the new stack condenses is
  `condensation-check`'s, and it should be re-run on any change that moves a
  layer.
- It does not decide whether to accept. That is a `substitution` decision with
  cost and risk behind it. Point at `value-engineering-advisor` for a
  construction-stage list and `submittal-review` for a formal substitution.
- It does not compare documents or drawings generally. `document-diff` and
  `drawing-diff` do.
- It does not replace the enclosure consultant or the Architect of Record.

**What you need before starting.** Both versions, layer by layer, with whatever
values came with each. Which is the earlier one. Who proposed the change and
why. The junction details drawn against the old version, or a list of them.

## Workflow

### Step 1. Establish the two versions and who wants the change

Ask, in one message:

> 1. Both versions, in order, inside face to outside face, with values.
> 2. Which is the earlier one? Say it explicitly.
> 3. Who proposed the change and what reason was given: cost, availability,
>    programme, buildability, performance, or a manufacturer's standard detail?
> 4. What junction details exist against the old version? Point at
>    `design-envelope` for the junction schedule.
> 5. Has anything been built to the old version already?

**Question 3 is not a formality.** A change proposed for cost and a change
proposed for availability need different questions asked of them, and a change
proposed because a manufacturer's standard detail was easier to draw usually
loses something nobody costed.

### Step 2. Report what moved, layer by layer

| # | Old | New | Change | Control layer affected |
|---|---|---|---|---|

Then, separately, the four questions that matter more than the layer list:

| Control layer | Old position | New position | Still continuous? |
|---|---|---|---|

**A layer that stayed the same but moved relative to the insulation has
changed**, and a plain layer comparison hides it. That is the single most common
consequential envelope change and it is invisible in a side-by-side list.

### Step 3. Say what the change does to the junctions

The step that earns the exercise. For each junction detail drawn against the old
version:

| Junction | Still correct? | What has to change |
|---|---|---|

A membrane that moved outboard changes every lap at every opening, every
termination at the base and the top, and every penetration closure. Report the
count of junction details now wrong, before anything else.

Where the junction list is unavailable, say so and say the change cannot be
assessed properly without it.

### Step 4. Say what else moved with it

- **Drying direction.** From where the low-perm layers now sit. A direction,
  never a rate.
- **Thickness.** Anything that changes the overall build-up changes the
  structure line, the window position, the parapet height, and the sill and head
  details.
- **Weight**, if it changed materially, which is the engineer's.
- **Fire and acoustic**, if either version was tested or listed. **A tested
  assembly modified is not that tested assembly**, and this is the finding that
  most often comes back at inspection.
- **Buildability and sequence**, which is often the real reason for the change
  and is worth stating out loud.

### Step 5. Report

- Count of junction details now wrong, first.
- The control layer table, with any layer that moved relative to the insulation
  named.
- Drying direction, before and after.
- Whether any listing or test is invalidated.
- Every value missing from either version, counted.
- What has to be re-run: `condensation-check`, and `air-barrier-trace` if the
  air barrier plane moved.

Say plainly whether this is a change of build-up or a change of strategy. A
different insulation of the same thickness in the same place is the first. A
membrane on the other side of the sheathing is the second, and the second is
never a like-for-like substitution however it is presented.

### Step 6. Save, if asked

Ask whether to write the comparison to a file and where. Keep it where a
substitution was proposed; it is the record of what was accepted and why.

## Rules

- **Establish which version is earlier**, explicitly.
- Ask who proposed the change and why.
- Report the control layers' positions relative to the insulation, not just the
  layer list.
- **Report the count of junctions now wrong before anything else.**
- Say whether a listing or a tested assembly is invalidated.
- Say whether this is a build-up change or a strategy change.
- Never supply a value to complete a comparison.

## Anti-patterns

- Comparing the two lists and calling equal thicknesses equivalent.
- Missing that a layer moved relative to the insulation.
- Reviewing the section and not the junctions drawn against it.
- Accepting a manufacturer's standard detail as a like-for-like change.
- Treating a modified tested assembly as still tested.
- Reporting a drying rate.
- Assessing a change without the junction list and not saying so.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
