---
name: thumbnail-set-designer
description: Turn a title and hook into a set of genuinely different on-brand thumbnail prompts, rotating distinct layouts against accent colours, with the traps that ruin AI-generated thumbnails built in. Use when generating several thumbnail or cover-image options for one piece of content, when every AI thumbnail comes back looking the same, when on-image text renders wrong, or when setting up a repeatable thumbnail system for a channel.
---

# Thumbnail Set Designer

Ask an image generator for seven thumbnails and you get seven versions of one
idea, because nothing told it to be different. This turns a title and a hook into
a set of specific, deliberately unlike prompts, and carries the traps that
otherwise cost you a whole generation run.

Pair it with `thumbnail-legibility-check` to choose between the results.

## When to use

- Generating several thumbnail or cover-image options for one piece of content.
- Every option coming back as a variation of the same composition.
- On-image text rendering wrong.
- Building a repeatable system rather than making one thumbnail.

## Step 1: plan the set

```bash
python scripts/rotation.py "Your video title" --count 7
```

Standard library only, `--json` for machine output. It pairs seven distinct
layouts against rotating accent colours, seeded from the title so the same
subject always produces the same plan.

**The layouts and colours in the script are a neutral starting set, not a house
style.** Replace `LAYOUTS` and `COLOURWAYS` with your own before real use. What
matters is the shape of the system:

- **Distinct means the eye lands somewhere different**, not that the crop moved.
  A face-left layout and a face-right layout are one layout.
- **One accent per image**, rotating across the set, so a channel looks like one
  channel while individual videos stay distinguishable.
- **Determinism over randomness.** A seeded rotation is reproducible and
  debuggable. Random assignment gives you the same thumbnail twice and no way to
  find out why.

## Step 2: extract the hero element

Most thumbnails need one thing that carries the claim: a figure, a short phrase,
or an object.

**The trap that costs runs:** whatever extracts that figure will happily grab a
number from anywhere in your inputs. A currency amount mentioned in passing in
the notes field beats the actual headline figure, because currency symbols look
important. The generated set is then built around the wrong number and you find
out after the images exist.

Fix it by pulling the hero element from the title and hook only, never from free
notes, and by showing the person what was extracted before generating.

## Step 3: write the prompts

Each prompt needs, in this order:

1. **The composition**, concretely. "Subject on the left third, three stacked
   words on the right", not "an engaging layout".
2. **The exact on-image text, character for character**, followed by an explicit
   instruction to render that punctuation exactly. Generators drop and mangle
   punctuation; a figure like `$1.4M` comes back as `$1 4M` often enough that
   every prompt containing punctuation must call it out.
3. **The accent colour**, as a value, plus where it appears.
4. **Reference handling**: which references attach, and a likeness instruction
   naming who must match which reference.
5. **The output format**: aspect ratio and resolution.
6. **What to avoid**: watermarks, borders, extra limbs, invented logos, text
   other than the string you specified.

Keep the prompts in files, one per candidate, rather than inside a script. Every
generation path can then read the same prompts, and a person can read them too.

## Step 4: the rules that keep a set usable

- **Keep some slots subject-only.** On interview or two-person content, put the
  guest in most of the set but not all of it. A set where every option has the
  same two faces is not a set of options.
- **Cap attachments deliberately.** Hosted interfaces limit images per message.
  When you hit the cap, drop props and logos, never faces.
- **Filenames are an interface.** Decide the naming up front and have every path
  write those exact names. A renamed file is silently invisible to whatever reads
  the folder next.
- **Verify a reference photo shows the right person** before generating anything.
  Automated image search returns confident wrong answers, especially for people
  linked to a well-known company.

## Step 5: close the loop

Record which layout and which colour won each time. After enough decisions,
lead the next set with the combination that keeps winning, while still generating
the full spread so the system can be proved wrong. `scripts/rotation.py --lead`
takes that pair.

## Rules

- Never invent the hero figure. Take it from the title and hook, and show it to
  the person before generating.
- Always state on-image text exactly, and always demand exact punctuation.
- Distinct layouts, one accent each, deterministic assignment.
- Confirm reference identity before generating.
- Replace the example layouts and palette with the actual brand before use.

## Output

One prompt file per candidate with the layout, exact text, accent value,
reference list and format, plus a short plan table showing which layout and
colour each slot received.
