---
name: blender-forest
description: Make an ultra-realistic 3D environment in Blender with Claude (a forest, a nature scene, a car driving through it) by following a long YouTube tutorial instead of writing a prompt - Claude watches the tutorial, writes the shot plan, checks the downloaded assets for anything unsafe, builds the world in stages with its own scatter system, rigs the car itself, measures the camera moves from the reference frames, benchmarks the render settings and renders overnight. Use when someone wants a realistic environment / forest / landscape / car-in-nature shot in Blender with Claude, wants to "recreate a tutorial scene", or asks for any single step (scatter, gravel path, car rig, render benchmark, clay preview).
---

# Ultra-realistic environment from a tutorial

The workflow behind a 13-second shot of a Porsche driving through a sunlit forest (2560x1440, 390 frames). The big idea:
**don't ask Claude for a scene. Give it a long tutorial and let it follow the tutorial step by step.** Claude writes the code and
places the cameras. The tutorial's free assets and open-source tools make the models. Every script in `scripts/` was actually run
for that shot. Names inside them (`forest.blend`, his material and collection names) come from that scene - rename them for yours.

## Rules for Claude

- Do not build 3D models or animation from scratch. Use the free assets that come with the tutorial, or open-source ones.
- You are good at code and cameras: scripts, scatter systems, camera moves, render settings. Do those.
- Write your own code. Do not install add-ons or run scripts you did not read. (The paid Geo-Scatter add-on and the Rig-A-Car add-on
  were both replaced by our own code.)
- After every stage, render a small test still and put it next to the reference frame. Fix what is off before moving on.
- Hand render-and-compare loops to a cheaper sub-agent (Sonnet) with a tight brief and read only its short report. Saves tokens.
- Tell me how long a render will take before you start it. Keep the PC usable: below-normal priority, 8 threads, texture limit 2048
  for tests.

## 0. Setup

- Blender 5.x (made on 5.2), an NVIDIA GPU (OptiX), Python 3, `ffmpeg`.
- Project folder `~/blender-forest` (the scripts use it as `ROOT`): `scene/forest.blend`, `assets/`, `research/`, `render/`.
- Background runs: `blender -b scene/forest.blend --python scripts/<script>.py`. For a live session, use the bridge from the
  `blender-film` skill (`tools/bridge.py` + `tools/send.py`).

## 1. Pick the tutorial

A long (1 h+) Blender environment tutorial that gives its assets away for free. Then say:
"Go watch his video. We are going to recreate his scene exactly as he did."

## 2. Claude watches it

- Download the transcript and read all of it.
- Capture the first 30 s at 30 fps, build contact sheets, detect the cuts (`notes/camera_moves.md` is what that analysis looks like).
- Write `PLAN.md`: every shot, its camera move and its length, plus the build stages (`notes/PLAN.md`).
- YouTube may block command-line downloaders with a bot check. Then grab frames and the transcript through the browser.

## 3. Assets and safety

- Download every asset, unpack each archive into its own folder. Run a virus scan on the downloads.
- List each archive for `.exe .bat .ps1 .py .dll` before unpacking.
- Open every .blend headless with `--disable-autoexec`. `scripts/audit_blend.py` counts embedded scripts, drivers and linked
  libraries: expect 0. `scripts/inspect_assets.py` lists what is inside, `scripts/check_missing.py` finds missing textures.
- Write the results to `SECURITY.md` (`notes/SECURITY.md` is the real one).

## 4. Build in stages

One script per stage, resumable, save the .blend after each. Rebuild order: `build_world` -> `scatter` -> `build_path`.

- `build_world.py`: terrain, ground material, HDRI world with a light-path split (the HDRI lights the scene at one strength and is
  seen by the camera at another), sun, colour management. His numbers where he gives them.
- `layout.py`: shared layout (clearing, where the path runs) that every later stage reads.
- `scatter.py`: our own Geometry Nodes scatter instead of a paid add-on. One layer table with his densities and scales.
  560k to 730k instances, built in about 15 s, because everything is an instance.
- `build_path.py`: gravel ribbon + pad from the layout spline, his gravel material with a cleaner wobbly middle band, a transparent
  edge fade into the ground, leaf litter riding on the path.
- `camset.py` places a look-dev camera from `CAM="x,y,height,yaw,pitch,lens"`; `test_still.py` renders a 960x540 still.
  32 samples is fine for layout, but the denoiser smears gravel: judge textures at 128 samples.

## 5. Pivot when something looks dull

The tutorial's cabins looked dull in our build, so we dropped them and switched to his car clip (19-32 s, 390 frames, 4 shots).
Same world, new target. Don't polish something that doesn't work.

## 6. The car

`build_car.py`: his Porsche model + **our own rig** instead of the add-on. The car follows the path, the wheels spin with the
distance travelled, the front wheels steer into the curve, the body bounces slightly. `car.json` holds the path and speed.
Part names the rig expects: `mycar_body`, `mycar_wheel.Ft.R`, `mycar_wheel.Ft.L`, `mycar_wheel.Bk.R`, `mycar_wheel.Bk.L`,
`mycar_wheelbrake.Ft.R`, `mycar_wheelbrake.Ft.L`, `mycar_wheelbrake.Bk.R`, `mycar_wheelbrake.Bk.L`.

## 7. The camera shots

- Capture every frame of the target clip. Have a sub-agent measure each shot: camera height, lens, fisheye, speed, cut times
  (`notes/clip-analysis.md` is the full measurement).
- `build_shots.py` builds every shot from `shots.json`: start and end camera, lens, f-stop, focus, easing, shake, and one sun
  angle per shot. The 4 shots: a slow truck through leaves, a locked wide with the car crossing, a camera rigid on the car's rear
  corner with a fisheye, a top-down follow.

## 8. Look pass

`look.py` is driven entirely by `look_params.json`: haze, sun dapples, depth of field, motion blur, colour, denser ground cover.
Change numbers in the JSON, not the script.

## 9. Render

- `bench.py` renders the same frames with different Cycles settings and times them. Result: **128 samples + OpenImageDenoise looks the
  same as 256 samples and is about 45% faster (51 s -> 28 s a frame).**
- Persistent data on, so the forest is built once and stays in GPU memory between frames.
- `render_final.py` / `render_final.cmd`: 2560x1440 PNG sequence, resumes after a power cut (empty placeholder frames are removed
  first). 390 frames took about 3 hours overnight.
- `watch_render.ps1` shows frames done, speed and time left. `stay_awake_encode.ps1` keeps the PC awake (no settings changed) and makes
  the MP4 at the end. `screen_guard.ps1` keeps the monitor off while nobody is using the PC.
- Preview first: `render_clay.py` renders a grey clay (Workbench) version of the whole clip in about 4 minutes. `preview.py` makes a
  fast low-quality animation preview to check timing and cuts.

## 10. Sound

The render is silent. Real recorded CC0 sound effects (BigSoundBank) sounded better than generated ones: ambience, the car passing,
onboard sound, whooshes. `gen_sfx.py` can generate effects with your own ElevenLabs key (`ELEVENLABS_API_KEY`) if you want that.

## Start prompt

"Go watch this video: [tutorial link]. We're going to recreate his scene exactly on my GPU. Capture the transcript and the first
30 seconds at 30 fps, write PLAN.md, then tell me which assets to download. Follow the rules in the blender-forest skill."

License: MIT. Made by Mr omi with Claude.
