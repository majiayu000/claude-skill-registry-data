---
name: puzzle-design
description: 'Design principles for this repo''s genre: daily puzzles, engine-builder runs, and the rules that make compounding scores feel earned rather than arbitrary. Use when adding a part, tuning a quota curve, designing a boss twist, changing what a draft offers, or judging whether a proposed mechanic is fun.'
---

# Designing for this arcade

Distilled from research into Balatro, Slay the Spire, Into the Breach, Wordle, NYT
Connections, the Nikoli catalogue, and the broughlike tradition. These are the
principles that survived contact with a play-through audit of Payload.

## The one that decides everything

The player must be able to form a hypothesis, commit to it, and see it confirmed.

A game that fails this reads as a slot machine however deep it is. Payload's audit
found exactly that failure: real depth in the maths, a marble going from 3 to 76,
and no way to predict or reconstruct it. Depth the player cannot perceive is noise.

Check every proposed mechanic against this before anything else.

## Rules for the engine-builder half

Multiplication, not addition. Additive bonuses feel like wages; multiplication
feels like an explosion. The player has to build the exponent, and every factor
being a decision they made is what makes a big number feel earned rather than
granted.

Escalate quotas exponentially so turtling loses. A linear build must
mathematically fail against the curve. That is what forces commitment to a
strategy instead of hedging. Current curves: Easy `12/30/68/145`, Hard
`10/22/48/95/190/340/600/1000`.

Position must be a decision, not a formality. A Coil below the Weights is worth
double one above them, a Prism is worth zero unless the column to its right is
loaded, and a Tuning Fork is worth nothing unless it touches something. If the
interface does not make that legible, the game asks "which part" while the actual
game is "which cell".

That was the state of it until the placement preview shipped in #45: empty cells
are now shaded by what the board's best drop becomes with the card installed
there, computed from the same simulation the real drop runs. If you add a part,
the preview covers it for free, because it simulates rather than estimates.

Never let a run be starved. `rollOffers` forces a scaling part into every offer. A
run that cannot win because the draft never offered a multiplier is unfair, not
hard.

Adding something must cost something. Board space is the dilution cost, and
permanent placement is what makes a bad early part hurt. Preserve that. It is the
Slay the Spire deck-dilution tension in spatial form.

## Rules for the daily half

One puzzle, everyone, per UTC day. Scarcity is the retention engine, and identical
seeds are what make comparison meaningful. Details in `daily-seeded-runs`.

Failure must be informative. The most-cited criticism of NYT Connections is that
it invites guesses and punishes them without teaching. A wasted drop must show the
player why it was wasted, or it teaches nothing. The loss message gives both
numbers for the same reason: "round 3 demanded 102, the machine paid 90" is
actionable where "more than the machine paid" is not.

Guarantee a floor. Any completion should preserve the streak. Punishing failure
states are the genre's worst feel-bad, so keep the ceiling in the score rather than
in whether you finish.

Share the performance, never the board. The solved layout is the spoiler. Share
what the run felt like, score, rounds, best drop, so two people's results differ
interestingly even when both won.

## Boss twists, the Jams

A good twist attacks the build, not the player's luck. The existing ones are the
template:

- Short Shift: fewer drops, so per-drop output has to be real.
- Slippery: each marble skids past its first part, which quietly turns a junk part
  at the top of a column into a deliberate shield. That emergent counterplay is
  what a good twist produces.
- Power Cut: Echo Bells stay silent.

Never name a mechanic the player has not met. "Echo Bells stay silent" is
meaningless to someone who has never been offered one and cannot look it up.
Either gate the twist on the part existing, or ship a compendium. The compendium
shipped in #46, so a new jam can name a part; keep it that way.

## Tuning method

Never claim balance from inspection. Use two bots, and `verify-puzzle-game` has
the harness:

- A lazy bot, skipping drafts and dropping into empty columns, must lose. If it
  wins, the curve is too soft.
- A competent bot, drafting scalers and stacking a column, must win Easy and get
  close on Hard.

Bots systematically underuse Prism catcher columns and Spring loops, so read their
results as the pessimistic bound and leave that headroom in.

## Difficulties are different games, not one truncated

Easy and Hard deliberately share no round: different length, drops, starting
machine, pools, jams, blueprint cadence, and a daily seed salted per difficulty so
they never deal the same parts on the same day. "Easy is Hard cut short" was
explicitly rejected. Keep it that way.

## Judging a proposed mechanic

Ask in order:

1. Can the player see its consequence before committing? If not, can that be fixed
   cheaply? If not, reject it.
2. Does it interact with at least two existing parts? Isolated mechanics add rules
   without adding depth.
3. Does it make position matter more, or less?
4. Can a bot verify it did not break the quota curve?
5. Is it legible at cell size on a phone, without relying on colour alone, and
   present in the accessible name?
