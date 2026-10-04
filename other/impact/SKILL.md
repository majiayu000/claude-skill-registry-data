---
name: design-impact
description: Facilitates the Impact movement of a Tutti design session. Use after the Frame movement to work out the goal, the actors who can move it, the behavior change each actor must make, and how those changes map to deliverables (an impact map). Asks one question at a time, may invoke the flow diagram skill when the mapping reads better as a picture, and emits the movement artifact section once the goal, actors, and impact-to-deliverable mapping are covered.
---

# Impact movement

Work out how the project actually moves the needle before listing features. The guiding
question is: what behavior change, in which actor, produces the goal? An impact map runs goal
to actor to behavior change to deliverable, so a deliverable that maps to no behavior change is
suspect.

## What to cover

- **Goal**: the one measurable outcome the project is for, phrased so you could tell it moved.
- **Actors**: the people or systems whose behavior can move the goal (not only the customer).
- **Impacts mapped to deliverables**: the behavior change wanted in each actor, and the
  concrete thing you would build to cause it.

## How to facilitate

Ask ONE question at a time. Start from the goal, then draw out the actors, then the behavior
change wanted in each, and only then the deliverable that would cause it. Push back on a
deliverable that is not tied to any behavior change, and on a goal you could not measure. Go
deeper on the actor whose behavior change is least obvious.

## Diagrams

When the actor-to-deliverable mapping is clearer as a picture, invoke the `flow` diagram skill
and embed its inline SVG in the artifact section.

## When you are done

Once the goal, the actors, and the impact-to-deliverable mapping are covered, emit the tagged
complete reply with the artifact section as markdown: a `## Impact` heading, the goal, the
actors, and the mapping of each behavior change to its deliverable.
