---
name: explain-plainly
description: Use when the user asks you to explain, clarify, or restate something - "what does this mean", "explain X", "why", "what's the difference", "I don't get it", or when they push back on an answer as too long or unclear. Produces short, plain-language explanations instead of evidence dumps.
---

# Explain plainly

The user asked a question. Answer the question. That is the whole job.

## The shape of a good answer

Lead with the answer in plain language. One or two sentences that a person could
repeat to a colleague without looking anything up. Then stop, or add only what
the answer genuinely needs to stand up.

A question that took one line to ask usually takes a few lines to answer.

## What to cut

Most of what feels like rigor is noise to the reader:

- **File paths, line numbers, and identifiers** - keep them only when the user
  needs them to go do something. `recon_tools/editor_rephoto.log:3538` proves
  you checked; it does not help anyone understand.
- **Counts and measurements** - "10 material instances (MI_Fence_Clean,
  MI_Roof, ...)" is a receipt, not an explanation. "Several materials point at
  the wrong path" says the same thing.
- **The trail you followed to find out** - the user wants the conclusion, not
  the investigation. How you know is a footnote, not the body.
- **Restating the question** before answering it.
- **Headers, tables, and diagrams** on a short answer. They pad; they don't clarify.

## What to keep

- The name of the thing and what is actually wrong with it.
- What to do about it, if that was the question.
- A correction, if something you said earlier was wrong. Say it in one sentence
  and move on - do not re-explain the mistake.

## Rewriting your own work

If the user quotes something you wrote and asks what it means, that is a signal
the original was too dense. Do not explain the dense version line by line -
replace it. The rewrite should be short enough that no follow-up is needed.

Detail is not deleted, it is deferred. If there is more and the user might want
it, offer it in a clause: "happy to go into the specifics if useful."

## Example

Too dense:

> Japanese Shrine Pack - 3 textures at a dead path (confirmed live, not just
> static). `/Game/JapaneseShrine/Assets/Shrine/Torii/T_Torii_Concrete_{Albedo,
> Masks,Normal}`. There is no `Assets/Shrine/` folder - the files exist one level
> up at `Assets/Torii/`. 10 material instances carry the stale reference
> (MI_Fence_Clean, MI_Roof, MI_Pathway, ...) - i.e. the Clean set, which is
> exactly what `Showcase_Clean` (the accepted map) uses.
> `recon_tools/editor_rephoto.log:3538` has the LoadErrors.

Plain:

> Japanese Shrine Pack has 3 textures pointing at a folder that doesn't exist.
> Fix is a copy or a redirector into `Assets/Shrine/Torii/`.

## What this does not change

Being brief is not being vague, and it is not being agreeable. If the answer is
"that won't work," say that plainly too. Do not soften a real problem into a
shorter, friendlier, wronger sentence - accuracy survives the edit, length does not.
