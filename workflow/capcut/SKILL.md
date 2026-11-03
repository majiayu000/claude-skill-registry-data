---
name: capcut
description: "Finish a job inside CapCut — the CapCut-user counterpart to premiere-pro (editing apps are the primary path; Premiere is your default, CapCut is for CapCut-user clients). Builds a real CapCut draft from the EDL (one trimmable clip per cut), then drives the running app live to place graphics, edit, and export — CapCut has no API, so this is the only way to script it. Triggers: send to capcut, open in capcut, finish in capcut, hand off to capcut, edit this in capcut, build a capcut draft, export from capcut, take it into capcut."
---

> **Video Studio:** this skill lives in `engines/legacy-editor`. Before running anything from it, `cd engines/legacy-editor` and use that folder's copy (`engines/legacy-editor/.claude/skills/capcut/`), which has its scripts and reference files. Every path below is relative to `engines/legacy-editor`. This copy only lets Claude find the skill from the Video Studio folder.


# To CapCut — Rough Cut Handoff + Live Driving

The CapCut twin of [`premiere-pro`](../premiere-pro/SKILL.md). **Editing apps are the primary finishing path — this is not an "off-ramp."** Premiere is your default app; **CapCut is the lane for CapCut-user clients.** After the rough cut (pipeline step 2), rebuild the cut on a CapCut timeline and do the work there — this skill can carry it all the way to an exported file.

Everything runs through one script: **`workflows/capcut-bridge.py`** (macOS only, self-contained `uv` header — no venv). Run `uv run workflows/capcut-bridge.py` with no args to print the full command list.

## Why this is different from every CapCut MCP

CapCut has **no API of any kind** (researched exhaustively 2026-07-27 — see Lab Notes). Every "CapCut MCP" on the market blind-writes a draft file and stops there. This bridge does both halves for real:

- **File lane** — writes/edits the plaintext draft JSON CapCut stores under `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`. Structural, batchable, exact. Requires the app be **quit** during the write (it rewrites its draft registry on exit); the bridge quits + relaunches around each write.
- **Live lane** — drives the *running* app through ByteDance's own internal automation IDs, exposed in the macOS accessibility tree. Find element by name → click its center with a synthesized event → **read state back**. A true locate-act-verify loop, no restart.

**This drives the real desktop app: it takes over mouse, keyboard, and window focus for a few seconds per live action.** Warn before starting a live-lane run if the machine is in use (file-lane writes only need the app quit, no screen takeover). AX ids are internal test hooks, **not a contract** — if anything stops responding after a CapCut update, re-map with `dump` before assuming the bridge broke.

⚠️ **The ruler has a dead strip about 90px wide at its left edge** that silently eats clicks (measured at two zoom levels, fixed in screen space), so the first few seconds of the timeline can't be clicked to directly. `seek` handles it — it lands where it can, then closes the gap with arrow-key frame steps. Those steps must be **paced**: sent back to back CapCut drops most of them (195 sent, 28 applied). `key <k> --times N` paces them for you. Two other focus rules: synthesized input only reaches CapCut when it's frontmost (the bridge activates it before every click and key — when it wasn't, the *first* click was consumed activating the window, which is what made `calibrate` fit garbage), and arrow keys only reach the timeline after something in the timeline has been clicked.

⚠️ **Check for a coach-mark before trusting any live action.** CapCut pops yellow onboarding tooltips ("Right-click the keyframe to create variable speed animations", etc.) that sit *over* the UI and silently swallow clicks in that region — they do **not** appear in the AX tree, so `dump` looks clean and every command reports success while doing nothing. One parked over the left end of the ruler broke `seek` for half an hour: clicks near t=0 vanished, `calibrate` fitted garbage from the one point that did land, and the playhead ended up 40s from target. **If a live action reports success but the state didn't change, `shot` the window and look for a yellow bubble**, then dismiss it with an offset click on its OK. Worth a `shot` at the top of any live session.

## When to use
- Any trigger phrase above, OR a rough cut exists and the job should finish/export in CapCut rather than HyperFrames or Premiere, OR it's a deliverable for a client who edits in CapCut.

If there's no rough cut yet, run `rough-cut` first **with `RENDER=0` on the splice** — same as the Premiere path, the EDL + canonical transcript generate in ~8s with no flat render, and `replay` consumes nothing else. Never render a flat MP4 for a CapCut-finish job.

## The two lanes — pick per action, don't mode-switch up front

| Need | Lane | Restart? |
|---|---|---|
| Build the rough cut from the EDL | file (`replay`) | no — a fresh draft has no cache yet |
| Place graphics / text / transforms in bulk | file (`add-overlay`, `add-text`, `transform`, `remove`, `graphics`) | yes — quits + relaunches (the bridge does it) |
| Interactive trim / split / delete / seek | live (`seek`, `split`, `delete`, `undo`, …) | no |
| Export the finished video | live (`export`) | no |

**Golden rule (learned the hard way, 2026-07-27):** once a draft has been hand-edited in the app, file-lane commands **additive-edit the current `draft_info.json`** — those edits are saved into it on quit. Never regenerate from the EDL over that work; a rebuild clobbered a hand-extended segment. `replay` is for a *fresh* draft only; `add-*`/`transform`/`remove` build on whatever's there.

## Procedure — build → edit → export

1. **Resolve the job.** Newest folder under `projects/` unless one was named. The EDL is `projects/<job>/transcript/cuts.json`; the raw clips are in `projects/<job>/raw/`. Both must exist (same requirement as the Premiere replay).

2. **Build the rough cut:**
   ```
   uv run workflows/capcut-bridge.py replay <job> [--name <draft>]
   ```
   Writes a whole draft from the EDL — one timeline segment per cut, source times in microseconds, butt-joined so each cut lands where the EDL says (verified 10/10 exact on the intro, zero drift). Draft name defaults to the job name. The raw is **hardlinked** into `<draft>/Resources/` because CapCut's sandbox (`assets.movies.read-write` only) can't read repo paths — a path outside `~/Movies` opens as a red "File not accessible" timeline. `replay` relaunches CapCut when done.

3. **Open it and confirm:**
   ```
   uv run workflows/capcut-bridge.py open <draft>
   uv run workflows/capcut-bridge.py state --draft <draft>   # JSON snapshot: tracks, exact seg times, unsaved-edit flag
   ```
   `state` reads exact times from disk and compares the live clip count against the saved draft, so it flags unsaved changes.

4. **Place graphics (file lane, batched).** Alpha HyperFrames movs and text both work:
   ```
   uv run workflows/capcut-bridge.py add-overlay <draft> <path/to/graphic.mov> --at 1.0 [--layer 1] [--dur 3]
   uv run workflows/capcut-bridge.py add-text   <draft> "built by claude" --at 20 --dur 3
   uv run workflows/capcut-bridge.py transform  <draft> --track overlay --index 0 --scale 0.6 --y -0.25
   uv run workflows/capcut-bridge.py remove     <draft> --track text --index 1
   ```
   - **Overlay** = a second video track (`flag: 2`, `render_index` 1). ProRes 4444 alpha composites with true transparency (validated on `g1txt.mov`). `--layer N` stacks higher.
   - **PREMULTIPLY every CapCut-bound alpha mov first.** CapCut composites ProRes 4444 assuming PREMULTIPLIED alpha; hyperframes renders STRAIGHT. Where alpha is 255 the two are identical, which is why solid type (the `g1txt` validation) looked perfect, but every semi-transparent pixel (motion blur, glows, soft shadows, letter fades) composites as `RGB + (1-a)*bg` and blows out to white; motion-blur trails become fat white blobs. Convert before `add-overlay`: `ffmpeg -i in.mov -vf "format=rgba64le,premultiply=inplace=1,format=yuva444p10le" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le out.mov` (working script: `projects/your-job/hf-graphics/render-title.sh`). Premiere AND Resolve both assume STRAIGHT (Resolve auto-detects it), so never premultiply a render bound for either — this fix is CapCut-only.
   - **Text** = a text track (`flag: 1`), built from a template lifted from a real draft (`workflows/capcut-templates/`). The style run is re-pointed at the new string automatically.
   - **transform** — exact scale/position/rotation/opacity written straight into the draft. Position is canvas-normalized (`--y -0.25` shifts up a quarter-frame). This is file-lane on purpose: the inspector's on-screen fields take focus but **ignore synthesized keystrokes**, so the JSON is both the precise and the only reliable path.
   - **graphics** `<draft> <job>` places a whole `graphics-plan.json` in one cache cycle. `--force` on `add-*` allows a deliberate duplicate (there's a guard against an interrupted run double-applying).
   - Batch related edits into **one** invocation where you can — each file-lane command is one quit+relaunch cycle (~15s).

   **Z-order is TRACK stacking, not segment `render_index`.** A segment's `render_index` only orders it *within* its track; what composites is the track's position (`track_render_index` / array order). So `--layer N` is the real z control, and a **text track can't be pushed below a video layer** — CapCut keeps text on top. Type that has to sit *behind* something gets baked to an alpha mov and placed as a video overlay.

5. **Background removal (text-behind-subject, validated 2026-07-27).** Cutout is a live-lane click; the matte itself is CapCut's own AI (needs Pro). The layered build, bottom to top:

   | Layer | What | How |
   |---|---|---|
   | main | the cut, untouched | already there |
   | 1 | black clip, opacity = "background darkness" | `add-overlay <black.mp4> --layer 1` + `transform --opacity 0.3` |
   | 2 | the title, baked alpha ProRes | `add-overlay <title.mov> --layer 2` |
   | 3 | duplicate of the same footage, background removed | `add-overlay <raw> --layer 3 --src <source in-point> --mute --force` |

   `--src` re-lays a slice of the raw above the main track; `--mute` is **mandatory** on that duplicate or its audio doubles the voice. Then enable the matte on the top clip:
   ```
   uv run workflows/capcut-bridge.py select 0
   uv run workflows/capcut-bridge.py click "VESettingPanelSubTabControl:Remove BG"
   uv run workflows/capcut-bridge.py clickxy 2976 286      # the Auto removal checkbox
   ```
   The checkbox is the left edge of `automationaiMattingGroup` — an offset click, like the export dialog (the row exposes no AX child). It writes `matting.flag: 3` plus a mask cache under `<draft>/matting/<hash>/`, keyed on the media, so a second clip off the same raw computes fast. Give it ~20s, then `seek` somewhere else and back to force the preview to re-render.

   **QA gotcha that costs an hour if you miss it:** the top layer is the *same footage* as the main track, so before the matte lands it covers the whole frame — the dim and the title below look like they aren't rendering at all. Don't debug the lower layers off that; confirm with `matting.flag == 3` in the draft JSON, or `delete` the top clip and look.

6. **Motion keyframes — zooms, pushes, moves (validated 2026-07-27).** Same expressive range as Premiere's Effect Controls, and easier to hit exactly, because the values are written rather than typed into a UI:
   ```
   uv run workflows/capcut-bridge.py keyframe <draft> --track overlay --index 2 --at 0   --scale 1.0
   uv run workflows/capcut-bridge.py keyframe <draft> --track overlay --index 2 --at 2.0 --scale 1.09
   uv run workflows/capcut-bridge.py clear-keyframes <draft> --track overlay --index 2
   ```
   Animatable: `--scale` (writes ScaleX+ScaleY together), `--x`, `--y` (canvas-normalized), `--rotate`, `--opacity`. Two calls = a ramp; more calls = a multi-beat move. `--at` is **timeline** seconds and must land inside the segment (the bridge converts to the segment-relative `time_offset` CapCut stores). Re-keying the same time replaces that point.

   Under the hood it's `common_keyframes` on the segment: one entry per `property_type` (`KFTypeScaleX`, `KFTypePositionY`, `KFTypeRotation`, `KFTypeAlpha`, …), each holding a `keyframe_list` of `{time_offset µs, values: [v], curveType}`.

   ⚠️ **`time_offset` is in the SOURCE time domain, not segment-relative** — a point is `source_timerange.start + (t − target start)`. This is the single thing to get right, and it fails silently: segment-relative offsets fall outside a cut's source window and CapCut collapses the whole animation to **one static value** rather than erroring, so the clip looks zoomed but never moves. It also hides during testing — probe on a clip whose source in-point is 0 and the two domains are identical. Verify on a real cut, and verify by parking the playhead *between* two keyframes and reading the inspector: an interpolated value (100 → **112** → 122) is proof; matching the last keyframe means it flattened.

   **Only `curveType: "Line"` (linear) is verified** — `--curve` passes a value through, but the app's ease-curve names haven't been probed, so anything else is a guess. For an eased move, stack extra keyframes instead.

   Keyframing the cutout layer *alone* pushes the subject while the background holds still — a real parallax move, and the reason to keep the cutout as its own layer.

7. **Interactive edits (live lane, no restart)** — for the surgical stuff:
   ```
   uv run workflows/capcut-bridge.py seek 42.0 --draft <draft>   # frame-exact, closed-loop
   uv run workflows/capcut-bridge.py split 30.0                  # razor at a time (or at the playhead)
   uv run workflows/capcut-bridge.py delete 3                    # select clip 3 + delete
   uv run workflows/capcut-bridge.py undo | redo | marker | zoomfit | play | playhead | clips
   ```
   `seek` clicks the mapped ruler point then nudges with arrow keys until the app's own `currentProgress` readout hits the exact frame — it **self-calibrates** from that readout, so it survives any zoom/scroll state.

8. **Export (validated end-to-end 2026-07-27):**
   ```
   uv run workflows/capcut-bridge.py export [--to <dir>] [--timeout 400]
   ```
   Drives CapCut's real export dialog and **verifies the file that lands** (defaults: 1080p HEVC mp4 into `~/Downloads`, the draft name). Proven raw EDL → alpha overlay + programmatic text → rendered file with both graphics baked in (confirmed by frame-grab). Leaves cloud-sync off. Screen is controlled for ~10s (escape stale modal → Export → confirm), then it's pure file-polling while CapCut renders — the machine is free during the render.

## Lab-Notes locks — read before trusting any step

The full war stories live in the root `CLAUDE.md` **"CapCut lane"** Lab Note. The ones that bite:

- **`Timelines/` cache.** CapCut imports `draft_info.json` only on a draft's **first** open, then builds native state in `<draft>/Timelines/` and trusts *that* forever — later JSON edits are silently ignored. `edit_draft` handles it (wipes `Timelines/` + the `.bak` to force re-import); if you ever hand-edit a draft's JSON some other way, do the same or the change vanishes.
- **`source_timerange: null` WEDGES the encoder** mid-render (froze at exactly the offending segment, twice — cost an afternoon). CapCut writes null there for text segments internally; it survives a file-lane rewrite into the re-imported draft. `edit_draft` now backfills every null source range before writing. A wedged export needs `kill -9` (the modal blocks a graceful quit) + `Timelines/` delete before relaunch.
- **The post-export share screen is MODAL** and blocks the next export — the bridge escapes it before and after. **Never click through it: it publishes to TikTok/YouTube.**
- **Keystrokes only reach CapCut when it's frontmost** — the bridge activates the app before any key (`ensure_front`). Clicks are positional and don't need it.
- **Import re-quantizes cuts to the 30fps timeline grid** (≤17ms/cut vs the 23.976-snapped EDL). Acceptable for this lane; don't fight it.
- **No real API is buildable.** CDP via `--remote-debugging-port` works but the editor is native QML (CEF sees no timeline); dylib injection is technically open but means reversing a 655MB stripped engine that breaks every auto-update. The live AX lane is the answer.

## Relationship to the rest of the repo
- **Premiere** stays your finishing surface ([`premiere-pro`](../premiere-pro/SKILL.md)); both ship. Route to CapCut only on an explicit CapCut ask or a CapCut-user client deliverable.
- The bridge consumes the same `transcript/cuts.json` EDL the Premiere replay does — one rough cut feeds either app.
- Ships in the client package as the CapCut-user client lane (macOS only — the bridge is macOS desktop automation, so it's dormant on Windows/Linux installs).
