---
name: sk-style
description: Polishes the wording of a short's spoken script without changing what it says, by splitting long sentences, cutting filler and AI-slop phrases, naming the subject at the start of each scene, and replacing worn phrases. Use when the user says "tighten the script", "this sounds like AI", "this sentence is clunky", "make it punchier", "rewrite for flow", "too many adjectives", or when bun run lint reports §3b sentence-style warnings.
---

# sk-style: fix the words, not the meaning

**Announce:** "Using sk-style for <id>."

Rules: §3b (`docs/soul/01-voice-and-structure.md`); numbers and phrase lists in
`docs/soul/thresholds.json` (`maxWordsPerSentence`, `medianWordsPerSentence`,
`shortSentenceMaxShare`, `bannedPhrases`, `intensifiersMax`, `strongWords`). To
measure top channels in your niche instead of guessing: `docs/lessons/style-measurement.md`.

## Boundary

| Fix here | Go elsewhere |
|---|---|
| split a long sentence, cut filler, swap a connective | change or drop a **number** → `sk-facts` |
| reorder clauses inside a sentence | reorder **scenes** or change flow → `sk-brief` |
| name the subject in a scene's first line | add or remove a **claim** → `sk-facts`, then `sk-narration` |
| replace a worn phrase | the phrase is prescribed by a § → `sk-improve` |

If a polish pass loses a number, a caveat or a date, it is no longer a polish.
Stop and go back to the brief and the ledger.

## Steps

1. **Snapshot.** `bun run lint <id>` and keep the output. It is the baseline for
   step 6 and the to-do list for step 3.
2. **Read the whole script once without editing.** Editing on first read rewrites
   things that were already right.
3. **One pass per fault**, across the whole script, before the next fault. Mixing
   faults in one pass is how things get missed and meaning gets broken.
   1. *Long sentences* over `maxWordsPerSentence`: split at a clause; keep every fact.
   2. *Filler*: phrases in `bannedPhrases` and stacked intensifiers. Delete, or
      replace with the number from the ledger that the adjective was standing in for.
   3. *Scene openers*: a scene whose first word is a pronoun. Name the subject; the
      viewer may have just arrived.
   4. *Worn phrases*: a phrase used in earlier videos. Write a new one for this video.
   5. *The closing turn*: negate what the viewer believes, then give the real reason.
      Avoid parallel negation ("not X, not Y, not Z").
   6. *Read aloud*: where you run out of breath mid-sentence, it is still too long,
      even if lint passed.
   7. *Contrast pairs* ("one does X, the other Y"): has the viewer heard both names,
      and which ledger record states the contrast? The ledger holds single claims;
      a relation between two numbers is the easiest thing to invent and no check
      catches it.
4. **Re-run TTS:** `bun run tts <id>`. Mandatory, because `text` changed.
5. **Listen.** Does a split sentence sound clipped? Does a removed connective leave
   a gap?
6. **Lint again and diff against step 1.** §3b warnings must go down and **nothing
   else may appear**. A new fact or flow warning means you edited content, not words.
7. **A fault repeated across videos is a rule, not this video's bug.** Note it and
   use `sk-improve`; do not quietly fix it by hand in every script.

## Do not

- Drop a number to make a sentence shorter.
- Invent a relation between two facts to make a sentence balance.
- Add phrases to `bannedPhrases` mid-video. Changing a rule is `sk-improve`,
  and it edits the § too.
- Polish a video that is already posted. Posted videos are history.

## Exception

A verbatim quote from a real person keeps their words even if it breaks
`maxWordsPerSentence`. Say so in the brief so the next pass does not "fix" it.

Next: `sk-scene` if scene lengths changed, otherwise `sk-render`.
