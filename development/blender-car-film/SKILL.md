---
name: blender-car-film
description: Make a short cinematic story film in Blender with Claude (about 20 seconds, several shots, a car, night, snow, sound and voice) - storyboard first, a real downloaded car model, a set Claude builds in Python, a live bridge so Claude drives the open Blender, hand-held cameras, snow particles, a render that went from a 5-8 hour estimate to about 1 hour, and a resumable overnight render queue. Use when someone wants a short film / car story / night or snow scene in Blender with Claude, or asks for any single step (live bridge, snow particles, render speed-up, render queue, grade).
---

# Short story film with Claude

The workflow behind "The Last Drive Home": a 20-second film about an old family car on a snowy night. It starts, drives past a
school and a hospital, parks at the house, the engine turns off and the porch light comes on. No people on screen. 6 shots,
2.39:1 widescreen, 600 frames at 30 fps. Every script in `scripts/` was actually run for that film, in order.

## Rules for Claude

- Storyboard first. Every shot gets its camera move, timing and sound before anything is built.
- Find a real model, don't build one: the car is a free CC BY model, trees, lamp, hydrant, fence, textures and sky are Poly Haven (CC0).
  Claude builds the simple things in Python: road, snow banks, school, hospital, house.
- Write your own code, read anything you download, ask before any long render.
- Never render inside the live Blender window (it crashes). Render in background Blender from a saved .blend.

## 0. Setup and the live bridge

- Blender 5.x (made on 5.2), an NVIDIA GPU (OptiX), Python 3, `ffmpeg`. Project folder `~/blender-car-film`.
- In Blender's Text Editor, open and run `tools/bridge.py`: a tiny listener on `127.0.0.1:9876` that runs the Python it receives on
  Blender's main thread and sends back the output.
- From a terminal: `python tools/send.py scripts/01_world.py`. Claude sends each script and sees the result live in your Blender.
- Send the numbered scripts in order in one Blender session: later scripts reuse helpers defined by earlier ones (`pbr()`, `col()`...).
- `scripts/dl_ph.py <folder>` downloads the Poly Haven assets the set uses.

## 1. Storyboard (`notes/PLAN.md`)

Ask Claude for a 20-second car story, 6 shots, no people. The real plan: wide low push-in on the parked car under a streetlight,
macro of the frosted headlight clicking on, the drive past the school and hospital, the house, engine off, porch light on.
Cold blue night, warm orange streetlight, warm porch light. Two short voice lines, sound effects ducked under the voice.

## 2. Build: the 17 scripts

| Script | What it does |
|---|---|
| `01_world.py` | fresh scene, world, ground, PBR material helper |
| `02_car.py` | imports the car model and scales it to its real length (4.5 m) |
| `03_rig.py` | wheel origins at their centre so they spin in place |
| `04_set.py` | street, lamps, hydrants, fence, school, hospital, signs, light helpers |
| `05_house.py` | the house, built in Python with real textures |
| `06_light_viewport.py` | autosave on, light viewport so the PC stays usable |
| `07_anim.py` | the drive from a speed profile, wheels roll by distance / radius, head and tail lights, porch light on at 17.5 s |
| `08_fx.py` | falling snow (pre-rolled so it is already falling at frame 1), a fog volume for light cones, exhaust steam while the engine runs, snow spray from the tyres |
| `09_cams.py` | 6 cameras with Shakify hand-held shake |
| `10_fix.py` | headlight spots at the real lamp positions, emissive lamp discs keyed with the lights |
| `11_fast_render.py` | the render speed-up (below) |
| `12_fixes.py` | snow visibility, fog banding (finer volume steps + dither), a too-dark interior shot, house shot blockers, road reads as packed snow |
| `13_speed_cine.py` | speed + cinematic pass: all cameras on the car's left side (180-degree rule), stronger depth of field on wides, faint cold moonlight rim |
| `14_comp.py` | compositor: lens look (the colour grade here was removed, it looked pinkish) |
| `15_grade_speed.py`, `16_grade_shot2.py` | grade: shadows neutral blue, highlights warm, never green |
| `17_fps30.py` | 24 -> 30 fps with frame mapping, so all keys stay in place |

`tools/preview.py` renders a quick still from any camera or position, `scripts/render_stills.py` renders the key stills.

## 3. Render: 5-8 hour estimate -> about 1 hour

- Adaptive sampling + OptiX AI denoise; 24-30 samples are enough at night.
- Fewer light bounces (it's night).
- **Bake the snow particles to disk once.** Without it every frame re-simulates the snow: 158 s -> about 6 s per frame.
- Camera and distance culling.
- 600 frames at 2560x1072, 30 fps, rendered in background Blender from the saved file.
- `tools/render_all.sh` renders every remaining shot one by one and encodes each shot and the full film. It is resumable: run it again
  after a power cut. `tools/progress.ps1` opens a progress window, `tools/stay_awake.ps1` keeps the PC awake until the film exists.
- `scripts/render_clay.py`: white clay breakdown render (EEVEE) for the "how it was made" part.

## 4. Sound

Sound effects, music and voice lines were generated with ElevenLabs (`scripts/gen_sfx.py`, needs your own `ELEVENLABS_API_KEY`).
`tools/mix.sh` builds the 20 s mix with ffmpeg: every sound with start time, volume, trim and fades, sound effects ducked under the voice.

## Lessons

- A Cycles emitter with `visible_camera = False` also hides its particles. Use `show_instancer_for_render = False` instead.
- Bake particle caches to disk, or every still re-simulates (100+ s a frame).
- Grade only where it helps. Green and purple casts look wrong immediately.
- Cost: about 20% of a weekly Claude limit (Opus, high effort) for the whole film.

## Start prompt

"Use the blender-car-film skill. Write a 20-second storyboard for [your story], 6 shots, no people on screen. For every shot give the
camera move, timing and the key sound. Use real downloaded models. Don't touch Blender until I approve it."

License: MIT. Made by Mr omi with Claude.
