---
name: voice-matching
description: >
  Making one voice sit next to another in a documentary or podcast mix: long-term average
  spectrum (LTAS) EQ matching with opendubstage ltasmatch, bridging a TTS or cloned voice into
  a location recording (band-limit, early reflections, room-tone floor), riding and placing an
  off-mic second speaker, phone and tape-sync matching, and when two voices should deliberately
  stay different. Use when a narrator and a pickup line sound like different rooms, when
  synthetic or re-recorded lines must blend with original tape, when an interviewer's
  interjections are buried, when a phone caller sits against a studio voice, or when someone
  asks for "EQ match", "dialogue match", "make these voices match" or "the bridge sounds dry
  and clinical". Do NOT use for cleaning a single recording (dialogue-editing-and-restoration)
  or for voice cloning itself.
---

# voice-matching

Dialogue editors match voices with an EQ match (FabFilter Pro-Q "EQ Match", iZotope Ozone /
Neutron "Match EQ", RX "Dialogue Match"): compare the long-term average spectrum of a
reference voice with the voice that sounds different and apply a smoothed, gain-limited
difference curve. OpenDubStage does this offline: `opendubstage ltasmatch`
(`opendubstage.match.ltasmatch`), numpy plus an `ffmpeg` binary.

## 1. Decide the reference, then match *down*

- The reference is the film's main voice (the interview, the field recording, the archive), not the cleanest source. Match the clean or synthetic voice **down** to the recording: band-limit it, give it the room, lay the same floor under it. Lifting the reference up to the clean voice destroys what makes it a document (NPR §5.8; Podcast Engineering School on phone matching: "reduce the frequency range of someone recording directly to more closely match the telephone caller").
- Match per line, not per source, when sources vary within themselves: Phil Heywood EQ'd each veteran's line with narrow cuts "so one guy sounded the same as the next" (*They Shall Not Grow Old*, Mix). Practically: one chain per source class, then a per-passage loudness match to the anchor and a per-passage 2-band tilt toward the median spectrum.
- Sync sound from a camera stays "the other room": it is the world, the narration is the storyteller (Murch's "colour"). Match it at a small amount (0.25) and keep both at the same dialogue loudness (±2 LU short-term) so the ear is not jolted. *Minding the Gap* keeps home video centre and dry; only the score gets width.
- Two eras of a voice are **never** matched to each other (Moonage Daydream, 32 Sounds): equal loudness (−24 ± 1), timbre deliberately different, LTAS differing ≥ 6 dB above 6 kHz; the listener must always know which year is talking.

## 2. The LTAS method and its numbers

```
opendubstage ltasmatch REFERENCE SOURCE [--gmax 6] [--half-octave] [--protect-below HZ] [--json]
```

| Step | Setting | Why |
|---|---|---|
| Speech-active frames | energy VAD (`energy_vad`: frame RMS within 20 dB of the 95th percentile and ≥ 12 dB above the 10th) or word timings (`interval_mask`); drop the first/last 2 frames of each run | the match must compare speech with speech, not room with room |
| LTAS | 1/3-octave bands 80 Hz–12.5 kHz (`THIRD_OCTAVE`), STFT 4096 / hop 1024 at 48 kHz, power mean over active frames, dB | 1/3-octave is coarse enough not to copy formants |
| Smoothing | 1/6-octave Gaussian on a log axis (one `smooth` pass) | matching at fine resolution copies the other voice's formants and sounds phasey |
| Correction curve | `G(f) = amount × (P_ref − P_src)`, amount 0.3–0.5 (RX docs: "10–40 % is often enough"; more when the sources differ more than lav vs boom); zero-mean in 300 Hz–3 kHz so loudness normalisation is untouched | partial matches sound like the same room; full matches sound like a filter |
| Gain limit | ±6 dB per band (`--gmax`), ±5 dB above 8 kHz; never boost above the source's real bandwidth (an 11 kHz-bandwidth source has no 12 kHz to boost; boosting adds hiss) | large boosts lift the noise floor |
| Filter | least-squares fit of octave-spaced (`OCTAVE_EQ`, Q 1.4) or half-octave (`HALF_OCTAVE_EQ`, Q 2.1) RBJ peaking bands → an ffmpeg `equalizer` chain (`eq_string`); alternatively `firwin2` → `minimum_phase` → `afir` | plain filter strings, reproducible, cacheable |
| Pass criterion | residual \|LTAS_src′ − LTAS_ref\| ≤ 3 dB in every band 200 Hz–6.3 kHz (`deviation`); RMS < 2 dB | measured in practice: ±3 dB reads as "same room", ±4 as "a different voice" |

Suggested amounts: synthetic bridge → main recording 0.4–0.45; camera speech → main recording 0.25; a second speaker inside the same recording → main speaker 0.5.

## 3. Bridging a TTS or cloned voice into a recording

The synthetic line must be *degraded* to the recording's bandwidth and given its room; the
recording is never cleaned up to meet it (NPR §5.8; TSNGO's "glue" of old crowd libraries
under new actor lines).

| Stage | Setting | Check |
|---|---|---|
| Band-limit | `highpass=f=110..120`, `lowpass=f=7500..9000` | LTAS above the source's cutoff within 3 dB of the reference |
| Proximity warmth | `equalizer=f=180:t=q:w=1.2:g=1.5` if the TTS is thin; `equalizer=f=2500:t=q:w=1.2:g=-2` against TTS "presence" | |
| Early reflections | `early_reflections()` from `ltasmatch`: taps at 3.1, 5.3, 7.9, 11.3, 17.2, 26.0, 39.0 ms, first tap 0.30, RT60 ≈ 110 ms (a car or small room has almost no tail; early reflections plus bandwidth sell it, a long IR puts him in a bathroom) | `decay_ratio_db` (0–30 ms vs 30–120 ms) within 3 dB of the reference |
| Compression | `acompressor=threshold=-22dB:ratio=2:attack=10:release=200` | |
| Fitted EQ | the `ltasmatch` curve at amount 0.4–0.45 | deviation ≤ 3 dB |
| Level | −3 dB relative to the anchor is often right for a bridge (it is a connective line, not the voice) | short-term within ±2 LU of the main voice |
| Floor | the main recording's room tone under every bridge at −46 LUFS, starting 1 s before and ending 1 s after | a blind listener cannot tell the bridge from the recording by room alone |
| Direction of travel | DNSMOS BAK of the bridge should go **down** (it should get dirtier, not cleaner) | |

Credit it. Synthetic or re-voiced lines in nonfiction go on the end card (*Deaf President
Now!* credited the actors who voiced its interviewees; Cinema Eye and Peabody juries are
alert to undisclosed synthetic voice). One line; it costs nothing and its absence costs trust.

## 4. The off-mic second speaker

An interviewer or partner who chimes in from beside the microphone is content (Cameraperson,
Radio Diaries). Treat it as its own lane, the way a tape-sync engineer treats the phone side.

- Find the spans: diarisation labels merge and split on a two-person recording, so confirm with pitch (`median_f0`, autocorrelation 70–400 Hz, voicing 0.45) and, as a fallback, "spans ≤ 12 words that sit ≥ 6 dB below the cue's median short-term loudness". Clamp spans to ≥ 0.4 s, merge gaps < 0.3 s, expand each by 0.08 s so switches land in air.
- Ride: +2 to +5 dB per span (measured in practice: 1.7 LU under the main voice before the ride); target short-term loudness within ±2 LU of the main voice over the same cue (Byers: "every voice roughly the same volume"). Hand-ride the one or two lines that still fail.
- EQ per span: `equalizer=f=450:t=q:w=1.2:g=-3,highshelf=f=3000:g=3` as a start, or the fitted curve against the main speaker at amount 0.5.
- Place: a level-only pan of 15–20 % toward one side (`pan=stereo|c0=0.85*c0|c1=1.0*c0` style, no delay, no width tricks). Verify the mono sum of the dialogue stem differs from the stereo mid by < 0.1 dB (no cancellation). On headphones: two people in a room, not one voice with a volume ride (Mangini: "no loudspeaker can reproduce proximity").
- Music stays down through the interjection: the span counts as speech for the envelope.

## 5. Phone, tape-sync and remote callers

- Match the studio voice toward the caller for long passages; cut mud 250–450 Hz on the caller, add 2–3 kHz; put the thin source slightly **louder** because it is harder to understand (Podcast Engineering School).
- Push fixes to the source where possible (NPR Training interview checklist).

## 6. Verify

| Check | Threshold |
|---|---|
| LTAS deviation per voice class vs the reference | ≤ 3 dB in every 1/3-octave band 200 Hz–6.3 kHz (≤ 4 dB before matching is applied) |
| per-band correction | no band boosted > +6 dB; nothing above the source's cutoff |
| loudness per class | short-term (3 s) within ±2 LU of −24 across the film; per-cue sentence std ≤ 1.5 LU |
| second speaker | spans ≥ 0.4 s; within ±2 LU of the main voice after the ride; mono sum < 0.1 dB |
| bridges | DNSMOS BAK lower than the raw TTS; decay ratio within 3 dB of the reference; a blind A/B against the preceding line passes in both orders |
| tonal QC | `opendubstage qc` `tonal`: 1–4 kHz presence share per class within ±4 dB of the class mean |
| different-era voices | LTAS differs ≥ 6 dB above 6 kHz; loudness within ±1 LU |

See `references/ltas-method.md` for the algebra and the pitfalls.
