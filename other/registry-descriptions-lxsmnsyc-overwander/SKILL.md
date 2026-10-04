---
name: registry-descriptions
description: >
  How to write the one-line `description` a registered item, ability or
  move carries. Applies whenever adding an entry to a data registry
  under src/data, or rewording an existing line. The line describes
  this engine's behaviour, not the mainline's, and is derived from the
  data wherever the data already knows the answer.
---

Every registry entry carries a `description`: one line saying what the thing does. The field is **required**, so an entry cannot be added without one, and `tsc` names the file that forgot.

## What the line is for

It is player-facing text under the name in a list — a market row, a bag entry, a catch sheet. Write it for somebody deciding whether to carry the thing, not for somebody maintaining it.

## Rules

- **Describe this engine, never the mainline.** Where the two differ, the line follows the code. A Zoom Lens here answers a target that is _casting or channelling_, because there is no "moved second" in a real-time fight. Analytic is the same. Leftovers pays out _each time its holder acts_, because there are no turns to hang a residual on. Pressure doubles a _cooldown_, not PP.
- **Use the engine's own numbers.** Read the constant, do not remember the mainline's. `1.2x`, `a sixteenth of its HP`, `30%`. Round a fraction like `5325 / 4096` to `1.3x` — the reader wants the size, not the ratio.
- **State the modifier, not a derived total.** Sniper is "1.5x on critical hits", never "criticals do 3x rather than 2x": a total baked from today's base goes stale the moment another feature also touches that number. Describe what this entry contributes.
- **Say "HP" for health, never "pool".** Pool is too broad a term to read cold in a list.
- **Figures, not number words.** "1/3 of its HP", "at 1/2 HP", "2 stages", "2x Speed", "5 seconds" — never "a third", "two stages", "doubles", "five seconds". Shorter and easier to scan. Articles stay words: "one of its moves", "the two nobody learns".
- **One sentence where one will do, two at most.** Ends with a full stop; a test enforces that.
- **Say the cost as well as the benefit** when the entry has one: "1.5x Attack, but physical moves are 20% less accurate."
- **No implementation vocabulary.** No event names, no file paths, no "listener", "veto", "lifecycle". "Refuses every stat drop from anybody else" — not "vetoes CheckUnitCanAddStage".
- **Plain, complete prose.** Short is not cryptic. Same voice as the codebase.

## Derive it when the data already knows

A line that restates a table drifts the moment the table changes. Where the registry has the answer, compute it:

```ts
// gems: the type is already in the table
description: `${TYPE_NAMES[type]} moves hit 1.5x. Spent on the first one that lands.`,

// valuables: the sell price is already the entry
description: `Worth ${sell.toLocaleString('en-US')} gold to a vendor. Nothing else.`,
```

For a family whose members differ in kind rather than in a value, write a `describeX(item)` that reads the same tables the engine reads — see `describeBerry` in `src/data/items/berries.ts` and `describeMedicine` in `src/data/items/medicine.ts`. A berry moved between tables then re-describes itself with no edit.

Entries whose behaviour is genuinely their own get a hand-written line, kept in a `DESCRIPTIONS` map beside the names rather than inline in the loop.

## Where they live

| registry  | field added in                   | filled in                     |
| --------- | -------------------------------- | ----------------------------- |
| items     | `src/data/items/__create.ts`     | each `src/data/items/*.ts`    |
| abilities | `src/data/abilities/__create.ts` | `src/data/abilities/gen-1.ts` |

## Test it

Each registry has a test asserting every registered entry has a non-empty description ending in a full stop. The empty string is what a derived description falls back to when nothing matches, so that assertion is what catches a new entry falling through the table — keep it when adding a registry.
