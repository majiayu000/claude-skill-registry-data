---
name: module-depth
description: "Use when creating a module, reshaping an interface, placing a seam, or code keeps resisting change or tests. Not for feature work that fits the existing shape."
user-invocable: false
---
# Module depth
Job: Give code a shape where callers learn little and changes land in one place.
Takes: a design question, or an area or history to survey.   Gives: a firm shape recommendation, or a visual survey and a chosen candidate.
Team moves: dispatch (scouts)

## Words

Use these exact words in everything this block produces.

- **Deep module** (Ousterhout): much behaviour for little to learn, at any scale. Measure depth as what a caller gets for each thing it has to learn. Line ratios don't measure it, because they reward padding.
- **Interface**: everything callers rely on to use the module safely. That means the signature plus invariants, call order, failure behaviour, configuration and speed.
- **Seam** (Feathers): the place where two pieces meet and one could be swapped. Say seam, not boundary. Where a seam sits is a design choice of its own, apart from what sits behind it.
- **Adapter**: the role of whatever fills one side of a seam, at any size.

Callers gain because they can reuse the module. Maintainers gain because a change stays in one place.

## Rules

- **Removal test.** Imagine deleting the module. If tricky logic would land on its callers, keep it. If the callers lose nothing, it only passed calls along.
- **Seams need two.** Add one only where behaviour truly differs and you can name two real implementations. Production and test usually count.
- **Tests cross the interface callers cross.** Wanting to reach past it suggests the shape is wrong. Inside, a module may hold little replaceable pieces joined by private seams. Keep those hidden from tests as well.
- **Shrink the interface.** Fewer methods, simpler parameters, dependencies taken as inputs, results returned rather than state mutated.

## Consolidating a cluster

Classify each dependency, then treat it by category.

| Dependency | Treatment |
|---|---|
| In-process logic | Merge directly |
| Has a local stand-in | Keep behind an internal seam |
| Network service you own | Ports and adapters (Cockburn), with a production and an in-memory adapter |
| Third party you don't control | Inject it and mock it |

When the merged interface has its own tests, remove the tests that targeted the old shallow pieces.

## Steps

1. Name the need: a shape question, or a search for friction. Read the glossary and decision records.
2. For a shape question, apply Words, Rules and Consolidating, and give one recommendation with its reasons in those words.
3. If the shape is in real doubt or the user asks for options, follow `design-it-twice.md`.
4. To find where structure hurts, follow `structure-survey.md`.
5. If the answer contradicts a decision record, state that openly and make the case for reopening it.

## Done when

- The output uses the words above consistently, with no synonyms for them.
- It ends in one recommendation, or in a candidate the user chose. A list of options with no pick is not an ending.
- Each proposed module passed the removal test and each proposed seam names its two implementations.
- Each dependency in a consolidation has a category and a treatment.
- A survey or design-it-twice run met the Done when in its own file.
