---
name: re-pitch
description: "Side-route skill for when an explanation did not land. Use when the user says 'wait, what', 'I don't follow', 'say that again', or 'in plain English' — it diagnoses which kind of confusion occurred and re-states the same answer in controlled technical English with every domain term glossed on first use. Not for producing new work, retracting a wrong answer, or trimming a long answer the reader already understood."
sources:
  primary:
    - "A Survey and Classification of Controlled Natural Languages — Tobias Kuhn (Computational Linguistics 2014)"
  secondary:
    - "The Programmer's Brain — Felienne Hermans"
    - "Domain-Driven Design — Eric Evans"
    - "On Writing Well — William Zinsser"
---

# Re-pitch

Say it again so it lands. `/re-pitch` takes the answer that just failed and re-states the *same* content under a checkable restriction: short declarative sentences, active voice, the project's own domain terms, and a short in-line definition for every one of those terms the first time it appears.

## Overview

Re-explaining is not the same as summarizing. A summary assumes the reader understood and wants it shorter. `/re-pitch` assumes the reader did **not** understand, and that saying less of the same thing will fail the same way.

Two ideas do the work.

**Confusion has three distinct causes, and each has a different repair** (Hermans). A reader stalls because a term is unknown to them, because the situational facts are missing, or because too many steps arrived at once. Shortening only fixes the third. Applied to the first, a shorter answer still contains the unexplained term — now with less around it to infer from.

**A restricted language works only when its restrictions are checkable** (Kuhn). Caterpillar Fundamental English restricted vocabulary to under 1,000 words and was discontinued in 1982 because "the basic guidelines of CFE were not enforceable in the English documents produced" (p. 15). GM Global English pruned a 62-rule predecessor to 15 crisp rules and shipped without the checker that had enforced them — a stricter-looking rule set that was functionally advisory from day one (p. 35). "Write more simply" is that failure mode in one sentence. Step 4 below is this skill's checker, and it is the step that makes the rest real.

Two consequences follow from the same survey and shape the rules deliberately.

- **Domain terms outrank the vocabulary restriction.** Wycliffe EasyEnglish holds a hard lexicon cap and still admits out-of-list words *when they are glossed in-text on first use* (p. 35). That is the escape hatch this skill runs on, and it resolves the standing conflict between "use restricted vocabulary" and "use the project's ubiquitous language" (Evans) in favor of both.
- **Restricting harder buys nothing here.** Restrictions layered on top of ordinary English sit at the survey's Simplicity floor no matter how many are added: Basic English caps vocabulary at 850 words and E-Prime bans a single verb, and both land at S1 (p. 12). Effort spent tightening the rule list is wasted. Effort spent on the diagnosis and the gloss is not.

The goal type is comprehension, not precision. That is also where the evidence is strongest: controlled English "significantly improves text comprehension, with a particularly large effect for complex texts and non-native speakers" (p. 24) — which describes a reader who has just lost the thread of a technical explanation.

## Invocation Position

`/re-pitch` is a side-route skill. It sits outside the delivery pipeline and can fire during any stage of any skill.

Use `/re-pitch` when:

- the user signals non-comprehension — "wait, what", "I don't follow", "say that again", "in plain English", "you lost me"
- the user asks a question whose answer was already in the message they are replying to, which means that message did not land
- an explanation crossed several layers at once (schema plus migration plus rollout) and the reply came back narrow or off-target
- the reader is reading in a second language, or is new to this codebase's vocabulary

Use a plain answer instead when:

- the earlier answer was **wrong**, not unclear — correct it directly and move on, since re-pitching a wrong answer only makes the error more legible
- the reader understood and wants it **shorter** — trim it; a re-pitch is usually longer than what it replaces, because glosses cost words
- the reader understood and wants to go **deeper** — answer the deeper question
- nothing has been explained yet — this skill rewrites an existing answer and has no input without one

`/re-pitch` reconnects to the main workflow by returning control to whatever was in flight. It produces no file, no commit, and no issue.

## Process

### 1. Diagnose which confusion this is

Read the failed answer and the user's reply together. Name the dominant cause before writing anything — it decides where the effort goes.

| Cause | What the reader is missing | The repair |
|---|---|---|
| **Unknown term** | A word, acronym, or concept they have never met — `boundary map`, `tracer bullet`, `idempotent`, a repo-local coinage | Gloss it in-line. Give the definition before the sentence that relies on it. |
| **Missing situation** | They know the words, but not this system's current facts — which branch, which file, what already ran, what state we are in | Supply the specific facts. Name the branch, the file, the issue number, the command that ran. |
| **Too much at once** | They know the words and the situation, but the answer chained five steps into one paragraph | Split into ordered steps, one claim per sentence, in the order things happen. |

More than one cause is common. Rank them and repair the dominant one first.

Infer the cause rather than asking. The reader has already spent one round trip on an answer that failed, and "which part didn't you get?" spends another to learn something the transcript usually shows. Ask one question only when two causes are genuinely equally likely and the repairs pull in opposite directions.

### 2. Re-anchor before re-explaining

Open with one or two sentences that place the reader: where we are, and why this step exists. Then re-explain.

Anchor first even when the diagnosis is "unknown term." A reader who has lost the thread has usually lost the frame with it, and a definition delivered into a missing frame is one more unplaced fact.

Re-explain the part that failed. The parts that landed stay landed.

### 3. Write to the rules

Rules carry two strengths, following COGRAM's split between hard prohibition, hard restriction, and soft style guidance (pp. 29–30). A flat list overstates how binding it is; naming the strength per rule is what lets Step 5 check them.

**Hard — these hold in every re-pitch:**

- One claim per sentence, with its causal link stated rather than implied. "The hook blocks the write because the classification gate never ran" is one claim, and it stays one sentence. Two claims joined by "and" are two sentences.
- Active voice, with the actor named. Write "the hook blocks the write," not "the write is blocked."
- One meaning per word within a single answer. A word that meant "the PR branch" in paragraph one still means that in paragraph three.
- At most three words in a noun cluster. Break "slice issue boundary map contract" into a phrase with a preposition in it.

**Soft — prefer these, and yield when meaning needs the words:**

- Around 20 words per sentence for a procedure, 25 for a description. Read the number as a symptom rather than the rule: a sentence past it is usually carrying a second claim, and the repair is to find that claim, not to cut words until the count fits. A 30-word sentence carrying one claim and its reason is doing its job.
- At most six sentences per paragraph.
- Say it straight: "this breaks the build," not "this may potentially cause issues with the build."
- Prefer the shorter word where both are exact.
- Order steps the way they happen in time, and use the imperative when the re-pitch contains a procedure.

**Choppy is not the same as clear, and the caps are why.** They come from ASD-STE100, whose sentence limits were written for maintenance procedures — discrete physical actions, one per step, where a cap and a claim count amount to the same thing. An explanation is not a sequence of actions. It is a chain of claims with causal links between them, and those links live in exactly the subordinate clauses a hard word cap deletes. Enforced literally, the cap yields a wall of short declaratives that the reader has to reassemble into an argument: measurably compliant, and harder to read than the sentence it replaced. That is the survey's own evaluation caveat arriving in practice — benefit depends on "the precise problem domain, the background of the users, and—perhaps most importantly—the quality of the design of the language and its supporting tools" (p. 26), and a procedural cap imported into an explanatory domain fails the first of the three.

The standard itself is a licensed specification with an approved-word list this skill does not reproduce — see <https://asd-ste100.org> for the source of record. What is written above is the whole rule set `/re-pitch` claims; there is no larger hidden list an agent should try to recall.

### 4. Source the vocabulary from the project, then gloss it

Prefer the project's own term over any synonym for it (Evans). Look for the glossary in this order and stop at the first hit:

1. `UBIQUITOUS_LANGUAGE.md` — produced by `/ubiquitous-language`
2. `CONTEXT.md`, or the entry `CONTEXT-MAP.md` points to when the repo holds more than one
3. `README.md` and `CLAUDE.md`, for terms the repo uses without defining
4. the conversation itself, for terms coined during this session

Then gloss. **Every domain term gets a short in-line definition the first time it appears in the re-pitch — including terms the glossary already defines.** The glossary is a document the reader is not currently holding. A gloss is a clause, not a paragraph:

> The slice issue — one vertical unit of PRD work, sized for a single PR — carries a boundary map, which lists what it produces and what it consumes.

Keeping the project's term and adding the gloss is the move. Swapping the term for a plainer synonym trades one round of confusion for permanent vocabulary drift.

### 5. Check the draft before sending it

This is the step that separates this skill from advice. Run all four checks against the draft:

1. **Claims per sentence, then rhythm.** Find every sentence carrying more than one claim and split it at the seam. Sentence length is the search heuristic — start with the longest — but the fix is removing the second claim, not cutting words to reach a number. A long sentence carrying one claim passes.

   Then read the draft aloud. A run of short declaratives with nothing joining them fails this check too: the connectives went missing, and the reader now has to rebuild the argument the links were carrying. Restore them.
2. **Gloss coverage.** List every domain term in the draft. Confirm each one carries a definition at its first appearance. The list is exhaustive — check every term, not the first few.
3. **Voice.** Find every passive construction. Rewrite each with the actor in subject position, or confirm the actor is genuinely unknown.
4. **Diagnosis fit.** Re-read Step 1's dominant cause. Confirm the draft repairs *that* cause. A draft that is merely shorter, when the diagnosis was "unknown term," has not been repaired.

A draft that fails any check goes back to Step 3.

### 6. Stop

Send the re-pitch and return to the work that was in flight.

Add nothing else: no new scope, no summary paragraph restating what was just said, no offer of three further directions. The reader asked to understand one thing.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "They're confused, so I'll say it shorter." | Shortening repairs one of three causes. Against an unknown term it removes the surrounding context the reader was using to infer, and leaves the term. Run Step 1 first. |
| "The term is in `UBIQUITOUS_LANGUAGE.md`, so it's already defined." | The reader is not holding that file. Gloss on first use, every time — this is the rule Wycliffe EasyEnglish uses to admit out-of-list words at all. |
| "That word is jargon — I'll swap in a plain synonym." | Domain terms outrank the vocabulary restriction. Keep the project's term and gloss it. The synonym reads easier once and costs the shared vocabulary permanently. |
| "I'll add more restrictions so it comes out simpler." | Restrictions layered on ordinary English sit at the Simplicity floor regardless of count — Basic English's 850-word cap and E-Prime's single banned verb both land at S1. The diagnosis and the gloss are where the gain is. |
| "I'll ask which part they didn't understand." | That spends a second round trip after one already failed, usually to learn what the transcript shows. Infer it. Ask only when two causes are equally likely and pull opposite ways. |
| "I'll re-explain the whole thing from the beginning to be safe." | Re-anchor in one or two sentences, then repair the part that failed. Re-running the parts that landed buries the repair. |
| "Every sentence is under 20 words, so the draft passes." | The count is a symptom detector for a sentence carrying two claims, not the property being checked. Splitting a one-claim sentence to satisfy a number deletes the connective that made it one thought, and a wall of short declaratives is harder to read than what it replaced. |
| "I read the rules, so the draft follows them." | Unchecked rules are advisory rules, and advisory rules are why Caterpillar Fundamental English was discontinued. Run Step 5 against the actual draft. |
| "The original answer was wrong, so I'll re-pitch it more clearly." | Correct it. A clearer wrong answer is a better-understood wrong answer. |

## Red Flags

- The draft went out without Step 5 running against it.
- A domain term appears with no definition at its first use.
- A sentence carries two claims joined by "and".
- The draft reads as a wall of short declaratives with no connectives — the word count was optimized for, and the causal links were what it cost.
- The re-pitch opens with the explanation instead of the anchor.
- The project's term was replaced by a plainer synonym.
- A closing paragraph summarizes the re-pitch that precedes it.
- New scope, new suggestions, or new work appear in the re-pitch.
- The draft is shorter but the diagnosis was "unknown term" or "missing situation."
- The user signals non-comprehension a second time on the same point — go back to Step 1 and pick a different dominant cause.

## Verification

A run of `/re-pitch` is complete when:

- Step 1 named one dominant cause, and the draft repairs that cause
- the answer opens with one or two sentences of anchor
- every sentence carries one claim with its causal link intact, confirmed by reading the draft aloud rather than by word count alone
- every domain term carries a gloss at first use, checked exhaustively
- every passive construction was rewritten or its actor is genuinely unknown
- the project's terms survived intact, with no synonym substitutions
- nothing was written to disk, committed, or filed

## Handoff

- **Expected input:** the answer that did not land, plus the user's signal of non-comprehension. No artifact, issue, or branch is required.
- **Produces:** a replacement explanation in the conversation. No durable artifact — `/re-pitch` writes nothing to disk.
- **Comes next by default:** whatever was in flight. `/re-pitch` returns control to the interrupted skill or conversation at the point it paused.
- **Does not invoke:** any other skill. It reads `UBIQUITOUS_LANGUAGE.md`, `CONTEXT.md`, or `CONTEXT-MAP.md` when present.
- **May recommend:** `/ubiquitous-language` — when the same terms keep needing glosses across several re-pitches, the repo is missing a glossary and the fix belongs there rather than here. Recommend it; do not invoke it.
