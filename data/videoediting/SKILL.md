---
name: videoediting
description: "Use when editing or re-voicing the owner's videos. Video Editing — the owner's own video post pipeline, end to end: correcting HIS OWN VOICE in a finished video (hesitations cut from the real recording, wrong words regenerated with F5-TTS in-filling, never a re-read), re-timing the picture and the burned text to the new voice, the robot panel and Apple-TV-style subtitles, the music bed / typing / limiter mix, the brand vignettes (and the rule NEVER to add them twice), and the measured delivery gates that prove a file is shippable. Use whenever the owner asks to edit, fix, re-cut, re-voice, re-mix, subtitle or re-deliver a video or a screencast — 'fix the audio', 'fix my voice', 'remove the hesitations', 'add the subtitles', 'assemble the video', 'check the video', 'deliver the videos', 'same fix on the other videos' — or any work on sample_project / EXAMPLE SERIES / Sample Project deliverables."
version: "1.0"
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, video, ffmpeg, subtitles, voice]
    related_skills: [ridervoice, camera-and-action]
---
> Ported from the owner's skills library (port 1.0.0, upstream version 1.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos only. Needs `ffmpeg` on PATH, `ffprobe` on PATH, `python3` on PATH, `$F5TTS_VENV`, `$VIDEOEDITING_PIPELINE_DIR`. Not ported (the owner's own records — notes, logs, examples, project data — never ship): `references/CHANGELOG.md`, `references/LEARNED.md`.
> In this copy a folder of the owner's machine is written `<your project folder>` (in code, the `PROJECT_DIR` environment variable); folders of the owner's machine are environment variables the host sets: `VIDEOEDITING_PIPELINE_DIR` (the reference video pipeline: its voice engine and its assets); a path into the owner's own folders is written `<your project folder>/…` (in shell code, `${PROJECT_DIR:?}`); the owner's own folder and project names are written `sample project` (in the case and joiner they had); the brand-vignette assets are written `vignette_<width>x<height>_<fps>.mov`.

# Video Editing — the owner's standard

**The golden rule: the voice in the video is HIS voice.** Nothing is re-read, nothing is dubbed by a voice actor, nothing is "improved" by a
generic model. A hesitation **is cut** from the real recording; a wrong word **is regenerated in his timbre** and only that
stretch is replaced. If a model cannot say the word the way he would say it, **his stays** — his voice with a small
flaw is worth more than a synthetic stretch with the same flaw.

**The second rule: nothing is claimed without measuring.** Every correction passes numeric gates, every delivery passes `verify3.py`.
"Looks fine" is not a result. If a gate fails, state the number that failed.

**Language.** Everything on screen and in code in English (subtitles, robot boxes, file names). Replies to the owner in
his language, short. Final report short: what changed, the numbers, what is left.

---

## 0. Before touching anything: the state of the file

Three questions, every time, in this order:

1. **Does it already have the brand vignettes at the start and at the end?**
   → `python3 tools/detect_vignettes.py <video.mp4>` and `references/vignettes.md`.
   **If it does: NEVER add them again.** Work only on the body; the vignettes are copied from the file itself, intact.
   If it does not: they can be added naturally (11 s at the head + 11 s at the tail, asset of the right resolution) — or exactly
   as the owner says. In doubt between "has" and "has not", **assume it has** and ask in one line.
2. **Is the picture already approved?** (subtitles and robot panel burned in, the owner has already said "it's approved")
   → then it is **audio-only** work: `references/picture-pipeline.md § audio-only mode`. The picture is kept and is
   **re-timed** by the voice time map; text is never rendered again.
3. **What is the source?** Raw recording (VFR!) or an already delivered file? A VFR source goes through `fps=` **before** cutting.

---

## 1. The pipeline map

Root of the reference pipeline: `$VIDEOEDITING_PIPELINE_DIR`
(voice engine in `sample_project/`, venv `$F5TTS_VENV`).

```
new voice                                       picture
──────────────────────────────────────────      ──────────────────────────────────────────
find_fixes.py      speech↔subtitle differences
prep_edits.py      differences → real tasks
evidence.py        2 whisper models per task
report_tasks.py    prep/<k>_brief.md
   ↓ EDITOR agent (references/agents.md)
edits_<k>.json  →  check_edits.py
   ↓
run_fix.sh <k> out_<k>          engine: cuts/regenerates, gates T1/T2/T3
   ↓                            → out_<k>/<k>_voice_fixed.wav + <k>_timemap.json
run_critic.sh <k> out_<k>       measurements per correction (+ --episode)
   ↓ CRITIC agent               verdict per id
apply_verdicts.py edits_<k>.json out_<k>/critic/verdicts.json <round>
   ↓ repeat until 0 redos
                                           apply_to_video.sh <k> out_<k>
                                           ├─ apply_voicefix.py   "virtual raw" (picture that follows the voice)
                                           ├─ retime_cues.py      subtitles to the new timing
                                           ├─ activity.py         screen activity
                                           ├─ edit3.py plan/cut   speed-ups + cut
                                           ├─ run_r3.sh boxes     robot + keys + mix
                                           └─ run_r3.sh final     subtitles + MP4 + deliver
                                                   ↓
                                           validate_text.py  (BEFORE the render)
                                           verify3.py        (AFTER: delivery gates)
```

**Audio-only mode** (picture already approved): skips the whole right-hand side and uses
`sample_project/v2/fix_audio_only.py <finished.mp4> <out_dir> <key> <out.mp4>` — keeps the picture, re-times it by the
map, rebuilds only the body's sound and copies the two vignettes from the finished file.

---

## 2. The non-negotiable laws

| Layer | Law | Where |
|---|---|---|
| Voice | cut from the real recording or regeneration in his timbre; only the replaced stretch | `references/voice-correction.md` |
| Voice | gates T1 (words heard), T2 (no leftovers ≥ 0.25 s), T3 (pitch/level vs the REPLACED stretch) | same |
| Vignettes | if they are already in the file, they are not added again; they are copied intact | `references/vignettes.md` |
| Delivery | 11 + body + 11 (±0.06 s), 50 fps, H.264 High yuv420p bt709, AAC 48 kHz stereo | `references/delivery-gates.md` |
| Delivery | program −18..−15 LUFS, vignettes −14..−11, peak ≤ −0.9 dBTP | same |
| Delivery | sync by **correlation** within a 1× segment, never by an isolated peak | same |
| Subtitles | ≤ 20 chars/s, 1.0–6.5 s, ≥ 0.08 s gap, ≤ 2 lines, ≤ 42 chars/line | `references/subtitles-and-boxes.md` |
| Robot | ≥ 12 s between boxes, end ≥ 3 s before the cut ends, t ≥ 6 s, 7–14 s, text "Name: …" ≤ 118 ASCII chars | same |
| Mix | voice −16.5 LUFS · bed −34 LUFS from 0:14 with ducking · keys −30 dBFS · `alimiter=0.891` | `references/audio-mix.md` |
| Process | **one writer per file**: never two integrations of the same episode at the same time | `references/traps.md` |

---

## 3. How the work is done (pace)

- **Parallel up to the machine's limit**, but never two writes to the same file. The voice engine is sequential per
  episode; different episodes run at the same time. Chrome renders: 4 in parallel.
- **Everything resumable.** MLX segfaults now and then; every long step saves per item and resumes
  (`run_fix.sh`, `run_critic.sh`, `evidence.py` already do this).
- **Two agents per episode**: an EDITOR that decides and an adversarial CRITIC that tries to fail it. The critic only approves
  with numbers. `references/agents.md` has both contracts.
- **Always confirm the file's date** before calling a result good (`ls -la`): the engine stops without writing the wav
  when two corrections overlap, and the old file stays there, misleading.
- Requests to the owner: short. Work: fast and measured.

---

## 4. Self-improvement (mandatory)

This skill must get sharper with every job. **At the end of every job, without the owner asking:**

1. `references/CHANGELOG.md` — one entry: date, file/series, what was done, the final numbers (durations, LUFS,
   how many corrections, how many refused), how long it took.
2. `references/LEARNED.md` — each new lesson in three lines: **Rule** / **Why (measured)** / **How to apply**.
   A correction from the owner goes in immediately, with the prefix `owner:` and his words.
3. If a lesson shows up **twice**, it is promoted: it moves to the reference file of the respective layer (and the
   `metadata.version` of this SKILL.md goes up 0.1). A promoted lesson stops being a "lesson" and becomes a law in the §2 table.
4. If a new gate proves useful, it is added to the gates script, not just to the text.

The test: an identical job, done later, cannot repeat a mistake that is already written here.

---

## 5. References

- `references/voice-correction.md` — the engine, the gates, the overrides, what to do when one fails
- `references/vignettes.md` — the vignette law, how to detect, how to add them if missing
- `references/delivery-gates.md` — formats, loudness, sync by correlation, proofs
- `references/subtitles-and-boxes.md` — Apple TV-style subtitles and robot boxes, and the re-alignment after the voice
- `references/audio-mix.md` — voice, music bed, keys, ducking, limiter
- `references/picture-pipeline.md` — virtual raw, plan/cut, audio-only mode
- `references/agents.md` — EDITOR and CRITIC contracts
- `references/traps.md` — everything already paid for (read before debugging)
- `references/LEARNED.md` · `references/CHANGELOG.md` — the skill's living memory
- `tools/detect_vignettes.py` · `tools/probe_delivery.sh` — the two start-up checks
