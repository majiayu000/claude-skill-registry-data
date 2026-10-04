---
name: design-decompose
description: Facilitates the Decompose movement of a Tutti design session. Use after the Slice movement to break the work into milestones, epics, and issues, write EARS acceptance criteria for each unit ("WHEN a condition holds THE SYSTEM SHALL do a behavior"), and order the units by dependency. Asks one question at a time and emits the movement artifact section once the milestone and epic and issue tree, the EARS criteria, and the dependency ordering are covered.
---

# Decompose movement

Turn the sliced plan into small, testable, ordered units. The guiding question is: what are the
small, testable, dependency-ordered units? Each unit is small enough to finish and check, its
acceptance is written so a machine or a reviewer could tell it is done, and the units are laid
out so nothing is scheduled before what it depends on.

## What to cover

- **Milestones/epics/issues drafted**: the tree from milestone down to issue, each issue a unit
  of work small enough to complete and verify on its own.
- **EARS acceptance criteria written**: each unit's acceptance in EARS form, for example
  "WHEN a paired phone sends a turn THE SYSTEM SHALL stream the reply", so done is testable.
- **Dependencies ordered**: the units sequenced so nothing lands before what it needs.

## How to facilitate

Ask ONE question at a time. Draw out the tree from the backbone and ribs of the Slice movement,
then write EARS criteria for each unit (push back on an "acceptance" that is not observable),
then order the units by dependency. Split any issue too big to verify in one pass. Go deeper
where a dependency is unclear.

## When you are done

Once the milestone, epic, and issue tree, the EARS criteria, and the dependency ordering are
covered, emit the tagged complete reply with the artifact section as markdown: a `## Decompose`
heading, the milestone/epic/issue tree, the EARS acceptance criteria per unit, and the
dependency-ordered sequence.
