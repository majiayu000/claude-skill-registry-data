---
name: plain-writing
description: >-
  How to write anything a person reads: README sections and docs pages, upgrade and release
  notes, changelogs, issue and PR comments, PR descriptions, plan files, reviews and triage
  notes. Lead with the point, plain words, concise without losing detail, and no restating
  what a table or screenshot shows. Use whenever you write or revise prose for a human
  reader, in a file or in a reply. Not for code comments, commit messages or executable
  specs.

---

# Plain writing

## *Why*

Reading is where a person spends most of their time in this pipeline. Every plan file, PR
description and review gets read at least once, often several times, and usually by someone
switching in from other work. A document that takes twice as long to read costs that time on
every read. A document that's short but vague costs more: the reader has to go and find what
it left out.

The goal is the shortest text that still leaves the reader knowing everything they need.

## Lead with the point

- Start each document, section and bullet with the thing the reader needs: the answer, the
  decision, the change. Background and reasons come after, if at all.
- A section's first sentence should make sense on its own to someone who reads nothing else.
- No preamble ("This document describes..."), no restating the request, no closing summary
  that repeats what's above it.

## Plain words, short sentences

- Write the way you'd explain it to a smart colleague from a different team. Short sentences,
  common words, active voice ("the builder writes X", not "X is written").
- Prefer the everyday word: "use" not "utilize", "check" not "validate against", "before" not
  "prior to".
- A technical term is fine when it's the real name of the thing (a class, an extension point,
  a UUI element), but explain it the first time if a non-specialist reader would stumble:
  "a `uui-ref-node` (a row showing a linked item)".
- Don't invent labels or acronyms a reader has to learn just to follow this one document.
- One idea per sentence, one topic per bullet.

## Concise is not vague

Cutting words must never cut information. Keep:

- **Names**: the actual class, route, property, setting or screen, not "the relevant service".
- **Numbers**: limits, sizes, counts, versions, timeouts, not "a reasonable number".
- **Conditions**: when something applies and when it doesn't, not "in some cases".
- **The why** behind a decision that someone might later want to undo.

What to cut instead: filler words, hedging ("it might be worth considering"), repeated points,
explanations of things the reader already knows, and anything the document's own structure
already says (a heading doesn't need a sentence repeating it).

## Let pictures carry what they show

When a document includes a screenshot, mockup, table or diagram, the text doesn't describe what
the reader can already see in it: the layout, the labels, the column names, the order of
things, the colours. The text covers only what the picture can't show:

- behaviour over time: what happens on click, save, failure, reload
- rules and limits: validation, permissions, what's hidden from whom
- where the data comes from and when it updates
- the states the picture doesn't show: empty, loading, error

For a screen in `SPEC.md`, that usually means the screenshot plus a short list of behaviours,
not a paragraph walking through the screen.

## Shape for scanning

- Use a list when items are parallel (options, steps, rules). Use prose when ideas build on
  each other.
- Use a table when comparing several things across the same few attributes.
- Headings should say what's in the section ("Data model", "What happens on save"), not be
  clever.
- Bold sparingly, for the one phrase per section a skimming reader must not miss.

## Before handing it over

Read it once as the reader, then check:

1. Could someone act on this without asking a follow-up question? If not, something specific
   is missing.
2. Is there a sentence that, deleted, would lose nothing? Delete it.
3. Is there a term a non-specialist wouldn't know, used without a short explanation?
4. Does any text describe what a picture or table right next to it already shows?
