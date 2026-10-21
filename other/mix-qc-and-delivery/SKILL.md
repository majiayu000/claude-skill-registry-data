---
name: mix-qc-and-delivery
description: >
  The objective QC gate and delivery specs for a spoken-word mix (documentary, radio feature,
  podcast): dialogue-anchored loudness, true peak at 4x oversampling, LRA, dead air, clicks
  at cue edges, masking, level jumps, tonal balance, the transcription check of every
  narration cut, the half-volume test and the multi-system listen, with the thresholds and
  their sources (PRSS, ATSC A/85, EBU R128, Netflix, Torcoli/AES) and the opendubstage qc CLI.
  Use before any picture render, when someone asks "is this mix ready", "what loudness should
  this be", "why does the limiter still show overs", "is there a click here", "how do I check
  the cuts", or when writing a verify step / CI gate for a mix. Do NOT use for choosing
  processing (dialogue-editing-and-restoration) or music placement (music-under-narration).
---

# mix-qc-and-delivery

The mix is checked before any picture is rendered. A late mix failure after a picture
render cost hours in practice; the gate exists so that cannot happen again. OpenDubStage tool:
`opendubstage qc` (`opendubstage.qc.mixqc`: `qc(mix, cues, stems, thresholds)`, `Thresholds`).

```
opendubstage qc MIX.wav [--cues SHEET.json] [--stem dialogue=DX.wav --stem background=BG.wav] [--thresholds T.json] [--json OUT.json] [--md OUT.md]
```

Exit 1 when a blocking check fails. Without a cue sheet only the programme-wide checks run
(loudness, LRA, true peak, dead air). Cue-sheet schema and the full threshold table with
sources: `references/thresholds.md`.

## 1. Delivery specs

| Spec | Integrated | True peak | Notes |
|---|---|---|---|
| PRSS (public radio distribution) | −24 LUFS ± 2 | −2 dBTP (sample −3) | Current 2014; Radio World |
| ATSC A/85 | −24 LKFS ± 2, dialogue-anchored | −2 dBTP | |
| Netflix v1.5 | dialogue −27 LKFS ± 2, dialog-gated | −2 dBTP | LRA programme 4–18 LU, dialogue ≤ 7 LU (guidance) |
| EBU R128 | −23 LUFS ± 1 | −1 dBTP | LRA descriptive; talk ≈ 5 LU (Auphonic) |
| Apple Podcasts | −16 LKFS ± 1 | −1 dBTP | |
| AES TD1004 streaming | −16…−20 LUFS | ≤ −1 dBTP | lossy codecs overshoot |
| Home-viewing feature (recommended) | **dialogue −24 LUFS dialogue-gated ± 1**; programme free (expect −22 ± 3) | **≤ −2 dBTP after the codec; ≤ −2.3 before AAC** | LRA 8–18 LU reported, not clamped; dialogue-only LRA ≤ 7 |

Anchor on dialogue, not on the programme: measure dialogue-gated loudness on the dialogue +
live-speech stems, apply **one linear gain**, then a limiter as the only non-linear stage.
Never `loudnorm` in dynamic mode on a long mix: ffmpeg falls back to dynamic (3 s window
compression) whenever the measured LRA exceeds the target LRA; check the first pass's
`normalization_type`.

## 2. True peak

A sample-peak limiter misses inter-sample overs. Measured in practice: a mix limited at
−2.5 dBFS sample read −1.3 dBTP. Rules:

- Limit at 4× oversampling (ITU-R BS.1770-4) or set the sample ceiling 0.6 dB below the target: `alimiter=limit=0.74` (−2.6 dBFS) to land ≤ −2.3 dBTP before AAC, ≤ −2 after.
- Verify with `ebur128=peak=true` or `opendubstage qc` (`true_peak_max` −2.0), never with the limiter's own meter.
- Leave 0.3–0.5 dB for the codec; re-measure the encoded file.

## 3. The checklist

| # | Check | Threshold | Gate | Source |
|---|---|---|---|---|
| Q1 | dead air | no span < −60 dBFS sample peak for > 3 s (strict: −50 dBFS / 2 s), head and tail 5 s exempt, designed silences whitelisted | blocking | `silencedetect`; Torcoli (ambience ≥ 15 LU under speech) |
| Q2 | gaps are air | momentary (400 ms) ≥ −46 LUFS in every speech gap; ambience in the clear −38…−42 LUFS | blocking | Torcoli; Tech 3341 |
| Q3 | dialogue anchor | dialogue-gated −24 ± 1 LUFS | blocking | PRSS; A/85 |
| Q4 | programme | integrated −27…−16 (report); LRA 4–18 LU; dialogue-only LRA ≤ 7 (narrated segments ≤ 10, live ≤ 15 advisory) | advisory | Netflix; Auphonic; Tech 3342 |
| Q5 | true peak | ≤ −2.0 dBTP at 4× oversampling (−2.3 before AAC) | blocking | PRSS; Netflix; BS.1770-4 |
| Q6 | every voice at the same level | short-term (3 s) per voice class within ±2 LU of −24; per-cue sentence std ≤ 1.5 LU | advisory | Byers |
| Q7 | tonal balance | 1–4 kHz presence share per voice class within ±4 dB of the class mean; LTAS per class within ±3 dB of the reference 200 Hz–6.3 kHz | advisory | RX EQ Match practice; measured in practice |
| Q8 | rumble | < 100 Hz ≥ 25 dB below the 1 kHz band on dialogue | advisory | measured in practice |
| Q9 | masking | music + ambience ≤ dialogue −10 dB in 1–4 kHz over any ≥ 3 s stretch of speech (strict: −14 dB in 1.2–4.8 kHz, 99th percentile); broadband music ≤ −10 LU, ambience ≤ −15 LU | blocking (default) | Torcoli; Shirley & Kendrick |
| Q10 | no vocals under speech | no `under` cue overlapping speech > 1 s whose section has vocals | blocking (plan) | NPR practice |
| Q11 | music entries | downbeat / section / song start ≤ 60 ms; `fade_in ≥ 0.5` mid-song; none within 2 s before a first word | blocking (plan) | Menjivar |
| Q12 | music exits / posts | every `under` cue ends on a downbeat or section end with ≥ 1 s out; posts 2–12 s; music-only > 15 s flagged | advisory | Menjivar |
| Q13 | music density | per 10 min: 30–70 % music; no cue > 150 s under speech; no dry stretch > 90 s without bed | advisory | Menjivar |
| Q14 | crossfade at every boundary | ±3 s: a non-dialogue stem non-zero on both sides ≥ 1.5 s; music adjacency gap < 0.1 or ≥ 3 s or overlap ≥ 1.5 s | blocking | `check_transitions` |
| Q15 | edit points | every dialogue cue `fade_in ≥ 0.05`, `fade_out ≥ 0.25`, `last_word_end + 0.35 ≤ cue_end` | blocking | Audition 5 ms rule; measured in practice |
| Q16 | clicks | sample step > 8× the local difference RMS within ±5 ms of a cue edge, above −60 dBFS; `adeclick` save-mode < 1 click/min outside repaired events | blocking | engineering practice |
| Q17 | speech heard correctly | transcription check: head and tail ratio ≥ 0.5 for **every** narration cue; key live phrases ≥ 0.75 | blocking | measured in practice |
| Q18 | event residue | energy inside each repaired event window within 3 dB of the floor | advisory | |
| Q19 | restoration safety | DNSMOS SIG not lower than source; speaker-embedding cosine ≥ 0.9; texture floor Δ ≤ 6 dB; WER on secondary speakers unchanged | blocking for any neural pass | Smule 2025 metrics; measured in practice |
| Q20 | half-volume test | mix attenuated 12 dB plus a −50 dBFS pink floor: Whisper WER on 10 random 30 s windows ≤ 1.3× the WER at full level | advisory | Byers: "turn it down halfway, can you understand every word?" |
| Q21 | level jumps | > 5 LU between adjacent voices' momentary max within 1.5 s of a voice-to-voice edit; scene starts exempt | advisory | JND ~1 LU; A/85 ±2 LU |
| Q22 | hard stops | music / ambience / effects fade-out < 1.5 s while still sounding (programme end exempt) | advisory | Byers |
| Q23 | mix length | mix = timeline ± 0.05 s; picture later = audio ± 0.05 s | blocking | |
| Q24 | anti-fatigue | every 10-min window has ≥ 2 of {music enters/exits, bed change, live sound, ≥ 90 s music-free} | advisory | Kwok, *Get Back* |
| Q25 | separated speech keeps the room | residual stem ≥ −20 dB vs separated speech in every separated span | advisory | *Get Back* |

Blocking by default in `Thresholds`: `loudness`, `dead_air`, `click`, `masking`. Tune per
programme; every threshold carries its source in the dataclass.

## 4. Two rules learned the hard way

**Dead air comes from beds shorter than their scenes.** Before mixing, check every bed's
source length against the span it must cover (loop it, or crossfade a second bed); then run
the detector. Designed silences are whitelisted explicitly (a list of `(at, dur)`); the
dead-air check reads the list; nothing else passes.

**Only hard edits can click.** A cue edge with a fade ≥ 50 ms cannot produce a step
discontinuity; a transient found at a faded edge belongs to other content (a consonant, a
spot effect, the music) and is not a click. Report clicks only on edges whose fade is
< 50 ms, and report the fade length with the finding so the reader can tell the two apart.

## 5. The transcription check (every cut)

Transcribe each narration cue out of the finished mix (not the source) and compare its
first and last six words with the word-timed transcript. Procedure in
`references/transcription-check.md`. Essentials:

- normalise both sides: lower-case, strip punctuation, drop fillers (`um uh er ah hmm mm`), drop false starts (tokens ending in `-`, e.g. "bea-"), collapse stutter repeats (Whisper smooths these; the transcript keeps them; neither is a clipped word);
- overlapping cross-talk is optional: Whisper drops the other speaker, so build two expectations, all speakers and the main speaker of the cue (most common label), and **pass if either matches** (diarisation labels are unreliable);
- `difflib.SequenceMatcher` ratio on `want[:6]` vs `got[:8]` and `want[-6:]` vs `got[-8:]`; pass when head ≥ 0.5 and tail ≥ 0.5;
- check **every** cue: a 12-cut sample missed "and--" endings a model reviewer heard;
- for live scenes, check that a handful of key phrases are heard (fuzzy ≥ 0.75).

## 6. The humans

- **Multi-system**: a 90 s excerpt bounced through a phone-speaker EQ (`highpass=300, lowpass=6000`), a laptop and the living-room TV, at normal volume (Tavella checked *The War* on six to eight systems down to an 11-inch mono TV).
- **Headphones**: three 60 s excerpts (opening, a bed-heavy passage, the ending) on open-back headphones before lock; −40 LUFS beds and spot effects that vanish on a TV are plainly audible there (Mangini, *32 Sounds*).
- **Half volume**: Byers' test, by ear as well as by Q20.
- **The witnesses sign off**: the people who were there decide, on their own system.

## 7. What the automated gate does not hear

Measured in practice against a model reviewer's 139 relevant notes: the checks caught 38
(dead air 21/31, masking 9/25, level 8/29, abrupt edges 5/47, tone 6/49). The misses were
content edits (mid-sentence cuts: covered by the transcription check once it runs on every
cue), local rumble (the tonal check compares class averages, not moments), sung vocals under
speech (energy-based masking is not vocal-aware) and music chopped mid-phrase with a ≥ 1.5 s
fade still present. Keep the transcription check, the model listener (`ai-review-of-audio`)
and the human listens in the gate; the numbers alone pass mixes a professional would not.

Known blind spot: a cue wrongly tagged as non-speech (e.g. a live-music bypass applied to a
speech) drops out of the duck sidechain and out of every dialogue check. Assert the count of
bypassed cues in the build, and that known speech sources are not among them.
