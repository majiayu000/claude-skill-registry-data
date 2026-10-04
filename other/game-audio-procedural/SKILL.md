---
name: game-audio-procedural
description:
  "Compose game music and design sound effects in code with a bundled numpy/scipy synthesis toolkit, then export
  loop-ready OGG with a metadata manifest and objective checks. Use for original, reproducible, license-free music, SFX,
  jingles and UI sounds without samples or paid services, as the local audio route of game-audio-vfx in GameGen projects
  or as standalone work for any engine."
---

# Procedural game audio

Every sound is a Python function and every track is a Python score, rendered deterministically from seeds. Assets are
reproducible, diffable, license-clean (no samples) and cheap to iterate. The toolkit in `scripts/` has been used to ship
a full game soundtrack: about 40 SFX and 12 music cues including stage loops, boss themes, jingles, intro and credits.

What it does well: synth, chiptune, electronic, funk/pop, ambient, retro arcade, UI and abstract or stylised SFX. What
it cannot do convincingly: realistic acoustic instruments or orchestras, vocals, field-recorded realism (real footsteps
on gravel, crowds, nature). Say so early and offer a stylised alternative or a licensed-sample route for those.

## Requirements

`uv` (scripts declare their deps inline: numpy, scipy, soundfile), `ffmpeg` for review images and EBU R128 cross-checks,
and the target engine CLI if integration is verified headlessly (Godot adapter included).

## GameGen projects and standalone use

In a GameGen project, this skill is the `local` audio route of [game-audio-vfx](../game-audio-vfx/SKILL.md), which stays
the entry point and owns the cue list, budgets, accessibility and completion evidence. Read
[shared context](../../references/shared-context.md), the ready preferences and
[repository contracts](../../references/repository.md), then:

- Reuse the cue list, audio direction and gameplay/animation event markers instead of re-running step 1. Still do step 2
  (sonic identity) when the brief does not define one, and record it in the audio direction.
- Resolve paths from preferences: the toolkit under `<paths.tools>/audio`, runtime files under
  `<paths.runtime_assets>/audio`, the audio manifest under `<paths.sources>/audio/manifest.json`.
- Pass `--project-manifest <paths.manifest>` to `build.py` so every built cue also gets a per-asset record in the
  project's asset manifest (provider `local`, source, output path, SHA-256, duration, loop data, review state). Advance
  the review state there as the cue passes review and integration.
- game-audio-vfx's evidence rule applies: an engine capture with sound or clear timing evidence, not an isolated render.

For a standalone request outside a GameGen project, do not start `game-bootstrap` or create preferences: resolve the cue
list, sonic identity, engine and paths from the request and existing files, and skip `--project-manifest`.

## Workflow

### 1. Audio direction and cue list

Skip when GameGen already provides them (above). Otherwise, before writing any sound, agree on a short audio-direction
doc (use [references/audio-direction-template.md](references/audio-direction-template.md)): aesthetic and references
described in words, music cue table (id, use, mood, tempo, key, loop or one-shot), SFX cue list derived from gameplay
events, mix targets, engine and runtime format. Tie each SFX to a game event and mark which cues the player must react
to (hazards, damage, timing windows) versus decoration. Ask the user about aesthetic and genre when they are unknown:
they are the decisions that most change the output.

### 2. Sonic identity

The toolkit is shared by every game that uses it, so a game only sounds like itself if its identity is decided up front.
Fill the "Sonic identity" section of the audio direction (home key and scale, source families, material, brightness,
grit, space, width, pitch bias, signature gestures, music palette), propose it to the user for any choice that is a
matter of taste, and mirror it in `style.py` (`STYLE`). Every SFX recipe reads its pitches (`STYLE.tone`), cutoffs
(`STYLE.cutoff`) and final chain (`STYLE.finish`) from it, and the music's custom voices, kit and key follow it too. The
same event in two games should differ at least in source family, key/intervals and signature chain.

### 3. Vendor the toolkit into the project

Copy `scripts/` to the project's tools dir (e.g. `tools/audio/`) so the generator lives with the game and stays
reproducible. Edit the config block at the top of `build.py` (output dir, manifest path, artist tag) and fill
`style.py`. The vendored `sfx.py` and `music/__init__.py` start empty on purpose.

`examples/` (not vendored) holds about 30 SFX recipes and five music cues (action loop with intro, chiptune, ambient,
victory, fail) for one specific palette. Use them to learn the toolkit and to audition what it can do
(`uv run <skill>/examples/render_examples.py --out <scratch dir>`), never as project content. `build.py` fails when an
asset renders identically to an example (`scripts/example_hashes.json`; best-effort, hashes may differ across
numpy/scipy builds). `--allow-example-copies` exists only for throwaway prototypes. Library modules:

| Module           | Contents                                                                                                                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `core.py`        | SR (44.1 kHz), note/MIDI/frequency math, pan, fades, trimming, BS.1770 LUFS meter, look-ahead limiter, OGG/WAV writers                                                                       |
| `synth.py`       | PolyBLEP saw/pulse/square, triangle, sine, 2-op FM, supersaw, white/pink/brown noise, 808 metallic, ADSR, glides, pitch drops, vibrato, LFOs, breakpoint lines                               |
| `fx.py`          | RBJ biquads (static and swept), drive, wavefolder, bitcrush, comb/allpass, ping-pong delay, Freeverb, chorus, flanger, sidechain duck envelope, width, Haas, autopan, tremolo                |
| `drums.py`       | kick, snare, clap, hats, ride, crash, toms, shaker, rim, 8-bit chip kick/snare/hat/noise, riser, downlifter, impact                                                                          |
| `instruments.py` | `Voice` classes: FunkBass, ReeseBass, DriveBass, DeepBass, SubSine, PulseLead, SuperLead, Brass, EPiano, Pad, Bell, Pluck, Stab, GuitarMute (Karplus-Strong), Choir, ChipPulse, ChipTriangle |
| `sequencer.py`   | `Song`: tempo grid with swing, chord map, step-notation melodies, chord-relative grooves, comping, pads, arps, diatonic harmony, drum patterns, filter/gain automation                       |
| `mixer.py`       | stem rendering, per-stem loudness levels, reverb/delay sends, sidechain ducking, tail wrap-around loops, intro+loop rendering, mastering                                                     |
| `style.py`       | the project's sonic identity (`STYLE`): key/scale tones, brightness, grit, space, width, pitch bias, signature `finish()` chain                                                              |
| `sfx.py`         | empty `@sfx` registry (loudness tier, loop, round-robin `variants`, notes) plus generic building blocks (`_env`, `_sweep_noise`, `_place`)                                                   |
| `music/`         | empty `TRACKS` registry and `common.py` helpers (kits, fills, risers, crashes, `Track`, `Jingle`, loop metadata)                                                                             |
| `build.py`       | renders, cleans, levels, encodes (skips unchanged renders), writes the manifest, rejects example copies, optional `--split-intro`                                                            |
| `review.py`      | decodes outputs, checks peak/clipping/DC/length/loop seam, ffmpeg loudness, waveform and spectrogram PNGs                                                                                    |
| `engines/godot/` | sets loop flags and offsets in `.import` files from the manifest and verifies them through Godot headlessly                                                                                  |

### 4. Representative slice first

Build 3–5 representative SFX (one frequent, one reward, one hazard, one UI) and one music loop. Integrate and trigger
them in the actual game before producing the rest. That calibrates loudness tiers, duration and aesthetic cheaply.

### 5. Design SFX

Follow [references/sfx-design.md](references/sfx-design.md): layer anatomy (transient, body, tail), pitch semantics,
sync to animation events, loudness tiers, duration budgets, anti-fatigue (round-robin `variants`, mirrored or
alternating pairs, runtime pitch jitter), seamless SFX loops, and a pattern cookbook mapping game events to layers plus
the dimensions each project sets from `STYLE`.

### 6. Compose music

Follow [references/music-composition.md](references/music-composition.md): step notation, the `Song` API, song forms per
game context, genre palettes, project-specific voices and kit, harmony and progressions by mood, arrangement moves that
make sections differ, and stem levels. Write all melodies originally. Never transcribe or imitate a recognisable
existing tune; "in the spirit of" means genre conventions, not melodies.

### 7. Build, review, iterate

```bash
uv run tools/audio/build.py --only <id>
uv run tools/audio/review.py --only <id>
```

You cannot listen, so verify objectively. Read the build/review numbers against
[references/mixing-and-loops.md](references/mixing-and-loops.md), and open the spectrogram/waveform PNGs to check
envelopes, tails, section structure, sweeps, harsh resonances and aliasing. Ask the user to listen for the subjective
judgments (catchiness, mood, fatigue) and say so when you report. Do not claim a sound "sounds great".

### 8. Integrate and verify in the engine

Follow [references/engine-integration.md](references/engine-integration.md): buses (Master/Music/SFX/UI) with player
volume settings, voice pools, music crossfades, loop offsets per engine (Godot adapter included; split intro/loop files
for engines without loop offsets), and runtime variation. Verify the decoded length and loop flags in the engine, then
trigger cues in a real play session (a capture or the game's own logs). An isolated render is not a verified
integration.

### 9. Record provenance

The audio manifest stores per-asset path, loop data, loudness, peak, duration, seam ratio, notes and a render hash; with
`--project-manifest` the project's asset manifest gets the compact per-asset records too. Commit the generator, manifest
and encoded files together. Credit "procedurally generated" and list the public-domain techniques below if the project
keeps a credits or licenses file.

## Conventions and gotchas

- Mono arrays are `(n,)`, stereo `(n, 2)`, full scale 1.0, 44.1 kHz. Seed every random source.
- Short SFX: momentary loudness reads low for sounds under ~100 ms, so the peak ceiling dominates. That is expected;
  judge those by peak and in-game.
- Vorbis overshoots peaks slightly; the -1.5 dBFS sample ceiling keeps decoded true peak around -1 dBTP.
- Never ship MP3 for loops (encoder padding breaks seams). OGG Vorbis, Opus or WAV loop cleanly.
- Re-encoding identical audio changes the Ogg serial number; `build.py` skips unchanged renders to avoid churn and
  engine re-imports.
- Render speed: 30–90 s tracks render in a few seconds; voices cache repeated notes and drums cache variants.
- Keep music generation per track module and SFX per function so one cue can be rebuilt with `--only`.

## Techniques credited (all public domain or classic literature)

PolyBLEP band-limited oscillators (Välimäki et al.), RBJ Audio EQ Cookbook biquads, Freeverb (Jezar, public domain),
ITU-R BS.1770-4 / EBU R128 loudness gating, Karplus-Strong plucked string, Chowning FM synthesis, Paul Kellet's
pink-noise filter, TR-808-style six-square metallic cymbal, NES-style 2A03 channel conventions (pulse duties, 4-bit
volume, quantised triangle, LFSR noise).
