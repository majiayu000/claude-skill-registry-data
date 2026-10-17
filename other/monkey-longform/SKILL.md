---
name: monkey-longform
description: Edit a raw Monkey App / video-chat recording into a retention-paced 16:9 long-form compilation (Jammer / Jay Throck style) with SFX, memes, captions and music. Use when the user wants a long-form video made from raw call footage.
---

# Monkey App long-form edit

Details and layout constants: `long-form-video-editing/monkey-app-longform-01/claude.md`. For a new video,
copy that folder's scripts and assets (`*.py`, `sfx/ music/ memes/ emoji/ fonts/`) into
`long-form-video-editing/<new-name>/`, not `raw/ work/ out/`.

## Steps
1. **Source:** Drive files over ~100 MB are too big for the Drive connector. Use `gdown <FILE_ID> -O raw/raw.mkv`
   (no `--fuzzy` in the installed gdown). Check `ffprobe` and grab one frame to confirm the crop still matches.
2. **Privacy scan:** `python scan_chat.py` finds chat bubbles (typed Instagram handles, numbers) and writes
   `work/chat_blur.json`. `render.py` blurs every piece overlapping one, and the name badge is always blurred.
3. **Transcribe + tag speakers:** extract `work/audio16k.wav` (mono 16k), `python transcribe.py` (~0.5x realtime
   on CPU, so 60 min takes ~30 min, run in background), then `python diarize.py`.
4. **Map the e-dates** from `work/transcript.txt`. Skip calls with kids, and cut any phone number, handle or
   address said out loud. Rank beats: flirt first, small talk cut (user preference).
5. **Write `build_edit.py`:** highlight teaser (max 3 clips, about 10 s: the strongest beats building to the payoff, `teaser=True`, then a title freeze) -> one section per girl, each
   about 1.5-2 min. Split the strongest call into part 1 / part 2 with an open loop ("we're coming back to
   her 👀"), finale = best payoff. Use `python words.py a b ...` for exact word times. Rizz SFX only on the
   creator's lines. **Every beat keeps its setup line** (the question or remark it answers). Read the caption
   flow clip by clip and add the setup wherever a line would land out of nowhere. Look for running gags (same line used on two girls) and cut them back to back.
6. **`python build_edit.py`, then `python retranscribe.py`** (medium.en on kept ranges only, ~12 min).
   Re-run `build_edit.py` (cut snapping uses the new word times) and print captions per clip to review.
   Where medium is wrong, set `cap_src="small"` on that clip or add `caption_fixes`. If neither model is
   sure, `nocap=True`. Never guess her words.
7. **Render:** `python render.py` (pieces cached in `work/pieces/`, only changed pieces re-render; the full
   first run takes ~25 min). Then `python qa/run_checks.py --level full out/<name>.mp4` and fix until clean.
8. **Open the render automatically** (user preference). Write `package.md` (title, thumbnail text, pinned
   comment) and send it through the `critic` agent. The `title-overclaim` gate checks it.

On-screen wording: they're **e-dates** ("E-DATE #1"), never calls. No "I only flirt" text anywhere.

## Brand look (Sparked: cool, smooth, mature; user feedback on v2)
- **SFX:** subtle pools only (soft shimmers `rizz`, low `impact`, soft `whoosh`, `tension`; heartbeats retired as too loud). Every file is
  peak-normalized to -24 dBFS (`norm_sfx`), one sound per moment, at least 4 s apart. No crowd, trombone, boing,
  whistle or arcade sounds (`CAT_REMAP` retires them).
- **Reactions = Jameer-style full-screen cutaways** (reference: Jameer `youtube.com/watch?v=l5k1civJmDo` and the
  user's own edit). The call pauses, a 1-4 s meme clip plays full-screen with its own audio line, then back.
  About one every 15-20 s (user preference), picked to match the line (see `CUTAWAYS` in `build_edit.py`). A TV color-bar glitch
  (with generated static) opens every new call. Library: `memeclips/*.mkv` + `library.json` (what each clip says),
  cut from the user's own published edit. Swears in clips are auto-bleeped (`cut_mutes`), and audio is peak-matched
  (`cut_gain`). Add new clips the same way: extract with `-c:a pcm_s16le`, check for burned-in captions.
- **Text:** Montserrat ExtraBold, white or soft gold, fades only, no bounce or rotation. Few pops, adult voice
  ("SHE CALLED ME BABY", "SAME LINE. DIFFERENT GIRL."), no slang pops ("EMOTIONAL DAMAGE").
- **Voice balance:** the creator's mic records ~5 dB quieter than the women. `creator_boost` measures the gap
  (diarized ME vs HER segments) and lifts only his speaking stretches in the final pass (printed each render).
- **Music:** auto-calibrated 22 dB under the creator's voice (`music_gain_db`, printed each render), then ducked.
  The raw mic is quiet (about -28 dBFS), so fixed music volumes come out too loud.
- **Zooms:** eased push-ins (zoompan, about 0.4 s) at 1.35-1.45x.

## Gotchas (keep updated)
- **Mix audio in its own pass** (`work/final_audio.wav`), then attach it to the video run. Mixing a separate
  voice WAV inside the heavy video/subtitle graph made ffmpeg drop ~18 s of audio: v7/v8 went out of sync in
  places, while the container still reported full length.
- **Cutaways are loudness-normalized to -27 LUFS** (`cut_gain`), not peak-normalized. Raw meme clips range
  from -7 to -34 LUFS, and peak matching left the Law & Order and El Risitas clips as loudness spikes.
- **Run QA after the file settles.** The gate used to cache "still writing, skip" as a pass. Fixed in
  `qa/checks.py`, but if a render "passes" instantly, re-run the check.
- **Pieces must be frame-exact** (video `-frames:v n`, audio `atrim=end_sample`). Otherwise each piece's video
  rounds up a frame, concat leaves audio gaps, and the audio drifts (v2 was 0.75 s off by the end).
- **QA `loudness spike` gate** (momentary > integrated + 8 LU) is how "SFX too loud" gets caught automatically.
- **AAC pieces + concat -c copy = A/V drift** (each piece keeps ~21 ms of encoder priming; v1 drifted about
  3.5 s by the end). Pieces are now PCM `.mkv`, and AAC is encoded once in the final pass. The QA gate checks
  sample count vs video length.
- **ffmpeg filters lock frame size on the first frame**, so animated `scale` overlays shrink. Pop-in overlays
  are pre-rendered by PIL as fixed-canvas PNG sequences (`overlay_seq`).
- **libass can't draw color emoji.** `render.py` strips emoji from text pops and places Twemoji PNGs beside them;
  add new emoji to `EMOJI_FILES`.
- **The end card needs sound.** Music swells to 0.35 under the final freeze (there's no speech to duck under).
- **Don't overwrite a render the user has open** (Windows file lock). Bump `name` in `build_edit.py` per version.
- **Seeking with `-ss` before `-i` on the MP4 when measuring levels gave false silence.** Measure on a full decode.
- **Whisper word end-times run long.** Captions include a word if it *starts* inside the clip.
