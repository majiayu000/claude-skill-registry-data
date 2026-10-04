---
name: light-comments
description: >
  Keep comments light: short enough to read at a glance, and about the
  why rather than the what. Applies whenever writing or reviewing a
  comment or a doc block. Most blocks are one to four lines; history,
  anecdote and restatement of the code below are cut.
---

A comment earns its place by saying something the code cannot. Write it short, write the reason, and stop.

## Rules

- **Length.** Most blocks are 1–4 lines. A block over ~8 lines needs a real reason to exist: a formula, a protocol, a subtle invariant, a module header.
- **Say the why.** The non-obvious reason, the constraint, the trap. Never restate the signature or the next line in prose.
- **No history.** Cut "It used to be…", "That is what was wrong with…", "This replaced…". The old design is in git; the comment describes what is here now.
- **No build-up.** One statement of the point, not a paragraph arriving at it. Cut rhetorical repetition and the second example that makes the same case as the first.
- **One idea per block.** If a doc block has three paragraphs about three things, either the thing does too much or two of them belong next to the code they are about.
- **Keep verbatim**: lint directives (`oxlint-disable…`), external links, formulas, and any warning that prevents a bug or a data loss.

## Doc blocks

Exported functions, types and constants keep a `/** */` block. It answers what the thing is and the one thing a caller could get wrong — not how it works inside.

Interface fields: one line each unless the field carries a rule (a default, a stored-empty convention, a value that must never be trusted).

## Inline comments

An inline `//` explains a line that looks wrong but is right. If the code is plainly readable, delete the comment instead of writing one.

## Examples

```ts
// Bad — history, build-up, and a restatement of the field name
/**
 * Whether this pokemon has changed hands in a trade.
 *
 * The history already says so — an entry with `Acquisition.Trade` in
 * it is exactly this fact — but a history is a list, and a list
 * cannot be asked of the store. This can: "which of mine came from
 * somebody else" is one query rather than a whole box read and
 * filtered, which is what the same argument buys `auctionable`.
 *
 * Nothing sets it yet: trading does not exist. It is written `false`
 * from the day catches are created so that the day it does, old
 * records do not have to be told apart from new ones by their shape
 */
traded: boolean;

// Good — the query reason, the consumer, the caveat
/**
 * Whether it has changed hands. A field rather than a read of
 * `history` so the store can be queried, and what opens a trade
 * evolution. Always false for now: trading does not exist, but the
 * field ships so old records match new ones later
 */
traded: boolean;
```

```ts
// Bad — says what the line says
// Loop over every unit on the field and add it to the list
for (const unit of battle.units()) { ... }

// Good — says what a reader would get wrong
// Copied first: the effect fields units mid-iteration, and a live
// view would visit whatever it added
for (const unit of [...battle.units()]) { ... }
```

## Prose style

Prose stays plain and complete — full sentences, no shorthand, no unresolvable references ("the fix", a bare ticket id). Light does not mean cryptic: a one-line comment that nobody can decode is worse than the paragraph it replaced.
