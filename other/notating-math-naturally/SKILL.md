---
name: notating-math-naturally
description: Writes math explanations goal-first, one new symbol per step, with labelled groups. Use to explain a loss, derivation or formula.
---

# Notating math naturally

[references/examples.md](references/examples.md) has a bad and a good passage from a real
session, with what makes each work or fail. Read it before writing the first explanation in a
session.

## Order

1. **Start from what is being optimized or asked**, in words. Example: "copy the human driver",
   not "let L denote…".
2. **Introduce ideas in the order they were devised in real life**, each one fixing a problem
   in the one before. Example: imitation → the flow-model loss that replaces likelihood →
   fine-tuning with rollouts → AWR → the specific advantage.
3. **No glossary up front.** A symbol appears the first time the story needs it, never earlier.

## One symbol at a time

- **One display block introduces one new symbol** (or one tightly coupled pair, such as a
  rollout and its index). Say what it is in a plain sentence *before* the block.
- **After its definition, use only the symbol.** Code identifiers (`loss_flow`,
  `weighted_valid_mask`) appear once, where the symbol is defined, and only the symbol after
  that.
- **Reuse earlier symbols freely; never redefine one.** If a quantity changes meaning, give it a
  new name.

## Long expressions

- **Split any expression with more than about three parts into labelled groups** using
  `\underbrace{…}_{\text{(1) name}}`.
- **Right after the block, say the reading order:** "Read (1) first: …; then (2): …". Say what
  each group contributes, not what it literally computes.
- **When an expression is later specialized** (e.g. to one scene, or to one advantage), keep the
  same group labels so the reader can track which part changed.

## Numbers

- **Before a table, work one row in full** so the reader can check the method.
- **Label every number as measured, computed from a formula, or estimated.** Estimates also say
  how they were estimated and their known bias.
- **Cite sources** (file:line, run IDs, metric names) in prose, not inside equations.
