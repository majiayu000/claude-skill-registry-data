---
name: view-analysis
description: "Works views in both directions, because a window is two things at once: what a room looks at, and what looks back into it. Establishes what is worth seeing and whether it will still be there, what each room needs to see and what it must not, where privacy runs both ways between this building and its neighbours, and which views depend on land somebody else owns. Trigger on \"view analysis\", \"what does this room look at\", \"will we still have this view\", \"overlooking\", \"privacy from the neighbours\", \"view-analysis\", or a scheme where the windows have been placed by elevation rather than by what they see. Carries no angles, no distances and no separation requirements; overlooking rules are local text you quote and sun angles come from `shadow-study`. It does not model and does not replace the Architect of Record."
license: MIT
metadata:
  title: "View Analysis"
  summary: "Work out what each room sees, and what protects it"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# View Analysis

Windows get placed by the elevation and justified by the view afterwards. Two
things go wrong: the view turns out to belong to somebody who is about to build
on it, and the window that frames it also lets the neighbour look in.

A view is never one-directional and it is rarely permanent.

## Scope and limits — read first

**What this does.** Works each significant opening in both directions: what it
sees and what sees it. Establishes which views are protected and which are
borrowed from land somebody else controls. Names where privacy has to be
resolved and by what.

**What this does not do.**

- **It carries no angles, distances or requirements.** Overlooking separation,
  privacy distances and window-to-boundary rules are local text you quote, and
  they vary widely.
- It does not do sun. `shadow-study` computes sun angles and shadow reach, and
  `daylight-study` how far light reaches in. This is about what you see.
- It does not model or render.
- It does not establish what the neighbours can build. That is zoning, and it
  comes from `zoning-summary` or `/test-far` applied to their parcel.
- It does not resolve an objection. Point at `entitlement-tracker` where
  approval is discretionary.
- It does not replace the Architect of Record.

**What you need before starting.** The scheme and the site. What surrounds it,
including what could be built there. Who is in each room and what they are
doing. The local rules on overlooking, if they exist.

## Workflow

### Step 1. Establish what is worth seeing, and whether it lasts

Ask, in one message:

> 1. What is worth seeing from this site, in which direction, and from what
>    height? A view available from the second floor and not the first is a
>    massing decision.
> 2. **What is between here and it, and who owns that?** For each, what could be
>    built there under the zoning that applies to it?
> 3. What is not worth seeing: a blank wall, a yard, a road, a parking lot, a
>    neighbour's window?
> 4. Who is in each room, doing what, and at what times?
> 5. Are there local rules on overlooking or privacy separation? Quote them.
> 6. Is anything protected: a designated view, a viewshed, a right to light?

**Question 2 is the one that gets skipped.** A view over a low neighbouring
building is a view until that building is replaced, and the zoning on their
parcel says what replaces it. A scheme whose main rooms all face a view that can
legally be built out has a problem nobody has priced.

Mark every view as **protected** (a park, water, a designated viewshed, a
distance too far to build out) or **borrowed** (it depends on somebody not
building). Report the count.

### Step 2. Work each room outward: what it needs to see

| Room | Wants to see | Must see | Must not see | Direction |
|---|---|---|---|---|

`Must see` is a real category and it is not about pleasure: a reception that has
to see the door, a kitchen that has to see the garden where children are, a
nurse station that has to see a corridor, a workshop that has to see the yard.
These are functional and they beat the view.

`Must not see` is equally real: a bedroom that should not look at a parking
area, a waiting room that should not see a treatment room, a dining room that
should not look at the bins.

### Step 3. Work each opening inward: what sees it

The half that is usually missing. For every significant opening:

| Opening | Seen from | Distance | At what times | Resolved by |
|---|---|---|---|---|

- The neighbour's windows, existing and possible.
- The street, the sidewalk, and anywhere the public stands or waits.
- Higher ground, and taller buildings nearby.
- The building's own other rooms across a courtyard or a return, which is the
  overlooking people forget because it is theirs.

Then say what resolves each: distance, an angle, a level change, planting that
takes years, a screen, obscured glazing, a sill height, or accepting it.

**Say plainly where the resolution is planting.** It works eventually and it does
not work at handover, and somebody has to maintain it.

### Step 4. Work the reciprocal cases

The ones where both sides are affected and only one is usually drawn:

- Where this building overlooks a neighbour, and what the local rules say.
- Where a neighbour overlooks this building.
- Where two parts of this building overlook each other.
- Where a terrace or balcony overlooks something a window would not. **An
  outdoor space overlooks far more than a window** because people stand and look
  around in it, and this is the most common objection to a balcony. Point at
  `design-balcony`.
- Where a view from a lower floor is fine and from an upper floor is not.

### Step 5. Report

- Protected views against borrowed views, counted, with what each borrowed view
  depends on.
- Every room whose `must see` or `must not see` is unresolved.
- Every opening with an unresolved overlooking condition, and what would resolve
  it.
- Every resolution that depends on planting or on a neighbour not building.
- What the neighbours are likely to raise, if approval is discretionary.
- What was assumed about what could be built nearby, and whether anyone checked.

Close by saying nothing was modelled and that the zoning on neighbouring parcels
was assumed unless checked.

### Step 6. Save, if asked

Ask whether to write the analysis to a file and where.

## Rules

- **Work every opening in both directions**, every run.
- Mark every view protected or borrowed, and say what each borrowed one depends
  on.
- Check what could be built on the land the view crosses.
- Treat outdoor space as overlooking more than a window does.
- Say when a resolution depends on planting, and that it takes years.
- Never quote an overlooking distance from memory.

## Anti-patterns

- Placing windows on the elevation and describing the view afterwards.
- Treating a view over a neighbouring site as permanent.
- Working what rooms see and not what sees them.
- Forgetting that the building overlooks itself across a courtyard.
- Resolving privacy with planting and drawing it mature.
- Ignoring the balcony, which overlooks more than any window on the same wall.
- Recalling a privacy separation distance.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
