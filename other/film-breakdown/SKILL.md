---
name: film-breakdown
description: Build scene plans and shot cards from scripts or ideas.
---

# Film Breakdown

Turn a script, treatment, or one-paragraph idea into a scene list and production-ready shot cards.

## Locate the studio

Work inside the current studio root.
Use `/docs/breakdown.md` for the scene list and `/prompts/` for shot-card files.
If either path is missing, ask whether to create the needed folder or document.
Ask one question at a time and wait for each answer.

## Read the source

Accept any of these inputs:

- a full script
- a treatment
- a one-paragraph idea

Preserve supplied dialogue verbatim.
Do not fill story gaps with invented facts.
If the input is incomplete, interrogate the user scene by scene.
Ask only the next question needed to define the current scene, then wait.
Finish the current scene before moving to the next one.

## Build the scene list

Write the scene table in `/docs/breakdown.md`.
Give every scene a stable scene ID.
For each scene, record its summary, location, time of day, characters, props, shot-card file, and status.
Keep asset tags and state variants exactly as supplied.
Mark unresolved information plainly instead of guessing.

## Create one shot-card file per scene

Create `/prompts/scNN-shot-cards.md` for each scene, using its stable scene number.
Represent every shot through exactly three lanes and 22 fields.
Do not add a fourth lane or merge fields.

### Lane 1: identity

Use these nine fields in this order:

1. Scene / shot ID
2. Location
3. Time of day
4. Characters with asset tags and state variants
5. Props
6. Description
7. Verbatim dialogue
8. Running time
9. Complexity

### Lane 2: direction

Use these six fields in this order:

1. Shot goal
2. Task as a verb
3. Dramaturgy
4. Blocking
5. Acting
6. Style device

### Lane 3: camera / edit

Use these seven fields in this order:

1. Size
2. Movement
3. Lens
4. Angle
5. Cut type
6. Pace
7. Transition

The three lanes contain 9 + 6 + 7 fields: 22 total.
Use a separate heading for each shot and a table for each lane.
Keep the same field order in every shot.

## Enforce clip boundaries

Give each clip one action only.
Target 10–15 seconds per clip.
If a card contains multiple actions, split it into separate shots.
If a single action cannot fit the target duration, ask the user how to divide or simplify it.

## Separate in-frame text

Remove signs, screens, titles, and other in-frame text from generation instructions.
Create `/docs/text-tasks.md` if any such text exists.
Record each text task with its scene / shot ID, exact required text, placement, and context.
Leave a pointer in the shot card to the matching text task.
Do not ask generation to render the text.

## Validate the breakdown

Check that every scene row points to one shot-card file.
Check that every shot has exactly the three lanes and all 22 fields.
Check that every clip has one action and runs 10–15 seconds.
Check that dialogue remains verbatim and all in-frame text is separated.
List unresolved fields and continue asking about them one at a time.

## Close the output

Summarize the files written and the scenes and shots created.
End with this note: the prompt is written later from the card almost mechanically because the three column groups map one-to-one to prompt blocks.
