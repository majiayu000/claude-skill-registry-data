---
name: editor-v3
description: "Editor V3: a cinematic long-format edit in a backlit side-profile silhouette style. The speaker talks as a near-black silhouette on a colour backdrop (red, blue, pale teal, one colour per chapter), with date titles inside the head, huge words behind the head, film burns, typed screens, counting charts, sparse B-roll, music and hard sound effects, always 16:9. The silhouette clips are made in Higgsfield from the speaker's own recording, then everything else is cut locally. Use whenever someone says Editor V3, side effect, silhouette edit, or asks for this style."
---

## Video Studio (read first; overrides the rest of this file)

This skill is installed in Video Studio (`Edits/.claude/skills/`), from the NextPhase / creator packs
Bryan downloaded on 2026-10-31. Video Studio's `CLAUDE.md` wins wherever the two disagree.

- **Start from the studio job, never an intake.** Jobs come from the studio page (`jobs/<id>/job.json`).
  This skill runs when the job's `style` is `silhouette`. Never ask "short or long?" or "which style?":
  the page already asked. (`nextphase-studio`'s intake is not used here.)
- **One transcript:** `projects/<id>/transcript/words.json` (WhisperX). Don't run this skill's own transcriber.
- **Brand:** `styles/brand.json` (purple `#8B5CF6` / `#C4B5FD` / `#4C1D95`, Inter + Playfair Display)
  replaces this skill's default colours. Generate its theme/tokens from it.
- **Show the motion graphics before rendering (Bryan's rule):** design first, show stills of each graphic over
  the real frame in batches (the `design` → `graphics` stages, `graphics.json`), wait for approval, then render.
- **Sounds and music:** the studio's library (`styles/sfx.json`, `node studio/sfx.mjs place`) on the locked
  picture; music only from tracks Bryan owns or licensed.
- **Windows Git Bash, not macOS/WSL:** `python` not `python3`; a venv's Python is `Scripts/python.exe`;
  long paths fail, so map a short drive (`cmd //c "subst R: <winpath>"`). Run this skill's setup/doctor script
  only the first time the style is used, and ask before any download over ~500 MB.
- **Where work goes:** editing work in `projects/<id>/`, deliverables in `jobs/<id>/`.
- **Costs credits:** the silhouette clips are made in Higgsfield from Bryan's recording. Before any generation, show the credit cost and wait for his yes. Needs a second take filmed from the side (`needsTwoTakes`).


# Editor V3

**Format: always 16:9, 1920x1080.** Read `reference/study.md` before planning anything. It holds the look, the colours, the type, every transition frame by frame, the beat map, the pacing and the sound.

## Rules

- **Nothing in Higgsfield before there's a recording.** No generations, uploads, price checks or model lookups.
- **The silhouette is made in Higgsfield, not faked in code.** No local matte or colour grade to fake it. Everything else is edited locally: cuts, captions, titles, charts, transitions, sound. Generated video never does the editing.
- **Credits need approval.** Show the shot list with the credits on a local browser page and wait for a clear yes before spending anything.
- **Real people only.** Every shot of the person starts from their real footage. No invented people.
- **Use the song in the kit** (`music/song.m4a`) unless they give you another. Never pick music yourself.

## What you need from them

1. **A front take:** talking to the camera. This gives the voice and the script.
2. **A side take:** the same script, filmed from the side, as close to a plain profile as they can get. This gives the outline and the mouth. Filmed with the face pointing right is fine, you mirror it. Without a side take, stop and ask them to film one, because the mouth won't match otherwise.
3. **B-roll (optional but good):** 1 to 4 clips of them working at a desk, side on.
4. **A connected Higgsfield account with credits.** If the connector isn't there, tell them how to add it and wait. Before quoting anything, check the prices and model names are still current with `models_explore`.

## How to make a video

Start a folder with `bash ~/.claude/skills/editor-v3/scripts/new_project.sh <name>`. It copies the worked example from `template/` to `~/editor-v3/videos/<name>/`. Put the footage in `raw/`. Run Python with `~/.claude/skills/editor-v3/scripts/py`.

1. **Voice first.** Transcribe the front take (`scripts/transcribe.py take.mp4 --out work/take_tx.json`). Write `cut.json` (the format is at the top of `scripts/voicecut.py`) and run `scripts/voicecut.py <project>` to get `work/voice.wav`. Mistakes and restarts come out. Then transcribe each kept section on its own with `--from` and `--to`, because a whole-file pass can hide a line said twice. Read them.
2. **Line up the two takes.** Their words will differ a little, so match them phrase by phrase. Where the side take has no version of a line, cover that line with a typed screen or B-roll. Never force a mouth.
3. **Plan the shots** in `shots.py`, using the beat map in the study: about half the time on the silhouette, one backdrop colour per chapter, dated titles, numbers that move, a false win, a question that stops the video, then a plain final take with no effects. Rewrite the story around their script. The example is one real video, not a formula.
4. **Show the storyboard and the credits** (`storyboard.py` builds a local page, once the chapter stills exist; before that, show the list and the cost). Wait for approval. Say what the total will be first. For scale: 12 clips and 49 seconds on Kling Pro cost about 98 credits, and each still costs 0.25.
5. **Make the silhouette clips**, as below.
6. **Edit.** Rewrite the timeline `T` at the bottom of `edit.py`. Each shot gets knots that map voice time to side-take time, so the mouth stays on the words. `edit.py 12 18 work/out/test.mp4` renders a piece to check it.
7. **Mix.** Change the moments in `mix.py` and set the voice, the song and the drop. A new mix takes seconds and copies the picture.
8. **Render everything** with `bash render_all.sh`. It runs four parallel pieces and mixes the sound, writing `work/out/final.mp4`.
9. **Check before you show it.** Look at frames either side of every cut. Check the titles aren't hidden by the head and the type doesn't leak through glasses. Transcribe every section with the music on, to prove the words still read. You can't hear the audio, so say that levels are measured only.

## Making the silhouette clips

Tested on one 5 s clip of a real side take, against three models. **Kling 3.0 Omni Edit won** (`kling_video_edit`, roles `video_references` plus `image_references`, mode `pro`, 2 credits a second at 1080p, or `std` at 1.5 at 720p, or `4k` at 6).

1. Mirror the side take if needed so the face points left, crop to the head, scale to 1920x1080. For example, on a 4K source: `hflip,crop=2478:1394:738:170,scale=1920:1080`. Cut it into clips of 3 to 7 s around the lines you need, with a little spare at each end.
2. Make one still per chapter colour from a real frame with `gpt_image_2_5` (0.25 credits). The exact prompts are in `reference/prompts.md`.
3. Run Kling on each clip with its chapter's still as the look target. The prompt must keep every mouth, jaw and head movement from the source.

Without the still, Kling gives a cyan halo and a painted look. Without "no light on him", the clothes stay lit.

Compared in the same test:
- **Genjutsu motion transfer** (`hf_mult_motion_control`): 7 credits a second at 720p. A lovely look, but the mouth follows less clearly.
- **Seedance 2.5 `video_edit`:** 7.6 credits a second at 720p, 20 at 1080p. It left a piece of the mic in the corner and came back shorter than the source.
- **Genjutsu Styles aren't the tool:** they keep the camera and framing as filmed, and the looks are cartoon, 3D and painted.

Higgsfield can divert a generation to its "IN THE DARK" preset. Pass `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612` to get the literal prompt.

**Judge the mouth by eye.** Tile mouth close-ups of the real take above each generated clip at 8 fps. Automatic mouth measures on silhouettes gave contradictory numbers, so don't trust or quote them.

## Sound

These rules came from a first mix that nobody could hear.

- Music and effects sit under the voice for the whole video, 3.5 to 8.6 dB. Keep the voice at about -15 LUFS and the music about 5.5 LU under it.
- Check what's above 300 Hz. Laptop and phone speakers play little below that, so a bass-only sound is silent there.
- The song in the kit repeats every 58 s with a drop at 43.5 s. It's 5 minutes long. Land the drop on a line, cut the music out under the punchlines, and bring it back on the next line. For a longer video, join it to itself on a 58 s boundary. For another song, `scripts/song_drop.py <song>` finds its drop.
- Check every line against the music and the effects. Ticks can end up as loud as the voice.
- A film burn has a sound going in, total silence on the black, then a whoosh coming out.
- Final master: -14 LUFS with a limiter at 0.89.

The effects in `sfx/` are made in code by `scripts/synth_sfx.py`. To use your own sound, drop a WAV with the same name into `sfx/`. It won't be overwritten.

## Studying another reference

`scripts/study_reel.py <video> <outdir>` makes contact sheets of every unique frame, a spectrogram and the cuts and sound hits per second. To read a reel's sound properly, run `setup.sh --demucs`, then `scripts/py -m demucs -n htdemucs --two-stems=vocals -d cpu -o sep <wav>` and compare stems band by band, like for like. Only study references. Their sounds and pictures belong to their owners.

## Files

- `reference/study.md`: the full study
- `reference/prompts.md`: the exact still and Kling prompts
- `template/`: `shots.py` shot list, `gfx.py` and `comp.py` graphics, `edit.py` picture, `mix.py` sound, `storyboard.py` review page, `render_all.sh`
- `scripts/`: `setup.sh`, `demo.py`, `new_project.sh`, `transcribe.py`, `voicecut.py`, `song_drop.py`, `study_reel.py`, `synth_sfx.py`, `py`
- `music/song.m4a`, `sfx/`
