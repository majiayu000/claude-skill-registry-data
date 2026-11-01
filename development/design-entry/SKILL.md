---
name: design-entry
description: "Works the entrance as a continuous sequence rather than as a door: how it is found from the street, what happens on the way in, what the threshold has to hold at once, and where somebody stands when they arrive and nobody is expecting them. Names the four things that meet at a doorway and cannot all be optimised — level access, weather, energy, and security — and says which one this project lets win. Trigger on \"entrance design\", \"the entry sequence\", \"where is the front door\", \"vestibule\", \"the entrance is hard to find\", \"design-entry\", or an entrance that is a door on a plan and nothing more. Carries no dimensions, no threshold limits and no requirements; accessible thresholds and vestibule requirements are code and standards you quote. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Entry"
  summary: "Work the entry as a sequence from the street to the second door"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Entry

The entrance is drawn as a door and it is a sequence: seen from the street,
approached, arrived at, entered, and then a second moment inside where somebody
either knows where to go or does not. Every part of it is a decision and the
door is the least of them.

## Scope and limits — read first

**What this does.** Works the sequence from the point the building is first seen
to the first decision inside. Names the four demands that meet at the threshold
and which one this project lets win. Works the arrival for the person nobody is
expecting.

**What this does not do.**

- **It carries no dimensions.** Accessible threshold limits, manoeuvring
  clearances, vestibule requirements, door forces: code and standards you quote.
- It does not trace the rest of the building. `circulation-study` works every
  journey; this works the first thirty metres of one.
- It does not detail the door or its perimeter. `design-window-perimeter` holds
  the perimeter method.
- It does not do accessibility review. Point at `accessibility-specialist`,
  whose whole method is the journey, and `/test-ada` for one clearance.
- It does not do the security design. `security-design-review` does, and the
  entrance is where it starts.
- It does not replace the Architect of Record.

**What you need before starting.** The site and the approach. Who arrives, how,
and from where. The climate. Whether anyone staffs the entrance. What the
building is, because a house, a clinic and an office entrance answer different
questions.

## Workflow

### Step 1. Establish who arrives and from where

Ask, in one message:

> 1. Who arrives: on foot, by car, by bike, dropped off, by transit, by
>    delivery? From which direction does each come? Point at
>    `site-access-study`.
> 2. Is anyone expecting them? A staffed reception, a doorbell, a code, or
>    nobody.
> 3. What is the weather doing on arrival: prevailing wind, driving rain, snow
>    that has to be cleared, sun in the eyes?
> 4. Is this the only entrance? Where do staff, deliveries and refuse go, and is
>    the accessible entrance the same one as everybody else's?
> 5. What is inside the door, and what decision does the arriver have to make
>    there?
> 6. What is fixed: a level, a boundary, an existing opening, a required
>    frontage?

**Question 4 has one right answer and it is often not taken.** An accessible
entrance separate from the main one is compliant and is not equivalent, and if
it is separate it should be a decision with a reason rather than what the levels
produced.

### Step 2. Work the approach: found, then reached

Two different problems and both are usually skipped:

**Found.** From where the building is first seen, is it obvious where the
entrance is? Say what makes it obvious: a change in the massing, a canopy, a
light, a path, a change in the ground. **If the answer is a sign, note it** —
a sign is what gets used when the building did not say it.

**Reached.** The route from where somebody arrives to the door:

- Is it the shortest route, or is the shortest route somewhere else? People take
  the short one and wear a path across whatever is in the way.
- Does it work for someone with a stroller, a suitcase, a wheelchair, or a
  delivery trolley?
- Is it lit, and overlooked?
- Where does the accessible route run, and does it join the main one before the
  door or at it? Joining at the door is better than arriving separately.
- Where does somebody wait if they are early, and where do they stand while
  looking for a key?

### Step 3. Name the four demands at the threshold and say which wins

They meet at one line and they cannot all be optimised:

| Demand | Wants | Conflicts with |
|---|---|---|
| Level access | No upstand at all | Weather, which wants a threshold |
| Weather | To keep rain and wind out | Level access |
| Energy | A closed, sealed, possibly double door | Ease of use, and openness |
| Security | A controlled, closed door | Welcome, and being found |

State which one this project lets win, and what the others get instead: a
drainage channel, a canopy or recess, a vestibule, a revolving or automatic
door, a mat well, a wind lobby.

**A recess or a canopy buys most of the weather argument without an upstand**,
and it also gives somebody a place to stand while they find a key. Say so where
it applies.

Then check the threshold against the quoted accessible provision, and against
what the drainage does. Point at `design-window-perimeter` for the perimeter
detail and `civil-drawing-review` for the grading right outside.

### Step 4. Work the vestibule, if there is one

- Is one required? Quote the energy provision if so.
- Is it deep enough that the second door can be opened before the first closes,
  by somebody with their hands full or in a wheelchair? Two doors in a shallow
  lobby is the most common accessibility failure at an entrance.
- Both doors' swings and their manoeuvring clearances, against each other.
- Where the mat is, how long it has to be to work, and how it is cleaned.
- Where snow and water go, and whether the floor is safe wet.
- What it does to the acoustics and the draught.

### Step 5. Work the first moment inside

The entry is not over at the door:

- Where does the arriver's eye go, and is that where they should go?
- Is the destination visible: a desk, a lift, a stair, a corridor? If not, what
  tells them?
- How many choices do they have to make, and is one of them wrong?
- Where does somebody stand and wait, and is that in the door swing or in the
  route?
- Where do coats, bags, buggies and umbrellas go?
- Where does the person at the desk look, if there is one, and can they see the
  door? Point at `security-design-review`.

### Step 6. Report

- The sequence, point by point, with each weak moment marked.
- What makes the entrance findable, and whether it is a sign.
- Which of the four demands wins at the threshold, and what the others got.
- Whether the accessible route arrives with everyone else or separately.
- Every dimension still open, with the provision to quote.
- What has to be checked elsewhere: the grading outside, the accessible
  clearances, the security position.

Then ask whether to write it to a file and where.

## Rules

- **Work found and reached as two separate problems.**
- Name which of the four demands wins at the threshold, every run.
- Say when findability depends on a sign.
- Ask whether the accessible entrance is the same one as everybody else's, and
  say so plainly when it is not.
- Check the vestibule for someone with their hands full.
- **Never supply a threshold limit, a clearance, or a door force.**
- Carry the sequence past the door to the first decision inside.

## Anti-patterns

- Designing the door and calling it the entrance.
- A separate accessible entrance arrived at by default rather than by decision.
- A level threshold with no drainage, or a drainage upstand with no level route.
- A vestibule too shallow to use with a suitcase.
- Relying on a sign to say where the front door is.
- Ignoring the route people will actually take, which is the short one.
- Ending the sequence at the door.
- No place to stand while finding a key, in the rain.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
