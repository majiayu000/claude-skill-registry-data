---
name: ai-review-of-audio
description: >
  Using multimodal LLMs (Gemini, GPT-4o-audio and similar) as a second pair of ears on a mix
  or radio cut: chunking and proxies, the review brief and JSON schema, timestamped notes by
  category and severity, blind A/B tests with position-bias controls (run both orders, count
  only order-consistent wins), rating tables for restoration variants, hidden-vocal checks on
  generated underscores, and cross-checking model notes against opendubstage qc. Use when
  someone wants an AI to "listen to the mix", review pacing or music, compare two versions of
  a cleanup, judge an A/B, check a generated track for buried vocals, or asks how far to trust
  a model's audio judgement. Do NOT use for ASR-only tasks (transcription-check in
  mix-qc-and-delivery) or for the objective numeric gate itself.
---

# ai-review-of-audio

A multimodal model is a useful listener and an unreliable judge. It hears pacing holes, dead
air, abrupt edges, mid-sentence cuts, hidden vocals and tonal mismatches that energy-based
checks miss; it transcribes lyrics badly, it cannot read absolute levels, and in pairwise
tests it prefers whichever clip you played first (or second). The protocol below keeps the
first and controls the second.

## 1. What it is good at, measured in practice

Against a 190-minute radio cut, a model reviewer produced 280 timestamped notes; the objective
gate (`opendubstage qc`) independently caught 38 of the 139 that overlapped its checks.
The model was the only ear on: cuts that start or end mid-thought; sung vocals under speech
(energy-based masking is not vocal-aware); local rumble and room jumps between adjacent voices
(the tonal check averages per class); music chopped mid-phrase behind a ≥ 1.5 s fade; a
60–90 s music interlude read as a pacing hole. It also caught voices buried in a generated
instrumental that both Whisper and the generator's own lyric channel missed.

What it is bad at: word and lyric transcription (do not use its text); absolute loudness
(it will call −24 LUFS dialogue "quiet" if the previous chunk was louder); consistency across
chunks (scores drift ±2); and pairwise preference (see §4).

## 2. Running a review

- **Proxy**: audio-only `aac 128k` in an mp4 container (sound review), or 360p H.264 CRF 30 + 128k AAC (picture + sound). Inline upload; nothing stored server-side.
- **Chunks ≤ 240 s** (model context and attention both degrade past that); overlap 5 s; convert each note's clip-relative `t` to absolute film time.
- **Brief**: role ("senior documentary editor and re-recording mixer"), the kind of piece and its intent, what the narration and sources are, and the categories to report. Say "timestamps are seconds from the start of THIS clip" and "do not transcribe lyrics". Full briefs in `references/prompts.md`.
- **Schema** (structured output): `summary`, `pacing_score` (1 rushed, 5 ideal, 9 drags), `mix_score` (1–10), `notes[]` with `t`, `t_end`, `category` ∈ {pacing, music, dialogue, ambience, picture, praise}, `severity` 1–3, `note`, `fix`. Ask for praise too: it marks what to protect.
- **Output**: `<label>.json` plus a Markdown digest per chunk with scores and notes. Keep a `.partial.json` as chunks complete so a failed run resumes.
- **Cost control**: the per-chunk summaries are what you read first; drill into notes by severity.

## 3. Reading the notes

- Sort by severity, then by category. Severity-3 dialogue notes ("cuts off mid-sentence") go to the transcription check; severity-3 music notes ("vocals clash") go to the vocals rule; pacing notes ("15 s of dead air") go to bed coverage.
- Cross-check against `opendubstage qc`: match each note to the nearest problem of the same kind within ±15 s and print caught / missed per kind. The misses define which listens must stay in the gate.
- Treat the score as a trend within one run, not a number to ship on. Median mix scores of 3–7/10 across chunks were typical for a rough radio cut in practice; the same mix scored 6 after beds and transitions were added.
- Never make a content edit from the model's transcription; verify the words with ASR on the cue.

## 4. Pairwise A/B: position bias is real

Measured in practice: the same pair of restoration variants, swapped in order, produced the
opposite preference. LLM judges have a strong, documented position bias (Zheng et al. 2023
and later audio-judge work). Rules:

1. **Blind labels**: variants are named A/B (or by random letters), never by method.
2. **Run both orders** for every pair: (A, B) and (B, A), identical prompt.
3. **Count only order-consistent wins**: a variant wins a pair only if it is preferred in both orders; otherwise the pair is a tie. Report wins, ties and order-flips separately; a high flip rate (> 30 %) means the pair is below the model's discrimination threshold and a human must decide.
4. **Rate before you pick**: ask for per-variant scores (intelligibility, naturalness, noise, 1–10) and a one-line reason, then the pick. In practice the model's pick sometimes contradicted its own ratings; treat the ratings as the data and the pick as a tiebreak.
5. **Multi-variant sets** (4–5 chains): present as a labelled set, randomise the order per call, run ≥ 2 orderings, and keep only variants whose rank is stable within ±1 across orderings.
6. **Include a control**: the original clip, or two identical clips under different labels. If the model prefers one identical clip to the other with confidence, discard the run.
7. **Decision rule**: a model A/B shortlists; a blind human A/B on headphones and a TV decides. Nothing ships on a model score alone (NPR §5.11; the texture-floor and WER rules in `dialogue-editing-and-restoration` apply regardless of the model's opinion).

A/B prompt and result table template: `references/prompts.md`.

## 5. Hidden vocals in generated underscores

Generated "instrumental" beds sometimes contain buried vocalisations, hums or words that an
ASR model and the generator's own lyric channel report as empty. Before an underscore goes
under speech:

1. Render the bed alone at full level, 30–60 s windows covering the whole file.
2. Ask the model: "Does this track contain any human voice, singing, humming, chanting, choir, vocoded voice or spoken words, however faint? Answer `none` or list each with a timestamp and a confidence 1–5. Do not transcribe words." Run twice with the windows in different orders.
3. Any report of confidence ≥ 3 in both runs: separate the vocals (BS-RoFormer), inspect the vocals stem's energy, and either use the instrumental stem or drop the track.
4. Also run a separation pass on every generated bed regardless (cheap) and flag vocal-stem energy > −40 dB relative to the mix.

## 6. Prompts that work and prompts that do not

- Good: concrete categories, a required `fix` field, "be specific and practical", a request for things that work well.
- Bad: "rate this mix" with no brief (scores collapse to 6–7); asking for lyrics or exact words; asking for absolute levels in dB; chunks over 4 minutes; asking a picture+sound review to also judge the radio cut (give it the audio-only pass separately).
- Always pass the intent (timeless, unhurried, a feature documentary, not a slideshow) or the model will optimise for a trailer.

## 7. Verify

| Check | Threshold |
|---|---|
| chunking | every chunk ≤ 240 s; absolute timestamps; `.partial.json` present |
| schema | every note has `t`, `category`, `severity`, `note`; `fix` present on severity ≥ 2 |
| A/B | both orders run per pair; wins counted only when order-consistent; flip rate reported; a control pair included |
| hidden vocals | two runs, different window orders; separation pass energy reported |
| cross-check | caught / missed table against `opendubstage qc` within ±15 s |
| decision | no restoration or mix choice shipped on the model alone; a human blind A/B logged |
