---
name: dialogue-editing-and-restoration
description: >
  Cutting and cleaning narration, interview and handheld-recorder recordings for documentary and
  podcast mixes: sentence-exact cuts with measured air and fades, breaths and laughs kept,
  room-tone fills and floors, spectral repair of coughs, throat-clears and thumps
  (opendubstage specrepair), de-rumble and the dialogue chain order, sentence-level
  levelling, and what neural restoration (DeepFilterNet, Resemble Enhance, VoiceFixer,
  de-reverb) may and may not do. Use whenever someone is editing spoken-word audio, asks why
  a cut sounds clipped or "switched on", wants to remove a cough / click / rumble / hiss,
  is choosing or evaluating a denoiser or enhancer, or is tempted to run an AI cleanup over
  interview tape. Do NOT use for music restoration or for matching one voice to another
  (that is voice-matching).
---

# dialogue-editing-and-restoration

Dialogue is the anchor of a documentary mix. The rules below keep it whole (sentence-exact
cuts), keep it human (breaths, laughs, the room) and keep it honest (repair events, not
character). OpenDubStage tool: `opendubstage specrepair` (`opendubstage.restore.specrepair`).

## 1. Cut on sentences, with air

| Rule | Number | Source |
|---|---|---|
| In-point | a sentence start, after a full stop or a pause ≥ 1.0 s | NPR Training checklist; measured in practice |
| Out-point | a real full stop; never on "and so…", a dangling "and", a false start | measured in practice (a model reviewer flagged 35 "mid-" endings in one cut) |
| Pre-roll air | 0.15–0.20 s before the first word; fade-in ≤ 0.08–0.12 s | rule of thumb, derived from the 5 ms Audition minimum and the breath |
| Post-roll air | 0.45–0.60 s after the last word; fade-out ≤ 0.25 s and it must start **after** `last_word_end + 0.20 s` | measured in practice: a 0.30 s tail with a quarter-sine fade is heard as a clipped word when the last word has a long decay |
| Fades inside a passage | 20–40 ms, equal-power; the editor's default 5 ms crossfade removes clicks from non-zero crossings; 60 ms (two video frames) is too long | Adobe Audition community; Taylor & Francis dialogue-editing text |
| Between passages | ≥ 1.0 s; 0.7 s when two parts of one sentence are joined | measured in practice |
| Pause after a passage | 1.5–3 s inside a thought; 5–10 s between thoughts; 12–25 s when the subject changes | interview practice (PremiumBeat; Sundance Collab); Murch on silence |
| Never | cut into a neighbouring word; end a cue inside a laugh, sigh or breath (a "keep span") | Third Coast / Peabody pattern (*Finn and the Bell* kept the stammers) |

Check every cut by transcribing it out of the mix, not by trusting the edit list. The
procedure is in `mix-qc-and-delivery` (`references/transcription-check.md`): normalise
disfluencies ("um", "uh", false starts like "bea-", stutter repeats) on both sides,
treat overlapping cross-talk as optional, and pass a cut if either the all-speaker or the
main-speaker comparison matches (diarisation labels are unreliable). Head and tail
similarity ≥ 0.5 on the first/last six words.

## 2. Breaths, laughs and interjections are content

- Breaths: attenuate −8 dB (−12 dB right before a music post), 30 ms ramps; never delete, or the voice "sounds robotic" (IRPR; NPR practice). Replacing a breath with the same duration of room tone keeps the pause.
- Keep-spans: every `[laughs]`, `[chuckles]`, `[sighs]`, `[sniffs]` plus 0.3 s, and any breath within 1 s of a sentence end. They count as speech for the music and ambience envelopes (music does not rise into a laugh), are excluded from dips and levelers, and a cue may not end inside one (extend to `keep_end + 0.45 s`). Verify: ≥ 95 % of laughs sit at full duck depth; zero cue ends inside a keep-span.
- A second speaker's off-mic interjections stay; ride them up (see `voice-matching`), do not gate them.
- The recording's own room (a car, a kitchen, tape hiss) is a quality, not a fault (LeBlanc, *Fire of Love*; Bergh, *Becoming Led Zeppelin*).

## 3. Room tone

- Fill every hole with room tone; room tone never stacks under speech ("audio levels are additive"); fills built from scraps use equal-power crossfades ≤ 20 ms (Post Audio Tips).
- Lay a learned room-tone floor at −46 LUFS under the whole narration stem and under any synthetic bridge line, below the designed beds and above digital silence. It is what the ear uses to accept a cut, and what makes J-cuts possible.
- Synthesis: take frames in the bottom 10 % RMS with no word within 150 ms (≥ 20 s total); either concatenate the longest clean gaps with 500 ms equal-power crossfades into a 60 s loop (2 s loop crossfade), or synthesise from the median PSD (`n_fft` 2048, Rayleigh magnitude, random phase). Verify: LTAS of the bed within ±2 dB of the learned PSD 100 Hz–8 kHz; autocorrelation peak at the loop length < 0.3.
- Loop lengths that are not multiples of each other (e.g. 41 s and 67 s) so the ear cannot find the cycle.

## 4. Spectral repair: `opendubstage specrepair`

```
opendubstage specrepair SRC DST --events '[[t0,t1],...]' --protected '[[w0,w1],...]' [--thumps [all|JSON]] [--report R.json]
```

- **Replace** (room-tone fill) for a non-verbal event in a pause: cough, throat-clear, sneeze, handling. Boundaries are refined from frame energy against the local floor (`active_db` 6, `peak_db` 10, `merge_gap` 0.25 s, `search` ±0.5 s) inside the gap the protected word intervals leave (`guard` 10 ms); the patch is room tone from the nearest quiet stretch within `context` 30 s, EQ-matched to the local noise spectrum (1/3-oct, clamped ±6 dB), level-matched, spliced with 30 ms equal-power crossfades. This is RX "Spectral Repair > Replace" plus "Ambience Match".
- **Attenuate** for an event that overlaps speech or a low-frequency thump: per-bin magnitudes above the context reference (median of the surrounding frames, or a left/right interpolation) are pulled down to it, optionally only below `fmax`; phase is kept. Thump detector: 20–150 Hz band jumps ≥ 12 dB over its 2 s running median with a ≥ 9 dB rise, ≤ 0.5 s long, and LF within 3 dB of the 300–3000 Hz band at the peak (speech is mid-heavy, a thump is LF-heavy); attenuate bins up to 250 Hz.
- Samples outside the reported regions are bit-exact to the input; verify with a sample diff and a cross-correlation lag of 0.
- Event seeds come from the transcript's audio-event tags (`[coughs]`, `[clears throat]`, `[sneezes]`, `[microphone rustling]`) refined ±0.3 s by spectral flux in 1–6 kHz (> median + 12 dB for ≥ 3 frames).
- Verify after repair: energy inside each event window within 3 dB of the surrounding floor; neighbouring words untouched; Whisper transcript before = after; DNSMOS not lower. Leave `[sniffs]` at −10 dB attenuate rather than replace (a synthesised 600 ms gap where someone inhaled reads as an edit).
- Mouth clicks: detect with a 3 kHz high-pass, 2 ms frames, kurtosis > 8, duration < 10 ms, only in word gaps > 80 ms; fill with `adeclick=w=20:o=75:a=4:t=1.5` under `enable=between(t,…)`. Autoregressive fills are valid to ~45–80 ms (Mokrý & Rajmic 2024); nothing packaged does longer gaps well.
- A gain dip is the fallback, not the method: a −22 dB step is an edit you can hear. If you must dip, widen 40 ms and ramp in three steps (0.3 / 0.08 / 0.3).

## 5. De-rumble and the chain order

Order: repair → high-pass / sub-cut → subtractive EQ → de-ess → compressor → presence → sentence-level ride → the stem is measured once.

| Stage | Starting point | Check | Source |
|---|---|---|---|
| Sub-cut + high-pass | `asubcut=cutoff=70:order=10,highpass=f=90:p=2` (phone or handheld-recorder narration); 100–120 Hz for a distant camera microphone | band < 100 Hz ≥ 25 dB below the 1 kHz band | Krotos; measured in practice |
| Proximity guard | do not go further: energy 100–250 Hz stays within 12 dB of the 1 kHz band | per-cue band ratio ≥ −12 dB on ≥ 95 % of cues | Mangini (*32 Sounds*): headphones carry the intimacy |
| Boxiness | 250–400 Hz −2 to −4 dB, Q ≈ 1.5; small-room boom 1.5 kHz −1.5 dB | LTAS within ±4 dB of target 200 Hz–5 kHz | Gearspace ("cut more than boost") |
| De-ess before compression | `deesser=i=0.3:m=0.5:f=0.5` | | Joey Sturgis Tones |
| Compression | 2:1–3:1, 3–6 dB GR on peaks, attack 5–10 ms, release 100–250 ms | | Gearspace |
| Presence | +1.5 to +3 dB at 3–5 kHz, Q ≈ 1, only if dull after NR | | Krotos |
| Leveler | per-sentence gain `clamp(target − L_s, −6, +8)` dB, slope ≤ 3 dB/s, 150 ms raised-cosine joins placed in the air between words; then a light 2:1 for intra-sentence peaks | sentence loudness std ≤ 1.5 LU per cue; dialogue-only LRA ≤ 7 LU | Netflix (dialogue LRA ≤ 7); Auphonic (talk ≈ 5) |
| Not | `dynaudnorm` (breathes in 100–500 ms frames), `speechnorm` (half-cycle gain pumps on breathy speech) | | measured in practice |

## 6. Neural restoration: what it may and may not do

The failure that matters: a model can raise DNSMOS while destroying off-mic speech and
timbre. Measured in practice: the same denoiser that was transparent on phone or handheld-recorder narration
produced "severe musical noise, aggressive gating, underwater robotic artefacts" on a distant
recorder and dropped a second speaker's interjections. Judge on the voice you cannot afford to
lose, not on the mean opinion score.

Rules:

1. **Nothing generative on live sound** (ceremonies, performances, crowd). Generative enhancers (Resemble Enhance's enhancer stage, VoiceFixer, AudioSR, Adobe Enhance v2) resynthesise; they hallucinate consonants, remove laughter and change timbre. Denoise-only modes and DeepFilterNet3 are subtractive and safe to try.
2. **Process lightly, in stages, and blend**: 60–80 % wet with 20–40 % dry (`amix` with weights), or keep a quieter copy of the original as a noise bed. Delta-listen (processed minus original): words in the delta mean over-processing.
3. **The texture floor is a binding limit**: the cleaned noise floor in word gaps may sit at most 6 dB below the raw floor on ≥ 95 % of cues (10 % trimmed mean of gap RMS, gaps ≥ 0.4 s). Beyond that the room disappears and musical noise appears (Bergh: "no broadband denoise anywhere in this film").
4. **De-reverb is the hard part.** WPE (`nara_wpe`, 48 kHz: STFT 1024/256, taps 10, delay 3, 3 iterations) removes late reverb only and is safe; apply before denoise. Anything stronger is a blind-test candidate, not a default.
5. **Measure, then listen blind**:
   - WER on **secondary speakers** and on the quietest 10 % of words, not just the main voice;
   - timbre: 1/3-octave LTAS delta ≤ 2 dB 200 Hz–6 kHz, or speaker-embedding cosine ≥ 0.9 vs the original;
   - DNSMOS SIG not lower (BAK may rise);
   - the texture floor rule above;
   - a blind A/B in both presentation orders (see `ai-review-of-audio` for the position-bias protocol), then a human on headphones and on a TV. Adopt the lightest chain whose transcript is not worse and whose delta carries no words.
6. **Where not to process**: passages that are already clean; any span whose speech-to-floor is > 25 dB; music that is the content; the one explicit passage you have excluded anyway.
7. **Separation for speeches recorded over a band** (BS-RoFormer via `audio-separator`): remix, do not replace. Vocals stem up, residual (band + crowd) −6 to −9 dB, and keep the residual ≥ −20 dB relative to the separated speech so a speech still sounds like a room full of people (Kwok on *Get Back*: keep the audience "in the room").

See `references/restoration-tools.md` for the tool table (local, Apple-silicon, licence, batch) and the RX-process equivalents.

## 7. Verify (binding numbers)

| Check | Threshold |
|---|---|
| every dialogue cue | `fade_in ≥ 0.05`, `fade_out ≥ 0.25`, `last_word_end + 0.35 ≤ cue_end` |
| transcription check | head and tail ratio ≥ 0.5 for every narration cue |
| rumble | < 100 Hz ≥ 25 dB below 1 kHz |
| proximity | 100–250 Hz within 12 dB of 1 kHz |
| repaired events | window energy within 3 dB of the floor; bit-exact outside |
| leveler | sentence std ≤ 1.5 LU; dialogue LRA ≤ 7 LU |
| restoration | texture floor Δ ≤ 6 dB; WER on secondary speakers unchanged; embedding cosine ≥ 0.9 |
| clicks | `adeclick` in save mode reports < 1 click/min outside repaired events |
