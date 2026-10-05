---
name: Anki Flashcards
description:
  Create Anki flashcards for spaced repetition learning. Use when the user wants
  to ankify content, asks for flashcards or Anki cards, or wants to memorize or
  study material from text, notes, code, or images.
version: 0.3.0
---

# Anki Flashcards

Transform content into Anki flashcards optimized for long-term retention,
following Andy Matuschak's
[prompt-writing principles](https://andymatuschak.org/prompts/).

## Output

Tab-separated values, one card per line: `Front<tab>Back`. Cloze cards use
`{{c1::answer}}` syntax. Deliver inline in the response; write a `.txt` file
instead when the user asks for one or the deck reaches 10+ cards (Anki imports
it directly). End with the card count and a suggested deck name.

## Card Attributes

Every card must pass all five. A card that fails one gets rewritten or dropped.

1. **Focused** - one atomic unit of knowledge per card. "What 1914 assassination
   triggered World War I?", not "What were the causes of World War I?"
2. **Precise** - unambiguous about what it asks. "What type of chicken parts are
   best for stock?", not "What about chicken stock?"
3. **Consistent** - the same accepted answer every time. "What JavaScript array
   method creates a new array by applying a function to each element?" →
   "map()", not "Name an important array method."
4. **Tractable** - answerable correctly almost every time. Break down or add
   cues until it is. "First 5 digits of pi after the decimal", not "first 20
   digits."
5. **Effortful** - demands active retrieval: the answer must not be inferable
   from the question. "What organelle is called the powerhouse of the cell?",
   not "Is the mitochondria the powerhouse of the cell?"

## Process

1. **Select what to encode.** Start with prerequisite knowledge, frequently
   needed information, and easy-to-confuse details. Each card must connect to
   knowledge or interests the user already has - an orphan card (interesting but
   disconnected) is a card to skip. Done when every key concept in the source is
   either carded or deliberately skipped.

2. **Classify each piece** as factual (facts, definitions, terminology - simple
   Q&A), conceptual (relationships, causes, mental models), or procedural (steps
   and processes - one card per step, plus "what comes next" prompts). For
   conceptual knowledge, create separate prompts for attributes and tendencies
   and for similarities and differences. Cover causes and effects alongside
   significance and implications.

3. **Encode from multiple angles.** A central fact becomes cards that approach
   it differently - forward, backward, and from its context (e.g.,
   organelle→process, process→organelle, process→product). For lists, create
   fill-in-the-missing-element prompts with consistent order, and break large
   lists into coherent subcategories that each fit on one card.

4. **Choose the card type.** Basic Q&A is the default and wins whenever
   understanding matters. Reversed pairs (two cards) for vocabulary and
   bidirectional facts. Cloze for definitions, sequences, and high-volume card
   creation.

5. **Connect.** Add cards that link new knowledge to what the user already knows
   ("How does [new concept] relate to [known concept]?"), and - for ideas the
   user wants top-of-mind - salience prompts ("Where could [principle] apply to
   [user's project]?").

Done when every card passes the five attributes and every key concept from step
1 has at least one card.

## Reference

[references/patterns.md](references/patterns.md) - worked examples by subject
and content type (science, programming, history, language learning, anatomy,
math, image-based cards), with per-type strategies and tag suggestions.
