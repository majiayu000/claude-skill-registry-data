---
name: game-feel
description: 'Juice craft for this arcade: hit-stop, staged reveals, easing that reads as mechanical, audio pitch as information, and the difference between feedback that is legible and feedback that is merely loud. Use when adding or tuning any animation, sound, screen effect or score presentation, or when a moment that should feel good does not.'
---

# Game feel

This is the "does it feel good" half. Its sibling, `fixing-motion-performance`,
answers "does it drop frames". Those are different questions, and this one is not
about milliseconds.

## The rule that matters most here

Payload's cascades are the strategy, not decoration. Match-3 games deliberately
pace cascades fast because you do not need to understand them. Copying that pacing
is what produced the original failure: 8 float labels stacked inside 700ms, with
the biggest jump, 18 to 76, arriving in a 95ms gap.

So pace for comprehension, not momentum. Slower and legible beats fast and
unreadable, and those are the only two options on offer.

## Staged reveal, one thing at a time

The Balatro pattern, and the fix for the cascade. Per part, in fall order:

1. The marble stops on the cell.
2. The cell bounces, scale 1.0 to 1.12 to 1.0.
3. One value chip flies from the cell to the running total.
4. The total's digits roll with overshoot easing.
5. One note sounds, one step up a scale.

Budget roughly 130ms per step. Eight parts is a little over a second, which is
longer than the original 700ms, and that is the point.

Never animate two parts at once. If a cell fires twice, as with a Spring
re-trigger, show the two chips side by side rather than stacked. Slay the Spire 2
specifically changed from stacked to side-by-side for this reason.

One caveat now that marbles advance together: separate marbles in different columns
may fire in the same frame, and that is fine because they are spatially separated.
The rule is about two effects landing in the same place.

## Easing

Use `cubic-bezier(0.34, 1.56, 0.64, 1)` for anything that should read as
mechanical: a digit rolling, a chip landing, a part seating. The overshoot is the
whole trick. A linear or ease-out lerp reads as a web page, not a machine.

Reserve smooth sub-pixel motion for the marble's travel. Everything discrete should
snap.

## Hit-stop

The single highest-value borrow available. Freeze everything for 120 to 180ms
before the final number lands. Nothing moves, nothing sounds. It is what makes a
total feel delivered rather than merely displayed, and it costs one `await sleep`.

Spend the big payoff, meaning flash, bass and full shake, only when the total
crosses the quota. Not per part. Peggle gates its entire musical climax to the last
orange peg; sprinkling it earlier spends the currency.

## Shake, scaled to meaning

Three tiers, tied to score divided by quota rather than to absolute score. The
quota escalates, so an absolute threshold makes every late drop shake maximally and
the signal dies.

- small: 0.2s
- larger: 0.3s
- plus rotation: 0.5s

## Audio carries information, not just mood

The blips walk up a scale as the trigger count rises, `blip(300 + triggers * 45)`.
That is doing real work: pitch encodes how deep into the chain you are, without a
number. Preserve it.

Cap concurrent triggers. Eight marbles landing on parts in the same frame is a
burst of noise rather than information; `usePayloadRun` plays at most two per frame.

Add a distinct timbre for multipliers against adds, so the two are separable with
the screen ignored. Keep a separate, unmistakable sound for the quota being
crossed.

Audio is a bonus channel. The game must be fully legible muted, which is how most
people will play it.

## The receipt, which none of the reference games do

Balatro, Peggle and match-3 cascades are all ephemeral: the animation happens and
is gone. That is fine when the cascade is decoration. Here it is the strategy, so a
player must be able to re-read it afterwards:

```
3 → +3 → 6 → ×2 → 12 → +3 → 15 → ×2 → 30
```

This is the differentiator, and it shipped as the "Last drop" panel. It also lets
the animation be faster, because comprehension is no longer trapped inside the
animation window.

If an effect changes the value, it belongs in the receipt. Gravity Well's per-row
`+1` was omitted from it once, and every line was wrong for anyone holding the
blueprint: 1 + 3 rendered as 7.

## Non-negotiables

- Every effect must be skippable, and reduced motion must skip them automatically.
  One round-winning drop measured 20.7 seconds; a staged reveal makes that worse
  unless skipping is real.
- Ship a speed setting, 1x, 2x and 3x, on day one. Balatro shipped one and players
  still modded the game faster. A staged reveal that cannot be sped up becomes the
  top complaint by hour ten.
- Never encode meaning in motion alone. Anything a shake or flash communicates must
  also be readable from a number or a label, and from an accessible name.
- Silent effects are bugs.
