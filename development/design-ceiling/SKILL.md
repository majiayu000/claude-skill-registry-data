---
name: design-ceiling
description: "Works the ceiling as the place every discipline's leftovers land: adds up what has to fit in the plenum in the order it gets installed, finds the one crossing that sets the height for the whole floor, and works access, transitions and the elements that arrive late and wreck a reflected ceiling plan. Reports the height available against the height wanted. Trigger on \"ceiling height\", \"what fits in the plenum\", \"reflected ceiling plan\", \"will the duct clear the beam\", \"ceiling access\", \"design-ceiling\", or a floor-to-floor with a question about what it leaves. Carries no depths, no clearances and no code requirements; structural depths come from the engineer, service sizes from the MEP set, and required heights from the code you quote. It does not size services or structure and does not replace the engineers or the Architect of Record."
license: MIT
metadata:
  title: "Design Ceiling"
  summary: "Set the ceiling height by what has to fit above it"
  discipline: "structure-mep"
  tags: "Design"
---

# Design Ceiling

Ceiling height is presented as a design decision and it is arithmetic. The
floor-to-floor is fixed, the structure takes what it takes, the services take
what they take, and the ceiling gets what is left. The useful work is finding
the one crossing that governs, because it usually sets the height everywhere and
it is usually in a corridor nobody drew a section through.

## Scope and limits — read first

**What this does.** Adds up the plenum from the values you supply, finds the
governing crossing, and works access, transitions and the late arrivals. Reports
the height available against the height wanted, room by room.

**What this does not do.**

- **It carries no dimensions.** No structural depth, no duct size, no clearance,
  no minimum ceiling height, no hanger allowance. Structure from the engineer,
  services from the MEP set, required heights from the code you quote.
- **It sizes nothing.** Not a duct, not a beam. It holds space for what others
  give you.
- It does not review the MEP set. `mep-review` reads that set for its own
  conflicts, and this takes its output as input.
- It does not do the acoustic design of the ceiling.
  `design-acoustic-separation` works the plenum as a path.
- It does not select a ceiling system or resolve its appearance.
- It does not replace the engineers or the Architect of Record.

**What you need before starting.** Floor-to-floor. The structure and its depths,
with the direction it spans. The services and their sizes, with insulation. The
required or wanted ceiling height per room, and what sets it. The MEP set if it
exists.

## Workflow

### Step 1. Establish the givens

Ask, in one message:

> 1. Floor-to-floor, and is it the same everywhere?
> 2. The structure: what, how deep, spanning which way, and where are the deep
>    members? Point at `structural-drawing-review`.
> 3. What services are in the plenum, at what size including insulation, and is
>    there an MEP set?
> 4. What ceiling height does each room want, and what sets it: the code, the
>    brief, the use, a datum, a window head?
> 5. What ceiling system is intended, and what depth does it need for itself?
> 6. Is there a raised floor or a floor build-up eating the same dimension?

### Step 2. Add up the plenum in the order things are installed

Not a total. A stack, in installation order, because each layer has to get past
the ones already there:

```
underside of structure
  + structure depth at this location
  + what hangs from it first
  + the deepest service crossing here
  + what crosses that
  + hanger and support space
  + the ceiling system's own depth
= underside of ceiling
```

Show it with the source beside every term. Anything without a source is `not
supplied` and never a typical figure.

State plainly that services cross each other, and that two services that fit
individually may not fit where they cross.

### Step 3. Find the governing crossing

The floor's ceiling height is set by one place, and it is rarely the room
anybody sectioned:

- Where the main duct run crosses the deepest beam.
- Where several services converge: outside a plant room, at a riser, at a
  corridor junction.
- Where the structure changes depth or direction.
- At a transfer, where a beam is much deeper than the rest.
- Where a service has to fall for gravity and its lowest point is at the far
  end of a run.

Report the governing location by name, with the arithmetic. Then say what the
height would be without it, because that number is the argument for rerouting
one service rather than dropping the whole floor.

### Step 4. Work access, which is decided by the ceiling type

- What has to be reached above the ceiling: dampers, valves, VAV boxes,
  junction boxes, isolation, cleanouts. Ask the MEP set and list them.
- Whether the ceiling type gives access anywhere or only at panels, and where
  panels would land in the reflected ceiling plan.
- Whether anything needing regular access sits above a hard ceiling, which is
  the finding that comes back during commissioning.
- Whether access panels can be reached from a ladder or need equipment.

### Step 5. Work the transitions and the late arrivals

**Transitions.** Where the ceiling changes height, changes system, meets a wall,
meets the facade, or steps around a beam. Every change is a detail and a cost,
and a reflected ceiling plan with many is a plan that was drawn to avoid one
decision.

**Late arrivals.** The elements that appear after the reflected ceiling plan is
coordinated and wreck it. Name each and ask whether it is located yet:

- Sprinkler heads, which have their own spacing rules and land on the grid or
  do not.
- Emergency and exit lighting, added by a different discipline.
- Smoke detectors and speakers.
- Diffusers and returns.
- Access panels from Step 4.
- Structural bracing, seismic or lateral, added late.
- Window blind pockets and their recesses.

### Step 6. Report

| Room | Height wanted | Height available | Difference | Governed by |
|---|---|---|---|---|

Then:

- The governing crossing, named, with the height that would be available
  without it.
- Every `not supplied` dimension, counted, with who supplies it.
- Everything needing access that currently sits above a hard ceiling.
- The late-arrival list, marked located or not.
- What has to reach the engineers: a reroute request, a beam that needs
  penetrating, a transfer that needs looking at again.

Then ask whether to write the take-off to a file and where.

## Rules

- **Never supply a depth, a clearance, or a required height.**
- Add the plenum in installation order, not as a sum.
- Name the governing crossing and what the height would be without it.
- List everything requiring access and check it against the ceiling type.
- Ask about the late arrivals, every run, before the plan is called coordinated.
- Never size a service or a structural member.

## Anti-patterns

- Setting the ceiling height in the room that was sectioned.
- Totalling the services rather than stacking them in installation order.
- Recalling a typical plenum depth or a duct size.
- Coordinating the reflected ceiling plan before sprinklers and emergency
  lighting are located.
- Putting a damper above a hard ceiling.
- Dropping the whole floor for one crossing without asking whether that service
  can move.
- Ignoring the floor build-up, which competes for the same dimension.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
