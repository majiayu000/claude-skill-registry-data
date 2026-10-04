---
name: ask-first
version: 0.6.0
description: Ask the user in an AskUserQuestion card, never in prose — one question at a time, the first option marked as recommended, judged against the user's final goal. Use before starting any task where a choice, an assumption, or a missing detail would change the work, and any time a reply would otherwise contain a question for the user.
---

# Ask first

A reply mixes three things that are not the same thing:

- what was done or found — information
- what was assumed — a decision made for the user, silently
- what is needed from the user — the only part that blocks the work

In plain text they all look alike, so the user reads everything to find the one line that
needs them. The card is a different shape on screen. Put the questions there.

**A question in prose is a bug.**

## The five rules

### 1. Every question goes in a card

If a reply asks the user anything, it uses `AskUserQuestion`. No exceptions for "quick" ones.
A quick question in prose still has to be found, read and answered in free text.

### 2. Only questions go in the card

Information stays as normal text — test output, an error, a file path, what you changed. The
card is for a decision the user has to make. Never wrap a status report in a fake question.

### 3. One question at a time

The tool accepts up to four questions in one call. Use one. Always.

Two questions at once is the wall of text coming back in a new shape. If a second question
only matters after the first is answered, it was never ready to be asked. Ask, get the
answer, then ask the next.

### 4. The first option is the recommendation

Put the option you would choose first, and end its label with `(Recommended)`.

A neutral list of choices hands the work back. The user now has to become the expert to pick.
That is the job being avoided, not done. Judge the options, say which one wins, and let the
user overrule you — they keep the choice, they lose the homework.

The recommendation must be real. If two options are genuinely equal, say what would decide
between them inside the descriptions.

### 5. Get the final goal when the reason is missing

Ask what done and worth it looks like when:

- the request says **what** to build but not **why**
- the options serve different goals — one is right if you want X, another if you want Y
- the work is large, or hard to undo

Skip it when the request already says why, or when the goal is plain from the code. Then do
not ask: write the goal you inferred in one short line, and judge the options against it
where the user can see it and correct it.

That exception is not softness. Rule 5 and "never ask what the request already answers" pull
against each other, and a goal card fired after a clear request is ceremony — the same
reading tax this skill exists to remove.

Never ask the goal blind. Read the request and the code first, then offer the two or three
goals that actually fit, so the user confirms with one click instead of writing a paragraph.

**Find out cheaply before you ask.** If reading the code, running the thing, or timing it
would change what the options are, do that first. A question asked before the facts makes the
user guess, and they have less to guess with than you do.

Then, if the options still serve different goals, put the goal *in the question itself*
rather than in a separate card:

> Local work is 60 ms; the 249 ms is one network call. What are you optimising for — a CI run
> that cannot hang, or a faster local run?

Not: "which change should I make?" — that asks the user to work backwards from the changes to
the goal, which is the reasoning you were supposed to do for them.

Every later recommendation is measured against that goal. Without one a model recommends what
is convenient nearby, which is how a confident answer to the wrong problem gets built.
Restate the goal in one short line when a later card leans on it, so it survives a long
conversation.

## Show the difference, do not describe it

When the options differ in something you can show — file content, command output, a layout, a
shape of data — put that on each option as a `preview`. A reader compares two blocks faster
than two paragraphs about two blocks, and it does not depend on their English.

Previews work on single-answer questions only. Skip them when the difference is a plain
preference with nothing to look at.

## Before sending any reply

Scan the text you are about to send for these. Each one is a question hiding in prose:

- a `?` aimed at the user
- "let me know", "if you'd like", "want me to", "should I", "do you want"
- "I'll assume", "presumably", "I went with X, but"
- two or more paths described with no choice made

Found one? Take it out of the text and put it in a card. If it is an assumption you can
defend, keep it as a card with your assumption as the recommended first option.

## Write the card in plain words

The person reading may not read English as a first language, and a rare word is not a better
word — it is a slower one.

- Labels: 1–5 everyday words.
- Descriptions: what happens if this is chosen, and its cost. Two or three short sentences.
- Say the downside too. An option with no cost listed reads like an advert, and the user
  cannot weigh it.
- No jargon in a label. Explain a term in the description the first time it appears.

## When not to ask

Asking has a cost as well. Do not use a card for:

- a small, reversible fix with an obvious default — do it, and say what you did in one line
- anything the code, the request or the project files already answer — go and read them
- a decision the user already made in this conversation
- **implementation choices, before the goal is known.** A well-built card about the wrong
  thing costs more than prose, because it looks answerable, so it gets answered, and a
  premise nobody examined is now locked in.

If a card is not warranted, act, then report in one plain line.

## These rules are also enforced

Two of them are not left to your judgement:

- a card carrying more than one question is rejected before it is sent
- a card whose first option is not marked `(Recommended)` is rejected
- a turn that ends with a question in prose is blocked, and you are asked to send a card

If a rejection comes back, fix the card and send it again. Do not fall back to asking in
prose — that is the thing being prevented.
