---
name: game-audio
description: "Sound in the arcade: the synthesised blip vocabulary and what each cue means, why the AudioContext is built lazily, the mute preference, the per-frame cap that stops a cascade becoming noise, and the OfflineAudioContext plan for the native port. Use when adding or changing a sound, when a cue fires at the wrong moment or not at all, or when tuning how a drop sounds."
---

# Sound

Synthesised, never sampled. The arcade installs and runs offline, and a handful
of oscillators cost nothing to ship where audio files would dominate the
bundle. Everything lives in `src/ui/audio.ts`, about 90 lines.

## The primitive

```ts
blip(freq, dur = 0.06, type: OscillatorType = 'square', gain = 0.05)
```

One oscillator into one gain node, with an **exponential ramp to 0.0001**
rather than a hard stop. That ramp is not decoration: stopping an oscillator at
full amplitude clicks, and the click is louder than the note. Never replace it
with `setValueAtTime(0, …)`.

Every call is wrapped in try/catch. A device that refuses to make sound must
not stop the game.

## The vocabulary

`sfx` in `audio.ts`. Each cue has one job; adding a sound means asking what it
tells the player that nothing else does.

| Cue | Sound | Means |
|---|---|---|
| `trigger(n)` | rising square, `300 + min(n,22)*45` Hz | a part fired. Pitch climbs with the count, so a long cascade audibly builds |
| `split` | 880 Hz triangle | a Prism cloned the marble |
| `spring` | 660 Hz sine | a Spring bounced it back up |
| `skid` | 180 Hz sawtooth | an Anvil knocked it sideways |
| `seized` | 120 Hz sawtooth, long | the marble was confiscated |
| `bank(value)` | 784 Hz, or 1046 above 80 | the payout. The only cue that changes with the number |
| `place` / `blueprint` | short square / triangle | UI confirmation, not simulation |
| `roundWon` | bass note plus a 523/659/784 arpeggio | a quota was crossed |
| `runLost` | 110 Hz sawtooth, long | the run ended |

`roundWon` is deliberately expensive and deliberately rare. Peggle gates its
whole musical climax to the last orange peg; spending that per part is exactly
what stops it meaning anything. Fire it on a quota crossing and nowhere else.

## The context is lazy, and that is load-bearing

`context()` constructs the `AudioContext` on the first blip, not at module
load. Browsers refuse to start one outside a user gesture, so constructing it
eagerly leaves a permanently suspended context and silence for the entire
session. It also calls `resume()` when suspended, which is safe because the
first blip always follows a tap. That is the iOS unlock, and it is already
done. Do not add a second one.

`context()` returns `null` when muted, so mute costs nothing rather than
playing into a zeroed gain node.

## Mute

`isMuted()` / `setMuted()`, persisted at `payload.muted.v1`, read once at
module load inside a try/catch because blocked site data must not throw. The
toggle is in the settings sheet with an `aria-pressed` and a `soundOn` /
`soundOff` icon, so the state is in the accessible name and not only the glyph.

## Density is capped, at one place

`usePayloadRun.ts` fires the simulation cues as it walks the event log. One
line does the rationing:

```ts
if (fired <= 2) sfx.trigger(triggers);
```

Eight marbles landing on parts in the same frame is a burst of noise, not
information. Two per frame is the cap. If a new cue can fire many times in one
frame, it needs the same treatment.

## What skipping does to sound, measured

Animation and no-animation are the same loop; only the sleeps differ. `paint()`
returns immediately under `prefers-reduced-motion` or after Skip, but **the
`sfx` calls are not gated by it**, so the same sounds still fire, compressed.

Measured on the live build: a two-sound drop spanned 668ms played normally and
143ms when skipped. A loaded column computed in Node produces five sounding
events, not twenty, and the per-frame cap holds. So it is a burst rather than a
wall on the boards that could be constructed.

**What is unmeasured** is a late-round board with three marbles and a full
multiplier stack. If someone reports that skipping is loud, that is the case to
build first. Tracked rather than guessed at.

Note that reduced motion is a request to lower sensory load. Sound is not
motion and is not covered by that media query, so muting on it would be wrong.
Compressing the same cues into a fifth of the time is still worth watching.

## The native port

`docs/PLATFORM.md` records the plan and the constraint: React Native cannot
synthesise audio, and `expo-audio` plays files only. The route is to pre-render
each cue offline with `OfflineAudioContext` and ship about eight assets. That
is the only reason the vocabulary above is worth keeping small.

## Where it is not

`public/payload.html` has its own copy of `blip` from before the port. That
file is the reference the parity tests diff against, not the game. Changing
sound there changes nothing a player hears.
