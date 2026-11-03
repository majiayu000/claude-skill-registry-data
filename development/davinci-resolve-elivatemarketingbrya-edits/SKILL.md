---
name: davinci-resolve
description: "The DaVinci Resolve finishing lane, counterpart to premiere-pro for Resolve users. Replays the rough-cut EDL (cuts.json) as separate trimmable clips on a real Resolve timeline via the davinci-resolve MCP, then keeps working through Resolve's official scripting API: silence-ripple auto cuts, AI subtitles + transcript-based cut proposals, Fusion node graphs, custom DCTL color shaders, in-app Python, vision metadata, native renders. Triggers: send to resolve, open in resolve, finish in resolve, davinci, edit this in resolve, resolve timeline."
---

> **Video Studio:** this skill lives in `engines/legacy-editor`. Before running anything from it, `cd engines/legacy-editor` and use that folder's copy (`engines/legacy-editor/.claude/skills/davinci-resolve/`), which has its scripts and reference files. Every path below is relative to `engines/legacy-editor`. This copy only lets Claude find the skill from the Video Studio folder.


# To DaVinci Resolve: Rough Cut Handoff + API Editing

The Resolve counterpart to the `premiere-pro` skill. Same job: get the cut **onto a Resolve timeline as separate, trimmable clips** by replaying the EDL (`transcript/cuts.json`) against the raw footage, then keep working there. Unlike Premiere there is **no bridge panel**: the `davinci-resolve` MCP talks to Resolve's official first-party scripting API in-process, which reaches four apps in one (Edit, Fusion, Color, Fairlight). Resolve must be RUNNING; `resolve_control launch` can start it (headless supported, but several AI features are GUI-only, noted below).

## Wiring

- MCP = `davinci-resolve` in `.mcp.json` → pinned local clone at `vendor/davinci-resolve-mcp/` ([samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp) v2.72.0, commit `a9fd831`, update checks off; bump the pin deliberately). Compound server (`src/server.py`, 34 grouped tools; `--full` = 341 granular). Venv built by `python3 install.py --clients manual`.
- Fresh machine: run `./setup-resolve.sh` (ships with the system). It clones the pin, builds the venv, and writes the `.mcp.json` entry with the three env vars (`RESOLVE_SCRIPT_API` / `RESOLVE_SCRIPT_LIB` / `PYTHONPATH`).
- Resolve side: nothing to configure in the normal case: **External scripting = Local is Resolve's shipped default** (verified on multiple installs, 2026-08-13; don't tell users to go set it). Only if the MCP can't connect after a Claude Code restart, verify Preferences → System → General → External scripting = Local as a troubleshooting step. External scripting is a Studio feature; the free edition needs the in-app bridge script instead (see `vendor/davinci-resolve-mcp` docs).
- Second server, NOT wired: `resolve-advanced/` (18 Node tools) edits `.drp`/`.drt`/`.drx` with Resolve closed. Its `.prproj` conform bridge extracted 0 editorial events from a real Premiere project, so don't rely on it.

## EDL replay: one call

Run the splice `RENDER=0` first (same rule as the Premiere path: never render the flat cut for an app finish). Then the whole rebuild is a single call:

1. **Create the project from a matching template (see "Project setup" below). Never `create_project` + `set_setting`.** Match the template to the fps **Resolve ingests the clips at** (`GetClipProperty('FPS')` after import), not ffprobe's `r_frame_rate`; iPhone VFR footage differs between the two (trap below).
2. `media_pool create_timeline_from_clips` with `clip_infos` = `{clip_id, start_frame, end_frame, record_frame}` in **SOURCE frames at the fps Resolve ingested the clip at** (`GetClipProperty('FPS')`; see the iPhone VFR trap in Project setup). `end_frame` is **EXCLUSIVE** (dur = end − start; matched a real EDL 8/8 to the frame). `record_frame` is timeline-relative. Linked audio comes along automatically.
3. Verify with `timeline get_items_in_track` readback: starts sit on the 108000 = 01:00:00:00 offset.
   **When clip fps ≠ timeline fps, `GetLeftOffset()` reads back in CONFORMED (timeline) frames while `start_frame` is consumed as NATIVE source frames**: a 29.97 clip on a 30 fps timeline reads back `native × 1.001`, which looks like a growing drift (up to 4 frames over 2.5 min) and is NOT one. Durations and `record_frame` read back exact, so verify those and don't "fix" the offsets. Resolve conforms by TIME, not 1:1 frames (measured: a 4612-native-frame span occupies 4616 timeline frames at 30 fps); that one probe settles the domain question in a single call.
4. `project_manager save` **immediately**. GUI mode + unsaved project = a modal no script can dismiss. (The `save` tool wrapper can return false while the raw call works; verify via `run_inline`, where `pm.SaveProject()` returns True.)

## Project setup: MATCH THE SOURCE FPS, and never ask for a click

**Step zero of every Resolve job: `ffprobe` the raw and read its real frame rate.** The project must match the footage: 24 fps source gets a 24 fps project, 30 gets 30. Do not assume, and do not default to whatever the last job used.

**ffprobe is only the first read: after import, `GetClipProperty('FPS')` on the clip is the authority (iPhone VFR trap, measured 2026-08-13, Resolve Studio 21.0.4.5, real job).** iPhone `.MOV` footage is variable frame rate: ffprobe's `r_frame_rate` reports `30000/1001` (29.97) while Resolve ingests the same clip at **30.00 native** (clip readback: 20218 frames over 673.92 s = 30.000 exactly; its duration timecode `00:11:13:28` only parses at 30). A template + EDL conversion built on the 29.97 reading conformed every clip ÷1.001 and placed every cut ~0.5 s early. So: import the media, read `GetClipProperty('FPS')`, and let THAT decide both the template (iPhone footage gets `1080p30.drp`, **not** `1080p2997.drp`) and the EDL seconds→source-frames math; if the template guess was wrong, delete the project and rebuild at the right rate. **Diagnostic signature:** a uniform ÷1.001 (or ×1.001) pattern across every item's duration/left-offset readback means the fps model is wrong: rebuild, never nudge individual frames. (The ffmpeg/flat-render path is unaffected: ffmpeg trims by time, so `splice.sh`'s frame-snap at the ffprobe rate stays correct there.)

**Then clone a template `.drp` at that fps. Do NOT use `create_project` + `set_setting`.** A new project defaults to 3840x2160 / **24 fps**, and `timelinePlaybackFrameRate` (a *separate* setting from `timelineFrameRate`) cannot be written by the API at all (`SetSetting` returns False for every value and type, on a fresh project and on one with a timeline; confirmed independently by `resolve_control api_truth`). A 30 fps timeline left playing back at 24 produces **chopped, glitchy audio**.

Importing a `.drp` restores fps + resolution wholesale, bypassing `SetSetting` entirely. Verified 2026-08-04: importing the 30 fps template while a 24 fps / 4K project was loaded still produced a 30/30/1920 project, so the settings genuinely ride in the file and do not leak from whatever is currently open.

```python
pm = resolve.GetProjectManager()
pm.SaveProject()                                     # outgoing project, or a GUI modal blocks everything
pm.ImportProject('workflows/resolve-templates/1080p30.drp', '<Project Name>')
pm.LoadProject('<Project Name>')
p = pm.GetCurrentProject(); mp = p.GetMediaPool(); root = mp.GetRootFolder()
mp.SetCurrentFolder(root)
tls = [p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount()+1)]
if tls: mp.DeleteTimelines(tls)                      # strip inherited content
if root.GetClipList(): mp.DeleteClips(root.GetClipList())
```

**Always read `timelinePlaybackFrameRate` AND `timelineFrameRate` back** before building the timeline.

**One template per frame rate: a template cannot be re-pitched** (once a project carries a playback fps, `timelineFrameRate` goes read-only too). But minting a template at ANY rate is **fully scripted, zero clicks** (2026-08-04): `python3 workflows/resolve-templates/mint-template.py 1080p30.drp <fps> <out.drp>`. The settings blob was cracked: SM_Config FieldsBlob = keyed-dict → zstd → protobuf, where f15 (varint, floor(fps)×2) is the timeline rate and **f248 (float32) is the "unwritable" playback rate**; exact 24 = both fields absent. Available now: 1080p30, 1080p2997 (both in [`workflows/resolve-templates/`](../../../workflows/resolve-templates/), details + verified enum table in its README). Always import + read back both fps keys before trusting a fresh mint. 24 fps needs no template (a stock `create_project` is already 24/24, just set the resolution).

## Vertical (9:16) framing

A clip dropped on a 1080×1920 timeline arrives LETTERBOXED (project Input Scaling defaults to fit, and that setting is UI-only from the API). The fix is one property write, resolution-agnostic, no math:

```
item.SetProperty('Scaling', 3)   # 3 = scale full frame with crop = FILL at Zoom 1.0
```

Values: 0 = fit, 1 = center-crop-at-native, 2 = fit, 3 = FILL. Zoom math (`tl_h / (tl_w * src_h / src_w)`) is quality-identical (Resolve concatenates sizing transforms and resamples once), so prefer Scaling=3 for simplicity. 16:9 → 9:16 is a ~1.78x upscale from a 1080p source, inherent to the crop; shoot 4K for vertical (downscale instead). `SetClipProperty('Super Scale', N)` takes **bare ints only** (1=off, 2=2x, 3=3x); every string form returns False.

**Mixed-resolution assets: let Resolve conform, NEVER hand-scale (2026-08-05).** The project setting `timelineInputResMismatchBehavior` defaults to `scaleToFit`, so a 1080p asset (title card, alpha overlay, older footage) already fills a 4K frame on drop. The Premiere habit (Motion Scale 200) doubles that to 400% and crops the middle out, plausibly enough to ship: a title card lost its first and last letters. Leave `ZoomX`/`ZoomY` at 1.0, check the setting before scaling anything, and verify with a real render (clip-level readback reports whatever zoom it was told and hides the crop). Upside of the same conform: mixed fps lands frame-for-frame (a 29.97 clip on a 30.000 timeline keeps its frame count), so frame-indexed graphics and same-rate overlays stay in sync with no re-render.

## What the API can do (all readback-verified)

- **Auto rough-cut in-app: `edit_engine plan_silence_ripple` → `execute_silence_ripple`.** Validated end to end (75 lifts, 548.5s → 397.4s, mirrored audio items, original timeline untouched: it assembles a named VARIANT). Also reports keep-ranges too short to dissolve. **This is the working cut path; never `apply_cuts` (below).** For frame-exact word-level cuts, the house WhisperX rough-cut still wins (see below).
- **Text-based editing, read half:** `timeline_ai create_subtitles` (GUI only, ~57s for 9 min) → `timeline get_transcript` → `timeline propose_cuts` (dry-run proposals with kind/span/confidence/rationale for stammers, repeats, long pauses).
- **Fusion node graphs from the API:** `fusion_comp` add_tool / connect / set_input / add_keyframe, plus `bulk_set_expressions` for procedural animation. Scope arg must be nested: `timeline_item: {track_type, track_index, item_index}`, NOT flat.
- **Custom GPU color shaders + multi-clip grading:** author a DCTL, put it on a **color group's post-clip node**, and every member clip inherits it. Full playbook + gotchas: [`workflows/resolve-grading/`](../../../workflows/resolve-grading/README.md) — read it before any grading work. Short version below.
- **Arbitrary Python inside Resolve:** `script_plugin run_inline` with `resolve` / `project` / `fusion` pre-bound. Hard 60s timeout; long ops go through the tool wrappers.
- **`timeline_versioning`** auto-archives before destructive ops (`<name>_archived_vNN` in Master/Archive) with rollback + diff. Rollback restores into a NEW `<name>_rolled_back_<hhmmss>` timeline.
- **Vision loop:** `media_analysis analyze_clip` extracts frames → Claude reads them → `commit_vision` writes Description/Comments/Keywords onto the clip + builds a SQLite FTS index.
- **Voice Isolation** writes at the TRACK level (`timeline set_voice_isolation_state`); the timeline_item version returns false.
- **Native render queue** (fast, in-app, no external encoder): `SelectAllFrames` must be a real bool; MarkIn/MarkOut are ABSOLUTE timeline frames (a 01:00:00:00 start means frame 86400 at 24 fps, not 0). **Before scripting a DELIVERY render, read [`workflows/resolve-export.md`](../../../workflows/resolve-export.md)** (measured 2026-08-06): `VideoQuality` is a dropdown INDEX, not a bitrate (50000 is silently ignored; 100 gives 1.1 Mbps), `MultiPassEncode` is the only real quality lever, multi-pass renders look FROZEN at a tiny file size while working fine, `GetRenderSettings` is not callable (verify with ffprobe on the finished file), and the Premiere CBR-50 lock does NOT port.
- **Frame QA per clip only:** `timeline_markers get_thumbnail_image` returns the CURRENT CLIP's graded frame inline (GUI + Color page only), NOT the program composite: over a graphics track it shows the overlay on black and proves nothing. Fine for a single-track frame check; compositing and multi-track grades need a real render.
- Bin organization (`folder` / `media_pool`), markers, color groups, layout + keyboard presets, project settings: all live.

## Graphics on the timeline (validated 2026-08-05, 9 overlays on V2)

- **HyperFrames alpha ProRes 4444 drops in with ZERO alpha config: Resolve auto-detects `Alpha mode: Straight`**, exactly what hyperframes writes. **NEVER premultiply a Resolve-bound render.** Premultiply is the CapCut lane's fix; here it would blow out every soft pixel (motion blur, glows, fades).
- Placement is `AppendToTimeline` with `clipInfo` `{mediaPoolItem, startFrame: 0, endFrame: <frame count>, recordFrame: 108000 + start, trackIndex: 2, mediaType: 1}`. `endFrame` is **EXCLUSIVE**, `recordFrame` is **ABSOLUTE**. Script it idempotent and readback-verified.
- **`TimelineItem` has NO keyframe API** (only static `SetProperty` plus the Fusion methods), so an animated footage move is a Fusion comp on the clip: `AddFusionComp` → `add_tool Transform` → connect MediaIn→Transform→MediaOut → `add_keyframe` on `Size` (verified interpolating: 1.0→1.07 reads 1.035 mid-clip).
- Resolve's embedded Python opens files as **ASCII**: `io.open(..., encoding='utf-8')` everywhere, and keep em dashes out of timeline names (either one kills the script).
- Verify compositing with a real render, never `get_thumbnail_image` (current clip's frame only, see above).

## Color grading (validated 2026-08-06, `your-job` intro: 9 clips, one shader)

Full playbook, reference shader and numpy previewer: [`workflows/resolve-grading/`](../../../workflows/resolve-grading/README.md).

**A COLOR GROUP is Resolve's adjustment layer, and it is fully scriptable.** The group API hangs off
`project`, not the media pool (`MediaPool` exposes zero group methods):

```python
project.AddColorGroup('Intro Pastel')
grp = [g for g in project.GetColorGroupsList() if g.GetName() == 'Intro Pastel'][0]
for it in items: it.AssignToColorGroup(grp)          # True per clip
grp.GetPostClipNodeGraph().SetLUT(1, 'MCP/look_v3.dctl')
```

Four levels: **Clip** (one clip) · **Group Pre-Clip** (all members, before each clip's grade) ·
**Group Post-Clip** (all members, after — put the shared look HERE) · **Timeline** (everything
including graphics tracks). A group covers only its members, so **overlays on V2 stay ungraded** —
covering them is the Timeline graph and a decision to confirm, never assume.

`Graph` has no AddNode, so a whole look goes in ONE node = a DCTL. Non-negotiables:

- **Write in Blackmagic's sample dialect** (`.../Developer/DaVinciCTL/`, `README.txt` = authoritative
  function list): `const float` locals inside `transform`, `_saturatef`, `_hypotf`, implicit
  int→float, no early returns, no scientific notation, every literal `f`-suffixed. Deviating cost
  two failed compiles; which construct Resolve rejected is still unknown (all were on the supported
  list, clang parsed them clean).
- **The DCTL error is a bare modal with NO diagnostic** — not in `ResolveDebug.txt` either. It is a
  pass/fail bit. `dctl validate` is a stub (`checker: minimal`) and returns valid for code Resolve
  rejects.
- **`dctl install` writes the USER LUT dir; `set_lut` stages a COPY into the master dir under
  `MCP/`. Re-installing does NOT re-stage** — Resolve keeps compiling the old file, readbacks report
  the new name, and the render comes back silently ungraded. Re-run `set_lut` after every edit and
  `diff` the two paths. Version the filename.
- **Hardcode constants; `DEFINE_UI_PARAMS` sliders only exist in the ResolveFX DCTL plugin**, not on
  a node LUT.
- **Measure, don't eyeball:** sample frames → mean/shadow/highlight/face/median-luma, design the look
  in numpy (`sim-grade.py`, ~1s per iteration vs ~1min per render), then port. The sim predicted the
  rendered result within .01 per channel.
- **Verify with a real render**, never a readback and never `get_thumbnail_image` (returns the
  current clip's frame, not the program composite). Check what's on screen at your sample timecode
  first — a sample that lands on a full-frame V2 graphic reads as a wildly broken grade.

### Do we still need WhisperX?

Yes, for the rough cut. Measured on the same clip: Resolve gives phrase-level cues (median ~1.9s / 6 words, timing only at cue edges, ~6x fewer anchors than WhisperX's per-word timestamps), and cue starts sit inside the very error band `refine-cuts.py` exists to fix. Keep the locked WhisperX rough-cut for cutting; Resolve's transcription is useful for long-form CC and machines without the venv.

## Audio pass: ffmpeg on the source files + `ReplaceClip`, NOT the API

**The scripting API has zero audio-effects surface in 21.0.3, and it is NOT a version thing, don't re-litigate.** No clip Volume/Pan (`SetProperty('Volume')` returns False on audio AND video items; the full property dump is transform/composite only), no track fader, no bus access, no FX insertion. The MCP's `timeline_item get_audio`/`set_audio` actions query keys Resolve doesn't have (all-null reads and False writes), don't trust the wrapper's advertisement. Independently corroborated 2026-08-04: (a) the 21.0.3 shipped scripting README documents no audio property keys at all; (b) the vendored repo's own `api_truth` DB tested `Volume|Level|Gain|AudioVolume` live on 21.0.0: all False, surface read-only ('Pan' misleadingly succeeds because it's the VIDEO transform key); (c) the upstream author's release probe hit the same wall (`vendor/davinci-resolve-mcp/docs/kernels/audio-fairlight-kernel.md`: "Volume write and restore return false") and ships `timeline probe_audio_item`/`safe_set_audio_properties` as guarded probes precisely because writes don't stick; (d) upstream HEAD (v2.75.0) contains no audio fix, so bumping the pin buys nothing. The repo's capability map lists Fairlight mix automation and plugin internals as unsupported by the public API, period. What DOES exist natively: track-level Voice Isolation, `resolve.GetFairlightPresets()` + `project.ApplyFairlightPresetToCurrentTimeline(name)` (presets are UI-authored only; none saved yet, effect untested), and GenerateSpeech.

**The standard final audio pass is [`workflows/resolve-audio-polish/`](../../../workflows/resolve-audio-polish/README.md), validated 2026-08-06 (9 sections, 210 clips, section spread 4.7 → 1.1 LU, zero clips moved). Read it before running one.** The shape: measure each SOURCE FILE with `ebur128` (gated, so dead air barely moves it) → static gain to −16 LUFS integrated, measured per file, never a flat house gain → `alimiter limit=0.891251` (−1 dBFS delivery ceiling, same `level=disabled:latency=1` locks) → aac 320k, video stream-copied, into `projects/<job>/audio-normalized/` → verify ZERO timing drift (duration, video/audio frame counts, audio start_time) → swap under the locked timeline with `replace-clips.py` (before/after track snapshot, REVERT.json, version the filename). The README also carries the traps this pass found: **`ReplaceClip` RENAMES the media pool item** (breaks every name-keyed script; strip `-vN` when matching) and **CLEARS the clip color label**; **retimed clips need their original level**, with protected ranges derived from the AUDIO items, not the video. Run it only after the edit is locked (never during a rough-cut handoff).

The earlier single-clip validation (2026-08-04, superseded for the final pass but still the mechanism proof): the house splice chain (`volume=<G>dB` + −6 dBFS `alimiter`, pcm_s24le into `audio/`) applied to the raw, then `MediaPoolItem.ReplaceClip('<abs path>')`. Verified live: video stream-copies (EDL stays frame-exact), all timeline items keep src_in/duration, and a second `ReplaceClip` back to the raw fully reverts. Its measured lesson stands: at +10 gain, 3.2% of speech windows took >2 dB of limiting (audible micro-ducks); +8 read clean. And put normalized files in `audio/` or `audio-normalized/`, never `raw/`: `transcribe.sh` globs `raw/*.mov` and would transcribe them as extra clips on a `--force` re-run.

**To READ an audio pass someone made by hand, bounce and measure; the state is unreadable.** `get_audio`/`get_property` return nulls on audio items, and a `.drp` export hides mix state in opaque zstd blobs (per-item `EffectFiltersBA` are byte-identical defaults regardless of the mix). Instead `render prepare_render_job` a throwaway 480x270 mp4 (a 55s timeline rendered in 2.2s) and `volumedetect` each segment against the same source range in the raw: a uniform peak ceiling across every segment plus a gain delta that shrinks as the source gets louder = gain-into-limiter, and the numbers tell you the settings. Gotcha: `ExportVideo: false` produces a job with an empty VideoCodec and `StartRendering` then just returns False: render tiny video, not none. Clean up with `delete_all_jobs` + re-set format/codec (`GetRenderSettings` is unavailable here, so the tool's "before" snapshot is empty; track what you changed yourself).

## Broken or dangerous: do not build on these

- **`timeline apply_cuts` DESTROYS the timeline while reporting success.** A "lift" deletes whole timeline ITEMS intersecting the span (it does not razor at boundaries); on a single-clip timeline the first lift deleted the entire clip, yet the tool reported `success: true, applied: 19`. Its claimed auto-archive did NOT happen (`_versioning.archived: false`). If it ever runs: never trust the applied count, read `results[].deleted` per cut, verify item counts after, and recover via `timeline_versioning rollback`. Use `execute_silence_ripple` or razor-based edits instead.
- **`SmartReframe`: the feature works, the API call does not.** The Inspector button fills the frame; the API call returns `success: true` and changes nothing, and there is no getter to even verify a UI reframe. Keep using `workflows/face-frame.py` for the measured 9:16 crop.
- `create_magic_mask` / `RegenerateMagicMask` return False in every mode, GUI included.
- `Stabilize` returns True but exposes no property to verify. Unverifiable through the API.
- `gallery_stills grab_and_export` **crashes the MCP server.** Use the two-step path: `timeline_ai grab_still` → `gallery_stills export_stills` (also drops a `.drx` of the grade).
- `Graph` has no AddNode: you can set LUTs/labels/enable on existing nodes but cannot create serial nodes. Workarounds: `ApplyGradeFromDRX` (a .drx carries a whole node tree, built once by hand or grabbed off a graded clip), a Fusion comp (`AddFusionComp` + `add_tool` — node creation IS exposed there), or fold the look into one DCTL.
- **`graph get_lut` reports the wrapper's own record, not Resolve's state (2026-08-06).** It returned a LUT name for a node where `GetLUT(1)` in-process read `None`; the matching `set_lut` had also reported success. Any grading readback must go through `script_plugin run_inline` against the real API objects, then be confirmed by a render.
- **`render start` returns `success: false` while the render runs fine.** `project.StartRendering([job_id])` returns `True` and produces the file — don't retry on the wrapper's false.
- `resolve_control` has **`open_page`, not `set_page`**; `resolve.RefreshLUTList()` doesn't exist (it's `project.RefreshLUTList()`).
- The scripting API cannot switch the Color page's node-graph level (Clip / Group Pre / Group Post / Timeline). Its whole UI surface is page switching + layout presets, so a session can build a group grade but cannot show it on screen — that dropdown is a hand-click.
- Bundled whisper.cpp transcription produced 0 segments; Resolve's own subtitle engine is the working path. Slate-clap sync detection false-positives on speech.

## Discipline

- **Target timelines by NAME, never `GetCurrentTimeline`,** whenever the user has the GUI open. They switch timelines while you work, and two writes have landed on the wrong timeline that way. Loop `GetTimelineByIndex` and match `GetName()`.
- **Read back after every write** (same rule as the Premiere bridge): property writes return success generously; the readback is the truth.
- Getting the cut onto the timeline is where the handoff ends unless asked for more. The user's own editing happens in the app.
