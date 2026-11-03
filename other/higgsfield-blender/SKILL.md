---
name: higgsfield-blender
description: "Use when making a Blender video with Higgsfield. Claude → Higgsfield Bridge → Blender pipeline on this Mac — block a scene in Blender with the iCLONE hero, render the previz, generate the final video with Higgsfield (Seedance). Use whenever the owner mentions Higgsfield, Blender video/animation of the GLB model, previz/blocking, Seedance, \"Sample Project\", or asks for a video of the robot in a 3D world."
version: 1.0.0
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, Blender, 3D, Higgsfield, video]
    related_skills: [davinci-resolve]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos only. Needs `python3` on PATH, MCP server `higgsfield`, `/Applications/Blender.app`, `$VIDEO_ENGINE_DIR`.
> In this copy a folder of the owner's machine is written `<your project folder>` (in code, the `PROJECT_DIR` environment variable); folders of the owner's machine are environment variables the host sets: `VIDEO_ENGINE_DIR` (the video engine folder); a path into the owner's own folders is written `<your project folder>/…` (in shell code, `${PROJECT_DIR:?}`); the owner's own folder and project names are written `sample project` (in the case and joiner they had); the video engine is launched with its own `<launcher>.command`.

# Claude · Higgsfield · Blender

The 2026 loop (Higgsfield's own article, "This Blender + Higgsfield AI Workflow Changes How You
Make AI Video", @adilinthewild, 2026-08-28): **block the scene in 3D first, then generate.**
Claude builds the blocking in Blender through the Higgsfield Bridge; the viewport render of that
blocking drives a Seedance video-to-video pass that keeps camera, cuts and timing 1:1 and dresses
the world from image references. Not a single credit is spent before the shot is locked.

## The three pieces on this Mac 

| piece | where | state |
|---|---|---|
| Higgsfield Blender plugin 1.5.51 (Blender extension, GPL) | installed in Blender 5.1.2 as `bl_ext.user_default.higgsfield_blender`; source in `<your project folder>/sample-project/` | installed + enabled; **owner must Sign in** (View3D › N › Higgsfield) |
| Higgsfield MCP for Claude Code | `claude mcp get higgsfield` → `https://bridge.higgsfield.ai/mcp` (HTTP, OAuth via clerk.higgsfield.ai, PKCE, dynamic client reg.) | registered (user scope); **owner must authenticate** in an interactive `claude` session with `/mcp` |
| Sample Project engine (ours) | `$VIDEO_ENGINE_DIR/` | hero GLB → clips → world → camera → MP4, headless or from inside Blender |

Launch Blender with `$VIDEO_ENGINE_DIR/<launcher>.command` — same plugin, Amplitude
analytics off (empty `HIGGSFIELD_AMPLITUDE_API_KEY`), engine on `sys.path`.

How the bridge works: after sign-in the plugin opens a local exec socket on `127.0.0.1:9876`
(falls back to 9877–9879) and its `bridge_runner.py` connects OUT to
`wss://bridge.higgsfield.ai/plugin/ws` with the owner's OAuth token. Claude talks to
`bridge.higgsfield.ai/mcp`; the worker forwards each tool call to that Blender. **Blender must be
open and signed in**, otherwise the MCP tools answer "not connected".

Tools the plugin services (names on Claude's side are set by the worker; these are the wire
tools): `execute_python` / `bl_execute` (run bpy code, returns result/stdout/stderr),
`execute_script` (the worker's `bl_*` scene helpers), `search_api_docs`, `search_manual_docs`,
`get_python_api_docs`, `fnf_list_models`, `fnf_generate_image`, `fnf_generate_3d`,
`fnf_image_to_3d`, `fnf_job_status`, `fnf_import_motion`, `bl_install_py_addon`.
`fnf_*` tools **spend the owner's Higgsfield credits** — say what it costs and get a yes first.

Inside Blender the plugin also has: Image / Video / 3D Model catalogs, Extract Object from Image,
Environment (HDRI), Body → 3D, Realtime & Viewport prerender, Mesh & Materials (remesh /
retexture), Auto-Rig, Motion (text timeline → ARDY `kimodo` motion, retarget onto Mixamo rigs by
bone meaning), Phone camera (drive the scene camera from a phone by gyroscope), Supercomputer chat.

## The loop, step by step

1. **Block** in Blender (through the bridge, or with Sample Project). 24 fps, 1920×1080 (21:9 for
   dialogue), 30 s max. Proxies are fine — colour is identity (red/green/blue…), never animate
   what the generation will invent. Camera on rails, targets a null, accelerations and holds are
   the story. Save a backup `.blend` after every stage.
   *Our edge:* the hero is not a box. `Sample Project` puts the real rigged iCLONE (any GLB in
   `<your project folder>/Sample Project/assets/`) with real Mixamo clips into the blocking, so the previz already
   carries silhouette and motion.
2. **Render** the blocking: Viewport Render Animation, MPEG-4 H.264 (or `Sample Project` → EEVEE MP4).
3. **Generate** on Higgsfield with Seedance 2.5 video-to-video: attach the previz as `@Video`,
   the character/location sheets as `@Image`, and a prompt in this shape —
   `TITLE (duration, video-to-video)` · `ACTIVE REFERENCES` (what each @ defines and what is NOT
   inherited) · `LOOK` · `CAMERA — follow @Video 1:1, any deviation = failure` · `RULES` (counts,
   who is where) · `ACTION TIMING` (per-second beats) · `AUDIO` · `HOLD FOR THE FULL TIMELINE`.
   Off-screen voices stay off-screen; unresolved conflicts → the @Video wins.

## Sample Project quick reference

```
cd $VIDEO_ENGINE_DIR
./render.sh shots/kick_neon.json --preview          # 540p, a minute
./render.sh shots/kick_neon.json --still 40         # one PNG to judge the frame
./render.sh shots/kick_neon.json                     # 1080p MP4 → sample.project/
blender -b --python make_video.py -- --list          # the clip library (sample.project/)
```
Shot spec keys: `hero`, `height`, `keep_env`, `glow`, `world{preset: studio|neon|void|grid|flat,
accent, accent2, floor, bg, haze, hdri}`, `timeline[{clip, in_place, repeat, seconds, blend}]`
(`"own"` = the clip inside the GLB), `move{path, from, to}`, `camera{type: orbit|dolly|crane|
follow|static, frame: wide|full|medium|close, lens, fstop, start, sweep}`, `render{engine:
EEVEE|CYCLES, res, fps, quality: preview|final|ultra}`. From inside Blender (bridge or console):
`import sys; sys.path.insert(0, os.environ['VIDEO_ENGINE_DIR']); from engine import shot; shot.build(shot.load('shots/kick_neon.json'))`.

## Gotchas
- Blender 5.x: `action.fcurves` is gone → `action.layers[0].strips[0].channelbag(slot).fcurves`;
  NLA strips get `action_slot` automatically. Retarget = world-space Copy Rotation + hips Copy
  Location, then `bpy_extras.anim_utils.bake_action` (0.1 s for 41 bones).
- Shipped GLBs: rig at 0.01 scale, a stray `Icosphere`, the OpenSea backdrop field and SAMPLE PROJECT
  shells ride along — `stage.load_hero` strips them and normalises to 1.75 m.
- `sample.project/` and `sample.project/` are deliberate: Desktop is iCloud; `.nosync` folders never
  upload and never get evicted to dataless stubs (which hang Blender's importer).
- Plugin log: `~/Library/Logs/Higgsfield/Blender/blender.log`; auth: `~/Library/Application
  Support/Higgsfield/Blender/auth.json`. "Restart MCP" button in the plugin's MCP tab.
- Never type the owner's Higgsfield credentials; both sign-ins are theirs.

## First training run: use case 1 with our hero — what was learned
- Shot file: `shots/sample_project.json` (hero r0955, corridor preset, `Running` clip in place,
  root moved at the clip's own speed, `path` camera: follow → half-orbit → profile → top-down).
  Prompt: `shots/sample_project.prompt.md`. Hero sheet: `shots/hero_sheet_0955.json --still 1`.
- **Camera must stay inside the set.** A profile at radius 3.4 in a 3.6 m corridor and a top-down
  at 7.5 m under a 3.4 m ceiling both render black. Size the set (`width`, `height`) for the shot
  and use wider lenses (22 mm at 2.2 m = full body) instead of distance.
- **Clip speed decides the set length.** `Running` travels 5.7 m/s → 85 m in 15 s; the corridor
  was 60 m and the hero ran out of it. `move.speed: "clip"` keeps feet from sliding; the world
  must be as long as speed × seconds. The library has no plain `Walking` clip yet — download one
  from Mixamo into `sample.project/` for walks.
- The haze is a box; size it to the set (`haze(center, size)`), and keep density ≤ 0.01 when
  the set has dozens of lamps, or everything goes milky.
- Grid materials read Object coordinates: apply scale on scaled planes or one cell = the plane;
  and use FLOORED_MODULO — plain MODULO is negative for negative coordinates and lights half the plane.
- Blocking spec for the article's shot: 24 fps, 1920×1080, 15–30 s, one continuous camera; the
  generation prompt then lists ACTION TIMING per second matching the camera keys' `at` fractions.

## Building in the OPEN Blender (owner watches) — `engine/live.py`
- The plugin's local exec socket (127.0.0.1:9876, signed-in only) takes `{"type":"execute","code","strict_json"}`
  + `\0`. `live.run(code)` / `live.run_file(path, LIVE=True)`; the client purges `engine.*` from the live
  `sys.modules` first so edits land. Rendering stays headless (a render in the live window blocks the UI).
- The bridge sandbox blocks `wm.read_factory_settings` / `read_homefile` / `quit_blender`: build scripts
  use `stage.new_scene(fps, reset=False)` when LIVE (clears objects/orphans by hand, keeps the layout).
- **The owner's Blender UI is Portuguese: node names are localised.** Never `nodes["Background"]` —
  `stage.node(tree, "BACKGROUND")` (by type). Same for BSDF_PRINCIPLED / OUTPUT_MATERIAL / OUTPUT_WORLD.
- Headless runs must disable the extension first (`addon_disable('bl_ext.user_default.higgsfield_blender')`),
  or each render session registers it, refreshes catalogs with the token and bumps the live bridge (code 4000).
- Shipped GLB shells arrive animated by the file's own action (their own slots): `animation_data_clear()`
  on extras before keying them. Mixamo *Falling* drops the hips tens of metres inside the clip →
  `clips.load(..., pin_vertical=True)`.
- Irys film: `shots/sample_project.py` (+ `.md` storyboard, `.prompt.md`, `.refs.md`), hero =
  `<your project folder>`, sheets `hero_sheet_irys*.json`.
