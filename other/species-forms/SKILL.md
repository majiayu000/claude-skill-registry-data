---
name: species-forms
description: >
  A form is its own species, numbered in the band past a million, and
  it is its own row in the dex record while sharing one row in the
  printed dex. Applies whenever adding an alternate form, or writing
  code that turns a species id into a dex number, a region or a sheet.
---

An alternate form (an unown letter, and later an Alolan Vulpix or a Mega) is a **full species** here: its own `Species` id, its own registration in `src/data/species/`, its own sprite folder, its own dex tallies. What makes it a form is `baseForm: false` and the id it was given.

## The numbering

```
form id = 1000000 + dexNumber * 100 + formIndex
```

The default form is **not** in the band: its id is its dex number, which is what keeps `Species === dexNumber` true everywhere that relies on it. So Unown A is `201` and Unown B is `1020101`.

The scheme buys three things: a hundred slots per species (Alcremie's 63 is the largest set the mainline prints), a species' forms sorting straight after it, and the base form recoverable from the id by arithmetic alone. The helpers in [`src/data/ids/species.ts`](../../../src/data/ids/species.ts) are `speciesDexNumber`, `speciesFormIndex` and `getBaseFormSpecies`.

**An id is stored player data**, so nothing in the band may be renumbered once it ships. The same rule the family ids keep.

## What reads the base form

- **Region and sheets.** `getSpeciesRegion` asks the dex number, so a form is filed beside its species: `johto/1020101`. The folder is still named after the id.
- **The printed dex.** `getBaseForms` backs the dex grid and `dexOrder`, and both list the default form alone: twenty-eight rows all numbered 201 and all called Unown is not a dex. The row lights up when **any** of its forms has been met.
- **The dex record.** `pokedex_entries` is keyed on the concrete species, so each form is seen and caught on its own. A read that counts pokemon rolls that up (`countDexSpecies`, `readCaughtDexCount`); a read that shows which forms were found does not.

## The two dialogs

Pressing a dex row with several forms behind it opens `SpeciesFormsDialog`, not the entry: the row stands for the pokemon, and which form was meant has not been said yet. That dialog is only the grid of forms, labelled by `formLabel` rather than by the number they share, and pressing one hands over to `DexEntryDialog` for that form alone.

So a form's entry is an ordinary species page. It answers for itself, and its arrows walk the **forms** rather than the dex, since that is the list it was reached through. The default form has no page of its own beyond the one its first square opens.

## A form's own ability

A shape worn in battle (an Origin forme with its orb, Sky Shaymin with a Gracidea) brings its own ability as a **bonus**. The form item grants it with `unit.wearAbility` when the holder takes the shape, on top of whatever the catch carries. The list lives in `SHAPE_ABILITIES` in [`src/battle/items/forms.ts`](../../../src/battle/items/forms.ts).

- It takes no ability slot, and Role Play, Skill Swap, Gastro Acid and Worry Seed cannot touch it, the way Shadow is exempt.
- It never trades away one of the catch's abilities mid-fight.
- It never goes in the base species' pool: a base species is not handed its form's ability.

## Adding one

1. An id in `Species`, written directly after the species' own and inside the band.
2. `baseForm: false` on the registration, and the same `dexNumber` and `family` as the default form.
3. A name that tells it apart in a box. The default keeps the plain name; a variant is marked (`Unown Q`).
4. The species' dex number in `FORMS` in [`scripts/import-sprites.ts`](../../../scripts/import-sprites.ts), with how many forms the game now has ids for. Anything past the count is skipped rather than imported under an id nothing knows.
5. `pnpm import-sprites && pnpm compact-sprites`.
