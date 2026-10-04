---
name: signature-abilities
description: >
  A signature ability is one invented ability per evolution family,
  numbered in the 200000 band and granted rather than rolled at birth.
  A legendary **group**, a region's **starter trio** and a pair of
  **counterpart families** each share one theme across their members.
  Applies whenever designing, naming, implementing or reviewing a
  signature ability.
---

Every evolution family gets one non-canon **signature ability**, themed on both what the line is and how it fights. They are not part of any pool: the ids sit in their own band from `200001` up in [`abilities.ts`](../../../src/data/ids/abilities.ts), and nothing rolls one at birth or breeds for one, so a line's four ordinary abilities stay four and the [`ability-pools`](../ability-pools/SKILL.md) walk is untouched.

## A group shares one theme

**A legendary group, a region's three starters and two counterpart families are each designed as a set: one idea told several ways, never a separate design each.** Pick the frame from what the group shares, usually their lore, their role or the ability all of them carry, then vary one axis per member.

- The three beasts share what Ho-Oh did for them in the burned tower. Each survives the first blow that would finish it, is cured, and comes back a stage sharper in the stat it is built on: Raikou Speed, Entei Attack, Suicune Defense.
- The three Kanto birds share the beat of their wings as one takes the field, each taking a different stat off the whole enemy side: Articuno Speed, Zapdos Special Defense, Moltres Defense.

This covers every set the mainline presents as a set, the tower duo and the weather trio and the Regis and the Lati pair among them, and it covers **each region's starter trio**, whose shared frame comes from being the player's first partner rather than from lore. A legendary that stands alone, Mewtwo for instance, needs no shared frame.

It also covers **counterpart pairs**, the two families the games themselves pair off: Nidoran female and male, Plusle and Minun, Volbeat and Illumise, Zangoose and Seviper, Lunatone and Solrock, Sableye and Mawile, Latias and Latios, Kyogre and Groudon, and a region's two fossils (Omanyte and Kabuto, Lileep and Anorith). The list is not exhaustive, so check whether the games pair a family off before designing it alone, version exclusives and Mega pairs included. A pair's two designs either **complement** each other, so the two are worth more on one side than apart, or **cancel** each other, so meeting the counterpart is the one thing that answers the ability. Take whichever the pair's own flavour suggests, and complement when neither reads as an opposition.

Because the members then share one behaviour, the implementation goes in a **meta factory** beside the other shared ones in [`signature/__create.ts`](../../../src/battle/abilities/signature/__create.ts) (`createRisenAbility`, `createWingbeatAbility`), never copied per member. A cancelling pair is the one shape that may stay two listeners, each looking for the other's ability, since the halves are not the same behaviour. That is the repository's standing rule for abilities that share an effect, and it is what keeps the group's numbers in one place.

## Read what the family already has

**Before proposing anything, read that family's own ability pool** in `src/data/species/`, every stage of the line included. Two failures come out of skipping it, and both mean the concept has to be thrown away rather than tuned.

The first is saying the same thing twice. Shroomish already has Effect Spore, so a signature that put a spore on whoever touched it was giving the line nothing it did not have.

The second is stacking a cost on a line that is already paying one. Slaking already carries Truant, so a signature that bought damage with longer cast times made the family worse rather than more interesting. Where a pool ability is itself a penalty, the signature should pay some of that back, or at least cost nothing of its own.

## What the design may not do

**A name may never be the same as a move's or an item's.** All three appear in the same lists and tooltips, so one word standing for two mechanics is confusing however it is described. A name that merely contains a move's word is fine: Mimed Barrier stands beside Barrier. Check `src/data/moves` and `src/data/items` before proposing, not after.

**Nothing shortens a cooldown.** Speed already decides how fast a unit's moves come back, and a second source of the same thing muddies what the stat means. Reach for Speed itself, or for cast and channel times, which Speed does not govern. A cooldown **penalty** is a different thing and is fair as the cost side of a trade, the way the Squirtle line's Overpressure adds to its own cooldowns for the power it gains.

**Nothing keys on whether a move repeats the last one landed**, in either direction. The AI scores each move on its own merits through the speculative resolvers and has no notion of what it threw a moment ago, so a rule written on move history plays completely differently in a player's hands than in the AI's. Counting landed moves without caring which they were is fine, and so is keying on the target rather than the move.

## Directions worth reaching for

Flat multipliers and stat stages are the crowded end of the registry. These four kinds of design change how a fight plays rather than how hard it hits, so propose them first when the family's theme allows:

- **Handing a teammate a specific item**, as Delibird's Delivery gives a Berry Juice to the teammate lowest on HP.
- **Widening a move's reach** to several enemies or allies, as Caterpie's Powder Burst does for status moves and Yanma's Resonance for sound moves.
- **Redirecting a move or its effect**, as Nosepass's Magnetize pulls enemy moves onto itself and Finneon's False Eyes draws a move aimed at a badly hurt teammate.
- **Triggering a move's effect on a condition other than arriving on the field**, on itself, a teammate or an enemy, as Sandshrew's Curl Up casts Defense Curl each time it is hit and Exeggcute's Psyseed seeds whatever its Psychic moves damage.

The uniqueness rules still apply: a second design in one of these directions has to be a different mechanic, not the same one with another move or number.

## Reach for a move before writing machinery

**Where a move already does the thing, cast it.** Drought casts Sunny Day and Cursed Body casts Disable, and a signature that wants weather, a screen, a trap, a heal, a hazard or a status should reach for the move rather than a hand-written listener: the move's own duration, power and cure list stay authoritative, so tuning the move tunes every ability built on it. Cast with `unit.triggerMove(move, target, 0)`, and remember a cast move resolves on its own flight delay, which a test has to advance the clock for.

## Building one

The concept is the user's decision and is put up for approval before any of it is written; how it is built is not. Once a concept is settled, a signature ability costs four things:

1. An id in the signature band, appended rather than inserted, since an id reaches a player's caught rows.
2. A registry entry in [`signature.ts`](../../../src/data/abilities/signature.ts) with a one-line player-facing description, grouped under a comment naming the family.
3. An implementation in the region's file under [`abilities/signature/`](../../../src/battle/abilities/signature/), wired through the list in that folder's `index.ts`. A test checks the registry against every ability the engine implements, so a missing entry fails rather than going quiet.
4. A test suite asserting real engine state, and a changeset. Work that only changes something introduced on the same branch edits that branch's changeset in place instead of adding one.
