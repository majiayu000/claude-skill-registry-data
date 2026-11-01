---
name: fit-out-study
description: "Tests whether a tenancy works in a shell that is already there, which is a different problem from fitting a building on a site: the grid, the core, the servicing and the base building's own rules are fixed, and the programme has to bend around them. Establishes what is actually immovable before laying anything out, works the programme against the fixed points, and separates what the landlord provides from what the tenant does, since that boundary decides the budget and it is in a document nobody has read. Trigger on \"fit out\", \"will this programme fit in this space\", \"tenant improvement\", \"test fit for a lease\", \"is this floor plate any good for us\", \"fit-out-study\", or a floor plan of an existing building with a programme to place in it. Carries no areas, no ratios and no code requirements; areas come from the user and the lease's measurement basis from `area-measurement`. `test-fit` works a site under zoning limits; this works a shell under a lease. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Fit-Out Study"
  summary: "Fit a programme into a shell somebody else built"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# Fit-Out Study

Fitting a programme into an existing shell is not the same exercise as fitting a
building on a site. On a site most things are still negotiable. In a shell the
grid, the core, the risers, the window line and the base building's own rules
are already decided by somebody who was not thinking about this tenant, and the
programme is the only thing that can move.

## Scope and limits — read first

**What this does.** Establishes what is genuinely fixed in the shell before any
layout, tests the programme against those fixed points, and separates the
landlord's scope from the tenant's, which is where fit-out budgets are won and
lost.

**What this does not do.**

- **It carries no areas, ratios or requirements.** Programme areas come from
  you or from `space-program`; the lease's measurement basis from
  `area-measurement`; code from the jurisdiction.
- **It is not `test-fit`.** That works a site against zoning limits. This works a
  shell against a lease and a base building.
- It does not read the lease. It says which parts of it decide the design and
  have to be read, by you or by an attorney.
- It does not do the code analysis for a change of occupancy, which a fit-out
  frequently is. Point at `senior-code-consultant` and `design-egress`.
- It does not do interiors. `interior-architect` and `design-partition` follow.
- It does not replace the Architect of Record.

**What you need before starting.** The shell drawings, and how reliable they
are. The programme with areas. The lease or the offer, or the fact that it is
not signed. The base building's rules, if the landlord has issued any. Whether
this is a study to decide on a space, or a design for one already taken.

## Workflow

### Step 1. Establish which question is being asked

Ask, in one message:

> 1. Is this to decide whether to take the space, or to design one already
>    taken? Completely different exercises with the same drawings.
> 2. What is the programme, with areas, and where did the areas come from?
> 3. What shell information exists, and is it the landlord's marketing plan or a
>    measured survey? Point at `existing-conditions-survey`.
> 4. Is there a lease or an offer? What does it say about the measurement basis,
>    the landlord's work, the tenant allowance, and the make-good at the end?
> 5. Has the landlord issued base building rules, tenant criteria, or a design
>    guide?
> 6. Is the use changing from what the space was last used for?

**Question 1 changes everything.** A study to decide on a space should be fast,
should test the hard constraints, and should say plainly whether it fits with
room to be wrong. A design for a space already taken has to make it work.

### Step 2. Establish what is actually fixed, before laying anything out

Three categories, and people routinely put things in the wrong one:

| Element | Fixed | Movable at a cost | Negotiable with the landlord |
|---|---|---|---|

Work through: the structural grid and column locations, the core and its
position on the plate, the window line and the mullion module, the floor-to-
floor and the slab-to-slab, the risers and where services come from, the
sprinkler and life-safety systems, existing washrooms, the demising walls, the
floor loading, the ceiling height available, and where the tenancy's entrance is.

**The third column is worth asking about.** Tenants assume the shell is fixed;
a landlord with a vacancy will move a demising wall, add a riser, or upgrade a
service. Nobody finds out unless somebody asks.

### Step 3. Test the programme against the fixed points, in order

Place in this order, because each one removes options for the rest:

1. **What must be at the window**, and how much window line there is. This is
   the scarcest thing in most shells and the one most fought over internally.
2. **What must be near the core**, and what the core's position does to the
   plan. A core in the middle and a core at one end give completely different
   layouts of the same area.
3. **What needs services**: anything wet, anything with heat load, anything with
   exhaust. Each has to reach a riser and the routes are fixed.
4. **What needs to be separated**: acoustically, for security, for confidentiality.
   Point at `design-acoustic-separation`.
5. **Everything else**, which is usually most of the area and is genuinely free.

For each, report whether it lands, and against what constraint if not.

### Step 4. Work the ratio the shell actually gives

Report as three figures, never as one:

```
area leased        <on the lease's basis, from area-measurement>
area usable        <what the plan can actually occupy>
area programmed    <what the programme needs>
```

Then account for the difference between the first two: the core, the columns,
the structure, the corridor the code requires, the plan's own inefficiency at
this shape. **A shell's usable proportion is a property of the shell and it
varies more than anyone expects.** Point at `area-measurement`, because the
lease and the programme are almost certainly on different bases.

If the programme does not fit, say by how much and against which constraint,
and do not shrink the programme to make it land.

### Step 5. Separate landlord's work from tenant's work

The boundary that decides the budget, and it is in a document nobody has read:

| Item | Landlord provides | Tenant provides | Where it says so |
|---|---|---|---|

Work through the items that are always ambiguous: the ceiling, the lighting,
the sprinkler drops and their relocation, the HVAC distribution beyond the main
plant, the floor finish and levelling, the demising walls and which side is
finished, the electrical distribution and the panel, the washrooms, the entrance
door and the signage, and the make-good obligation at the end of the term.

Anything with no source cited is a question for the lease or the landlord, and
it goes on the list rather than being assumed either way.

**The make-good obligation is a design decision made now.** A fit-out that has
to be stripped back at the end of the term costs more than one that does not,
and nobody thinks about it while signing.

### Step 6. Report

- Fits or does not fit, with the shortfall against a named constraint.
- The three area figures and what accounts for the gaps.
- The fixed / movable / negotiable table, with the negotiable items listed for
  the landlord conversation.
- The landlord-versus-tenant table, with every unsourced item flagged.
- What the change of use triggers, if any, named as a question for the code
  consultant.
- What is provisional because the shell information is marketing rather than
  measured.

### Step 7. Save, if asked

Ask whether to write the study to a file and where.

## Rules

- **Ask first whether this decides on a space or designs one.**
- **Never supply an area, a ratio, or an efficiency figure.**
- Sort every shell element into fixed, movable at a cost, or negotiable, and ask
  about the third.
- Report leased, usable and programmed as three figures. Never one.
- Never shrink the programme to make it fit. Report the shortfall.
- Every landlord-versus-tenant item cites where it says so, or is flagged.
- Name the make-good obligation, every run.

## Anti-patterns

- Treating a landlord's marketing plan as a measured survey.
- Assuming everything in the shell is fixed without asking.
- Comparing the leased area against the programme area without checking they are
  on the same basis.
- Reporting one efficiency percentage.
- Shrinking the programme quietly so the study concludes that it fits.
- Assuming the landlord provides the ceiling, the lighting, or the sprinkler
  relocation.
- Designing a fit-out with no thought to what has to be removed at the end.
- Missing that a fit-out is often a change of occupancy.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
