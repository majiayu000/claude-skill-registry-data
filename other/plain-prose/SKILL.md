---
name: plain-prose
description: Write clear, plain prose, and strip register-jargon out of text that already has it. Use this whenever writing prose that should sound like a person talking (essays, web copy, emails, docs, explanations, scripts) AND whenever cleaning up text that reads like a whitepaper, a consulting deck, or systems-engineering English. Trigger it when the user asks to make writing "clearer," "plainer," "simpler," "cleaner," "less corporate," "less jargony," or "less abstract"; when they say text sounds like it is "performing intelligence," showing off, or hiding behind big words; when they flag register-marker words like "substrate," "load-bearing," "artifact," "leverage," "scaffold," "surface," "primitive," "robust," or "unpack"; and proactively whenever about to produce prose where being understood matters more than sounding sophisticated. Do not wait for the word "jargon" — abstract, consultant-flavored writing is itself the cue.
user-invocable: true
allowed-tools: Read, Edit, Write
---

# Plain Prose

Write so a person understands you on the first read. Clean text that has drifted into jargon. These are two sides of one skill, because both depend on hearing the same thing: prose that has stopped communicating and started signaling.

## The one idea to hold

The enemy is not a word. It is a **register** — a dialect that certain professions slip into, where the writing performs intelligence instead of delivering it.

This matters because a banned-word list does not work. Ban "substrate" and the writing reaches for "scaffold." Ban "scaffold" and it reaches for "primitive." You have treated a symptom and the disease walks on. So the skill is to hear the *register* and write outside it — not to memorize a blocklist.

The register has a clear tell. It is built mostly from **dead structural metaphors borrowed into abstract writing**: words from architecture, geology, engineering, and archaeology, used to describe things that are not buildings, rock, machines, or dug-up objects. "Load-bearing" is a wall. "Substrate" is the layer under soil. "Artifact" is something pulled from a dig. Each one smuggles in a feeling of solidity and rigor. None of them is making you see a picture anymore. They have been used so often in one professional accent that they no longer mean; they just mark the tribe.

Two other things the register does, worth naming because you will catch them by feel:

- **It climbs the abstraction ladder.** It prefers the category to the thing. "The relational substrate" instead of "the relationships." "A trust artifact" instead of "a page that proves you can be trusted." Every climb sounds more sophisticated and tells the reader less, because it trades a picture for a label.
- **It reaches for status, not clarity.** The deep motive under the jargon is to sound smart. That is the real thing to write against. When a sentence is working to impress, it has stopped working to be understood.

## The decisive test: costume or term of art?

This is the most important rule in the skill, because it keeps the skill from dumbing writing down.

Not every technical word is jargon. Some are the *right* word and the only word. "Substrate" in chemistry, "artifact" in machine learning or archaeology, "load" in electrical engineering — these are terms of art doing real work, and replacing them would lose meaning. Keep them.

So before cutting any suspect word, run one test:

> **Could you swap it for a plainer word with no loss of meaning?**
> - If **yes** → it was costume. Swap it.
> - If **no** → it is a real term of art. Keep it.

"The relational substrate of the network" → swap "substrate" for "basis" or just say "the relationships," and nothing is lost. Costume. Cut it.
"The enzyme binds to its substrate" → no plainer word means the same thing. Term of art. Keep it.

Apply this every time. It is the difference between clear writing and merely simple writing.

## Writing clean from the start

Five working habits. They are tests you run as you write, not rules to memorize.

1. **Prefer the picturable noun.** For any abstract noun, ask: *could a sharp fifteen-year-old picture it?* If not, replace it with something they could. "The page," not "the artifact." "The relationships," not "the relational layer."

2. **Use the simplest word that does the job.** Not the simplest word, period — the simplest one that still carries the meaning. "Use," not "leverage" or "utilize." "Build on," not "scaffold." "Show," not "surface."

3. **Say it the way you would say it out loud, to one person.** This is the single best clarity test there is, because speech naturally refuses this vocabulary. You would never tell a friend at a table about "the relational substrate." You would say "the relationships." The mouth is more honest than the keyboard. Write toward the mouth.

4. **Cut anything that is performing.** Read the sentence back and ask: *is this communicating, or is it trying to sound smart?* If it is reaching for status, cut it or say it plainly. Confidence in plain words beats insecurity in big ones.

5. **Short sentences carry hard ideas better than long ones.** When the thought is complex, the sentence should get simpler, not fancier. Break it up. Let it breathe.

## Cleaning up text that already has it

When fixing existing text, work in this order. Do not rewrite wholesale on the first pass — diagnose first, or you will lose the author's meaning and voice.

1. **Read it once for the register.** Notice where it stops sounding like a person and starts sounding like a deck or a spec. Mark those spots. The feeling of "this is showing off" is reliable; trust it.

2. **Find the suspect words.** Scan for the register markers (see `references/register-markers.md` for the watchlist by domain). Underline each one.

3. **Run the costume-or-term-of-art test on each.** Keep the real terms. Mark the costume for replacement. Do not skip this — it is what protects genuine precision.

4. **For each costume word, restore the concrete thing.** Replace the abstract category with the specific, picturable noun underneath it. Often this means asking "what actual thing is this standing in for?" and naming that.

5. **Read it back out loud.** Anywhere your mouth stumbles or your ear hears "performance," fix it. Shorten. Plain-word it. This pass catches what the eye misses.

6. **Preserve the author's meaning and voice.** Clarity is not flattening. Do not strip real precision, do not remove genuine technical terms, and do not erase the writer's personality. You are removing costume, not character.

## A few before / afters

**Costume → plain (swap loses nothing):**
- "the relational substrate of the network" → "the relationships in the network"
- "this is the load-bearing claim" → "everything depends on this claim"
- "we built a trust artifact" → "we built a page that proves we can be trusted"
- "leverage the existing infrastructure" → "use what's already there"
- "surface the key insight" → "show the key point"
- "a robust, scalable approach" → "an approach that holds up and grows"
- "let's unpack this" → "let's look at this closely"
- "operationalize the framework" → "put the framework to work"

**Term of art → keep (no plainer word exists):**
- "the enzyme and its substrate" — keep.
- "the build produced three artifacts" (software, where "artifact" is the precise name for a build output) — keep.
- "a load-bearing wall" (literal architecture) — keep.

The pattern: when the word names a real, specific thing in its home field, it stays. When it has wandered into abstract writing to sound rigorous, it goes.

## The one-line version

Write the way you would say it out loud to one person. Prefer the thing you can picture over the category it belongs to. Use the simplest word that still carries the meaning. And whenever a sentence is reaching to sound smart, cut the reach and say the thing.
