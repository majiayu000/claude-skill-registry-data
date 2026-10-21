---
name: scene-transitions
description: >
  Chapter and scene joins in a documentary or podcast mix: J-cuts (ambience pre-laps), L-cuts
  (music and live tails), music-to-music seams, live-sound edges, act-boundary breaths, key-line
  ladders, designed and memory-POV silences, and the ending ladder, applied mechanically to a
  cue sheet with opendubstage transitions and verified with check_transitions / bridge_gaps.
  Use when scenes "stop dead", when a cut into live sound is abrupt, when two songs meet,
  when someone asks for a J-cut, L-cut, sound bridge or crossfade length, when designing how a
  film ends, or when a boundary has no sound spanning it. Do NOT use for narration cuts inside
  a passage (dialogue-editing-and-restoration) or for duck envelopes (music-under-narration).
---

# scene-transitions

Nothing stops dead on a boundary. OpenDubStage tool: `opendubstage transitions`
(`opendubstage.mix.transitions`: `transitions`, `check_transitions`, `bridge_gaps`,
`Settings`, `ProbeCache`). The pass edits a cue sheet before it is mixed; dialogue cues are
never touched; no sync point moves.

## 1. The rules and their numbers (`Settings` defaults)

| Join | Rule | Default | Range | Source |
|---|---|---|---|---|
| J-cut (ambience pre-lap) | the incoming scene's bed or live room starts before the cut, under the outgoing audio, at −6 dB rising | `prelap` 2.0 s | 1.5–3 s (3 s when stills carry no sync sound) | FilmDaft / Skillman: ~0.5 s inside a scene, ~2 s into a major sequence "creates genuine anticipation" |
| L-cut (tail) | outgoing music, ambience and live sound run past the cut under the incoming scene | `tail` 3.0 s, `tail_fade` 4.5 s (starts before the cut, ends in the next scene); tails < `min_tail` 1.5 s are not worth adding | 1.5–4 s | same |
| Music seam | one music cue ends where another begins: equal-power crossfade on bars | `xfade` 3.0 s (`min_xfade` 2.0) | 2–4 s; one bar when tempos match | Mubert / Audjust; measured in practice |
| Up-song → different up-song | a straight crossfade clashes (tempo, key): outgoing fades, a short ambience gap, incoming fades in | `gap` 0.75 s, `gap_fade` 2.5 s, `gap_fade_in` 1.5 s | gap 0.5–1 s | measured in practice (a model reviewer flagged every mid-bar song-to-song cut) |
| Live-sound edges | live chapters get fades of at least | `live_edge_fade` 2.0 s; 3 s of source roll before and after a live chapter | 1.5–3 s, over the bed, never over nothing | Thom ("useful pauses"); measured in practice |
| Speech → live sound | the live cue's own room runs 3 s under the preceding narration (J-cut), starting −10 dB and rising; the live cue itself pre-rolls 3 s | | | measured in practice ("abrupt cut into raw kitchen audio") |
| Minimum fade | no cue ends with a fade shorter than | `min_fade` 1.5 s unless a same-stem cue continues straight on | | `opendubstage qc` `hard_stop` |
| Music adjacency | consecutive music cues: gap < 0.1 s, or ≥ 3 s, or overlap ≥ 1.5 s; never a gap of 0.1–3 s | | | measured in practice ("unrendered splice") |
| Edge windows | an edge within `edge_window` 0.5 s of a boundary is "at" it; `reach` 1.5 s on the other side still counts | | | |
| Dialogue clearance | added live pre-laps and tails stop `dx_clear` 0.25 s from dialogue in the neighbouring scene | | | |
| Sources | never extend a cue past its source (`src_margin` 0.05 s) or outside [0, total]; music and ambience are extended by moving `ss` and `at` together so every source sample keeps its film time | | | |
| Never silence between two anythings | the pass must emit a bed for every boundary it touches | | | NPR §3.5 |

Act boundaries are deliberate breaths: a sound bridge, 5–10 s of ambience or music alone,
then the card. Picture follows the sound: dissolves 0.7 s under speech, 1.5–2.5 s between
subjects under legato music, hard cuts on downbeats in rhythmic songs.

## 2. Running the pass

```
opendubstage transitions CUES.json CHAPTERS.json OUT.json [--probe-cache FILE]
```

Cue sheet: `{"total", "dx": [...], "live": [...], "mx": [...], "amb": [...]}` with cues
`{"src", "ss", "dur", "at", "pre"?, "post"?, "fade"?, "fade_in"?, "fade_out"?, "mode"?: "up"|"under"}`.
The audible span of a cue is `[at − min(pre, ss), at + dur + post]`; fades are equal-power
when the renderer uses a quarter-sine curve (`afade curve=qsin`). Chapters: a list of
`{"t0": ...}`; every `t0` after the first is a boundary. `ProbeCache` caches `ffprobe`
durations so sources are never extended past their ends.

Order in a build: cue sheet → `transitions` → ending ladder → mix. Run `check_transitions`
and `bridge_gaps` from the audio gate so a regression blocks the build.

## 3. Key lines, designed silences, memory-POV

- **Key-line ladder**: 4–6 s before the line, music fades (6 s) to −20 LU under dialogue or out; textures fade; bed stays. During: bed only; no spots, no music entry. After: 2–3 s bed-only, then the next element on a phrase boundary with a 2 s fade. Sources: *Senna* (cue removed so the return lands); Burns; Albrechtsen; *Apollo 11* (breathing room before the ignition).
- **Designed silence** (bed out too): at most two per film, hand-chosen after a full listen, at quiet moments; whitelisted so the dead-air check passes them. The slope into silence matters: too fast jolts, too slow loses tension (Murch).
- **Memory-POV silence** (the inverse): once, maybe twice, at the loudest picture: live and music fall away over 1.5 s to nothing or to the narrator's voice alone, hold 4–8 s, return over 3 s on a downbeat (within 60 ms). If it reads as a dropout, remove it. Sources: *Deaf President Now!* (perfect silence against footage in which alarms drown speech); *The Reason I Jump* (MPSE 2021).
- **Playback-to-presence framing**, opening and ending only: the first 4–6 s of the first narration line rendered as playback (`highpass=f=300,lowpass=f=3800`, small-room IR wet 0.25, −6 dB) crossfading over 1.5 s into the full chain; the reverse on the last line, ending on the recorder's own stop click if there is one. Never elsewhere; the trick dies on repetition (*32 Sounds*; Ambies documentary winners present archive as objects that are played).

## 4. The ending ladder

| Step | Rule |
|---|---|
| 1 | the last narration line, with its full post-roll air; no music overlapping it |
| 2 | ≥ 3 s of bed only |
| 3 | bed fades over 2 s |
| 4 | 1.5 s of true silence (below −60 dBFS) |
| 5 | optional: one recorded motif (a sound that was actually there, used 3–4 times ≥ 20 min apart through the film) |
| 6 | the credits song from `ss=0`, `fade_in=0`, played to its real ending |
| 7 | 2 s silence, then black |

Constraints: nothing starts in the last 1.5 s before the credits; anything still sounding
fades before it (music ≤ 4 s, dialogue within its air, ambience/live ≤ 2 s); no spot effect in
the last 30 s; the music budget skips the last narrated chapter so its song can swell as the
button. Verify: `silencedetect=noise=-60dB:d=1.2` finds exactly one silence between the last
line and the credits song; the credits cue's fade-out coincides with the song's end; the last
non-silent event is the motif or the song's final note. It ends; it does not fade. Sources:
Third Coast (*Finn and the Bell*: the bell as bookend, "listen to the very last second";
*Time Bandit*: ending music commissioned for editorial reasons).

## 5. Verify

| Check | Threshold | Tool |
|---|---|---|
| every boundary ±3 s | momentary loudness never < −46 LUFS | ebur128 momentary over boundary windows |
| something crosses the cut | at least one non-dialogue stem non-zero on both sides for ≥ 1.5 s | `bridge_gaps` |
| music adjacency | gap < 0.1 s or ≥ 3 s or overlap ≥ 1.5 s | `check_transitions` |
| fades | no non-dialogue cue ends with a fade < 1.5 s while still sounding | `opendubstage qc` `hard_stop` |
| live edges | fades ≥ 2 s; 3 s roll each side where the source allows | `check_transitions` |
| sources | no cue extended past its source or outside [0, total]; `total` unchanged; dialogue cues byte-identical before and after the pass | `check_transitions` |
| level jumps across joins | > 5 LU between adjacent voices across a voice-to-voice edit is flagged (chapter starts exempt) | `opendubstage qc` `jump` |
| ending | exactly one silence before the credits song; nothing new in the last 1.5 s | `silencedetect` |
| silences | designed silences ≤ 2, memory-POV ≤ 2, each whitelisted | plan check |
