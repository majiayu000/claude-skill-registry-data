---
name: copy-review
description: Review and improve marketing copy that already exists - a page, an email, an ad, a post, a deck slide - using a fixed six-pass edit. Produces a marked-up diagnosis, a rewritten version, and a per-pass score so the user can see what changed and why. Use when the user says "review this copy", "improve this", "make this better", "tighten this", "edit this page", "does this copy work", "why is this flat", "punch this up", "proofread", or pastes existing copy and asks for feedback. Also use when copy is on-brand but underperforming. For writing new copy from nothing, see content-writer or landing-page-writer. For diagnosing a page's conversion problem beyond its words, see page-cro. For voice consistency rules, see brand-context.
metadata:
  grounded_in:
    - "On Writing Well - William Zinsser"
    - "Style: Lessons in Clarity and Grace - Joseph Williams"
    - "Ogilvy on Advertising - David Ogilvy"
    - "Everybody Writes - Ann Handley"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
  writes:
    - output/copy-review/
---

# copy-review

Improves copy that already exists. Most real requests are "here is our page, make it better", not "write me a page from nothing". This skill never starts from a blank sheet.

The output is always three things: what is wrong and where, the rewritten copy, and a score per pass so the user can see the delta rather than trusting an assertion.

## The six passes

Run in this order. Order matters, because cutting clutter before fixing the claim just produces a shorter wrong sentence.

| # | Pass | Question | Grounded in |
|---|---|---|---|
| 1 | **Claim** | Is the central promise specific, true, and about the reader? | Ogilvy, *Ogilvy on Advertising* |
| 2 | **Evidence** | Is every claim backed, or is it asserted? | Ogilvy, and Cialdini on proof |
| 3 | **Clarity** | Can a first-time reader parse each sentence once? | Williams, *Style: Lessons in Clarity and Grace* |
| 4 | **Clutter** | What can be deleted without loss? | Zinsser, *On Writing Well* |
| 5 | **Rhythm** | Does it sound like a person, read aloud? | Handley, *Everybody Writes* |
| 6 | **Voice** | Does it match this brand specifically? | `knowledge/brand/voice.md` |

## Process

1. **Load context.** Read `knowledge/brand/voice.md` and `knowledge/icp/personas.md`. If voice is missing, say so once and continue in generic mode with a warning in the output, rather than stopping. Never claim brand-matched output without the voice file.

2. **Establish the job.** Ask, or infer from the copy, and state it back in one line: what is this copy for, who reads it, what should they do next. If the user cannot say what action it drives, that is finding number one and it outranks every word-level fix.

3. **Score the original** on each pass, 0 to 5. Show the table before rewriting so the user sees where the problems actually are.

4. **Run the passes in order.** For each, quote the specific line, name the problem, give the fix.

5. **Produce the rewrite** in full, not as fragments.

6. **Score the rewrite** on the same six, in the same table, and state the delta.

7. **Save** and offer next steps.

## Pass detail

### Pass 1: claim
- What is the single promise? If you cannot state it in one sentence, the copy has no claim, it has a topic.
- Is it about the reader's outcome or the company's activity? "We built an AI-powered platform" is activity. "Close the books three days sooner" is outcome.
- Is it specific enough to be falsifiable? A promise nobody could disagree with is not a promise.
- Could a competitor make the identical claim? If yes, flag it and check `knowledge/markets/positioning.md` for a differentiated angle.

### Pass 2: evidence
- Tag every claim as `PROVEN` (number, named customer, source cited), `ASSERTED` (stated with nothing behind it), or `VAGUE` ("industry-leading", "seamless").
- Every `ASSERTED` claim needs one of: a number, a named customer, a demonstration, or deletion.
- Never invent the number. Write `[NEEDS INPUT: conversion figure]` and keep going.
- Target: no `VAGUE` claims survive, and at least one `PROVEN` claim appears above the fold or in the first paragraph.

### Pass 3: clarity
- Prefer a concrete subject doing a concrete action. Abstract subjects with buried verbs are the most common cause of copy that is grammatical and unreadable.
- Flag: nominalisations ("the implementation of" for "implementing"), passive voice hiding the actor, sentences over 30 words, and any sentence needing two reads.
- Flag undefined jargon and acronyms on first use.

### Pass 4: clutter
- Delete qualifiers that weaken without adding: very, really, quite, just, actually, simply, basically.
- Delete throat-clearing openers: "In today's fast-paced world", "It's no secret that", "We're excited to announce".
- Collapse redundant pairs: "plan ahead", "end result", "free gift".
- Target a 15 to 30 percent word reduction on most business copy. If the draft cannot lose 15 percent, say so, do not pad the cut to hit a number.

### Pass 5: rhythm
- Read it aloud. Mark anywhere you would not naturally pause where the punctuation says to.
- Vary sentence length deliberately. A run of same-length sentences flattens, whatever the words are.
- Check the first three words of each paragraph. If several start the same way, vary them.
- One idea per paragraph. Two ideas means two paragraphs.

### Pass 6: voice
- Check against every rule in `knowledge/brand/voice.md`: tone positions, words we use, words we never use, punctuation rules.
- Compare the rewrite against the on-brand and off-brand examples in that file. Say which it reads closer to.
- Voice is the last pass on purpose. Fixing voice on a sentence that is about to be deleted is wasted work.

## Output format

```markdown
# Copy review: [what it is]

**Job:** [what this copy is for, who reads it, what they do next]
**Source:** [where the copy came from]
**Voice file:** [loaded | MISSING - output is generic]

## Score

| Pass | Before | After |
|---|---|---|
| Claim | N/5 | N/5 |
| Evidence | N/5 | N/5 |
| Clarity | N/5 | N/5 |
| Clutter | N/5 | N/5 |
| Rhythm | N/5 | N/5 |
| Voice | N/5 | N/5 |
| **Total** | **N/30** | **N/30** |

Word count: [before] to [after] ([N]% reduction)

## Findings

### 1. [Pass name]: [one-line problem]
> [quoted original line]

[why it fails, one or two sentences]

**Fix:** [the replacement]

[repeat, worst first, not in pass order]

## Rewrite

[the full rewritten copy, ready to paste]

## What I could not fix
[anything needing information only the user has, each as [NEEDS INPUT: ...]]
```

Order findings worst-first, not pass-order. The reader should hit the biggest problem in the first line.

## Self-check before saving

- Every finding quotes the actual original line, never a paraphrase
- Every `ASSERTED` claim in the rewrite is either proven, deleted, or tagged `[NEEDS INPUT]`
- No invented statistic, customer name, or quote anywhere in the rewrite
- The rewrite is complete and pasteable, not a list of fragments
- The after-score is justified by the findings, not inflated. If a pass did not improve, score it flat and say why
- If the voice file was missing, the output says so explicitly

## Rules

- **Never invent evidence to fix an evidence problem.** That is the one failure mode of this skill that damages the user, because fabricated proof reads as the most improved part of the rewrite.
- Preserve any legal, compliance, or regulatory line exactly unless the user says it can change. Flag it, do not edit it.
- If the copy is already strong, say so and score it honestly. A review that manufactures findings to look useful trains the user to ignore the next one.
- If the real problem is the offer rather than the words, say that plainly and point at `/positioning-doc` or `/page-cro`. Better copy on a weak offer is a small win presented as a large one.
- Save to `output/copy-review/<DD-MM-YYYY>-<slug>.md`.

## Related skills

- `/page-cro` when the page underperforms for reasons beyond the words: layout, CTA hierarchy, friction, trust
- `/content-writer` and `/landing-page-writer` to write new copy rather than fix existing
- `/brand-context` if `knowledge/brand/voice.md` does not exist yet
- `/ab-copy-writer` to turn the top finding into testable variants
