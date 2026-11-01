---
name: stacking-diagram
description: "Distributes a programme vertically against the constraints that actually decide it: the floor plate you have, the core capacity, the loads and heights each use demands, and the ground-level frontage everything competes for. Places the uses that cannot move first, then works down the list, and reports every floor where the programme assigned exceeds what the plate can hold. Trigger on \"stacking diagram\", \"stack the programme\", \"which floor does this go on\", \"vertical zoning\", \"how many floors do we need\", \"stacking-diagram\", or a programme and a floor plate handed over with a request for how it distributes. Carries no areas, no floor-to-floor dimensions, no lift capacities and no loading figures; every one comes from you or from `space-program`, `design-core` and `test-fit`. It does not size the core, does not lay out a floor and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Stacking Diagram"
  summary: "Stack the programme against what the floor plate and the core will actually take"
  discipline: "design-building-types"
  tags: "Design"
---

# Stacking Diagram

Stacking looks like sorting a list into floors and it is not. The programme
competes for three scarce things — ground-level frontage, core capacity, and the
floors that can take the load or the height — and a stack that ignores those
produces a diagram that survives until the first section is drawn.

## Scope and limits — read first

**What this does.** Establishes what cannot move before distributing anything
else, works the programme down against the plate, and reports where the stack
does not close: floors over capacity, uses that need a plate this building does
not have, and demand on the core beyond what it was sized for.

**What this does not do.**

- **It carries no numbers.** No areas, no efficiency ratios, no floor-to-floor
  heights, no live loads, no lift capacities, no travel times. They come from
  you, from `space-program` for the areas, from `design-core` for the core, from
  `test-fit` for what the site takes.
- It does not size the core. `design-core` does, and this reports demand against
  whatever that established.
- It does not lay out a floor. Stacking is which floor; `test-fit` and the plan
  are what fits on it.
- It does not check code. Occupancy separations, allowable area by storey,
  egress from each level, and construction type limits all bear on a stack and
  none of them are here. `senior-code-consultant` and `design-egress` take them.
- It does not do structure. Transfer structure where a stack changes column grid
  between uses is engineering and it is expensive; the stack names where it
  would be needed.
- It does not replace the Architect of Record.

**What you need before starting.** The programme with areas. The floor plate,
its dimensions and its usable area per floor. The core, or the fact that it is
not yet fixed. Site constraints: frontage, access, levels, what the ground floor
has to give up to servicing. Any use with a fixed floor-to-floor, load, or
adjacency to the ground.

## Workflow

### Step 1. Take the programme and the plate

Ask, in one message:

> 1. The programme with areas. Point at `space-program` if it is running.
> 2. The floor plate: dimensions, usable area per floor, and whether every floor
>    is the same. Say if the plate is not fixed.
> 3. The core: its position and capacity, or that `design-core` has not run.
> 4. What the ground floor has to accommodate that no other floor can: entrance,
>    loading, plant intake, retail frontage, drop-off.
> 5. Which uses have a fixed floor-to-floor, a load beyond office loading, or a
>    requirement to be at or near grade?
> 6. Is the number of storeys fixed by something outside the programme: a height
>    limit, a datum, a planning constraint?

### Step 2. Place what cannot move, before anything else

Work in this order, because each one removes options for the rest:

1. **Ground level.** Everything that must touch grade competes here, and the
   competition is the hardest decision in most stacks. List what wants it,
   list what actually needs it, and say what gets displaced.
2. **Plant and servicing.** Where it goes, and whether it takes a floor, a roof,
   a basement, or parts of several. It also takes riser space out of every floor
   it passes.
3. **Uses with a plate this building only has in places.** A use needing a
   deeper or shallower plate, more height, or a heavier load can only sit where
   the building offers it.
4. **Uses with an external requirement.** Daylight, outlook, a terrace, a
   separate entrance, a security separation, an operational shift pattern.

Everything not placed by these four is genuinely free, and there is usually less
of it than expected.

### Step 3. Distribute the rest, and hold each floor to the plate

| Floor | Use | Area assigned | Usable area | Over or under | Core demand | Note |
|---|---|---|---|---|---|---|

Work down or up, whichever the fixed items suggest. For each floor:

- Compare area assigned against usable area, and report the difference. Never
  round a use to fit a floor.
- Note what the assignment does to the core: lift demand, riser demand, egress
  demand.
- Note where two uses share a floor and what separates them.

### Step 4. Read the stack for what does not close

- **Floors over capacity.** Listed with the overage.
- **Uses split across floors** that were not intended to be, and whether the
  split is workable.
- **Core demand** against what `design-core` established, or the statement that
  it has not been established.
- **Transfer structure.** Any point where the stack changes the column grid or
  the plate between floors. Flag each; these are the most expensive consequences
  of a stacking decision and they are invisible in the diagram.
- **Ground-level losers.** What wanted grade and did not get it, and what that
  costs the operation.
- **Adjacencies broken.** Any `required` adjacency from `adjacency-matrix` that
  the stack has put on different floors. A vertical adjacency is not the same as
  a horizontal one and the matrix does not distinguish them.

### Step 5. Report

The stack table, the six readings, then:

- Total programme area against total usable area, as two figures, never as a
  ratio unless you supplied the efficiency assumption.
- Every figure that came from an assumption rather than from a source, counted.
- What has to be checked elsewhere: code, structure, core sizing.

### Step 6. Save, if asked

Ask whether to write the stack to a file and where.

## Rules

- **Never supply an area, a height, a load, or a lift capacity.**
- Place the immovable before distributing the movable, every run.
- Never round a use to fit a floor. Report the overage.
- Flag every transfer structure the stack implies.
- Check the stack against `adjacency-matrix` requirements where one exists.
- Say what has to be checked for code and structure, and do not check it here.

## Anti-patterns

- Sorting the programme into floors and calling it a stack.
- Assuming an efficiency ratio to make the areas close.
- Putting plant on the roof without asking what the risers take from each floor.
- Ignoring what the ground floor gives up to servicing.
- Changing the plate between floors without flagging the transfer.
- Treating a required adjacency as satisfied because the two rooms are on
  adjacent floors.
- Producing a stack when the plate is not fixed, without saying it is
  provisional.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
