---
name: de-ai-prose
description: Use when about to show any prose a human will read - docs, README, commit bodies, UI copy, store text.
---

## The rule

Readers can tell when a machine wrote the text, and it costs trust the same way sloppy code does. After you write any prose a person will read, read it back once and cut the tells. Plain words, varied sentences, say the thing instead of announcing you're about to say it.

## Fires when

About to show a human a README, a doc page, a commit or PR body, a changelog entry, a UI string, store copy — anything a person will read as writing rather than run as code.

## Tells to cut

- Signposting sentences: "Here's the thing.", "That's the point.", "This is the important part.", "By the end you'll know what, why, and how."
- Closers like "That's it." or "And that's all there is to it."
- Em-dash overuse as the default connector. The constant em-dash rhythm is a fingerprint.
- Parallel triads everywhere ("a texture, a config, a script"), over-balanced sentences, the list-of-three cadence.
- Arrow constructions in prose ("write one function -> the whole thing appears").
- A table for everything; bold sprinkled on every other phrase as decoration.
- Bullet lists where every item opens with a bold label ("**Fast:** ...", "**Simple:** ..."), parallel from top to bottom.
- Cutesy section names and peppy filler ("the payoff", "the ones that bite").
- Paragraphs that are all the same length and shape. Too tidy.

## How to apply

Plain, varied sentences. Some short. Let one run long and a little uneven, like a person typing.

Say it directly instead of signposting it. Use em-dashes rarely. Prefer periods, commas, "and". Vary connectors. Cutting an em-dash means rebuilding the sentence (a comma, a colon, parentheses, or two sentences), not swapping a different mark into the same joint.

Keep bold for genuinely key terms, not decoration. Drop a table where a sentence reads more naturally.

Read it back and ask: "would a tired engineer writing this actually phrase it this way?" If it sounds like a polished AI explainer, flatten it.

## Before / after

Before (AI voice):
> Here's the thing about our caching layer — it's fast, it's simple, and it's reliable. The payoff? Sub-millisecond reads.

After (human):
> The cache keeps reads under a millisecond. It's a plain in-memory map with a TTL, nothing clever.

What changed: dropped the signpost, dropped the triad, dropped the rhetorical question, said the concrete thing.

## Red flags

| Thought | Reality |
|---|---|
| "It's just a commit message" | A commit body is prose someone will read. Same pass. |
| "The user asked for polish" | Polish means clear, not machine-shiny. |
| "A table makes this clearer" | Sometimes. A table for everything is a tell. |

---

This skill must obey its own rule. The read-back pass applies here too. If this file sounds like AI, it has failed on its face.
