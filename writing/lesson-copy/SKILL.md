---
name: lesson-copy
description: Voice and tone guide for writing this Lessons site's content so it is fun to study — witty, lightly sarcastic, analogy-driven, conversational copy that keeps learners engaged without sacrificing accuracy. Use when writing or rewriting lesson prose, Callouts, quiz questions/explanations, taglines, or when the user asks to make a lesson "more fun", "funnier", "less dry", "add humor/analogies", or improve the copywriting.
---

# Copywriting voice — make studying fun

Lessons should read like a sharp, funny friend who actually knows the subject —
not a textbook. The goal: people *want* to keep reading. Engagement is a
teaching feature, not fluff. **Accuracy always wins** — humor never distorts a
fact. (See `TOPIC.md` for the subject and any domain-specific tone rules — read
it first; match its voice.)

## The voice

- **Conversational & direct.** Second person ("you"), short sentences, active
  voice. Talk *to* the learner.
- **Witty, lightly sarcastic.** Dry humor, playful asides, the occasional
  knowing wink at how confusing the topic usually is. Punch up at the jargon,
  never down at the learner.
- **Analogy-first.** Open hard concepts with a concrete, everyday analogy before
  the formal definition (e.g. "a key signature is basically the song agreeing in
  advance which notes get the funny accent" — illustrative; use one fit to your
  subject). One strong analogy beats three paragraphs of abstraction.
- **Concrete over abstract.** Real numbers, named examples, vivid imagery.
- **Honest about hard parts.** "Yeah, this bit is weird — here's why it clicks."
  Acknowledging difficulty builds trust.

## Techniques to reach for

- Surprising-but-true hooks to open a section.
- Callbacks (reuse a running gag/analogy across the lesson).
- Rhetorical questions that mirror the learner's actual confusion.
- A `Callout variant="tip"` for the joke-that-also-teaches; `variant="warning"`
  for "here's the trap everyone falls into."
- Make quiz **explanations** entertaining — that's where understanding sticks.

## Writing questions that are actually hard

A question only teaches if getting it right takes thought. The classic tells that
make a question trivial — kill all of them:

- **Equal-length options.** Never let the correct answer be the long, detailed,
  hedged one while the distractors are short. Length is a giveaway; learners pick
  the longest option without reading. Trim the right answer or pad the others so
  all options sit at roughly the same length.
- **Distractors are real mistakes.** Each wrong option should be a misconception
  a half-learner would genuinely fall for — an adjacent term, a plausible-but-
  wrong mechanism — not an obvious joke. At most one nonsense option per *lesson*.
- **Make them discriminate, not recall.** The best questions force a choice
  between two close, both-plausible ideas. If the answer is obvious from the
  question stem alone, make it harder.

(Mechanics of `MCQ`/`FillBlank` options live in the `exercise-components` skill.)

## Guardrails (don't be annoying)

- **Substance first.** Every joke must sit next to a real, correct point. If a
  line is *only* a joke, cut it.
- **Don't overdo it.** A witty beat every few paragraphs, not every sentence.
  Wall-to-wall jokes are as tiring as wall-to-wall jargon.
- **No filler, no clichés, no "in today's fast-paced world."** No fake
  enthusiasm or exclamation spam.
- **Inclusive & kind.** Humor never relies on stereotypes, punching down, or
  making the reader feel dumb.
- **Keep definitions clean.** The formal definition itself stays precise; put
  the comedy in the lead-in and the examples, not in the math.

## Translation (es twin)

Spanish copy should be **equally fun, not literally translated**. Adapt jokes,
analogies, and idioms so they land naturally in **peninsular Spanish (Spain,
es-ES — `vosotros`, Castilian vocabulary)** — same spirit, native Spain humor.
Keep technical terms correct. See the `translate-lesson` skill.

## Quick self-check before shipping prose

1. Would a bored student keep reading past the first paragraph?
2. Is every claim still accurate and defensible (`research-topic` brief)?
3. At least one memorable analogy per hard concept?
4. Did I cut every line that's *only* a joke or *only* filler?
