---
name: gaming-vod
description: "Gaming stream and VOD editor for Claude: mines a long Twitch / YouTube / Kick stream recording for the loudest, most chaotic moments, cuts each into a punchy 9:16 clip with facecam on top and gameplay below, word-pop captions, zooms and meme-timed sound effects, plus a 16:9 best-of. Use when the user says 'clip my stream', 'make TikToks from my VOD', 'gaming highlights', 'best moments of my stream', 'funny moments compilation', 'facecam on top gameplay below', or hands over a stream recording. Runs on video-studio-core (timeline highlights, clip candidates, reframe, captions, SFX, deliver, QC)."
license: MIT
---

# Gaming VOD

Six hours of stream in, the eight moments chat lost its mind over out, each one a vertical clip that lands the punchline.

- **Best for:** Twitch / YouTube / Kick streams, let's plays, esports scrims, reaction streams
- **Inputs:** the VOD (gameplay + facecam in one file, or separate facecam and gameplay recordings), streamer name
- **Default skin:** `chaos-stack` · alternatives `bold-bounce`, `comic-panel`, `y2k-chrome` (add `--no-matte`)
- **Formats:** 9:16 clips (facecam top, gameplay bottom), 16:9 best-of
- **Durations:** clips 20-60 s, best-of 5-10 min
- **Genre preset:** `--genre gaming-vod` (`python CORE/scripts/editor.py genre gaming-vod`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: channel name / handle, games played, moments they remember (timestamps), words to avoid (slurs from chat,
  doxxing info), and whether copyrighted music played on stream (mute or cut those parts).
- **Limits of the engine:** there is no chat-log or kill-feed input. Peaks come from audio loudness + on-screen motion
  (`timeline.py --mode highlights`) and from the transcript (`clip_candidates.py`). If the user has a chat log or
  stream markers, read the timestamps and add those moments to the spec by hand.
- Hide personal info visible on screen (Discord names, addresses, emails): cover it with a `shape` or crop it out.

## How a pro cuts this

**Clip structure (% of a 30-45 s clip)**

| beat | % | what goes here |
| --- | --- | --- |
| peak moment | 10 | the funniest frame / scream / clutch first, or a 1 s flash-forward of it |
| setup | 20 | just enough context: what is about to go wrong |
| the play | 50 | the action, cut tight, zooms on the key frame |
| reaction | 15 | the streamer's face and words: this is the payoff, let it breathe |
| CTA | 5 | handle / "full stream on YouTube", or loop back to the start |

**Pacing.** ASL 1-3 s, a visual change every 2 s; remove dead time (menus, loading, walking) completely. Comedic timing
beats rhythm: keep the half-second pause before the punchline.

**Cut rules.** Jump cuts are native here. Never cut off the reaction early; never put an SFX on top of the streamer's
own punchline. One zoom punch on the key frame (1.15-1.3x), alternate sizes.

**Transition grammar.** Hard cuts, zoom punches, flash on the impact, a whip between clips in a compilation. Glitch only
for a fail moment.

**Music and sound.** Game audio + voice, ducked music bed only where it was quiet (bed ~-22 dB). Meme SFX are high
density (up to ~20/min): `record-scratch`, `boing`, `tape-stop`, `impact`, `bass-drop`, but each motivated by a moment.

**Colour.** `gaming-vivid` or `punchy`, light (0.5-0.6) so the game UI keeps its colours.

**Captions.** Word-pop, 1-3 words, uppercase: `"preset": "beast"` or `"hormozi"`, keywords in accent, emoji on key words.

**What the client judges.** Comedic timing, the reaction landing, readable gameplay in the vertical crop.

**Common mistakes.** Too much setup; reaction cut off; gameplay squashed so small it is unreadable; SFX over the joke;
copyrighted stream music left in; captions over the facecam.

## Make the edit

```bash
# 1. candidates from loudness + motion peaks (run timeline.py directly: run.py does not forward --model to it)
python CORE/scripts/timeline.py auto vod.mp4 --work gv --mode highlights --duration 300 --format 16:9 --model base --dry-run
# 2. candidates from what was said (hooks, punchlines)
python CORE/scripts/prep.py vod.mp4 --work gvt
python CORE/scripts/transcribe.py --work gvt --model base
python CORE/scripts/clip_candidates.py --work gvt --min 20 --max 45 --top 15
```

Read `gv/timeline_spec.json` (each candidate is a ~3 s window around a peak) and `gvt/candidates.json`. Pick the real
moments, then for each clip make a work folder with the moment trimmed (`--start/--end` in source seconds, padded for
setup and reaction):

```bash
python CORE/scripts/prep.py vod.mp4 --work raw03 --start 4512.0 --end 4549.5
python CORE/scripts/run.py raw03/source.mp4 --style SKILLS/chaos-stack --genre gaming-vod --format 9:16 --retakes --model base --work clip03 --stop-after plan
python CORE/scripts/render.py clip03/plan.json --frames 1,5,10,18,25
python CORE/scripts/render.py clip03/plan.json
python CORE/scripts/finish.py clip03/plan.json --platform tiktok
```

The 9:16 plan centre-crops the 16:9 stream; for the usual facecam-over-gameplay layout build it with the `split`
element (below). Two people on camera instead: `track.py reframe raw03/source.mp4 --out raw03/stack.mp4 --format 9:16 --layout stack2`
stacks the two **faces** and you run on `stack.mp4`; it does not know where a facecam box or the game is.
Best-of 16:9: keep the chosen windows in `gv/timeline_spec.json` and
`run.py - --timeline gv/timeline_spec.json --style SKILLS/chaos-stack --genre gaming-vod --format 16:9 --model base --work gvb --stop-after plan`.

## Refine the plan

- **Facecam top, gameplay bottom (9:16):** crop the two regions from `clip03/cut.mp4` (already on the cut timeline, so they stay in sync) with FFmpeg `crop=w:h:x:y`
  into `face.mp4` and `game.mp4`, register them as plan clips
  `"clips": [{"id": "face", "src": "face.mp4"}, {"id": "game", "src": "game.mp4"}]` (pane `clip` is a clip **id**), then
  `{"type": "split", "layout": "v", "panes": [{"clip": "face"}, {"clip": "game"}], "start": 0, "end": 30, "x": 540, "y": 960, "w": 1080, "h": 1920}`
  and `"speaker": {"mode": "none"}`. Check on the contact sheet that the panes fill the frame; adjust `w`/`h`.
  Keep the game audio: the run's source (`cut.mp4`) still carries the sound even with the speaker hidden.
- **Captions:** `{"type": "captions", "preset": "beast", "keywords": ["clutch", "no way"], "emoji": {"dead": "💀"}, "dodge": [{"start": 0, "end": 30, "y": 0.5}]}`
  so words sit on the seam, not over the facecam or the game HUD.
- **Zoom punch:** `"speaker": {"zooms": [{"start": 12.3, "end": 13.4, "scale": 1.25}]}` (full-frame layout), or `keys`
  on the gameplay `clip` element: `{"s": [[0, 1], [0.15, 1.25, "expoOut"], [1.0, 1.0]]}`.
- **SFX:** `[{"t": 12.3, "kind": "impact", "gain": 0.5}, {"t": 18.9, "kind": "record-scratch", "gain": 0.45}]`.
- **Flash on the hit:** `{"type": "flash", "times": [12.3], "opacity": 0.5, "dur": 0.12}` (photosensitivity: max 2-3).
- **Music:** `"music": {"src": "bed.wav", "under": 22, "duck": "speech-aware"}`; none if the game audio is the joke.
- **Colour:** `"color": {"look": "gaming-vivid", "intensity": 0.5}`.
- **Hook text:** a `headline` "HE DIDN'T SEE IT COMING" for the first 2 s (<= 7 words).
- `python CORE/scripts/editor.py review clip03/plan.json --genre gaming-vod --fix`.

## Deliver

```bash
python CORE/scripts/deliver.py clip03/plan.json --to tiktok,shorts,reels --out-dir clip03/deliver --burn no
python CORE/scripts/deliver.py gvb/plan.json --to youtube --out-dir gvb/deliver
python CORE/scripts/qc.py clip03/deliver/final_tiktok.mp4 --plan clip03/plan.json --platform tiktok --strict
```

The plan already burns creator captions, so `--burn no` avoids a second caption layer. Name clips
`handle_vod2026-11-14_clip03_v001_9x16.mp4`.

## Check before delivering

- Contact sheet: facecam and gameplay both readable, captions not over the face or the HUD, nothing in the bottom 25%
  (TikTok UI) or the right 14%.
- The reaction is complete; the punchline is not covered by an SFX.
- No copyrighted stream music, no visible personal info, no slurs from chat on screen.
- `qc.py`: loudness -14 LUFS, photosensitivity (game flashes + `flash` elements) passes or is flagged to the user.
- Tell the user which timestamps each clip came from and which peak-detector candidates were rejected.

## Example requests

- "Here's my 5-hour stream, make me 8 TikToks of the best moments."
- "Facecam on top, gameplay at the bottom, big captions, meme sounds."
- "10-minute best-of for YouTube from last week's streams."
