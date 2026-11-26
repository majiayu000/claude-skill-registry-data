---
name: plain-writing
description: Write or edit prose in plain language - lead with the point, cut backstory, signpost, then fix voice, verbs, fluff, and grammar. Use when the user asks to write, rewrite, tighten, simplify, de-jargon, proofread, restructure, or "plain-writing" any text (docs, emails, Slack messages, PRDs, design docs, READMEs, proposals, slides, commit messages).
license: MIT
---

# Plain Writing

Produce prose that a reader understands on the first pass and can act on. Two modes:

- **Draft mode** — the user wants new text. Write it plain from the start.
- **Correct mode** — the user supplies existing text. Rewrite it and show what changed.

If the user does not say which, infer: existing text present → correct mode.

Work in two layers, structure first. A perfectly plain sentence in the wrong place still fails the reader.

- **Layer 1 — structure**: what the point is, where it goes, what the reader must do. See `references/structure-and-tone.md`.
- **Layer 2 — sentences**: the five principles below.

## Layer 1: get the structure right first

Do this before touching any sentence.

1. **Decide the main point.** Clear thinking is the bottleneck, not word choice. "Bottom line up front" assumes you already know what the bottom line is. Answer: what do I want out of this, what is the single most important thing, what action does the reader need to take? If the source text cannot answer these, that is the real problem — say so.
2. **Main point above, context below.** Never jumble the ask, the backstory, and the detail together. Separating them lets the reader take as much context as they need and stop.
3. **Aim for a 2–3 sentence core.** One sentence causes analysis paralysis; ten becomes a monologue. Two or three forces the thesis plus the ask.
4. **Cut to minimum viable backstory.** Start right before you get eaten by the bear. Backstory should be 10–20% of the message, not 80%. Skip the play-by-play; offer it if asked.
5. **Signpost.** Use headers, topic sentences, numbered lists, and transition words (*for context*, *because*, *going forward*, *this means*, *to be clear*, *as a next step*) so the reader never wonders where you are taking them. Number your questions so none get skipped.
6. **State the ask explicitly.** Never make the reader guess whether action is required or what happens next. Label FYIs as FYIs.
7. **Robot-voice the tone.** Read the draft flat and monotone. Anything that lands cold, harsh, or entitled gets rewritten — the words carry all the goodwill your face would have.

**Concise means dense, not short.** A 1,500-word memo can be concise; a 150-word one can be fluff. Use as many words as necessary and no more. Never delete a fact, caveat, or number to hit a length. Some ideas cannot be reduced further, and squeezing them past that point misrepresents them. Clarity overrides conciseness whenever they conflict.

## Layer 2: the five principles

Apply in this order. Each pass feeds the next.

### 1. Use the active voice
Word order **subject → verb → object**. The actor comes first.

- Active: *The manager reviewed the policy.*
- Passive: *The policy was reviewed by the manager.* (longer, actor demoted)
- Passive with no actor: *The policy was reviewed.* (reader cannot tell who)

Test: find the main verb, then find who performed it. If the actor comes after the verb, or is missing, it is passive.
Mnemonic: **S–V–O: it's a go. O–V–S: make 'em guess.**

Passive is acceptable when:
- the object is genuinely the focus (*The buildings are leased for six months.*)
- the actor is unknown or irrelevant (*The original code was written five years ago.*)
- naming the actor would sound like blame (*Two items were left out of the report, but we will add them in the next version.*)

Never leave the actor implicit in text that assigns work, responsibility, or expectations.

### 2. Use simple words and simple sentences
Prefer the simplest word that carries the exact meaning. Simpler is not always shorter — it is the most **precise** word. Keep a complex word only when precision requires it.

One concept per sentence. If a sentence contains more than two actions, split it. Load the first sentence with what the reader must do; put detail in the next.

See `references/word-substitutions.md`.

### 3. Choose strong verbs
Strong verbs are concrete and precise. Weak verbs are abstract and need propping up.

Strengthen the verb by deleting what props it up:
- **Helper verbs** (*has, had, have, can, will be able to*) — *You have to enter your username before you can continue* → *To continue, enter your username.*
- **Infinitives** (*to propose, to prevent*) — *I would like to propose that we adopt this plan* → *I propose we adopt this plan.*
- **`to be` openings** (*there are, it is, it was*) — *There are five benefits to adopting this tool* → *This tool has five benefits.*
- **Adverbs** — they hide imprecision. *The team will quickly finish the report* → *The team will finish the report within one day.* Delete the adverb and the sentence forces you to say what you mean.

Keep a helper verb when tense actually carries meaning (*We have had good luck with this tool* ≠ *We had good luck with this tool*).

### 4. Delete words that add no meaning
If a word or phrase adds no meaning, delete it.

- **Fluff intensifiers**: really, very, totally, particularly, especially, definitely, actually, generally, basically, for all intents and purposes, kind of, sort of, type of, individual, specific.
- **Throat-clearing openers**: *I'm writing this email because I want to ask you…*, *It has come to our attention that…*, *At this time it is recommended that…* → say the thing.
- **Words that state the obvious**: *We implemented a successful solution* — a solution that failed is not a solution.
- **Negative framing**: say *do this*, not *don't do that*. A reader told only what to avoid still has to work out what to do.
- **Jargon**: acceptable only when every reader knows it and it is the shortest accurate route. Otherwise replace it or define it on first use.
- **Clichés**: no place in professional writing and untranslatable. *ballpark figure* → *approximate*; *run of the mill* → *standard*; *think outside the box* → *be original*.
- **Redundancies**: *various differences* → *differences*; *reply back* → *reply*; *future plans* → *plans*; *end goal* → *goal*; *past experience* → *experience*.

Test: read the sentence without the candidate words. If it still means the same thing, they were fluff.

**Exception — signpost words are not fluff.** *For example*, *because*, *for context*, *this means*, *to be clear*, and *as a next step* cost a few words and repay them by showing the reader the structure and logic. Keep them. Fluff adds no information; signposts add navigation.

See `references/fluff-and-redundancy.md`.

### 5. Correct grammar, spelling, and punctuation
Errors do not just look careless — they change meaning and make readers doubt the content.

- **Subject–verb agreement**: match the verb to the true subject, not the nearest noun. *The list of code examples **is** included in the report.*
- **Prepositional phrases**: place them next to what they modify. *We received the report from the data center about issues with the inventory on August 4* is ambiguous — move the date to the front or attach it to the noun.
- **Commonly confused words**: than/then, it's/its, your/you're, affect (verb) / effect (noun), i.e. (that is) / e.g. (for example), historic/historical.
- **Punctuation**: periods end sentences; commas guide flow; use the serial comma. Simple sentences need few commas — another reason to write them.

See `references/grammar-traps.md`.

## Workflow

**Draft mode**
1. Answer the Layer 1 questions: reader, purpose, main point, required action.
2. Lead with the point. Put context below it. Keep backstory to the minimum viable amount.
3. Draft in S–V–O, one idea per sentence, with signposts at the memo, paragraph, and sentence level.
4. Run the correct-mode checklist over your own draft, including the robot-voice tone pass.
5. Return the text only — no commentary unless asked.

**Correct mode**
1. Read the original and identify its intended meaning. Never change meaning to make a sentence simpler; if the original is ambiguous, flag it instead of guessing.
2. **Structure pass first**: is the main point on top? Is there backstory to cut? Is the ask explicit? Does it need signposts or numbering? Restructuring usually beats any sentence-level edit.
3. **Then five sentence passes in order**: voice → words and sentences → verbs → fluff → grammar.
4. **Tone pass**: read it in a robot voice and soften anything that lands cold or demanding.
5. Preserve the author's register and any required terminology, names, numbers, links, code, and formatting.
6. Return:
   - **Rewrite** — the full corrected text, ready to paste.
   - **What changed** — a short bullet list, structure changes first, then sentence-level edits. Skip the obvious ones.
   - **Open questions** — anything ambiguous you refused to guess at, and any missing information the reader would need.
   - **Word count** — original → new.
7. Do not pad the rewrite. If the best edit is a deletion, delete. If the best edit is *adding* a missing ask or a missing criterion, add it and flag it.

## Rules
- Never invent facts, numbers, names, commitments, or opinions that are not in the source.
- Never strip technical precision to hit a simpler word. Clarity beats brevity every time they conflict.
- Do not cut a detail just because it is a detail. Cut the *wrong* details — the ones the reader does not need to sort. Keep the ones that carry the decision.
- Preserve markup, code blocks, and identifiers exactly.
- Shorter is the usual outcome, not the goal. Density is the goal.
- If a passage is already plain, say so and leave it alone.

## References
- `references/structure-and-tone.md` — main point above / context below, minimum viable backstory, signposting words, robot voice, context calibration (Wes Kao).
- `references/word-substitutions.md` — complex → simple word table, sentence length.
- `references/fluff-and-redundancy.md` — fluff, clichés, redundancy tables.
- `references/grammar-traps.md` — agreement, prepositions, confused words, punctuation.
- `references/before-after.md` — worked rewrite examples.
