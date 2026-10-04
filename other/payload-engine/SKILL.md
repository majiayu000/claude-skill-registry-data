---
name: payload-engine
description: 'Map of the Payload engine-builder: the marble simulation, how parts, blueprints, jams and difficulties are declared, and the invariants that keep runs deterministic and fair. Use when adding or changing a part, blueprint, jam, difficulty or quota, when a drop scores wrong, or when marbles animate out of sync with what actually fired.'
---

# The Payload engine

Payload is React and TypeScript. This skill used to describe it as one file,
`public/payload.html`, which stopped being true when it was ported.

```
src/game/     the rules. Imports nothing from React or the DOM, and CI enforces that.
  types.ts    branded CellIndex and Column, the Phase union, the DropEvent log
  content.ts  PARTS, BLUEPRINTS, VARIANTS, DIFFICULTIES, derived JAMS
  simulate.ts simulateDrop: board + column + rules -> total and an event log
  run.ts      the reducer over RunState, plus the derived helpers
  rng.ts      UTC date key -> FNV-1a -> mulberry32, salted by difficulty
  daily.ts    records, streaks, share text
  preview.ts  projections for the placement and column previews
src/ui/       React. Plays the event log back; owns no rules.
public/payload.html   the superseded single-file build. Kept only as the
                      reference parity.test.ts diffs against. Do not edit it
                      to change the game.
```

The split is load-bearing. The engine decides what happened, the view decides how
fast to show it. That is what lets the skip control collapse the timing without
touching the maths, and what would let a server re-derive a score from a move
list.

## The shape of a run

`startRun(options)` returns state and a seeded rng. From there the reducer drives
it: `selectOffer` then `placeSelected` (or `skipDraft`), optionally `takeBlueprint`,
then `applyDrop` per drop, until `phase` becomes `runOver`.

`RunState.phase` is a discriminated union, so states that cannot coexist cannot be
represented. The old build carried phase, busy and submitted as parallel booleans.

Read config through the helpers, never the raw tables: `quotaFor`, `dropsForRound`,
`jamFor`, `rulesFor`. They fold in the difficulty and the daily variant together.
Reading `difficulty.quotas` directly skips the variant multiplier and silently
desyncs the HUD from the win check.

## The simulation (`simulateDrop`)

Pure. No timers, no animation, no randomness. Given a board, a column and a
`Rules` object it returns the total banked plus an ordered `DropEvent[]` of
everything that happened. The renderer replays that log at whatever speed it
likes; the breakdown panel reads it; `src/ui/playback.ts` regroups it into frames
so every marble in flight advances together.

Adding a part means one case in `applyPart`, which is exhaustive over `PartKey`, so
a new part that is not handled fails to compile rather than silently doing nothing.
The contract for a case:

- Mutate `m.value`, and `m.col` if it deflects. Row changes belong in the caller,
  which owns position: see how Spring and Prism are handled.
- Return a label. A part that changes the score without one is invisible, and the
  player cannot reconstruct the arithmetic.
- Respect `k`, which is 2 when `isForked` says a Tuning Fork is adjacent. Fork
  doubling does not stack, and forks never double each other.
- To spawn a marble, push onto the queue guarded by `MARBLE_CAP`.

Order of operations along the path is the whole strategy. Adds before a Prism get
duplicated; a Coil after a merge multiplies everything. Do not reorder resolution
to be helpful. The geometry the player built is the hand they played.

### Invariants. Breaking these breaks the game

1. Resolution is deterministic. No randomness inside a drop, ever. The same
   machine and the same column must always pay the same. All randomness lives in
   drafting, through the seeded rng.
2. A split copy starts at the prism, not the top of the column. This was a real
   bug: copies drawn from the top appeared to fall through parts that correctly
   never fired, and it read as "tiles don't register".
3. Every trigger is visible. Flash the cell, float a label, blip. The log is what
   makes that possible, so an event that changes the value must be emitted.
4. The player is never multiplier-starved. `rollOffers` forces a `SCALER_KEYS`
   member into every draft. An unwinnable run is unfair, not hard.
5. Shuffling uses Fisher-Yates over explicit rng draws. `sort(() => rng() - 0.5)`
   is not portable: the number and order of comparator calls is
   implementation-defined, so the same seed can deal different offers in different
   browsers, which breaks the daily's one promise.

## Declaring content

Part: add to `PARTS` with a glyph, name, badge, rule and role, add the case in
`applyPart`, then add the key to the difficulty `pools` for the rounds where it
should appear. A part absent from every pool is dead content. The compendium in
`src/ui/Compendium.tsx` renders straight from `PARTS`, and `content.test.ts` fails
if a part is missing a field.

Blueprint: add to `BLUEPRINTS`, then read it wherever it applies, through
`rulesFor` if it changes resolution. Granted after the rounds listed in
`blueprintAfter`. A blueprint the UI never exposes is worse than none: Loose Screws
shipped with a working reducer case and no way to reach it.

Jam: declare on the difficulty as `{ key, name, rule }` under a round index, then
honour `key` where it bites. `dropsForRound` for `shortShift`, `simulateDrop` for
`noBells` and `slippery`. Jams are keyed by name, never by round index, because the
same jam appears at different rounds in different difficulties. `JAMS` is derived
from `DIFFICULTIES` so the compendium cannot drift from what the rules read.

Difficulty: a `DIFFICULTIES` entry is a complete run definition. Easy and Hard
deliberately share no round: different length, drops, starting machine, pools,
jams, blueprint cadence, and a daily seed salted with the difficulty key so the two
never deal the same parts on the same day. Keep it that way. "Easy is Hard
truncated" was explicitly rejected.

## Balance

Quotas roughly double per round, and that curve is what forces multiplicative
builds. When you change it, re-run both bots, so a lazy bot loses and a competent
one wins Easy, and quote the actual numbers. Current shape: Easy `12/30/68/145`
over 4 rounds with 4 drops; Hard `10/22/48/95/190/340/600/1000` over 8 rounds with
3 drops.

Bot runs underplay Prism catchers and Spring loops, so treat their results as the
pessimistic bound rather than the truth.

## Changing the maths

`parity.test.ts` diffs `simulateDrop` against a transcription of the original
`runMarble` over 4000 random boards. If you intend a scoring change, that test is
supposed to fail, and the transcription has to be updated deliberately. If you did
not intend one, it just caught you.

It compares totals only, which is why a bug in the event log once survived it. The
log has its own tests in `simulate.test.ts`.
