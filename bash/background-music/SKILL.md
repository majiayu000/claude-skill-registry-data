---
name: background-music
description: "Lays a background music bed UNDER the voice on a near-final cut — a FLAT constant bed by default (no ducking, no fade-in, −18 dB, short tail fade-out only). Ducking + fade-in are opt-in. OPTIONAL, format-agnostic (any short or long video). Runs after captions, before final render. Triggers: add background music, add a music bed, lay music under, BGM, add a soundtrack, put music behind this."
---

> **Video Studio:** this skill lives in `engines/legacy-editor`. Before running anything from it, `cd engines/legacy-editor` and use that folder's copy (`engines/legacy-editor/.claude/skills/background-music/`), which has its scripts and reference files. Every path below is relative to `engines/legacy-editor`. This copy only lets Claude find the skill from the Video Studio folder.


# Background Music — Flat Bed Under the Voice

Optional step **6**. Takes a near-final cut and lays a music bed under the voice.

**The default is a FLAT bed:** the music sits at **one constant level for the whole video** — no sidechain ducking, no fade-in — with only a short tail fade-out at the end. The voice arrives peak-limited at −6 dBFS (≈ −21 dB mean) from the static rough-cut chain, so a quiet fixed bed (−18 dB) rides cleanly under it. A peak limiter guards the sum; there is **no loudnorm** on the flat path (single-pass loudnorm on a finished mix pumps and re-introduces the very level variation we're avoiding).

> **Why flat is the house default:** ducking (music dipping under the voice and swelling back up in the gaps) made past mixes get audibly *louder and quieter in parts*. A flat bed has a measured loudness range of **0.0 LU** — it does not move. That's the default. Ducking and fade-in are **opt-in only.**

Most useful on **short-form explainers**, but works on any format. It's opt-in — skip it unless asked.

## When to run
After **Captions (5)**, before **Final render (7)**. Long-form skips captions, so for long-form it runs right after the graphics/second-pass cut. Always operate on the **latest rendered cut**, never on raw.

## Where the music comes from
Drop a track into `projects/<job>/audio/`. Two ways to get one:
1. **Your own / licensed track** — drop an `.mp3`/`.wav`/`.m4a` into `audio/`. Use the newest file there.
2. **Generate one** (royalty-free, no copyright strikes — on brand) via the vendored `media-use` skill: `node .claude/skills/media-use/scripts/resolve.mjs --type bgm --intent "<mood>" --project projects/<job>` (run its sign-in Preflight first per `media-use/audio/references/bgm.md`; there is NO `npx hyperframes bgm` command). Prompt the mood to match the reel, write the result into `audio/`.

If `audio/` is empty and no track is pointed at, ask one line: *"Drop a music track in `audio/` or want me to generate one — what vibe?"*

## Run it
```bash
.claude/skills/background-music/scripts/mix-music.sh \
  <near-final-video.mp4> \
  projects/<job>/audio/<track>.mp3 \
  projects/<job>/outputs/<job>-music.mp4 \
  [bed_db] [duck] [fadein]
```
- Output is non-destructive — `<job>-music.mp4`, never clobbering the no-music cut. That music-mixed file is what **Final render (7)** exports as the deliverable.
- `bed_db` — music gain. **Default −18 (quiet, clearly background).** More negative = quieter: `-24` ≈ barely-there, `-16` ≈ noticeable, `-12` ≈ prominent. Stay negative — this is a bed, not a duet. Balance is taste; re-run with a different `bed_db` to tune.
- `duck` — **`off` (default) = FLAT constant bed, no ducking.** `on` = opt-in sidechain auto-duck (music dips under voice, swells in the gaps) **and** re-normalizes the whole mix to −14 LUFS. Only turn it on when you specifically want the bed to breathe with the talking.
- `fadein` — music fade-in seconds at the start. **Default `0` = no fade-in (the bed is just there).** Pass e.g. `2` for a 2-second fade-in. Opt-in.

**Default (flat) is just three args past the output** — no flags needed:
```bash
mix-music.sh cut.mp4 audio/track.mp3 out-music.mp4
```

## Tuning notes
- The script loops the track to cover the full video and fades the tail out over the last ~1.2s (always on — a clean ending, not a level move).
- Voice intelligibility is the priority. If the bed feels too present, drop `bed_db` further (e.g. −22). If it's buried and you want it more felt, raise toward −16. Keep it flat — don't reach for ducking just to make it louder; lower the bed or raise it as a whole.
- **Don't default to ducking.** It's there for the rare case you want the bed to swell in the gaps. The flat bed is the house sound.
- Verify after: play it, or `ffprobe`/`ebur128` the output. On the flat path the bed sits at a constant level (the mix's loudness range tracks the *voice*, not the music); on the duck path the mix is re-normalized to −14 LUFS.
