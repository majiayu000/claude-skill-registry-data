---
name: editor-handoff
description: "Editor hand-off for Claude: packages a Video Studio edit so another editor can finish it in Premiere, DaVinci Resolve, Final Cut or Avid: CMX3600 EDL, FCPXML 1.10 and OpenTimelineIO timelines with markers, the graphics layer as ProRes 4444 with alpha, a ProRes or DNxHR picture reference, the mix as WAV, captions as SRT, and a README that explains it all. Use when the user says 'send this to my editor', 'export an EDL', 'XML for Premiere', 'FCPXML', 'OTIO', 'turnover to Resolve', 'give me the graphics with transparency', 'finish it in DaVinci', 'conform this'. Runs on video-studio-core (export_edl, render --keep, deliver, qc)."
license: MIT
---

# Editor Handoff

A turnover a stranger can open at 2 a.m. and understand: timeline, media, graphics with alpha, mix, captions, notes.

- **Best for:** finishing in an NLE, colourist or mixer turnovers, agency hand-offs, archiving an edit
- **Inputs:** a Video Studio work folder `W` (after `run.py`/`autocut.py`, ideally rendered), the receiving NLE
- **Outputs:** `W/handoff/` with EDL, FCPXML, OTIO, `front_4444.mov`, `source.mp4`, picture reference, mix WAV,
  `captions.srt`, `README.md`

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder.
- First run on a machine: `python CORE/scripts/check_env.py`. `opentimelineio` is optional (OTIO is written by hand
  without it).
- Ask: which NLE and version, frame rate the project must use, timecode start (default `01:00:00:00`), and whether
  they want burned graphics or separate alpha layers. Picture lock first: a hand-off of a moving edit wastes everyone's day.

## What gets handed over

| file | made by | what it is |
| --- | --- | --- |
| `<name>.edl` | `export_edl.py` | CMX3600, one video track, reel = file stem, `* FROM CLIP NAME`, `* LOC` markers |
| `<name>.fcpxml` | `export_edl.py` | FCPXML 1.10 (Final Cut; Resolve and Premiere import it), asset-clips on the spine, markers |
| `<name>.otio` | `export_edl.py` | OpenTimelineIO JSON (Resolve, Premiere via plug-in, Avid via adapters) |
| `source.mp4` | the work folder | the media the timelines point at (30 fps, upright, normalised by `prep.py`) |
| `front_4444.mov` | `render.py --keep` + `export_edl.py --encode-alpha` | captions and graphics with alpha, full length |
| `final_prores-422hq.mov` | `deliver.py` | picture reference / mezzanine with the full mix |
| `final_audio-wav.wav` | `deliver.py` | the mix, 48 kHz 24-bit, untouched loudness |
| `captions.srt/.vtt/.ttml` | `deliver.py` | subtitles from the transcript |
| `README.md` | you (Claude) | how to conform, what is where, known issues |

Limits to say out loud: the timelines carry the **cut only** (one video track from `cutlist.json`). Overlays, zooms,
colour and the mix are not editable in the NLE: they come as the alpha layer, markers and baked files. Multi-clip
timelines from `timeline.py` export the assembled cut against `source.mp4` (= the assembled video), not the original
camera files. There are no separate DX/MX/FX stems: hand over the mix WAV, and the music file and voice separately if
the mixer needs them.

## Make the hand-off

```bash
# 1. timelines (record starts at 01:00:00:00; drop-frame used for 29.97/59.94)
python CORE/scripts/export_edl.py W --plan W/plan.json --out-dir W/handoff --record-start 01:00:00:00 --title "client_project_v003"
# 2. graphics layer with alpha: render once keeping the PNG frames, then encode ProRes 4444
python CORE/scripts/render.py W/plan.json --keep
python CORE/scripts/export_edl.py --encode-alpha "W/render/front/%05d.png" --fps 30 --out W/handoff/front_4444.mov
# 3. picture reference + mix + captions
python CORE/scripts/finish.py W/plan.json
python CORE/scripts/deliver.py W/plan.json --to prores-422hq,audio-wav --out-dir W/handoff --burn no --no-thumbs --no-post
# 4. QC the reference
python CORE/scripts/qc.py W/handoff/final_prores-422hq.mov --plan W/plan.json --platform none
```

`render.py --keep` leaves one PNG folder per layer in `W/render/` (`front` always when there are overlays; `bg` and
`behind` only when the plan uses them). Encode each layer you hand over (e.g. `behind` for text behind the speaker:
`--encode-alpha "W/render/behind/%05d.png" --out W/handoff/behind_4444.mov`; it only works over the matte, so also
hand over `W/matte.mp4`). Then copy `W/source.mp4` into `W/handoff/`. `python CORE/scripts/export_edl.py --alpha`
prints the same recipe.

ProRes 4444 decodes as `yuva444p12le` in FFmpeg: that is normal. Check alpha by importing it over a colour matte.

## Write the README

Write `W/handoff/README.md` for the receiving editor (plain text, no jargon they would not use):

```text
PROJECT  client_project_v003   FPS 30 (constant)   RES 1920x1080   TC start 01:00:00:00
TIMELINE  client_project_v003.fcpxml (Final Cut / Resolve), .edl (Avid/Premiere), .otio
MEDIA     source.mp4  <- relink to this; reel name = "source"
LAYERS    V1 source (cut per timeline)  V2 front_4444.mov (graphics + captions, alpha, starts at 01:00:00:00)
AUDIO     final_audio-wav.wav = full mix (dialogue chain, music ducked, -14 LUFS when finished for web)
          the timeline audio is the raw camera sound; mute it if you lay the mix
REFERENCE final_prores-422hq.mov = how it should look and sound
CAPTIONS  captions.srt (sidecar), burned captions are inside front_4444.mov
MARKERS   text overlays and zoom punches are markers on the timeline (names = overlay text)
COLOUR    look "<name>" at <intensity> baked into the reference only; source.mp4 is ungraded
KNOWN     <anything unresolved: a name to confirm, a music licence, a shot to replace>
CONTACT   <who to ask>
```

## Check before delivering

- Import the FCPXML or EDL yourself into any free NLE if available (Resolve), or at least open the EDL as text:
  event count matches the number of segments in `W/cutlist.json`, record total equals the length of `cut.mp4`.
- `ffprobe front_4444.mov`: codec `prores` (4444 profile), pix_fmt with alpha, duration equals the plan duration.
- Reference and mix durations match the timeline to the frame; `qc.py` passes.
- README lists every file, the frame rate, timecode start and known issues. Zip or folder name carries the version
  (`client_project_v003_handoff`).

## Example requests

- "My editor wants to finish this in Premiere, give her an XML and the graphics separately."
- "Export the cut as an EDL with markers for the colourist, start at 10:00:00:00."
- "Package everything for Resolve: timeline, captions, mix, and a README."
