---
name: photo-reader
description: "Reads any photograph an architect ends up with — a site visit, an existing building, a defect somebody wants explained, a phone picture from a client, a product on a shelf — and separates what is visible from what is inferred, because a photograph is the most persuasive and least complete document on a project. Establishes when and where it was taken and which way the camera faced before reading anything, since a photograph with no location is evidence of nothing. Trigger on \"read this photo\", \"what am I looking at here\", \"the client sent a picture\", \"is this a problem\", \"photo-reader\", or an image handed over with a question. Carries no dimensions and measures nothing from an image. It diagnoses nothing: a photograph of a stain is not a diagnosis, and `leak-triage` takes it from there. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Photo Reader"
  summary: "Read a photograph for what it shows and what it cannot show"
  discipline: "construction-admin"
  tags: "Review"
---

# Photo Reader

A photograph persuades more than a drawing and carries less. It shows one
moment, from one position, with everything outside the frame missing and no
scale unless somebody put something in it.

Almost every wrong conclusion from a photograph comes from the same two places:
not knowing where it was taken, and reading a cause into an effect.

## Scope and limits — read first

**What this does.** Establishes the photograph's own facts first, then reports
what is visible, what is inferred, and what the frame excludes.

**What this does not do.**

- **It measures nothing.** No dimension, no slope, no gap width, no distance. A
  photograph has perspective and no scale. Where size matters, it says what to
  go back and measure.
- **It diagnoses nothing.** A stain is not a leak, a crack is not a structural
  failure, and rust is not a cause. Point at `leak-triage` for water and at the
  engineer for anything structural.
- It does not identify a building, an architect, or a product from an image.
- It does not read a drawing. `drawing-reader` and `sketch-reader` do.
- It does not write the report. `/create-site-visit-report` does, and this feeds
  it.
- It does not replace the Architect of Record.

**What you need before starting.** The photograph, at full resolution. When and
where it was taken and by whom. What question it was taken to answer, if any.

## Workflow

### Step 1. Establish the photograph's own facts, before looking at the subject

Ask, in one message:

> 1. When was it taken: date and roughly what time?
> 2. Where, precisely? Which building, which level, which room, which wall.
> 3. Which way is the camera facing?
> 4. Who took it, and what were they trying to show?
> 5. Is there anything in frame for scale?
> 6. Are there other photographs of the same thing, from other positions or
>    other dates?

**A photograph with no location is evidence of nothing**, and this is the most
common problem with images that arrive by phone. Say so plainly and ask, rather
than reading it anyway.

Question 4 matters as much: somebody photographed this on purpose, and what they
thought they were showing is not always what is in the frame.

### Step 2. Report what is visible, plainly

Describe what is in the image without interpreting it. Materials, condition,
construction, what meets what, what is finished and what is not, what is
temporary, what has been added.

Use plain description rather than conclusion. "A brown stain about a hand's
width, on the ceiling near the corner" rather than "water damage".

### Step 3. Mark every reading as one of three

| Observation | Visible / Inferred / Assumed |
|---|---|

- **Visible.** It is in the frame and unambiguous.
- **Inferred.** Reasonable from what is visible, and could be wrong. A wall
  looks load-bearing; a joint looks like it moved.
- **Assumed.** Brought to the image from outside it: what the construction
  probably is, what the material probably is, what probably happened.

Count them. **A reading that is mostly `assumed` is a reading somebody should
not act on**, and saying so is the useful output.

### Step 4. Say what the frame excludes

The half nobody does:

- What is immediately outside the frame that would change the reading?
- What is behind, above, or below what is shown?
- Is this the worst instance, a typical one, or the only one? A single
  photograph cannot say, and people assume typical.
- What time of day, season or weather would change what this shows? A stain
  photographed dry says nothing about when it is wet.
- Is the thing shown still there, or has it been covered since?

### Step 5. Say what to go back for

The output that makes the visit worth repeating:

- What to photograph next: from where, at what distance, with what in frame for
  scale.
- What to measure, since nothing here can be.
- What to open up or look behind.
- What to photograph at a different time or in different weather.
- Whether a photograph of the same thing already exists from another date, which
  turns one image into a comparison.

### Step 6. Report

- The photograph's own facts, and any that are unknown.
- What is visible, described plainly.
- The three counts, `assumed` named first if it is the largest.
- What the frame excludes.
- What to go back for.
- Where a diagnosis is wanted: the skill or the party that gives one.

### Step 7. Save, if asked

Ask whether to write the reading to a file and where. Keep it with the image, and
point at `/create-site-visit-report` where this is part of a visit.

## Rules

- **Establish when, where and which way the camera faced, before reading.**
- **Never measure anything from a photograph.**
- **Never diagnose.** Describe, then name the skill that diagnoses.
- Describe before interpreting, in plain words.
- Mark every reading visible, inferred, or assumed, and count them.
- Say what the frame excludes, every run.
- Never identify a building, an architect, or a product from an image.

## Anti-patterns

- Reading a photograph with no location.
- Calling a stain a leak.
- Scaling off an image because something familiar is in it.
- Treating one photograph as representative.
- Reporting an inference as an observation.
- Answering the question the photographer asked instead of reading what is
  actually in the frame.
- Ignoring what is just outside the edge.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
