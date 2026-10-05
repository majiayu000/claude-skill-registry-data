---
name: hylo-writing
description: Write an article beat-by-beat, drawing from the vault's knowledge base. The user states what to write, who it's for, and what stance to take — the skill discovers relevant knowledge units and leads a choose-your-own-adventure writing journey. Use when the user wants to write something grounded in their accumulated understanding, not assemble raw notes.
---

<what-to-do>

## Phase 0 — Topic alignment

Ask the user for three things (can be in one message):

1. **What** — the topic or question the article addresses
2. **Who** — the intended reader (their background, what they already know)
3. **Stance** — the position or argument the article will take

If the user didn't say where to save the article, ask now. Remember the path.

Once you have those three, scan the knowledge base:

```bash
hylo knowledge --help
hylo knowledge list-indexes
```

Select 1–3 domain indexes most relevant to the topic. Read those index files to find matching units. If no indexes exist, scan `_knowledge/` directly.

**Present the palette for confirmation.** Do not proceed to Phase 1 until the user signs off. Format it like this:

---
**Sources found**

| #   | Knowledge unit | What it contributes                                  |
| --- | -------------- | ---------------------------------------------------- |
| 1   | `unit-name`    | one sentence on what this unit brings to the article |
| 2   | …              | …                                                    |

**Possible gaps:** list anything you think the article needs that the knowledge base doesn't cover (if any).

> That's everything I found. Does this palette cover what you need, or should we add more? If something's missing, compile the relevant notes with `hylo-compile-note` first and I'll re-scan.
---

Wait for the user to confirm, remove units, or tell you what's missing before moving on. If the user wants to add coverage: suggest they run `hylo-compile-note` on the relevant source, then re-scan and re-present the updated palette. Do not continue to Phase 1 with a palette the user hasn't confirmed.

---

## Phase 1 — Starting beats

Write 2–3 candidate **starting beats**, each drawn from different units in the confirmed palette. Each beat is a different entry point into the article — a different angle on the same topic.

Show the beats before writing anything to the article file. For each, name which knowledge unit(s) it draws from, and preview where it might lead next.

The user picks one. Then go to Phase 2.

---

## Phase 2 — Beat-by-beat writing

Loop until the article reaches a natural end:

1. Write **only the chosen beat** to the article file. Pull material from relevant knowledge units — paraphrase, quote, recombine. The units are a quarry. Preserve any time-anchored content ("as of YYYY-MM-DD") if it matters to the argument.
2. Re-read the article file from disk.
3. Offer 2–3 candidate **next beats** — different directions from where the article now stands. Name the knowledge unit(s) each would draw from.
4. The user picks one. Repeat.

---

## Phase 3 — Close

When the article reaches its natural end, write the final beat and stop.

Then ask: **Do you want to compile this article back into the knowledge base?** If yes, trigger the `hylo-compile-note` skill on the article file. The article itself becomes a source — its argument, its synthesis, its publication date feed back as new knowledge.

Finally, output the article's wiki link — derive it from the saved path by taking the filename without the `.md` extension:

```
[[Article Title]]
```

For example, if the file was saved to `essays/on-focus.md`, output `[[on-focus]]`. Output this as the last line of your response so the user can copy it directly into any note.

</what-to-do>

<supporting-info>

## What is a beat

A beat is one move in the journey. It does one thing — sets a scene, lands a point, asks a question, drops an aside, twists the angle. Then it stops, leaving the reader at a place where the next beat can pivot.

A beat is sized by what it needs:

- A single sentence if that's all the move is ("And then nothing happened for three weeks.").
- A short paragraph if the move needs setup.
- Multiple paragraphs if the beat is a self-contained vignette, argument, or example.

If a "beat" needs five paragraphs and three subheadings, it's not a beat — it's two beats glued together. Split it.

## Writing one beat

Once a beat is picked, write _that beat only_ to the article file. Do not write the next beat.

Pull material from knowledge units to populate the beat. You can paraphrase, split, recombine, or quote directly. If a unit has dated opinions or time-anchored positions, use them — "as of 2024-03, X believed Y" is more honest than flattening it to a timeless claim.

**Drilling into source notes.** Knowledge units carry backlinks to the original notes they were compiled from. When the unit-level material feels thin — missing a concrete example, a specific quote, a vivid detail — follow the backlinks and read the source note directly. The source note is the unprocessed quarry; the knowledge unit is the refined extract. Use whichever layer serves the beat. If you pull something from a source note that isn't captured in its unit, note the gap — it may be worth compiling later.

**Partial reads.** `references/extract.md` documents `hylo extract` commands for reading outlines, sections, or line ranges without loading the full note. Use them when you don't need the whole file.

## Handling knowledge gaps

If a beat the user wants to write has no support in the palette, say so clearly: "The knowledge base doesn't have coverage here." Options:

1. Skip this beat and pivot to what is covered.
2. The user provides a fragment of raw material inline — treat it as a one-off quarry for this beat only, not a unit.
3. Pause the session, compile a new note, and resume.

Do not fabricate coverage that isn't in the knowledge units.

## Ending the journey

The article ends when the argument lands — not when the palette is exhausted. Most units will have content that doesn't make it in. That is fine; that is the point of having more understanding than any single article can hold.

## Writing rhythm

- Append one beat at a time. Never write ahead.
- Re-read the article file from disk before every write. Preserve user edits absolutely.
- If the user edits a previous beat substantially, let it change what comes next.
- If the user says "rewrite that beat" or "go back and try a different beat 3", do it — edit in place, leave the rest alone.

## The knowledge-writing loop

Writing is not separate from knowing. When the article is done, it contains synthesis that may not exist anywhere in the knowledge base yet — the act of writing created it. Compiling the article back closes the loop: the vault gets smarter from having written.

</supporting-info>
