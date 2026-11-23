---
name: short-film-finisher
description: "Finishing editor for a locked short film or narrative piece: per-shot colour correction and shot matching, a creative look on the footage only, film texture, dialogue / music / effects mix to the delivery loudness, room tone, titles and credits, then masters - ProRes 422 HQ, H.264 web, audio stems, M&E, textless, subtitles - and QC. Use when the user says: finish my short film, colour and mix my film, festival master, make a ProRes master, deliver stems and M&E, final export for my short, grade and sound my locked cut. Picture must be locked first. Default skin minimal-mono (titles only)."
license: MIT
---

# Short Film Finisher

Picture is locked; now it has to look and sound finished, and ship in every format a festival or distributor asks for.

- **Best for:** short films, narrative branded films, music-video narratives, student films after lock
- **Inputs:** the locked cut (a single file, or a `scene-editor` / timeline work folder), the music and SFX files, credits text, the delivery spec (festival / platform)
- **Default skin:** `minimal-mono` · alternatives `cinematic-phone`, `essay-mode`, `paper-cut` (only for title/credit styling)
- **Formats:** ProRes 422 HQ master, H.264 web master, stems (dialogue / music+effects mix), textless, `subtitles.srt`, EDL/FCPXML/OTIO
- **Duration target:** as locked (2-40 min); genre preset `short-film-finisher`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre short-film-finisher`.
- **Confirm picture lock** with the user. Any timing change after this means redoing colour, mix and subtitles.
- Get the delivery spec: festival (often ProRes 422 HQ + stereo mix + SRT), platform (H.264 -14 LUFS), broadcast (-23/-24). Always run with `--no-cut` (the cut is already final).
- Know the camera: log footage needs `color.log` (approximate) or, better, the official camera LUT in `color.lut`.

## How a pro cuts this (finishing order)

| stage | what happens |
| --- | --- |
| 1. conform + lock | one locked file or spec; nothing moves after this |
| 2. technical correction | levels, white balance, exposure per shot; log -> Rec.709 |
| 3. shot matching | every shot in a scene matched to a hero frame |
| 4. look | one creative look on the footage (titles stay clean) |
| 5. texture | grain, halation, gentle vignette, letterbox |
| 6. sound | dialogue edit + chain, room tone, effects, music, mix to target |
| 7. titles + credits | opening title, end credits, spelling checked |
| 8. masters + QC | ProRes, web, stems, textless, subs, QC report |

- **Colour rules:** correct before look; skin on the skin line; don't brighten deep skin; one look per film (a different look only for a motivated section like a flashback). Check scopes, not just the monitor.
- **Looks:** `kodak-2383` 0.7-0.85 (classic print), `fuji-eterna` (muted drama), `bleach-bypass` (grit), `cinestill-800t` + halation (night), `teal-orange-pro` (commercial).
- **Sound rules:** dialogue first and always intelligible; room tone under every cut; ambience continuous across picture cuts within a scene; music supports, never fights the lines; silence before the big moment.
- **Loudness:** web -14 LUFS / -1 dBTP; festival/cinema ~ -27 LUFS dialogue-led (approximate: no LUFS spec, rooms are calibrated); broadcast EBU -23 / ATSC -24.
- **Client judges:** looks and sounds finished, spec met, every deliverable present, no QC failures.
- **Common mistakes:** grading before lock, a look that turns skin green, legal-level violations, music masking dialogue, missing textless/M&E, typos in the credits.

## Make the edit

From a locked single file:

```bash
python CORE/scripts/run.py locked_cut.mp4 --style SKILLS/minimal-mono --genre short-film-finisher --no-cut --no-matte --format 16:9 \
  --model small --work fin --stop-after plan
```

From a `scene-editor` spec: `run.py - --timeline scene.json --style SKILLS/minimal-mono --genre short-film-finisher --no-cut --format 16:9 --work fin --stop-after plan`.

Pick the look on the real footage, check scopes, then render:

```bash
python CORE/scripts/color.py looks-sheet fin/source.mp4 --t 12 --out fin/looks.png --correct     # LOOK and choose
python CORE/scripts/color.py scopes fin/source.mp4 --t 12 --out fin/scopes.png
python CORE/scripts/render.py fin/plan.json --frames 5,40,90,150
python CORE/scripts/render.py fin/plan.json
python CORE/scripts/finish.py fin/plan.json --platform youtube
python CORE/scripts/color.py qc fin/final.mp4            # legal levels
```

Stems: make the dialogue-only and the music+effects mixes by rendering the plan twice with parts removed (see below), or split an existing mix with `python CORE/scripts/stems.py fin/final.mp4 --out fin/stems` (Demucs approximation, needs `pip install demucs`; not a true M&E).

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Graphics:** `"elements": []` except the title (`titlecard`) and credits (a `titlecard` or `text` per card, or a single `ticker` for a crawl), held long enough to read twice.
- **Colour:** `"color": {"auto": true, "wb_strength": 0.7, "lut": "C:/luts/official_camera_to_709.cube", "match": "hero_frame.png", "match_strength": 0.8, "look": "kodak-2383", "intensity": 0.8, "halation": 0.2}`. Per-clip balance in a timeline: the clip `color` field (`{"brightness": 0.02, "contrast": 1.04, "saturation": 0.95}`).
- **Texture:** `"finish": {"grain": {"strength": 8, "luma_weighted": true}, "halation": 0.3, "vignette": 0.3, "letterbox": 2.39, "legal": "strict"}`.
- **Dialogue:** `"audio": {"voice": {"denoise": "light", "declick": true, "eq": "warm", "deess": true}, "platform": "youtube"}, "roomTone": true`.
- **Effects:** `"sfx": [{"t": 41.2, "file": "door_slam.wav", "gain": 0.6}]` (your own recorded or licensed files; the procedural kinds are for stingers, not foley).
- **Score:** `"music": {"src": "score_v3.wav", "volume": 0.8, "duck": "speech-aware", "duckDepth": 6}`; for a pre-mixed score set `"duck": false`.
- **Dialogue stem:** copy the plan, remove `music` and `sfx`, `"outputFile": "stem_dialogue.mp4"`. **M+E stem:** copy, `"audio": {"voice": false}` does not remove dialogue - the engine cannot mute the production track, so a true M&E needs the music and effects mixed without the source audio outside this tool (or the Demucs approximation above).
- **Textless:** copy the plan, remove title/credit elements, `"outputFile": "textless.mp4"`.

## Deliver

```bash
python CORE/scripts/deliver.py fin/plan.json --to prores-422hq,youtube,audio-wav --out-dir fin/deliver
python CORE/scripts/deliver.py fin/textless.mp4 --to prores-422hq --out-dir fin/deliver_textless --no-post --no-thumbs
python CORE/scripts/qc.py fin/deliver/final_youtube.mp4 --plan fin/plan.json --platform youtube --strict
python CORE/scripts/export_edl.py fin --out-dir fin/handoff --title "FILM_TITLE"
```

- `captions.srt` from deliver.py is the subtitle file; check every line against the script and the final mix.
- ProRes keeps the mix untouched (24-bit PCM). For a cinema/festival room ask the festival's loudness spec; the cinema target in `audio.md` is an approximation.
- Name masters `TITLE_2026_ProRes422HQ_1920x1080_2398_stereo.mov` style (frame rate is the plan's fps, 30 by default after prep).

## Check before delivering

- Watch the whole master once, top to tail, with headphones and on a phone.
- `color.py qc` legal; scopes show sane blacks/whites; skin consistent across shots of a scene.
- Dialogue intelligible everywhere; no clicks at edits; room tone continuous; loudness on target.
- Credits and title spelled right (names triple-checked); textless and stems line up with the master frame-for-frame.
- Tell the user: look used, loudness measured, every file with its spec, known limits (M&E approximation).

## Example requests

- "My short is locked - grade it like a Kodak print, mix it and give me a ProRes festival master."
- "Finish this film: match the shots, add grain and 2.39 bars, credits at the end, stems for the sound guy."
- "Make the web version at -14 LUFS and a textless ProRes."
