---
name: abc-notation
description: Use when a task involves ABC music notation or tunes as text — reading or inspecting ABC, picking out a section or region of a tune, arranging or mashing several tunes together, transposing or tempo-matching tunes, or playing an ABC tune back as audio for a human to hear and react to.
---

# ABC Notation

ABC is a compact text notation for music. This skill turns ABC into (a) a normalized score plus a
**structure map** you can reason over, and (b) short audio clips a human can hear — because you
cannot hear the music yourself.

## When to use

- Reading, inspecting, summarizing, or validating ABC.
- Selecting part of a tune ("the chorus", "after the second verse").
- Arranging or mashing two or more tunes (medley, layering, transposition, tempo matching).
- Letting a human hear a clip and iterating on their feedback.

Not for: engraving sheet music, or studio-quality production.

## The loop

**analyze → decide (state the plan) → render a short clip → the human listens → map their feedback
to a knob → repeat.**

You cannot hear the result; the human's ear is the verifier. Always show the plan (key, tempo,
sections, mode, crossfade, gains) alongside the audio so feedback is actionable.

## Quick start

Run from this skill's directory (where this file lives). `<ref>` is a handle id from `send`, a file
path, or `-` for stdin.

```bash
# 1. hand ABC to the session; prints a handle id + structure summary
cat tune.abc | uv run python scripts/abcbox.py send

# 2. inspect the structure map (sections, times, active voices, chords)
uv run python scripts/abcbox.py sections <ref>

# 3. hear a short clip (default 5 seconds)
uv run python scripts/abcbox.py play <ref> --section chorus#2
uv run python scripts/abcbox.py play <ref> --after chorus#1 --seconds 5

# 4. playback control
uv run python scripts/abcbox.py replay        # the same clip again
uv run python scripts/abcbox.py stop          # stop now
uv run python scripts/abcbox.py status
uv run python scripts/abcbox.py volume 33     # 0-200, +N, -N, mute, unmute

# 5. render a WAV without playing it
uv run python scripts/abcbox.py render <ref> -o /tmp/out.wav --section verse#1

# 6. mash two tunes (prints the plan, then plays)
uv run python scripts/mash.py <refA> <refB> \
  --a-section chorus#1 --b-section chorus#1 \
  --key F --qpm 120 --mode seq --xfade 4 --seconds 5
```

## Audio policy (required)

- Clips default to **5 seconds** (`--seconds`, default 5). Play longer only when the user asks; use
  `--full` for the whole selection, or a larger `--seconds`.
- Playback is always **background** — it never blocks the conversation. Tell the human how to stop it.
- Always stoppable: `uv run python scripts/abcbox.py stop`.
- Announce the clip window (start/end) so the human knows what they are hearing.

## Selection vocabulary

| Flag | Meaning |
|---|---|
| `--section NAME[#n]` | A whole labeled section, e.g. `chorus#2` |
| `--after NAME[#n]` | The section following that one |
| `--from NAME[#n]` | From that section to the end |
| `--start SEC` | Start offset in seconds |
| `--seconds SEC` | Clip length (default 5) |
| `--full` | The whole resolved range |
| `--voice all\|NAME` | Which voice(s) sound (default all) |
| `--engine auto\|soundfont\|synth` | Renderer (default auto) |
| `--program N` | General MIDI instrument for the SoundFont engine (0 = piano) |

## Ambiguity rule

Section labels repeat (`chorus#1`, `chorus#2`). When a request like "the part after the chorus" is
ambiguous, **ask which occurrence — or state the one you chose and why.** Never silently guess.

## Reasoning over the structure map

`sections` gives each section's label+occurrence, start/end seconds, **active voices**, and
**chords**. Use it to choose musically rather than by time alone: pick a section where the voices
you want actually play, avoid a section that is a rest for your melody, match or deliberately
contrast chord progressions, and window the clip around a seam so the human hears the transition.

## Feedback → knob

| Feedback | Change |
|---|---|
| "abrupt" | raise `--xfade`; choose adjacent sections; align to a bar |
| "clashing" | change section; change `--key`; shorten `--xfade` |
| "too fast/slow" | `--qpm` |
| "can't hear B" | `--b-gain`, or `--voice` |
| "too loud/quiet" | `volume` |
| "wrong part" | re-resolve the selection |

## Mash semantics

- `--key K` transposes each source by the nearest semitone shift into K (default: source A's key).
- `--qpm Q` sets the pulse for **both** sources (their written tempo is ignored; beats are re-timed
  to Q).
- `--mode seq` runs A then B with `--xfade` seconds of overlap; `--mode layer` plays both at once.
- `--a-gain` / `--b-gain` balance the two sources.
- Crossfade gain is applied per note onset (approximate for long sustained notes).

## Rendering

`--engine auto` uses fluidsynth + a SoundFont when available, otherwise a built-in synth. Provide a
SoundFont with `ABC_SOUNDFONT=/path/to.sf2`, or place one in `~/.local/share/soundfonts/` (for
example `MuseScore_General.sf3`). Without one, playback still works but sounds synthetic.

## Pitch convention

`C` is middle C = C4 = MIDI 60. Lowercase `c` is the octave above (C5); `,` lowers an octave and `'`
raises it. See `references/abc-notation.md` for the notation itself.
