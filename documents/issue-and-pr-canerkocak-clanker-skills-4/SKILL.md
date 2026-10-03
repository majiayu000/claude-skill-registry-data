---
name: issue-and-pr
description: >
  Write issues and pull requests as plain-words engineering tasks. Use when
  creating or rewriting an issue or pull request, when a draft reads like a
  filled-in form, or when a report needs its structure rethought.
---

# Issues and pull requests

An issue asks for one change. A pull request delivers one change. Write each
so a stranger can act without asking for context.

## One idea each

An issue holds one idea. A pull request holds one delivery. A second idea
gets its own issue; an unrelated fix gets its own pull request. Mixed work
cannot be accepted or rejected as a unit, so reviewers stall on it.

## Shape follows thought

Do not pour every report into the same fixed sections. Labels like problem,
acceptance, and non-goals turn different thoughts into identical grey text
and teach readers to skim past them. Instead, say what is happening, what
should change, and what done looks like, in whatever order fits this case.
Short reports need only a few sentences; only complex work earns a heading,
and even then the heading names the thought, not the template slot. Tables
are tools, not scaffolding: both issues and pull requests use a table where
it makes evidence digestible at a glance, per Default to tables.

## Issues

Start from something observed, not something felt. Name the behavior, where
it happens, and the conditions around it: file paths, commands, measured
numbers with their machine and date. A table is required when there are two
or more comparable entries: measurements, comparisons, before-and-after.
One row per item, short cells, counts taken from the displayed rows. Never a
table for a single fact. Then describe the change you want and
how to recognize it working. If the reader would need your chat history to
understand the request, the issue is unfinished: pull the needed facts out
of the chat and into the text.

## Pull requests

Say what changed and why, in that order, in plain sentences short enough to
read in one pass. Then use a table for the review evidence whenever there
are two or more comparable entries: verification commands and what they
printed, files or areas to look at first, and edge cases checked. One row
per item, short cells. Keep the diff narrow enough that approval means
something.

## How eyes read

Readers do not read; they scan until something earns a closer look. Write
for the scan first. Put the point in the first sentence, because that
sentence decides whether the second one gets read. Keep lines short so the
eye never gets lost travelling back to the left edge. One idea per
paragraph, blank lines between thoughts, and split any paragraph that grows
past four lines.

Use markdown the way the brain uses landmarks. A table turns scattered facts
into one glance. A short list turns a procedure into steps the eye can count.
Code formatting lifts paths and commands off the page so they read as things
to act on, not as more prose. A heading tells a skimmer what sits below it
before they commit to reading. None of this is decoration: every marker must
make the meaning faster to find, or it goes.

## Evidence, not ceremony

Point at things a stranger can open. Never link a private conversation or
paste a transcript and call it context. Screen recordings and logs help only
with the conditions attached. Uncertainty stays visible: mark guesses as
guesses instead of writing around them. Run $prompt-leakage on the final
draft so no chat motive, restatement, or conversation-dependency survives.

## Simple English

Short sentences. Common words. No jargon without an explanation on first
use. Load $simple-english for the full redundancy self-check. For commit messages, branches, and history rewrites, see
`$git-hygiene`.
