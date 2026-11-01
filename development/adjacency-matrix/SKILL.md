---
name: adjacency-matrix
description: "Builds a programme adjacency matrix from movement and constraint rather than from stated preference: takes the room list, asks for each pair what actually travels between them and how often, separates a required adjacency from a desired one and from a required separation, then reads the finished matrix for the rooms that want to be everywhere at once and the conflicts that no plan can satisfy. Trigger on \"adjacency matrix\", \"bubble diagram\", \"which rooms need to be near each other\", \"programme relationships\", \"adjacency-matrix\", or a room list handed over with a request for how it should be organised. Carries no adjacency conventions for any building type, because who has to be near whom is the client's operation and not a rule. Reads a room list from `space-program` where one exists and does not duplicate its area tracking. It does not lay out a plan and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Adjacency Matrix"
  summary: "Build the matrix from who actually moves, not from who says they are close"
  discipline: "design-building-types"
  tags: "Design"
---

# Adjacency Matrix

Ask a user group who they need to be near and everyone says everyone. The matrix
only becomes useful when the question changes from preference to movement: what
travels between these two rooms, how often, and what happens if it has to go
further.

## Scope and limits — read first

**What this does.** Takes the room list, works every pair that matters, and
records the relationship as one of a small set of kinds with the reason behind
it. Then reads the completed matrix back for what it reveals: the rooms with too
many demands to satisfy, the pairs in direct conflict, and the clusters that
suggest how the building organises itself.

**What this does not do.**

- **It carries no conventions.** There is no built-in view that a given room
  type belongs beside another in any building type. That is the client's
  operation, and assuming it produces a plan that fits a generic building rather
  than this one.
- It does not track areas. `space-program` holds the room list, the targets and
  the designed areas. This reads that list where it exists rather than starting
  a second one.
- It does not lay out a plan. A matrix is an input to a plan, and the step
  between them is design.
- It does not resolve the conflicts it finds. Naming them is the deliverable.
- It does not decide the brief. `brief-review` interrogates that.
- It does not replace the Architect of Record.

**What you need before starting.** The room list, ideally from `space-program`.
Who uses each room and when. What moves between rooms: people, goods, patients,
waste, information, sound. Any separation that is required rather than preferred,
and what requires it.

## Workflow

### Step 1. Take the list and the movements

Ask, in one message:

> 1. The room list. If `space-program` is running, point at it rather than
>    retyping.
> 2. For the building as a whole: who moves through it, and are there flows that
>    must not cross? Public and staff, clean and dirty, secure and open,
>    goods and people.
> 3. Which rooms have a fixed position already: an entrance, a loading dock, a
>    plant space, an existing core?
> 4. Are there separations required by code, licensing, security or acoustics?
>    Name what requires each.
> 5. Who is available to answer questions about the operation, and have they
>    been asked yet?

If the room list is long, ask which rooms are worth pairing. A matrix of eighty
rooms has three thousand cells and almost all of them are empty.

### Step 2. Fix the vocabulary before filling any cell

Agree the relationship kinds first, and use no others:

| Mark | Means | Test for it |
|---|---|---|
| Required | Must be adjacent, and something fails if not | What fails? Name it |
| Desired | Better if adjacent | Better for whom, and by how much? |
| Neutral | No relationship | |
| Separate | Should not be adjacent | Why not? |
| Prohibited | Must not be adjacent | What prohibits it? Quote it |

The difference between `required` and `desired` is the whole value of the
matrix, and it collapses the moment a cell is filled without a reason. Every
`required` and every `prohibited` carries a reason in the same cell or it is
downgraded.

### Step 3. Fill by movement, one row at a time

For each pair, ask what actually travels between them and how often. Not "should
these be close". A relationship with no traffic behind it is `desired` at best.

Fill by row rather than by scanning the whole grid. A room at a time, with the
person who uses that room, produces answers that a group session does not.

Record the source of each answer: which user, which department, which document.
When two user groups disagree about the same pair, record both and mark the cell
disputed rather than averaging them.

### Step 4. Read the matrix back

The reading is the point, and it is what a bubble diagram cannot do:

- **Over-demanded rooms.** Count the `required` marks per room. Any room with
  many is a room that cannot be where everything needs it. Name them; these
  usually turn out to be reception, a lift core, a store, or a staff base, and
  the answer is usually to duplicate or to relocate the demand rather than the
  room.
- **Direct conflicts.** Any pair that is `required` to one group and `separate`
  to another. List them individually; they are decisions, not errors.
- **Chains.** A required to B, B required to C, C separate from A. These cannot
  all hold and the matrix is where they are visible.
- **Clusters.** Groups of rooms with dense internal requirements and few
  external ones. These are the building's departments whether the brief named
  them or not.
- **Orphans.** Rooms with no relationships at all. Either they were not asked
  about, or they can go anywhere, and those are very different findings.

### Step 5. Report

The matrix, then the five readings, then:

- Every cell filled without a reason, counted.
- Every disputed cell, with both positions and who holds each.
- Every `prohibited` whose source was not quoted.
- What has not been asked yet, and of whom.

Close by saying that the matrix is an input and that no plan follows from it
automatically.

### Step 6. Save, if asked

Ask whether to write the matrix to a file and where. Markdown or CSV.

## Rules

- **Never fill a cell from a building-type convention.**
- **Every `required` and `prohibited` carries a reason**, or it is downgraded.
- Ask what travels, never whether they should be close.
- Record who said each thing. Disputes stay disputed, never averaged.
- Report over-demanded rooms and conflicts, every run.
- Never produce a layout.

## Anti-patterns

- Filling the matrix from what is usual for the building type.
- Treating a user group's preference as a requirement because they stated it
  firmly.
- Averaging two departments' disagreement into one mark.
- Marking everything required, which produces a matrix with no information in
  it.
- Producing a bubble diagram and calling the analysis done.
- Duplicating `space-program`'s room list instead of reading it.
- Presenting a plan as following from the matrix.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
