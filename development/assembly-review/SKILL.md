---
name: assembly-review
description: "Takes any envelope assembly you are handed — a wall, a roof, a floor, a below-grade construction, from a consultant, a contractor, a manufacturer or an earlier phase of your own project — and reads it for what it is trying to do and where it does not. Locates the four control layers, checks each is continuous through the stack and has somewhere to go at the edges, names every layer with no job, and reports which direction it can dry. Trigger on \"review this assembly\", \"is this wall build-up any good\", \"they sent us a section\", \"read this stack\", \"assembly-review\", or any layered construction handed over for an opinion. Carries no R-values, permeance figures or code minimums; every value comes with the assembly or is marked missing. The `design-` assembly skills build one from demands; this reads one that already exists. It runs no arithmetic — `condensation-check` does — and does not replace the enclosure consultant or the Architect of Record."
license: MIT
metadata:
  title: "Assembly Review"
  summary: "Read an assembly somebody else built up and say what it does not do"
  discipline: "envelope-performance"
  tags: "Review"
---

# Assembly Review

Assemblies arrive already built up: on a consultant's section, in a
manufacturer's detail, on a drawing from the last phase. The question is not
whether the layers are reasonable. It is what this stack is trying to do, and
which of those things it does not actually do.

## Scope and limits — read first

**What this does.** Reads any assembly you hand it. Works out what it is for,
locates the four control layers, checks each for continuity and for an exit at
the edges, finds the layers doing nothing, and reports the drying direction.

**What this does not do.**

- **It carries no values.** No R-values, no permeance, no thicknesses, no code
  minimums. Every figure comes with the assembly, and a layer with no figure is
  reported as unquantified rather than assumed.
- **It runs no arithmetic.** Boundary temperatures and the condensing plane are
  `condensation-check`'s, with values you supply.
- It does not build an assembly. The `design-` assembly skills do that from
  demands, and this reads one that exists.
- It does not audit continuity around the building. `air-barrier-trace` does.
- It does not review a submittal package. `submittal-review` and
  `curtain-wall-submittal-review` do.
- It does not replace the enclosure consultant or the Architect of Record.

**What you need before starting.** The assembly, layer by layer, in order, with
whatever values came with it. Where it is used and what is on each side. The
climate zone, if any judgement about drying is wanted. Who produced it.

## Workflow

### Step 1. Establish what it is and where it came from

Ask, in one message:

> 1. The layers in order, inside face to outside face, with any values given.
> 2. Where is this used, and what is on each side of it?
> 3. Who produced it: a consultant, a contractor, a manufacturer, a previous
>    phase, a standard detail?
> 4. What climate zone, and from what source?
> 5. Is it presented as tested or listed, and is the listing cited?
> 6. What is being asked: is it acceptable, or what is wrong with it?

**Question 3 changes what to look for.** A manufacturer's detail is drawn to
show their product working and the layers around it are decoration. A
contractor's proposed alternate is drawn to be buildable and cheap. A previous
phase's assembly is drawn to a brief that may have changed.

Read the order back, numbered, before anything else. An assembly given
outside-in produces a clean reading that is exactly backwards.

### Step 2. Say what the assembly is trying to do

Before finding faults, state the intent as the stack implies it. Then ask
whether that matches what it has to do here. Half the findings in a review of an
inherited assembly are not defects; they are an assembly built for a different
job.

### Step 3. Locate the four control layers

| Control layer | Which layer is it | Continuous? | Where does it go at the edges |
|---|---|---|---|

- **Water.** Which plane sheds bulk water, and does it drain or is it sealed?
- **Air.** Which plane stops air, is it continuous through the stack, and is it
  reachable to be sealed during construction?
- **Vapor.** Which is the lowest-perm layer, and which side of the insulation is
  it on?
- **Thermal.** Where is the insulation relative to the structure, and does
  anything cross it?

Where a layer cannot be identified, say so. **An assembly with no identifiable
air barrier is the most common finding** and it is usually not deliberate.

Note where one material is doing two of these jobs, and say that one failure
then takes out both.

### Step 4. Find the layers doing nothing

Go through the stack and ask what each layer is for. Report:

- Layers with no job that anyone can name.
- Layers duplicating another layer's job.
- Layers whose job depends on a value nobody supplied.
- Anything present because it was on the last project.

This is where cost sits in an inherited assembly, and it is also where a layer
turns out to be load-bearing for a reason nobody wrote down. Ask rather than
delete.

### Step 5. Say which way it dries, and what it cannot do

- Which direction can it dry, from where the low-perm layers sit? A direction,
  never a rate.
- Is it closed both ways, and if so is that deliberate?
- What does the assembly not address at all: thermal bridging at framing or
  penetrations, movement, fire, acoustics, buildability, maintenance.

State the last one plainly. A stack is a section through the middle of a wall
and the middle of a wall is not where walls fail.

### Step 6. Report

- What it appears to be for, and whether that matches the job here.
- The control layer table, with anything unidentifiable named first.
- Layers with no job, counted.
- The drying direction, and whether it is closed.
- Every value that came with the assembly and every one missing, counted.
- What this review did not cover, and the hand-offs: `condensation-check` for
  the arithmetic, `air-barrier-trace` for continuity around the building, the
  junction skills for the edges.

### Step 7. Save, if asked

Ask whether to write the review to a file and where.

## Rules

- **Never supply a value.** Missing is reported as missing.
- Read the layer order back before reviewing.
- Ask who produced it, and read it accordingly.
- State what the assembly is for before finding faults.
- Name any control layer that cannot be identified.
- Ask before calling a layer unnecessary.
- Say on every run that the middle of a wall is not where walls fail.

## Anti-patterns

- Reviewing an assembly given outside-in as though it were inside-out.
- Treating a manufacturer's detail as a design.
- Listing faults without saying what the assembly was for.
- Assuming an R-value or a permeance to complete the picture.
- Deleting a layer nobody can explain rather than asking.
- Reporting a drying rate.
- Reviewing the section and never mentioning the edges.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
