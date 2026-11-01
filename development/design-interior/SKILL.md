---
name: design-interior
description: "The door into interior work, and the step that is usually missing: before partitions, ceilings, millwork or finishes are drawn, establish what each space actually has to withstand, where the money should go, which spaces repeat and which get attention, and what the base building has already decided. Produces the strategy the specific skills then execute against, and hands each part off by name. Trigger on \"design the interior\", \"interior strategy\", \"where do we spend on this fit-out\", \"what finishes for this project\", \"the interior feels arbitrary\", \"design-interior\", or an interior scope with no strategy behind it. Carries no finishes, no specifications, no costs and no ratings; every requirement comes from the brief, the client's operation, or the code you quote. It details nothing itself — `design-partition`, `design-ceiling`, `design-millwork` and `schedule-builder` do that — and does not replace the interior designer or the Architect of Record."
license: MIT
metadata:
  title: "Design Interior"
  summary: "Decide what the interior has to do before detailing any part of it"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Interior

Interiors get drawn part by part: partitions from a legend, a ceiling grid,
millwork when the joiner asks, finishes from a schedule filled in at the end.
Each part can be competent and the interior still reads as arbitrary, because
nobody said what it was supposed to do.

This is the step before those. It is deliberately broad, and it does one thing:
it settles the demands so the specific skills have something to work against.

## Scope and limits — read first

**What this does.** Establishes what each kind of space has to withstand, where
the budget should concentrate, which spaces repeat and which are singular, and
what the base building has already fixed. Then hands every part of the work to
the skill that does it.

**What this does not do.**

- **It details nothing.** Partitions are `design-partition`, ceilings
  `design-ceiling`, joinery `design-millwork`, schedules `schedule-builder`,
  acoustic separation `design-acoustic-separation`, lighting
  `senior-lighting-consultant`. This produces what each of them needs to be
  told.
- **It carries no finishes, ratings, costs or specifications.** Requirements
  come from the brief, the client's operation, and the code you quote.
- It does not select products or name manufacturers.
- It does not lay out the plan. `test-fit`, `fit-out-study` and
  `adjacency-matrix` do.
- It does not critique. `design-critic` and `interior-architect` do.
- It does not replace the interior designer or the Architect of Record.

**What you need before starting.** The plan, at whatever stage. Who uses each
space and how hard. The budget, or the fact that there is not one yet. The base
building's constraints if this is a fit-out. Anything the client has already
decided or already owns.

## Workflow

### Step 1. Take the operation, not the taste

Ask, in one message:

> 1. Who is in each kind of space, how many, how often, and doing what?
> 2. What happens to these surfaces: trolleys, chairs, water, grease, chemicals,
>    children, shoes, bicycles, animals?
> 3. Who cleans it, how often, with what, and can they reach everything?
> 4. How long is this expected to last before it is redone? A five-year fit-out
>    and a thirty-year institution are different buildings with the same plan.
> 5. What is the budget, and has anyone said where it should concentrate?
> 6. What is fixed already: the base building, an existing element, something
>    the client owns or has chosen?
> 7. Is there a brand, a house standard, or a previous project this has to sit
>    beside?

**Question 3 is the one nobody asks** and it decides more of the specification
than any other. A finish that cannot be cleaned by the person who actually
cleans it fails within a year, and no drawing shows that.

### Step 2. Group the spaces by demand, not by name

Not room by room. By what the space has to withstand:

| Group | Rooms in it | Wear | Acoustic | Cleanability | Privacy | Life |
|---|---|---|---|---|---|---|

Most projects have three or four groups and thirty rooms. Working by group is
what makes the interior coherent, and working room by room is what makes it
arbitrary.

For each demand, record where the requirement came from: the operation, the
brief, the code, or an assumption. Assumptions get counted.

### Step 3. Decide where the money goes, out loud

The decision that is otherwise made by attrition, at the end, by whatever
survives the last cut:

| Where | Why it earns it | What pays for it |
|---|---|---|

State it as a trade, always. Money spent on the entrance is money not spent on
the back corridor, and saying so is what makes it a decision rather than a
drift. Point at `budget-reconciliation` when the number is already short.

Two things worth deciding here rather than later:

- **What repeats and what is singular.** A repeating standard, done well and
  once, buys the attention for the two or three spaces that carry the project.
  An interior where everything is special is an interior where nothing is.
- **What is buried and what is replaceable.** Money in something that has to be
  demolished to change is a longer commitment than money in something that gets
  swapped.

### Step 4. Establish what the base building already decided

If this is a fit-out or a renovation, much of the interior is not a choice.
Point at `fit-out-study` and `existing-conditions-survey`, and record here what
they found that constrains the interior specifically:

- Floor-to-floor and what the ceiling can be. Point at `design-ceiling`.
- Where structure lands, and what cannot be moved or covered.
- What the servicing forces: diffuser positions, sprinkler heads, riser
  locations, panel locations.
- What the landlord requires or provides.
- The level of the existing floor, which is never flat.

### Step 5. Work the four constants across every group

Every interior decision is one of these, and each has a skill:

| Constant | Question | Skill |
|---|---|---|
| Enclosure | What separates the spaces, and how far up | `design-partition` |
| Overhead | What the ceiling is and what is above it | `design-ceiling` |
| Fitted | What is built in rather than bought | `design-millwork` |
| Surface | What the floors, walls and ceilings are | `schedule-builder` |

For each group from Step 2, state the demand each constant has to meet. Do not
answer it here. The answer is the specific skill's, and the point of this step
is that it arrives with a brief instead of a blank.

Then the two that cut across all four: acoustic separation
(`design-acoustic-separation`) and light (`senior-lighting-consultant`,
`daylight-study`).

### Step 6. Report and hand off

- The space groups with their demands, and how many demands are assumptions.
- Where the money concentrates, and what pays for it.
- What repeats and what is singular.
- What the base building already decided.
- A hand-off list: for each of the four constants, which skill takes it and what
  it has been told.
- What has not been decided and who decides it.

Close by saying nothing was detailed and nothing was specified here.

### Step 7. Save, if asked

Ask whether to write the strategy to a file and where. It is read back every
time one of the specific skills runs.

## Rules

- **Detail nothing.** Every specific decision names the skill that owns it.
- **Never supply a finish, a rating, a cost, or a product.**
- Group by demand, never room by room.
- Ask who cleans it, every run.
- State where the money concentrates as a trade, with what pays for it.
- Record where every requirement came from, and count the assumptions.
- Say what the base building already decided before proposing anything.

## Anti-patterns

- Starting with a palette.
- Working room by room, which produces thirty decisions and no interior.
- Deciding the finish before knowing who cleans it and how.
- Letting the budget concentrate by attrition rather than by decision.
- Making everything special.
- Detailing a partition or a ceiling here.
- Treating a fit-out's base building as a blank slate.
- Producing a strategy with no hand-offs, which leaves the specific work exactly
  where it was.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
