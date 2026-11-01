---
name: area-measurement
description: "Settles the question every project answers three times and differently: which area standard is being used, where its boundary is drawn, and what counts toward it. A building has a zoning floor area, a code floor area, a gross and a net for programming, and a leasable area, and each is measured by a different rule from a different document. Records one basis per purpose with its source, reconciles the figures that result, and reports the difference rather than resolving it into one number. Trigger on \"which area standard\", \"gross versus net\", \"what counts as floor area here\", \"our areas do not match the lease\", \"BOMA measurement\", \"area-measurement\", or two area figures that disagree. Carries no standards, no definitions and no factors; each comes from the document you quote. It measures nothing itself and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Area Measurement"
  summary: "Establish which area standard governs and what actually counts in it"
  discipline: "design-building-types"
  tags: "Analysis"
---

# Area Measurement

Every project carries several area figures that were measured differently, and
almost nobody writes down which rule produced which number. The programme says
one thing, the zoning submission another, the lease a third, and each is
correct. The problem appears when two of them are compared.

## Scope and limits — read first

**What this does.** Establishes, for each purpose the project has, which standard
governs, where the boundary is drawn, and what is included and excluded. Records
them side by side and reconciles the resulting figures so the differences are
explained rather than argued about.

**What this does not do.**

- **It carries no standards and no definitions.** Which document governs, and
  what its text says counts, comes from you: the zoning ordinance, the building
  code, the measurement standard the lease names, the client's own brief. These
  differ between jurisdictions, between editions, and between standards.
- **It measures nothing.** It does not take areas off a drawing or a model. You
  supply the figures; it establishes what rule each was produced under.
- It does not track the programme. `space-program` does, and this establishes
  the basis that programme is measured on.
- It does not do the zoning arithmetic. `/test-far` does, against the
  jurisdiction's own text.
- It does not resolve which figure is right. They can all be right.
- It does not replace the Architect of Record.

**What you need before starting.** The purposes the project measures for. For
each, the governing document, quoted where it defines the measurement. The
figures you already have and where each came from. The drawings or the model
they were taken from, and by whom.

## Workflow

### Step 1. List the purposes before any number

Ask, in one message:

> 1. What does this project measure area for? Work through: zoning submission,
>    building code (allowable area, occupant load), the client's programme,
>    a lease or sale, a fee based on area, a certification, a cost plan, a
>    facilities or asset record.
> 2. For each, what document governs the measurement, and can you quote where it
>    defines it?
> 3. What figures exist today, who produced each, from what drawing or model,
>    and on what date?
> 4. Is anything already committed: a lease signed, a submission made, a fee
>    agreed on an area?

**Question 4 changes the exercise.** Where a figure has already been relied on,
the job is to explain the difference rather than to correct it, and to find out
who has to be told.

### Step 2. Record one basis per purpose

One row per purpose. Every cell comes from a quoted document or is marked open.

| Purpose | Standard | Boundary | Included | Excluded | Source quoted |
|---|---|---|---|---|---|

`Boundary` is the cell that produces most of the disagreement: measured to the
outside face, to the centreline, to the inside face, or to a dominant portion.
Two figures produced to different boundaries will never reconcile and the
difference is not an error.

Work `Included` and `Excluded` explicitly rather than assuming. The items that
differ between standards, and which one to ask about every time:

- Shafts, stairs, and lift wells, and whether they count on every floor or once.
- Structure: columns, walls, and which side of them.
- Mechanical space, plant rooms and rooftop enclosures.
- Parking, whether structured, below grade, or at grade.
- Covered but unenclosed area: balconies, terraces, arcades, porte cochères.
- Mezzanines, and at what ceiling height they begin to count.
- Basement and below-grade space, often the largest single difference.
- Space below a stated headroom.
- Interstitial and service floors.
- Loading, refuse and utility rooms.

### Step 3. Reconcile the figures

Take the figures you were given and set them against the bases:

| Figure | Purpose | Basis it was measured on | Confirmed? |
|---|---|---|---|

`Confirmed?` asks whether anyone verified the figure was actually produced under
the basis it is attributed to. Usually nobody did, and a figure inherited from an
earlier phase is often on a basis nobody recorded.

Then, for each pair that people compare, show the difference and account for it
item by item:

```
<purpose A>   <figure>
<purpose B>   <figure>
difference    <figure>
accounted for by:   <item>  <item>  <item>
unaccounted:        <figure>
```

**The unaccounted line is the finding.** A difference fully accounted for by
known exclusions is not a problem. An unaccounted remainder means one figure is
wrong, or was measured on a basis nobody recorded.

### Step 4. Name what depends on each figure

For each purpose, record what is riding on it: a submission already made, a
lease, a fee, an allowable area calculation, a certification. Then say what
would have to happen if that figure moved.

This is what turns a measurement exercise into a decision. A programme area that
drifts is a conversation; a leased area that drifts is an amendment.

### Step 5. Report

- The basis table, with every cell that was assumed rather than quoted, counted.
- The reconciliation, with the unaccounted remainder for each pair compared.
- Every figure whose basis nobody confirmed.
- Every committed figure and what depends on it.
- What to quote and from where, for the bases still open.

Close by saying that nothing was measured here, and that several figures being
different is the normal condition rather than an error.

### Step 6. Save

Ask where. One file per project, and revisit it whenever a new figure appears,
because the point is that the bases stay written down.

## Rules

- **Never supply a standard, a definition, an exclusion, or a factor.**
- One basis per purpose, and every basis names its source or is marked open.
- Record the boundary explicitly for every basis.
- Never reconcile two figures into one. Explain the difference and report the
  unaccounted remainder.
- Ask, for every basis, about the items in Step 2 rather than assuming.
- Name what is committed and what would move if a figure did.
- Say on every run that nothing was measured here.

## Anti-patterns

- Producing one area for the project.
- Assuming a standard's exclusions from what is usual.
- Comparing a figure from the programme against one from the lease without
  asking what boundary each used.
- Treating an unaccounted difference as a rounding error.
- Inheriting a figure from an earlier phase without recording its basis.
- Recalling whether a jurisdiction counts below-grade area.
- Correcting a committed figure without naming who has to be told.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
