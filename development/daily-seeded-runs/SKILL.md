---
name: daily-seeded-runs
description: 'How this repo builds Wordle-style daily puzzles: UTC date keys, deterministic seeding, rotating rule variants, first-attempt-counts records, streaks that survive being offline, and spoiler-free share payloads. Use when adding or changing a daily mode, a seed, a streak, a share string, or when a puzzle must be identical for every player on a given day.'
---

# Daily seeded runs

Both games use the same spine: the calendar date is the seed, so everyone in the
world gets the same puzzle without a backend.

Payload's implementation is `src/game/rng.ts` for seeding and `src/game/daily.ts`
for records, streaks and share text. Both are pure, and both are tested. Ledger
Lane has no daily yet.

## The date is the identity

```ts
export const EPOCH_DATE_KEY = '2026-08-31';

export function utcDateKey(now: Date = new Date()): string {
  return now.toISOString().slice(0, 10);
}

export function dayNumber(dateKey: string): number {
  const ms = Date.parse(`${dateKey}T00:00:00Z`) - Date.parse(`${EPOCH_DATE_KEY}T00:00:00Z`);
  return Math.max(1, Math.round(ms / 86_400_000) + 1);
}
```

`toISOString()` is what makes this UTC. Local-time date maths is the classic bug:
it gives players either side of midnight different puzzles and silently breaks
streaks. The `dateKey`, not "now", is the identity for the puzzle, the stored
record and the streak comparison.

The `Math.max(1, ...)` clamp matters. A wrong system clock would otherwise produce
a negative day number, index the variant table out of bounds, and throw from deep
inside the content table with an error naming the wrong thing.

Hold the date in state, not only in a ref. Anything that reads it, the banner, the
streak line, the locked-in lookup, needs to be told when it changes; a session left
open across UTC midnight otherwise keeps showing yesterday.

## Deterministic generation

FNV-1a hash into mulberry32, then route every random decision through it:

```ts
export function dailyRng(dateKey: string, difficulty: DifficultyKey): Rng {
  return mulberry32(hashDateKey(`${dateKey}:${difficulty}`));
}
```

Salt the seed with anything that should not repeat. Payload salts with the
difficulty key, so Easy and Hard deal completely different parts on the same day
and playing one never spoils the other.

Rules for keeping it deterministic:

- One rng for the run; free play swaps in `Math.random`. Never call `Math.random()`
  on a code path a daily can reach.
- Draw in a fixed order. Adding a draw earlier in the sequence reshuffles
  everything after it, which changes today's puzzle for anyone mid-run.
- Shuffle with Fisher-Yates over explicit draws. `sort(() => rng() - 0.5)` is not
  portable: the number and order of comparator calls is implementation-defined, so
  the same seed can deal different offers in different browsers. That was a real
  bug here, fixed in #31.
- Resolution must not consume randomness at all. Only generation does. In Payload
  a drop is pure simulation, so replaying the same machine always pays the same.
- If generation logic changes materially, bump a version into the hash rather than
  silently serving a different puzzle under the same day number.

## Rotating variants

The day number picks a rule twist, so consecutive days feel different without new
content:

```ts
export function variantForDay(day: number): VariantDef {
  const v = VARIANTS[(day - 1) % VARIANTS.length];
  if (!v) throw new Error('VARIANTS must not be empty');
  return v;
}
```

A variant is a small config object folded in through the helpers, `quotaFor`,
`dropsForRound`, `rulesFor`, rather than by branching at the call sites. Each pairs
a buff with a cost, so Heavyworks starts marbles at 3 and raises quotas by half.
That keeps variants differently shaped rather than simply easier or harder.

Always show the player what today's rules are. An unannounced rule change reads as
a bug.

## Records and streaks

The logic is pure in `src/game/daily.ts`; `src/ui/store.ts` is the only thing that
touches storage.

- First attempt counts. `recordFor` returns the stored record when one already
  exists for that `dateKey`. Replays stay allowed, they just cannot improve the
  recorded result, which keeps the one-and-done ritual without hiding the game.
  It returns the attempt object itself when it accepts it, so reference equality
  tells the UI whether the run just played is the one that counts.
- Compute the streak against the record's own `dateKey`, comparing to a yesterday
  derived from it, never against "now". An attempt finished offline and synced
  later must not break the chain.
- `bumpStreak` is idempotent for a day already counted, so replays cannot inflate
  it, and a loss ends the streak rather than pausing it.
- A streak is only live if it was extended today or yesterday. Otherwise it is a
  stale number that reads as still running.
- Wrap every storage call in try/catch. `localStorage` throws outright in some
  contexts, including `data:` URLs and private mode. The run must stay playable
  with persistence quietly disabled, and that path is easy to regress.
- Version the storage key, and validate what comes back rather than casting it.
  Payload uses `.v2` because the vanilla build wrote a different shape under `.v1`:
  reading it produced a share string saying "stalled at 4/undefined" and reported
  an Easy run as Hard. A stored value is untrusted input like any other.

## Share payloads

Spoiler-free: report the performance, never the board or the solution.

```
Payload Daily #6 ⚒️ Heavyworks
🌤 Easy · cleared 4/4
banked 210 · best drop 96
⚙ 4-day streak
```

Line 1 identifies the day and variant so results are comparable, the rest is the
outcome, and the streak line is omitted when it is not live so a first-timer's
share is not sad. There is a test asserting the string contains no part names,
rows or columns.

Offer a copy button and fall back gracefully when the clipboard API is
unavailable, since `navigator.clipboard` rejects on insecure origins. Keep the
text on screen so there is still a way to share it.

Free play produces no share text at all. There is nothing to compare.
