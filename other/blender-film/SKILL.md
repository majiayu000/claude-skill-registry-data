---
name: blender-film
description: Make a short, realistic cinematic shot in Blender with Claude, start to finish - storyboard, city layout, a physics-driven flight path, a chase camera, a hero that moves like the real thing, a realism pass, night lighting that actually reads as night, handheld camera shake, sound designed from the 3D motion, an overnight render with automatic checks, and a "white clay build-up" reveal that proves it's real 3D. Use when someone wants a cinematic Blender shot / short film / drone or superhero flythrough made with Claude, asks to "do the whole workflow from the video", or wants any single step of it (physics path, night lighting, sound from motion, clay build-up).
---

# Blender film with Claude

The workflow behind a 10-second night FPV drone shot through a city: one storyboard, a real physics path, one pivot (the first hero
didn't work), night lighting, sound from the motion, a 3.5-hour render, and a clay build-up reveal. Every step below is a script in
`scripts/` that was actually run for that shot; names in them (`Drone Empty`, `Street Asphalt`, `Building_1`...) come from that
scene - rename them for yours.

## 0. Setup

- Blender 4.4+ (made on 5.2), a GPU for Cycles, Python 3 + `ffmpeg` on PATH (+ `numpy`, `scipy` for the sound step).
- **Live bridge** (Claude drives the open Blender, you watch): in Blender's Text Editor run `tools/bridge.py` (listens on
  127.0.0.1:9876). Then from a terminal: `python tools/send.py scripts/06_night.py` or `python tools/send.py -c "print(bpy.data.filepath)"`.
- Set `FILM_ROOT` to your project folder (default `~/blender-film`): `scene/`, `render/`, `audio/`, `research/` live there.
  `tools/lib.py` is loaded by every script (helpers: `coll()`, `save()`, `snap()`...).
- **Work on copies.** Before replaying or re-running any script that edits materials, copy the .blend - several passes are not
  idempotent if a run crashes halfway (re-running orphaned node links once).

## 1. Storyboard first

Ask Claude for a 10-second storyboard *before touching Blender*: shot list with timings, camera per shot, where the hero is, what
the viewer feels. Turn it into one image sheet (any image model) and keep it open - every later decision gets checked against it.

## 2. City

Use a city asset pack you own (buildings, roads, props) or free CC0 assets (Poly Haven). Have Claude lay out one avenue + one
intersection along +X from a top-view map (keep the hero's path clear of props), then dress it: cars (parked / moving / stopped),
lamps, trees, hydrants. Bake every external asset into the .blend.

## 3. Motion from physics, not hand-keyed curves

`scripts/01_swing_sim.py` simulates the move (gravity, air drag, a rope that can't stretch, web anchors from the storyboard) and
searches the anchor timings until the path threads the street. `02_path_empty.py` turns it into a path curve + an empty on
Follow Path with the offset keyed per frame (real speed, not linear). The hero is parented to the empty, the camera follows its
own path (`03_camera.py`, + `03b_camera_noise.py` for subtle shake).

## 4. The hero - and when to pivot

The first hero was a rigged Spider-Man animated with Mixamo clips. It failed: mocap is recorded on the ground, so in the air it
hung like a puppet, poses were stiff, and he was tiny in frame. **If the character with limbs looks wrong, swap the hero - keep the
city, camera and path.** Ask Claude for options (we got: hawk, supercar, fix by hand, FPV drone).

The FPV drone works because nothing can look stiff. `04_drone_attitude.py` flies it like a real quad:
- **attitude from physics**: thrust axis = acceleration + gravity, nose along velocity -> it tilts into speed-ups, banks hard in fast
  turns, flares nose-up when braking;
- **throttle cut where the path is ballistic** -> freestyle tricks layered on top: power flip, barrel roll, back flip;
- braking flare into a hover, then a slow yaw to stare at the lens; spinning props + cyan/magenta LED strips.

## 5. Realism pass (`05_realism.py`)

The tiny stuff nobody notices until it's missing: AgX exposure (no grade), a thin haze volume, asphalt with broken texture repeat,
wheel paths, an oil drip line down each lane, repair patches, worn paint, and dirt at the foot of every wall + faint run-off streaks.

## 6. Night that reads as night (`06_night.py`)

Rule: **at night the sky doesn't light the scene - practical lights do.** Dark gradient sky with city glow, LED street lamps,
lit windows, car head/tail lights, red traffic signals, blue-tinted fog with a touch of emission, wet asphalt with puddles.
- First attempt failed (orange fog everywhere, glowing blocks instead of windows).
- The fix: **the facade textures already know where the glass is** - glass is smooth, walls are rough. Use the roughness map as
  the window mask (`roughness < 0.3`), then light a random subset per window cell: warm, cool, off.

## 7. Camera like a real operator (`07_shakify_cams.py`)

Replace procedural noise with **Shakify** (free add-on with real recorded camera motion) on every shot camera. Add close shots:
a street-level camera ~0.45 m above the wet road, the drone dives at the lens and stops right in front of it.
`08_lens_look.py`: bloom around lights, slight barrel distortion + dispersion - no colour grade, the look is the lighting.

## 8. Sound designed from the motion

Free CC0 recordings (BigSoundBank: DJI drone, city at night, wet-road traffic, horns, distant siren, wind, rain on a puddle,
an air-conditioner). `11_motion_data.py` reads the animation per frame (drone distance / radial speed / side / throttle, nearby cars)
into `audio/motion.json`; `12_build_sfx.py` drives the mix from it:
- throttle -> motor RPM -> pitch; radial speed -> **Doppler** (pitch drops as it passes the lens); side -> equal-power pan;
- distance gain + air absorption, prop-wash bursts on throttle punches, spray when it hovers low over the wet road,
  the rooftop AC only on the roof shot, car pass-bys at their closest approach, street-canyon reverb;
- make two versions (calm night / full city chaos) and pick by ear. Calm won: let the hero be the star. Loudness -14 LUFS.

## 9. Render overnight - safely

- `09_render_opt.py`: remove hidden duplicate geometry (the tree asset carried extra copies), use a lighter LOD for anything far
  from every shot camera, GPU denoising. No visible change.
- Render **six test stills at final quality** first and check them.
- `10_render_edit.py` renders only the frames the edit uses (shot list = camera + frame range), resumable, and writes
  `render/status.json`; `tools/render_window.ps1` (Windows) shows a clean progress panel: %, time left, last finished frame.
- After the render: check every frame exists, no black/broken frames (brightness per frame, jumps only at planned cuts), sound
  matches the approved mix, loudness ready for YouTube. Only then encode + (if you asked for it) shut the PC down.

## 10. The clay build-up reveal (proof it's real 3D)

`13_aerial_cam.py` adds a high camera above the avenue. On a **fresh copy** of the scene, `14_clay_build.py` turns everything into
white clay, freezes the camera + traffic at one frame, and hides every piece until its turn, then drops it from the sky: cars first,
then buildings nearest the camera first, then the far city, then lamps and hydrants (~500 pieces). Each fall accelerates and
bounces a tiny bit on landing. `tools/clay_assemble.sh`: night | hard cut | clay build | one 0.25 s wipe | night, same camera,
same frame. Clay vs night split stills make great thumbnails.

## Lessons that cost time

- Screen recorders capture black if the window spec is wrong - check the first recorded frame before you walk away.
- Viewport recordings: Material Preview needs motion blur off and volumes unlinked or it smears; Cycles viewport needs a denoiser.
- Relative output paths in `blender -b` resolve to the drive root - always pass absolute paths.
- Ask before any long GPU job; test at low quality first, final quality last.

License: MIT. Made by Mr omi with Claude.
