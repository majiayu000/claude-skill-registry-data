---
name: doc-style-write
kind: pattern
rule: doc-style
description: Pattern of rule doc-style. Load when writing any project prose — rules, specs, README, code comments, commit bodies, PR descriptions. Samples of "so" and "not so" for each wording convention. Not for the structure of a spec — that is rule spec-driven.
---
<!-- rt-kit v0.34.0 · patterns/doc-style-write.md · 6d62745fd39d · правится надстройкой, не здесь -->

# How to word

Pattern of the rule `doc-style`. What must be true — the law
`docs/constitution/project-documentation.md`.

## When to use

- A rule, an article of a law, a spec item or a README is being written.
- A code comment, a commit body, a PR description is being written.

## A rule is one sentence

The rule itself fits in one sentence. After it — at most two sentences about what breaks
otherwise, and only if the sentence itself does not show it. A justification that had an
alternative goes into the pitfalls — the cold part of the rule — not into the law itself: a
bloated bullet is skimmed, and a law says what is true — not why it was once chosen so.

```
✗ **A booking has at least one adult — on every write path, no exceptions.** The lower
  bound is held by the database: there are three write paths, and a check in one of them
  does not cover all. The upper bound (the property's capacity) cannot be expressed as a
  database constraint — it lives in the property row and is changed by the owner.

✓ **A booking has at least one adult.** No exceptions: there is no check-in without adults.
✓ **Adults and children do not exceed the property's capacity.**
```

## What is true, not where it is held

"The database holds it, not the service", "checked inside the transaction", "column default",
"on three write paths out of four", function and column names inside the sentence — that is the
structure of the code. The reader needs to know **what** is true.

The place of enforcement changes at the first refactoring, and a document naming it goes stale
silently. It has a separate file — `implementation.md` next to it.

The exception is the pitfalls in the rule's cold part: there the structure of the code is named
directly, because the pitfall is the very place where people step on it.

## No claims about the future

"Not planned", "will not be", "a separate feature on request" — that is the owner's intention,
not a property of the system. What is not done — yes; why not — yes; what will never be done —
no. Instead of a verdict — an open question `Q-<law letter>-<number>` with what the decision would
change.

The error is silent: a claim about the future has nothing to be checked against, it passes any
check. That is how "there is no online payment and none is planned" got into the first live spec,
while payment was in the plans.

Hence also: what is not in `docs/PRD.md`, the product document does not claim. A guess made while
retelling sounds more convincing than the source — it is shorter and more categorical.

## In plain words

Aphorisms, metaphors and inversions make reading harder and add nothing.

```
✗ a record of the past must not run into a rule that appeared later
✗ the owner's own record must not be erased on the platform's silence
✗ an empty list without text and a failure without a button look the same — like a broken page

✓ a booking the owner entered by hand is not removed when the event disappears from the feed
✓ an empty list must have a text, a failure must have a retry button
```

The test: read the sentence aloud. If people do not talk like that — rewrite. The ear catches it
in the sentence being read and does not catch it in an eight-hundred-line file: the turn of
phrase surfaces throughout the text, and eyes do not count it.

A borrowed turn of phrase comes from what the writer has just read, and it hits hardest when
writing in the same genre: not a single word in such a sentence is outside the glossary, each
passes proofreading on its own, and it is the sentence as a whole that turns out to be
unintelligible. So the introductory paragraph is written last — once the source has faded.

The second half of the test is counting, and where the tree has laid out the prose check
`checks/check-prose-style.mjs`, the set of turns of phrase is accumulated in it: every marker is
named together with its replacement, and a find is printed with file and line. A turn of phrase
found by proofreading is added to the set in the same turn — otherwise the next writer starts
from scratch and rebuilds it from their own memory.

Not only the word is read, but also whether the sentence has one reading. Three causes of
unreadability come in turn, and fixing one starts the next — an article of a law was rewritten
three times, and each time the owner failed to understand it for a new reason:

```text
✗ not telling them apart is not allowed         — a double negative reads as the opposite of what was said
✗ each one shows where it came from             — a pronoun without an owner, and "came from" names no action
✗ either lifted by the role, or kept forever    — two outcomes joined by "or" with no rule for which one occurs

✓ what was granted personally is revoked only personally: the role does not touch it
```

The argument "without this arrangement it would be so" does not go into the text at all: it
argues with what does not exist and reads as "what is this about?".

What neither the ear nor the check sees: repetition of a legitimate turn of phrase. Each
occurrence is legitimate on its own, but standing in the text by the dozen it is no longer a
device but a tic — the reader stops noticing it along with the meaning. This is counted by grep
over the text, and the number by itself is never a rejection: it is judged by whoever edits next.

## A new word in the glossary

A word that means something specific in the tree lives in the glossary. The order is four steps,
and the first is not skipped: the glossary is read before the text is written, not checked
afterwards.

1. **A search over the whole assembled glossary**, including the section of rejected words. A
   word the tree has dropped stands right there — and introducing it anew means silently
   overturning someone else's decision.
2. **Choosing your own section.** An override section replaces the package section of the same
   name entirely: pick a name the set does not have.
3. **A line as a pair — the word and what it is.** Without the second half the word is not
   introduced: it is merely named.
4. **Layout by the same change**, with the check green. A word entered into the override and not
   laid out has not yet appeared for the reader.

A word the tree drops is filed in the same place with its replacement on the same line: a
rejection without a replacement cannot be acted on — the writer sees the ban and does not see
what closes it.

## A fact is checked, not recalled

Before writing that the code does X — open the code and look. A retelling from memory looks as
confident as a verified statement, and afterwards there is no way to tell them apart.

This applies to failures above all: "it will return `value out of range`" held on in two
documents although such a failure is unreachable — the contract and the column have the same
width.

**A statement about the state of another branch is read from it, not from your own copy.** The
copy taken at branching answers any question about a file's contents and shows by no sign how
far behind it is. Three times in one session the state of the shared branch was inferred from a
file on one's own branch, seven commits behind; all three inferences were wrong, one reached the
task document and was reported to the owner as fact. Caught by a rebase, that is, by accident.

```bash
git fetch origin
git show origin/main:<path to file>
```

**A statement "all N such-and-such" is written after listing the routes by which a value reaches
a place, not after a scan by one sample.** A scan confirms exactly the route built into it and
is silent about all others — the more confidently, the more precise the sample. Places were
counted by the pattern of the call itself, 22 were found and written into the plan and the PR
description as "the order is held by the structure"; ten calls of a wrapper that takes the value
as an argument were missed. There were 32 places, and in ten the value stood as a literal.

**The command a number was obtained with is checked for measuring what was asked.** Command
output is no confirmation by itself: the tool answers the question it understood and is silent
about the part of the pattern it did not. Three numbers in a row in one session: a word boundary
not implemented in this build of the tool and not declared a failure gave 278 occurrences instead
of 79; counting calls by regular expression gave 32 and 42 on the same input, while by the syntax
tree there are 27.

**A number that came from a previous session does not count as a measurement.** It is
indistinguishable from a measured one and looks just as confident in a document; it is recomputed
in the same turn the text is written.

## Do not retell what has a source

- contract types and fields — `libs/common/proto/proto/<area>/v1/`, by link;
- columns and indexes — `prisma/schema.prisma`;
- numbers the owner edits (base price, min-nights, capacity) — only how they are applied;
- layers and class names — the rule `lib-layers` and the code itself.

## Code comments

The same rules. A comment answers "why so and not otherwise" — if the answer is not obvious.
What a line does is visible from the line.

A multi-line comment above every function is a sign that explanation has replaced naming. Rename
first, then write the comment.

A comment justifying a deviation from a rule holds that deviation up: as long as the explanation
looks convincing, the deviation is left alone. The fact in it is checked when the comment is
written and rechecked when the deviation is lifted.

## Common misses

- Another project named in a commit, a PR, a comment or a document. Neither the repository
  name, nor "ported from", nor links to its files — anywhere.
- A number written from memory rather than recomputed by a command in the same commit.
- A plan item struck out from memory of the work rather than from the tree.
- Wording that sounds like a heading rather than a rule: "discount handling" cannot be violated,
  "one maximum discount is applied" can.
