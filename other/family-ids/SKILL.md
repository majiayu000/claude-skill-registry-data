---
name: family-ids
description: >
  A family id in `src/data/ids/families.ts` is append-only: a new family
  takes the next number at the end, never a number between two existing
  ids, and no id is left unused. Players' candy stacks are keyed by it
  and the species day gives each id a day of the year. Applies whenever a
  new evolution family is registered.
---

`Families` runs from 0 with no gaps. A new family is appended with the
next number, whatever its national dex number. The enum is roughly in dex
order only because the regions were added in that order.

## Never insert between ids

A family id is stored player data. `bag_candies.family` and the candy
rows of `ledger` hold the number, so shifting a family silently moves
everybody's candy from one stack to another. Inserting Victini at 247
did that to every Unova family and cost a data migration.

## Never leave an id unused

The species day features the family whose id matches the day of the year
(`src/data/species/day.ts`). An id with no family is a day that features
nobody, and reserving one changes nothing that appending would not do
better. The 121 held for a Tyrogue family that already existed at 46 was
one of those, and closing it cost another migration.

## Joining an existing family

A species that joins a family already registered (a baby stage, a late
evolution, a form) takes that family's id and needs no new number.
