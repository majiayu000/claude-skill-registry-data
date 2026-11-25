---
name: narrated-video
description: Local pipeline to make, redo or patch any narrated explainer video (script as data, AI voice with OmniVoice, music with MusicGen, animated scenes in HyperFrames/SVG/GSAP, assembly with ffmpeg, sped-up version, phone copy, YouTube title/description/chapters). Use when the user asks "make a narrated video" / "faz um vídeo narrado", "explainer video about X" / "vídeo explicativo sobre X", "start a new video" / "começa um vídeo novo", "redo scene X" / "refaz a cena X", "swap the voice/audio" / "troca a voz/áudio", "reassemble the video" / "remonta o vídeo", "make the final version" / "gera a versão final", "speed it up to 1.35x" / "acelera pra 1,35x", "send it to my phone" / "manda pro celular", "YouTube description" / "descrição do youtube".
---

# Narrated video

Everything lives in the `claude-code-video-studio` repo: two folders above this skill's base directory when installed as a
plugin, `~/claude-code-video-studio` for a clone (otherwise look for the folder with `studio/assemble.py`). Below, `ST` is `<repo>/studio`.

Project = a folder with `script.py` + `scenes/<group>/build_<group>.py`. Every command runs **from inside the project folder**.
New video: `cp -r <repo>/template ~/videos/<name>` and replace the script. Full reference of a 13 min video made this way
(an English dub of a Brazilian Portuguese original): `<repo>/examples/your-mind/`.

## Steps

| Step | Command | Output |
|---|---|---|
| Script | edit `script.py` (`SCENES`, `PRONUNCIATION`, optional `LANG`, `VOICE` and `MUSIC`); `python3 script.py` counts words | |
| Voice | `$PY $ST/tts.py generate`, then `$PY $ST/tts.py pick` (separate processes, `MemoryMax=4G`) | `assets/voice/<scene>.wav`, `durations.json`, `asr-choice.tsv` |
| Time per word | `python3 $ST/transcribe.py` | `words/<scene>.json` |
| Check voice | `python3 $ST/find_stutters.py`, `python3 $ST/find_clicks.py` | list with time in the video |
| Clean voice | `python3 $ST/clean_voice.py cuts.json` (mutes stretches without changing duration) | `assets/voice_clean/` |
| Music | `$PY $ST/music.py` (MusicGen small, covers the narration) | `assets/music.mp3` |
| Scenes | `scenes/<group>/build_<group>.py` with `from engine import *`; `python3 $ST/scenes.py build <group>` | HyperFrames HTML |
| Look at frames | `$ST/snap.sh scenes/<group> <out> <t1,t2,...>` and `$ST/check.sh scenes/<group>` | PNG + contact sheet |
| Render scenes | `MEMCAP=4500M RFLAGS="--browser-gpu" python3 $ST/scenes.py render <group>` (`ONLY=id1,id2` for just some) | `assets/clips/<id>.mp4`, `map.json` |
| Assemble | `OUT=v1 VOICE=assets/voice_clean python3 $ST/assemble.py` (a segment without a clip becomes a dark screen and is listed) | `renders/v1.mp4` |
| Patch | `python3 $ST/patch.py v1 v2 <redone ids>`; audio: `VOICE=... python3 $ST/swap_audio.py v1 v2` | no full reassembly |
| Progress bar | `$ST/progress_bar.sh v2 v2-bar` | |
| Delivery | `$ST/deliver.sh v2-bar 1.35` | `-1.35x.mp4` and `-mobile.mp4` |

`PY` = a python with OmniVoice, faster-whisper and MusicGen (`transformers`). The rest runs on the system python3.
`FF` picks the ffmpeg (default: the one on PATH); `FF_GPU` an ffmpeg with NVENC, if you have one.
`LANG` in `script.py` is an ISO code (default `"en"`); set `LANG = "pt"` for pt-BR videos.

Scenes: delegate to subagents, one per group of ~10 segments, passing `$ST/AGENT.md` as the briefing (hard rules: text only from
the narration, prefixed ids, no render, only `snap.sh`). Check the frames before accepting. Rendering is the coordinator's job, one at a time.

## Delivery

Deliver ONE final version: 1.35x, 1080p. The phone copy (540p) exists to stay small for sending; say that is why it is not 1080p.

YouTube: title, description, chapters (times already in the sped-up version) and sources by topic. Template:
`examples/your-mind/film/youtube-description.md`. Cover: the `ai-cover` skill.

## Care

- Memory: voice, music, render and SDXL only with `free -h` >= 6 GB and inside
  `systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0`. Progress in taskline (the scripts already report).
- Never an em-dash in on-screen text, comments or descriptions.
- Voice and music are AI: the description says so. AI images never go inside the video, only on the cover.
- Film/trailer clips in the video: credits in a `CREDITS.md` and in the description.
