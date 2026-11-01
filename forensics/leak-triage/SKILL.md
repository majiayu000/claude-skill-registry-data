---
name: leak-triage
description: "Works out what kind of water is appearing before anyone opens a wall: rain driven in, groundwater, a plumbing failure, condensation, or air-carried moisture, which look identical inside and have entirely different causes, owners and repairs. Reads the evidence that separates them — when it appears, what the weather was doing, whether it is warm or cold, whether it is clean, whether it stops — then narrows the source and names what would confirm it. Trigger on \"there is a leak\", \"water is coming in\", \"a stain appeared on the ceiling\", \"is this condensation or a leak\", \"where is this water coming from\", \"leak-triage\", or water appearing anywhere with no agreed cause. Carries no dew points, no rainfall figures and no test standards; every value comes from the building's own data or the tester. It diagnoses rather than repairs, does not apportion liability, and does not replace the enclosure consultant, the plumber, or the Architect of Record."
license: MIT
metadata:
  title: "Leak Triage"
  summary: "Find out which water this is before anyone opens anything up"
  discipline: "envelope-performance"
  tags: "Analysis, Review"
---

# Leak Triage

Water appears on a ceiling and the meeting starts with everyone's favourite
theory. Five completely different mechanisms produce the same stain, they have
different owners and different repairs, and opening the wrong thing costs more
than the leak.

The point of this is to narrow the source before anybody cuts.

## Scope and limits — read first

**What this does.** Separates the mechanisms by the evidence that actually
distinguishes them, narrows to the likely one or two, and names the test that
would confirm it. Says what to open and in what order, and what to record before
anything is disturbed.

**What this does not do.**

- **It carries no values.** No dew points, no rainfall intensities, no test
  pressures or standards. Anything computed comes from `condensation-check` with
  values you supply.
- **It does not apportion fault.** Whose leak it is follows from what it is, and
  that conversation belongs to the contract. Point at `dispute-advisor` and
  `construction-attorney`.
- It does not design the repair. Once the mechanism is known,
  `design-wall-assembly`, `design-roof-drainage`, `design-window-perimeter`,
  `design-balcony` and `design-below-grade-assembly` hold the methods.
- It does not test. Water testing, thermal imaging and tracer dye are done by
  people with equipment, and it names which.
- It does not replace the enclosure consultant, the roof consultant, the
  plumber, or the Architect of Record.

**What you need before starting.** Where the water appears and what it looks
like. When it started and when it recurs. What the weather was doing. What is
above and outside that point. What was built or changed recently. Photographs,
dated.

## Workflow

### Step 1. Record the evidence before anyone has a theory

Ask, in one message, and ask for facts rather than conclusions:

> 1. Exactly where does it appear, and how far does the stain or wetness
>    extend? Photograph it with something for scale.
> 2. When did it first appear, and when does it recur? Dates.
> 3. What was the weather doing each time: rain, wind direction, temperature,
>    snow melt, or nothing at all?
> 4. Is the water clean, discoloured, or smelly? Is it warm or cold?
> 5. Does it stop, and how long after the weather stops?
> 6. What is directly above and directly outside that point, on every floor up
>    to the roof?
> 7. What has been built, altered or repaired in the last year?
> 8. Is the building occupied and heated, and how humid is it inside?

**Record all of this before anyone opens anything.** Opening destroys the
evidence that separates the mechanisms, and the most common failure in leak
investigation is cutting on the first theory.

### Step 2. Separate the five mechanisms by what actually distinguishes them

| Mechanism | Appears when | Water is | Stops | Points to |
|---|---|---|---|---|
| Rain penetration | During or shortly after rain, often with wind from one direction | Cold, usually clean, may be dirty from the cavity | Hours after the rain | The face it rained on |
| Roof or drainage | During rain, or during melt, often not at the same place as the defect | Cold, often dirty | Slowly | `design-roof-drainage` |
| Groundwater | With the water table or after prolonged rain, low in the building | Cold, often mineral-stained | Days, or never | `design-below-grade-assembly` |
| Plumbing | Any time, unrelated to weather | Warm or cold, may be clean or foul | Only when isolated | The plumber |
| Condensation / air leakage | Cold weather, often worst overnight, worse when occupied | Clean, on cold surfaces, often widespread rather than one point | With the weather, or when humidity drops | `condensation-check`, `air-barrier-trace` |

**The two questions that split the field fastest:** does it correlate with rain,
and does it correlate with cold. Something that appears in dry cold weather is
not rain. Something that appears in warm rain is not condensation. Something
unrelated to both is plumbing until proven otherwise.

Report which mechanisms the evidence rules **out**, not only which it suggests.
Ruling out is more reliable than ruling in, and it is what stops the wrong wall
being opened.

### Step 3. Follow the water backwards, not down

Water enters somewhere and appears somewhere else, and the two are rarely
vertically aligned:

- It runs along the top of anything horizontal: a stud plate, a ceiling
  membrane, a duct, a beam, a flashing.
- It follows fasteners and services.
- It appears at the first place it can get out, which is a joint, a light
  fitting, or the low point of a run.

So the search starts at the appearance point and works **up and outward**, not
straight up. List the candidate entry points in order of distance from the
stain, and say which are reachable without cutting.

### Step 4. Name the test that would confirm it, and its order

For each surviving mechanism, the confirmation:

| Mechanism | What confirms it | Who does it | What it costs |
|---|---|---|---|

- Rain penetration: a controlled water test, one area at a time, working
  upward, with somebody watching inside. **Testing everything at once proves
  nothing.**
- Plumbing: isolate and watch, or a pressure test. Cheap and fast, so do it
  early even when it seems unlikely.
- Condensation: surface temperature and humidity readings over time, and
  thermal imaging in cold weather. `condensation-check` on the assembly.
- Groundwater: monitor with the weather, and check the drainage and the sump.
- Roof: flood test where the construction allows it.

Order them by cost and by what they rule out. **Isolate the plumbing first**
almost every time: it is the cheapest test and it removes the mechanism that has
nothing to do with the envelope.

### Step 5. Say what to open, in what order, and what to record

- The first opening, and what it would tell you.
- What to photograph and measure before closing it.
- What not to open yet and why.
- Who should be present.
- Whether anything should be preserved for a later claim. Point at
  `dispute-advisor`.

### Step 6. Report

- What the evidence rules out, first.
- The surviving mechanisms, ranked, with the evidence for each.
- The confirmation tests in order.
- The first opening.
- What is still unknown, and what would answer it.

Close by saying nothing was tested and no cause is confirmed, and that a
repair designed before the mechanism is confirmed will be the wrong repair.

### Step 7. Save

Ask where. A leak investigation is read back months later, often by somebody
else, and often in a dispute.

## Rules

- **Record the evidence before anything is opened.**
- **Report what is ruled out before what is suspected.**
- Never name a cause as confirmed without a test.
- Search up and outward from the stain, never straight up.
- Isolate the plumbing early, whatever the theory.
- Never apportion fault. Name the mechanism and point at the contract.
- Say on every run that a repair designed before confirmation is the wrong
  repair.

## Anti-patterns

- Opening the wall on the first theory.
- Water testing a whole elevation at once.
- Assuming a stain is directly below its entry point.
- Calling clean water on a cold surface a leak without checking the humidity.
- Dismissing plumbing because the leak "looks like rain".
- Designing the repair before the mechanism is confirmed.
- Letting the meeting decide the cause by consensus.
- Closing an opening without photographing what was in it.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
