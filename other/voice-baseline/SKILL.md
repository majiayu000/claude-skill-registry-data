---
name: voice-baseline
description: Measure your own writing corpus for the words and sentence shapes you over-use, so an agent writing in your voice stops amplifying your tics into a style. Produces a counted baseline file and checks any new draft against it. Use when an agent's drafts start sounding like a caricature of you, before publishing anything written in your voice, or every ten new pieces to re-measure.
---

# voice-baseline

An agent writing in your voice does not only sample the median of the internet. It
samples the median of you, from the pieces and rules and memory files in its context,
and it regresses toward your most frequent choices because those are the highest
probability tokens in your corpus. A word that was a choice at one use comes back at
five. Then the fifth use teaches the next draft, and the tic becomes the style.

Generic ban lists cannot catch this, because the words are yours and they are not on
anyone's list. Measure instead.

## Run it

```bash
python3 scripts/census.py PATH/TO/YOUR/WRITING --out voice-baseline.md
python3 scripts/census.py PATH/TO/YOUR/WRITING --check DRAFT.md
```

The census walks a directory of your own finished pieces and reports word counts with
a per-file rate, sentence-shape counts, sentence openers, and heading first words.
`--check` compares one draft against those rates and prints only what sits above them.
Exit code 1 when something is above baseline, so it fits a pre-publish script.

Keep the output file next to your rules so the agent reads it before it writes.

## What it measures

**Words.** A watchlist of praise and emphasis words, counted with word boundaries and
reported per file. Read the per-file rate: a word used twice per file is a habit, and
the same word at eight in one draft is the draft's problem. Edit `WATCH` in the
script to add your own suspects; the point is that the list ends up specific to you.

**Paragraph-ending verdict sentences.** "The fix was one line." A concrete noun, a
past-tense verb, a short predicate, parked at the end of a paragraph so it lands like
a ruling. One per piece at most, and only when it carries a fact the paragraph has not
already delivered.

**Kicker closers.** "That is the point." "That is all a title is for." A closing line
that restates the piece as an aphorism. The cap is zero.

**Endings.** How many pieces close on a question to the reader. Most of them means the
question has become a formula.

**Sentence openers and heading first words.** These are where a personal tic hides
best, because each instance reads fine. If a third of your headings begin with the
same word, you have a template. In one real 27-file archive the census found 53
headings starting with "The", the exact shape people name as an AI tell, learned from
the author's own archive.

## How to read the result

The census counts; it does not judge. For each flagged word or shape, decide whether
it is your voice or your mode:

- **Voice.** The word carries meaning the sentence needs, or the rhythm is yours and
  deliberate. Keep it, and note the exception so the next check does not re-raise it.
- **Mode.** The word is praise, emphasis, or padding, and removing it changes nothing
  for the reader. Cut it, or replace it with the behaviour it was gesturing at.

Fix the shapes by cap rather than by ban: one verdict sentence, zero kickers, no
default question ending, one narrative heading pattern per piece.

## Re-measure

Run the census again after roughly ten new pieces. A tic you fixed should fall. A new
one will have appeared, usually the word you reached for while avoiding the last one,
which is the same substitution the model makes when a single word is banned.

Pair with `slop-gate` for the universal tells and `no-ai-slop` for the structural ones
a regular expression cannot see.
