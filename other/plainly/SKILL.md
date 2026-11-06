---
description: >-
  Explain something to a person in plain language, cause first. Invoked bare at
  an answer that did not land — a re-asked question, a "just tell me",
  punctuation doing the complaining — it re-explains that answer as a causal
  chain; invoked with a question, it answers that question under the house rule,
  investigation included; either way it shows the smallest concrete example of
  what the answer says. Names six defects — symptom-as-finding, buried lede,
  untranslated nouns, broken chain, fog, receipt — so one word calls out a bad
  report.
---

This file is the procedure: the invocations, the pass, and the six defects it
runs a draft against.

`.claude/voice/voice.md` is the other thing, resident in every session because
`CLAUDE.md` imports it: how this team wants to be talked to. The two agree here,
this team's manner being a plain one, and they drift independently — a house
voice can be deliberately less plain and still want a way to ask for something
plainer. Neither tracks the other.

## Two invocations

- **Bare, at an answer that did not land.** Re-explain your own previous answer
  as a causal chain in plain words. The operator is telling you the last one
  failed, so a longer version of it fails again; what was missing is the _why_,
  not the _more_.
- **With a question.** Answer that question under the rule, investigation
  included — find the cause before writing, not after being asked twice.

Either way the output is an answer, not a plan to produce one.

## The pass

1. **Name what the answer rests on, or go find it.** A cause where something
   happened, a reason where something was chosen, a constraint where something
   could not be otherwise — the question decides which, and not every question
   is about a malfunction. Then ask whether anything you can read settles it:
   the history, the input, the configuration, the prompt. An answer written from
   what the system printed is one written before the reading finished. When it
   is genuinely unknowable, say so once, name what would settle it, and stop
   there rather than filling the gap with evidence.
2. **Draft it somewhere you can re-read it, which here means thinking** —
   conclusion first, in the nouns of the person affected, then the chain that
   leads to it with each link saying why the next followed, then a concrete
   example (§ "The example"), then the caveats if and only if they change what
   the reader should do.
3. **Run the six defects below over that draft, then write it out again.** Each
   has a tell you can see in your own text without knowing the subject — but
   only in text you actually put down first.

## The example

**Show one concrete case of what the answer says, whatever the answer is
about.** A reader who lost the general statement usually follows a case, and
"give me a concrete example" is the question they would most often ask next. The
only answer that needs none is one already told as a scenario the reader could
replay — "this test fails because of that line" is not one yet.

- **The smallest thing that still shows it.** A few lines, two rows, one call
  and what it returns — stripped of everything not carrying the point. Past that
  size the reader is decoding the example instead of the idea.
- **Invented is fine, and often better.** A made-up `f()` or a toy table shows
  the shape without the local detail a real case drags along. Use the real one
  when the point is about that real thing.
- **It follows the conclusion, never replaces it.**

So a fix to a cache keyed only by the URL gets the scenario it broke: Alice
opens `/profile`, it is cached under `/profile`; Bob opens `/profile` and sees
Alice's.

## The six defects

They exist so a bad report can be called out in one word, the way `polar bear`
already works for `@.claude/skills/tend-prose/SKILL.md`. Read them as tells to
check a draft of your own against:

- **Symptom-as-finding** — the headline is a quoted error string or a metric the
  system emitted.
- **Buried lede** — counts, windows, method notes or caveats before the
  conclusion.
- **Untranslated nouns** — jargon the reader does not use, where their own word
  exists and is exact.
- **Broken chain** — steps in sequence with nothing saying why each one
  followed.
- **Fog** — uncertainty stated repeatedly and never resolved into "here's what
  would settle it".
- **Receipt** — a reply _about_ what the person said, where the thing they said
  wanted an answer — a joke acknowledged instead of returned, an aside filed
  instead of engaged.

**The sixth is the odd one, and it earns its place by being the only one
investigation cannot fix.** The other five are cured by knowing more: read the
history, find the cause, say it in the right nouns. _Receipt_ is cured by
answering the thing that was actually said. It is the same move as the rest one
level up, at the scale of a conversation rather than a report — narrating a
response instead of making it, which feels attentive and leaves the other person
unanswered. Its tell is the register shift: a neighboring sentence goes formal,
or refers to the remark in the third person ("noted", "a fair point", "I'll take
that on board").

Whether to return a joke at all is an operator entry — some people want the
deadpan. Acknowledging one instead of either returning it or passing it by is a
defect for everyone. The entry sets the register; the rule says don't hand
someone a receipt in place of a reply.

**A tell is a prompt to look again, not a verdict.** Someone who asks "what is
happening here??" has literally asked for a description, and a description
answers them; the question marks say they wanted it fixed. Which of the two
readings was owed is not always decidable, and nothing here decides it — what
the tell buys you is noticing that there were two.
