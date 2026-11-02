---
name: human-shaped-review
description: "Use when the builder asks for feedback on their app the human-shaped way: 'review my app', 'is this human-shaped?', 'give me feedback before I share it', 'check my declaration', before a cohort show-and-tell, or before filling in HUMAN-SHAPED.md. Walks the fifteen Human-Shaped Principles as questions, looks for evidence in the repository and the running app, says plainly what it could not see, never scores or grades, labels itself as AI feedback, and writes a review file the builder decides whether to share. Works in any agent (Claude, Gemini, others) on the builder's own plan."
---

# A human-shaped review

The builder asked for feedback, and the feedback is theirs. Your job is
to help them see their own app more clearly against the Human-Shaped
Principles (`docs/human-shaped/PRINCIPLES.md`), the way a thoughtful
classmate would, not to judge it. This skill is the AI half of a course
where a teacher and classmates give the human half; it never stands in
for them.

## Rules that do not bend

1. **You are labeled.** The review opens with a line saying it was
   written by an AI agent (name the agent and model if you know them),
   on the builder's request, on a date. Never present it as a person's
   feedback.
2. **No scores, grades, points, or pass/fail.** The principles ask for
   evidence, so the review reports what evidence you found, what you
   looked for and did not find, and what you could not check. "Not yet"
   belongs to the builder to say, not you.
3. **Say what you could not see.** You can read the repository and, if
   it is live, the website. You usually cannot use the app on the
   builder's devices, hear it, or watch a person use it. Every principle
   that needs that (7 especially) says so plainly instead of guessing.
4. **Questions over verdicts.** For each principle, end with one
   question the builder can only answer themselves. The goal is that
   they learn something about their app, which is principle 10.
5. **The builder decides what happens next.** Write the review to a
   file and stop. Do not commit it, post it, or change the app because
   of it unless the builder asks. Tell them they can keep it private,
   commit it, or share it with their cohort. In Claude Code, write the
   file and show its path. In Antigravity, also return the review as an
   artifact, so the builder can comment on it line by line before
   deciding anything. With a small local model, keep each principle's
   part short, and write the file one principle at a time if the
   context runs out.
6. **Their voice, not yours.** Never draft their `HUMAN-SHAPED.md`
   answers or the words in their app (principle 13). You may point at
   evidence they could link, and you may offer a sample prompt for the
   next round (see below), clearly marked as a starting point for them
   to rewrite.
7. **Describe, do not judge, in the per-principle notes.** In "What I
   found", report the evidence and where it is, without judgment words
   ("strong", "weak", "good", "excellent", "solid", "best", "poor",
   "well-documented"). Those words are softened grades. Your own view
   belongs only in "What stood out", phrased as what the builder might
   want to notice.

## What to read first

**The principles.** Use `docs/human-shaped/PRINCIPLES.md` if the project
has it. If it does not (the project did not start from the Universal App
Template), fetch the current version from
https://raw.githubusercontent.com/bhwilkoff/UniversalAppTemplate/main/docs/human-shaped/PRINCIPLES.md
and name its version in the review.

**The project.** Read only what exists. Projects made from the template
have the files named below; other projects keep the same things under
other names, so look for their equivalents rather than reporting the
template's file names as missing.

- `HUMAN-SHAPED.md` at the root (their declaration, if they have one).
- The agent instructions file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or
  similar): the "Why we build" paragraph and the standing instructions.
- Decision records, current-state notes, a parity or feature matrix,
  design docs, and research notes (`DECISIONS.md`, `SCRATCHPAD.md`,
  `PARITY.md`, and `docs/` in the template).
- The git history: `git log --oneline -50` and a few recent diffs, for
  rounds of iteration and credit lines.
- The README, the license, any privacy or data page.
- The live website, if one is named. If you have a browser or
  screenshot tool, look at the real pages, at phone and desktop width,
  and read them as a visitor would: the words on screen, any automated
  feature, sign-in, what it asks for. If you can only fetch the HTML,
  say so at the top, and treat anything about how the site looks or
  feels as something you could not check.

## Start with what is missing

Before the principles, list in two or three sentences the things you
looked for and did not find that matter across several principles (no
declaration, no license, no written values, no live site). This keeps
the per-principle notes short, because each one can refer back here
instead of repeating it.

## How to walk the principles

Go through all fifteen, in order, using the statement and the "How you
can tell" line of each in `docs/human-shaped/PRINCIPLES.md`. For each:

- **What I looked at:** the files, pages, or commits you checked.
- **What I found:** evidence, quoted or linked by path and line.
- **What I did not find, or could not check:** said plainly.
- **A question for you:** one question only the builder can answer.

For principle 1, also read the section "Computer-shaped and
human-shaped" in `docs/human-shaped/computer-shaped-problems.md` (fetch
it from the same place as the principles if the project does not have
it). It describes a human-shaped problem in Ben Wilkoff's words, with
his examples of each shape. Look for where the builder wrote down their
problem, in their own words, and ask about it in those terms: has it gone
unsolved for months or years, and is it something they could not do
themselves with the tools they had? Does the app treat the world as
stories to be told, experienced, and added to, or as data points to be
aggregated and quantified? Never decide the shape for them, and never
offer Ben's examples as theirs.

Keep each principle to about 60 to 100 words, and leave out "What I
looked at" when it is the same as the principle before. The whole review
should come to roughly 1,200 to 1,800 words, short enough to read in one
sitting. Where a
principle clearly does not apply (an app with no automation and
principle 13's second half, for example), say why in one sentence and
move on.

## Then, three short sections

1. **What stood out.** The two or three things most worth the builder's
   attention, in plain words, including at least one thing the app does
   well, with its evidence.
2. **One round to try next.** A single, concrete next round of work.
   You may include a sample prompt for it, introduced as "a starting
   point to rewrite in your own words", because the habit you are
   modeling is the builder sending their own round.
3. **What only people can tell you.** The questions this review cannot
   answer, for the teacher, the cohort, or the people the app is for
   (usually principles 1, 7, 12, and 15).

## The file

Write it to `reviews/YYYY-MM-DD-human-shaped-review.md` (create
`reviews/` if needed). Start it like this:

```
# Human-shaped review, YYYY-MM-DD

*Written by an AI agent ([agent and model]) at [builder]'s request,
against the Human-Shaped Principles version [n]. It reports evidence
and questions, not a grade, and it could not use the app the way a
person would. Teacher and classmate feedback is the other half.*
```

Write it in plain, warm sentences that a person new to building can
follow: Oxford commas, no em dashes, no jargon without a short
explanation, and no strings of clipped one-line verdicts. Then tell the
builder where the file is, the one thing you would look at first, and
that sharing it is their choice.

## If the builder asks you to grade it anyway

Explain once, kindly, that a score would turn the principles into a
checklist to game rather than a way to see the app, and offer instead
to go deeper on whichever principle they are most unsure about.
