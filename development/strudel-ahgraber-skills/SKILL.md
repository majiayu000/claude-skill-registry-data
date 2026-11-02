---
name: strudel
description: |-
  Use when writing, debugging, or explaining Strudel live-coding music patterns — mini-notation syntax, pattern functions (fast/slow/every/off/stack), synth/sample selection, audio effects, scale/chord/voicing API, or EDM production recipes. Triggers: "write a Strudel pattern", "how do I make a bassline in Strudel", "what does .every() do", "strudel drum beat", "strudel chord voicing", any Strudel code question.
---

# Strudel

Reference skill for programming music with [Strudel](https://strudel.cc) — a JavaScript live-coding environment based on TidalCycles patterns, running in-browser.

## Core Concepts

**Cycle** — the fundamental time unit (~2 seconds at the default 30 cpm).
All events fit within cycles; adding events makes each shorter, not the total longer.
One cycle = one bar of 4/4 at the default tempo.

**Pattern** — a pure function from time to events.
Everything is a pattern.
Transforming a pattern wraps it; the original is unchanged.

**Mini-notation** — a DSL written inside `"double quotes"` (single-line) or `` `backticks` `` (multi-line).
Single quotes `'...'` are plain JS strings and are NOT parsed as patterns.

**Chaining** — methods chain left-to-right: `note("c e g").s("piano").lpf(800).room(0.4)`.

**`$:` tracks** — the REPL syntax for parallel patterns.
Each `$:` line is an independent stream.
`_$:` mutes a track.
Outside the REPL, use `stack(...)`.

## Quick Start

```js
// First sound
s("bd sd hh cp")

// First note
note("c3 e3 g3 a3").s("piano")

// Stack drum + melody
stack(
  s("bd*4, ~ cp ~ cp, hh*8"),
  note("<c3 eb3 g3 bb3>/4").s("piano").room(0.4)
)

// Set BPM (default = 120 BPM in 4/4)
setcpm(120 / 4)   // cycles per minute = BPM ÷ beats-per-cycle
```

## BPM Quick Reference

```js
setcpm(120 / 4)   // 120 BPM, 4/4
setcpm(128 / 4)   // house
setcpm(135 / 4)   // techno
setcpm(174 / 4)   // drum and bass
setCps(140/60/4)  // cycles-per-second form
```

## Keyboard Shortcuts (REPL)

| Key          | Action                    |
| ------------ | ------------------------- |
| `Ctrl+Enter` | Evaluate / update pattern |
| `Ctrl+.`     | Stop all patterns         |

## Reference Files

Pull these when you need detail:

| File                                                                 | Contents                                                                                    |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`references/mini-notation.md`](references/mini-notation.md)         | Complete DSL syntax — all operators, euclidean, alternation, polyrhythm                     |
| [`references/pattern-functions.md`](references/pattern-functions.md) | All pattern combinators — time, conditional, random, accumulation, signals, stepwise        |
| [`references/sound-sources.md`](references/sound-sources.md)         | Synths, drum banks, GM samples, FM synthesis, samples loading, MIDI/OSC                     |
| [`references/audio-effects.md`](references/audio-effects.md)         | Full effects chain — filters, ADSR, envelopes, delay, reverb, phaser, distortion, sidechain |
| [`references/tonal.md`](references/tonal.md)                         | Scale/chord/voicing API, transposition, xenharmonic                                         |
| [`references/recipes.md`](references/recipes.md)                     | Production idioms — beats, bass, arpeggios, chord progressions, house/techno/D&B/trap       |
| [`references/visual-feedback.md`](references/visual-feedback.md)     | Visualizers (pianoroll, scope, spectrum, spiral) — what each shows and when to suggest them |

## Workflow

1. **Start with sound** — identify what you're building (drum beat, melody, chord progression, full track).
2. **Reach for the right reference** — use the table above.
   Most questions hit mini-notation or pattern-functions.
3. **Layer with `stack()`** — combine independent streams.
4. **Automate with signals** — use `sine`, `rand`, `perlin` for LFOs and continuous modulation.
5. **Add structure** — use `every`, `sometimes`, `chunk`, `arrange` for variation over time.
6. **Add visualizers, especially in educational contexts** — default to `pianoroll()`, `scope()`, or `spectrum()` when explaining or teaching.
   See `references/visual-feedback.md` for when each applies.

## Common Gotchas

- Mini-notation only parses inside `"..."` or `` `...` `` — not `'...'`.
- Adding more events to a pattern makes each event _shorter_, not the cycle longer.
- `<a b c>` alternates one element per cycle (3 cycles to complete) — the whole pattern isn't faster.
- `delay` feedback ≥ 1 creates an infinite loop; keep it < 1.
- Reverb `roomsize` is expensive to change while running; set it once.
- `.orbit(n)` — each orbit has its own shared delay/reverb bus.
  Default orbit = 1.
