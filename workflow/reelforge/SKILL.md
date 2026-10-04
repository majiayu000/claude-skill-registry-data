---
name: reelforge
description: Create videos, animations and motion graphics as MP4/GIF with synced music - YouTube Shorts / Reels / TikTok, animated word-by-word captions, kinetic typography, logo reveals, intros/outros, promo and explainer videos, animated charts and data stories, 3D shader loops, particle effects, music visualizers and showreels. GPU-rendered from Python + GLSL with real motion blur, bloom, beat-synced cuts and an original generated soundtrack (or the user's own music). Use whenever the user asks to make, generate, animate or render a video, animation, motion graphic, intro, GIF or short-form clip.
---

# ReelForge - motion graphics & video, rendered in code

You write a small Python file (scenes = pure functions of time), ReelForge renders it on the GPU with
motion blur, HDR bloom, filmic tonemapping and a beat-locked soundtrack, and you **look at the frames
before you ship**. Skill folder: `${CLAUDE_SKILL_DIR}`. If that variable was not expanded, the skill folder is
the directory containing this SKILL.md. Inside it: engine `reelforge/`, CLI `scripts/rf.py`, starters `templates/`.

## Workflow (follow in order)

1. **Doctor (once per machine):** `python ${CLAUDE_SKILL_DIR}/scripts/rf.py doctor`.
   Fix every FAIL before writing code (missing pip packages -> run the printed pip command).
2. **Storyboard in chat first.** Pick BPM (default 120 -> 1 beat = 0.5 s, 1 bar = 2 s) and write a table:
   `time | bar | shot | what moves | transition`. Cut on bars/beats. One idea per shot. Keep total length
   a whole number of bars. Pick one palette (`PALETTES`) and at most 2 fonts.
3. **Start from the closest template** (`rf.py templates`, `rf.py new <name> my_video.py`) and edit it,
   or write a new file with the same header. Templates: `kinetic_type`, `shorts_captions` (9:16),
   `logo_reveal`, `data_story`, `neon_loop` (seamless 3D loop).
4. **Write scenes as pure functions of time** - `render(self, eng, t, fb)` must not keep state between
   calls. Randomness = hash of an index, never `random()`. This is what makes motion blur, stills,
   chunked renders and montages work.
5. **LOOK - mandatory, you cannot watch video:**
   - `python my_video.py stills 0.5 2 4.2 ...` (a few per shot, incl. just after each transition), then
     **Read the PNGs** and critique: legibility, overlap, framing, contrast, anything off-screen.
   - `python my_video.py contact --every 0.5` and Read the sheet(s): pacing, dead/black/blown sections.
   - `python my_video.py check`: automatic black / blown-out / frozen-frame + audio-level report.
   Fix and repeat until it looks intentional. Never render the final before this passes.
6. **Render:** `python my_video.py render` (auto-chunked and resumable for > 20 s; each chunk is a
   separate process, so a crash only re-renders that chunk). Long renders: run in the background and wait.
7. **Verify the delivered file, then deliver:** `render` finishes with `verify`, which checks frame count and audio
   in the MP4 itself and writes `<name>_verify.png` (frames decoded from the file). **Read that PNG.** It proves
   the file holds the new edit. Report path, duration, resolution, fps. Offer `gif` and `audio`.

## Hard rules (each one prevents a real, silent failure)

- Colours are **linear** RGB (`lin(0xff5a1f)`, `PALETTES[...]`); the pipeline sRGB-encodes once at the end.
  Values > 1.0 are HDR and bloom - use 1.5-4x for neon/glow, keep text at ~1.0-1.2.
- Coordinates: origin centre, y up, **frame height = 1.0**, x in `[-aspect/2, +aspect/2]`
  (16:9 -> +-0.889, 9:16 -> +-0.281). Text `size` = cap height in these units. Use `eng.text.fit(...)`
  for any text whose length can vary - 9:16 frames are narrow.
- Every `eng.shapes.*` call is queued: call `eng.shapes.flush(fb)` before drawing text that must sit on top.
- Put internal hard cuts in `Scene.cuts` (local seconds) so motion blur never double-exposes across a cut.
- Keep per-pixel shader loops bounded (<= ~128 raymarch steps); a GPU draw over ~2 s triggers a driver reset.
- Don't import `random`/`time` inside scenes; don't read files per frame (load in `setup(self, eng)`).
- Music: `proj.music_score(...)` (original, royalty-free, arranged to your sections) or
  `proj.music_file("song.mp3")` (tempo + beats detected; use `proj.beat(n)` / `proj.bar(n)` for cut times).
  Put the biggest visual moment on the first `"drop"` bar.

## Craft checklist (what separates "AI slop" from motion design)

Ease everything (`ease_out_expo` for entrances, `ease_in_cubic` for exits, `ease_out_back` for pops) ·
stagger letters/items 30-60 ms · anticipation before big moves, overshoot + settle after · hold important
text >= 1 s per 3 words · secondary motion so no frame is frozen (drift, breathing, parallax) · beat-sync:
`eng.common["uKick"]` (0-1 envelope) for pulses, `Scene.shake()` for impacts · consistent palette,
2 fonts max, high contrast, 5% safe margin (9:16: keep captions out of the bottom 20% and top 12%).

## References (read when needed)

- [reference/api.md](reference/api.md) - Project / Scene / text / shapes / shaders / audio / CLI
- [reference/cookbook.md](reference/cookbook.md) - copy-paste recipes: backgrounds, glow, SDF morph,
  raymarching, GPU particles, captions, charts, montage, loops, transitions, lower thirds
- [reference/motion-principles.md](reference/motion-principles.md) - timing numbers, platform specs, typography
- [reference/troubleshooting.md](reference/troubleshooting.md) - black frames, wrong GPU, OOM, colour shifts, fonts
