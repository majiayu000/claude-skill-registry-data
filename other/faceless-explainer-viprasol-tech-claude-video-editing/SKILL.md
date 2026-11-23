---
name: faceless-explainer
description: "Faceless-channel editor: turns a script (or a recorded voice-over) into a finished explainer with no presenter on camera - offline TTS voice-over (Kokoro / Windows SAPI / say), one visual per sentence (B-roll, photos, charts, maps, kinetic type), heavy word-synced captions and a consistent channel template, in 16:9 and 9:16. Use when the user says: faceless video, make a video from this script, explainer with voice-over, AI voice video, top-10 / facts / history channel, narrate these images, turn my article into a video. Default skin essay-mode; any Video Studio skin works."
license: MIT
---

# Faceless Explainer

Script in, explainer out: a natural voice-over, a new visual every sentence, captions that carry muted viewers.

- **Best for:** explainers, top-N lists, history/facts, finance or tech breakdowns, article-to-video
- **Inputs:** a script (`script.txt`) or a recorded VO (`voice.wav`), a folder of visuals (clips/photos named after what they show), optional music
- **Default skin:** `essay-mode` · alternatives `data-story`, `swiss-poster` (use `--no-matte`), `countdown-list` (9:16 lists)
- **Formats:** 16:9 1920x1080 master + 9:16 cutdown; `captions.srt`, chapters for long ones
- **Duration target:** 60 s - 15 min; Shorts 30-60 s; genre preset `faceless-explainer`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Best free voice: `pip install kokoro soundfile`; without it `tts.py` falls back to Windows SAPI / macOS `say` / espeak-ng. List voices: `python CORE/scripts/tts.py --list-voices`.
- Preset: `python CORE/scripts/editor.py genre faceless-explainer`.
- **Platform note:** YouTube demonetises mass-produced, repetitive content. Every video needs a real script, real research and varied visuals; disclose AI voices where the platform asks. Use only footage, photos and music you have rights to.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| hook | 0-5 | the most surprising fact or question, on screen as text, by 2 s |
| promise | 5-10 | what the viewer will know by the end |
| points / chapters | 10-85 | one visual per sentence; a chapter card between sections |
| payoff | 85-95 | the answer, the twist, the number |
| CTA / next | 95-100 | one line + end screen space |

- **Script first:** short sentences (8-16 words), one claim each, numbers written as digits. Read it aloud before generating.
- **Pacing:** a new visual every 2-4 s (one per sentence, two for long ones); text changes every 1.5-3 s in Shorts. Leave 0.3-0.5 s of air between sections (pauses in the script via line breaks).
- **Visual rules:** the visual matches the *words being said* (literal for nouns, metaphor for ideas). Numbers become `counter`/`bars`/`linechart`, places become `map`, lists become `steps`/`checklist`. Never the same stock clip twice.
- **Transitions:** cuts on sentence ends; one soft transition kind (`fade` 0.3 s) between chapters only.
- **Music/SFX:** a bed 20-24 LU under the VO, ducked ("speech-aware"); whoosh on chapter cards, ticks on counters; sparse.
- **Colour:** unify mixed stock with one look: `documentary-natural` 0.5, or `finance-navy` / `cool-corporate` for money/tech.
- **Captions:** preset `boxed` or `clean` (16:9), `hormozi` (9:16); <= 20 cps; key words in accent.
- **Client judges:** audio that doesn't sound robotic, cut density, accuracy, a recognisable template.
- **Common mistakes:** monotone TTS at default speed, visuals unrelated to the words, a 20 s logo intro, wall-to-wall text, music louder than the voice, the same stock clip reused.

## Make the edit

1. Voice-over (skip if the user recorded `voice.wav`; then transcribe it in step 3):

```bash
python CORE/scripts/tts.py --script script.txt --out vo/voice.wav --words --model base --rate 1.05
#  -> vo/voice.wav + vo/words.json (word times, script spelling). Keep it OUT of the work folder fx/.
```

2. Read `vo/words.json` and write a timeline spec `fx/spec.json`: one visual per sentence, its `dur` (images) or `in`/`out` (clips) equal to that sentence's length, the voice as the spec `music` at full level so it becomes the soundtrack (paths are relative to the spec file):

```json
{"format": "16:9", "fps": 30,
 "clips": [{"src": "../visuals/ocean-waves.mp4", "in": 2, "out": 6.1, "audio": "mute"},
           {"src": "../visuals/old-map.jpg", "dur": 3.4},
           {"src": "../visuals/ship-deck.jpg", "dur": 4.0, "transition": {"type": "fade", "dur": 0.3}}],
 "music": {"src": "../vo/voice.wav", "volume": 1.0, "duck": false, "fadeOut": 0.2, "voiceover": true}}
```

Clip durations must add up to the voice length (`words.json` `duration`) **plus** every transition `dur` (a transition overlaps two clips). Images get a slow centre push-in automatically.

3. Assemble and plan. `"voiceover": true` in the spec's `music` block makes `timeline.py` transcribe the voice, so `words.json` gets word times for the captions (a plain music bed is never transcribed):

```bash
python CORE/scripts/run.py - --timeline fx/spec.json --style SKILLS/essay-mode --genre faceless-explainer \
  --model base --work fx --stop-after plan
#   fallback (no "voiceover" flag, or to keep the exact TTS spelling): run with --stop-after timeline, then
#   cp vo/words.json fx/words.json   (TTS words already sit on the timeline clock: the voice starts at 0)
#   python CORE/scripts/make_plan.py --work fx --style SKILLS/essay-mode --genre faceless-explainer
python CORE/scripts/editor.py review fx/plan.json --genre faceless-explainer --fix
python CORE/scripts/render.py fx/plan.json --frames 1,5,10,20
python CORE/scripts/render.py fx/plan.json
python CORE/scripts/finish.py fx/plan.json --platform youtube
```

Quick version (one background, B-roll placed by keyword): mux a still with the voice (`ffmpeg -loop 1 -i bg.jpg -i voice.wav -r 30 -pix_fmt yuv420p -c:v libx264 -c:a aac -shortest base.mp4`), then `run.py base.mp4 --style SKILLS/essay-mode --genre faceless-explainer --no-cut --broll visuals/ --work fx2 --stop-after plan`. Name visual files after the words they illustrate or `broll.py` will not match them.

## Refine the plan

- **Title card:** the skin's auto `titlecard` takes the first words of the VO and can cut mid-phrase; rewrite its `title` to the hook (<= 7 words).
- **Words:** fix any mis-heard word in `plan.words` to the script spelling (keep times).
- **Hook:** a `headline` 0-2.5 s with the hook question; `"sfx": [{"t": 0, "kind": "impact", "gain": 0.4}]`.
- **Chapter cards:** `{"type": "titlecard", "kicker": "Part 2", "title": "The Wreck", "start": 41.0, "end": 43.0, "in": "maskUp"}` plus a top-level `"chapters": [{"start": 0, "title": "Intro"}, {"start": 41.0, "title": "The Wreck"}]` list in the plan for delivery.
- **Data:** `counter`, `bars`, `linechart`, `donut`, `barrace` timed 0.1 s before the number is spoken; `map` with `pins` for places (seeded dot map, not real geography - say so if accuracy matters).
- **Lists:** `steps` or `checklist` with `items[].at` = spoken time.
- **Captions:** `{"type": "captions", "preset": "boxed", "keywords": ["1912", "iceberg"]}`.
- **Voice polish:** `"audio": {"voice": {"denoise": false, "eq": "broadcast", "deess": true}}` (TTS is clean; don't denoise).
- **Music:** `"music": {"src": "bed.mp3", "under": 22, "duck": "speech-aware", "fitTo": "beats", "endButton": true}`.
- **Look:** `"color": {"look": "documentary-natural", "intensity": 0.5}`, `"finish": {"grain": 5, "vignette": 0.3}`.

## Deliver

```bash
python CORE/scripts/deliver.py fx/plan.json --to youtube,shorts --out-dir fx/deliver
python CORE/scripts/qc.py fx/deliver/final_youtube.mp4 --plan fx/plan.json --platform youtube
```

- YouTube: upload `captions.srt` as a sidecar; paste `chapters.txt` into the description (needs >= 3 chapters of >= 10 s).
- The 9:16 from a 16:9 plan is a blurred pillarbox. For a real vertical, re-run step 3 with `"format": "9:16"` in the spec, `--format 9:16` and `countdown-list` or `bold-bounce`.
- Thumbnails: `thumb_*.png`; check the headline is the actual hook.

## Check before delivering

- Every sentence has a matching visual; no repeats; no visual left on screen > 6 s without motion.
- VO natural (rate, pronunciation of names); captions match the script; numbers and dates verified.
- Music never masks the VO; `qc.py` -14 LUFS / -1 dBTP; no black frames between clips.
- Rights: every clip, photo and track is licensed or the user's own; credits in the description if required (CC BY).
- Tell the user: the voice used, video length, chapter list, file paths.

## Example requests

- "Turn this script into a faceless YouTube video with an AI voice and stock footage."
- "Make a 60-second faceless Short from these 6 facts, big captions."
- "Narrate my blog post over these photos, add a chart for the numbers."
