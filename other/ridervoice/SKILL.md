---
name: ridervoice
description: "Use when speaking text in the owner's own voice. Rider Voice — the owner's voice spoken by a model trained on his voice (F5-TTS v1 Base fine-tuned). Use ALWAYS when the owner says /ridervoice, 'speak in my voice', 'say this in my voice', 'make an audio of me', 'narration in my voice', 'voice over', asks for an English audio/voice-over/narration for a video, podcast, presentation or message, or asks to re-train/improve/evaluate the voice model. Covers: speaking a text (say.sh), measuring against his real profile (check.sh), revoicing a finished video fitted to its subtitles (revoice.sh), a RAW video made from scratch with his voice (voice first, sample_project), the text rules, the gates, re-training with new voice data and the mandatory self-improvement."
version: "1.5"
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, voice, TTS, F5-TTS]
    related_skills: [videoediting]
---
> Ported from the owner's skills library (port 1.0.0, upstream version 1.5; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos only. Needs `ffmpeg` on PATH, `python3` on PATH, `$RIDERVOICE_HOME`, `$F5TTS_VENV`, `$RIDERVOICE_DIR`, `$RIDERVOICE_SUBTITLES_DIR`, `$RIDERVOICE_PIPELINE_DIR`, `~/Movies`. Not ported (the owner's own records — notes, logs, examples, project data — never ship): `references/CHANGELOG.md`, `references/LEARNED.md`, `references/pronunciation.md`, `references/revoice-video.md`, `references/training-record.md`, `tools/revoice.sh`.
> In this copy measured voice-profile numbers of a real person are written `<n>`; folders of the owner's machine are environment variables the host sets: `RIDERVOICE_DIR` (the Rider Voice folder: engine, docs and samples), `RIDERVOICE_SUBTITLES_DIR` (the subtitles of the videos to re-voice), `RIDERVOICE_PIPELINE_DIR` (the raw-video pipeline); the owner's own folder and project names are written `sample project` (in the case and joiner they had); a value labelled as the owner's own prosody is written `<n>` or left out; pointers to a file that is not ported are left out.
> Kept by the owner's decision: "Rider Voice" (the owner's product name and public persona, kept by his decision).

# Rider Voice — the owner's voice

**What it is.** A model that speaks like the owner in English: his timbre, pitch, intonation, rhythm and pauses, without
hesitations, studio-clean. Trained on his real voice (28.7 clean min, 224 sentences) and **approved by the owner** on
the owner's own verdict: "velocity, entonation, pronunciation, space between phrases is all very similar".

**Where it is.**
- Model + references + profile: `$RIDERVOICE_HOME/` (`model/rider_v1_ck2000.safetensors`, `model/vocab.txt`, `refs.json`,
  `refs/*.wav`, `profile_his_voice.json`). Outside iCloud on purpose.
- Full engine, docs and samples: `$RIDERVOICE_DIR/` (local git). Heavy training work:
  `~/Movies/sample_project/`.
- Environment: `$F5TTS_VENV` (F5-TTS 1.1.22, mlx-whisper, resemblyzer, jiwer). GPU = Apple MPS.

## 1. Speak (the everyday case)

```bash
{skill_dir}/tools/say.sh "The text to say. Short sentences work best." out.mp3
{skill_dir}/tools/say.sh @script.txt out.wav --speed 1.12 --seed 23
```

Approved defaults: `--speed 1.12` (= his real rhythm, <n> words/s), `--pause 0.4` (pause between sentences), `--seed 23`, `--verify 3` (each sentence is heard by whisper and re-generated with another seed while
a word is missing or extra), mastered to −16 LUFS / peak −1.5 dBTP, 48 kHz. `--no-master` gives the raw 24 kHz output.

**Text rules** (the model reads characters):
- English. Short sentences (7–25 words); sentences under 7 words are merged with their neighbour automatically.
- Numbers spelled out: "number seven", "two thousand twenty six", "ten percent". Never digits.
- Names as they are written and as he says them: iCLONE OS, iNFT, Virtuals Protocol, Claude Code, GitHub, OpenSea, KYC.
  Rare/foreign words may need phonetic spelling; `--verify` catches most of them.
- Only letters, space and `. , ? ! '` (`;` and `:` become commas). No emojis, markdown, parentheses.
- Punctuation is prosody: comma = short pause; full stop = his pause; `?` rises.

## 2. Measure (never deliver without numbers)

```bash
{skill_dir}/tools/check.sh out.wav "The text to say. Short sentences work best."
```

Gates (from `SAMPLE_PROJECT.md`): WER ≤ 0.10 · 0 fillers · 0 repetitions · similarity ≥ 0.90 (the finals give 0.97–0.98)
· pitch ±2.5 st · rhythm 0.85–1.25× · median pause <n> s · noise floor ≤ −55 dBFS · peak ≤ −1 dBFS in the
delivered file. One FAIL = re-generate (another seed, or split the sentence) before delivering. For a large batch
(8+ texts), the adversarial critic (Opus agent with `engine/SAMPLE_PROJECT.md`) reads the measurements and approves only with numbers.

## 3. Deliver

- Files with a readable name (`s01 - Title.mp3`), WAV + MP3 when it is for the owner to listen on his phone (SendUserFile
  delivers straight to the iPhone via Remote Control).
- Always state the measured numbers (WER, similarity, rhythm) in one line; "sounds good" is not a result.

## 3b. Revoice a finished video (the video's whole voice becomes the model's)

When the owner asks "do the video's voice with the model", "replace my voice in the video", "revoice": the picture (burned-in subtitles and
panel, vignettes) is not touched; the speech is regenerated **group by group from the subtitles**, fitted into each window
(speed first, time-stretch only as a last resort), verified word by word and by forced alignment, and the
body sound is remixed with the original recipe (music, keys, ceiling). Full step-by-step, gates and traps in
`references/revoice-video.md`.

```bash
{skill_dir}/tools/revoice.sh <in_folder> <out_folder> [keys]          # sample_project series (+ d1)
$F5TTS_VENV/bin/python "$RIDERVOICE_DIR/engine/revoice_video.py" <key> in.mp4 out.mp4
$F5TTS_VENV/bin/python "$RIDERVOICE_DIR/engine/verify_revoice.py" in.mp4 out.mp4 cues.srt --voice <key>_voice_new.wav
```
The owner's video is replaced only when `verify_revoice` says `PASS` (duration, identical video stream, vignettes, −18…−15 LUFS,
WER ≤ 0.10, every cue within ≤ 0.5 s **by forced alignment**, voice in the mix at lag 0). The originals go to a `DATA/` subfolder.
A video that fails on 1–2 words is fixed with `MODE=patch SEED=<new> revoice.sh … <key>` (regenerates only the groups with
errors, reuses the rest); never regenerate the whole video for one error.

## 3c. Raw video (screen recording with his voice, no subtitles): the voice first, the picture follows it

When the owner hands over a raw recording and asks "prepare the full video, transcribe it and fix the voice with my model" (sample_project): word-by-word transcription → clean US English script (script critic) → **voice sentence by sentence at his rhythm**
→ picture **re-timed to the voice** (anchors on the 1st/last word of each sentence + event anchors: a click lands on the word that says it)
→ subtitles from the forced alignment of the new voice, positioned by screen → robot, music, keys, vignettes → gates → delivery critic.

```bash
P=$RIDERVOICE_PIPELINE_DIR
$P/run_a1.sh 3                                   # everything: voice → plan → subtitles/layout → robot → mix → assembly → 14 gates
$F5TTS_VENV/bin/python $P/voice_a1.py $P/text/script_a1.json ~/Movies/sample_project/voice --cands 3 --only 12 --speeds 1.06,1.12,1.18
$F5TTS_VENV/bin/python $P/tone_ref.py $P/text/script_a1.json <recording.mov> $P/qa/tone_ref_a1.json
$F5TTS_VENV/bin/python $P/sample_project.py $P/text/script_a1.json ~/Movies/sample_project/voice $P/qa/tone_ref_a1.json   # the whole sequence, in his tone
```
**The tone is his, and the whole sequence is chosen** (owner: "aggressive, off tone, the last sentence does not finish"):
`tone_ref.py` measures on his recording, sentence by sentence, the relative pitch, the relative energy and the final contour; `sample_project.py` applies the hard
gates per take (words · name by TWO recognisers in context AND in the sentence cut on its own · sim ≥ 0.86 · intonation ≥ 1.3 st ·
<n> words/s · silences ≤ 0.22 s within the sentence / ≤ 0.65 s at punctuation · **the LAST WORD of each on-screen sentence: ≤ +0.3 st
on '.', ≤ +4.5 st on ','; pitch ±1.8 st and volume ≥ −3.5 dB between neighbouring sentences; the sign-off falling**) and chooses the sequence by
Viterbi (cost against his tone + jump cost between neighbours). Never `!` for the model (it shouts and rises at the end).
`NO take passes every hard gate` on a sentence = generate 24 more takes of that sentence (`--only g --refs … --speeds … --append`), never
assemble with the "least bad" one: the verifier has the same gates and fails the assembly (20 min lost per round, sample_project r13–r15).
Spelling for the model: iNFT → `eye N F T`, iclone os → `eye clone oh ess` (written as-is it almost always fails at the end of the sentence).
One reference can pull a sentence 3 st higher in every take: `voice_a1.py --cands … --refs 0,1,2,5` swaps them.
The numbers of the first delivery live in the owner's own records, which this port does not ship.

## 4. Improve the model (when there is new voice data of his)

Full pipeline in `$RIDERVOICE_DIR/engine/` (see `references/pipeline.md`):
clean (`df_clean.py` + `voice_chain.sh`) → `segment.py` (cuts hesitations, 2 listens) → `make_dataset.py batches` →
text editors (Sonnet, `SAMPLE_PROJECT.md`) → `make_dataset.py build` → `train.sh` → `auto_eval.sh` →
critic (`SAMPLE_PROJECT.md`) chooses the checkpoint → export slim to `$RIDERVOICE_HOME/model/` → samples → approval.
Overfitting shows up after ~2000
updates with 29 min of data (repetitions, rising pitch): always evaluate with 2 seeds.

## 5. Self-improvement (mandatory, on every use)

At the end of every job with this skill, without the owner asking:
1. `references/CHANGELOG.md` — date, what was spoken/trained, the numbers, what failed and how it was solved.
2. `references/LEARNED.md` — each new lesson in three lines (**Rule / Why (measured) / How to apply**); a correction from the
   owner goes in on the spot with the prefix `owner:` and his words.
3. A lesson that appears twice is promoted to the right section of this SKILL.md or into the engine (a new gate
   goes into the script, not only into the text) and `version` goes up 0.1.
4. Words the model says wrong go into `references/pronunciation.md` with the spelling that worked.

## 6. References

- `references/pipeline.md` — the engine step by step, paths, commands, traps already paid for
- `references/revoice-video.md` — replacing the whole voice of a finished video, fitted to the subtitles: method, commands, gates
- `references/pronunciation.md` — hard words and the spelling the model reads well
- `references/LEARNED.md` · `references/CHANGELOG.md` — the skill's living memory
