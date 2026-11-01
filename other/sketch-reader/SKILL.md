---
name: sketch-reader
description: "Reads the drawings that are not drawings: a hand sketch, a napkin diagram, a photograph of a whiteboard, a rendered view, a screenshot of a model. Separates what is decided from what is drawn loosely and what is placeholder, since the three look alike in a sketch and the difference is the whole content. Then names what the sketch has already committed to without anybody deciding it. Trigger on \"read this sketch\", \"what does this diagram say\", \"the client sent a drawing they did\", \"read this rendering\", \"what does this model view show\", \"sketch-reader\", or any informal drawing handed over. Carries no dimensions and reads no scale off an unscaled drawing. `drawing-reader` reads a measured PDF; this reads the ones drawn by hand or produced to look convincing. It does not judge the design and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Sketch Reader"
  summary: "Read a sketch, an image, or a model view and say what it commits to"
  discipline: "design-building-types"
  tags: "Review, Design"
---

# Sketch Reader

A sketch says three things at once and shows them identically: this is decided,
this is roughly where it goes, and this is a placeholder somebody drew so the
page was not empty. Everyone reading it picks a different assignment, and the
meeting agrees about a drawing nobody read the same way.

A rendering has the opposite problem. Everything in it looks decided, including
the parts that were defaults.

## Scope and limits — read first

**What this does.** Reads an informal or persuasive drawing and sorts what is in
it into decided, loose, and placeholder. Then names what it commits to
regardless of intent, and what it deliberately does not show.

**What this does not do.**

- **It measures nothing.** No scaling off a hand drawing or a rendered view.
  Anything dimensional is reported as a proportion or as unmeasurable.
- It does not read a measured drawing. `drawing-reader` does that, and
  `plan-review` reads a plan.
- It does not judge the design. `design-critic` and `precedent-critique` do.
- It does not identify a precedent image's building or architect. Where an image
  is offered as a reference, `precedent-finder` handles that, and a guess at
  what a photograph shows is not made here.
- It does not replace the Architect of Record.

**What you need before starting.** The image. Who drew it and when. What it was
drawn to do. What has been said about it since.

## Workflow

### Step 1. Establish who drew it and what for

Ask, in one message:

> 1. Who made it: you, a colleague, the client, a consultant, a previous
>    architect, or is it a reference from somewhere else?
> 2. When, and has anything changed since?
> 3. What was it made for: thinking, explaining, persuading, or recording a
>    decision?
> 4. Has anybody agreed to it, and what did they think they were agreeing to?
> 5. Is anything on it dimensioned or scaled at all?

**Question 3 decides how it is read.** A sketch made to think with contains
guesses on purpose. A rendering made to persuade contains defaults presented as
decisions. A client's own sketch contains what they actually want, which is
rarely what they said.

**Question 4 is the one that causes trouble.** A client who nodded at a
rendering believes the window sizes.

### Step 2. Sort everything in it into three

| What | Decided / Loose / Placeholder | How you can tell |
|---|---|---|

The tells, and they are worth stating because they are how the sorting is done:

- Drawn more than once, or drawn carefully, or dimensioned: decided.
- Drawn once, quickly, in the same weight as everything else: loose.
- Generic, symmetrical, evenly spaced, or from a library: placeholder. In a
  rendering this includes the furniture, the people, the sky, the trees, and
  usually the glazing pattern.
- Absent: not a decision, and it should not be read as one.

Where you cannot tell, say so. **An item nobody can classify is the item the
meeting will disagree about.**

### Step 3. Say what it commits to anyway

Regardless of what was intended, a drawing commits to things:

- Proportions and relative sizes, because people remember them.
- Where the entrance is.
- How many storeys, and roughly what height.
- What faces which way.
- Whether there is a courtyard, a corridor, a single volume.
- The material character, if the image has any.

For a rendering, add the ones that get believed: window proportions, the
material palette, the light, the landscape, and how much glass there is.

Report each with whether anybody has actually decided it.

### Step 4. Say what it deliberately does not show

- Structure, almost always.
- Services and plant, always.
- Levels and thresholds.
- Anything at the back or the sides, in a rendering.
- Scale, unless somebody put a person in it who is the right size.
- Code: exits, ratings, accessible routes.

This list matters because the absence gets read as "not a problem" rather than
"not addressed".

### Step 5. Report

- Who drew it, what for, and what that means for how to read it.
- The three-way sort, with anything unclassifiable named first.
- What it commits to, and which of those anybody has decided.
- What it does not show.
- What has to be asked of whoever drew it, as a short list of questions.

Where the client has already agreed to it, say plainly which parts they most
likely believe are settled.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where. Worth keeping where a
client has seen the image.

## Rules

- **Never measure or scale a hand drawing or a rendered view.**
- Ask who drew it and what for, before reading it.
- Sort into decided, loose and placeholder, and name what cannot be sorted.
- Report what it commits to regardless of intent.
- List what it does not show, and say that absence is not approval.
- Never identify a building or an architect from an image.
- Never judge the design.

## Anti-patterns

- Scaling off a sketch.
- Reading a rendering's furniture, glazing pattern or landscape as decisions.
- Treating what is absent as resolved.
- Reading a client's sketch as a brief rather than as a clue.
- Guessing what building a reference photograph shows.
- Assuming the person who drew it meant every line.
- Critiquing it.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
