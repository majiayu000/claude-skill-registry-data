---
name: reader-level
owner: baseline
description: Bring documentation prose down to a high-school reading level without losing precision. Runs after the content is written and before humanizer. Targets grade 9 on four measures — sentence length, vocabulary, clause load and jargon density — and carries the rewriting moves that actually shift them.
---

This skill exists because a page can pass every style check, state every fact correctly, and still be hard to read. The failure is not bad writing. It is writing pitched several grades above the reader, built out of long clauses and Latinate abstractions that each cost a beat to unpack.

> **Plain language is not dumbing down.** The research is consistent: higher-literacy readers *prefer* plain prose, because it gets them the information faster. An expert reading a dense paragraph is not impressed; they are just spending time they did not need to spend.

---

## The target

Grade **9** on the Flesch-Kincaid scale, and all four measures below. Run:

```
node .claude/skills/reader-level/score.mjs --target 9 <rendered page>
```

| Measure | Limit | What it catches |
|---|---|---|
| FK grade | 9 | Sentence length and syllable count |
| Hard words | 10% | Vocabulary the reader has to decode |
| Clause load | 0.4 / sentence | Subordination the reader has to hold |
| Jargon load | 1.2 / sentence | Identifiers per sentence |

**One measure alone is gameable, which is why there are four.** Flesch-Kincaid is *only* average sentence length and average syllables per word. A page of twelve-word sentences made of abstractions scores as middle-school and still reads hard, because the reader's cost is carrying unfamiliar concepts, not counting syllables. That is exactly how a page can score grade 7 and feel like a journal article.

---

## The seven moves

Ranked by how much they shift the score.

### 1. One idea per sentence

Split at every `which`, `so that`, `because`, `and when`. Two plain sentences beat one correct sentence with a hinge in the middle.

> Reach for an epic when one feature decomposes into several pieces that can land separately, and when the scouting and research behind them is shared.

> Use an epic when one feature splits into pieces that can ship separately. They also need to share the same background work.

### 2. Concrete verb over abstract noun

Nouns ending `-tion`, `-ment`, `-ance`, `-ity`, `-ness` are usually verbs in disguise. Turn them back.

- "performs a validation of" → "validates"
- "the escalation of a slice" → "escalating a slice", or better, "when a slice is risky"
- "on completion of the run" → "when the run finishes"

### 3. Anglo-Saxon over Latinate

Same meaning, one less beat to decode.

| Replace | With |
|---|---|
| amortize | spread the cost |
| decompose | split, break up |
| utilize | use |
| facilitate | help |
| require | need |
| provide | give |
| obtain | get |
| commence | start |
| terminate | end |
| subsequently | later |
| additional | more |
| sufficient | enough |
| approximately | about |
| therefore, consequently | so |
| however, nevertheless | but |
| regarding, concerning | about |
| prior to | before |
| in order to | to |

### 4. Kill metaphor-as-jargon

A metaphor the reader must decode is worse than the plain thing. "The discovery tax" is a coined term doing analytical work it never defines. Say what actually happens: "you pay for the same research twice".

Watch for: *tax, surface, lever, seam, floor, ceiling, spine, ladder, rail* used as nouns for abstractions.

### 5. Address the reader

"You" is shorter and clearer than a passive or an impersonal construction.

- "A child cannot be started before the epic is approved" → "You cannot start a child until the epic is approved"
- "The test is whether a second workflow would re-read the same code" → "Ask whether a second workflow would read the same code"

### 6. Front-load the point

Put the conclusion in the first clause. A reader who stops halfway should still have the answer.

- "Because the spec, scout and research stay resolvable for children, the bundle commits live" → "The bundle commits live. Children need the spec, scout and research to stay where they are."

### 7. Cut the wind-up

"It is worth noting that", "The thing to understand is", "What this means is". Delete and start at the noun.

### 8. Plain means familiar, never vague

The move that goes wrong most often. Reaching for a simpler word, a writer picks a *more general* one, and generality is not simplicity — it costs the reader the work of figuring out what was meant.

> An epic splits into **pieces**.

> An epic splits into **tasks**.

"Tasks" is the shorter word, the more common word, *and* the correct one. Every field has a standard everyday word for its ordinary things, and it is nearly always both plainer and more precise than the vague word a writer substitutes when trying to sound accessible.

**Before replacing a term, check what the product and its field already call the thing.** Grep the codebase. If `workflows.jsonl` says `task` ninety-nine times, the word is `task`.

Vague nouns to distrust: *piece, part, thing, item, element, aspect, area, component, entity, artifact, unit* — when used for something that has a real name.

This does not conflict with "What NOT to simplify" below; it is the same rule from the other side. That section says keep a real term. This one says when you *do* need an everyday word, take the field's everyday word rather than inventing a blander one.

---

## Paragraphs

- One idea per paragraph. If the second half introduces a new subject, split it.
- Three or four sentences is a normal paragraph. Six is a wall.
- Topic sentence first. The rest supports it.
- A paragraph that a reader can skip without losing the thread should probably be cut.

---

## What NOT to simplify

Precision beats plainness when the two conflict.

- **Real names.** `epic_approval_guard`, `.claude/state/epic/`, `PreToolUse`. Never paraphrase an identifier.
- **Exact numbers and paths.** "about ten" is worse than "nine" when nine is the number.
- **Quoted source text.** A description lifted from a `SKILL.md` or a config file belongs to its source. Mark it `class="excerpt"` and leave it alone.
- **Terms the product actually uses.** If the CLI calls it a "manifest", call it a manifest. Inventing a friendlier word for a real term costs the reader when they meet the real one.

Simplify the prose around the terminology, never the terminology.

---

## The pipeline

Order matters and is not optional.

1. **Write the content.** Facts first, from source material. Get it right before getting it readable.
2. **`Skill(reader-level)`** — this skill. Apply the seven moves. Then run `score.mjs` and keep going until all four measures pass.
3. **`Skill(humanizer)`** — last. Removes AI patterns from the simplified text.

**Why this order.** Humanizer works on the words that will ship. Simplifying afterwards would reintroduce phrasing humanizer had already cleaned, and the AI-pattern pass would need repeating. Simplify first, de-slop second.

When invoked from `technical-writer`, this sits between the draft and humanizer:

```
sources → technical-writing → reader-level → humanizer → measure.mjs + score.mjs
```

**Raise the target when the page is documentation.** `technical-writer` calls this skill with `--target 11` for reference and explanation, and `--target 10` for tutorials and how-tos, rather than the default 9. Professionally-written documentation measures at grade 10.7; a target of 9 pushes a page below that band and strips the qualifying clauses that carry the meaning. This skill is the ceiling, and `technical-writing` sets the floor.

Close with a receipt naming the score before and after. A page that never scored is not done.
