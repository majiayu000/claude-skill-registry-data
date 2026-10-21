---
name: music-under-narration
description: >
  Spotting, placing and mixing music under and around spoken word in documentaries, radio
  features and podcasts: where music enters and exits (downbeats, phrase ends, posts and
  buttons), ducking depth and timing, the 1–4 kHz carve (opendubstage carve), the music
  budget (how much of the narration may have music under it), song-relative levels,
  instrumentals instead of sung vocals under speech, checking generated underscores for hidden
  vocals, key-line handling and the ending ladder. Use when someone asks "where should the
  music come in", "how much should I duck", "the music fights the voice", "the song cuts off
  mid-phrase", "can I put this song under narration", is building a duck envelope or a
  sidechain, is designing an ending, or is choosing between a vocal track and an instrumental.
  Do NOT use for ambience beds or spot effects (ambience-and-sound-for-stills) or for chapter
  joins (scene-transitions).
---

# music-under-narration

Public-radio and feature-documentary practice for music against speech, made into numbers.
OpenDubStage tool: `opendubstage carve` (`opendubstage.mix.carve`: `carve`, `posts`,
`phrase_safe_end`, `band_energy_ratio_db`).

## 1. Spotting: music marks shifts

| Rule | Source |
|---|---|
| Build the story without music first; music's main job is to demarcate chapters because audio has no white space. | Rosenthal, Transom 2019 |
| An entrance or exit signals a shift; music enters **mid-action**, not at the first sentence; on a joke, after the punchline. | Menjivar, Transom 2015 |
| "Don't slowly fade up music. Choose a spot and start it there." Entries at a song start or a section start / downbeat, within 60 ms. | Menjivar; measured in practice |
| Cues run ~1:00–1:30, sometimes 0:40–2:30; "if you're going longer or shorter, ask yourself why." | Menjivar |
| "Go as long without music as you did with it." Whenever you take music away, the next line feels more important. | Menjivar; Mitchell, Transom 2014 |
| Take the music away **before** the moment you most want it to land. | *Senna* (a cue removed over a death so the score "hits harder when it returns") |
| Music underscores an emotion already established in the scene; it does not push. | Albrechtsen |
| When music is "felt" rather than "heard" it behaves like sound design: a chord for three seconds, space for six. | Dykstra, *20 Days in Mariupol* |
| Each song that is diegetic memory is heard "up" at least once where it was actually heard; a playlist used only as beds becomes wallpaper. | *Amy* (songs as text); measured in practice |
| Choose music that does not editorialise. | Harmon, Transom 2019 |

## 2. Entries, posts, exits (numbers)

| Event | Rule | Source |
|---|---|---|
| Entry point | song start, section start or downbeat; snap ≤ 60 ms; `fade_in` 0 at a true song start, ≥ 0.5 s mid-song, ≥ 2.0 s when entering under speech | Menjivar; allin1 / beat_this song maps |
| Entry vs the voice | never within 2 s before a first word; at a chapter open ≥ 12–15 s (one or two phrases) in the clear; ≥ 8 s mid-chapter | measured in practice; Burns "edit to the music" |
| Post | a lift between lines in gaps ≥ 2.5 s; target 4–7 s (allow 2–12); rises 1.0 s after the last word to −6 dB relative to music-up; pre-dips 0.5 s ending 0.25 s before the next word; a post shorter than 1.5 s reads as pumping | Menjivar "4 to 7 seconds"; `carve.posts` defaults |
| Full rise | only after ≥ 8 s with no speech | mixer rule of thumb |
| Music-only hold inside a narrated chapter | ≤ 15 s; a hold > 12 s with no speech is a plan problem ("interlude"), not a mix problem | measured in practice (model reviewer flagged every 30–90 s interlude) |
| Exit | on a section end, 4-bar phrase or downbeat within ±6 s of the wanted out (`phrase_safe_end`); fade = one bar clipped to 1.5–4 s; ≥ 3 s out generally, ≥ 6 s when a line follows within 10 s; real endings when the song's end is used | Menjivar; measured in practice |
| Button | the cue ends on a real musical ending, or cuts to a breakdown right before the line you want underlined | Menjivar |
| Never | time-stretch; cut between beats; fade out "wherever the chapter ends" | Mubert/Audjust music-edit practice |

Shorten by removing whole 4/8/16-bar phrases; crossfade one beat (≈ 200–600 ms at 60–120 bpm), equal-power.

## 3. Ducking: depth and frequency

The one controlled study: Torcoli et al., AES 146 (2019): listeners want music ≥ 10 LU
under commentary and ambience ≥ 15 LU; non-experts prefer ~4 LU more; voice-over-voice
≥ 20 LU. The opposite fault: "if the music drops 15–20 dB on every line the audience hears the
automation" (IRPR). WCAG 1.4.7 (AAA) is 20 dB and is a ceiling, not a target.

The pro move is a moderate broadband duck plus a spectral pocket where consonants live
(TrackSpacer, Neutron Unmask, pure:unmask do this live; `opendubstage carve` does it offline).

| Parameter | Value | Why |
|---|---|---|
| Broadband duck under speech | −14 dB with the carve; −17 dB without | 10 LU minimum plus margin; the carve buys the rest |
| Carve band | 1–4 kHz full cut, raised-cosine half-octave tapers; `--band 1000 4000` | ANSI S3.5 band importance peaks 1.5–3.5 kHz |
| Carve depth | −6 dB (`--cut-db`); below 3 dB the masking change is marginal, beyond 6 dB strings and piano turn hollow each time the voice speaks | measured in practice |
| Timing | attack 50 ms look-ahead (the pocket is open at the first syllable), hold 200 ms, release 300 ms; release < 200 ms pumps | measured in practice |
| Sidechain | dialogue 300 Hz–4 kHz frame RMS; gate −45 dBFS (`--gate-db`) with a 6 dB soft knee | no chatter on breaths |
| STFT | 2048 / 512, sqrt-Hann WOLA on an absolute frame grid; stateless blocks with `carve_pad()` context so a block render matches a single pass | seamless 60 s blocks |
| Duck envelope timing | down starts 0.5 s before speech over 0.6 s; up starts 1.0 s after over 2.0 s; gaps < 3 s stay down; 3–8 s rise half-way; ≥ 8 s full | a live sidechain cannot pre-roll; offline you know the timings |
| Result in band | music ≤ dialogue −20 dB in 1–4 kHz (−14 − 6) vs −17 without the carve; below 1 kHz the bed is 3 dB fuller and pumps less | |

```
opendubstage carve MUSIC.wav DIALOGUE.wav OUT.wav [--cut-db -6] [--band 1000 4000] [--gate-db -45] [--block-s 60]
```

Apply the envelope as a gain curve (10 ms frames, `amultiply` or `volume=…:eval=frame`),
not a compressor; keep `sidechaincompress` at most as a mild safety net (ratio 2, release
1500). Deterministic, plottable, testable.

Depth is per song, not per film: a sparse piano pad can sit at −8; a dense vocal song under
speech needs −14 to −17, or the instrumental. Sometimes the answer is an exit, not a duck.

## 4. The music budget

| Rule | Number | Source |
|---|---|---|
| One song under continuous speech | ≤ 45 s, then exit on a phrase and let the bed carry the voice | *Senna*; Dykstra; measured in practice |
| Music under narration, whole film | ≤ 50 % of narration minutes (warn above 60 %) | Menjivar "as long without as with"; Burns' team trade music and effects |
| Per 10-minute window | music present 30–70 % of the time; no cue > 150 s under speech; no stretch > 90 s with neither music nor bed | measured in practice (model reviewer scored dry 90 s stretches and 60 s interludes equally badly) |
| Longest runs | continuous music ≤ 8 min; music-free ≤ 6 min | rule of thumb |
| Anti-fatigue | every 10-min window has ≥ 2 of {music enters or exits, bed change, live sound, ≥ 90 s music-free} | Kwok on *Get Back* ("audio fatigue" over ten-minute stretches) |
| Music-up moments | no speech scheduled over `up` cues; a plan check, not a mix fix | |

## 5. Nothing sung under speech

- No vocal section overlaps speech for > 1 s. Either swap the whole cue for its separated instrumental (BS-RoFormer via `audio-separator`, whole song at once), or run the vocal version in the clear and crossfade to the instrumental 0.5 s (one bar, equal-power) before the first word (the TAL way of using a song with words).
- Separate once per song used in `under` mode and cache (≈ 2–4× real-time on Apple silicon).
- **Generated underscores must be checked for hidden vocals.** Measured in practice: an LLM listener caught buried voices in a generated instrumental that Whisper and the generator's own lyric channel both missed. Procedure in `ai-review-of-audio` (`references/prompts.md`, "hidden vocals").
- Lyric as button: for the one or two songs whose words matter, get word timings and mark a window per song; no speech starts within 2 s before it or overlaps it; the envelope is held at 0 dB through it.

## 6. Levels: each song keeps its own weight

- Per-cue target −17 LUFS integrated for `under` and `up` before any envelope; music-up −16 to −14 short-term in the clear.
- Song-relative offset: `offset = clamp(0.5 × (song_LUFS − playlist_median_LUFS), −2, +2)`; a ballad sits ~2 LU under a party track as it did on the night. Verify: `up` cues spread 3–5 LU across the film (not 0). Source: CAS 2026 (*Becoming Led Zeppelin*: one EQ/limiter across recordings and "some of that goes away").
- Nothing on the music bus but a panner: no `afftdn`, `loudnorm`, `dynaudnorm` or EQ on `mx` cues (a plan check greps the filter graphs). Provenance: the exact masters the subjects heard, not remasters.
- **Live music is not speech.** A processional, a band, a dance, an acoustic guitar on location never go through the speech chain (de-esser, compressor, voice EQ): `highpass=f=40..60` only, target like `up` (−17 to −20), not ducked, excluded from the duck sidechain, and given a solo listen (music + live-music stems alone) before the full mix. Verify: those cues' rendered filter graphs contain no `deesser` or `acompressor`; crest factor within 1 dB of the source. Source: BAFTA Factual pattern; *Summer of Soul* (a separate music mixer).

## 7. Key lines and the ending

- Key line: from 4–6 s before, music fades (6 s) to −20 LU under dialogue or out; textures fade; bed stays. During: bed only, no spots, no music entry. After: 2–3 s of bed only (the breath), then the next element enters on a phrase boundary with a 2 s fade. Sources: *Senna*; Burns ("nothing makes sound more effective than the absence of sound"); Albrechtsen; *Apollo 11* ("a few seconds of breathing room before the actual ignition").
- Laughter peaks: the recorded laugh is the sound; no laughter spot within 5 s; music holds its duck through it (keep-spans).
- **Ending ladder**: last line → ≥ 3 s bed only → bed fade 2 s → 1.5 s true silence → (optional: one recorded motif) → credits song from `ss=0`, `fade_in=0`, played to its real ending → 2 s silence → black. No music overlapping the final line; no spot effect in the last 30 s; nothing starts in the last 1.5 s before the credits; anything still sounding fades before it (music ≤ 4 s, dialogue within its air, ambience/live ≤ 2 s). The music budget skips the last narrated chapter so its song can swell as the button. Verify: `silencedetect=noise=-60dB:d=1.2` finds exactly one silence between the last line and the credits song; the last non-silent event is the motif or the song's final note. Sources: Third Coast (*Finn and the Bell*: "listen to the very last second"; *Time Bandit*: ending music is editorial).
- A recurring motif, if any, is a **recorded** sound from the film's own sources, used 3–4 times ≥ 20 min apart; a generated stinger reads as a stinger.

## 8. Verify

| Check | Threshold | Tool |
|---|---|---|
| masking under speech | music + ambience ≤ dialogue −10 dB in 1–4 kHz over any 3 s stretch (QC default); strict −14 dB in 1.2–4.8 kHz at the 99th percentile of speech frames | `opendubstage qc` `masking`; `carve.band_energy_ratio_db` |
| broadband | music ≤ dialogue −10 LU under speech | stems |
| entries | within 60 ms of a downbeat / section / song start; `fade_in ≥ 0.5` mid-song; none within 2 s before a first word | plan check with song maps |
| exits / posts | every `under` cue ends on a downbeat or section end with ≥ 1 s out; posts median 4–7 s; music-only holds > 15 s flagged | plan check |
| adjacency | consecutive music cues: gap < 0.1 s, or ≥ 3 s, or overlap ≥ 1.5 s | `check_transitions` |
| budget | under-minutes ÷ narration-minutes ≤ 0.5; 10-min window table with no failing window | plan check |
| vocals | no `under` cue overlapping speech > 1 s whose section has vocals and no instrumental swap; generated beds pass the hidden-vocals listen | plan check + model listener |
| levels | `up` spread 3–5 LU; no dynamics/EQ on music cues; live-music cues bypass the speech chain | grep of rendered graphs |
| ending | exactly one silence before the credits song; nothing new in the last 1.5 s | `silencedetect` |

See `references/song-maps-and-posts.md` for beat/section tooling and the post-planning algorithm.
