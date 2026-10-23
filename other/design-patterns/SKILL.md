---
name: design-patterns
description: Use when reaching for a named design pattern (Factory, Strategy, Observer, Repository) or reviewing code that has one, to check the structure earns its name — and when one already in the code has stopped earning it.
---

# design-patterns

Steps 3 (`archi`) and 6 (`code`) of the pipeline (`WORKFLOW.md`), and a reading angle during `review`.

The classic catalogue is 22 patterns across three families. Every one of them was extracted from code
that already existed: they are **names for structures people kept rediscovering**, not a menu to order
from. Read as a menu, the catalogue reliably produces the thing `over-engineering-review` tags as
`over-abstraction` — with the difference that a named pattern is harder to delete, because it looks like
a decision.

The useful skill here is subtraction. Two thirds of the catalogue is already in the framework you're
using, and naming a structure you don't have yet is how a one-caller interface gets built. Every rule
below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A).

**Relation to an org skill catalogue.** Where a company ships per-pattern implementation skills with
language-specific references, those are the authority on **how** to shape each pattern in that house style.
This block owns **whether to reach for one at all**, plus the entry conditions below — the trigger that says
a given pattern is now earned. Where such a catalogue is installed, follow its shape and this block's
threshold.

**An applied override is recorded, not hidden.** Write the code the governing rule actually requires, and
leave one short neutral trace addressed to whoever can decide (a line in the PR description, the task summary
or an ADR): which rule was overridden, by what, and that it is a resolved case. Never phrase it as "a conflict
between mentis and the house rules" to a non-technical stakeholder — that framing reads as broken even when
the case is a normal, resolved one, and has already caused a real project to get abandoned and restarted over
nothing. Raise one specific, named question to the decider only when no rule anywhere actually resolves the
case.

## When
When about to introduce a pattern by name; when a design discussion produces one as an answer; when
reviewing code that names one; when the same shape has appeared for the third time and needs a name; when
a pattern already in the code is being worked around rather than used.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; the normal path for a new pattern is §1 then §2, and only then §3 or §4. If you are
reviewing code that already has one, §4 and §6 are the two that apply.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Recognise, don't apply | a pattern is about to be introduced, or a design discussion produced a name | [`01-recognise-dont-apply.md`](./references/01-recognise-dont-apply.md) |
| 2 | Check the framework doesn't already do it | before writing any pattern by hand | [`02-framework-already-does-it.md`](./references/02-framework-already-does-it.md) |
| 3 | Where they do earn their place | a pattern survived §1 and §2 and has to be justified | [`03-where-they-earn-their-place.md`](./references/03-where-they-earn-their-place.md) |
| 4 | The seven concrete entry conditions | one of Strategy, State, Null Object, object construction, Value Object, Pipeline or transaction boundaries is in front of you | [`04-entry-conditions.md`](./references/04-entry-conditions.md) |
| 5 | If you use the name, use it correctly | a pattern name is going into a class name, an ADR or a review comment | [`05-use-the-name-correctly.md`](./references/05-use-the-name-correctly.md) |
| 6 | When a pattern stops earning its place | reviewing or auditing a pattern already in the code | [`06-when-it-stops-earning.md`](./references/06-when-it-stops-earning.md) |

## Output / checkpoint
No separate checkpoint: this feeds `archi`, `code` and `review`. What it owes at review time — for every
named pattern in the diff, the second real case exists, the framework doesn't already provide it, and the
structure is smaller with the pattern than without. Failing any of the three, it's a
`simplify` candidate. For a pattern already in the code, what it owes is §6.1's deletion test.

## Guardrails
- **Never introduce a pattern before the second real case.** "We'll need it" is the whole failure mode.
- **Never hand-roll what the container, the event bus or the middleware stack already does.**
- **Apply the net-line test** (`over-engineering-review`): if the pattern adds lines and removes none,
  it bought nothing today.
- **Never let a pattern name end a design discussion.** It's a label for an answer, not the answer.
- Don't refactor working code purely to make it match a pattern.
- **Never leave a removed pattern's justification standing** — the ADR line goes with the structure, or
  the next reader implements it again from the document (§5.8, §6.9).

## Origin
The catalogue itself is the classic Gang of Four set as published on the widely used `refactoring.guru`
reference; §4's entry conditions come from an org skill catalogue's per-pattern skills, extracted and
rewritten generically. The full provenance, the coverage pass over all 22 patterns and the refresh log are
in [`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
