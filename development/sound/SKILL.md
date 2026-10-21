---
name: sound
description: Music, sound effects and mixing for drawn-by-code videos. Use it when choosing or cutting music, syncing the animation to the beat, placing sound effects (sfx) or generating new ones with ElevenLabs, and when adding the audio to the MP4.
---

# Sound

The video is cut **to the music**, not the other way round: tempo first, cuts after.

## Music

- Find the BPM and the first beat (`beatOffset`). At 120 BPM one beat = 0.5 s and a
  4-beat bar = 2 s. Declare `bpm` and `beatOffset` in the scene.
- If the track doesn't fit the duration, cut it by bars with ffmpeg:
  soft intro → strong entry → groove → the intro returns → final hit.
- Leave 1.5–2.5 s at the end to read the closing line.
- Licenses: Pixabay allows commercial use without attribution, but **not redistributing
  the track on its own**; don't commit it to the repo (do commit the cutting script). If
  YouTube claims it via Content ID, dispute it with the license.

### Synthesized music (license-free)

If there is no track, it can be generated with code: `sandbox/2026-09-24-exquisite-corpse/music.mjs`
writes a WAV with kick, snare, hi-hat, bass, sitar and a filtered pad, and changes
texture at the same seconds as the scene's segments. It is deterministic, so the `.wav`
is not committed: it is regenerated. Without listening to it, check it with the waveform
(`ffmpeg -i mix.wav -filter_complex showwavespic=s=1600x240 -frames:v 1 wave.png`) and
`volumedetect`: no segment should end up nearly flat.

### Generated music (ElevenLabs Music)

`POST https://api.elevenlabs.io/v1/music` (key in `ELEVENLABS_API_KEY`, never in the repo;
commercial use = paid plan; the track is third-party audio: keep it in the experiment's
`private/` or `out/`, never committed).
- A plain `prompt` ignores tempo and timings («120 BPM, drop at 10 s» gave ~96 BPM with
  the drop at 24 s). A `composition_plan` (global styles with «120 bpm», sections with
  `duration_ms`, `respect_sections_durations: true`) gets the tempo right, but sections
  still don't land where asked.
- So: generate with a plan, **measure** it (`node engine/tempo.mjs track.mp3`: BPM, first
  beat, dB per half second → where the build, the drop and the ending really are), then
  cut it by bars with ffmpeg (`atrim` + 30 ms `acrossfade`) so each section lands on the
  edit. Example: `sandbox/2026-09-24-saas-promo/cut-music.sh`.

## Effects

- Library in `assets/sfx/` (33 paper, office and cartoon effects). The prompts they were
  generated with are in `assets/sfx/generate-sfx.mjs`: for a new one, add it to `SFX`
  and run `ELEVENLABS_API_KEY=… node assets/sfx/generate-sfx.mjs name`. The key never
  goes into the repo. Commercial use of ElevenLabs = paid plan.
- Every visible action with weight gets its sound (impacts, appearances, writing), but
  not everything: background effects at -13/-17 dB, hits at -4/-6 dB.
- Place them on the **frame of contact**, not on the frame where the movement starts.

## Mixing

`audio.json` in the experiment folder:

```json
{ "music": "music-cut.mp3", "musicDb": -2, "duration": 6.5, "sfxDir": "../../assets/sfx",
  "cues": [["pop", 1.0, -10], ["stamp", 2.5, -4], ["scribble", 3.0, -15]] }
```

`node engine/mix.mjs sandbox/x/audio.json` → `mix.wav`; with `audio: { mix: 'mix.wav' }`
in the scene, `render.mjs` adds it automatically. If you move a shot, move its cues.

- **`"align": "onset"`** (recommended): a cue's second is when its hit is *heard*. Many
  effects start with a breath of air (page_turn 0.16 s, tick 0.8 s into the file); without
  it they land a drawing or more late. Then write the contact second from the block's code
  (its landing/beat constants) as is.
- **A track that stops dead** before the end card holds: throw its last half second through
  a delay in time (`aecho` at eighth notes, decaying) and fade by the end; it rings out in
  its own key without you having to listen (see `sandbox/2026-09-24-saas-promo/cut-music.sh`).
- **Private music**: point `audio.mix` at a file in `private/`; `render.mjs` skips a missing
  mix, so the scene still renders without the private folder.

## Lessons

- 2026-09-23 · paper-short · A silence mid-video looks like a technical fault: if the music stops, make it on a clear, brief hit.
- 2026-09-24 · exquisite-corpse · With the kick at full and the pad low, the quiet segments were nearly mute after normalizing: balance per segment by looking at the waveform.
- 2026-09-25 · physics-history v2 · ElevenLabs with a `composition_plan` of one section per scene (`duration_ms` = the scene's length, `respect_sections_durations: true`) gave the film's exact length (58 s) and a fade-out; a dark beat in the picture (the fall into a black hole) is scored by ducking the track with an ffmpeg `volume=…:eval=frame` envelope, never by cutting it to silence (see `sandbox/2026-09-25-physics-history/gen-music.mjs`, `cut-music.sh`).
- 2026-09-29 · external trailer · A generated trailer track ignored its sections (no quiet drop, hits every 4 s wherever they fell): measure its hit onsets (an energy rise of more than 9 dB between 20 ms windows), find the one delay that lands most hits on the cuts (0.5 s fitted five of eight), and duck the track with a `volume=…:eval=frame` envelope where the picture asks for near-silence.
- 2026-09-29 · external trailer · Speech-to-text is not deterministic: a TTS line that passed one transcription was heard with an extra syllable by another pass over the same file (and the other way round on a later call). Check every line with two requests in different modes (plain and character timestamps) and flag it if either differs from the script.
- 2026-09-29 · external trailer · The user heard the volume "going up and down, it sounds odd": a voice-keyed `sidechaincompress` (ratio 6, release 350 ms) cut the music 15–20 dB on every phrase and gave it all back in every gap, and a single-pass `loudnorm` (dynamic mode) rode the gain too. Plot momentary loudness (`ebur128`, M every 0.25 s) of the music before and after ducking to see it. Fix: precompute the music envelope from the line timings (about −7 dB under speech, 0.25 s down, 0.6 s up, gaps under 1.2 s bridged) and multiply it in (`amultiply` with an envelope rendered to a raw f32 file); normalise with one measured static gain plus a peak limiter, not dynamic loudnorm; keep scripted quiet sections near −10 dB, not −18. Title cards in a trailer want a real impact: half a second of music suck-out before the cut, a reverse riser whose peak lands on the cut, and a long-tailed hit about 10 dB above the dialogue.
- 2026-09-29 · external trailer · Correction to the line above: the user rejected that recipe ("the title sounds are horrible, redo the whole sound"). Pasted title effects (a generated hit plus a riser on top of a playing track, with a suck-out before each) sound cheap, and the peaks drove the limiter into audible crushing. What worked: build the score from separate generated segments, one per section, each title card opening a new segment on its own orchestral impact (so the hit belongs to the music), quiet sections being genuinely quiet music, and no volume automation beyond a plain duck under speech. Generated short pieces fade out on their own, so request each one several seconds longer than needed and use only the strong part; a model that will not write a crescendo can give a decrescendo to reverse into a riser. Balance by measurement: title hits 4–6 dB (momentary) above the speech median, limiter under ~3 dB on isolated peaks, a light compressor on the narrator, and every line still transcribed correctly in the final mix.
- 2026-09-30 · external product promo · A weak fricative at the start of a brand name (an «f») disappears under a kick that lands on it: the final mix was transcribed as a different word twice while the dry voice read right. Say the name in a gap of the music (place the track so a beat-less bar or a break covers it and the groove returns right after), duck the music a further ~6 dB around every occurrence of the name, and transcribe the final mix, not the voice alone.
- 2026-09-30 · external product promo · A limiter at 44.1 kHz holds the samples, not the true peak (between samples): mixes measured +0.6 to +1.8 dBTP. Limit at 4× (`aresample=176400,alimiter=…,aresample=44100`), then measure `ebur128=peak=true` and trim the gain only if it still exceeds −1 dBTP; trimming alone cost 3 dB of loudness.
- 2026-09-30 · external product promo · A generated track that ends before a longer voice: repeat whole bars of its groove before its natural ending (cut on bar boundaries measured from the first beat, 10 ms fades at each joint, `concat`), so the music still resolves just after the last line instead of fading under it.
- 2026-09-30 · external product promo · Sound effects matched by their peak (−6 to −15 dBFS) said nothing about how far under the narration they sat: measured with stems, some were 26 dB above the voice, and the user heard them «very very loud», covering words. Put the effects on their own bus about −10 dB, duck that bus a further ~8 dB under each word (merged across gaps under 0.3 s, so hits between phrases keep their punch), lower any single effect that still masks a word by exactly what it lacks (computed per 50 ms window against the voice as it sounds in the mix, compressor included), and measure voice minus effects bus in every window with speech: at least 10 dB.
- 2026-10-02 · product videos (four styles) · Measure voice against effects at full band with K-weighting, never resampled to 8 kHz: a resampled mixer cannot hear anything above 4 kHz, so clicks, sparkles, crackle and keyboard clacks passed the check while sitting 3–10 dB above the narration. Use the same measure for the automatic per-effect gain and for the check (high-pass 38 Hz + high-shelf +4 dB from 1.5 kHz, at 44.1/48 kHz), and confirm it against `ebur128` on the stems before trusting it. Rules that held: with voice, effects ≥ 10–12 dB under it per 50 ms window; without voice, momentary effects ≥ 8 LU under the typical voice level (the per-word duck does nothing between phrases). Windows at a phrase edge (the voice's tail plus an effect right behind it) are the ones that fail. Put a −6 dB shelf above 6 kHz on the effects bus when they are mostly treble.
- 2026-10-02 · product videos · `ebur128` prints `M: nan` in silence. An analyser that skips those lines leaves exactly the voiceless stretches unchecked: parse `nan` as silence (very low) and pair windows by their timestamp, not by position in the list.
- 2026-10-02 · product videos · eleven_v3 sometimes cuts a take in the middle of the phrase's last sound, and speech-to-text fills in the missing letter from context (a word ending in «l» cut before the «l» is transcribed whole), so the transcription check passes it. Detect it by level: the last 40 ms of each take against the take's peak, cut if within 30 dB. Fix only the affected phrases with a non-spoken tag after them (`[breath]`, `[beat]`, `[short breath]`); on every phrase it makes several takes much slower. Each tag is a new take: compare spoken duration (first word to last), the last 40 ms, fricatives («s», «z») and what follows the last letter (some tags add 1–3 s of silence or a click), and keep each good take's cache before generating the next. When aligning, trim trailing spaces and the tag's gap so it does not count as part of the phrase; a clean ending is also longer (0.26–0.35 s natural decay), so re-tune the gaps to keep the rhythm.
- 2026-10-02 · product videos · A voice-heavy mix is checked by transcribing the final mix phrase by phrase, too, and by comparing against the whole track, not the isolated take: the spelling of a name is decided across the full text, and Scribe does not always return the same.
- 2026-10-02 · product videos · A limiter at 4× followed by a return to 44.1 kHz raised the true peak by ~1.2 dB with a hot voice, and trimming afterwards cost 1.8 LU: lower the limiter's ceiling and drive it harder instead. And an `afade` inside a graph with `adelay` inputs and `amix=duration=longest` did not land where expected (−39 dBFS on the last frame): fade in the normalisation step, on a file that starts at 0, with the duration in whole frames.
- 2026-10-02 · product videos · `afir` (ffmpeg 6.1): `dry` is the input's gain (`dry=0` gives silence), the reverb tail is cut where the input ends unless the input is padded with `apad`, and `gtype=none` leaves the level to the mixer.
- 2026-10-02 · product videos · Generated music (ElevenLabs Music) ignored the section contents again (the bass came in 2 s late, an «intro of 3.5 s» came out at 7 s, a section asked «without drums» came out as silence, and the ending was cut dead): always measure bass onsets and pulse and mount by measurement; sections under 3000 ms are rejected (422). A closing chord that has to ring until the logo is more reliable synthesised in the measured key. For retro/8-bit pieces, synthesise the effects (pulse with duty cycle, triangle, 15-bit LFSR noise): zero quota, deterministic and in the music's key.
